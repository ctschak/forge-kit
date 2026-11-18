"""Tests for plugins/forge/skills/forge/scripts/spec_check.py (contract: 1).

Run: python3 -m unittest discover tests/spec_check -v
"""
import os
import re
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SCRIPT = os.path.join(ROOT, "plugins", "forge", "skills", "forge", "scripts", "spec_check.py")

FRONT = {
    "contract": "1",
    "id": "SPEC-7",
    "revision": "2",
    "status": "proposed",
    "path": "standard",
    "source_rev": "9447a7f",
}

SECTIONS = {
    "Objective": "Cut tutor no-shows. Success: no-show rate measured for 4 weeks. Failure: < 80% lessons logged.",
    "Scope": "- Recurring lessons\n- 24h reminder",
    "Non-goals": "- Payments\n- Marketplace",
    "Users and value": "Tutor with existing families; job: keep slots filled.",
    "Journeys and rules": "Tutor adds weekly lesson → parent gets reminder 24h before.",
    "Requirements": "| ID | Requirement |\n|---|---|\n| R1 | Tutor creates weekly recurring lesson |\n| R2 | Parent gets reminder 24h before |",
    "Acceptance criteria": "| ID | Criterion | Verifies |\n|---|---|---|\n| AC1 | Weekly lesson appears for next 4 weeks | R1 |\n| AC2 | Reminder sent 24h ± 5 min before start | R2 |",
    "Constraints": "Solo founder, 3 days.",
    "Dependencies": "SMS provider account.",
    "KPIs": "No-show rate: baseline not measured (assumption 2/month/tutor), target -50%, from lesson outcomes.",
    "Telemetry": "- `lesson_created`\n- `reminder_sent`\n- `lesson_outcome_recorded`",
    "Priorities": "Now: lessons + reminders (3 days). Next: payments. Later: marketplace.",
}


def build(front=None, sections=None, drop=(), extra=""):
    f = dict(FRONT)
    f.update(front or {})
    s = dict(SECTIONS)
    s.update(sections or {})
    lines = ["---"] + ["%s: %s" % (k, v) for k, v in f.items() if v is not None] + ["---", "", "# Lessons + reminders", ""]
    for name, body in s.items():
        if name in drop:
            continue
        lines += ["## " + name, "", body, ""]
    return "\n".join(lines) + extra


class SpecCheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)

    def write(self, text, folder="07_lesson-reminders", name="2026-11-18_lesson-reminders_spec.md"):
        d = os.path.join(self.tmp.name, "tasks", folder)
        os.makedirs(d, exist_ok=True)
        p = os.path.join(d, name)
        with open(p, "w") as fh:
            fh.write(text)
        return p

    def run_check(self, path, *args):
        r = subprocess.run([sys.executable, SCRIPT, "check", path] + list(args),
                           capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def assertOk(self, text, *args, **kw):
        code, out = self.run_check(self.write(text, **kw), *args)
        self.assertEqual(code, 0, out)
        return out

    def assertError(self, text, needle, *args, **kw):
        code, out = self.run_check(self.write(text, **kw), *args)
        self.assertEqual(code, 1, out)
        self.assertIn(needle, out)
        return out

    # --- valid ---
    def test_valid_standard(self):
        out = self.assertOk(build())
        self.assertIn("OK SPEC-7 rev 2", out)

    def test_valid_fast_needs_only_core_sections(self):
        drop = ("Users and value", "Journeys and rules", "Constraints", "Dependencies", "KPIs", "Telemetry", "Priorities")
        self.assertOk(build(front={"path": "fast"}, drop=drop))

    def test_na_with_reason_accepted(self):
        self.assertOk(build(sections={"Telemetry": "n/a — no user-facing events"}))

    def test_legacy_without_contract_skipped(self):
        out = self.assertOk("# Old design\n\nStatus: design · ✅\n\n## Problem\nx\n")
        self.assertIn("legacy", out)

    # --- front matter ---
    def test_missing_field(self):
        self.assertError(build(front={"revision": None}), "revision")

    def test_bad_id_padded(self):
        self.assertError(build(front={"id": "SPEC-07"}), "id")

    def test_bad_id_lowercase(self):
        self.assertError(build(front={"id": "spec-7"}), "id")

    def test_id_must_match_task_folder(self):
        self.assertError(build(front={"id": "SPEC-8"}), "folder")

    def test_bad_status(self):
        self.assertError(build(front={"status": "in_progress"}), "status")

    def test_bad_path(self):
        self.assertError(build(front={"path": "huge"}), "path")

    def test_unsupported_contract_version(self):
        self.assertError(build(front={"contract": "2"}), "contract")

    def test_fixes_field_accepted(self):
        self.assertOk(build(front={"fixes": "[SPEC-3]"}))

    def test_fixes_field_invalid(self):
        self.assertError(build(front={"fixes": "[bug-3]"}), "fixes")

    # --- sections ---
    def test_missing_section_standard(self):
        self.assertError(build(drop=("KPIs",)), "KPIs")

    def test_empty_section(self):
        self.assertError(build(sections={"Non-goals": "<!-- fill -->"}), "Non-goals")

    def test_deep_requires_rollout_and_evidence(self):
        out = self.assertError(build(front={"path": "deep"}), "Rollout")
        self.assertIn("Evidence and assumptions", out)

    # --- R / AC ---
    def test_ac_cites_unknown_r(self):
        ac = "| ID | Criterion | Verifies |\n|---|---|---|\n| AC1 | x | R1 |\n| AC2 | y | R9 |"
        self.assertError(build(sections={"Acceptance criteria": ac}), "R9")

    def test_ac_without_r(self):
        ac = "| ID | Criterion | Verifies |\n|---|---|---|\n| AC1 | x | R1 |\n| AC2 | y | |\n| AC3 | z | R2 |"
        self.assertError(build(sections={"Acceptance criteria": ac}), "AC2")

    def test_r_without_ac(self):
        ac = "| ID | Criterion | Verifies |\n|---|---|---|\n| AC1 | x | R1 |"
        self.assertError(build(sections={"Acceptance criteria": ac}), "R2")

    def test_bullet_style_r_and_ac(self):
        self.assertOk(build(sections={
            "Requirements": "- R1 Tutor creates weekly lesson\n- R2 Reminder 24h before",
            "Acceptance criteria": "- AC1 (R1) lesson repeats\n- AC2 (R2) reminder on time",
        }))

    # --- status rules ---
    def test_approved_needs_approval_line(self):
        self.assertError(build(front={"status": "approved"}), "Approvals")

    def test_approval_for_old_revision_is_stale(self):
        text = build(front={"status": "approved"}, extra="\n## Approvals\n\n- 2026-11-18 Owner rev 1\n")
        self.assertError(text, "rev 1")

    def test_approved_ok(self):
        self.assertOk(build(front={"status": "approved"}, extra="\n## Approvals\n\n- 2026-11-18 Owner rev 2\n"))

    def test_dropped_needs_only_objective_and_decision(self):
        text = "\n".join(["---", "contract: 1", "id: SPEC-7", "revision: 1", "status: dropped",
                          "path: standard", "source_rev: abc1234", "---", "",
                          "## Objective", "", "AI forecasting for biggest customer.", "",
                          "## Decision", "", "Dropped 2026-11-18: 2/140 asked; test manual forecast first.", ""])
        self.assertOk(text)

    def test_dropped_without_decision(self):
        text = "\n".join(["---", "contract: 1", "id: SPEC-7", "revision: 1", "status: dropped",
                          "path: standard", "source_rev: abc1234", "---", "", "## Objective", "", "x", ""])
        self.assertError(text, "Decision")

    # --- template ---
    def test_filled_template_passes(self):
        tpl = os.path.join(ROOT, "plugins", "forge", "skills", "forge", "templates", "spec.md")
        with open(tpl) as fh:
            text = fh.read()
        text = (text.replace("SPEC-<n>", "SPEC-7")
                    .replace("<fast|standard|deep>", "standard")
                    .replace("<git short sha>", "9447a7f"))
        # fill every placeholder comment except the file-level note and the optional log sections
        text = re.sub(r"<!-- (fast\+|standard\+|deep|value|event|YYYY).*?-->", "filled", text)
        out = self.assertOk(text)
        self.assertIn("OK SPEC-7 rev 1", out)

    def test_unfilled_template_fails(self):
        tpl = os.path.join(ROOT, "plugins", "forge", "skills", "forge", "templates", "spec.md")
        with open(tpl) as fh:
            text = fh.read().replace("SPEC-<n>", "SPEC-7").replace("<fast|standard|deep>", "standard")
        self.assertError(text, "empty")

    # --- handoff flags ---
    def test_require_approved_rejects_proposed(self):
        self.assertError(build(), "approved", "--require-approved")

    def test_require_approved_accepts_approved(self):
        text = build(front={"status": "approved"}, extra="\n## Approvals\n\n- 2026-11-18 Owner rev 2\n")
        self.assertOk(text, "--require-approved")

    def test_pinned_rev_mismatch_is_stale(self):
        text = build(front={"status": "approved"}, extra="\n## Approvals\n\n- 2026-11-18 Owner rev 2\n")
        self.assertError(text, "stale", "--rev", "1")


if __name__ == "__main__":
    unittest.main()
