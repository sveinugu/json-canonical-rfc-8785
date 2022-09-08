from ga4gh_json_canonical.functions import dict_to_sorted_by_utf16_tuple, to_utf16_tuple
from ga4gh_json_canonical.util import JSON, preprocess_json_data


def test_to_utf16_tuple():
    assert to_utf16_tuple('€') == (8364,)
    assert to_utf16_tuple('\r') == (13,)
    assert to_utf16_tuple('דּ') == (64307,)
    assert to_utf16_tuple('1') == (49,)
    assert to_utf16_tuple('😀') == (55357, 56832)
    assert to_utf16_tuple('\x80') == (128,)
    assert to_utf16_tuple('ö') == (246,)
    assert to_utf16_tuple('€\rדּ'
                          '1😀\x80ö') == (8364, 13, 64307, 49, 55357, 56832, 128, 246)


def test_sort_all_dicts():
    def sort_all_dicts(data: JSON):
        return preprocess_json_data(data, dict_func=dict_to_sorted_by_utf16_tuple)

    assert sort_all_dicts({'b': 2, 'a': 1}) == {'a': 1, 'b': 2}
    assert sort_all_dicts({'b': {'d': 3, 'c': 2}, 'a': 1}) == {'b': {'c': 2, 'd': 3}, 'a': 1}
    assert sort_all_dicts({
        'a': [{
            '😀b': 3, '😀a': 2
        }, 4], 'b': 2
    }) == {
        'a': [{
            '😀a': 2, '😀b': 3
        }, 4], 'b': 2
    }
