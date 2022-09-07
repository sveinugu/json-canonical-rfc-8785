from ga4gh_json_canonical import __version__, canonicalize

def test_version():
    assert __version__ == '0.1.0'


def test_literals():
    assert canonicalize(None) == 'null'
    assert canonicalize(True) == 'true'
    assert canonicalize(False) == 'false'
