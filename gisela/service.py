from bottle import route, run


@route("/")
def index():
    return "My name is Gisela."


def main(host, port, debug=False):
    run(host=host, port=port, debug=debug)

if __name__ == '__main__':
    main("localhost", 8080)
