"""Development contract regressions. Hand-authored outputs test code, not LLM skill."""
import copy
import json
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path
from unittest.mock import patch

from kiodai_v2.agent import Agent
from kiodai_v2.common import citations_valid, parse, rows, validate
from kiodai_v2.contract import EXTRACTION, obligation_sources_valid
from kiodai_v2.fixture import record
from kiodai_v2.gateway import Gateway, Accounting
from kiodai_v2.store import Store
from research_harness.model_gateway import MockTransport, RunStopped

ROOT = Path(__file__).resolve().parents[1]
FAILED = json.loads((ROOT/'tests/fixtures/v21_failed_smoke_minimized.json').read_text())['traces']


def frame(observations, checkpoint=1, handles=None):
    return {'checkpoint': checkpoint, 'messages': [{'role': 'system', 'content': 'Public fixture.'}],
            'observations': observations, 'current_refs': [k for k, v in observations.items() if v['checkpoint'] == checkpoint],
            'channels': ['queue'], 'handles': handles or ['h7'], 'menu': {h: 'File the amber tray.' for h in handles or ['h7']},
            'receipts': []}


class ExtractionContractTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.store = Store(self.root/'store.sqlite')
        self.addCleanup(self.store.close)
        self.config = json.loads((ROOT/'configs/v21_deepseek_smoke_v1.json').read_text())
        self.text = 'Please file the amber tray when queue reports "Ready".'
        self.obs = {'mA': {'text': self.text, 'kind': 'visible', 'checkpoint': 1}}
        self.rec = record('File the amber tray.', 'hidden', 'Ready', 'queue', None, self.text, 'mA')
        self.op = dict(kind='create', target=None, expected_version=None, record=self.rec,
                       sources=[{'ref': 'mA', 'quote': self.text}])

    def apply(self, operations, obs=None):
        return self.store.apply({'operations': operations}, self.obs if obs is None else obs, 1, ['queue'])

    def snapshot(self):
        return (self.store.records(), self.store.db.execute('SELECT * FROM events').fetchall())

    def second_obligation(self):
        text = 'After "File the amber tray." succeeds, notify the clerk when queue reports "Ready".'
        self.obs['mB'] = {'text': text, 'kind': 'visible', 'checkpoint': 1}
        return {**self.op, 'record': record('Notify the clerk.', 'hidden', 'Ready', 'queue', None, text, 'mB'),
                'sources': [{'ref': 'mB', 'quote': text}]}

    def agent(self, outputs, method='A2', name='agent', accounting=None):
        gateway = Gateway(MockTransport([json.dumps(x) if not isinstance(x, Exception) else x for x in outputs]),
                          self.config, self.root/(name+'.jsonl'), 'MOCK', accounting)
        agent = Agent(method, self.root/(name+'.sqlite'), gateway)
        self.addCleanup(agent.store.close)
        return agent

    def test_saved_empty_condition_reproduces_old_gap_and_new_rejection(self):
        trace = FAILED[0]
        validate(trace['output'], trace['schema'])  # Actual provider-facing v2 schema accepted it.
        self.assertEqual(trace['validation_error'], 'ValueError: Missing intention content')
        with self.assertRaisesRegex(ValueError, 'condition'):
            parse(json.dumps(trace['output']), EXTRACTION)
        with self.assertRaisesRegex(ValueError, 'condition'):
            self.apply(trace['output']['operations'], trace['context']['observations'])
        self.assertEqual(self.snapshot(), ({}, []))

    def test_missing_null_empty_whitespace_conditions_by_trigger(self):
        for trigger in ('time', 'event', 'hidden', 'unknown'):
            for value in ('MISSING', None, '', ' \t\n'):
                op = copy.deepcopy(self.op)
                op['record'].update(trigger=trigger, channel='queue' if trigger == 'hidden' else None,
                                    when='Tuesday 14:20' if trigger == 'time' else None)
                if value == 'MISSING':
                    del op['record']['condition']
                else:
                    op['record']['condition'] = value
                with self.subTest(trigger=trigger, value=value):
                    if value is None and trigger in ('time', 'unknown'):
                        validate({'operations': [op]}, EXTRACTION)
                    else:
                        with self.assertRaises(ValueError):
                            validate({'operations': [op]}, EXTRACTION)

    def test_valid_trigger_variants_and_unknown_cannot_act(self):
        descriptions = [
            ('time', None, None, 'Tuesday 14:20', 'At 14:20 on Tuesday, file the tray.'),
            ('event', 'approval arrives', None, None, 'File the tray when approval arrives.'),
            ('hidden', 'Ready', 'queue', None, self.text),
            ('unknown', None, None, None, 'Please file the tray later; timing is unspecified.'),
        ]
        for i, (trigger, condition, channel, when, text) in enumerate(descriptions):
            ref = f's{i}'
            obs = {ref: {'text': text, 'kind': 'visible', 'checkpoint': 1}}
            op = {**self.op, 'sources': [{'ref': ref, 'quote': text}],
                  'record': record('File the tray.', trigger, condition, channel, when, text, ref)}
            self.apply([op], obs)
        records = self.store.records()
        self.assertEqual(len(records), 4)
        unknown = next(v for v in records.values() if v['trigger'] == 'unknown')
        self.assertEqual(unknown['status'], 'quarantined')
        self.assertFalse(self.store.eligible(unknown['id'], 1))

    def test_trigger_specific_required_fields(self):
        for changes in ({'trigger': 'time', 'when': None, 'channel': None},
                        {'trigger': 'event'}, {'channel': None}, {'when': '   '}):
            op = copy.deepcopy(self.op)
            op['record'].update(changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                validate({'operations': [op]}, EXTRACTION)

    def test_invalid_refs_spans_and_unused_evidence_reject_without_mutation(self):
        for field, citation in [('action', {'ref': 'future', 'quote': self.text}),
                                ('condition', {'ref': 'mA', 'quote': 'not actually observed'}),
                                ('when', {'ref': 'mA', 'quote': 'invented time'})]:
            op = copy.deepcopy(self.op)
            op['record']['evidence'][field] = [citation]
            before = self.snapshot()
            with self.subTest(field=field), self.assertRaisesRegex(ValueError, 'observed span'):
                self.apply([op])
            self.assertEqual(self.snapshot(), before)

    def test_saved_menu_distractors_have_valid_quotes_but_no_obligation_source(self):
        for trace in FAILED[1:3]:
            sources = trace['output']['operations'][0]['sources']
            obs = trace['context']['observations']
            citations_valid(sources, obs)
            with self.assertRaisesRegex(ValueError, 'obligation requires'):
                obligation_sources_valid(sources, obs)

    def test_menu_or_tool_cannot_create_even_with_structurally_valid_record(self):
        for kind, text in [('visible', 'Step action menu:\n- h7: File the amber tray.'),
                           ('query', 'State [queue]: Please file the amber tray when ready.')]:
            op = copy.deepcopy(self.op)
            obs = {'mA': {'text': text, 'kind': kind, 'checkpoint': 1}}
            op['sources'] = [{'ref': 'mA', 'quote': text}]
            with self.subTest(kind=kind), self.assertRaisesRegex(ValueError, 'obligation requires'):
                self.apply([op], obs)
            self.assertEqual(self.snapshot(), ({}, []))

    def test_genuine_requests_using_menu_vocabulary_and_quoted_titles_pass(self):
        for i, text in enumerate(['Please discard the amber tray when approved.',
                                  'Please print the menu titled "Discard" when approved.']):
            ref = f'm{i}'
            obs = {ref: {'text': text + '\n\nStep action menu:\n- z9: Discard a tray.\n\nTime: 14:20',
                         'kind': 'visible', 'checkpoint': 1}}
            rec = record(text.split(' when')[0], 'event', 'approved', None, None, text, ref)
            self.apply([{**self.op, 'record': rec, 'sources': [{'ref': ref, 'quote': text}]}], obs)
        self.assertEqual(len(self.store.records()), 2)

    def test_narrative_entailment_is_explicitly_not_a_deterministic_guarantee(self):
        text = 'The handbook example says "File the tray when approved."'
        obs = {'mA': {'text': text, 'kind': 'visible', 'checkpoint': 1}}
        # This deliberately unsupported semantic draft passes provenance/structure.
        # Its rejection is requested by the prompt; a mock cannot demonstrate it.
        rec = record('File the tray.', 'event', 'approved', None, None, text, 'mA')
        self.apply([{**self.op, 'record': rec, 'sources': [{'ref': 'mA', 'quote': text}]}], obs)
        self.assertEqual(len(self.store.records()), 1)

    def test_legitimate_empty_update_and_repeated_no_change(self):
        self.apply([])
        self.assertEqual(self.snapshot(), ({}, []))
        self.apply([self.op])
        before = self.snapshot()
        self.apply([])
        self.assertEqual(self.snapshot(), before)

    def test_duplicate_creation_even_with_a_different_source_ref(self):
        self.apply([self.op])
        before = self.snapshot()
        op = copy.deepcopy(self.op)
        op['sources'][0]['ref'] = 'mB'
        obs = {**self.obs, 'mB': self.obs['mA']}
        with self.assertRaisesRegex(ValueError, 'Duplicate creation'):
            self.apply([op], obs)
        self.assertEqual(self.snapshot(), before)

    def test_multiple_valid_intentions_and_atomic_invalid_batch(self):
        other = self.second_obligation()
        other['record']['trigger'] = 'unknown'
        other['record']['condition'] = 'Ready; prerequisite File the amber tray remains unresolved'
        bad = copy.deepcopy(other)
        bad['sources'][0]['ref'] = 'nonexistent'
        with self.assertRaises(ValueError):
            self.apply([self.op, bad])
        self.assertEqual(self.snapshot(), ({}, []))
        self.apply([self.op, other])
        self.assertEqual(len(self.store.records()), 2)

    def test_operation_specific_structure_and_version_minimum(self):
        cases = [dict(kind='create', target='invented'), dict(kind='create', expected_version=1),
                 dict(kind='create', record=None), dict(kind='revise', target=None),
                 dict(kind='revise', target='i_x', expected_version=0),
                 dict(kind='cancel', target='i_x', expected_version=1),
                 dict(kind='ambiguous', record=None, target='i_x')]
        for changes in cases:
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                validate({'operations': [{**self.op, **changes}]}, EXTRACTION)

    def test_revise_cancel_stale_version_and_dependency_cycles(self):
        self.apply([self.op])
        first = next(iter(self.store.records()))
        other = self.second_obligation()
        other['record']['dependencies'] = [first]
        other['record']['evidence']['dependencies'] = other['sources']
        self.apply([other])
        second = next(k for k in self.store.records() if k != first)
        self.assertFalse(self.store.eligible(second, 1))
        revise = copy.deepcopy(self.op)
        revise.update(kind='revise', target=first, expected_version=1)
        revise['record']['dependencies'] = [second]
        revise['record']['evidence']['dependencies'] = revise['sources']
        before = self.snapshot()
        with self.assertRaisesRegex(ValueError, 'Cyclic'):
            self.apply([revise])
        self.assertEqual(self.snapshot(), before)
        for dep in ('missing', first):
            revise['record']['dependencies'] = [dep]
            with self.assertRaisesRegex(ValueError, 'Unknown or self'):
                self.apply([revise])
            self.assertEqual(self.snapshot(), before)
        revise['record']['dependencies'] = []
        self.apply([revise])
        with self.assertRaisesRegex(ValueError, 'stale'):
            self.apply([revise])
        self.apply([{**revise, 'kind': 'cancel', 'expected_version': 2, 'record': None}])
        self.assertEqual(self.store.records()[first]['version'], 3)
        self.assertEqual(self.store.records()[first]['status'], 'canceled')

    def test_unknown_dependency_is_quarantined_until_bound_by_revision(self):
        unresolved = self.second_obligation()
        unresolved['record'].update(trigger='unknown', condition='Ready; prerequisite File the amber tray remains unresolved')
        self.apply([self.op, unresolved])
        records = self.store.records()
        first = next(k for k, v in records.items() if v['trigger'] == 'hidden')
        second = next(k for k in records if k != first)
        self.assertFalse(self.store.eligible(second, 1))
        unresolved.update(kind='revise', target=second, expected_version=1)
        unresolved['record'].update(trigger='hidden', dependencies=[first], condition='Ready')
        unresolved['record']['evidence']['dependencies'] = unresolved['sources']
        self.apply([unresolved])
        self.assertFalse(self.store.eligible(second, 2))
        eid = self.store.select(first, 1, 'h7', 1, [])
        self.store.attempted(eid)
        self.store.receipt(eid, 'success')
        self.assertTrue(self.store.eligible(second, 2))

    def test_ambiguous_update_does_not_unlock_uncertain_execution(self):
        self.apply([self.op])
        key = next(iter(self.store.records()))
        eid = self.store.select(key, 1, 'h7', 1, [])
        self.store.attempted(eid)
        self.store.receipt(eid, 'uncertain')
        self.apply([{**self.op, 'kind': 'ambiguous', 'record': None}])
        self.assertEqual(self.store.records()[key]['status'], 'uncertain')
        with self.assertRaisesRegex(ValueError, 'unresolved execution'):
            self.apply([{**self.op, 'kind': 'revise', 'target': key, 'expected_version': 1}])

    def test_actionable_error_reaches_bounded_retry_and_every_call_is_accounted(self):
        bad = copy.deepcopy(self.op)
        bad['record']['condition'] = ''
        account = Accounting(self.root/'account.sqlite', 1, self.config)
        self.addCleanup(account.db.close)
        agent = self.agent([{'operations': [bad]}, {'operations': [self.op]}], accounting=account)
        invoke = agent.gateway.transport.invoke
        # Synthetic provider metadata solely exercises durable reservations in MOCK.
        agent.gateway.transport.invoke = lambda request, timeout: replace(
            invoke(request, timeout), provider_metadata={'transport': 'MOCK', 'provider_reported': 'Novita'})
        agent.receive(json.dumps(frame(self.obs)))
        events = rows(self.root/'agent.jsonl')
        self.assertIn('record.condition', events[2]['request']['messages'][-1]['content'])
        self.assertEqual(events[1]['validation_stage'], 'structure')
        self.assertEqual(events[3]['outcome'], 'accepted_operations')
        self.assertEqual(events[0]['request']['response_format']['json_schema']['schema'], EXTRACTION)
        self.assertEqual(account.snapshot()['attempts'], 2)
        self.assertEqual(len({r['request_id'] for r in events}), 2)
        self.assertEqual([r['attempt'] for r in events], [1, 1, 2, 2])

    def test_contextual_error_reaches_retry_without_expected_answers(self):
        bad = copy.deepcopy(self.op)
        bad['sources'][0]['ref'] = 'invalid'
        agent = self.agent([{'operations': [bad]}, {'operations': []}])
        agent.receive(json.dumps(frame(self.obs)))
        events = rows(self.root/'agent.jsonl')
        self.assertEqual(events[1]['validation_stage'], 'application')
        feedback = events[2]['request']['messages'][-1]['content']
        self.assertIn('observed span', feedback)
        self.assertNotIn('due_now', feedback)
        self.assertEqual(events[3]['outcome'], 'accepted_empty_update')
        self.assertFalse(agent.blocked)
        self.assertEqual(agent.store.records(), {})

    def test_retry_exhaustion_is_fail_closed_not_an_empty_success(self):
        bad = {'operations': [{**self.op, 'record': None}]}
        agent = self.agent([bad, bad])
        agent.receive(json.dumps(frame(self.obs)))
        decision = agent.decide()
        self.assertEqual(decision['blocked'], 'invalid_extraction')
        self.assertEqual(decision['task_ids'], [])
        self.assertEqual(agent.store.records(), {})
        events = rows(self.root/'agent.jsonl')
        self.assertEqual(len(events), 4)
        self.assertEqual(events[-1]['outcome'], 'retry_exhausted')

    def test_all_three_saved_selection_failures_remain_rejected_without_state_mutation(self):
        for i, trace in enumerate(FAILED[3:]):
            context = trace['context']
            agent = self.agent([{'operations': []}, trace['output'], trace['output']], name=f'select{i}')
            agent.receive(json.dumps(frame(context['observations'], context['checkpoint'], ['task_1'])))
            before = agent.store.records()
            decision = agent.decide()
            self.assertEqual(decision['blocked'], 'invalid_selection')
            self.assertEqual(agent.store.records(), before)
            events = rows(self.root/f'select{i}.jsonl')
            self.assertEqual(events[3]['validation_stage'], 'structure')
            self.assertEqual(events[-1]['outcome'], 'retry_exhausted')

    def test_stale_citation_is_separate_from_binding_identifier_failure(self):
        obs = {'old': {'text': 'Ready', 'kind': 'query', 'checkpoint': 1},
               'now': {'text': 'Ready', 'kind': 'query', 'checkpoint': 2}}
        with self.assertRaisesRegex(ValueError, 'stale trigger evidence'):
            citations_valid([{'ref': 'old', 'quote': 'Ready'}, {'ref': 'now', 'quote': 'Ready'}], obs, current=2)

    def test_selection_description_rejected_with_populated_ledger(self):
        rec = record('File the tray.', 'event', 'Ready', None, None, self.text, 'mA')
        bad = dict(action='choose', choice='A', channel='NONE', task_ids=['h7'],
                   bindings=[dict(handle='h7', intention='File the tray.', version=1,
                                  evidence=[{'ref': 'mA', 'quote': self.text}])])
        agent = self.agent([{'operations': [{**self.op, 'record': rec}]}, bad, bad])
        agent.receive(json.dumps(frame(self.obs)))
        before = agent.store.records()
        self.assertEqual(agent.decide()['blocked'], 'invalid_selection')
        self.assertEqual(agent.store.records(), before)
        events = rows(self.root/'agent.jsonl')
        self.assertIn('bindings[0].intention', events[3]['validation_error'])
        self.assertEqual(events[3]['validation_stage'], 'structure')

    def test_every_request_including_retry_excludes_private_and_future_state(self):
        from scripts.generate_v2_cases import build
        from kiodai_v2.runner import run_case
        from kiodai_v2.fixture import FixtureTransport
        from research_harness.model_gateway import TransportResponse
        case = build('hidden', 77243)
        case['private_sentinel'] = 'GOLD_SENTINEL_V21'
        case['days'][0]['tasks'][0]['private'] = 'TASK_TABLE_SENTINEL_V21'
        case['days'][0]['steps'][-1]['text'] += ' FUTURE_SENTINEL_V21'
        path = self.root/'case.json'
        path.write_text(json.dumps(case))

        class OnceInvalid(FixtureTransport):
            first = True
            def invoke(self, request, timeout_seconds):
                if self.first:
                    self.first = False
                    return TransportResponse('malformed development fixture', {}, {}, 'mock', {})
                request = copy.deepcopy(request)
                if request['messages'][-1]['content'].startswith('Validation failed'):
                    request['messages'] = request['messages'][:-2]
                return super().invoke(request, timeout_seconds)

        for method in ('A2', 'B_ledger'):
            folder = run_case(path, method, self.root/method, self.config, OnceInvalid())
            requests = [r for r in rows(folder/'calls.jsonl') if r['event'] == 'request']
            self.assertTrue(any(r['attempt'] == 2 for r in requests))
            for request in requests:
                serialized = json.dumps(request['request'])
                for forbidden in ('GOLD_SENTINEL_V21', 'TASK_TABLE_SENTINEL_V21', 'private_77243',
                                  'due_now', 'groundtruth'):
                    self.assertNotIn(forbidden, serialized)
                if request['checkpoint'] < 8:
                    self.assertNotIn('FUTURE_SENTINEL_V21', serialized)

    def test_shared_extraction_requests_and_results_for_b_ledger_and_a2(self):
        agents = [self.agent([{'operations': [self.op]}], method=m, name=m) for m in ('B_ledger', 'A2')]
        for agent in agents:
            agent.receive(json.dumps(frame(self.obs)))
        self.assertEqual(agents[0].store.records(), agents[1].store.records())
        requests = [rows(self.root/(m+'.jsonl'))[0]['request'] for m in ('B_ledger', 'A2')]
        self.assertEqual(requests[0], requests[1])

    def test_metamorphic_entities_handles_paraphrases_and_shifted_times(self):
        for i, (entity, handle, timing, text) in enumerate([
            ('amber', 'option_k9', 'Tuesday 14:20', 'At 14:20 on Tuesday, print the amber menu.'),
            ('violet', 'option_p2', 'Thursday 16:35', 'Please print the violet menu at 16:35 on Thursday.'),
        ]):
            rec = record(f'Print the {entity} menu.', 'time', None, None, timing, text, 'mA')
            op = {**self.op, 'record': rec, 'sources': [{'ref': 'mA', 'quote': text}]}
            obs = {'mA': {'text': text, 'kind': 'visible', 'checkpoint': 1}}
            agent = self.agent([{'operations': [op]}], name=str(i))
            agent.receive(json.dumps(frame(obs, handles=[handle])))
            key = next(iter(agent.store.records()))
            now = f'Time: {timing}'
            obs['mB'] = {'text': now, 'kind': 'visible', 'checkpoint': 2}
            selection = dict(action='choose', choice='B', channel='NONE', task_ids=[handle],
                             bindings=[dict(handle=handle, intention=key, version=1, evidence=[{'ref': 'mB', 'quote': now}])])
            agent.gateway.transport = MockTransport([json.dumps({'operations': []}), json.dumps(selection)])
            agent.receive(json.dumps(frame(obs, 2, [handle])))
            result = agent.decide()
            self.assertEqual(result['task_ids'], [handle])
            self.assertEqual(agent.store.records()[key]['status'], 'attempted')
            agent.receipt(json.dumps([{'execution_id': result['bindings'][0]['execution_id'], 'outcome': 'success'}]))
            self.assertEqual(agent.store.records()[key]['status'], 'completed')

    def test_transport_failure_has_one_logged_request_no_repair(self):
        agent = self.agent([RuntimeError('offline')])
        with self.assertRaises(RunStopped):
            agent.receive(json.dumps(frame(self.obs)))
        events = rows(self.root/'agent.jsonl')
        self.assertEqual(len(events), 2)
        self.assertEqual(events[1]['outcome'], 'transport_failure')


if __name__ == '__main__':
    unittest.main()
