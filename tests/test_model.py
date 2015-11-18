# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
import unittest
import datetime
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from gisela.model import Base, Tag, Timelog
from gisela.helpers import sum_times
from gisela.response import Response
 
engine = create_engine("sqlite:///:memory:", echo=False)
Base.metadata.create_all(engine)
session = sessionmaker(bind=engine)()

def setup():
    t1 = Tag("Foo", "Foo description")
    t2 = Tag("Bar", "Baz description")
    t3 = Tag("Baz", "Baz description")
    session.add_all([t1, t2, t3])

    tl1 = Timelog(datetime.datetime(2015, 11, 15), 60)
    tl1.tags.append(t1)
    tl1.tags.append(t2)
    tl2 = Timelog(datetime.datetime(2015, 11, 16), 120)
    tl2.tags.append(t2)
    tl2.tags.append(t3)
    tl3 = Timelog(datetime.datetime(2015, 11, 17), 180)
    tl3.tags.append(t1)
    tl3.tags.append(t2)
    tl3.tags.append(t3)
    session.add_all([tl1, tl2, tl3])
    session.commit()

def teardown():
    session.query(Tag).delete()
    session.query(Timelog).delete()
    session.commit()

class TestTagModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        setup()

    @classmethod
    def tearDownClass(cls):
        teardown()

    def setUp(self):
        pass

    def tearDown(self):
        session.rollback()

    def test_taglist(self):
        result = session.query(Tag).all()
        assert len(result) == 3

    def test_read(self):
        result = session.query(Tag).filter(Tag.id == 1).one()
        assert result.name == "Foo"
        assert result.description == "Foo description"

    def test_update(self):
        result = session.query(Tag).filter(Tag.id == 1).one()
        result.name = "Foo 2"
        result.description = "Foo description 2"
        session.flush()
        result = session.query(Tag).filter(Tag.id == 1).one()
        assert result.name == "Foo 2"
        assert result.description == "Foo description 2"

    def test_delete(self):
        session.query(Tag).filter(Tag.id == 1).delete()
        session.flush()
        result = session.query(Tag).all()
        assert len(result) == 2

    def test_create(self):
        tag = Tag("Qux", "Qux description")
        session.add(tag)
        result = session.query(Tag).all()
        assert len(result) == 4
        result = session.query(Tag).filter(Tag.id == 4).one()
        assert result.name == "Qux"
        assert result.description == "Qux description"


class TestTimeModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        setup()

    @classmethod
    def tearDownClass(cls):
        teardown()

    def setUp(self):
        pass

    def tearDown(self):
        session.rollback()

    def test_read(self):
        today = datetime.date(2015, 11, 15)
        result = session.query(Timelog).filter(Timelog.id == 1).one()
        assert result.duration == 60
        assert result.state == 0
        assert result.start_date.date() == today
        assert len(result.tags) == 2

    def test_list(self):
        result = session.query(Timelog).all()
        assert len(result) == 3

    def test_delete(self):
        result = session.query(Timelog).filter(Timelog.id == 1).delete()
        result = session.query(Timelog).all()
        assert len(result) == 2

    def test_create(self):
        t1 = Timelog()
        t2 = Timelog(datetime.datetime(2015,11,1), 50)
        session.add_all([t1, t2])
        result = session.query(Timelog).all()
        assert len(result) == 5
        result = session.query(Timelog).filter(Timelog.id == 5).one()
        assert result.duration == 50

    def test_sum_times(self):
        result = session.query(func.sum(Timelog.duration)).one()[0]
        assert result == 360

    def test_sum_tag1(self):
        assert 240 == sum_times(session, [1])

    def test_sum_tag2(self):
        assert 360 == sum_times(session, [2])

    def test_sum_tag3(self):
        assert 300 == sum_times(session, [3])

    def test_sum_tag1_3(self):
        assert 360 == sum_times(session, [1, 3])

    def test_startpausestop(self):
        result = session.query(Timelog).filter(Timelog.id == 1).one()
        result.start()
        assert result.state == 1
        time.sleep(1)
        result.pause()
        assert result.duration == 61
        assert result.state == 2
        result.start()
        time.sleep(4)
        result.stop()
        assert result.duration == 65
        assert result.state == 0

class TestSerializeModel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        setup()

    @classmethod
    def tearDownClass(cls):
        teardown()

    def setUp(self):
        pass

    def tearDown(self):
        session.rollback()

    def test_read(self):
        timelog = session.query(Timelog).filter(Timelog.id == 1).one()
        result = Response(timelog)
        assert result['data']['state'] == 0
        assert len(result['data']['tags']) == 2
        for tag in result['data']['tags']:
            if tag["id"] == 1:
                assert tag['name'] == "Foo"

if __name__ == '__main__':
    unittest.main()
