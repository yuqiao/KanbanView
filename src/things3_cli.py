#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simple read-only Thing 3 CLI."""

from __future__ import print_function

__author__ = "Alexander Willner"
__copyright__ = "2020 Alexander Willner"
__credits__ = ["Alexander Willner"]
__license__ = "Apache"
__version__ = "0.0.1"
__maintainer__ = "Alexander Willner"
__email__ = "alex@willner.ws"
__status__ = "Development"

import argparse
import things3


class Things3CLI():
    """Simple read-only Thing 3 CLI."""

    def print_today(self):
        """Show Today."""
        tasks = things3.get_today()
        for task in tasks:
            print(' - ' + task[1])


def main(args):
    """ Main entry point of the app """
    if args.command == 'Today':
        Things3CLI().print_today()


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser()

    # Required positional argument
    PARSER.add_argument("command",
                        help="Inbox, Today, Scheduled, Waiting, ...")

    # Optional argument which requires a parameter (eg. -d test)
    PARSER.add_argument("-w", "--waiting", action="store", dest="waiting_tag")

    # Optional verbosity counter (eg. -v, -vv, -vvv, etc.)
    PARSER.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
        help="Verbosity (-v, -vv, etc)")

    # Specify output of "--version"
    PARSER.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    MYARGS = PARSER.parse_args()
    main(MYARGS)
