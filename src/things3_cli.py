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
    PARSER = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    COMMANDS={
        'inbox':'Shows all inbox tasks ordered by creationDate',
        'today':'Shows all todays tasks ordered by index',
        'upcoming':'Shows all upcoming tasks ordered by date',
        'next':'Shows all next tasks ordered by creationDate',
        'someday':'Shows all someday tasks ordered by creationDate',
        'completed':'Shows all completed tasks ordered by creationDate',
        'cancelled':'Shows all cancelled tasks ordered by cancel date',
        'trashed':'Shows all trashed tasks ordered by creationDate',
        'feedback':'Opens the feedback web page to request and propose changes',
        'all':'Shows all tasks ordered by creationDate',
        'csv':'Exports all tasks as semicolon seperated values incl. notes and Excel friendly',
        'due':'Shows all tasks ordered by due date',
        'headings':'Shows all headings ordered by creationDate',
        'hours':'Shows how many hours of work have been planned for today',
        'ical':'Shows all tasks ordered by due date as iCal',
        'logbook':'Shows all tasks completed today ordered by creationDate',
        'mostClosed':'Shows all days on which most tasks were closed',
        'mostCancelled':'Shows all days on which most tasks were cancelled',
        'mostTrashed':'Shows all days on which most tasks were trashed',
        'mostCreated':'Shows all days on which most tasks were created',
        'mostTasks':'Shows all projects that have most tasks',
        'mostCharacters':'Shows all tasks that have most characters',
        'nextish':'Shows all nextish tasks ordered by creationDate',
        'old':'Shows all old tasks ordered by creationDate',
        'projects':'Shows all projects ordered by creationDate',
        'repeating':'Shows all repeating tasks ordered by creationDate',
        'schedule':'Schedule an event by creating a number of related tasks',
        'search':'Searches for a specific task',
        'stat':'Provides a number of statistics about all tasks',
        'statcsv':'Exports some statistics as semicolon separated values for -1 year',
        'subtasks':'Shows all subtasks ordered by creationDate',
        'tag':'Shows all tasks with the tag "Waiting for" ordered by "creationDate"',
        'tags':'Shows all tags ordered by their usage',
        'waiting':'Shows all tasks with the tag "Waiting for" ordered by "creationDate"',
    }
    choices=[]
    help=""
    for command in COMMANDS:
        choices.append(command)
        help = help + command + "\t\t" + (COMMANDS[command]) + "\n"

    # Required positional argument
    PARSER.add_argument('command', choices=choices, metavar='command', help=help)
  
    # Optional argument which requires a parameter (eg. -d test)
    PARSER.add_argument("-l", action="store", dest="limit_by", help="Limit output by <number> of results")
    PARSER.add_argument("-w", action="store", dest="waiting_tag", help="Set waiting/filter tag to <tag>")
    PARSER.add_argument("-o", action="store", dest="order_by", help="Sort output by <column> (e.g. 'userModificationDate' or 'creationDate')")
    PARSER.add_argument("-s", action="store", dest="search", help="String <string> to search for")
    PARSER.add_argument("-r", action="store", dest="range", help="Limit CSV statistic export by <string>")
    PARSER.add_argument("-e", action="store", dest="eventfile", help="Event: <filename> that contains a list of tasks")
    PARSER.add_argument("-t", action="store", dest="start", help="Event: starts at <date>")
    PARSER.add_argument("-d", action="store", dest="duration", help="Event: ends after <days>")

    # Specify output of "--version"
    PARSER.add_argument(
        "--version",
        action="version",
        version="%(prog)s (version {version})".format(version=__version__))

    MYARGS = PARSER.parse_args()
    main(MYARGS)
