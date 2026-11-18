"""Tests for `spec_check.py plan` and `spec_check.py gaps` (contract: 1).

Run: python3 -m unittest discover tests/spec_check -v
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SKILL = os.path.join(ROOT, "plugins", "forge", "skills", "forge")
SCRIPT = os.path.join(SKILL, "scripts", "spec_check.py")

SPEC = """---
contract: 1
id: SPEC-7
revision: 3
status: approved
path: fast
source_rev: 9447a7f
---

# Lesson reminders

## Objective
Cut no-shows. Success: rate measured 4 weeks. Failure: < 80% lessons logged.

## Scope
- reminders

## Non-goals
- payments

## Requirements
| ID | Requirement |
|---|---|
| R1 | Store lessons |
| R2 | Send reminder 24h before |

## Acceptance criteria
| ID | Criterion | Verifies |
|---|---|---|
| AC1 | Lesson row persists with tutor id | R1 |
| AC2 | Reminder sent 24h +/- 5 min before | R2 |

## Approvals
- 2026-11-18 Owner rev 3
"""


def item(n, type_="task", refs="[R1, AC1]", deps="[]", layer="backend", files=("src/a.ts",), title=None):
    title = title or "item %d" % n
    return "\n".join([
        "---",
        "id: SPEC-7.TASK%d" % n,
        "type: %s" % type_,
        "refs: %s" % refs,
        "depends_on: %s" % deps,
        "layer: %s" % layer,
        "---",
        "",
        "# %02d %s" % (n, title),
        "",
        "## Outcome",
        "x",
        "",
        "## Files",
    ] + ["- Modify: `%s`" % f for f in files] + ["", "## Verify", "```bash", "npm test", "```", ""])


class PlanTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.task = os.path.join(self.tmp.name, "tasks", "07_lesson-reminders")
        os.makedirs(os.path.join(self.task, "impl-tasks"))
        with open(os.path.join(self.task, "2026-11-18_lesson-reminders_spec.md"), "w") as fh:
            fh.write(SPEC)

    def add(self, n, slug="step", **kw):
        p = os.path.join(self.task, "impl-tasks", "%02d_%s.md" % (n, slug))
        with open(p, "w") as fh:
            fh.write(item(n, **kw))

    def run_plan(self, *args):
        r = subprocess.run([sys.executable, SCRIPT, "plan", self.task] + list(args),
                           capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def assertPlanOk(self, *args):
        code, out = self.run_plan(*args)
        self.assertEqual(code, 0, out)
        return out

    def assertPlanError(self, needle):
        code, out = self.run_plan()
        self.assertEqual(code, 1, out)
        self.assertIn(needle, out)
        return out

    def diamond(self):
        self.add(1, type_="enabler", refs="[R1, AC1]", layer="db", files=("db/001.sql",))
        self.add(2, type_="story", refs="[R2, AC2]", deps="[SPEC-7.TASK1]", files=("src/api.ts",))
        self.add(3, type_="task", refs='[R2, "design §Telemetry"]', deps="[SPEC-7.TASK1]", layer="telemetry", files=("src/events.ts",))
        self.add(4, type_="story", refs="[R2]", deps="[SPEC-7.TASK2, SPEC-7.TASK3]", layer="frontend", files=("web/page.tsx",))

    def test_fast_single_item(self):
        self.add(1, refs="[R1, R2, AC1, AC2]", layer="mixed")
        out = self.assertPlanOk()
        self.assertIn("batch 1: SPEC-7.TASK1", out)

    def test_diamond_batches_and_critical_path(self):
        self.diamond()
        out = self.assertPlanOk()
        self.assertIn("batch 1: SPEC-7.TASK1", out)
        self.assertIn("batch 2: SPEC-7.TASK2, SPEC-7.TASK3", out)
        self.assertIn("batch 3: SPEC-7.TASK4", out)
        self.assertIn("critical path: SPEC-7.TASK1 → SPEC-7.TASK2 → SPEC-7.TASK4", out)

    def test_json_manifest(self):
        self.diamond()
        data = json.loads(self.assertPlanOk("--json"))
        self.assertEqual(data["spec"], "SPEC-7")
        self.assertEqual(data["revision"], 3)
        self.assertEqual(len(data["items"]), 4)
        self.assertEqual(data["batches"], [["SPEC-7.TASK1"], ["SPEC-7.TASK2", "SPEC-7.TASK3"], ["SPEC-7.TASK4"]])
        self.assertEqual(data["critical_path"], ["SPEC-7.TASK1", "SPEC-7.TASK2", "SPEC-7.TASK4"])
        first = data["items"][0]
        for key in ("id", "type", "layer", "refs", "depends_on", "title", "file", "outcome"):
            self.assertIn(key, first)
        for key in ("task_dir", "spec_file", "design_pinned_rev"):
            self.assertIn(key, data)
        for key in ():
            self.assertIn(key, first)

    def test_uncovered_ac(self):
        self.add(1, refs="[R1, R2, AC1]")
        self.assertPlanError("AC2")

    def test_unknown_dep(self):
        self.add(1, refs="[R1, R2, AC1, AC2]", deps="[SPEC-7.TASK9]")
        self.assertPlanError("SPEC-7.TASK9")

    def test_cycle(self):
        self.add(1, refs="[R1, AC1]", deps="[SPEC-7.TASK2]")
        self.add(2, refs="[R2, AC2]", deps="[SPEC-7.TASK1]", files=("src/b.ts",))
        self.assertPlanError("cycle")

    def test_duplicate_items(self):
        self.add(1, refs="[R1, R2, AC1, AC2]")
        self.add(2, refs="[R1, R2, AC1, AC2]")
        self.assertPlanError("duplicate")

    def test_id_must_match_file_number(self):
        p = os.path.join(self.task, "impl-tasks", "01_step.md")
        with open(p, "w") as fh:
            fh.write(item(2, refs="[R1, R2, AC1, AC2]"))
        self.assertPlanError("01_step.md")

    def test_bad_type_and_layer(self):
        self.add(1, refs="[R1, R2, AC1, AC2]", type_="epic", layer="cloud")
        out = self.assertPlanError("type")
        self.assertIn("layer", out)

    def test_ref_to_unknown_requirement(self):
        self.add(1, refs="[R1, R2, AC1, AC2, R9]")
        self.assertPlanError("R9")

    def test_no_items(self):
        self.assertPlanError("no work items")


class GapsTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def gaps(self, text, *args):
        p = os.path.join(self.tmp.name, "prd.md")
        with open(p, "w") as fh:
            fh.write(text)
        r = subprocess.run([sys.executable, SCRIPT, "gaps", p] + list(args), capture_output=True, text=True)
        with open(p) as fh:
            self.assertEqual(fh.read(), text, "gaps must not modify the file")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r.stdout

    def test_external_doc_without_front_matter(self):
        out = self.gaps("# Checkout v2\n\n## Overview\nMake checkout better.\n\n## Requirements\n- R1 Checkout must be fast\n- R2 Support saved cards\n")
        self.assertIn("Acceptance criteria", out)
        self.assertIn("Non-goals", out)
        self.assertIn("R1", out)          # vague wording
        self.assertIn("fast", out)
        self.assertIn("R2", out)          # no AC

    def test_missing_success_failure(self):
        out = self.gaps("## Objective\nGrow sales.\n")
        self.assertIn("success", out.lower())

    def test_clean_doc_reports_no_gaps(self):
        out = self.gaps(SPEC.replace("path: fast", "path: fast"), "--path", "fast")
        self.assertIn("0 gaps", out)

    def test_number_makes_vague_word_ok(self):
        out = self.gaps("## Requirements\n- R1 Page loads fast: p95 < 800 ms\n\n## Acceptance criteria\n- AC1 (R1) p95 < 800 ms\n", "--path", "fast")
        self.assertNotIn("vague", out)


if __name__ == "__main__":
    unittest.main()


class CompatibilityTest(unittest.TestCase):
    """Product (spec template, prompt 01) → engineering (impl-task template, prompt 02) → tracker planner."""

    def test_templates_round_trip(self):
        import re
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        task = os.path.join(tmp.name, "tasks", "07_lesson-reminders")
        os.makedirs(os.path.join(task, "impl-tasks"))
        with open(os.path.join(SKILL, "templates", "spec.md")) as fh:
            spec = fh.read()
        spec = (spec.replace("SPEC-<n>", "SPEC-7").replace("<fast|standard|deep>", "standard")
                    .replace("<git short sha>", "9447a7f").replace("status: proposed", "status: approved"))
        spec = re.sub(r"<!-- (fast\+|standard\+|deep|value|event).*?-->", "filled", spec)
        spec = spec.replace("<!-- YYYY-MM-DD <name> rev <n> -->", "- 2026-11-18 Owner rev 1")
        spec_path = os.path.join(task, "2026-11-18_lesson-reminders_spec.md")
        with open(spec_path, "w") as fh:
            fh.write(spec)
        with open(os.path.join(SKILL, "templates", "impl-task.md")) as fh:
            tpl = fh.read()
        for n, deps in ((1, "[]"), (2, "[SPEC-7.TASK1]")):
            body = (tpl.replace("SPEC-<n>.TASK<NN>", "SPEC-7.TASK%d" % n).replace("<story|enabler|spike|bug|task>", "story")
                       .replace("refs: [R<n>, AC<n>]", "refs: [R1, AC1]").replace("depends_on: []", "depends_on: %s" % deps)
                       .replace("<db|backend|frontend|integration|telemetry|test|mixed>", "backend")
                       .replace("# NN <item-name>", "# %02d part %d" % (n, n))
                       .replace("- Modify: `path/file.ext` (fn/area)", "- Modify: `src/part%d.ts`" % n))
            with open(os.path.join(task, "impl-tasks", "%02d_part-%d.md" % (n, n)), "w") as fh:
                fh.write(body)
        r = subprocess.run([sys.executable, SCRIPT, "check", spec_path, "--require-approved", "--rev", "1"],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout)
        r = subprocess.run([sys.executable, SCRIPT, "plan", task, "--json"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout)
        man_path = os.path.join(tmp.name, "plan.json")
        with open(man_path, "w") as fh:
            fh.write(r.stdout)
        ex_path = os.path.join(tmp.name, "issues.json")
        with open(ex_path, "w") as fh:
            fh.write("[]")
        sync = os.path.join(SKILL, "scripts", "tracker_sync.py")
        r = subprocess.run([sys.executable, sync, "plan", "--manifest", man_path, "--existing", ex_path],
                           capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertEqual(json.loads(r.stdout)["summary"]["create"], 3)
