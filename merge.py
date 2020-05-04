from typing import Any, Callable


def merge(dict1: dict, dict2: dict) -> dict:
    output = {}

    # adds keys from `dict2` if they do not exist in `dict1`
    intersection = {**dict2, **dict1}

    for k_intersect, v_intersect in intersection.items():
        if k_intersect not in dict1:
            v_dict2 = dict2[k_intersect]
            output[k_intersect] = v_dict2

        elif k_intersect not in dict2:
            output[k_intersect] = v_intersect

        elif isinstance(v_intersect, dict):
            v_dict2 = dict2[k_intersect]
            output[k_intersect] = merge(v_intersect, v_dict2)

        else:
            output[k_intersect] = v_intersect

    return output
