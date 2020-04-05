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
from wsgiref.simple_server import make_server
import falcon
from things3 import Things3

PORT = 8088
APP = falcon.App()
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
        if filename.endswith('ico'):
            resp.content_type = 'image/x-ico'
        with open(filename, 'rb') as source:
            resp.data = source.read()


class ThingsAPI:
    """Simple read-only Things API."""

    things3 = Things3()

    def on_get(self, req, resp, command):
        """Handles GET requests"""
        if command == "inbox":
            resp.media = self.things3.convert_tasks_to_model(
                self.things3.get_inbox())
        elif command == "today":
            resp.media = self.things3.convert_tasks_to_model(
                self.things3.get_today())
        elif command == "next":
            resp.media = self.things3.convert_tasks_to_model(
                self.things3.get_anytime())
        elif command == "backlog":
            resp.media = self.things3.convert_tasks_to_model(
                self.things3.get_someday())
        elif command == "upcoming":
            resp.media = self.things3.convert_tasks_to_model(
                self.things3.get_upcoming())
        elif command == "waiting":
            resp.media = self.things3.convert_tasks_to_model(
                self.things3.get_waiting())
        elif command == "mit":
            resp.media = self.things3.convert_tasks_to_model(
                self.things3.get_mit())
        elif command == "completed":
            resp.media = self.things3.convert_tasks_to_model(
                self.things3.get_completed())
        elif command == "cancelled":
            resp.media = self.things3.convert_tasks_to_model(
                self.things3.get_cancelled())
        else:
            resp.media = self.things3.convert_tasks_to_model(
                self.things3.get_not_implemented())
            resp.status = falcon.HTTP_404


def setup():
    APP.add_route('/api/{command}', ThingsAPI())
    APP.add_route('/{url}', ThingsGUI())
    HTTPD = make_server('', PORT, APP)
    print("Serving API at http://localhost:%d/api/{command}" % PORT)
    return HTTPD


def main():
    print("Starting up...")
    HTTPD = setup()

    try:
        HTTPD.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down...")
        HTTPD.server_close()
        sys.exit(0)


if __name__ == "__main__":
    main()
