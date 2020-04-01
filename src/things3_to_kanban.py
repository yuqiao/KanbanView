#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""KanbanView for Things 3."""

from __future__ import print_function

__author__ = "Luc Beaulieu and Alexander Willner"
__copyright__ = "Copyright 2018 Luc Beaulieu / 2020 Alexander Willner"
__credits__ = ["Luc Beaulieu", "Alexander Willner"]
__license__ = "unknown"
__version__ = "1.0.0"
__maintainer__ = "Alexander Willner"
__email__ = "alex@willner.ws"
__status__ = "Development"

import sqlite3
import webbrowser
import codecs
from os.path import expanduser, dirname, realpath
from os import environ
from random import shuffle

# Basic config
FILE_SQLITE = '~/Library/Containers/com.culturedcode.ThingsMac/Data/Library/'\
              'Application Support/Cultured Code/Things/Things.sqlite3'\
    if not environ.get('THINGSDB') else environ.get('THINGSDB')
ANONYMIZE = bool(environ.get('ANONYMIZE'))
TAG_WAITING = "Waiting" if not environ.get('TAG_WAITING') \
    else environ.get('TAG_WAITING')

# Basic variables
FILE_SQLITE = expanduser(FILE_SQLITE)
FILE_HTML = dirname(realpath(__file__)) + '/kanban.html'

CURSOR = sqlite3.connect(FILE_SQLITE).cursor()

# Database layout info
TASKTABLE = "TMTask"
AREATABLE = "TMArea"
TAGTABLE = "TMTag"
TASKTAGTABLE = "TMTaskTag"
ISNOTTRASHED = "TASK.trashed = 0"
ISTRASHED = "TASK.trashed = 1"
ISOPEN = "TASK.status = 0"
ISNOTSTARTED = "TASK.start = 0"
ISCANCELLED = "TASK.status = 2"
ISCOMPLETED = "TASK.status = 3"
ISSTARTED = "TASK.start = 1"
ISPOSTPONED = "TASK.start = 2"
ISTASK = "TASK.type = 0"
ISPROJECT = "TASK.type = 1"
ISHEADING = "TASK.type = 2"
ISOPENTASK = ISTASK + " AND " + ISNOTTRASHED + " AND " + ISOPEN

# Queries
LIST_SOMEDAY = ISOPENTASK + " AND " + ISPOSTPONED
LIST_INBOX = ISOPENTASK + " AND " + ISNOTSTARTED
LIST_ANYTIME = ISOPENTASK + " AND " + ISSTARTED + \
    " AND (TASK.area NOT NULL OR TASK.project in (SELECT uuid FROM " + \
    TASKTABLE + \
    " WHERE uuid=TASK.project AND " + ISSTARTED + \
    " AND " + ISNOTTRASHED + "))"
LIST_TODAY = ISOPENTASK + " AND " + ISSTARTED + \
    " AND TASK.startdate is NOT NULL"
LIST_UPCOMING = ISOPENTASK + " AND " + ISPOSTPONED + \
    " AND (TASK.startDate NOT NULL OR TASK.recurrenceRule NOT NULL)"
LIST_WAITING = ISOPENTASK + \
    " AND TAGS.tags=(SELECT uuid FROM " + TAGTABLE + \
    " WHERE title='" + TAG_WAITING + "')"


def anonymize(word):
    """Scramble output for screenshots."""

    if ANONYMIZE is True:
        word = list(word)
        shuffle(word)
        word = ''.join(word)
    return word


def write_html_column(uid, file, title, sql):
    """Create a column in the output."""

    sql = """
        SELECT
            TASK.uuid, TASK.title, PROJECT.title,
            PROJECT.uuid, TASK.dueDate
        FROM
            TMTask AS TASK
        LEFT JOIN
            TMTaskTag TAGS ON TAGS.tasks = TASK.uuid
        LEFT OUTER JOIN
            TMTask PROJECT ON TASK.project = PROJECT.uuid
        WHERE """ + sql + """
        ORDER BY
            TASK.duedate, TASK.startdate, TASK.todayIndex"""
    CURSOR.execute(sql)
    rows = CURSOR.fetchall()

    file.write('<div id="left' + str(uid) + '"><div class="inner"><h2>' +
               title + ' <span class="size">' +
               str(len(rows)) + '</span></h2>')
    for row in rows:
        project_name = '<a href="things:///show?id=' + \
            row[3] + '">' + anonymize(str(row[2])) + \
            '</a>' if row[2] is not None else 'None'
        css_class = 'hasProject' if row[2] is not None else 'hasNoProject'
        css_class = 'hasDeadline' if row[4] is not None else css_class
        file.write('<div id="box">' +
                   '<a href="things:///show?id=' + row[0] + '">' +
                   anonymize(row[1]) + '</a> <div class="area ' +
                   css_class + '">' + project_name + '</div></div>')
    file.write("</div></div>")


def write_html_header(file):
    """Write HTML header."""

    message = """<head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
        <link rel="stylesheet" href="../resources/style.css">
        </head>

        <body>
        <img id="logo" src="../resources/logo.png" alt="logo" />
        """
    file.write(message)


def write_html_footer(file):
    """Write HTML footer."""

    message = """
        <div id="foot"><br />
        Copyright &copy;2018 Luc Beaulieu / 2020 Alexander Willner
        </div></body></html>"""
    file.write(message)


def write_html_columns(file):
    """Write HTML columns."""

    write_html_column(1, file, "Backlog", LIST_SOMEDAY)
    write_html_column(2, file, "Upcoming", LIST_UPCOMING)
    write_html_column(3, file, "Waiting", LIST_WAITING)
    write_html_column(4, file, "Inbox", LIST_INBOX)
    write_html_column(5, file, "Today", LIST_TODAY)
    write_html_column(6, file, "Next", LIST_ANYTIME)


def main():
    """Convert Things 3 database to Kanban HTML view."""

    file = codecs.open(FILE_HTML, 'w', 'utf-8')

    write_html_header(file)

    write_html_columns(file)

    write_html_footer(file)

    file.close()
    CURSOR.close()

    webbrowser.open_new_tab('file://' + FILE_HTML)


if __name__ == "__main__":
    main()
