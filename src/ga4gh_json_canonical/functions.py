from typing import Tuple

from ga4gh_json_canonical.util import JSON, JSON_Dict, preprocess_json_data


def to_utf16_tuple(any_str: str) -> Tuple[int]:
    utf_16_bytes = any_str.encode('utf-16-be')
    return tuple(
        int.from_bytes(utf_16_bytes[i:i + 2], 'big') for i in range(0, len(utf_16_bytes), 2))


def key_to_utf16_tuple(keyval: Tuple[str, JSON]) -> Tuple[int]:
    key, _val = keyval
    return to_utf16_tuple(key)


def dict_to_sorted_by_utf16_tuple(d: JSON_Dict) -> JSON_Dict:
    return dict(sorted(d.items(), key=key_to_utf16_tuple))  # noqa
