# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
import unittest
import json
from gisela.response import Success, Error, Fail

class TestTagModel(unittest.TestCase):

    def test_success(self):
        success = Success()
        result = json.loads(success.serialize(None))
        assert result["status"] == "success"

    def test_fail(self):
        success = Fail()
        result = json.loads(success.serialize(None))
        assert result["status"] == "fail"

    def test_error(self):
        success = Error()
        result = json.loads(success.serialize(None))
        assert result["status"] == "error"
        assert result["message"] == None
        assert result["code"] == None


if __name__ == '__main__':
    unittest.main()
