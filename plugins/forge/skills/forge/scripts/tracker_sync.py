#!/usr/bin/env python3
"""Provider-neutral tracker sync planner + ledger writer for forge. Python 3.9+, stdlib only.

The agent does the provider calls (gh / glab / MCP, see rules/trackers.md); this script only decides
what to do and records results, so reruns are idempotent and testable.

Usage:
  python3 tracker_sync.py plan --manifest plan.json --existing issues.json [--native-deps]
      plan.json   = output of `spec_check.py plan <task dir> --json`
      issues.json = [{"ref": "#12", "url": "...", "state": "opened", "body": "..."}] — every issue
                    whose body contains `forge:<SPEC-n>` (any state)
      prints JSON {"actions": [...], "summary": {...}}; actions in safe order (deps first, parent last)
  python3 tracker_sync.py ledger <ledger.md> --set SPEC-7.TASK2=<url> [--set ...]
      writes verified issue URLs into the ledger `Issue` column; refuses to overwrite a different URL

Exit: 0 ok · 1 error.
"""
import argparse
import json
import re
import sys

MARKER_RE = re.compile(r"<!--\s*forge:(SPEC-[0-9]+(?:\.TASK[0-9]+)?)\s+rev=([0-9]+)\s*-->")


def marker(fid, rev):
    return "<!-- forge:%s rev=%d -->" % (fid, rev)


def index_existing(existing, spec):
    found = {}
    for iss in existing:
        for fid, rev in MARKER_RE.findall(iss.get("body", "")):
            if fid == spec or fid.startswith(spec + "."):
                found.setdefault(fid, []).append({"ref": iss["ref"], "url": iss.get("url"), "rev": int(rev)})
    return found


def plan(man, existing, native_deps):
    spec, rev = man["spec"], int(man["revision"])
    task_dir = man.get("task_dir", "").rstrip("/")
    found = index_existing(existing, spec)
    order = [i for batch in man.get("batches", []) for i in batch]
    items = {i["id"]: i for i in man["items"]}
    order += [i for i in items if i not in order]

    known, actions = {}, []

    def status_of(fid):
        hits = found.get(fid, [])
        if len(hits) > 1:
            return "conflict", hits
        if len(hits) == 1:
            known[fid] = hits[0]["ref"]
            return ("skip" if hits[0]["rev"] == rev else "update"), hits
        return "create", hits

    states = {fid: status_of(fid) for fid in order + [spec]}

    def ref(fid):
        return known.get(fid, "{{%s}}" % fid)

    for fid in order:
        it = items[fid]
        act, hits = states[fid]
        deps = it.get("depends_on", [])
        lines = [marker(fid, rev),
                 "**%s · %s · %s**" % (fid, it.get("type", ""), it.get("layer", "")), ""]
        if it.get("outcome"):
            lines += ["Outcome: %s" % it["outcome"], ""]
        lines += ["- Spec: `%s/%s` @ rev %d — refs: %s" % (task_dir, man.get("spec_file", ""), rev,
                                                        ", ".join(it.get("refs", [])) or "—"),
                  "- Work item (authoritative: scope, acceptance criteria, verify): `%s/%s`" % (task_dir, it.get("file", ""))]
        if deps and not native_deps:
            lines.append("- Depends on: %s" % ", ".join("%s (%s)" % (d, ref(d)) for d in deps))
        lines += ["", "_Managed by forge: edit the work item file, not this description. Live status lives here._"]
        actions.append({
            "action": act, "id": fid, "existing": [h["ref"] for h in hits] if act == "conflict" else (hits[0]["ref"] if hits else None),
            "title": "[%s] %s" % (fid, it.get("title", "")),
            "labels": ["forge", it.get("type", "task"), spec],
            "blocked_by": [ref(d) for d in deps] if native_deps else [],
            "body": "\n".join(lines),
        })

    act, hits = states[spec]
    slug = task_dir.rsplit("/", 1)[-1].split("_", 1)[-1] if task_dir else spec
    plines = [marker(spec, rev), "**%s** — spec `%s/%s` @ rev %d" % (spec, task_dir, man.get("spec_file", ""), rev), "",
              "Work items (dependency order):"]
    plines += ["- [ ] %s %s — %s" % (fid, ref(fid), items[fid].get("title", "")) for fid in order]
    plines += ["", "_Managed by forge._"]
    actions.append({"action": act, "id": spec,
                    "existing": [h["ref"] for h in hits] if act == "conflict" else (hits[0]["ref"] if hits else None),
                    "title": "[%s] %s" % (spec, slug), "labels": ["forge", spec], "blocked_by": [],
                    "body": "\n".join(plines)})

    for fid in sorted(found):
        if fid != spec and fid not in items:
            for h in found[fid]:
                actions.append({"action": "orphan", "id": fid, "existing": h["ref"], "title": "", "labels": [],
                                "blocked_by": [],
                                "body": "%s is no longer in %s rev %d. Proposed: comment and leave open for a human decision — never closed by forge." % (fid, spec, rev)})

    summary = {k: 0 for k in ("create", "skip", "update", "conflict", "orphan")}
    for a in actions:
        summary[a["action"]] += 1
    return {"spec": spec, "revision": rev, "actions": actions, "summary": summary}


def ledger(path, sets):
    with open(path, encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    header = next((i for i, l in enumerate(lines) if l.startswith("|") and "Issue" in l), None)
    if header is None:
        print("ERROR ledger: no table with an `Issue` column in %s" % path)
        return 1
    cols = [c.strip() for c in lines[header].strip().strip("|").split("|")]
    col = cols.index("Issue")
    wanted, errors = {}, []
    for s in sets:
        if "=" not in s:
            errors.append("ERROR --set %s: expected ID=URL" % s)
            continue
        k, v = s.split("=", 1)
        wanted[k.strip()] = v.strip()
    done = set()
    for i in range(header + 2, len(lines)):
        if not lines[i].startswith("|"):
            break
        cells = [c.strip() for c in lines[i].strip().strip("|").split("|")]
        if cells[0] in wanted:
            cur, new = cells[col], wanted[cells[0]]
            if cur not in ("", "—", "-") and cur != new:
                errors.append("ERROR %s: ledger already has %s, refusing to overwrite with %s" % (cells[0], cur, new))
            cells[col] = new
            lines[i] = "| " + " | ".join(cells) + " |"
            done.add(cells[0])
    for k in wanted:
        if k not in done:
            errors.append("ERROR %s: no ledger row" % k)
    if errors:
        for e in errors:
            print(e)
        return 1
    with open(path, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines))
    print("OK ledger: %d issue link(s) recorded" % len(done))
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="tracker_sync.py")
    sub = p.add_subparsers(dest="cmd", required=True)
    pl = sub.add_parser("plan")
    pl.add_argument("--manifest", required=True)
    pl.add_argument("--existing", required=True)
    pl.add_argument("--native-deps", action="store_true", help="tracker supports blocked-by links")
    lg = sub.add_parser("ledger")
    lg.add_argument("ledger")
    lg.add_argument("--set", action="append", default=[], metavar="ID=URL")
    a = p.parse_args(argv)
    if a.cmd == "ledger":
        return ledger(a.ledger, a.set)
    with open(a.manifest, encoding="utf-8") as fh:
        man = json.load(fh)
    with open(a.existing, encoding="utf-8") as fh:
        existing = json.load(fh)
    print(json.dumps(plan(man, existing, a.native_deps), indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
