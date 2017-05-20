class Base64Comparator():

    def same_length(self, a, b):
        return len(a) == len(b)

    def _validate_similar_sequence(self, a, b, offset):
        """ Evaluates 'a', 'b' char sequences and 'offset' value

        Both 'a' and 'b' should have the same length and offset value should be
        less than sequence length.

        :a: Sequence of chars to be compared to 'b' sequence.
        :b: Sequence of chars to be compared to 'a' sequence.
        :offset: Positive index of the position to start the difference lookup.
        :returns: True if len(a) == len(b) & -1 < offset < len(a).
        :raises: IndexError if offset is invalid and AssertionError if
        len(a) != len(b).
        """
        assert self.same_length(a, b)

        if offset < 0:
            raise IndexError("negative start index is not allowed")

        if 0 < offset >= len(a):
            raise IndexError("start index is greather than length(a)")

        return True

    def diff(self, a, b, offset=0):
        """ Lookup for next different char sequence comparing 'a' to 'b'
        Both 'a' and 'b' should have the same length and offset value should be
        less than sequence length.

        :a: Sequence of chars to be compared to 'b' sequence
        :b: Sequence of chars to be compared to 'a' sequence
        :offset: Positive index of the position to start the difference lookup.
        :returns: The offset of next different char starting from 'offset'
        argument. If all char sequence 'a' is equals to 'b' sequence,
        it returns -1
        """
        assert self._validate_similar_sequence(a, b, offset)

        l = len(a)
        i = offset

        while i < l and a[i] == b[i]:
            i += 1

        return -1 if i == l else i

    def diff_length(self, a, b, offset):
        """ Calculates different chars sequence between strings 'a' and 'b',
        starting from a given 'offset'.

        Both 'a' and 'b' should have the same length and offset value should be
        less than sequence length.

        :a: Sequence of chars to be compared to 'b' sequence
        :b: Sequence of chars to be compared to 'a' sequence
        :offset: Positive index of the position to start the difference lookup.
        :returns: Length of the different chars following to the offset
        position of the sequence 'a'
        """
        assert self._validate_similar_sequence(a, b, offset)

        l = len(a)
        i = offset
        length = 0

        while i < l and a[i] != b[i]:
            length += 1
            i += 1

        return length
