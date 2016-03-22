import datetime
from bottle import Bottle, request, response, HTTPResponse
from bottle.ext import sqlalchemy
from bottle import static_file

from gisela.model import engine, Base, Tag, Timelog, Timer
from gisela.response import Response

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


@app.hook('after_request')
def enable_cors():
    """
    You need to add some headers to each request.
    Don't use the wildcard '*' for Access-Control-Allow-Origin in production.
    """
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'PUT, GET, POST, DELETE, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Origin, Accept, Content-Type, X-Requested-With, X-CSRF-Token'

@app.route('/demo/<filename>')
def server_static(filename):
        return static_file(filename, root='./demo')


@app.get("/")
def index(db):
    return "My name is Gisela."


@app.route("/tags", method=["OPTIONS"])
@app.route("/tags/<id>", method=["OPTIONS"])
@app.route("/times", method=["OPTIONS"])
@app.route("/timers", method=["OPTIONS"])
@app.route("/timers/<id>", method=["OPTIONS"])
def allow_options(id=None):
    return {}


@app.post("/timers")
def timer_create(db):
    timer = Timer(request.json.get("description", ""))
    db.add(timer)
    db.commit()
    return Response(timer)


@app.get("/timers")
def timer_list(db):
    tags = db.query(Timer).all()
    return Response(tags)


@app.put("/timers/<id>")
def timer_update(id, db):
    timer = db.query(Timer).filter(Timer.id == id).one()
    timer.description = request.json.get("description", timer.description)
    timer.tags = []
    tags = request.json.get("tags", [])
    for tag in tags:
        tag = db.query(Tag).filter(Tag.id == tag.get("id")).one()
        timer.tags.append(tag)
    db.commit()
    return Response(timer)


@app.delete("/timers/<id>")
def timer_delete(id, db):
    timer = db.query(Timer).filter(Timer.id == id).delete()
    db.commit()
    return Response(timer)


@app.get("/tags")
def tag_list(db):
    tags = db.query(Tag).all()
    return Response(tags)


@app.post("/tags")
def tag_create(db):
    tag = Tag(request.json.get("name"),
              request.json.get("description", ""))
    db.add(tag)
    db.commit()
    return Response(tag)


@app.get("/tags/<id>")
def tag_read(id, db):
    tag = db.query(Tag).filter(Tag.id == id).one()
    return Response(tag)


@app.put("/tags/<id>")
def tag_update(id, db):
    tag = db.query(Tag).filter(Tag.id == id).one()
    tag.name = request.json.get("name", tag.name)
    tag.description = request.json.get("description", tag.description)
    db.commit()
    return Response(tag)


@app.delete("/tags/<id>")
def tag_delete(id, db):
    tag = db.query(Tag).filter(Tag.id == id).delete()
    db.commit()
    return Response(tag)


@app.get("/times")
def time_list(db):
    times = db.query(Timelog).all()
    return Response(times)


@app.post("/times")
def time_create(db):
    time = Timelog(request.json.get("start_date"),
                   request.json.get("duration"),
                   request.json.get("description"))
    # Add tags to the timelog
    for tagdata in request.json.get("tags", []):
        tag = db.query(Tag).filter(Tag.id == tagdata.get("id")).one()
        time.tags.append(tag)
    db.add(time)
    db.commit()
    return Response(time)


@app.get("/times/<id>")
def time_read(id, db):
    time = db.query(Timelog).filter(Timelog.id == id).one()
    return Response(time)


@app.put("/times/<id>")
def time_update(id, db):
    time = db.query(Timelog).filter(Timelog.id == id).one()
    start_date = request.json.get("start_date")
    if start_date:
        start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
        time.start_date = start_date
    time.duration = int(request.json.get("duration", time.duration))
    time.description = request.json.get("description", time.description)
    # Add/Remove tags
    tag_ids = request.json.get("tags", [])
    if tag_ids:
        time.tags = []
        for tag_id in tag_ids:
            tag = db.query(Tag).filter(Tag.id == tag_id).one()
            time.tags.append(tag)
    db.commit()
    return Response(time)


@app.delete("/times/<id>")
def time_delete(id, db):
    time = db.query(Timelog).filter(Timelog.id == id).delete()
    db.commit()
    return HTTPResponse(None, "204 OK")

@app.put("/times/<id>/start")
def time_start(id, db):
    time = db.query(Timelog).filter(Timelog.id == id).one()
    time.start()
    db.commit()
    return Response(time)

@app.put("/times/<id>/pause")
def time_pause(id, db):
    time = db.query(Timelog).filter(Timelog.id == id).one()
    time.pause()
    db.commit()
    return Response(time)

@app.put("/times/<id>/stop")
def time_stop(id, db):
    time = db.query(Timelog).filter(Timelog.id == id).one()
    time.stop()
    db.commit()
    return Response(time)
