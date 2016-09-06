import datetime
import json
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relation
 
Base = declarative_base()
engine = create_engine("sqlite:///gisela.db", echo=True)

nm_tags_timelogs = Table('nm_tags_timelogs', Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id')),
    Column('task_id', Integer, ForeignKey('timelogs.id'))
)

nm_tags_timers = Table('nm_tags_timers', Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id')),
    Column('timer_id', Integer, ForeignKey('timers.id'))
)

class Tag(Base):
    """Tag"""
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    def __json__(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description
        }

    def __init__(self, name, description=None):
        self.name = name
        self.description = description


class Timer(Base):
    """Timer"""
    __tablename__ = "timers"
    id = Column(Integer, primary_key=True)
    description = Column(String)
    tags = relation(Tag, secondary=nm_tags_timers, backref="timers")

    def __json__(self):
        return {
            "id": self.id,
            "name": "Foo",
            "time": {"duration": 0, "state": 0},
            "description": self.description,
            "tags": [t.__json__() for t in self.tags]
        }

    def __init__(self, description=None):
        if description:
            self.description = description
        self.tags = []


class Timelog(Base):
    """Timelog"""
    __tablename__ = "timelogs"
    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    duration = Column(Integer, nullable=False, default=0)
    state = Column(Integer, nullable=False, default=0)
    description = Column(String)
    tags = relation(Tag, secondary=nm_tags_timelogs, backref="timelogs")

    def __json__(self):
        return {
            "id": self.id,
            "state": self.state,
            "duration": self.duration,
            "description": self.description,
            "start_date": str(self.start_date.date()),
            "week": self.week,
            "tags": [t.__json__() for t in self.tags]
        }

    def __init__(self, start_date=None, duration=None, description=None):
        if start_date is not None:
            if (isinstance(start_date, datetime.datetime)
                or isinstance(start_date, datetime.date)):
                self.start_date = start_date
            else:
                self.start_date = datetime.datetime.strptime(start_date, '%Y-%m-%d')
        if duration is not None:
            self.duration = int(duration)
        if description:
            self.description = description

    @property
    def week(self):
        """Will return the week of the year of the start_date"""
        return self.start_date.date().isocalendar()[1]

    def start(self, start=None):
        if not start:
            start = datetime.datetime.utcnow()
        self.start_date = start
        self.state = 1

    def pause(self, pause=None):
        if not pause:
            pause = datetime.datetime.utcnow()
        self.duration += (pause - self.start_date).seconds
        self.start_date = pause
        self.state = 2

    def stop(self, stop=None):
        if not stop:
            stop = datetime.datetime.utcnow()
        self.duration += (stop - self.start_date).seconds
        self.state = 0


def main():
    """Create the database and add data to it"""
    Base.metadata.create_all(engine)
    create_session = sessionmaker(bind=engine)
    session = create_session()
    session.add_all([])
    session.commit()

if __name__ == '__main__':
    main()
