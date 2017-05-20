class Base64Comparator():
    def diff(self, a, b, index=0):
        assert len(a) == len(b)
        l = len(a)

        i = index

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
        self.assertEqual(0, Base64Comparator().diff("_ A", "a A"))
        self.assertEqual(0, Base64Comparator().diff("- a A", ". a A"))
