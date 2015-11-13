from bottle import Bottle, route, run
from bottle.ext import sqlalchemy

from gisela.model import engine, Base

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


@route("/")
def index():
    return "My name is Gisela."


@route("/tags", method="GET")
def tag_list():
    return {}


@route("/tags", method="POST")
def tag_create():
    return {}


@route("/tags/<id>", method="GET")
def tag_read():
    return {}


@route("/tags/<id>", method="PUT")
def tag_update():
    return {}


@route("/tags/<id>", method="DELETE")
def tag_delete():
    return {}


@route("/times", method="GET")
def time_list():
    return {}


@route("/times", method="POST")
def time_create():
    return {}


@route("/times/<id>", method="GET")
def time_read():
    return {}


@route("/times/<id>", method="PUT")
def time_update():
    return {}


@route("/times/<id>", method="DELETE")
def time_delete():
    return {}


def main(host, port, debug=False):
    run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main("localhost", 8080)
