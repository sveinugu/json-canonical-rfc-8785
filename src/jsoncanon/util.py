from dataclasses import dataclass
from types import NoneType
from typing import Callable, Dict, List, Optional, Tuple, Type, Union

JSON_Dict = Dict[str, 'JSON']
JSON_List = Union[List['JSON'], Tuple['JSON', ...]]
JSON = Union[JSON_Dict, JSON_List, str, int, float, bool, NoneType]
JSON_Type = Type[Union[str, int, float, bool, None, Dict, List]]


@dataclass
class JsonDataPreprocessor:
    str_func: Optional[Callable[[str], JSON]] = None
    int_func: Optional[Callable[[int], JSON]] = None
    float_func: Optional[Callable[[float], JSON]] = None
    bool_func: Optional[Callable[[bool], JSON]] = None
    none_func: Optional[Callable[[NoneType], JSON]] = None
    dict_func: Optional[Callable[[JSON_Dict], JSON_Dict]] = None
    list_func: Optional[Callable[[JSON_List], JSON_List]] = None

    def __call__(self, data: JSON) -> JSON:
        if isinstance(data, str):
            return self._preprocess_type(data, str, self.str_func)
        elif isinstance(data, bool):
            return self._preprocess_type(data, bool, self.bool_func)
        elif isinstance(data, int):
            return self._preprocess_type(data, int, self.int_func)
        elif isinstance(data, float):
            return self._preprocess_type(data, float, self.float_func)
        elif isinstance(data, NoneType):
            return self._preprocess_type(data, NoneType, self.none_func)
        elif isinstance(data, Dict):
            data = {key: self(val) for (key, val) in data.items()}
            return self.dict_func(data) if self.dict_func else data
        elif isinstance(data, List) or isinstance(data, Tuple):
            data = [self(val) for val in data]
            return self.list_func(data) if self.list_func else data
        else:
            raise TypeError(f'Object of type "{type(data)}" not supported')

    def _preprocess_type(
        self,
        data: JSON,
        data_type: JSON_Type,
        type_func: Callable[[JSON], JSON],
    ) -> JSON_Type:
        data = type_func(data) if type_func else data
        if not isinstance(data, data_type):
            data = self(data)
        return data
