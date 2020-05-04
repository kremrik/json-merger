from typing import Any, Callable


def merge(raw: dict, master: dict) -> dict:
    output = {}

    # adds keys from `master` if they do not exist in `raw`
    intersection = {**master, **raw}

    for k_intersect, v_intersect in intersection.items():
        if k_intersect not in raw:
            v_master = master[k_intersect]
            output[k_intersect] = v_master

        elif k_intersect not in master:
            output[k_intersect] = v_intersect

        elif isinstance(v_intersect, dict):
            v_master = master[k_intersect]
            output[k_intersect] = merge(v_intersect, v_master)

        else:
            output[k_intersect] = v_intersect

    return output
