from merge.merge import merge, merge_map, get_keys, get_values
import unittest
from unittest import skip
from functools import reduce


class test_merge(unittest.TestCase):

    def test_null_case(self):
        raw = {}
        master = {}
        gold = {}
        output = merge(raw, master)
        self.assertEqual(gold, output)

    def test_same_schema(self):
        raw = {"foo": "bar"}
        master = {"foo": None}
        gold = {"foo": "bar"}
        output = merge(raw, master)
        self.assertEqual(gold, output)

    def test_missing_key(self):
        raw = {"foo": 1}
        master = {"foo": None, "bar": None}
        gold = {"foo": 1, "bar": None}
        output = merge(raw, master)
        self.assertEqual(gold, output)

    def test_extra_key(self):
        raw = {"foo": 1, "bar": 2}
        master = {"foo": None}
        gold = {"foo": 1, "bar": 2}
        output = merge(raw, master)
        self.assertEqual(gold, output)

    def test_nested_master_has_more_default(self):
        raw = {
            "foo": {
                "bar": 1
            }
        }
        master = {
            "foo": {
                "bar": None,
                "baz": None
            }
        }
        gold = {
            "foo": {
                "bar": 1
            }
        }
        output = merge(raw, master)
        self.assertEqual(gold, output)

    def test_nested_master_has_more(self):
        raw = {
            "foo": {
                "bar": 1
            }
        }
        master = {
            "foo": {
                "bar": None,
                "baz": None
            }
        }
        gold = {
            "foo": {
                "bar": 1,
                "baz": None
            }
        }

        def dict_strat(dict1, dict2) -> dict:
            return merge(dict1, dict2)

        output = merge(raw, master, dict_strategy=dict_strat)
        self.assertEqual(gold, output)

    def test_nested_master_has_fewer(self):
        raw = {
            "foo": {
                "bar": 1,
                "baz": 2
            }
        }
        master = {
            "foo": {
                "bar": None
            }
        }
        gold = {
            "foo": {
                "bar": 1,
                "baz": 2
            }
        }
        output = merge(raw, master)
        self.assertEqual(gold, output)

    def test_two_completely_different_schemas(self):
        dict1 = {
            "key1": [1, 2, 3],
            "key2": 42,
            "key3": {
                "foo": "bar"
            }
        }
        dict2 = {
            "one": 1,
            "two": 2,
            "three": {
                "test": {
                    "hello": "world"
                }
            },
            "key3": {
                "foo": "bar",
                "baz": "dur"
            }
        }
        gold = {
            "key1": [1, 2, 3],
            "key2": 42,
            "key3": {
                "foo": "bar",
                "baz": "dur"
            },
            "one": 1,
            "two": 2,
            "three": {
                "test": {
                    "hello": "world"
                }
            }
        }

        def dict_strat(dict1, dict2) -> dict:
            return merge(dict1, dict2)

        output = merge(dict1, dict2, dict_strategy=dict_strat)
        self.assertEqual(gold, output)

    def test_merge_array_strategy_default(self):
        dict1 = {
            "foo": [1, 2]
        }
        dict2 = {
            "foo": [3, 4]
        }
        gold = {
            "foo": [1, 2]
        }

        output = merge(dict1, dict2)
        self.assertEqual(gold, output)

    def test_merge_array_strategy_custom(self):
        dict1 = {
            "foo": [1, 2]
        }
        dict2 = {
            "foo": [3, 4]
        }

        list_strategy = lambda x, y: reduce(lambda i, j: i+j, [x, y])

        gold = {
            "foo": [1, 2, 3, 4]
        }

        output = merge(dict1, dict2, list_strategy=list_strategy)
        self.assertEqual(gold, output)

    def test_merge_assortment(self):
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
        def dict_strategy(x, y):
            return merge(x, y, dict_strategy=dict_strategy, list_strategy=list_strategy)

        gold = {
            "foo": {
                "bar": [1, 2, 3, 4],
                "baz": "hello"
            },
            "qux": "sup",
            "pi": 3.14
        }

        output = merge(dict1, dict2, dict_strategy=dict_strategy, list_strategy=list_strategy)
        self.assertEqual(gold, output)


class test_merge_map(unittest.TestCase):

    def test_null_case_left(self):
        left = 1
        right = None
        gold = 1
        output = merge_map(left, right)
        self.assertEqual(gold, output)

    def test_null_case_right(self):
        left = None
        right = 1
        gold = 1
        output = merge_map(left, right)
        self.assertEqual(gold, output)

    def test_primitive(self):
        left = 1
        right = 2
        gold = 1
        output = merge_map(left, right)
        self.assertEqual(gold, output)

    def test_dict_default(self):
        left = {"foo": "bar"}
        right = {"baz": "qux"}
        gold = {"foo": "bar"}
        output = merge_map(left, right)
        self.assertEqual(gold, output)

    def test_array_default(self):
        left = [1, 2]
        right = [3, 4]
        gold = [1, 2]
        output = merge_map(left, right)
        self.assertEqual(gold, output)


class test_get_keys(unittest.TestCase):

    def test_null_case(self):
        left = {}
        right = {}
        gold = set()
        output = get_keys(left, right)
        self.assertEqual(gold, output)

    def test_left_null(self):
        left = {}
        right = {"foo": "bar"}
        gold = {"foo"}
        output = get_keys(left, right)
        self.assertEqual(gold, output)

    def test_right_null(self):
        left = {"foo": "bar"}
        right = {}
        gold = {"foo"}
        output = get_keys(left, right)
        self.assertEqual(gold, output)

    def test_union(self):
        left = {"foo": "bar"}
        right = {"baz": "qux"}
        gold = {"foo", "baz"}
        output = get_keys(left, right)
        self.assertEqual(gold, output)


class test_get_values(unittest.TestCase):

    def test_null_left(self):
        left = {}
        right = {"foo": 1}
        key = "foo"
        gold = (None, 1)
        output = get_values(left, right, key)
        self.assertEqual(gold, output)

    def test_null_right(self):
        left = {"foo": 1}
        right = {}
        key = "foo"
        gold = (1, None)
        output = get_values(left, right, key)
        self.assertEqual(gold, output)

    def test_both_exist(self):
        left = {"foo": 1}
        right = {"foo": 2}
        key = "foo"
        gold = (1, 2)
        output = get_values(left, right, key)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
