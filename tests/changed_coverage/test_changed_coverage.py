"""Tests for plugins/forge/skills/forge/scripts/changed_coverage.py.

Run: python3 -m unittest discover tests/changed_coverage -v
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SCRIPT = os.path.join(ROOT, "plugins", "forge", "skills", "forge", "scripts", "changed_coverage.py")


def git(repo, *args):
    subprocess.run(["git", "-C", repo, "-c", "user.name=t", "-c", "user.email=t@example.com"] + list(args),
                   check=True, capture_output=True)


class ChangedCoverageTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = os.path.join(self.tmp.name, "repo")
        os.makedirs(os.path.join(self.repo, "src"))
        git(self.repo, "init", "-q")
        self.write("src/a.py", "def f(x):\n    return x\n")
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-qm", "base")
        # change: lines 3-5 added to a.py; new untracked file b.py (2 lines)
        self.write("src/a.py", "def f(x):\n    return x\ndef g(x):\n    if x:\n        return 1\n")
        self.write("src/b.py", "def h():\n    return 2\n")

    def write(self, rel, text):
        p = os.path.join(self.repo, rel)
        with open(p, "w") as fh:
            fh.write(text)
        return p

    def run_cc(self, report, *args):
        r = subprocess.run([sys.executable, SCRIPT, "--report", report, "--repo", self.repo, "--base", "HEAD", "--json"]
                           + list(args), capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return json.loads(r.stdout)

    def test_lcov(self):
        rep = self.write("lcov.info", "\n".join([
            "SF:%s" % os.path.join(self.repo, "src/a.py"), "DA:1,1", "DA:2,1", "DA:3,1", "DA:4,1", "DA:5,0", "end_of_record",
            "SF:src/b.py", "DA:1,1", "DA:2,1", "end_of_record", ""]))
        d = self.run_cc(rep)
        self.assertEqual(d["changed_executable"], 5)    # a.py 3,4,5 + b.py 1,2
        self.assertEqual(d["covered"], 4)
        self.assertEqual(d["percent"], 80.0)
        self.assertEqual(d["files"]["src/a.py"]["uncovered"], [5])

    def test_cobertura(self):
        rep = self.write("coverage.xml", """<?xml version="1.0" ?>
<coverage><sources><source>%s</source></sources><packages><package><classes>
<class filename="src/a.py"><lines><line number="1" hits="1"/><line number="3" hits="0"/><line number="4" hits="0"/><line number="5" hits="0"/></lines></class>
<class filename="src/b.py"><lines><line number="1" hits="1"/><line number="2" hits="1"/></lines></class>
</classes></package></packages></coverage>""" % self.repo)
        d = self.run_cc(rep)
        self.assertEqual(d["changed_executable"], 5)
        self.assertEqual(d["covered"], 2)
        self.assertEqual(sorted(d["files"]["src/a.py"]["uncovered"]), [3, 4, 5])

    def test_changed_file_missing_from_report_counts_as_uncovered(self):
        rep = self.write("lcov.info", "SF:src/a.py\nDA:3,1\nDA:4,1\nDA:5,1\nend_of_record\n")
        d = self.run_cc(rep)
        self.assertEqual(d["files"]["src/b.py"]["uncovered"], [1, 2])
        self.assertTrue(d["files"]["src/b.py"]["not_in_report"])
        self.assertEqual(d["covered"], 3)
        self.assertEqual(d["changed_executable"], 5)

    def test_no_changes(self):
        git(self.repo, "add", "-A")
        git(self.repo, "commit", "-qm", "all")
        rep = self.write("lcov.info", "SF:src/a.py\nDA:1,1\nend_of_record\n")
        d = self.run_cc(rep)
        self.assertEqual(d["changed_executable"], 0)
        self.assertIsNone(d["percent"])

    def test_target_flag_in_text_output(self):
        rep = self.write("lcov.info", "SF:src/a.py\nDA:3,0\nDA:4,0\nDA:5,0\nend_of_record\nSF:src/b.py\nDA:1,0\nDA:2,0\nend_of_record\n")
        r = subprocess.run([sys.executable, SCRIPT, "--report", rep, "--repo", self.repo, "--base", "HEAD", "--target", "80"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("below target 80", r.stdout)


if __name__ == "__main__":
    unittest.main()
