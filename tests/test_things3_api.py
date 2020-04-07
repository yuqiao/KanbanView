#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

import unittest
from dataclasses import dataclass
from things3.things3_api import ThingsAPI, ThingsGUI
from things3.things3 import Things3


class Things3APICase(unittest.TestCase):
    """Class documentation goes here."""

    things_api = ThingsAPI()
    things_gui = ThingsGUI()
    things_api.things3 = Things3(database='tests/Things.sqlite3')
    @dataclass
    class Resp:
        """Store httpd responses."""
        media: str
        status: str
        data: bytes

    def test_today(self):
        """Test Today."""

        resp = self.Resp("", "", None)
        self.things_api.on_get(None, resp, "today")
        self.assertEqual(1, len(resp.media))

    def test_get_file(self):
        """Test get file."""

        resp = self.Resp("", "", None)
        self.things_gui.on_get(None, resp, "/kanban.html")
        self.assertIn("footer", resp.data.decode())


if __name__ == '__main__':
    unittest.main()
