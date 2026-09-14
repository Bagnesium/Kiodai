#!/usr/bin/env python3
"""Evaluator-side synthetic development generator. Never imported by an agent."""
import json
import random
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from kiodai_v2.common import dump

ROOT = Path(__file__).resolve().parents[1]


def build(family, seed):
    rng = random.Random(seed)
    name = rng.choice(['cobalt', 'saffron', 'jade', 'silver']) + str(seed)
    channel = 'board_' + name
    hour = rng.choice([7, 8, 9])
    times = [f'{hour+i:02d}:00' for i in range(8)]
    actions = [f'Register the {name} sample.', f'Seal the {name} case.', f'Archive the {name} note.']
    def task(index, **fields):
        return {'id': f'private_{seed}_{index}', 'label': actions[index], 'action_text': actions[index],
                'regular': False, 'encoding': 'start', **fields}
    def step(index, text='Discuss unrelated stationery prices.', **fields):
        return {'id': f'private_step_{seed}_{index}', 'time': times[index], 'text': text,
                'options': ['A) Read the notice', 'B) Sort stationery', 'C) Check a spelling'],
                'cues': [], 'updates': [], **fields}
    lures = [{'id': f'private_lure_{seed}_{i}', 'action_text': a} for i, a in enumerate([
        f'Register a spare {name} sample.', f'Discard the {name} case.', 'Count spare envelopes.',
        'Align a pen.', 'Polish a spare tray.', 'Fold a blank card.', 'Rearrange a stool.',
        'Count spare clips.', 'Move a cushion.', 'Read a wall poster.'])]
    steps = [step(i) for i in range(8)]
    instructions = []
    tasks = []
    if family == 'revision':
        instructions = [f'At {times[3]} on DayOne, {actions[0]} At {times[4]} on DayOne, {actions[1]}']
        tasks = [task(0, type='time', target_time=times[3]), task(1, type='time', target_time=times[4])]
        for index, target in [(1, 5), (2, 6)]:
            steps[index] = step(index, f'Change of schedule: "{actions[0]}" is now due at {times[target]} on DayOne; replace the earlier time.',
                                updates=[{'task_id': tasks[0]['id'], 'action': 'reschedule', 'new_target_time': times[target]}])
        steps[4] = step(4, f'Do not carry out "{actions[1]}"; that request has been canceled.',
                        updates=[{'task_id': tasks[1]['id'], 'action': 'cancel'}])
    elif family == 'visible_events':
        instructions = [f'When you see "{name} hexagon", {actions[0]} When you see "{name} lantern", {actions[1]}']
        tasks = [task(0, type='event', cue_id='cue_hexagon'), task(1, type='event', cue_id='cue_lantern')]
        steps[1] = step(1, f'You see a {name} circle; it is not a hexagon.')
        steps[2] = step(2, f'For "{actions[1]}" replace the earlier cue with "{name} triangle".',
                        updates=[{'task_id': tasks[1]['id'], 'action': 'override', 'new_cue_id': 'cue_triangle'}])
        steps[3] = step(3, f'A {name} lantern appears.', cues=['cue_lantern'])
        steps[5] = step(5, f'A {name} hexagon appears.', cues=['cue_hexagon'])
        steps[6] = step(6, f'A {name} triangle appears.', cues=['cue_triangle'])
    elif family == 'hidden':
        instructions = [f'At {times[1]} on DayOne, {actions[0]}',
                        f'When {channel} reports "Cooling is now fully stable.", {actions[1]} Only after "{actions[0]}" succeeds.',
                        f'When {channel} reports "Cooling is now fully stable.", {actions[2]}']
        tasks = [task(0, type='time', target_time=times[1]),
                 task(1, type='event', cue_id='cue_stable', cue_channel=channel, depends_on=f'private_{seed}_0'),
                 task(2, type='event', cue_id='cue_stable', cue_channel=channel)]
        for i in range(8):
            positive = i == 6
            steps[i]['state_events'] = {channel: [{'id': 'cue_stable' if positive else f'cue_negative_{i}',
                'text': 'Cooling is now fully stable.' if positive else 'Cooling is nearly stable; final stabilization is not complete.'}]}
        steps[6]['text'] = 'The review window opens while cooling continues out of sight.'
    elif family == 'cross_day':
        instructions = [f'At {times[2]} on DayTwo, {actions[0]}',
                        f'On DayTwo when you see "{name} cabinet clicks", {actions[1]} Only after "{actions[0]}" succeeds.']
        tasks = [task(0, type='time', target_time=times[2], cross_day=True, cross_day_offset=1),
                 task(1, type='event', cue_id='cue_cabinet', depends_on=f'private_{seed}_0', cross_day=True, cross_day_offset=1)]
        later = [step(i) for i in range(4)]
        later[1]['text'] = f'The {name} cabinet creaks, without a click.'
        later[3]['text'] = f'The {name} cabinet clicks.'
        later[3]['cues'] = ['cue_cabinet']
        for s in later:
            s['id'] += '_later'
        return {'scenario_name': f'v2_{family}_{seed}', 'time_visible_by_default': True,
                'state_visibility': {'clock': True}, 'state_channels': {'clock': {'mode': 'snapshot'}},
                'days': [{'name': 'DayOne', 'start_instructions': instructions, 'tasks': [], 'lures': lures, 'steps': steps[:4]},
                         {'name': 'DayTwo', 'start_instructions': ['Continue the work already assigned.'],
                          'tasks': tasks, 'lures': lures, 'steps': later}]}
    return {'scenario_name': f'v2_{family}_{seed}', 'time_visible_by_default': True,
            'state_visibility': {'clock': True, **({channel: False} if family == 'hidden' else {})},
            'state_channels': {'clock': {'mode': 'snapshot'}, **({channel: {'mode': 'snapshot'}} if family == 'hidden' else {})},
            'days': [{'name': 'DayOne', 'start_instructions': ["Today's one-off tasks (new):"] + ['- '+line for line in instructions], 'tasks': tasks, 'lures': lures, 'steps': steps}]}


def main():
    directory = ROOT/'data/v2'
    directory.mkdir(parents=True, exist_ok=True)
    catalog = []
    for family_index, family in enumerate(['revision', 'visible_events', 'hidden', 'cross_day']):
        for variant in range(3):
            seed = 91300 + family_index * 10 + variant
            scenario = build(family, seed)
            path = directory/(scenario['scenario_name'] + '.json')
            dump(path, scenario)
            catalog.append({'path': str(path.relative_to(ROOT)), 'family': family, 'seed': seed,
                            'exposure': 'synthetic development; authored and inspected by the implementation process'})
    dump(directory/'catalog.json', {'cases': catalog, 'generator': 'scripts/generate_v2_cases.py',
        'origin': 'Four new synthetic PM-compatible templates, informed by inspected PM-Bench development cases and TriggerBench negative controls. No published test set is claimed.',
        'selection': 'All three predefined seeds in each family; no selection by model outcomes.'})


if __name__ == '__main__':
    main()
