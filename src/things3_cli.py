#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simple read-only Thing 3 CLI."""

from __future__ import print_function

__author__ = "Alexander Willner"
__copyright__ = "2020 Alexander Willner"
__credits__ = ["Alexander Willner"]
__license__ = "Apache"
__version__ = "2.0.0"
__maintainer__ = "Alexander Willner"
__email__ = "alex@willner.ws"
__status__ = "Development"

import argparse
import json
from things3 import Things3


class Things3CLI():
    """Simple read-only Thing 3 CLI."""

    print_json = False
    things3 = None

    def __init__(self, print_json, things):
        self.print_json = print_json
        self.things3 = things

    def print_tasks(self, tasks):
        """Print a task."""
        if self.print_json:
            print(json.dumps(self.things3.convert_tasks_to_model(tasks)))
        else:
            for task in tasks:
                title = task[self.things3.I_TITLE]
                context = task[self.things3.I_CONTEXT]
                print(' - ', title, ' (', context, ')')

    @classmethod
    def print_unimplemented(cls):
        """Show warning that method is not yet implemented."""
        print("not implemented yet (see things.sh for a more complete CLI)")


def main(args):
    """ Main entry point of the app """
    things3 = Things3()
    things_cli = Things3CLI(args.json, things3)
    command = args.command

    if command == "inbox":
        things_cli.print_tasks(things3.get_inbox())
    elif command == "today":
        things_cli.print_tasks(things3.get_today())
    elif command == "next":
        things_cli.print_tasks(things3.get_anytime())
    elif command == "backlog":
        things_cli.print_tasks(things3.get_someday())
    elif command == "upcoming":
        things_cli.print_tasks(things3.get_upcoming())
    elif command == "waiting":
        things_cli.print_tasks(things3.get_waiting())
    elif command == "mit":
        things_cli.print_tasks(things3.get_mit())
    elif command == "completed":
        things_cli.print_tasks(things3.get_completed())
    elif command == "cancelled":
        things_cli.print_tasks(things3.get_cancelled())
    elif command == "trashed":
        things_cli.print_tasks(things3.get_trashed())
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
