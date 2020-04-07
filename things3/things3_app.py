#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""KanbanView (app) for Things 3."""

from __future__ import print_function

# pylint: disable=duplicate-code
__author__ = "Luc Beaulieu and Alexander Willner"
__copyright__ = "Copyright 2018 Luc Beaulieu / 2020 Alexander Willner"
__credits__ = ["Luc Beaulieu", "Alexander Willner"]
__license__ = "unknown"
__version__ = "2.0.0"
__maintainer__ = "Alexander Willner"
__email__ = "alex@willner.ws"
__status__ = "Development"

import sys
from os import system
from threading import Thread
from time import sleep
import webbrowser
import things3.things3_api


FILE = "kanban.html"


def open_browser():
    """Delay opening the browser."""
    sleep(2)
    webbrowser.open('http://localhost:%s/%s' %
                    (things3.things3_api.PORT, FILE))


def main():
    """Run the app."""
    # kill possible zombie processes; can't use psutil in py2app context
    system('lsof -nti:' + str(things3.things3_api.PORT) +
           ' | xargs kill -9 ; sleep 1')

    try:
        httpd = things3.things3_api.setup()
        Thread(target=open_browser).start()
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("Shutting down...")
        httpd.shutdown()
        sys.exit(0)


if __name__ == "__main__":
    main()
