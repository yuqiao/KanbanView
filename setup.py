"""
py2app configuration file.
"""

from setuptools import setup

APP = ['src/things3_app.py']
DATA_FILES = ['resources',
              'src/things3.py', 'src/things3_api.py']
OPTIONS = {
        'argv_emulation': True,
        'plist': {'CFBundleName': "KanbanView",
                  'CFBundleDisplayName': "KanbanView",
                  'CFBundleGetInfoString': "KanbanView",
                  'CFBundleIdentifier': "ws.willner.kanbanview",
                  'CFBundleVersion': "2.0.0",
                  'CFBundleShortVersionString': "2.0.0",
                  'NSHumanReadableCopyright':'Copyright 2020 Alexander Willner'},
        'optimize':'2'
}

setup(
    app=APP,
    name='KanbanView',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
