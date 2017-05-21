from tornado.web import Application, RequestHandler

from leftright.core import LeftRightCore


class DiffSideApiEndpoint(RequestHandler):

    def initialize(self, diff_storage):
        self.core = LeftRightCore(diff_storage)

    def post(self, id, side, value):
        if "left" == side:
            self.core.set_left(id, value)
        else:
            self.core.set_right(id, value)

        self.set_status(201)


class DiffApiEndpoint(RequestHandler):

    def initialize(self, diff_storage):
        self.core = LeftRightCore(diff_storage)

    def get(self, id):
        """ Returns diff report for a given diff :id

        :id: diff id
        :returns: diff report
        """

        try:
            diff = self.core.get_diff(id)
            if diff["state"] == LeftRightCore.STATE_PARTIAL_CONTENT:
                self.set_status(424)
            else:
                self.set_status(200)
        except KeyError as ke:
            self.set_status(404)
        self.flush()
