"""Tests for plugins/forge/skills/forge/scripts/tracker_sync.py (pure planner + ledger writer).

Run: python3 -m unittest discover tests/tracker_sync -v
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SCRIPT = os.path.join(ROOT, "plugins", "forge", "skills", "forge", "scripts", "tracker_sync.py")


def manifest(rev=3, items=None):
    items = items or [
        {"id": "SPEC-7.TASK1", "type": "enabler", "layer": "db", "refs": ["R1", "AC1"], "depends_on": [],
         "title": "lesson table", "outcome": "lessons persist", "file": "impl-tasks/01_lesson-table.md"},
        {"id": "SPEC-7.TASK2", "type": "story", "layer": "backend", "refs": ["R2", "AC2"],
         "depends_on": ["SPEC-7.TASK1"], "title": "reminder job", "outcome": "reminder sent 24h before",
         "file": "impl-tasks/02_reminder-job.md"},
    ]
    return {"spec": "SPEC-7", "revision": rev, "design_pinned_rev": rev, "task_dir": "docs/forge/tasks/07_lesson-reminders",
            "spec_file": "2026-11-18_lesson-reminders_spec.md", "items": items,
            "batches": [[i["id"]] for i in items], "critical_path": [i["id"] for i in items]}


def issue(ref, marker, state="opened"):
    return {"ref": ref, "url": "https://example.com/issues/%s" % ref.strip("#"), "state": state,
            "body": "<!-- forge:%s -->\nbody" % marker}


class PlannerTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def plan(self, man, existing, *args):
        mp = os.path.join(self.tmp.name, "m.json")
        ep = os.path.join(self.tmp.name, "e.json")
        with open(mp, "w") as fh:
            json.dump(man, fh)
        with open(ep, "w") as fh:
            json.dump(existing, fh)
        r = subprocess.run([sys.executable, SCRIPT, "plan", "--manifest", mp, "--existing", ep] + list(args),
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return json.loads(r.stdout)

    def by_id(self, result):
        return {a["id"]: a for a in result["actions"]}

    def test_first_publish_creates_items_then_parent_in_dependency_order(self):
        res = self.plan(manifest(), [])
        ids = [a["id"] for a in res["actions"]]
        self.assertEqual(ids, ["SPEC-7.TASK1", "SPEC-7.TASK2", "SPEC-7"])
        self.assertTrue(all(a["action"] == "create" for a in res["actions"]))
        t2 = self.by_id(res)["SPEC-7.TASK2"]
        self.assertIn("<!-- forge:SPEC-7.TASK2 rev=3 -->", t2["body"])
        self.assertIn("{{SPEC-7.TASK1}}", t2["body"])            # dep placeholder, filled at apply time
        self.assertIn("docs/forge/tasks/07_lesson-reminders/impl-tasks/02_reminder-job.md", t2["body"])
        self.assertEqual(t2["title"], "[SPEC-7.TASK2] reminder job")
        self.assertIn("forge", t2["labels"])
        self.assertIn("story", t2["labels"])
        self.assertIn("SPEC-7", t2["labels"])
        parent = self.by_id(res)["SPEC-7"]
        self.assertIn("{{SPEC-7.TASK1}}", parent["body"])
        self.assertEqual(res["summary"], {"create": 3, "skip": 0, "update": 0, "conflict": 0, "orphan": 0})

    def test_partial_publication_resumes(self):
        existing = [issue("#11", "SPEC-7.TASK1 rev=3")]
        res = self.plan(manifest(), existing)
        a = self.by_id(res)
        self.assertEqual(a["SPEC-7.TASK1"]["action"], "skip")
        self.assertEqual(a["SPEC-7.TASK1"]["existing"], "#11")
        self.assertEqual(a["SPEC-7.TASK2"]["action"], "create")
        self.assertIn("#11", a["SPEC-7.TASK2"]["body"])            # known dep resolved to its issue
        self.assertNotIn("{{SPEC-7.TASK1}}", a["SPEC-7.TASK2"]["body"])

    def test_rerun_after_full_publish_is_noop(self):
        existing = [issue("#11", "SPEC-7.TASK1 rev=3"), issue("#12", "SPEC-7.TASK2 rev=3"), issue("#10", "SPEC-7 rev=3")]
        res = self.plan(manifest(), existing)
        self.assertEqual(res["summary"]["skip"], 3)
        self.assertEqual(res["summary"]["create"], 0)

    def test_closed_issue_still_counts_as_existing(self):
        existing = [issue("#11", "SPEC-7.TASK1 rev=3", state="closed")]
        res = self.plan(manifest(), existing)
        self.assertEqual(self.by_id(res)["SPEC-7.TASK1"]["action"], "skip")

    def test_duplicate_marker_is_conflict_not_create(self):
        existing = [issue("#11", "SPEC-7.TASK1 rev=3"), issue("#15", "SPEC-7.TASK1 rev=3")]
        res = self.plan(manifest(), existing)
        a = self.by_id(res)["SPEC-7.TASK1"]
        self.assertEqual(a["action"], "conflict")
        self.assertEqual(sorted(a["existing"]), ["#11", "#15"])

    def test_revised_spec_updates_and_flags_orphans(self):
        items = manifest()["items"][:1]                           # TASK2 removed in rev 4
        existing = [issue("#11", "SPEC-7.TASK1 rev=3"), issue("#12", "SPEC-7.TASK2 rev=3"), issue("#10", "SPEC-7 rev=3")]
        res = self.plan(manifest(rev=4, items=items), existing)
        a = self.by_id(res)
        self.assertEqual(a["SPEC-7.TASK1"]["action"], "update")
        self.assertIn("rev=4", a["SPEC-7.TASK1"]["body"])
        self.assertEqual(a["SPEC-7.TASK2"]["action"], "orphan")    # comment proposed, never closed
        self.assertEqual(a["SPEC-7"]["action"], "update")

    def test_native_deps_capability(self):
        res = self.plan(manifest(), [issue("#11", "SPEC-7.TASK1 rev=3")], "--native-deps")
        t2 = self.by_id(res)["SPEC-7.TASK2"]
        self.assertEqual(t2["blocked_by"], ["#11"])
        self.assertNotIn("Depends on", t2["body"])

    def test_without_native_deps_body_carries_dependency(self):
        res = self.plan(manifest(), [issue("#11", "SPEC-7.TASK1 rev=3")])
        t2 = self.by_id(res)["SPEC-7.TASK2"]
        self.assertEqual(t2["blocked_by"], [])
        self.assertIn("Depends on: SPEC-7.TASK1 (#11)", t2["body"])

    def test_other_specs_markers_ignored(self):
        res = self.plan(manifest(), [issue("#30", "SPEC-8.TASK1 rev=1")])
        self.assertEqual(res["summary"]["orphan"], 0)
        self.assertEqual(res["summary"]["create"], 3)


class LedgerTest(unittest.TestCase):
    LEDGER = """# Ledger — 07 lesson-reminders

| ID | Item | Type | Depends | Status | Verified by | Issue | Updated |
|---|---|---|---|---|---|---|---|
| SPEC-7.TASK1 | lesson-table | enabler | — | ⬜ not started | — | — | — |
| SPEC-7.TASK2 | reminder-job | story | SPEC-7.TASK1 | ⬜ not started | — | https://x/2 | — |

Next: SPEC-7.TASK1
"""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = os.path.join(self.tmp.name, "ledger.md")
        with open(self.path, "w") as fh:
            fh.write(self.LEDGER)

    def run_ledger(self, *sets):
        args = []
        for s in sets:
            args += ["--set", s]
        r = subprocess.run([sys.executable, SCRIPT, "ledger", self.path] + args, capture_output=True, text=True)
        with open(self.path) as fh:
            return r.returncode, r.stdout + r.stderr, fh.read()

    def test_sets_issue_url(self):
        code, out, text = self.run_ledger("SPEC-7.TASK1=https://x/1")
        self.assertEqual(code, 0, out)
        self.assertIn("| SPEC-7.TASK1 | lesson-table | enabler | — | ⬜ not started | — | https://x/1 | — |", text)

    def test_same_url_again_is_noop(self):
        code, out, _ = self.run_ledger("SPEC-7.TASK2=https://x/2")
        self.assertEqual(code, 0, out)

    def test_refuses_to_overwrite_different_url(self):
        code, out, text = self.run_ledger("SPEC-7.TASK2=https://x/99")
        self.assertEqual(code, 1, out)
        self.assertIn("https://x/2", text)

    def test_unknown_id(self):
        code, out, _ = self.run_ledger("SPEC-7.TASK9=https://x/9")
        self.assertEqual(code, 1)
        self.assertIn("SPEC-7.TASK9", out)


if __name__ == "__main__":
    unittest.main()
