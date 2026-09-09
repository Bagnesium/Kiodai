"""v2.1 structural contract shared by provider requests, parsing and ledger writes.

No scenario inputs. JSON Schema support at the provider is not trusted: local
validation enforces every emitted constraint. Entailment remains model-dependent.
"""
from .common import array, obj, citations_valid

VERSION = 'v2.1-extraction'
TEXT = {'type': 'string', 'pattern': r'\S'}
NULL = {'type': 'null'}
OPTIONAL_TEXT = {'type': ['string', 'null'], 'pattern': r'\S'}
CITATION = obj({'ref': TEXT, 'quote': TEXT})
FIELDS = ('action', 'trigger', 'condition', 'channel', 'when', 'dependencies')


def record_schema(trigger, condition, channel, when):
    return obj({'action': TEXT, 'trigger': {'type': 'string', 'enum': [trigger]},
                'condition': condition, 'channel': channel, 'when': when,
                'dependencies': array(TEXT),
                'evidence': {'$ref': '#/$defs/evidence'}})


RECORD = {'anyOf': [
    record_schema('time', OPTIONAL_TEXT, NULL, TEXT),
    record_schema('event', TEXT, NULL, OPTIONAL_TEXT),
    record_schema('hidden', TEXT, TEXT, OPTIONAL_TEXT),
    record_schema('unknown', OPTIONAL_TEXT, OPTIONAL_TEXT, OPTIONAL_TEXT),
]}


def operation_schema(kind):
    targeted = kind in ('revise', 'cancel')
    return obj({'kind': {'type': 'string', 'enum': [kind]},
                'target': TEXT if targeted else NULL,
                'expected_version': {'type': 'integer', 'minimum': 1} if targeted else NULL,
                'record': {'$ref': '#/$defs/record'} if kind in ('create', 'revise') else NULL,
                'sources': {**array({'$ref': '#/$defs/citation'}), 'minItems': 1}})


EXTRACTION = {**obj({'operations': array({'anyOf': [operation_schema(k) for k in
                 ('create', 'revise', 'cancel', 'ambiguous')]})}),
              '$defs': {'record': RECORD, 'citation': CITATION,
                        'evidence': obj({key: array({'$ref': '#/$defs/citation'}) for key in FIELDS})}}


def obligation_sources_valid(citations, observations):
    """Reject tool-only/menu-only support using public renderer boundaries.

    This is provenance routing, not a language classifier. A narrative quotation
    or hypothetical can still pass; the extractor must decide whether it delegates.
    """
    citations_valid(citations, observations)
    for citation in citations:
        source = observations[citation['ref']]
        if source['kind'] != 'visible':
            continue
        text, quote = source['text'], citation['quote']
        start = text.find('\n\nStep action menu:\n')
        if text.startswith('Step action menu:\n'):
            start = 0
        end = text.find('\n\n', start + 2) if start >= 0 else -1
        end = len(text) if end < 0 else end
        offset = text.find(quote)
        while offset >= 0:
            if start < 0 or offset + len(quote) <= start or offset >= end:
                return
            offset = text.find(quote, offset + 1)
    raise ValueError('sources: obligation requires visible instruction support outside tool output and action-menu spans')
