#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

import unittest
import io
import src.things3_kanban
from src.things3 import Things3


class Things3KanbanCase(unittest.TestCase):
    """Class documentation goes here."""

    things3 = Things3(database='tests/Things.sqlite3')

    class CustomStringIO(io.StringIO):
        def close(self):
            True

    def test_today(self):
        """Test Today."""
        output = self.CustomStringIO()
        src.things3_kanban.THINGS3 = self.things3
        src.things3_kanban.main(output)
        self.assertIn("Today Todo", output.getvalue())

if __name__ == '__main__':
    unittest.main()
