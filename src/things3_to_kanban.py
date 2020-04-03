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

import webbrowser
import codecs
from os.path import dirname, realpath
from os import environ
from random import shuffle
import things3

# Basic config
ANONYMIZE = bool(environ.get('ANONYMIZE'))

# Basic variables
FILE_HTML = dirname(realpath(__file__)) + '/kanban.html'


def anonymize(word):
    """Scramble output for screenshots."""

    if ANONYMIZE is True:
        word = list(word)
        shuffle(word)
        word = ''.join(word)
    return word


def write_html_column(cssclass, file, header, sql):
    """Create a column in the output."""

    rows = things3.get_rows(sql)

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

    write_html_column("color1", file, "Backlog", things3.LIST_SOMEDAY)
    write_html_column("color5", file, "Upcoming", things3.LIST_UPCOMING)
    write_html_column("color3", file, "Waiting", things3.LIST_WAITING)
    write_html_column("color4", file, "Inbox", things3.LIST_INBOX)
    write_html_column("color2", file, "MIT", things3.LIST_MIT)
    write_html_column("color6", file, "Today", things3.LIST_TODAY)
    write_html_column("color7", file, "Next", things3.LIST_ANYTIME)


def main():
    """Convert Things 3 database to Kanban HTML view."""

    with codecs.open(FILE_HTML, 'w', 'utf-8') as file:
        write_html_header(file)
        write_html_columns(file)
        write_html_footer(file)

    webbrowser.open_new_tab('file://' + FILE_HTML)


if __name__ == "__main__":
    main()
