"""Small, explicit serialization and validation helpers (no environment imports)."""
import hashlib
import json
import os
from pathlib import Path


def digest(value):
    return hashlib.sha256(value).hexdigest()


def dump(path, value):
    path = Path(path)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n')
    temporary.replace(path)


def append(path, value):
    with Path(path).open('a') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, sort_keys=True) + '\n')
        stream.flush()
        os.fsync(stream.fileno())


def rows(path):
    return [json.loads(line) for line in Path(path).read_text().splitlines() if line.strip()]


def obj(properties):
    return {'type': 'object', 'properties': properties, 'required': list(properties),
            'additionalProperties': False}


def array(items, maximum=16):
    return {'type': 'array', 'items': items, 'maxItems': maximum}


STRING = {'type': 'string'}
NULL_STRING = {'type': ['string', 'null']}
CITATION = obj({'ref': STRING, 'quote': STRING})


def validate(value, schema):
    """Validate the exact subset used by our emitted strict JSON schemas."""
    kinds = schema.get('type')
    kinds = kinds if isinstance(kinds, list) else [kinds]
    types = {'object': dict, 'array': list, 'string': str, 'integer': int,
             'boolean': bool, 'null': type(None)}
    if not any(type(value) is types[k] for k in kinds):
        raise ValueError('Wrong JSON type')
    if 'enum' in schema and value not in schema['enum']:
        raise ValueError('Value outside enum')
    if isinstance(value, dict):
        if set(value) != set(schema['properties']):
            raise ValueError('Missing or extra fields')
        for key in value:
            validate(value[key], schema['properties'][key])
    if isinstance(value, list):
        if len(value) > schema.get('maxItems', 100):
            raise ValueError('Array too long')
        for item in value:
            validate(item, schema['items'])


def parse(text, schema):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError('Duplicate JSON key')
            result[key] = value
        return result
    value = json.loads(text, object_pairs_hook=unique)
    validate(value, schema)
    return value


def citations_valid(citations, observations, *, current=None):
    if not citations:
        raise ValueError('Missing source evidence')
    for citation in citations:
        source = observations.get(citation['ref'])
        if not source or not citation['quote'] or citation['quote'] not in source['text']:
            raise ValueError('Citation is not an observed span')
        if current is not None and source['checkpoint'] != current:
            raise ValueError('Stale trigger evidence')
