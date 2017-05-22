# coding=utf8

import json
import unittest

from tornado.testing import AsyncHTTPTestCase

from leftright.api import DiffApplication, DiffApiEndpoint, DiffSideApiEndpoint, is_base64
from leftright.core import LeftRightCore


class TestBase64Check(unittest.TestCase):

    def test_valid_base64_strings(self):
        self.assertTrue(is_base64(b"ZGF0YSB0byBiZSBlbmNvZGVk"))

    def test_invalid_base64_strings(self):
        self.assertFalse(is_base64(b" "))
        self.assertFalse(is_base64(b"a a"))
        self.assertFalse(is_base64(u"á"))
        self.assertFalse(is_base64(u"áć"))


class TestLeftRightRestApi(AsyncHTTPTestCase):

    def get_app(self):
        return DiffApplication().build()

    def test_set_invalid_base64_sequences(self):
        id="abc"
        resource_base = "/v1/diff/%s" % id

        response = self.fetch(resource_base+"/left/jbahjbh", method="POST", body="")
        self.assertEqual(400, response.code)

        response = self.fetch(resource_base+"/right/iojhquiojhuiwqhui", method="POST", body="")
        self.assertEqual(400, response.code)

    def test_get_diff_side(self):
        id = "abc"
        resource_base = "/v1/diff/%s" % id
        left_content = "Y29udGVudHJpa25hc2tqZGxhbWRsa3Nh"
        right_content = "Y29udGVudHJpZ2h0"

        response = self.fetch(resource_base+"/left", method="GET")
        self.assertEqual(404, response.code)

        response = self.fetch(resource_base+"/right", method="GET")
        self.assertEqual(404, response.code)

        response = self.fetch(resource_base+"/left/"+left_content, method="POST", body="")
        self.assertEqual(201, response.code)

        response = self.fetch(resource_base+"/left", method="GET")
        self.assertEqual(200, response.code)
        self.assertEqual("application/json", response.headers["Content-Type"])
        self.assertDictEqual({"length": len(left_content), "content": left_content}, json.loads(response.body))

        response = self.fetch(resource_base+"/right/"+right_content, method="POST", body="")
        self.assertEqual(201, response.code)

        response = self.fetch(resource_base+"/right", method="GET")
        self.assertEqual(200, response.code)
        self.assertEqual("application/json", response.headers["Content-Type"])
        self.assertDictEqual({"length": len(right_content), "content": right_content}, json.loads(response.body))

    def test_get_diff(self):
        id = "abc"
        resource_base = "/v1/diff/%s" % id
        left_content = "Y29udGVudHJpa25hc2tqZGxhbWRsa3Nh"
        right_content = "Y29udGVudHJpZ2h0"

        response = self.fetch(resource_base)
        self.assertEqual(404, response.code, "diff :id should not exists")

        response = self.fetch(resource_base+"/left/"+left_content, method="POST", body="")
        self.assertEqual(201, response.code)

        response = self.fetch(resource_base)
        self.assertEqual("application/json", response.headers["Content-Type"])
        self.assertEqual(424, response.code, "diff :id exists, but its content should be partial")

        response = self.fetch(resource_base+"/right/"+right_content, method="POST", body="")
        self.assertEqual(201, response.code)

        response = self.fetch(resource_base)
        self.assertEqual("application/json", response.headers["Content-Type"])
        self.assertEqual(200, response.code, "diff :id exists and should complete")

        response_json = json.loads(response.body)
        self.assertEqual(LeftRightCore.STATE_COMPLETE, response_json["state"])
        self.assertDictEqual({"length": len(left_content)}, response_json["left"])
        self.assertDictEqual({"length": len(right_content)}, response_json["right"])
        self.assertDictEqual({"state": LeftRightCore.RESULT_DIFF_LENGTH_UNMATCH, "diff_blocks": []}, response_json["compare"])
