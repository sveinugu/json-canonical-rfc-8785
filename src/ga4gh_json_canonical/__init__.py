__version__ = '0.1.0'

import json
from typing import Any, Callable, Dict, Tuple


def to_utf16_tuple(any_str: str) -> Tuple[int]:
    utf_16_bytes = any_str.encode('utf-16-be')
    return tuple(
        int.from_bytes(utf_16_bytes[i:i + 2], 'big') for i in range(0, len(utf_16_bytes), 2))


def key_to_utf16_tuple(keyval: tuple) -> Tuple[int]:
    key, val = keyval
    return to_utf16_tuple(key)


def sort_all_dicts(data: Any):
    if type(data) is dict:
        return dict(
            sorted(((key, sort_all_dicts(val)) for key, val in data.items()),
                   key=key_to_utf16_tuple))
    if type(data) in (list, tuple):
        return tuple(sort_all_dicts(el) for el in data)
    return data


def canonicalize(data: Any) -> bytes:
    data = sort_all_dicts(data)
    output = json.dumps(
        data,
        separators=(',', ':'),
        ensure_ascii=False,
        allow_nan=False,
    )
    return output.encode('utf8')
