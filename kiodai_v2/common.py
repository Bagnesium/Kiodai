"""Small, explicit serialization and validation helpers (no environment imports)."""
import hashlib
import json
import os
import re
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


def validate(value, schema, path='$', root=None):
    """Validate the exact subset used by our emitted strict JSON schemas."""
    root = schema if root is None else root
    if '$ref' in schema:
        target = root
        for part in schema['$ref'].removeprefix('#/').split('/'):
            target = target[part]
        return validate(value, target, path, root)
    if 'anyOf' in schema:
        errors = []
        for branch in schema['anyOf']:
            try:
                validate(value, branch, path, root)
                return
            except ValueError as exc:
                errors.append(str(exc))
        # Prefer the matching discriminant's error; never use it to accept a value.
        if isinstance(value, dict):
            for branch, error in zip(schema['anyOf'], errors):
                props = branch.get('properties', {})
                if any(k in props and value.get(k) in props[k].get('enum', [])
                       for k in ('kind', 'trigger')):
                    raise ValueError(error)
        raise ValueError(f'{path}: no allowed variant ({errors[0]})')
    kinds = schema.get('type')
    kinds = kinds if isinstance(kinds, list) else [kinds]
    types = {'object': dict, 'array': list, 'string': str, 'integer': int,
             'boolean': bool, 'null': type(None)}
    if not any(type(value) is types[k] for k in kinds):
        raise ValueError(f'{path}: wrong JSON type; expected {kinds}')
    if 'enum' in schema and value not in schema['enum']:
        raise ValueError(f'{path}: value outside offered enum')
    if isinstance(value, str) and 'pattern' in schema and not re.search(schema['pattern'], value):
        raise ValueError(f'{path}: requires non-whitespace content')
    if type(value) is int and value < schema.get('minimum', value):
        raise ValueError(f'{path}: below minimum {schema["minimum"]}')
    if isinstance(value, dict):
        if set(value) != set(schema['properties']):
            missing = sorted(set(schema['properties']) - set(value))
            # Do not echo arbitrary model-provided keys in corrective instructions.
            raise ValueError(f'{path}: missing fields {missing} or extra fields present')
        for key in value:
            validate(value[key], schema['properties'][key], f'{path}.{key}', root)
    if isinstance(value, list):
        if len(value) > schema.get('maxItems', 100):
            raise ValueError(f'{path}: array too long')
        if len(value) < schema.get('minItems', 0):
            raise ValueError(f'{path}: missing required items')
        for index, item in enumerate(value):
            validate(item, schema['items'], f'{path}[{index}]', root)


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


def citations_valid(citations, observations, *, current=None, path='sources'):
    if not citations:
        raise ValueError(f'{path}: missing source evidence')
    for citation in citations:
        source = observations.get(citation['ref'])
        if not source or not citation['quote'].strip() or citation['quote'] not in source['text']:
            raise ValueError(f'{path}: citation ref/quote is not an observed span')
        if current is not None and source['checkpoint'] != current:
            raise ValueError(f'{path}: stale trigger evidence; use current-checkpoint observations')
