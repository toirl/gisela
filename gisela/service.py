import datetime
from bottle import Bottle, run, request
from bottle.ext import sqlalchemy

from gisela.model import engine, Base, Tag, Timelog
from gisela.response import Success

# --------------------------------
# Add SQLAlchemy app
# --------------------------------
app = Bottle()

plugin = sqlalchemy.Plugin(
        engine,
        Base.metadata,
        keyword='db',
        create=True,
        commit=True,
        use_kwargs=False
)
app.install(plugin)


@app.get("/")
def index(db):
    return "My name is Gisela."


@app.get("/tags")
def tag_list(db):
    tags = db.query(Tag).all()
    response = Success()
    return response.serialize(tags)


@app.post("/tags")
def tag_create(db):
    tag = Tag(request.params.get("name"),
              request.params.get("description"))
    db.add(tag)
    db.commit()
    response = Success()
    return response.serialize(tag)


@app.get("/tags/<id>")
def tag_read(id, db):
    tag = db.query(Tag).filter(Tag.id == id).one()
    response = Success()
    return response.serialize(tag)


@app.put("/tags/<id>")
def tag_update(id, db):
    tag = db.query(Tag).filter(Tag.id == id).one()
    tag.name = request.params.get("name", tag.name)
    tag.description = request.params.get("description", tag.description)
    db.commit()
    response = Success()
    return response.serialize(tag)


@app.delete("/tags/<id>")
def tag_delete(id, db):
    tag = db.query(Tag).filter(Tag.id == id).delete()
    response = Success()
    db.commit()
    return response.serialize(None)


@app.get("/times")
def time_list(db):
    times = db.query(Timelog).all()
    response = Success()
    return response.serialize(times)


@app.post("/times")
def time_create(db):
    time = Timelog(request.params.get("start_date"),
                   request.params.get("duration"),
                   request.params.get("description"))

    db.add(time)
    db.commit()
    response = Success()
    return response.serialize(time)


@app.get("/times/<id>")
def time_read(id, db):
    time = db.query(Timelog).filter(Timelog.id == id).one()
    response = Success()
    return response.serialize(time)


@app.put("/times/<id>")
def time_update(id, db):
    time = db.query(Timelog).filter(Timelog.id == id).one()
    start_date = request.params.get("start_date")
    if start_date:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        time.start_date = start_date
    time.duration = int(request.params.get("duration", time.duration))
    time.description = request.params.get("description", time.description)
    db.commit()
    response = Success()
    return response.serialize(time)


@app.delete("/times/<id>")
def time_delete(id, db):
    time = db.query(Timelog).filter(Timelog.id == id).delete()
    db.commit()
    response = Success()
    return response.serialize(None)

@app.put("/times/<id>/start")
def time_delete(id, db):
    time = db.query(Timelog).filter(Timelog.id == id).one()
    time.start()
    db.commit()
    response = Success()
    return response.serialize(time)

@app.put("/times/<id>/pause")
def time_delete(id, db):
    time = db.query(Timelog).filter(Timelog.id == id).one()
    time.pause()
    db.commit()
    response = Success()
    return response.serialize(time)

@app.put("/times/<id>/stop")
def time_delete(id, db):
    time = db.query(Timelog).filter(Timelog.id == id).one()
    time.stop()
    db.commit()
    response = Success()
    return response.serialize(time)

def main(host, port, debug=False):
    run(app, host=host, port=port, debug=debug)

if __name__ == '__main__':
    main("localhost", 8080)
