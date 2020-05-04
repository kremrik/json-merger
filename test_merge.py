from merge import merge
import unittest
from unittest import skip


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
        output = merge(raw, master)
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
        output = merge(dict1, dict2)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
