#!/usr/bin/env python
# encoding: utf-8
from bottle import run
from gisela.service import app

def main(host="localhost", port=8080, debug=False):
    run(app, host=host, port=port, debug=debug)

if __name__ == '__main__':
    main("localhost", 8080)
