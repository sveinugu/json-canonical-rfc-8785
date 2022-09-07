from ga4gh_json_canonical import __version__, canonicalize, sort_all_dicts, to_utf16_tuple
import pytest


def test_version():
    assert __version__ == '0.1.0'


def test_to_utf16_tuple():
    assert to_utf16_tuple('€') == (8364,)
    assert to_utf16_tuple('\r') == (13,)
    assert to_utf16_tuple('דּ') == (64307,)
    assert to_utf16_tuple('1') == (49,)
    assert to_utf16_tuple('😀') == (55357, 56832)
    assert to_utf16_tuple('\x80') == (128,)
    assert to_utf16_tuple('ö') == (246,)


def test_sort_all_dicts():

    assert sort_all_dicts({'b': 2, 'a': 1}) == {'a': 1, 'b': 2}
    assert sort_all_dicts({'b': {'d': 3, 'c': 2}, 'a': 1}) == {'b': {'c': 2, 'd': 3}, 'a': 1}
    assert sort_all_dicts({
        'a': [{
            'd': 3, 'c': 2
        }, 4], 'b': 2
    }) == {
        'a': ({
            'c': 2, 'd': 3
        }, 4), 'b': 2
    }


def test_whitespace():
    assert canonicalize({'a': [2, 3, 4, {'b': 2}, 3]}) == b'{"a":[2,3,4,{"b":2},3]}'


def test_literals():
    assert canonicalize(None) == b'null'
    assert canonicalize(True) == b'true'
    assert canonicalize(False) == b'false'


def test_strings():
    for c in range(8):
        assert canonicalize(chr(c)) == b'"\\u00%(c)02x"' % {b'c': c}

    assert canonicalize(chr(8)) == b'"\\b"'

    assert canonicalize(chr(9)) == b'"\\t"'

    assert canonicalize(chr(10)) == b'"\\n"'

    assert canonicalize(chr(11)) == b'"\\u000b"'

    assert canonicalize(chr(12)) == b'"\\f"'

    assert canonicalize(chr(13)) == b'"\\r"'

    for c in range(14, 32):
        assert canonicalize(chr(c)) == b'"\\u00%(c)02x"' % {b'c': c}

    assert canonicalize(chr(32)) == b'" "'

    for c in range(35, 92):
        assert canonicalize(chr(c)) == bytes(f'"{chr(c)}"', 'utf8')

    assert canonicalize(chr(92)) == b'"\\\\"'

    for c in range(93, 55296):
        assert canonicalize(chr(c)) == bytes(f'"{chr(c)}"', 'utf8')

    for c in range(55296, 57344):
        with pytest.raises(UnicodeEncodeError):
            canonicalize(chr(c))

    for c in range(57344, 65536):
        assert canonicalize(chr(c)) == bytes(f'"{chr(c)}"', 'utf8')

    assert canonicalize('€') == bytes(f'"€"', 'utf8')
    assert canonicalize('דּ') == bytes(f'"דּ"', 'utf8')
    assert canonicalize('😀') == bytes(f'"😀"', 'utf8')
    assert canonicalize('\x80') == bytes(f'"\x80"', 'utf8')
    assert canonicalize('ö') == bytes(f'"ö"', 'utf8')


def test_numbers():
    with pytest.raises(ValueError):
        assert canonicalize(float('nan'))
    with pytest.raises(ValueError):
        assert canonicalize(float('inf'))


def test_sorting():
    input = {
        '€': 'Euro Sign',
        '\r': 'Carriage Return',
        'דּ': 'Hebrew Letter Dalet With Dagesh',
        '1': 'One',
        '😀': "Emoji: Grinning Face",
        '\x80': "Control",
        'ö': "Latin Small Letter O With Diaeresis"
    }

    output = bytes(
        '{"\\r":"Carriage Return",'
        '"1":"One",'
        '"\u0080":"Control",'
        '"ö":"Latin Small Letter O With Diaeresis",'
        '"€":"Euro Sign",'
        '"😀":"Emoji: Grinning Face",'
        '"דּ":"Hebrew Letter Dalet With Dagesh"}',
        'utf8')

    assert canonicalize(input) == output
