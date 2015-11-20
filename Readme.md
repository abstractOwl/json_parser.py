# Python JSON parser

## Examples

```
λ> python jsonparse.py
[1,
2,
 3, 
4]
 [1, 2, 3, 4]
```

```
λ> python json_parse.py
{
  arr: [
      1,
      2,
      3,
      4,
      "hello"
    ],
  b: 5
}
{'arr': [1, 2, 3, 4, 'hello'], 'b': 5}
```

## TODO:
1. Fix object keys. The keys should be quoted strings according to the RFC.


https://tools.ietf.org/html/rfc7159#section-2
