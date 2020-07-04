# Recursive Python dict merge function

### Usage

```python
from merge import merge
from functools import reduce

dict1 = {
    "foo": {
        "bar": [1, 2]
    },
    "qux": "sup"
}

dict2 = {
    "foo": {
        "bar": [3, 4],
        "baz": "hello"
    },
    "pi": 3.14
}

list_strategy = lambda x, y: reduce(lambda i, j: i+j, [x, y])

merge(dict1, dict2)
{
    "foo": {
        "bar": [1, 2, 3, 4],
        "baz": "hello"
    },
    "qux": "sup",
    "pi": 3.14
}
```