#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""KanbanView for Things 3."""

from __future__ import print_function

__author__ = "Luc Beaulieu and Alexander Willner"
__copyright__ = "Copyright 2018 Luc Beaulieu / 2020 Alexander Willner"
__credits__ = ["Luc Beaulieu", "Alexander Willner"]
__license__ = "unknown"
__version__ = "1.1.0"
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
FILE_SQLITE = '~/Library/Containers/'\
              'com.culturedcode.ThingsMac.beta/Data/Library/'\
              'Application Support/Cultured Code/Things/Things.sqlite3'\
    if not environ.get('THINGSDB') else environ.get('THINGSDB')
ANONYMIZE = bool(environ.get('ANONYMIZE'))
TAG_WAITING = "Waiting" if not environ.get('TAG_WAITING') \
    else environ.get('TAG_WAITING')
TAG_MIT = "MIT" if not environ.get('TAG_MIT') \
    else environ.get('TAG_MIT')

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
LIST_SOMEDAY = ISOPENTASK + " AND " + ISPOSTPONED + \
    " AND TASK.startdate IS NULL AND TASK.recurrenceRule IS NULL" + \
    " ORDER BY TASK.duedate DESC, TASK.creationdate DESC"
LIST_INBOX = ISOPENTASK + " AND " + ISNOTSTARTED + \
    " ORDER BY TASK.duedate DESC , TASK.todayIndex"
LIST_ANYTIME = ISOPENTASK + " AND " + ISSTARTED + \
    " AND TASK.startdate is NULL" + \
    " AND (TASK.area NOT NULL OR TASK.project in (SELECT uuid FROM " + \
    TASKTABLE + \
    " WHERE uuid=TASK.project AND start=1" + \
    " AND trashed=0))" + \
    " ORDER BY TASK.duedate DESC , TASK.todayIndex"
LIST_TODAY = ISOPENTASK + " AND " + ISSTARTED + \
    " AND TASK.startdate is NOT NULL" + \
    " ORDER BY TASK.duedate DESC , TASK.todayIndex"
LIST_UPCOMING = ISOPENTASK + " AND " + ISPOSTPONED + \
    " AND (TASK.startDate NOT NULL OR TASK.recurrenceRule NOT NULL)" + \
    " ORDER BY TASK.startdate, TASK.todayIndex"
LIST_WAITING = ISOPENTASK + \
    " AND TAGS.tags=(SELECT uuid FROM " + TAGTABLE + \
    " WHERE title='" + TAG_WAITING + "')" + \
    " ORDER BY TASK.duedate DESC , TASK.todayIndex"
LIST_MIT = ISOPENTASK + " AND " + ISSTARTED + \
    " AND TASK.startdate is NOT NULL" + \
    " AND TAGS.tags=(SELECT uuid FROM " + TAGTABLE + \
    " WHERE title='" + TAG_MIT + "')" + \
    " ORDER BY TASK.duedate DESC , TASK.todayIndex"


def anonymize(word):
    """Scramble output for screenshots."""

    if ANONYMIZE is True:
        word = list(word)
        shuffle(word)
        word = ''.join(word)
    return word


def get_rows(sql):
    """Query Things database."""

    sql = """
        SELECT DISTINCT
            TASK.uuid,
            TASK.title,
            CASE
                WHEN AREA.title IS NOT NULL THEN AREA.title
                WHEN PROJECT.title IS NOT NULL THEN PROJECT.title
                WHEN HEADING.title IS NOT NULL THEN HEADING.title
            END,
            CASE
                WHEN AREA.uuid IS NOT NULL THEN AREA.uuid
                WHEN PROJECT.uuid IS NOT NULL THEN PROJECT.uuid
            END,
            CASE
                WHEN TASK.recurrenceRule IS NULL
                THEN date(TASK.dueDate,"unixepoch")
            ELSE NULL
            END
        FROM
            TMTask AS TASK
        LEFT JOIN
            TMTaskTag TAGS ON TAGS.tasks = TASK.uuid
        LEFT OUTER JOIN
            TMTask PROJECT ON TASK.project = PROJECT.uuid
        LEFT OUTER JOIN
            TMArea AREA ON TASK.area = AREA.uuid
        LEFT OUTER JOIN
            TMTask HEADING ON TASK.actionGroup = HEADING.uuid
        WHERE """ + sql
    CURSOR.execute(sql)
    return CURSOR.fetchall()


def write_html_column(cssclass, file, header, sql):
    """Create a column in the output."""

    rows = get_rows(sql)

    file.write("<div class='column'><div class=''>" +
               "<h2 class='" + cssclass + "'>" + header +
               "<span class='size'>" + str(len(rows)) +
               "</span></h2>")

    for row in rows:
        task_uuid = str(row[0]) if row[0] is not None else ''
        task_title = anonymize(str(row[1])) if row[1] is not None else ''
        context_title = anonymize(str(row[2])) if row[2] is not None else ''
        context_uuid = str(row[3]) if row[3] is not None else ''
        deadline = str(row[4]) if row[4] is not None else ''

        task_link = '<a href="things:///show?id=' + task_uuid + '">' + \
            task_title + '</a>' if task_uuid != '' else task_title
        context_link = '<a href="things:///show?id=' + context_uuid + '">' + \
            context_title + '</a>' if context_uuid != '' else context_title
        css_class = 'hasProject' if context_title != '' else 'hasNoProject'
        css_class = 'hasDeadline' if deadline != '' else css_class

        file.write('<div class="box">' + task_link +
                   '<div class="deadline">' + deadline + '</div>' +
                   '<div class="area ' + css_class + '">' + context_link +
                   '</div>' +
                   '</div>')
    file.write("</div></div>")


def write_html_header(file):
    """Write HTML header."""

    message = """
        <!DOCTYPE html>
        <html>
        <head>
          <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
          <link rel="stylesheet" href="../resources/style.css">
          <title>KanbanView for Things 3</title>
        </head>

        <body>
          <header>
            <a href="#" onclick="refresh();" title="click to refresh">
              <img class="logo" src="../resources/logo.png" alt="logo">
            </a>
          </header>
          <article class='some-page-wrapper'>
            <div class='row'>
        """
    file.write(message)


def write_html_footer(file):
    """Write HTML footer."""

    message = """
            </div>
          </article>
        <footer class="footer"><br />
        Copyright &copy;2018 Luc Beaulieu / 2020 Alexander Willner
        </footer></body></html>"""
    file.write(message)


def write_html_columns(file):
    """Write HTML columns."""

    write_html_column("color1", file, "Backlog", LIST_SOMEDAY)
    write_html_column("color5", file, "Upcoming", LIST_UPCOMING)
    write_html_column("color3", file, "Waiting", LIST_WAITING)
    write_html_column("color4", file, "Inbox", LIST_INBOX)
    write_html_column("color2", file, "MIT", LIST_MIT)
    write_html_column("color6", file, "Today", LIST_TODAY)
    write_html_column("color7", file, "Next", LIST_ANYTIME)


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
