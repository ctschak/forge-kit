import os
import sys
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from projapp.db import connect  # noqa: E402
from projapp.projects import create_project, list_projects  # noqa: E402


class ProjectsTest(unittest.TestCase):
    def setUp(self):
        self.conn = connect()

    def test_create_and_list_scoped_by_org(self):
        create_project(self.conn, 1, "a")
        create_project(self.conn, 2, "b")
        self.assertEqual([p["name"] for p in list_projects(self.conn, 1, page=0)], ["a"])

    def test_name_required(self):
        with self.assertRaises(ValueError):
            create_project(self.conn, 1, "  ")
