#!/usr/bin/env python3
"""Validate a forge spec against rules/contract.md (contract: 1). Python 3.9+, stdlib only.

Usage:
  python3 spec_check.py check <spec.md> [--require-approved] [--rev N]

Exit: 0 ok (or legacy doc skipped) · 1 errors.
"""
import argparse
import os
import re
import sys

CONTRACT = 1
STATUSES = ("proposed", "approved", "implemented", "verified", "released", "dropped")
APPROVED_OR_LATER = ("approved", "implemented", "verified", "released")
PATHS = ("fast", "standard", "deep")
REQUIRED_FIELDS = ("contract", "id", "revision", "status", "path", "source_rev")

CORE = ["Objective", "Scope", "Non-goals", "Requirements", "Acceptance criteria"]
STANDARD = CORE + ["Users and value", "Journeys and rules", "Constraints", "Dependencies",
                   "KPIs", "Telemetry", "Priorities"]
SECTIONS_BY_PATH = {
    "fast": CORE,
    "standard": STANDARD,
    "deep": STANDARD + ["Evidence and assumptions", "Rollout"],
}
DROPPED_SECTIONS = ["Objective", "Decision"]

ID_RE = re.compile(r"^SPEC-[1-9][0-9]*$")
DEF_RE = {
    "R": re.compile(r"^\s*(?:[-*]\s*|\|\s*)\**R([0-9]+)\b"),
    "AC": re.compile(r"^\s*(?:[-*]\s*|\|\s*)\**AC([0-9]+)\b"),
}
CITE_R = re.compile(r"\bR([0-9]+)\b")
APPROVAL_RE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b.*\brev\s+([0-9]+)\b")
COMMENT_RE = re.compile(r"<!--.*?-->", re.S)


def norm(name):
    return re.sub(r"\s+", " ", name.replace("&", "and")).strip().lower()


def parse(text):
    """Return (front matter dict or None, {normalized heading: body})."""
    front = None
    body = text
    if text.startswith("---\n"):
        end = text.find("\n---", 4)
        if end != -1:
            front = {}
            for line in text[4:end].splitlines():
                if ":" in line and not line.lstrip().startswith("#"):
                    k, v = line.split(":", 1)
                    front[k.strip()] = v.split(" #", 1)[0].strip()
            body = text[end + 4:]
    sections, current = {}, None
    for line in body.splitlines():
        m = re.match(r"^##\s+(.+?)\s*$", line)
        if m and not line.startswith("###"):
            current = norm(m.group(1))
            sections[current] = []
        elif current is not None:
            sections[current].append(line)
    return front, {k: "\n".join(v) for k, v in sections.items()}


def has_text(body):
    return bool(COMMENT_RE.sub("", body).strip())


def defined(kind, body):
    out = {}
    for line in body.splitlines():
        m = DEF_RE[kind].match(line)
        if m:
            out[int(m.group(1))] = line[m.end():]
    return out


def check(path, require_approved=False, pinned_rev=None):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    front, sections = parse(text)
    if not front or "contract" not in front:
        return [], "NOTICE %s: no `contract:` front matter — legacy doc, skipped" % path

    errors = []
    err = errors.append
    for f in REQUIRED_FIELDS:
        if not front.get(f):
            err("ERROR front matter: `%s` missing → add it (rules/contract.md CT2)" % f)

    if front.get("contract") and front["contract"] != str(CONTRACT):
        err("ERROR front matter: contract %s unsupported (this validator: %d) → upgrade forge or migrate doc"
            % (front["contract"], CONTRACT))
        return errors, None

    sid = front.get("id", "")
    if sid and not ID_RE.match(sid):
        err("ERROR front matter: id `%s` invalid → `SPEC-<n>`, no zero-padding" % sid)
    folder = os.path.basename(os.path.dirname(os.path.abspath(path)))
    fm = re.match(r"^(\d+)_", folder)
    if sid and ID_RE.match(sid) and fm and int(fm.group(1)) != int(sid.split("-")[1]):
        err("ERROR front matter: id %s does not match task folder `%s` → SPEC-<n> = folder number"
            % (sid, folder))

    rev = front.get("revision", "")
    if rev and not rev.isdigit():
        err("ERROR front matter: revision `%s` not a number" % rev)
    status = front.get("status", "")
    if status and status not in STATUSES:
        err("ERROR front matter: status `%s` invalid → one of %s" % (status, ", ".join(STATUSES)))
    spath = front.get("path", "")
    if spath and spath not in PATHS:
        err("ERROR front matter: path `%s` invalid → fast, standard or deep" % spath)

    required = DROPPED_SECTIONS if status == "dropped" else SECTIONS_BY_PATH.get(spath, CORE)
    for name in required:
        key = norm(name)
        if key not in sections:
            err("ERROR section: `## %s` missing (required for %s) → add it or write `n/a — <why>`"
                % (name, "dropped" if status == "dropped" else spath))
        elif not has_text(sections[key]):
            err("ERROR section: `## %s` empty → fill it or write `n/a — <why>`" % name)

    if status != "dropped" and norm("Requirements") in sections and norm("Acceptance criteria") in sections:
        rs = defined("R", sections[norm("Requirements")])
        acs = defined("AC", sections[norm("Acceptance criteria")])
        if not rs:
            err("ERROR section: `## Requirements` has no R<n> → number requirements R1, R2…")
        if not acs:
            err("ERROR section: `## Acceptance criteria` has no AC<n> → number criteria AC1, AC2…")
        covered = set()
        for n, rest in sorted(acs.items()):
            cited = {int(x) for x in CITE_R.findall(rest)}
            if not cited:
                err("ERROR AC%d: cites no requirement → add the R<n> it verifies" % n)
            for c in sorted(cited - set(rs)):
                err("ERROR AC%d: cites R%d which is not in `## Requirements`" % (n, c))
            covered |= cited
        for n in sorted(set(rs) - covered):
            err("ERROR R%d: no acceptance criterion → add an AC that verifies R%d" % (n, n))

    if status in APPROVED_OR_LATER:
        approvals = sections.get(norm("Approvals"), "")
        revs = [int(m.group(1)) for m in (APPROVAL_RE.search(l) for l in approvals.splitlines()) if m]
        if not revs:
            err("ERROR status %s: `## Approvals` needs a line `YYYY-MM-DD <name> rev <n>`" % status)
        elif rev.isdigit() and int(rev) not in revs:
            err("ERROR status %s: latest approval is rev %d but spec is rev %s → re-approve or set status proposed"
                % (status, max(revs), rev))

    if require_approved and status not in APPROVED_OR_LATER:
        err("ERROR handoff: status `%s` — engineering needs an approved spec → approve it first" % status)
    if pinned_rev is not None and rev.isdigit() and int(rev) != pinned_rev:
        err("ERROR handoff: design pinned rev %d but spec is rev %s — design is stale → re-check scope changes"
            % (pinned_rev, rev))

    ok = None if errors else "OK %s rev %s (%s, %s)" % (sid, rev, spath, status)
    return errors, ok


def main(argv=None):
    p = argparse.ArgumentParser(prog="spec_check.py")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="validate one spec file")
    c.add_argument("spec")
    c.add_argument("--require-approved", action="store_true", help="fail unless status is approved or later")
    c.add_argument("--rev", type=int, help="revision the design is pinned to; mismatch = stale")
    a = p.parse_args(argv)
    errors, msg = check(a.spec, a.require_approved, a.rev)
    for e in errors:
        print(e)
    if msg:
        print(msg)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
