from leftright.compare import Base64Comparator


import unittest


class TestiDifferenceLength(unittest.TestCase):

    def test_get_difference_length_raises_error_for_not_similar_strings(self):
        self.assertRaises(AssertionError, Base64Comparator().diff_length, "", "a", 1)
        self.assertRaises(AssertionError, Base64Comparator().diff_length, "a", "aa", 2)
        self.assertRaises(AssertionError, Base64Comparator().diff_length, "ab", "abc", 2)
        self.assertRaises(AssertionError, Base64Comparator().diff_length, "abc", "ac", 2)

    def test_get_difference_length_raises_error_for_invalid_offset(self):
        self.assertRaises(IndexError, Base64Comparator().diff_length, "", "", 1)
        self.assertRaises(IndexError, Base64Comparator().diff_length, "a", "a", 2)
        self.assertRaises(IndexError, Base64Comparator().diff_length, "ab", "ab", 2)
        self.assertRaises(IndexError, Base64Comparator().diff_length, "ab", "ac", 2)
        self.assertRaises(IndexError, Base64Comparator().diff_length, "ab", "ac", 1000)
        self.assertRaisesRegex(IndexError, "^negative start index is not allowed$", Base64Comparator().diff_length, "", "", -1)

    def test_get_difference_length_for_equal_sequences(self):
        self.assertEqual(0, Base64Comparator().diff_length("", "", 0))
        self.assertEqual(0, Base64Comparator().diff_length("a", "a", 0))
        self.assertEqual(0, Base64Comparator().diff_length("ab", "ab", 0))
        self.assertEqual(0, Base64Comparator().diff_length("ab", "ab", 1))
        self.assertEqual(0, Base64Comparator().diff_length("abc", "abc", 2))

    def test_get_difference_length_for_similar_strings(self):
        self.assertEqual(0, Base64Comparator().diff_length("", "", 0))
        self.assertEqual(0, Base64Comparator().diff_length("a", "a", 0))
        self.assertEqual(1, Base64Comparator().diff_length("a", "b", 0))
        self.assertEqual(1, Base64Comparator().diff_length("aa", "ba", 0))
        self.assertEqual(1, Base64Comparator().diff_length("aaa", "baa", 0))
        self.assertEqual(2, Base64Comparator().diff_length("aaa", "bba", 0))
        self.assertEqual(1, Base64Comparator().diff_length("aaa", "bba", 1))
        self.assertEqual(0, Base64Comparator().diff_length("aaa", "bba", 2))
        self.assertEqual(3, Base64Comparator().diff_length("aaaccc", "bbaddd", 3))
        self.assertEqual(3, Base64Comparator().diff_length("aaaccceee", "bbadddeee", 3))
        self.assertEqual(2, Base64Comparator().diff_length("aaaccceee", "bbadddeee", 4))


class TestLength(unittest.TestCase):

    def test_equals_length(self):
        self.assertTrue(Base64Comparator().same_length("", ""))
        self.assertTrue(Base64Comparator().same_length("a", "b"))
        self.assertTrue(Base64Comparator().same_length("a", "a"))
        self.assertTrue(Base64Comparator().same_length("aa", "aa"))
        self.assertTrue(Base64Comparator().same_length("aa", "AA"))

    def test_not_equals_length(self):
        self.assertFalse(Base64Comparator().same_length("", "a"))
        self.assertFalse(Base64Comparator().same_length("a", ""))
        self.assertFalse(Base64Comparator().same_length("a", "ab"))
        self.assertFalse(Base64Comparator().same_length("aa", "a"))
        self.assertFalse(Base64Comparator().same_length("aab", "aa"))
        self.assertFalse(Base64Comparator().same_length("aa", "AbA"))


class DiffTestCase(unittest.TestCase):

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
        self.assertEqual(4, Base64Comparator().diff("110001", "111010", 4))
        self.assertEqual(6, Base64Comparator().diff("1234566", "1234567", 5))

    def test_next_different_sequence_index_from_invalid_start_index(self):
        self.assertRaises(IndexError, Base64Comparator().diff, "", "", 1)
        self.assertRaises(IndexError, Base64Comparator().diff, "a", "a", 2)
        self.assertRaises(IndexError, Base64Comparator().diff, "ab", "ab", 2)
        self.assertRaises(IndexError, Base64Comparator().diff, "ab", "ac", 2)
        self.assertRaisesRegex(IndexError, "^negative start index is not allowed$", Base64Comparator().diff, "", "", -1)
