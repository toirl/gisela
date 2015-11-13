# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
import unittest


class TestService(unittest.TestCase):

    def test_index(self):
        from gisela.service import index
        assert index() == "My name is Gisela."


class TestTagService(unittest.TestCase):

    def test_list(self):
        from gisela.service import tag_list
        assert tag_list() == {}

    def test_create(self):
        from gisela.service import tag_create
        assert tag_create() == {}

    def test_read(self):
        from gisela.service import tag_read
        assert tag_read() == {}

    def test_update(self):
        from gisela.service import tag_update
        assert tag_update() == {}

    def test_delete(self):
        from gisela.service import tag_delete
        assert tag_delete() == {}


class TestTimeService(unittest.TestCase):

    def test_list(self):
        from gisela.service import time_list
        assert time_list() == {}

    def test_create(self):
        from gisela.service import time_create
        assert time_create() == {}

    def test_read(self):
        from gisela.service import time_read
        assert time_read() == {}

    def test_update(self):
        from gisela.service import time_update
        assert time_update() == {}

    def test_delete(self):
        from gisela.service import time_delete
        assert time_delete() == {}

if __name__ == '__main__':
    unittest.main()
