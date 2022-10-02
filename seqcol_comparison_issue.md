# Comparison function does not maintain row-wise dependencies when reporting on order

There is one problem with the current solution for the comparison function that I believe we have 
not properly considered. It might be that we are ok the current functionality, but think that it
should be conscious decision, and we should report this as a known issue.

The issue is best explained with a simple contriver example. Given the following sequence 
collection A:

| names | lengths | sequences |
|-------|---------|-----------|
| chr1  | 12345   | 96f04ea2c |
| chr2  | 23456   | 00330e995 |
| chr3  | 34567   | 572853213 |

Let's compare this with sequence collection A', where we shuffle the rows, e.g.:

| names | lengths | sequences |
|-------|---------|-----------|
| chr3  | 34567   | 572853213 |
| chr1  | 12345   | 96f04ea2c |
| chr2  | 23456   | 00330e995 |

The comparison function would return the following:

```
{
  "digests": {
    "a": "b57173a40",
    "b": "1ab89fe61"
  },
  "arrays": {
    "a-only": [],
    "b-only": [],
    "a-and-b": [
      "lengths",
      "names",
      "sequences"
    ]
  },
  "elements": {
    "total": {
      "a": 3,
      "b": 3
    },
    "a-and-b": {
      "lengths": 3,
      "names": 3,
      "sequences": 3
    },
    "a-and-b-same-order": {
      "lengths": false,
      "names": false,
      "sequences": false
    }
  }
}
```

So let's say we instead shuffle the `names` and `sequences` array independently, but let the `lengths` array 
follow the `sequences` to keep the internal consistency, such as in the following sequence collection A'':


| names | lengths | sequences |
|-------|---------|-----------|
| chr2  | 23456   | 00330e995 |
| chr1  | 34567   | 572853213 |
| chr3  | 12345   | 96f04ea2c |

Then comparing _any_ two of the three collections `A`, `A'`, and `A''` would give the same result from the 
comparison function, which would typically be interpreted as "they have the same sequences, the only difference is their
order".

The reason behind this is simply that the comparison function considers each array individually, which is again due 
to the fact that we are structuring the sequence collections array-wise instead of item-wise (or column-wise instead 
of row-wise, if you want).

Granted, this is in practice an edge case which might never happen in the data itself. But it could very much appear 
due to some coding bug. To me, having this logical flaw reduces the trust one can have to the comparison function as 
a consumer.

I do have a suggestion that might solve this and other related issues. Sorry for not posting this earlier, but I 
have been swamped with work lately.