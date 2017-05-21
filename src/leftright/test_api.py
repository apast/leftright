from tornado.testing import AsyncHTTPTestCase
from tornado.web import Application

from leftright.api import DiffApiEndpoint, DiffSideApiEndpoint


class TestLeftRightRestApi(AsyncHTTPTestCase):

    def get_app(self):
        diff_storage = {}
        endpoints = [
            (r"/v1/diff/(?P<id>[^$/]+)/?$", DiffApiEndpoint, {"diff_storage": diff_storage}),
            (r"/v1/diff/(?P<id>[^$/]+)/(?P<side>(?:left|right))/(?P<value>[0-9A-Za-z]+)$", DiffSideApiEndpoint, {"diff_storage": diff_storage}),
        ]
        return Application(endpoints)

    def test_get_diff(self):
        id = "abc"
        resource_base = "/v1/diff/%s" % id

        response = self.fetch(resource_base)
        self.assertEqual(404, response.code)

        response = self.fetch(resource_base+"/left/contentleft", method="POST", body="")
        self.assertEqual(201, response.code)

        response = self.fetch(resource_base)
        self.assertEqual(424, response.code, "Response code should be compatible with Partial Content, when one side of diff is invalid")

        response = self.fetch(resource_base+"/right/contentright", method="POST", body="")
        self.assertEqual(201, response.code)

        response = self.fetch(resource_base)
        self.assertEqual(200, response.code, "Diff was found and is complete")
