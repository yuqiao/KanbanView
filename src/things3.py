#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Simple read-only API for Things 3."""

from __future__ import print_function

__author__ = "Alexander Willner"
__copyright__ = "2020 Alexander Willner"
__credits__ = ["Alexander Willner"]
__license__ = "Apache"
__version__ = "0.0.1"
__maintainer__ = "Alexander Willner"
__email__ = "alex@willner.ws"
__status__ = "Development"

import sqlite3
from os.path import expanduser
from os import environ

# Basic config
FILE_SQLITE = '~/Library/Containers/'\
              'com.culturedcode.ThingsMac.beta/Data/Library/'\
              'Application Support/Cultured Code/Things/Things.sqlite3'\
    if not environ.get('THINGSDB') else environ.get('THINGSDB')
TAG_WAITING = "Waiting" if not environ.get('TAG_WAITING') \
    else environ.get('TAG_WAITING')
TAG_MIT = "MIT" if not environ.get('TAG_MIT') \
    else environ.get('TAG_MIT')

# Basic variables
FILE_SQLITE = expanduser(FILE_SQLITE)
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

# Query Index
I_UUID = 0
I_TITLE = 1
I_CONTEXT = 2
I_CONTEXT_UUID = 3
I_DUE = 4

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
LIST_MIT = ISOPENTASK + " AND " + ISSTARTED + " AND PROJECT.status = 0 " \
    " AND TAGS.tags=(SELECT uuid FROM " + TAGTABLE + \
    " WHERE title='" + TAG_MIT + "')" + \
    " ORDER BY TASK.duedate DESC , TASK.todayIndex"


def get_inbox():
    """Get all tasks from the inbox."""
    return get_rows(LIST_INBOX)


def get_today():
    """Get all tasks from the today list."""
    return get_rows(LIST_TODAY)


def get_not_implemented():
    """Not implemented warning."""
    return [["0", "not implemented", "no context", "0", "0"]]


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


def convert_task_to_model(task):
    """Convert task to model."""
    model = {'uuid': task[I_UUID],
             'title': task[I_TITLE],
             'context': task[I_CONTEXT],
             'context_uuid': task[I_CONTEXT_UUID],
             'due': task[I_DUE],
             }
    return model


def convert_tasks_to_model(tasks):
    """Convert tasks to model."""
    model = []
    for task in tasks:
        model.append(convert_task_to_model(task))
    return model
