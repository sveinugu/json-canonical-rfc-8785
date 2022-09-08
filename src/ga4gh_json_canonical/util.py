from typing import Callable, Dict, List, Optional, Tuple, Union

JSON_Dict = Dict[str, 'JSON']
JSON_List = Union[List['JSON'], Tuple['JSON', ...]]
JSON = Union[JSON_Dict, JSON_List, str, int, float, bool, None]


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
