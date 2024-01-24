# jsoncanon

Typed Python implementation of JSON Canonicalization Scheme as described in 
[RFC 8785](https://www.rfc-editor.org/rfc/rfc8785.html). The initial release (v0.2.x) is a partial release focused on the 
features needed by the [Sequence Collections working group](https://seqcol.readthedocs.io/) in the
[Global Alliance for Genomics and Health (GA4GH)](https://www.ga4gh.org/).

## Usage

```
>>> import json
>>> from jsoncanon import canonicalize
>>>
>>> data = json.loads('{ "b": [1,3,7], "a": { "y": true, "x": null } }')
>>> canonicalize(data)
b'{"a":{"x":null,"y":true},"b":[1,3,7]}'
```

## Releases

v0.2.0 - Initial release, supporting all data types except for floating point numbers
v0.2.1 - Yanked due to incorrect link
v0.2.2 - Initial release with updated project information