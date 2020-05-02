from typing import Callable


def merge(raw: dict, master: dict, type_check: Callable = lambda x, y: x) -> dict:
    """
    raw = {"one": 1, "two": 2, "three": 3, "four": 4, "five": 5}
    master = {"two": int, "three": int, "four": int, "five": int, "six": int}

    # 2 µs ± 24.1 ns per loop (mean ± std. dev. of 7 runs, 100000 loops each)
    1.42 µs ± 4.29 ns per loop (mean ± std. dev. of 7 runs, 1000000 loops each)

    30% reduction in execution time
    """
    if not master:
        return master

    output = {}
    raw_keys = set(raw)
    master_keys = set(master)
    missing_from_master = raw_keys - master_keys
    missing_from_raw = master_keys - raw_keys
    intersection = master_keys & raw_keys

    # three loops is a lot of repeated code, can't figure out a simpler way yet
    for key in missing_from_raw:
        output[key] = None

    for key in missing_from_master:
        output[key] = raw[key]

    for key in intersection:
        output[key] = type_check(raw[key], master[key])

    return output
