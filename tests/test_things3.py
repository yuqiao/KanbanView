#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""Module documentation goes here."""

import unittest
import sys
import src.things3


class Things3Case(unittest.TestCase):
    """Class documentation goes here."""
    def test_today(self):
        """Test Today."""
        # TODO: set database to test database here
        tasks = src.things3.get_today()
        self.assertEqual(4, len(tasks))

    def test_inbox(self):
        """Test Inbox."""
        # TODO: set database to test database here
        tasks = src.things3.get_inbox()
        self.assertEqual(1, len(tasks))


if __name__ == '__main__':
    unittest.main()
