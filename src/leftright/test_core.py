from leftright.core import LeftRightCore


import unittest


class TestLeftRightCore(unittest.TestCase):

    """Test case docstring."""

    def setUp(self):
        self.core = LeftRightCore()

    def tearDown(self):
        pass

    def test_update_right(self):
        id = "id"
        sequence = "sequence-right"
        self.assertRaises(KeyError, self.core.get_right, id)
        self.core.set_right(id, sequence+"-1")
        self.assertEqual(sequence+"-1", self.core.get_right(id))

        self.core.set_right(id, sequence+"-2")
        self.assertEqual(sequence+"-2", self.core.get_right(id))

        self.core.set_right(id, None)
        self.assertRaises(KeyError, self.core.get_right, id)

    def test_update_left(self):
        id = "id"
        sequence = "sequence-left"
        self.assertRaises(KeyError, self.core.get_left, id)
        self.core.set_left(id, sequence+"-1")
        self.assertEqual(sequence+"-1", self.core.get_left(id))

        self.core.set_left(id, sequence+"-2")
        self.assertEqual(sequence+"-2", self.core.get_left(id))

        self.core.set_left(id, None)
        self.assertRaises(KeyError, self.core.get_left, id)

    def test_set_left(self):
        id = "id"
        sequence = "sequence-left"
        self.assertRaises(KeyError, self.core.get_left, id)
        self.core.set_left(id, sequence)
        self.assertEqual(sequence, self.core.get_left(id))

        self.core.set_left(id, None)
        self.assertRaises(KeyError, self.core.get_left, id)

    def test_set_right(self):
        id = "id"
        sequence = "sequence-right"
        self.assertRaises(KeyError, self.core.get_right, id)
        self.core.set_right(id, sequence)
        self.assertEqual(sequence, self.core.get_right(id))

        self.core.set_right(id, None)
        self.assertRaises(KeyError, self.core.get_right, id)

    def test_get_diff_by_id(self):
        id = "id"
        self.assertRaises(KeyError, self.core.get_diff, id)

        self.core.set_left(id, "abc")
        self.core.set_right(id, "def")
        self.assertIsNotNone(self.core.get_diff(id))
        self.assertDictEqual(dict(state="ok"), self.core.get_diff(id))

        self.core.set_left(id, None)
        self.core.set_right(id, None)
        self.assertRaises(KeyError, self.core.get_diff, id)

    def test_get_partial_diff_by_id(self):
        id = "id"
        self.assertRaises(KeyError, self.core.get_diff, id)

        self.core.set_left(id, "abc")
        self.assertIsNotNone(self.core.get_diff(id))
        self.assertDictEqual(dict(state="partial_content"), self.core.get_diff(id))
        self.core.set_left(id, None)
        self.assertRaises(KeyError, self.core.get_diff, id)

        self.core.set_right(id, "def")
        self.assertDictEqual(dict(state="partial_content"), self.core.get_diff(id))
        self.core.set_right(id, None)
        self.assertRaises(KeyError, self.core.get_diff, id)

    def test_multiple_complete_diff_pairs(self):
        for i in range(10):
            id = "id:%s"%i
            self.core.set_left(id, "l_%s"%i)
            self.assertDictContainsSubset(dict(state="partial_content"), self.core.get_diff(id))
            self.core.set_right(id, "r_%s"%i)
            self.assertDictContainsSubset(dict(state="ok"), self.core.get_diff(id))

        for i in range(10):
            id = "id:%s"%i
            self.assertIsNotNone(self.core.get_diff(id))
            self.assertDictContainsSubset(dict(state="ok"), self.core.get_diff(id))
            self.core.set_left(id, None)
            self.assertDictContainsSubset(dict(state="partial_content"), self.core.get_diff(id))
            self.core.set_right(id, None)
            self.assertRaises(KeyError, self.core.get_diff, id)
