__version__ = '0.1.0'

import json

from .functions import dict_to_sorted_by_utf16_tuple
from .util import JSON, preprocess_json_data


def canonicalize(data: JSON) -> bytes:
    data = preprocess_json_data(
        data,
        dict_func=dict_to_sorted_by_utf16_tuple,
    )
    output = json.dumps(
        data,
        separators=(',', ':'),
        ensure_ascii=False,
        allow_nan=False,
    )
    return output.encode('utf8')
