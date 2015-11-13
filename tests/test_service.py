# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
import unittest


class TestService(unittest.TestCase):

    def test_index(self):
        from gisela.service import index
        assert index() == "My name is Gisela."


if __name__ == '__main__':
    unittest.main()
