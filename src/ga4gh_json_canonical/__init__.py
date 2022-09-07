__version__ = '0.1.0'

import json


def canonicalize(data):
    return json.dumps(data)
