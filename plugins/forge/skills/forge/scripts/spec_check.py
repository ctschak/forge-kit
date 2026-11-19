#!/usr/bin/env python3
"""Validate a forge spec against rules/contract.md (contract: 1). Python 3.9+, stdlib only.

Usage:
  python3 spec_check.py check <spec.md> [--require-approved] [--rev N]
  python3 spec_check.py gaps <doc.md> [--path fast|standard|deep]      # report only, exit 0
  python3 spec_check.py plan <task dir> [--json]                       # work items, batches, critical path
  python3 spec_check.py prd <root>/PRD.md                              # released behavior only, FEAT evidence
  python3 spec_check.py release <root>/releases/vX.Y.Z.md              # specs, revs, readiness, PRD
  python3 spec_check.py trace <root> [--json] [--strict]               # R → item → evidence → release → PRD

Exit: 0 ok (or legacy doc skipped) · 1 errors.
"""
import argparse
import json
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


UX_PROTO_RE = re.compile(r"\]\((ux/rev-[0-9]+/[^)\s]*\.html)\)")
IMG_RE = re.compile(r"!\[[^\]]*\]\(([^)\s]+)\)")
DEF_U_RE = re.compile(r"^\s*(?:[-*]\s*|\|\s*)\**U([0-9]+)\b")


def check_ux(path, sections, rs):
    """CT14: `ui: true` → `## UX` links an existing prototype, image paths exist, U rules cite existing R."""
    body = sections.get(norm("UX"))
    if body is None:
        return ["ERROR ui: `## UX` missing → run stages/ux.md (prototype, screenshots, U rules) (CT14)"]
    errors = []
    body = COMMENT_RE.sub("", body)
    folder = os.path.dirname(os.path.abspath(path))
    protos = UX_PROTO_RE.findall(body)
    if not protos:
        errors.append("ERROR ui: `## UX` links no prototype → add [prototype](ux/rev-N/index.html) (CT14)")
    for rel in protos:
        if not os.path.isfile(os.path.join(folder, rel)):
            errors.append("ERROR ui: prototype `%s` not found → build it (stages/ux.md step 3)" % rel)
    for rel in IMG_RE.findall(body):
        if "://" not in rel and not os.path.isfile(os.path.join(folder, rel)):
            errors.append("ERROR ui: screenshot `%s` not found → capture it or remove the link (rules/ux.md UX2)" % rel)
    for line in body.splitlines():
        m = DEF_U_RE.match(line)
        if not m:
            continue
        cited = {int(x) for x in CITE_R.findall(line[m.end():])}
        if not cited:
            errors.append("ERROR U%s: cites no requirement → add the R<n> it serves (CT14)" % m.group(1))
        for c in sorted(cited - set(rs)):
            errors.append("ERROR U%s: cites R%d which is not in `## Requirements`" % (m.group(1), c))
    return errors


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

    for ref in [x.strip() for x in front.get("fixes", "").strip("[]").split(",") if x.strip()]:
        if not ID_RE.match(ref):
            err("ERROR front matter: fixes `%s` invalid → `[SPEC-<n>]`" % ref)

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

    if front.get("ui", "").lower() == "true" and status != "dropped":
        errors.extend(check_ux(path, sections, defined("R", sections.get(norm("Requirements"), ""))))

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


VAGUE = ("fast", "quick", "quickly", "easy", "simple", "user-friendly", "intuitive", "scalable",
         "robust", "seamless", "better", "efficient")


def gaps(path, spath=None):
    """Report (never fix) what a doc is missing to become a contract spec. Always exit 0."""
    with open(path, encoding="utf-8") as fh:
        front, sections = parse(fh.read())
    spath = spath or (front or {}).get("path") or "standard"
    out = []
    for name in SECTIONS_BY_PATH.get(spath, STANDARD):
        key = norm(name)
        if key not in sections:
            out.append("GAP section: `## %s` missing" % name)
        elif not has_text(sections[key]):
            out.append("GAP section: `## %s` empty" % name)
    obj = sections.get(norm("Objective"))
    if obj is not None and not (re.search(r"success", obj, re.I) and re.search(r"fail", obj, re.I)):
        out.append("GAP Objective: no success + failure criteria")
    rs = defined("R", sections.get(norm("Requirements"), ""))
    acs = defined("AC", sections.get(norm("Acceptance criteria"), ""))
    covered = set()
    for rest in acs.values():
        covered |= {int(x) for x in CITE_R.findall(rest)}
    for n, text in sorted(rs.items()):
        low = text.lower()
        hits = [w for w in VAGUE if re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(w), low)]
        if hits and not re.search(r"\d", text):
            out.append("GAP R%d: vague wording '%s' without a number → state a measurable target" % (n, hits[0]))
        if n not in covered:
            out.append("GAP R%d: no acceptance criterion" % n)
    for line in out:
        print(line)
    print("%d gaps (path %s)" % (len(out), spath))
    return 0


ITEM_TYPES = ("story", "enabler", "spike", "bug", "task")
LAYERS = ("db", "backend", "frontend", "integration", "telemetry", "test", "mixed")
ITEM_ID_RE = re.compile(r"^(SPEC-[1-9][0-9]*)\.TASK([1-9][0-9]*)$")
REF_RE = re.compile(r"^(?:SPEC-[0-9]+\.)?(R|AC)([0-9]+)$")
PIN_RE = re.compile(r"Spec:\s*(SPEC-[0-9]+)\s*@\s*rev\s*([0-9]+)")


def as_list(value):
    v = (value or "").strip()
    if v.startswith("[") and v.endswith("]"):
        v = v[1:-1]
    return [x.strip().strip("'\"") for x in v.split(",") if x.strip()]


def task_num(item_id):
    return int(ITEM_ID_RE.match(item_id).group(2))


def plan(task_dir, as_json=False):
    """Check work items in <task_dir>/impl-tasks against the task's spec; print batches + critical path."""
    errors = []
    err = errors.append
    specs = sorted(f for f in os.listdir(task_dir) if f.endswith("_spec.md"))
    if len(specs) != 1:
        print("ERROR plan: expected one *_spec.md in %s, found %d" % (task_dir, len(specs)))
        return 1
    with open(os.path.join(task_dir, specs[0]), encoding="utf-8") as fh:
        sfront, ssections = parse(fh.read())
    sfront = sfront or {}
    sid, srev = sfront.get("id", ""), sfront.get("revision", "")
    rs = set(defined("R", ssections.get(norm("Requirements"), "")))
    acs = set(defined("AC", ssections.get(norm("Acceptance criteria"), "")))

    pinned = None
    for f in sorted(os.listdir(task_dir)):
        if f.endswith("_design.md"):
            with open(os.path.join(task_dir, f), encoding="utf-8") as fh:
                m = PIN_RE.search(fh.read())
            if m:
                pinned = int(m.group(2))
                if srev.isdigit() and pinned != int(srev):
                    err("ERROR design: pinned %s @ rev %d but spec is rev %s — design is stale → re-check scope"
                        % (m.group(1), pinned, srev))

    idir = os.path.join(task_dir, "impl-tasks")
    files = sorted(f for f in (os.listdir(idir) if os.path.isdir(idir) else [])
                   if re.match(r"^\d+_.+\.md$", f))
    if not files:
        print("ERROR plan: no work items in %s → run impl-plan" % idir)
        return 1

    items = {}
    for f in files:
        with open(os.path.join(idir, f), encoding="utf-8") as fh:
            text = fh.read()
        front, sections = parse(text)
        front = front or {}
        iid = front.get("id", "")
        m = ITEM_ID_RE.match(iid)
        if not m:
            err("ERROR %s: id `%s` invalid → `%s.TASK<n>`" % (f, iid, sid or "SPEC-n"))
            continue
        if sid and m.group(1) != sid:
            err("ERROR %s: id %s belongs to %s, task spec is %s" % (f, iid, m.group(1), sid))
        if int(m.group(2)) != int(f.split("_", 1)[0]):
            err("ERROR %s: id %s does not match file number → TASK<n> = file NN" % (f, iid))
        if iid in items:
            err("ERROR %s: id %s reused (also %s)" % (f, iid, items[iid]["file"]))
            continue
        itype, layer = front.get("type", ""), front.get("layer", "")
        if itype not in ITEM_TYPES:
            err("ERROR %s: type `%s` invalid → %s" % (f, itype, ", ".join(ITEM_TYPES)))
        if layer not in LAYERS:
            err("ERROR %s: layer `%s` invalid → %s" % (f, layer, ", ".join(LAYERS)))
        refs = as_list(front.get("refs"))
        for r in refs:
            rm = REF_RE.match(r)
            if rm and int(rm.group(2)) not in (rs if rm.group(1) == "R" else acs):
                err("ERROR %s: ref %s not in spec %s" % (f, r, sid))
        title = re.search(r"^#\s+(?:\d+\s+)?(.+?)\s*$", text, re.M)
        paths = re.findall(r"`([^`]+)`", sections.get(norm("Files"), ""))
        outcome = COMMENT_RE.sub("", sections.get(norm("Outcome"), "")).strip().splitlines()
        items[iid] = {"id": iid, "type": itype, "layer": layer, "refs": refs,
                      "outcome": outcome[0].strip() if outcome else "",
                      "depends_on": as_list(front.get("depends_on")),
                      "title": title.group(1) if title else f, "file": "impl-tasks/" + f,
                      "_paths": sorted(paths)}

    covered = set()
    for it in items.values():
        for r in it["refs"]:
            rm = REF_RE.match(r)
            if rm:
                covered.add((rm.group(1), int(rm.group(2))))
    for n in sorted(rs):
        if ("R", n) not in covered:
            err("ERROR coverage: R%d has no work item → add it to an item's refs" % n)
    for n in sorted(acs):
        if ("AC", n) not in covered:
            err("ERROR coverage: AC%d has no work item → add it to an item's refs" % n)

    for it in items.values():
        for d in it["depends_on"]:
            if d not in items:
                err("ERROR %s: depends on unknown %s" % (it["file"], d))
    seen = {}
    for it in sorted(items.values(), key=lambda x: task_num(x["id"])):
        key = (tuple(sorted(it["refs"])), tuple(it["_paths"]))
        if key in seen:
            err("ERROR duplicate: %s and %s have the same refs and files → merge or differentiate"
                % (seen[key], it["id"]))
        else:
            seen[key] = it["id"]

    # cycle detection (DFS)
    state, stack = {}, []

    def visit(n):
        state[n] = 1
        stack.append(n)
        for d in items[n]["depends_on"]:
            if d not in items:
                continue
            if state.get(d) == 1:
                cyc = stack[stack.index(d):] + [d]
                err("ERROR cycle: %s" % " → ".join(cyc))
                return True
            if state.get(d) is None and visit(d):
                return True
        stack.pop()
        state[n] = 2
        return False

    for n in sorted(items, key=task_num):
        if state.get(n) is None and visit(n):
            break

    if errors:
        for e in errors:
            print(e)
        return 1

    order = sorted(items, key=task_num)
    level, length, prev = {}, {}, {}

    def lvl(n):
        if n not in level:
            deps = items[n]["depends_on"]
            level[n] = 1 + max([lvl(d) for d in deps] or [0])
            best = None
            for d in sorted(deps, key=task_num):
                lvl(d)
                if best is None or length[d] > length[best]:
                    best = d
            length[n] = 1 + (length[best] if best else 0)
            prev[n] = best
        return level[n]

    for n in order:
        lvl(n)
    batches = [[n for n in order if level[n] == k] for k in range(1, max(level.values()) + 1)]
    end = max(order, key=lambda n: (length[n], -task_num(n)))
    path = []
    while end:
        path.append(end)
        end = prev[end]
    path.reverse()

    if as_json:
        out = {"spec": sid, "revision": int(srev) if srev.isdigit() else srev, "design_pinned_rev": pinned,
               "task_dir": task_dir, "spec_file": specs[0],
               "items": [{k: v for k, v in items[n].items() if not k.startswith("_")} for n in order],
               "batches": batches, "critical_path": path}
        print(json.dumps(out, indent=2, ensure_ascii=False))
    else:
        print("OK plan %s rev %s: %d items" % (sid, srev, len(items)))
        for k, b in enumerate(batches, 1):
            print("batch %d: %s" % (k, ", ".join(b)))
        print("critical path: %s" % " → ".join(path))
    return 0


EVIDENCE = ("verified-prod", "exercised-local", "code-only", "docs-only", "not-exercised")
SEMVER_RE = re.compile(r"^v?(\d+\.\d+\.\d+)$")
SPEC_REF_RE = re.compile(r"\bSPEC-([1-9][0-9]*)\b")


def read_front(path):
    with open(path, encoding="utf-8") as fh:
        text = fh.read()
    front, sections = parse(text)
    return front or {}, sections, text


def load_specs(root):
    """{SPEC-id: {front, sections, task_dir, path}} for contract specs under <root>/tasks/."""
    out = {}
    tdir = os.path.join(root, "tasks")
    for d in sorted(os.listdir(tdir)) if os.path.isdir(tdir) else []:
        full = os.path.join(tdir, d)
        if not os.path.isdir(full):
            continue
        for f in sorted(os.listdir(full)):
            if f.endswith("_spec.md"):
                front, sections, _ = read_front(os.path.join(full, f))
                if front.get("contract") and front.get("id"):
                    out[front["id"]] = {"front": front, "sections": sections, "task_dir": full,
                                        "path": os.path.join(full, f)}
    return out


def ver(v):
    m = SEMVER_RE.match((v or "").strip())
    return m.group(1) if m else None


def prd_features(text):
    """Parse `## FEAT-n name` sections → {n: {name, evidence, reqs, cites}} plus order list."""
    feats, order, cur = {}, [], None
    for line in text.splitlines():
        m = re.match(r"^##\s+FEAT-([1-9][0-9]*)\s+(.*?)\s*$", line)
        if m:
            cur = int(m.group(1))
            order.append(cur)
            feats.setdefault(cur, {"name": m.group(2), "evidence": None, "reqs": [], "cites": []})
            continue
        if line.startswith("## "):
            cur = None
            continue
        if cur is None:
            continue
        e = re.match(r"^\s*Evidence:\s*([A-Za-z-]+)", line)
        if e:
            feats[cur]["evidence"] = e.group(1)
        for r in re.findall(r"^\s*(?:[-*]|\|)\s*\**FEAT-([0-9]+)\.R([0-9]+)\b", line):
            feats[cur]["reqs"].append((int(r[0]), int(r[1])))
        c = re.match(r"^\s*(?:Added|Changed) by:\s*(.*)$", line)
        if c:
            feats[cur]["cites"] += ["SPEC-%s" % n for n in SPEC_REF_RE.findall(c.group(1))]
    return feats, order


def prd(path):
    errors = []
    err = errors.append
    front, _, text = read_front(path)
    for f in ("contract", "type", "revision", "status", "source_rev"):
        if not front.get(f):
            err("ERROR front matter: `%s` missing" % f)
    if front.get("type") and front["type"] != "prd":
        err("ERROR front matter: type `%s` → `prd`" % front["type"])
    if front.get("status") and front["status"] not in ("proposed", "approved"):
        err("ERROR front matter: status `%s` → proposed or approved" % front["status"])
    feats, order = prd_features(text)
    if not feats:
        err("ERROR PRD: no `## FEAT-<n> <name>` sections")
    for n in sorted({x for x in order if order.count(x) > 1}):
        err("ERROR FEAT-%d: defined more than once → IDs are unique, never reused" % n)
    specs = load_specs(os.path.dirname(os.path.abspath(path)))
    seen_reqs = set()
    for n in sorted(feats):
        f = feats[n]
        if not f["evidence"]:
            err("ERROR FEAT-%d: no `Evidence:` line → one of %s" % (n, ", ".join(EVIDENCE)))
        elif f["evidence"] not in EVIDENCE:
            err("ERROR FEAT-%d: evidence `%s` invalid → one of %s" % (n, f["evidence"], ", ".join(EVIDENCE)))
        for fn, rn in f["reqs"]:
            if fn != n:
                err("ERROR FEAT-%d.R%d: defined under FEAT-%d → move it or renumber" % (fn, rn, n))
            if (fn, rn) in seen_reqs:
                err("ERROR FEAT-%d.R%d: defined more than once" % (fn, rn))
            seen_reqs.add((fn, rn))
        for sid in f["cites"]:
            if sid not in specs:
                err("ERROR FEAT-%d: cites %s, not found under tasks/" % (n, sid))
            elif specs[sid]["front"].get("status") != "released":
                err("ERROR FEAT-%d: cites %s (status %s) — PRD holds released behavior only (CT13)"
                    % (n, sid, specs[sid]["front"].get("status")))
    for e in errors:
        print(e)
    if not errors:
        print("OK PRD rev %s: %d features" % (front.get("revision"), len(feats)))
    return 1 if errors else 0


def release_specs(sections):
    return [("SPEC-%s" % a, int(b)) for a, b in
            re.findall(r"\bSPEC-([1-9][0-9]*)\s*@\s*rev\s*([0-9]+)", sections.get(norm("Specs"), ""))]


def release(path):
    errors = []
    err = errors.append
    front, sections, _ = read_front(path)
    root = os.path.dirname(os.path.dirname(os.path.abspath(path)))
    if front.get("type") != "release":
        err("ERROR front matter: type `%s` → `release`" % front.get("type"))
    v = ver(front.get("version"))
    if not v:
        err("ERROR front matter: version `%s` → semver X.Y.Z" % front.get("version"))
    status = front.get("status")
    if status not in ("planned", "released"):
        err("ERROR front matter: status `%s` → planned or released" % status)
    if not front.get("date"):
        err("ERROR front matter: `date` missing")
    listed = release_specs(sections)
    if not listed:
        err("ERROR `## Specs`: no `SPEC-n @ rev N` lines")
    specs = load_specs(root)
    prd_path = os.path.join(root, "PRD.md")
    cited = set()
    if os.path.exists(prd_path):
        with open(prd_path, encoding="utf-8") as fh:
            for f in prd_features(fh.read())[0].values():
                cited |= set(f["cites"])
    for sid, rev in listed:
        s = specs.get(sid)
        if not s:
            err("ERROR %s: not found under tasks/" % sid)
            continue
        sf = s["front"]
        if sf.get("revision") != str(rev):
            err("ERROR %s: release lists rev %d but spec is rev %s → re-check scope" % (sid, rev, sf.get("revision")))
        if not [f for f in os.listdir(s["task_dir"]) if f.endswith("_readiness.md")]:
            err("ERROR %s: no readiness report in %s → run review code first" % (sid, os.path.basename(s["task_dir"])))
        st = sf.get("status")
        if status == "planned" and st not in ("verified", "released"):
            err("ERROR %s: status %s — a release needs verified specs" % (sid, st))
        if status == "released":
            if st != "released" or ver(sf.get("released_in")) != v:
                err("ERROR %s: not marked released in v%s (status %s, released_in %s)"
                    % (sid, v, st, sf.get("released_in") or "—"))
            if sid not in cited:
                err("ERROR %s: PRD has no FEAT `Added by` / `Changed by` %s" % (sid, sid))
    for e in errors:
        print(e)
    if not errors:
        print("OK release v%s (%s): %d spec(s)" % (v, status, len(listed)))
    return 1 if errors else 0


def ledger_rows(task_dir):
    p = os.path.join(task_dir, "impl-tasks", "ledger.md")
    rows = {}
    if not os.path.exists(p):
        return rows
    with open(p, encoding="utf-8") as fh:
        lines = fh.read().splitlines()
    col = None
    for line in lines:
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if "Verified by" in cells:
            col = cells.index("Verified by")
            continue
        if col is not None and ITEM_ID_RE.match(cells[0]) and len(cells) > col:
            rows[cells[0]] = cells[col]
    return rows


def trace(root, as_json=False, strict=False):
    specs = load_specs(root)
    rel_by_spec, rdir = {}, os.path.join(root, "releases")
    for f in sorted(os.listdir(rdir)) if os.path.isdir(rdir) else []:
        if f.endswith(".md"):
            front, sections, _ = read_front(os.path.join(rdir, f))
            for sid, _ in release_specs(sections):
                rel_by_spec.setdefault(sid, []).append(ver(front.get("version")) or f)
    prd_by_spec = {}
    if os.path.exists(os.path.join(root, "PRD.md")):
        with open(os.path.join(root, "PRD.md"), encoding="utf-8") as fh:
            for n, f in sorted(prd_features(fh.read())[0].items()):
                for sid in f["cites"]:
                    prd_by_spec.setdefault(sid, []).append("FEAT-%d" % n)
    gaps, report = [], []
    for sid in sorted(specs, key=lambda x: int(x.split("-")[1])):
        s = specs[sid]
        st = s["front"].get("status", "")
        rs = sorted(defined("R", s["sections"].get(norm("Requirements"), "")))
        acs = sorted(defined("AC", s["sections"].get(norm("Acceptance criteria"), "")))
        idir = os.path.join(s["task_dir"], "impl-tasks")
        items, covered = [], set()
        for f in sorted(os.listdir(idir)) if os.path.isdir(idir) else []:
            if re.match(r"^\d+_.+\.md$", f):
                fr, _, _ = read_front(os.path.join(idir, f))
                if fr.get("id"):
                    items.append(fr["id"])
                    for r in as_list(fr.get("refs")):
                        m = REF_RE.match(r)
                        if m:
                            covered.add((m.group(1), int(m.group(2))))
        led = ledger_rows(s["task_dir"])
        if st in APPROVED_OR_LATER and items:
            gaps += ["%s: R%d has no work item" % (sid, n) for n in rs if ("R", n) not in covered]
            gaps += ["%s: AC%d has no work item" % (sid, n) for n in acs if ("AC", n) not in covered]
        if st in ("verified", "released"):
            for i in items:
                if led.get(i, "—") in ("", "—", "-"):
                    gaps.append("%s: %s has no `Verified by` evidence" % (sid, i))
        if st == "verified" and sid not in rel_by_spec:
            gaps.append("%s: verified, not in any release" % sid)
        if st == "released" and sid not in prd_by_spec:
            gaps.append("%s: released but no PRD FEAT cites it" % sid)
        report.append({"id": sid, "status": st, "requirements": ["R%d" % n for n in rs],
                       "acceptance": ["AC%d" % n for n in acs], "items": items,
                       "releases": rel_by_spec.get(sid, []), "prd_features": prd_by_spec.get(sid, [])})
    if as_json:
        print(json.dumps({"specs": report, "gaps": gaps}, indent=2))
    else:
        for r in report:
            print("%s (%s): %d R · %d AC · %d items · releases %s · PRD %s" % (
                r["id"], r["status"], len(r["requirements"]), len(r["acceptance"]), len(r["items"]),
                ", ".join("v" + v for v in r["releases"]) or "—", ", ".join(r["prd_features"]) or "—"))
        for g in gaps:
            print("GAP " + g)
        print("%d gaps" % len(gaps))
    return 1 if (strict and gaps) else 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="spec_check.py")
    sub = p.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("check", help="validate one spec file")
    c.add_argument("spec")
    c.add_argument("--require-approved", action="store_true", help="fail unless status is approved or later")
    c.add_argument("--rev", type=int, help="revision the design is pinned to; mismatch = stale")
    g = sub.add_parser("gaps", help="report what a doc lacks to be a contract spec (read-only)")
    g.add_argument("doc")
    g.add_argument("--path", choices=PATHS)
    pl = sub.add_parser("plan", help="check work items of a task; print batches + critical path")
    pl.add_argument("task_dir")
    pl.add_argument("--json", action="store_true", help="machine-readable manifest")
    pr = sub.add_parser("prd", help="validate the living PRD (released behavior only)")
    pr.add_argument("prd_file")
    rl = sub.add_parser("release", help="validate a release doc")
    rl.add_argument("release_file")
    tr = sub.add_parser("trace", help="R → item → evidence → release → PRD, with gaps")
    tr.add_argument("root")
    tr.add_argument("--json", action="store_true")
    tr.add_argument("--strict", action="store_true", help="exit 1 when gaps exist")
    a = p.parse_args(argv)
    if a.cmd == "prd":
        return prd(a.prd_file)
    if a.cmd == "release":
        return release(a.release_file)
    if a.cmd == "trace":
        return trace(a.root, a.json, a.strict)
    if a.cmd == "gaps":
        return gaps(a.doc, a.path)
    if a.cmd == "plan":
        return plan(a.task_dir, a.json)
    errors, msg = check(a.spec, a.require_approved, a.rev)
    for e in errors:
        print(e)
    if msg:
        print(msg)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
