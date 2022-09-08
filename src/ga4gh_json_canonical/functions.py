from typing import Tuple, Union

from ga4gh_json_canonical.util import JSON, JSON_Dict


def int_to_str_if_too_large(i: int) -> Union[int, str]:
    if i >= 2**63 or i <= -2**63:
        return str(i)
    else:
        return i


def float_to_int_if_whole_and_not_large_exp(f: float) -> Union[int, float]:
    if f.is_integer() and abs(f) < 1e22:
        return int(f)
    else:
        return f


def to_utf16_tuple(any_str: str) -> Tuple[int]:
    utf_16_bytes = any_str.encode('utf-16-be')
    return tuple(
        int.from_bytes(utf_16_bytes[i:i + 2], 'big') for i in range(0, len(utf_16_bytes), 2))


def _key_to_utf16_tuple(keyval: Tuple[str, JSON]) -> Tuple[int]:
    key, _val = keyval
    return to_utf16_tuple(key)


def dict_to_sorted_by_utf16_tuple(d: JSON_Dict) -> JSON_Dict:
    return dict(sorted(d.items(), key=_key_to_utf16_tuple))  # noqa