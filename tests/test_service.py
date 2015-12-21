# the inclusion of the tests module is not meant to offer best practices for
# testing in general, but rather to support the `find_packages` example in
# setup.py that excludes installing the "tests" package
import datetime
import unittest
from webtest import TestApp
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


class TestService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import gisela
        setup()
        cls.app = TestApp(gisela.app)

    @classmethod
    def tearDownClass(cls):
        teardown()

    def test_index(self):
        response = self.app.get("/")
        assert response.status == '200 OK'
        assert "My name is Gisela." in response


class TestTagService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import gisela
        setup()
        cls.app = TestApp(gisela.app)

    @classmethod
    def tearDownClass(cls):
        teardown()

    def test_list(self):
        response = self.app.get("/tags")
        assert response.status == '200 OK'

    def test_create(self):
        response = self.app.post_json("/tags",
                                 {"name": "New",
                                  "description": "New description"})
        assert response.status == '201 OK'

    def test_read(self):
        response = self.app.get("/tags/1")
        assert response.status == '200 OK'

    def test_update(self):
        response = self.app.put_json("/tags/1",
                                    {"name": "Foo2",
                                     "description": "Changed description"})
        assert response.status == '200 OK'
        assert response.json["data"]["name"] == "Foo2"

    def test_delete(self):
        response = self.app.delete_json("/tags/3")
        assert response.status == '204 OK'


class TestTimeService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        import gisela
        setup()
        cls.app = TestApp(gisela.app)

    @classmethod
    def tearDownClass(cls):
        teardown()

    def test_list(self):
        response = self.app.get("/times")
        assert response.status == '200 OK'

    def test_create(self):
        from datetime import datetime
        response = self.app.post_json("/times",
                                      {"name": "Bar",
                                       "start_date": "2015-11-18",
                                       "duration": 50,
                                       "description": "Bar description",
                                       "tags": [1, 2]})
        assert response.status == '201 OK'

    def test_read(self):
        response = self.app.get("/times/1")
        assert response.status == '200 OK'

    def test_update(self):
        response = self.app.put_json("/times/1",
                                     {"name": "Bar",
                                      "start_date": "2015-11-01",
                                      "duration": 50,
                                      "description": "Changed",
                                      "tags": [1]})
        assert response.status == '200 OK'
        assert response.json["data"]["start_date"].find("2015-11-01") > -1
        assert response.json["data"]["duration"] == 50
        assert response.json["data"]["description"] == "Changed"
        assert len(response.json["data"]["tags"]) == 1

    def test_delete(self):
        response = self.app.delete_json("/times/3")
        assert response.status == '204 OK'

    def test_start(self):
        response = self.app.put_json("/times/1/start")
        assert response.json["data"]["state"] == 1
        assert response.status == '200 OK'
        response = self.app.put("/times/1/stop")

    def test_pause(self):
        response = self.app.put_json("/times/1/start")
        response = self.app.put_json("/times/1/pause")
        assert response.json["data"]["state"] == 2
        assert response.status == '200 OK'
        response = self.app.put_json("/times/1/stop")
        assert response.status == '200 OK'

    def test_stop(self):
        response = self.app.put_json("/times/1/start")
        response = self.app.put_json("/times/1/stop")
        assert response.json["data"]["state"] == 0
        assert response.status == '200 OK'

if __name__ == '__main__':
    unittest.main()
