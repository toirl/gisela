import datetime
from sqlalchemy import create_engine, Column, Integer, String, DateTime, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relation
 
Base = declarative_base()
engine = create_engine("sqlite:///gisela.db", echo=True)

nm_tags_timelogs = Table('nm_tags_timelogs', Base.metadata,
    Column('tag_id', Integer, ForeignKey('tags.id')),
    Column('task_id', Integer, ForeignKey('timelogs.id'))
)

class Tag(Base):
    """Tag"""
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    description = Column(String, nullable=False)

    def __init__(self, name, description=None):
        self.name = name
        self.description = description

class Timelog(Base):
    """Timelog"""
    __tablename__ = "timelogs"
    id = Column(Integer, primary_key=True)
    start_date = Column(DateTime, nullable=False, default=datetime.datetime.utcnow)
    duration = Column(Integer, nullable=False, default=0)
    state = Column(Integer, nullable=False, default=0)
    description = Column(String)
    tags = relation(Tag, secondary=nm_tags_timelogs, backref="timelogs")

    def __init__(self, duration=None):
        if duration is None:
            duration = 0
        self.duration = duration

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
