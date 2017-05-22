import json
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

            self.write(json.dumps(diff))
        except KeyError as ke:
            self.set_status(404)
        self.flush()


class DiffApplication(object):

    """Docstring for DiffApplication. """
    def build(self, debug=False):
        diff_storage = {}
        endpoints = [
            (r"/v1/diff/(?P<id>[^$/]+)/?$", DiffApiEndpoint, {"diff_storage": diff_storage}),
            (r"/v1/diff/(?P<id>[^$/]+)/(?P<side>(?:left|right))/(?P<value>[0-9A-Za-z]+)$", DiffSideApiEndpoint, {"diff_storage": diff_storage}),
        ]
        return Application(endpoints, debug=debug)
