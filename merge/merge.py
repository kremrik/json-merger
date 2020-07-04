from functools import partial, reduce
from typing import Any, Callable, Optional, Tuple


__all__ = [
    "merge"
]


def merge(
    dict1: dict, 
    dict2: dict, 
    list_strategy: Optional[Callable] = None
    ) -> dict:
    """
    `merge` is a function to recursively, uhh, merge two dictionaries
    """
    if not list_strategy:
        list_strategy = lambda x, y: x
    else:
        list_strategy = validate_signature(list_strategy)

    output = {}

    for key in get_keys(dict1, dict2):
        left, right = get_values(dict1, dict2, key)

        if key not in dict1:
            output[key] = dict2[key]
        elif key not in dict2:
            output[key] = dict1[key]
        elif isinstance(left, dict):
            output[key] = merge(left, right, list_strategy)
        elif isinstance(left, list):
            output[key] = list_strategy(left, right)
        else:
            output[key] = left
        
    return output


def get_keys(
    left: dict, 
    right: dict
) -> set:
    return left.keys() | right.keys()


def get_values(
    left: dict, 
    right: dict, 
    key: str
) -> Tuple[Any, Any]:
    return get_value_from_dict(left, key), get_value_from_dict(right, key)


def get_value_from_dict(
    d: dict, 
    key: str
) -> Optional[Any]:
    if key in d:
        return d[key]
    return None


def validate_signature(
    fnc: Callable
) -> Callable:
    from inspect import getsource, signature

    sig = signature(fnc)
    fnc_params = len(sig.parameters)

    if fnc_params != 2:
        msg = f"The function given takes {fnc_params} parameter(s), but requires 2:\n{getsource(fnc)}"
        raise TypeError(msg)

    return fnc
