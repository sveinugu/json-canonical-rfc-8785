import json

from jsoncanon.functions import (dict_to_sorted_by_utf16_tuple,
                                 float_to_int_if_whole_and_not_large_exp,
                                 int_to_str_if_too_large)
from jsoncanon.util import JSON, JsonDataPreprocessor


def canonicalize(data: JSON) -> bytes:
    preprocess = JsonDataPreprocessor(
        int_func=int_to_str_if_too_large,
        float_func=float_to_int_if_whole_and_not_large_exp,
        dict_func=dict_to_sorted_by_utf16_tuple,
    )
    data = preprocess(data)
    output = json.dumps(
        data,
        separators=(',', ':'),
        ensure_ascii=False,
        allow_nan=False,
    )
    return output.encode('utf8')
