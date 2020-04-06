"""
py2app configuration file.
"""

from setuptools import setup

VERSION = "2.0.1"
APP_NAME="KanbanView"
APP = ['src/things3_app.py']
DATA_FILES = [('resources', ["resources/logo.png"]),
              ('resources', ["resources/kanban.js"]),
              ('resources', ["resources/kanban.css"]),
              ('resources', ["resources/kanban.html"]),
              ('resources', ["resources/favicon.ico"]),
              'src/things3.py',
              'src/things3_api.py',
              'src/things3_app.py',
              'src/things3_cli.py']
OPTIONS = {
        'argv_emulation': True,
        'plist': {'CFBundleName': APP_NAME,
                  'CFBundleDisplayName': APP_NAME,
                  'CFBundleGetInfoString': APP_NAME,
                  'CFBundleIdentifier': "ws.willner.kanbanview",
                  'CFBundleVersion': VERSION,
                  'CFBundleShortVersionString': VERSION,
                  'NSHumanReadableCopyright':'Copyright 2020 Alexander Willner'},
        'optimize':'2'
}

setup(
    app=APP,
    name=APP_NAME,
    version=VERSION,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    entry_points = {
        'console_scripts': [
            'things-cli = things3_cli:main',
            'things-api = things3_api:main',
            'things-kanban = things3_app:main'
            ]
    }
)
