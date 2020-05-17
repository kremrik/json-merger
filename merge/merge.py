from functools import partial
from typing import Any, Callable, Optional, Sequence, Tuple


def merge(
    dict1: dict, 
    dict2: dict, 
    dict_strategy: Callable = lambda x, y: x,
    list_strategy: Callable = lambda x, y: x
    ) -> dict:
    """
    `merge` is a function to recursively, uhh, merge two dictionaries

    By default, `merge` operates like the expression ``{**dict1, **dict2}``, 
    but when supplied functions for `dict_strategy` and `list_strategy` it 
    is capable of merging any Python dict in any way imaginable. You can 
    choose from some predefined functions from the `strategies` module to 
    get started quickly, or roll your own for even more fun. 

    TODO: add `strategies` module
    """

    keys = get_keys(dict1, dict2)
    return {
        key: merge_map(
            *get_values(dict1, dict2, key), 
            dict_strategy, 
            list_strategy)
        for key in keys
    }


def get_keys(left: dict, right: dict) -> set:
    return left.keys() | right.keys()


def get_values(left: dict, right: dict, key: str) -> Tuple[Any, Any]:
    return get_value_from_dict(left, key), get_value_from_dict(right, key)


def get_value_from_dict(d: dict, key: str) -> Optional[Any]:
    if key in d:
        return d[key]
    return None


def merge_map(
    left: Any, 
    right: Any, 
    dict_strategy: Callable = lambda x, y: x, 
    list_strategy: Callable = lambda x, y: x
    ):

    if not (left and right):
        return first(
            list(
                filter(lambda x: bool(x), [left, right])
            )
        )

    if is_dict(left):
        return dict_strategy(left, right)

    if is_list(left):
        return list_strategy(left, right)
    
    return left


def first(obj: Sequence) -> Optional[Any]:
    if not obj:
        return None
    return obj[0]


def is_instance_of(value: Any, obj: Any) -> bool:
    return isinstance(value, obj)

is_dict = partial(is_instance_of, obj=dict)

is_list = partial(is_instance_of, obj=list)
