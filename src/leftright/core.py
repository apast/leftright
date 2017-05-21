class LeftRightCore():

    def __init__(self):
        self.store = {}

    def _set(self, id, qualifier, value):
        key = "%s:%s" % (id, qualifier)
        if value is None:
            del self.store[key]
        else:
            self.store[key] = value

    def _get(self, id, qualifier):
        return self.store["%s:%s" % (id, qualifier)]

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
