"""Tests for `spec_check.py prd`, `release`, `trace` (contract: 1, CT13).

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


def spec_text(status="verified", rev=2, released_in=""):
    lines = ["---", "contract: 1", "id: SPEC-1", "revision: %d" % rev, "status: %s" % status, "path: standard",
             "source_rev: abc1234"]
    if released_in:
        lines.append("released_in: %s" % released_in)
    lines += ["---", "", "# Archive projects", "", "## Objective", "Hide old projects. Success: x. Failure: y.", "",
              "## Requirements", "| ID | Requirement |", "|---|---|", "| R1 | archive |", "| R2 | list hides archived |", "",
              "## Acceptance criteria", "| ID | Criterion | Verifies |", "|---|---|---|",
              "| AC1 | archived_at set | R1 |", "| AC2 | default list excludes | R2 |", "",
              "## Approvals", "- 2026-11-18 Owner rev %d" % rev, ""]
    return "\n".join(lines)


PRD = """---
contract: 1
type: prd
revision: 2
status: approved
source_rev: abc1234
---

# projapp — PRD

## Product
Tiny project tracker.

## FEAT-1 Project list
Evidence: code-only (`src/projapp/projects.py:12`)
- FEAT-1.R1 List an org's projects, paged
{changed}

## FEAT-2 Create project
Evidence: exercised-local
- FEAT-2.R1 Name required

## Open decisions
- Q1 Should names be unique per org?
"""


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = self.tmp.name
        self.task = os.path.join(self.root, "tasks", "01_archive-projects")
        os.makedirs(os.path.join(self.task, "impl-tasks"))
        os.makedirs(os.path.join(self.root, "releases"))

    def put(self, rel, text):
        p = os.path.join(self.root, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as fh:
            fh.write(text)
        return p

    def spec(self, **kw):
        self.put("tasks/01_archive-projects/2026-11-18_archive-projects_spec.md", spec_text(**kw))

    def readiness(self):
        self.put("tasks/01_archive-projects/2026-11-18_readiness.md", "# Readiness — SPEC-1\n")

    def items(self, verified=True):
        self.put("tasks/01_archive-projects/impl-tasks/01_all.md",
                 "---\nid: SPEC-1.TASK1\ntype: story\nrefs: [R1, R2, AC1, AC2]\ndepends_on: []\nlayer: mixed\n---\n\n# 01 all\n")
        self.put("tasks/01_archive-projects/impl-tasks/ledger.md",
                 "| ID | Item | Type | Depends | Status | Verified by | Issue | Updated |\n|---|---|---|---|---|---|---|---|\n"
                 "| SPEC-1.TASK1 | all | story | — | %s | %s | — | 2026-11-18 |\n"
                 % (("✅ done", "`python3 -m unittest` → 9 OK") if verified else ("🔄 in progress", "—")))

    def prd(self, changed="Added by: SPEC-1"):
        return self.put("PRD.md", PRD.replace("{changed}", changed))

    def release(self, status="released", specs="- SPEC-1 @ rev 2", version="1.4.0"):
        return self.put("releases/v%s.md" % version, "\n".join([
            "---", "contract: 1", "type: release", "version: %s" % version, "status: %s" % status, "date: 2026-11-18",
            "---", "", "# Release v%s" % version, "", "## Specs", specs, ""]))

    def run_cmd(self, *args):
        r = subprocess.run([sys.executable, SCRIPT] + list(args), capture_output=True, text=True)
        return r.returncode, r.stdout + r.stderr

    def ok(self, *args):
        code, out = self.run_cmd(*args)
        self.assertEqual(code, 0, out)
        return out

    def err(self, needle, *args):
        code, out = self.run_cmd(*args)
        self.assertEqual(code, 1, out)
        self.assertIn(needle, out)
        return out


class PrdTest(Base):
    def test_valid_baseline_without_spec_links(self):
        out = self.ok("prd", self.prd(changed=""))
        self.assertIn("OK PRD rev 2: 2 features", out)

    def test_released_spec_link_ok(self):
        self.spec(status="released", released_in="v1.4.0")
        self.ok("prd", self.prd())

    def test_unreleased_spec_in_prd_is_error(self):
        self.spec(status="verified")
        self.err("SPEC-1", "prd", self.prd())

    def test_unknown_spec_in_prd(self):
        self.err("SPEC-9", "prd", self.prd(changed="Changed by: SPEC-9"))

    def test_missing_evidence_level(self):
        self.err("FEAT-2", "prd", self.put("PRD.md", PRD.replace("{changed}", "").replace("Evidence: exercised-local\n", "")))

    def test_bad_evidence_level(self):
        self.err("evidence", "prd", self.put("PRD.md", PRD.replace("{changed}", "").replace("exercised-local", "works-great")))

    def test_duplicate_feat(self):
        self.err("FEAT-1", "prd", self.put("PRD.md", PRD.replace("{changed}", "").replace("## FEAT-2 Create project", "## FEAT-1 Create project")))

    def test_requirement_under_wrong_feat(self):
        self.err("FEAT-1.R1", "prd", self.put("PRD.md", PRD.replace("{changed}", "").replace("- FEAT-2.R1 Name required", "- FEAT-1.R1 Name required")))

    def test_front_matter_type(self):
        self.err("type", "prd", self.put("PRD.md", PRD.replace("{changed}", "").replace("type: prd", "type: spec")))


class ReleaseTest(Base):
    def test_planned_release_of_verified_spec(self):
        self.spec(status="verified")
        self.readiness()
        self.ok("release", self.release(status="planned"))

    def test_planned_release_needs_readiness(self):
        self.spec(status="verified")
        self.err("readiness", "release", self.release(status="planned"))

    def test_planned_release_rejects_unverified_spec(self):
        self.spec(status="implemented")
        self.readiness()
        self.err("verified", "release", self.release(status="planned"))

    def test_rev_mismatch(self):
        self.spec(status="verified", rev=3)
        self.readiness()
        self.err("rev", "release", self.release(status="planned"))

    def test_released_requires_spec_released_and_prd(self):
        self.spec(status="released", released_in="v1.4.0")
        self.readiness()
        self.prd()
        self.ok("release", self.release())

    def test_released_but_spec_not_marked(self):
        self.spec(status="verified")
        self.readiness()
        self.prd(changed="")
        self.err("released", "release", self.release())

    def test_released_but_prd_missing_feature(self):
        self.spec(status="released", released_in="v1.4.0")
        self.readiness()
        self.prd(changed="")
        self.err("PRD", "release", self.release())

    def test_bad_version(self):
        self.err("version", "release", self.release(version="1.4"))


class TraceTest(Base):
    def test_full_trace_no_gaps(self):
        self.spec(status="released", released_in="v1.4.0")
        self.readiness()
        self.items()
        self.prd()
        self.release()
        out = self.ok("trace", self.root, "--strict")
        self.assertIn("0 gaps", out)

    def test_gaps_reported(self):
        self.spec(status="verified")
        self.items(verified=False)
        out = self.ok("trace", self.root)
        self.assertIn("SPEC-1.TASK1", out)          # no Verified by
        self.assertIn("not in any release", out)

    def test_strict_fails_on_gaps(self):
        self.spec(status="verified")
        self.items(verified=False)
        self.err("GAP", "trace", self.root, "--strict")

    def test_json(self):
        self.spec(status="released", released_in="v1.4.0")
        self.readiness()
        self.items()
        self.prd()
        self.release()
        data = json.loads(self.ok("trace", self.root, "--json"))
        s = data["specs"][0]
        self.assertEqual(s["id"], "SPEC-1")
        self.assertEqual(s["releases"], ["1.4.0"])
        self.assertEqual(s["prd_features"], ["FEAT-1"])
        self.assertEqual(data["gaps"], [])


if __name__ == "__main__":
    unittest.main()


class TemplateTest(Base):
    def fill(self, name):
        with open(os.path.join(SKILL, "templates", name)) as fh:
            return fh.read()

    def test_prd_template_filled_passes(self):
        t = (self.fill("prd.md").replace("<git short sha>", "abc1234")
             .replace("<verified-prod|exercised-local|code-only|docs-only|not-exercised>", "code-only"))
        self.ok("prd", self.put("PRD.md", t))

    def test_release_template_filled_passes(self):
        self.spec(status="verified")
        self.readiness()
        t = (self.fill("release.md").replace("<X.Y.Z>", "1.4.0").replace("<YYYY-MM-DD>", "2026-11-18")
             .replace("SPEC-<n> @ rev <N>", "SPEC-1 @ rev 2"))
        self.ok("release", self.put("releases/v1.4.0.md", t))
