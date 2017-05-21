from tornado.testing import AsyncHTTPTestCase

from leftright.api import DiffApplication, DiffApiEndpoint, DiffSideApiEndpoint


class TestLeftRightRestApi(AsyncHTTPTestCase):

    def get_app(self):
        return DiffApplication().build()

    def test_get_diff(self):
        id = "abc"
        resource_base = "/v1/diff/%s" % id

        response = self.fetch(resource_base)
        self.assertEqual(404, response.code, "diff :id should not exists")

        response = self.fetch(resource_base+"/left/contentleft", method="POST", body="")
        self.assertEqual(201, response.code)

        response = self.fetch(resource_base)
        self.assertEqual(424, response.code, "diff :id exists, but its content should be partial")

        response = self.fetch(resource_base+"/right/contentright", method="POST", body="")
        self.assertEqual(201, response.code)

        response = self.fetch(resource_base)
        self.assertEqual(200, response.code, "diff :id exists and should complete")
