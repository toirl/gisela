# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
import unittest
from gisela.response import Success, Error, Fail


class TestTagModel(unittest.TestCase):

    def test_success(self):
        success = Success()
        result = success.serialize(None)
        assert result["status"] == "success"

    def test_fail(self):
        success = Fail()
        result = success.serialize(None)
        assert result["status"] == "fail"

    def test_error(self):
        success = Error()
        result = success.serialize(None)
        assert result["status"] == "error"
        assert result["message"] is None
        assert result["code"] is None


if __name__ == '__main__':
    unittest.main()
