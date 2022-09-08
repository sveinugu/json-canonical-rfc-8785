__version__ = '0.1.0'

import json
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

JSON_Dict = Dict[str, 'JSON']
JSON_List = Union[List['JSON'], Tuple['JSON', ...]]
JSON = Union[JSON_Dict, JSON_List, str, int, float, bool, None]


def to_utf16_tuple(any_str: str) -> Tuple[int]:
    utf_16_bytes = any_str.encode('utf-16-be')
    return tuple(
        int.from_bytes(utf_16_bytes[i:i + 2], 'big') for i in range(0, len(utf_16_bytes), 2))


def key_to_utf16_tuple(keyval: Tuple[str, JSON]) -> Tuple[int]:
    key, _val = keyval
    return to_utf16_tuple(key)


def dict_to_sorted_by_utf16_tuple(d: JSON_Dict) -> JSON_Dict:
    return dict(sorted(d.items(), key=key_to_utf16_tuple))  # noqa


def sort_all_dicts(data: JSON):
    return preprocess_json_data(data, dict_func=dict_to_sorted_by_utf16_tuple)


def canonicalize(data: JSON) -> bytes:
    data = sort_all_dicts(data)
    output = json.dumps(
        data,
        separators=(',', ':'),
        ensure_ascii=False,
        allow_nan=False,
    )
    return output.encode('utf8')


def preprocess_json_data(
    data: JSON,
    str_func: Optional[Callable[[str], JSON]] = None,
    int_func: Optional[Callable[[int], JSON]] = None,
    float_func: Optional[Callable[[float], JSON]] = None,
    bool_func: Optional[Callable[[bool], JSON]] = None,
    none_func: Optional[Callable[[None], JSON]] = None,
    dict_func: Optional[Callable[[JSON_Dict], JSON]] = None,
    list_func: Optional[Callable[[JSON_List], JSON]] = None,
):
    if isinstance(data, str):
        return str_func(data) if str_func else data
    elif isinstance(data, bool):
        return bool_func(data) if bool_func else data
    elif isinstance(data, int):
        return int_func(data) if int_func else data
    elif isinstance(data, float):
        return float_func(data) if float_func else data
    elif data is None:
        return none_func(data) if none_func else data
    elif isinstance(data, Dict):
        data = {
            key: preprocess_json_data(
                val,
                str_func=str_func,
                int_func=int_func,
                float_func=float_func,
                bool_func=bool_func,
                none_func=none_func,
                dict_func=dict_func,
                list_func=list_func,
            ) for (key, val) in data.items()
        }
        return dict_func(data) if dict_func else data
    elif isinstance(data, List) or isinstance(data, Tuple):
        data = [
            preprocess_json_data(
                val,
                str_func=str_func,
                int_func=int_func,
                float_func=float_func,
                bool_func=bool_func,
                none_func=none_func,
                dict_func=dict_func,
                list_func=list_func,
            ) for val in data
        ]
        return list_func(data) if list_func else data
    else:
        raise TypeError(f'Object of type "{type(data)}" not supported')
