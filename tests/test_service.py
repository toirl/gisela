# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from gisela.model import Base, Tag, Timelog

engine = create_engine("sqlite:///:memory:", echo=False)
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()


def setup():
    t1 = Tag("Foo", "Foo description")
    t2 = Tag("Bar", "Baz description")
    t3 = Tag("Baz", "Baz description")
    session.add_all([t1, t2, t3])

    tl1 = Timelog(60)
    tl1.tags.append(t1)
    tl1.tags.append(t2)
    tl2 = Timelog(120)
    tl2.tags.append(t2)
    tl2.tags.append(t3)
    tl3 = Timelog(180)
    tl3.tags.append(t1)
    tl3.tags.append(t2)
    tl3.tags.append(t3)
    session.add_all([tl1, tl2, tl3])
    session.commit()


def teardown():
    session.query(Tag).delete()
    session.query(Timelog).delete()
    session.commit()


class TestService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        setup()

    @classmethod
    def tearDownClass(cls):
        teardown()

    def test_index(self):
        from gisela.service import index
        assert index(session) == "My name is Gisela."


class TestTagService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        setup()

    @classmethod
    def tearDownClass(cls):
        teardown()

    def test_list(self):
        from gisela.service import tag_list
        assert tag_list(session) == {}

    def test_create(self):
        from gisela.service import tag_create
        assert tag_create(session) == {}

    def test_read(self):
        from gisela.service import tag_read
        assert tag_read(1, session) == {}

    def test_update(self):
        from gisela.service import tag_update
        assert tag_update(1, session) == {}

    def test_delete(self):
        from gisela.service import tag_delete
        assert tag_delete(1, session) == {}


class TestTimeService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        setup()

    @classmethod
    def tearDownClass(cls):
        teardown()

    def test_list(self):
        from gisela.service import time_list
        assert time_list(session) == {}

    def test_create(self):
        from gisela.service import time_create
        assert time_create(session) == {}

    def test_read(self):
        from gisela.service import time_read
        assert time_read(1, session) == {}

    def test_update(self):
        from gisela.service import time_update
        assert time_update(1, session) == {}

    def test_delete(self):
        from gisela.service import time_delete
        assert time_delete(1, session) == {}

if __name__ == '__main__':
    unittest.main()
