from typing import Any, Callable


def merge(raw: dict, master: dict) -> dict:
    """
    raw = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
    master = {"two": int, "three": int, "four": int, "five": int, "six": int}

    # 2 µs ± 24.1 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
    # 1.42 µs ± 4.29 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)
    1.16 µs ± 39.1 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

    > 40% reduction in run time
    """
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
