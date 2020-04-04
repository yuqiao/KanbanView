#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""KanbanView Server for KanbanView for Things 3."""

from __future__ import print_function

__author__ = "Alexander Willner"
__copyright__ = "Copyright 2020 Alexander Willner"
__credits__ = ["Alexander Willner"]
__license__ = "MIT"
__version__ = "1.1.0"
__maintainer__ = "Alexander Willner"
__email__ = "alex@willner.ws"
__status__ = "Development"

from io import StringIO
from os.path import dirname, realpath
from os import system
from signal import signal, SIGINT
from threading import Thread
from time import sleep
import sys
import webbrowser
from wsgiref.simple_server import make_server
import falcon
import things3_to_kanban

FILE = 'kanban.html'
PATH = dirname(realpath(__file__)) + '/../resources/'
PORT = 8080
HTTPD = None


class ThingsKanbanAPI:
    """Simple KanbanView API."""

    def on_get(self, req, resp, url):
        """Handles GET requests"""

        if url == "kanban":
            resp.content_type = falcon.MEDIA_HTML
            output = StringIO()
            things3_to_kanban.write_html_columns(output)
            resp.data = output.getvalue().encode()
        else:
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
    # kill possible zombie processes; can't use psutil in py2app context
    system('lsof -nti:' + str(PORT) + ' | xargs kill -9 ; sleep 1')

    APP = falcon.App()
    APP.add_route('/{url}', ThingsKanbanAPI())

    HTTPD = make_server('', PORT, APP)
    print("Serving at http://localhost:%d/" % PORT)
    Thread(target=open_browser).start()
    HTTPD.serve_forever()
