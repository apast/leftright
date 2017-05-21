import unittest

from leftright.core import LeftRightCore


class TestDiffStorage(unittest.TestCase):

    def test_switch_portable_storage(self):
        core_a = LeftRightCore()
        core_b = LeftRightCore({})

        id = "abc"
        core_a.set_left(id, "valuea")
        core_a.set_right(id, "valuea")

        # "Key was registered into storage_a and should not be present at storage_b")
        self.assertRaises(KeyError, core_b.get_left, id)
        # "Key was registered into storage_a and should not be present at storage_b")
        self.assertRaises(KeyError, core_b.get_right, id)

        core_b.set_left(id, "valueb")
        core_b.set_right(id, "valueb")

        self.assertNotEqual(core_a.get_left(id), core_b.get_left(id),
                          msg="Different keys were registered for the same ID and should be different in each storage")
        self.assertNotEqual(core_a.get_right(id), core_b.get_right(id),
                          msg="Different keys were registered for the same ID and should be different in each storage")


class TestLeftRightCoreComparison(unittest.TestCase):

    def setUp(self):
        self.core = LeftRightCore()

    def tearDown(self):
        self.core.store.clear()

    def test_comparison_of_different_length_sequences(self):
        id = "id"

        self.core.set_left(id, "")
        self.core.set_right(id, "a")
        self.assertRaises(AssertionError, self.core.next_diff, id)

        self.core.set_left(id, "a")
        self.core.set_right(id, "")
        self.assertRaises(AssertionError, self.core.next_diff, id)

        self.core.set_left(id, "aa")
        self.core.set_right(id, "a")
        self.assertRaises(AssertionError, self.core.next_diff, id)

    def test_comparison_of_similar_with_multiple_diff_sequences(self):
        id = "id"
        self.core.set_left(id, "bab")
        self.core.set_right(id, "aaa")
        first_diff = self.core.next_diff(id, offset=0)
        first_length = self.core.diff_length(id, offset=first_diff)
        self.assertEqual(0, first_diff)
        self.assertEqual(2, self.core.next_diff(id, offset=first_diff+first_length))

        self.core.set_left(id, "abab")
        self.core.set_right(id, "aaaa")
        first_diff = self.core.next_diff(id, offset=0)
        first_length = self.core.diff_length(id, offset=first_diff)
        self.assertEqual(1, self.core.next_diff(id, offset=0))
        self.assertEqual(3, self.core.next_diff(id, offset=first_diff+first_length))

    def test_comparison_of_similar_but_not_equal_sequences(self):
        id = "id"
        self.core.set_left(id, "a")
        self.core.set_right(id, "A")
        next_diff = self.core.next_diff(id)
        self.assertEqual(0, next_diff)
        self.assertEqual(1, self.core.diff_length(id, next_diff))

        self.core.set_left(id, "A")
        self.core.set_right(id, "a")
        next_diff = self.core.next_diff(id)
        self.assertEqual(0, next_diff)
        self.assertEqual(1, self.core.diff_length(id, next_diff))

        self.core.set_left(id, "_")
        self.core.set_right(id, "-")
        next_diff = self.core.next_diff(id)
        self.assertEqual(0, next_diff)
        self.assertEqual(1, self.core.diff_length(id, next_diff))

        self.core.set_left(id, "aa")
        self.core.set_right(id, "ab")
        next_diff = self.core.next_diff(id)
        self.assertEqual(1, next_diff)
        self.assertEqual(1, self.core.diff_length(id, next_diff))

        self.core.set_left(id, "aaaa")
        self.core.set_right(id, "aaab")
        next_diff = self.core.next_diff(id)
        self.assertEqual(3, next_diff)
        self.assertEqual(1, self.core.diff_length(id, next_diff))

        self.core.set_left(id, "aaaaac")
        self.core.set_right(id, "aaabbc")
        next_diff = self.core.next_diff(id)
        self.assertEqual(3, next_diff)
        self.assertEqual(2, self.core.diff_length(id, 3))

    def test_comparison_of_equal_sequences(self):
        id = "id"
        self.core.set_left(id, "")
        self.core.set_right(id, "")
        self.assertEqual(-1, self.core.next_diff(id))

        self.core.set_left(id, "a")
        self.core.set_right(id, "a")
        self.assertEqual(-1, self.core.next_diff(id))

        self.core.set_left(id, "A")
        self.core.set_right(id, "A")
        self.assertEqual(-1, self.core.next_diff(id))


class TestLeftRightCoreStorage(unittest.TestCase):

    def setUp(self):
        self.core = LeftRightCore()

    def tearDown(self):
        self.core.store.clear()

    def test_set_get(self):
        id = "abc"
        value = "sequence"
        self.assertRaises(KeyError, self.core._get, id, "left")

        self.core._set(id, "left", value)
        self.assertEquals(value, self.core._get(id, "left"))

        self.core._set(id, "left", None)
        self.assertRaises(KeyError, self.core._get, id, "left")

    def test_set_none_value(self):
        self.core._set("id", "q", None)
        self.assertRaises(KeyError, self.core._get, "id", "q")

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
