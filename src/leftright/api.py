import base64
import json
from tornado.concurrent import return_future
from tornado.gen import coroutine
from tornado.web import Application, RequestHandler, HTTPError

from leftright.core import LeftRightCore


def is_base64(string):
    """ Check if :string base64 decoded
    :returns: True if string is base64 encoded. False, otherwise
    """
    try:
        return base64.b64decode(string)
    except:
        return False


class DiffSideApiEndpoint(RequestHandler):

    def initialize(self, diff_storage):
        self.core = LeftRightCore(diff_storage)

    @return_future
    def get_content(self, id, side, callback=None):
        if side == "left":
            callee = self.core.get_left
        else:
            callee = self.core.get_right

        data = callee(id)
        data_dict = {"length": len(data), "content": data}
        callback(data_dict)

    @coroutine
    def get(self, id, side):
        try:
            data_dict = yield self.get_content(id, side)
            self.set_status(200)
            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(data_dict))
        except KeyError as ke:
            self.set_status(404, "diff side not found for %s:%s" % (id, side))
            self.write_error(404)
        self.flush()

    @coroutine
    def post(self, id, side, value):
        if is_base64(value):
            yield self.save_content(id, side, value)
            self.set_status(201, "Created")
        else:
            self.set_status(400, "Malformed request. :value should be base64 encoded.")
            self.write_error(404)
        self.flush()

    @return_future
    def save_content(self, id, side, value, callback=None):
        if "left" == side:
            self.core.set_left(id, value)
        else:
            self.core.set_right(id, value)
        callback()



class DiffApiEndpoint(RequestHandler):

    def initialize(self, diff_storage):
        self.core = LeftRightCore(diff_storage)

    @return_future
    def get_diff(self, id, callback=None):
        diff = self.core.get_diff(id)
        callback(diff)

    @coroutine
    def get(self, id):
        """ Returns diff report for a given diff :id

        :id: diff id
        :returns: diff report
        """

        try:
            diff = yield self.get_diff(id)

            if diff["state"] == LeftRightCore.STATE_PARTIAL_CONTENT:
                self.set_status(424)
            else:
                self.set_status(200)

            self.set_header("Content-Type", "application/json")
            self.write(json.dumps(diff))
        except KeyError as ke:
            self.set_status(404, "diff not found for key[%s]"%id)
            self.write_error(404)
        self.flush()


class DiffApplication(object):

    """Docstring for DiffApplication. """
    def build(self, debug=False):
        diff_storage = {}
        endpoints = [
            (r"/v1/diff/(?P<id>[^$/]+)/?$", DiffApiEndpoint, {"diff_storage": diff_storage}),
            (r"/v1/diff/(?P<id>[^$/]+)/(?P<side>(?:left|right))/(?P<value>[0-9A-Za-z]+)$", DiffSideApiEndpoint, {"diff_storage": diff_storage}),
            (r"/v1/diff/(?P<id>[^$/]+)/(?P<side>(?:left|right))$", DiffSideApiEndpoint, {"diff_storage": diff_storage}),
        ]
        return Application(endpoints, debug=debug)
