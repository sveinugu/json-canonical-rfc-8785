from enum import IntEnum
from functools import partial
from typing import Callable

from ga4gh_json_canonical.util import JSON, JSON_Dict, JSON_List, preprocess_json_data
import pytest


@pytest.fixture
def preprocess_json_data_test_func() -> Callable[[JSON], JSON]:
    def str_func(s: str) -> JSON:
        return s.upper()

    def int_func(i: int) -> JSON:
        return i + 1

    def float_func(f: float) -> JSON:
        return f / 2

    def bool_func(b: bool) -> JSON:
        return not b

    def none_func(b: None) -> JSON:
        return ''

    def dict_func(d: JSON_Dict) -> JSON:
        d['new'] = 'value'
        return d

    def list_func(li: JSON_List) -> JSON:
        li = list(li)
        li.append([])
        return li

    return partial(
        preprocess_json_data,
        str_func=str_func,
        int_func=int_func,
        float_func=float_func,
        bool_func=bool_func,
        none_func=none_func,
        dict_func=dict_func,
        list_func=list_func,
    )


def test_preprocess_json_data_core_types(preprocess_json_data_test_func):
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
    assert preprocess_json_data_test_func(data,) == {
        'key_1': [
            'TEXT',
            2,
            1.0,
            False,
            '',
            {
                'key_2': ['STRING', 4, 2.0, True, '', []],
                'key_3': ['CONTENT', 6, 3.0, False, '', []],
                'new': 'value'
            },
            [False, True, 'MAYBE', []],
            [],
        ],
        'new': 'value',
    }


def test_preprocess_json_data_int_enum(preprocess_json_data_test_func):
    class Choice(IntEnum):
        Yes = 1
        No = 0

    assert preprocess_json_data_test_func([Choice.Yes, Choice.No]) == [2, 1, []]


def test_preprocess_json_data_set_fail(preprocess_json_data_test_func):
    with pytest.raises(TypeError):
        assert preprocess_json_data_test_func(set([1, 2, 3]))  # noqa
