import json
from tornado.testing import AsyncHTTPTestCase

from leftright.api import DiffApplication, DiffApiEndpoint, DiffSideApiEndpoint
from leftright.core import LeftRightCore


class TestLeftRightRestApi(AsyncHTTPTestCase):

    def get_app(self):
        return DiffApplication().build()

    def test_get_diff(self):
        id = "abc"
        resource_base = "/v1/diff/%s" % id
        left_content = "contentleft"
        right_content = "contentright"

        response = self.fetch(resource_base)
        self.assertEqual(404, response.code, "diff :id should not exists")

        response = self.fetch(resource_base+"/left/"+left_content, method="POST", body="")
        self.assertEqual(201, response.code)

        response = self.fetch(resource_base)
        self.assertEqual(424, response.code, "diff :id exists, but its content should be partial")

        response = self.fetch(resource_base+"/right/"+right_content, method="POST", body="")
        self.assertEqual(201, response.code)

        response = self.fetch(resource_base)
        self.assertEqual(200, response.code, "diff :id exists and should complete")

        response_json = json.loads(response.body)
        self.assertEqual(LeftRightCore.STATE_COMPLETE, response_json["state"])
        self.assertDictEqual({"length": len(left_content)}, response_json["left"])
        self.assertDictEqual({"length": len(right_content)}, response_json["right"])
        self.assertDictEqual({"state": LeftRightCore.RESULT_DIFF_LENGTH_UNMATCH, "diff_blocks": []}, response_json["compare"])
