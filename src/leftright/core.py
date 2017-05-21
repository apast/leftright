from leftright.compare import Base64Comparator


class LeftRightCore():

    STATE_COMPLETE="complete"
    STATE_PARTIAL_CONTENT="partial_content"
    RESULT_DIFF_EQUALS="equals"
    RESULT_DIFF_NOT_EQUALS="not_equals"
    RESULT_DIFF_INCONSISTENT="inconsistent"

    def __init__(self, store=None):
        self.store = {} if store is None else store

    def _set(self, id, qualifier, value):
        """
        Sets entry for concatenation of :id:qualifier.
        If value is None, it removes data associated data from storage
        """
        key = "%s:%s" % (id, qualifier)
        if value is None:
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
        """TODO: Docstring for set_rigth.

        :id: TODO
        :value: TODO

        """
        self._set(id, "left", value)

    def get_left(self, id):
        """TODO: Docstring for set_rigth.

        :id: TODO
        :returns: left-side sequence chars for given :id key

        """
        return self._get(id, "left")

    def set_right(self, id, value):
        """TODO: Docstring for set_rigth.

        :id: TODO
        :value: TODO

        """
        self._set(id, "right", value)

    def get_right(self, id):
        """TODO: Docstring for set_rigth.

        :id: TODO
        :returns: right-side sequence chars for given :id key

        """
        return self._get(id, "right")

    def get_diff(self, id):
        """TODO: Docstring for get_diff.

        :id: diff ID
        :returns: TODO

        """
        left_in = "%s:left"%id in self.store
        right_in = "%s:right"%id in self.store

        result = dict()
        import json

        if left_in and right_in:
            state = "ok"
            return dict(state=state)
        elif left_in or right_in:
            return dict(state="partial_content")
        else:
            raise KeyError()
