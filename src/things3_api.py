#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simple read-only Things 3 Web Serivce."""

from __future__ import print_function

__author__ = "Alexander Willner"
__copyright__ = "Copyright 2020 Alexander Willner"
__credits__ = ["Alexander Willner"]
__license__ = "MIT"
__version__ = "2.0.0"
__maintainer__ = "Alexander Willner"
__email__ = "alex@willner.ws"
__status__ = "Development"

from os import sys
from os.path import dirname, realpath
from signal import signal, SIGINT
from threading import Thread
from time import sleep
import webbrowser
from wsgiref.simple_server import make_server
import falcon
import things3

FILE = "kanban2.html"
PORT = 8088
HTTPD = None
PATH = dirname(realpath(__file__)) + '/../resources/'


class ThingsGUI:
    """Simple read-only Things KanbanView."""

    def on_get(self, req, resp, url):
        """Handles GET requests"""
        filename = PATH + url
        resp.status = falcon.HTTP_200
        if filename.endswith('css'):
            resp.content_type = 'text/css'
        if filename.endswith('html'):
            resp.content_type = falcon.MEDIA_HTML
        if filename.endswith('js'):
            resp.content_type = falcon.MEDIA_JS
        if filename.endswith('png'):
            resp.content_type = falcon.MEDIA_PNG
        if filename.endswith('jpg'):
            resp.content_type = falcon.MEDIA_JPEG
        with open(filename, 'rb') as source:
            resp.data = source.read()


class ThingsAPI:
    """Simple read-only Things API."""

    def on_get(self, req, resp, command):
        """Handles GET requests"""
        if command == "inbox":
            resp.media = things3.convert_tasks_to_model(things3.get_inbox())
        elif command == "today":
            resp.media = things3.convert_tasks_to_model(things3.get_today())
        else:
            resp.media = things3.convert_tasks_to_model(
                things3.get_not_implemented())
            resp.status = falcon.HTTP_404


def open_browser():
    """Delay opening the browser."""
    sleep(1)
    webbrowser.open('http://localhost:%s/%s' % (PORT, FILE))


def handler(signal_received, frame):
    """Handle any cleanup here."""
    print("Shutting down...: " + str(signal_received) + " / " + str(frame))
    HTTPD.server_close()
    sys.exit(0)


if __name__ == "__main__":
    print("Starting up...")
    signal(SIGINT, handler)

    APP = falcon.App()
    APP.add_route('/api/{command}', ThingsAPI())
    APP.add_route('/{url}', ThingsGUI())

    HTTPD = make_server('', PORT, APP)
    print("Serving at http://localhost:%d/api/{command}" % PORT)
    Thread(target=open_browser).start()
    HTTPD.serve_forever()
