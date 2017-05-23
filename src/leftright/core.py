from leftright.compare import Base64Comparator


class LeftRightCore():

    STATE_COMPLETE="complete"
    STATE_PARTIAL_CONTENT="partial_content"
    RESULT_DIFF_EQUALS="equals"
    RESULT_DIFF_NOT_EQUALS="not_equals"
    RESULT_DIFF_INCONSISTENT="inconsistent"
    RESULT_DIFF_LENGTH_UNMATCH="lenght_unmatch"

    def __init__(self, store=None):
        self.store = {} if store is None else store

    def _set(self, id, qualifier, value):
        """
        Sets entry for concatenation of :id:qualifier.
        If value is None, it removes data associated data from storage
        """
        key = "%s:%s" % (id, qualifier)
        if value is None:
            if key in self.store:
                del self.store[key]
        else:
            self.store[key] = value

    def _get(self, id, qualifier):
        return self.store["%s:%s" % (id, qualifier)]

    def diff_length(self, id, offset=0):
        return Base64Comparator().diff_length(self.get_left(id), self.get_right(id), offset)

    def next_diff(self, id, offset=0):
        """
        Compare sequencie entries for given :id key.

        :id: key for left & right sequences.
        :offset: Positive index of the position to start the difference lookup.
        :returns: The index of the next different char between sentences.
        :raises:
            KeyError if :id:left or :id:right doesn't exists.
            AssertionError in case of :id:left and :id:right differs in length
        """
        return Base64Comparator().diff(self.get_left(id), self.get_right(id), offset)

    def set_left(self, id, value):
        """ Sets the value for left-side of comparison

        :id: key of diff case
        :value: sequences of characters to be compared to right-side

        """
        self._set(id, "left", value)

    def get_left(self, id):
        """ Returns the value of left-side of comparison

        :id: key of diff case
        :returns: left-side sequence chars for given :id key

        """
        return self._get(id, "left")

    def set_right(self, id, value):
        """ Sets the value for right-side of comparison

        :id: key of diff case
        :value: sequences of characters to be compared to left-side

        """
        self._set(id, "right", value)

    def get_right(self, id):
        """ Returns the value of right-side of comparison

        :id: key of diff case
        :returns: right-side sequence chars for given :id key

        """
        return self._get(id, "right")

    def get_diff(self, id):
        """Returns complete result for diff comparison between left-side and 
        right-side pair of char sequences

        :id: key of diff case
        :returns: complete report with possible states of comparison.
        :raises: KeyError if no sequences (left/right) were registered for this key

        """
        left_in = "%s:left"%id in self.store
        right_in = "%s:right"%id in self.store

        result = dict()

        if left_in and right_in:
            result["state"] = LeftRightCore.STATE_COMPLETE
        elif left_in or right_in:
            result["state"] = LeftRightCore.STATE_PARTIAL_CONTENT
        else:
            raise KeyError()

        result["left"] = dict(length=len(self.get_left(id))) if left_in else None
        result["right"] = dict(length=len(self.get_right(id))) if right_in else None
        result["compare"] = self.get_compare_report(id)

        return result

    def exists(self, id):
        left_in = "%s:left"%id in self.store
        right_in = "%s:right"%id in self.store
        return left_in or right_in

    def is_complete(self, id):
        left_in = "%s:left"%id in self.store
        right_in = "%s:right"%id in self.store
        return left_in and right_in

    def is_partial(self, id):
        return not self.is_complete(id)

    def get_compare_report(self, id):
        left_in = "%s:left"%id in self.store
        right_in = "%s:right"%id in self.store

        if left_in and right_in:
            try:
                diff_blocks = self.build_diff_blocks(id)
                if diff_blocks:
                    state = LeftRightCore.RESULT_DIFF_NOT_EQUALS
                else:
                    state = LeftRightCore.RESULT_DIFF_EQUALS
            except AssertionError:
                state = LeftRightCore.RESULT_DIFF_LENGTH_UNMATCH
                diff_blocks = []
        elif left_in or right_in:
            state = LeftRightCore.RESULT_DIFF_INCONSISTENT
            diff_blocks = []

        report = dict()
        report["state"] = state
        report["diff_blocks"] = diff_blocks
        return report

    def build_diff_blocks(self, id):
        blocks = []

        diff_idx = self.next_diff(id, offset=0)

        while diff_idx > -1:
            length = self.diff_length(id, offset=diff_idx)
            blocks.append({"offset": diff_idx, "length": length})

            # lookup for the next sequence
            next_offset = diff_idx+length
            try:
                diff_idx = self.next_diff(id, offset=next_offset)
            except IndexError:
                diff_idx = -1

        return blocks
