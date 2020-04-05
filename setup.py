"""
py2app configuration file.
"""

from setuptools import setup

APP = ['src/things3_app.py']
DATA_FILES = ['resources/kanban.css', 'resources/logo.png', 'resources/kanban.js', 'resources/kanban.html',
              'src/things3.py', 'src/things3_api.py']
OPTIONS = {
        'plist': {'CFBundleShortVersionString':'2.0.0'},
        'optimize':'2'
}

setup(
    app=APP,
    name='KanbanView',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
