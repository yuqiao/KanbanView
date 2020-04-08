#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""KanbanView (app) for Things 3."""

from __future__ import print_function

# pylint: disable=duplicate-code
__author__ = "Luc Beaulieu and Alexander Willner"
__copyright__ = "Copyright 2018 Luc Beaulieu / 2020 Alexander Willner"
__credits__ = ["Luc Beaulieu", "Alexander Willner"]
__license__ = "Apache License 2.0"
__version__ = "2.0.1"
__maintainer__ = "Alexander Willner"
__email__ = "alex@willner.ws"
__status__ = "Development"

import sys
from os import system
from threading import Thread
import webbrowser
import things3.things3_api as things3_api


FILE = "kanban.html"


def open_browser():
    """Delay opening the browser."""
    webbrowser.open('http://localhost:%s/%s' %
                    (things3_api.PORT, FILE))


def main():
    """Run the app."""
    # kill possible zombie processes; can't use psutil in py2app context
    system('lsof -nti:' + str(things3_api.PORT) +
           ' | xargs kill -9')

    try:
        Thread(target=open_browser).start()
        things3_api.APP.run(port=things3_api.PORT)
    except KeyboardInterrupt:
        print("Shutting down...")
        sys.exit(0)


if __name__ == "__main__":
    main()
