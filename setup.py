"""
py2app configuration file.
"""

from setuptools import setup

APP = ['src/things3_to_kanban_server.py']
DATA_FILES = ['resources/style.css', 'resources/logo.png', 'resources/scripts.js', 'resources/kanban.html',
              'src/things3_to_kanban.py', 'src/things3.py']
OPTIONS = {
        'plist': {'CFBundleShortVersionString':'1.1.0'},
        'optimize':'2'
}

setup(
    app=APP,
    name='KanbanView',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
