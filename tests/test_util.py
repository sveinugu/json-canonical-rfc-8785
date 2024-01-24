from enum import IntEnum
from types import NoneType

from jsoncanon.util import JSON, JSON_Dict, JSON_List, JsonDataPreprocessor
import pytest


@pytest.fixture
def json_data_preprocessor() -> JsonDataPreprocessor:
    def str_func(s: str) -> JSON:
        return s.upper()

    def int_func(i: int) -> JSON:
        return i + 1

    def float_func(f: float) -> JSON:
        return int(f / 2)

    def bool_func(b: bool) -> JSON:
        return not b

    def none_func(n: NoneType) -> JSON:
        return str(n)

    def dict_func(d: JSON_Dict) -> JSON:
        d['new'] = 'value'
        return d

    def list_func(li: JSON_List) -> JSON:
        li = list(li)
        li.append([])
        return li

    return JsonDataPreprocessor(
        str_func=str_func,
        int_func=int_func,
        float_func=float_func,
        bool_func=bool_func,
        none_func=none_func,
        dict_func=dict_func,
        list_func=list_func,
    )


def test_preprocess_json_data_core_types(json_data_preprocessor):
    data: JSON = {
        'key_1': [
            'text',
            1,
            2.0,
            True,
            None,
            {
                'key_2': ['string', 3, 4.0, False, None],
                'key_3': ['content', 5, 6.0, True, None],
            },
            (True, False, 'maybe'),
        ],
    }
    assert json_data_preprocessor(data,) == {
        'key_1': [
            'TEXT',
            2,
            2,
            False,
            'NONE',
            {
                'key_2': ['STRING', 4, 3, True, 'NONE', []],
                'key_3': ['CONTENT', 6, 4, False, 'NONE', []],
                'new': 'value'
            },
            [False, True, 'MAYBE', []],
            [],
        ],
        'new': 'value',
    }


def test_preprocess_json_data_int_enum(json_data_preprocessor):
    class Choice(IntEnum):
        Yes = 1
        No = 0

    assert json_data_preprocessor([Choice.Yes, Choice.No]) == [2, 1, []]


def test_preprocess_json_data_set_fail(json_data_preprocessor):
    with pytest.raises(TypeError):
        assert json_data_preprocessor(set([1, 2, 3]))  # noqa
