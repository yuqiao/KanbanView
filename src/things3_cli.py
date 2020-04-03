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
import json
import things3


class Things3CLI():
    """Simple read-only Thing 3 CLI."""

    I_UUID = 0
    I_TITLE = 1
    I_CONTEXT = 2
    I_CONTEXT_UUID = 3
    print_json = False

    def __init__(self, print_json):
        self.print_json = print_json

    def print_tasks(self, tasks):
        """Print a task."""
        for task in tasks:
            title = task[self.I_TITLE]
            context = str(task[self.I_CONTEXT])
            if self.print_json:
                print(json.dumps([{
                    'title': title,
                    'context': context
                    }]))
            else:
                print(' - ' + title + ' (' + context + ')')

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
    things = Things3CLI(args.json)
    if args.command == "inbox":
        things.print_inbox()
    elif args.command == "today":
        things.print_today()
    else:
        Things3CLI.print_unimplemented()


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(
        description='Simple read-only Thing 3 CLI.')

    SUBPARSERS = PARSER.add_subparsers(help='One of the following commands:',
                                       metavar="command",
                                       required=True,
                                       dest="command")
    SUBPARSERS.add_parser('inbox',
                          help='Shows all inbox tasks')
    SUBPARSERS.add_parser('today',
                          help='Shows all todays tasks')
    SUBPARSERS.add_parser('upcoming',
                          help='Shows all upcoming tasks')
    SUBPARSERS.add_parser('next',
                          help='Shows all next tasks')
    SUBPARSERS.add_parser('someday',
                          help='Shows all someday tasks')
    SUBPARSERS.add_parser('completed',
                          help='Shows all completed tasks')
    SUBPARSERS.add_parser('cancelled',
                          help='Shows all cancelled tasks')
    SUBPARSERS.add_parser('trashed',
                          help='Shows all trashed tasks')
    SUBPARSERS.add_parser('feedback',
                          help='Give feedback')
    SUBPARSERS.add_parser('all',
                          help='Shows all tasks')
    SUBPARSERS.add_parser('csv',
                          help='Exports all tasks as CSV')
    SUBPARSERS.add_parser('due',
                          help='Shows all tasks with due dates')
    SUBPARSERS.add_parser('headings',
                          help='Shows all headings')
    SUBPARSERS.add_parser('hours',
                          help='Shows how many hours have been planned today')
    SUBPARSERS.add_parser('ical',
                          help='Shows all tasks ordered by due date as iCal')
    SUBPARSERS.add_parser('logbook',
                          help='Shows all tasks completed today')
    SUBPARSERS.add_parser('mostClosed',
                          help='Shows days on which most tasks were closed')
    SUBPARSERS.add_parser('mostCancelled',
                          help='Shows days on which most tasks were cancelled')
    SUBPARSERS.add_parser('mostTrashed',
                          help='Shows days on which most tasks were trashed')
    SUBPARSERS.add_parser('mostCreated',
                          help='Shows days on which most tasks were created')
    SUBPARSERS.add_parser('mostTasks',
                          help='Shows projects that have most tasks')
    SUBPARSERS.add_parser('mostCharacters',
                          help='Shows tasks that have most characters')
    SUBPARSERS.add_parser('nextish',
                          help='Shows all nextish tasks')
    SUBPARSERS.add_parser('old',
                          help='Shows all old tasks')
    SUBPARSERS.add_parser('projects',
                          help='Shows all projects')
    SUBPARSERS.add_parser('repeating',
                          help='Shows all repeating tasks')
    SUBPARSERS.add_parser('schedule',
                          help='Schedules an event using a template')
    SUBPARSERS.add_parser('search',
                          help='Searches for a specific task')
    SUBPARSERS.add_parser('stat',
                          help='Provides a number of statistics')
    SUBPARSERS.add_parser('statcsv',
                          help='Exports some statistics as CSV')
    SUBPARSERS.add_parser('subtasks',
                          help='Shows all subtasks')
    SUBPARSERS.add_parser('tag',
                          help='Shows all tasks with the waiting for tag')
    SUBPARSERS.add_parser('tags',
                          help='Shows all tags ordered by their usage')
    SUBPARSERS.add_parser('waiting',
                          help='Shows all tasks with the waiting for tag')

    PARSER.add_argument("-j", "--json",
                        action="store_true", default=False,
                        help="output as JSON", dest="json")
    PARSER.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    ARGUMENTS = PARSER.parse_args()
    main(ARGUMENTS)
