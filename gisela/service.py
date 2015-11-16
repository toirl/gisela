from bottle import Bottle, run, request
from bottle.ext import sqlalchemy

from gisela.model import engine, Base, Tag
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
    #tag = db.query(Tag).filter(Tag.id == id).delete()
    response = Success()
    return response.serialize(None)


@app.get("/times")
def time_list(db):
    return {}


@app.post("/times")
def time_create(db):
    return {}


@app.get("/times/<id>")
def time_read(id, db):
    return {}


@app.put("/times/<id>")
def time_update(id, db):
    return {}


@app.delete("/times/<id>")
def time_delete(id, db):
    return {}


def main(host, port, debug=False):
    run(app, host=host, port=port, debug=debug)

if __name__ == '__main__':
    main("localhost", 8080)
