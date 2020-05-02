from merge import merge
import unittest


class test_merge(unittest.TestCase):

    def test_null_case(self):
        raw = {}
        master = {}
        gold = {}
        output = merge(raw, master)
        self.assertEqual(gold, output)

    def test_same_schema(self):
        raw = {"foo": "bar"}
        master = {"foo": str}
        gold = {"foo": "bar"}
        output = merge(raw, master)
        self.assertEqual(gold, output)

    def test_type_mismatch(self):
        raw = {"foo": 1}
        master = {"foo": str}
        gold = {"foo": "1"}
        output = merge(raw, master)
        self.assertEqual(gold, output)

    def test_missing_key(self):
        raw = {"foo": 1}
        master = {"foo": int, "bar": int}
        gold = {"foo": 1, "bar": None}
        output = merge(raw, master)
        self.assertEqual(gold, output)

    def test_extra_key(self):
        raw = {"foo": 1, "bar": 2}
        master = {"foo": int}
        gold = {"foo": 1, "bar": 2}
        output = merge(raw, master)
        self.assertEqual(gold, output)


if __name__ == "__main__":
    unittest.main()
