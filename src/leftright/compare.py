class Base64Comparator():
    def diff(self, a, b, start=0):
        """TODO: Docstring for next_diff.

        :a: TODO
        :b: TODO
        :start: TODO
        :returns: TODO
        """
        assert len(a) == len(b)

        if start < 0:
            raise IndexError("negative start index is not allowed")

        l = len(a)

        if 0 < start >= l:
            raise IndexError("start index is greather than length(a)")

        i = start

        while i < l and a[i] == b[i]:
            i += 1

        return -1 if i == l else i


import unittest


class TestLeftRightDiff(unittest.TestCase):

    """Test case docstring."""

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_equals_sequences(self):
        self.assertEqual(-1, Base64Comparator().diff("", ""))
        self.assertEqual(-1, Base64Comparator().diff("a", "a"))
        self.assertEqual(-1, Base64Comparator().diff("A", "A"))
        self.assertEqual(-1, Base64Comparator().diff("aA", "aA"))
        self.assertEqual(-1, Base64Comparator().diff("a A", "a A"))
        self.assertEqual(-1, Base64Comparator().diff(" a A", " a A"))

    def test_zero_index_different_sequences(self):
        self.assertEqual(0, Base64Comparator().diff("0", "1"))
        self.assertEqual(0, Base64Comparator().diff("a", "A"))
        self.assertEqual(0, Base64Comparator().diff("A", "a"))
        self.assertEqual(0, Base64Comparator().diff("Aa", "aA"))
        self.assertEqual(0, Base64Comparator().diff("_A", "aA"))
        self.assertEqual(0, Base64Comparator().diff("-aA", ".aA"))

    def test_middle_index_different_sequences(self):
        self.assertEqual(1, Base64Comparator().diff("10", "11"))
        self.assertEqual(2, Base64Comparator().diff("aaa", "aaA"))
        self.assertEqual(3, Base64Comparator().diff("nheA", "nhea"))
        self.assertEqual(2, Base64Comparator().diff("Aa ", "Aac"))

    def test_next_different_sequence_index_from_start_index(self):
        self.assertEqual(1, Base64Comparator().diff("10", "11", 0))
        self.assertEqual(1, Base64Comparator().diff("10", "11", 1))
        self.assertEqual(2, Base64Comparator().diff("110", "111", 0))
        self.assertEqual(2, Base64Comparator().diff("110", "111", 2))

    def test_next_different_sequence_index_from_invalid_start_index(self):
        self.assertRaises(IndexError, Base64Comparator().diff, "", "", 1)
        self.assertRaises(IndexError, Base64Comparator().diff, "a", "a", 2)
        self.assertRaises(IndexError, Base64Comparator().diff, "ab", "ab", 2)
        self.assertRaises(IndexError, Base64Comparator().diff, "ab", "ac", 2)
        self.assertRaisesRegex(IndexError, "^negative start index is not allowed$", Base64Comparator().diff, "", "", -1)
