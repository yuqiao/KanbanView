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

    @classmethod
    def print_tasks(cls, tasks):
        """Print a task."""
        for task in tasks:
            print(' - ' + task[1])

    def print_today(self):
        """Show Today."""
        self.print_tasks(things3.get_today())

    def print_inbox(self):
        """Show Inbox."""
        self.print_tasks(things3.get_inbox())

    @classmethod
    def print_unimplemented(cls):
        """Show warning that method is not yet implemented."""
        print("not implemented yet")


def main(args):
    """ Main entry point of the app """
    COMMANDS[args.command][1]()


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(
        formatter_class=argparse.RawTextHelpFormatter)
    COMMANDS = {
        'inbox': ['Shows all inbox tasks',
                  Things3CLI().print_inbox],
        'today': ['Shows all todays tasks ordered by index',
                  Things3CLI().print_today],
        'upcoming': ['Shows all upcoming tasks ordered by date',
                     Things3CLI().print_unimplemented],
        'next': ['Shows all next tasks',
                 Things3CLI().print_unimplemented],
        'someday': ['Shows all someday tasks',
                    Things3CLI().print_unimplemented],
        'completed': ['Shows all completed tasks',
                      Things3CLI().print_unimplemented],
        'cancelled': ['Shows all cancelled tasks ordered by cancel date',
                      Things3CLI().print_unimplemented],
        'trashed': ['Shows all trashed tasks',
                    Things3CLI().print_unimplemented],
        'feedback': ['Opens the feedback web page to propose changes',
                     Things3CLI().print_unimplemented],
        'all': ['Shows all tasks',
                Things3CLI().print_unimplemented],
        'csv': ['Exports all tasks as semicolon seperated values',
                Things3CLI().print_unimplemented],
        'due': ['Shows all tasks ordered by due date',
                Things3CLI().print_unimplemented],
        'headings': ['Shows all headings',
                     Things3CLI().print_unimplemented],
        'hours': ['Shows how many hours of work have been planned for today',
                  Things3CLI().print_unimplemented],
        'ical': ['Shows all tasks ordered by due date as iCal',
                 Things3CLI().print_unimplemented],
        'logbook': ['Shows all tasks completed today',
                    Things3CLI().print_unimplemented],
        'mostClosed': ['Shows all days on which most tasks were closed',
                       Things3CLI().print_unimplemented],
        'mostCancelled': ['Shows all days on which most tasks were cancelled',
                          Things3CLI().print_unimplemented],
        'mostTrashed': ['Shows all days on which most tasks were trashed',
                        Things3CLI().print_unimplemented],
        'mostCreated': ['Shows all days on which most tasks were created',
                        Things3CLI().print_unimplemented],
        'mostTasks': ['Shows all projects that have most tasks',
                      Things3CLI().print_unimplemented],
        'mostCharacters': ['Shows all tasks that have most characters',
                           Things3CLI().print_unimplemented],
        'nextish': ['Shows all nextish tasks',
                    Things3CLI().print_unimplemented],
        'old': ['Shows all old tasks',
                Things3CLI().print_unimplemented],
        'projects': ['Shows all projects',
                     Things3CLI().print_unimplemented],
        'repeating': ['Shows all repeating tasks',
                      Things3CLI().print_unimplemented],
        'schedule': ['Schedule an event by creating a number of related tasks',
                     Things3CLI().print_unimplemented],
        'search': ['Searches for a specific task',
                   Things3CLI().print_unimplemented],
        'stat': ['Provides a number of statistics about all tasks',
                 Things3CLI().print_unimplemented],
        'statcsv': ['Exports some statistics as semicolon separated values',
                    Things3CLI().print_unimplemented],
        'subtasks': ['Shows all subtasks',
                     Things3CLI().print_unimplemented],
        'tag': ['Shows all tasks with the waiting for tag',
                Things3CLI().print_unimplemented],
        'tags': ['Shows all tags ordered by their usage',
                 Things3CLI().print_unimplemented],
        'waiting': ['Shows all tasks with the waiting for tag',
                    Things3CLI().print_unimplemented],
    }
    CHOICES = []
    DOCU = ""
    for command in COMMANDS:
        CHOICES.append(command)
        DOCU = DOCU + command + "\t\t" + (COMMANDS[command][0]) + "\n"

    # Required positional argument
    PARSER.add_argument('command', choices=CHOICES,
                        metavar='command', help=DOCU)

    # Optional argument which requires a parameter (eg. -d test)
    PARSER.add_argument("-l", action="store", dest="limit_by",
                        help="Limit output by <number> of results")
    PARSER.add_argument("-w", action="store", dest="waiting_tag",
                        help="Set waiting/filter tag to <tag>")
    PARSER.add_argument("-o", action="store", dest="order_by",
                        help="Sort output by <column> (e.g. 'creationDate')")
    PARSER.add_argument("-s", action="store", dest="search",
                        help="String <string> to search for")
    PARSER.add_argument("-r", action="store", dest="range",
                        help="Limit CSV statistic export by <string>")
    PARSER.add_argument("-e", action="store", dest="eventfile",
                        help="Event: <filename> that contains a list of tasks")
    PARSER.add_argument("-t", action="store", dest="start",
                        help="Event: starts at <date>")
    PARSER.add_argument("-d", action="store", dest="duration",
                        help="Event: ends after <days>")

    # Specify output of "--version"
    PARSER.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    MYARGS = PARSER.parse_args()
    main(MYARGS)
