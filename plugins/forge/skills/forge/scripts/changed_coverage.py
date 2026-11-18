#!/usr/bin/env python3
"""Changed-line coverage from an existing coverage report. Python 3.9+, stdlib only.

Reads lcov (`lcov.info`) or Cobertura XML (`coverage.xml`, JaCoCo/cobertura converters, coverage.py `xml`)
and `git diff -U0 <base>` (+ untracked new files). Counts only changed lines the report marks executable;
a changed code file absent from the report counts all its changed non-blank lines as uncovered.
Never runs tests itself (rules/quality.md QG6).

Usage: python3 changed_coverage.py --report <file> [--repo .] [--base origin/main] [--target 80] [--json]
"""
import argparse
import json
import os
import re
import subprocess
import sys
import xml.etree.ElementTree as ET

CODE_EXT = {".py", ".js", ".jsx", ".mjs", ".cjs", ".ts", ".tsx", ".java", ".kt", ".go", ".rb", ".cs", ".php",
            ".scala", ".rs", ".swift", ".c", ".cc", ".cpp", ".h", ".hpp"}


def git(repo, *args):
    r = subprocess.run(["git", "-C", repo] + list(args), capture_output=True, text=True)
    if r.returncode != 0:
        raise SystemExit("ERROR git %s: %s" % (" ".join(args), r.stderr.strip()))
    return r.stdout


def changed_lines(repo, base):
    out, cur = {}, None
    for line in git(repo, "diff", "-U0", "--no-color", base, "--").splitlines():
        if line.startswith("+++ "):
            path = line[4:].strip()
            cur = None if path == "/dev/null" else re.sub(r"^b/", "", path)
            continue
        m = re.match(r"^@@ -\S+ \+(\d+)(?:,(\d+))? @@", line)
        if m and cur:
            start, count = int(m.group(1)), int(m.group(2) or "1")
            out.setdefault(cur, set()).update(range(start, start + count))
    for path in git(repo, "ls-files", "--others", "--exclude-standard").splitlines():
        try:
            with open(os.path.join(repo, path), encoding="utf-8", errors="replace") as fh:
                out[path] = set(range(1, sum(1 for _ in fh) + 1))
        except OSError:
            continue
    return {p: ls for p, ls in out.items() if os.path.splitext(p)[1] in CODE_EXT}


def norm_path(path, repo, sources=()):
    repo = os.path.realpath(repo)
    cands = [path] + [os.path.join(s, path) for s in sources]
    for c in cands:
        full = os.path.realpath(c if os.path.isabs(c) else os.path.join(repo, c))
        if full.startswith(repo + os.sep):
            return os.path.relpath(full, repo)
    return path.lstrip("./")


def read_report(report, repo):
    """{relpath: {line: hits}}"""
    cov = {}
    with open(report, encoding="utf-8", errors="replace") as fh:
        text = fh.read()
    if text.lstrip().startswith("<"):
        root = ET.fromstring(text)
        sources = [s.text.strip() for s in root.iter("source") if s.text]
        for cls in root.iter("class"):
            f = norm_path(cls.get("filename", ""), repo, sources)
            lines = cov.setdefault(f, {})
            for ln in cls.iter("line"):
                n, h = int(ln.get("number")), int(ln.get("hits", "0"))
                lines[n] = max(lines.get(n, 0), h)
    else:
        cur = None
        for line in text.splitlines():
            if line.startswith("SF:"):
                cur = cov.setdefault(norm_path(line[3:].strip(), repo), {})
            elif line.startswith("DA:") and cur is not None:
                n, h = line[3:].split(",")[:2]
                cur[int(n)] = max(cur.get(int(n), 0), int(float(h)))
            elif line.startswith("end_of_record"):
                cur = None
    return cov


def measure(report, repo, base):
    changed = changed_lines(repo, base)
    cov = read_report(report, repo)
    files, total, covered = {}, 0, 0
    for path in sorted(changed):
        lines = changed[path]
        if path in cov:
            execu = sorted(l for l in lines if l in cov[path])
            unc = [l for l in execu if cov[path][l] == 0]
            entry = {"changed_executable": len(execu), "covered": len(execu) - len(unc), "uncovered": unc,
                     "not_in_report": False}
        else:
            with open(os.path.join(repo, path), encoding="utf-8", errors="replace") as fh:
                src = fh.read().splitlines()
            execu = sorted(l for l in lines if l <= len(src) and src[l - 1].strip())
            entry = {"changed_executable": len(execu), "covered": 0, "uncovered": execu, "not_in_report": True}
        if entry["changed_executable"]:
            files[path] = entry
            total += entry["changed_executable"]
            covered += entry["covered"]
    pct = round(100.0 * covered / total, 1) if total else None
    return {"base": base, "changed_executable": total, "covered": covered, "percent": pct, "files": files}


def main(argv=None):
    p = argparse.ArgumentParser(prog="changed_coverage.py")
    p.add_argument("--report", required=True)
    p.add_argument("--repo", default=".")
    p.add_argument("--base", default="HEAD")
    p.add_argument("--target", type=float)
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    d = measure(a.report, a.repo, a.base)
    if a.json:
        print(json.dumps(d, indent=2))
        return 0
    if d["percent"] is None:
        print("changed-line coverage: no changed executable lines vs %s" % a.base)
        return 0
    line = "changed-line coverage: %.1f%% (%d/%d) vs %s" % (d["percent"], d["covered"], d["changed_executable"], a.base)
    if a.target is not None:
        line += " — %s target %g" % ("meets" if d["percent"] >= a.target else "below", a.target)
    print(line)
    for f, e in d["files"].items():
        if e["uncovered"]:
            print("  %s uncovered: %s%s" % (f, ",".join(map(str, e["uncovered"])), " (not in report)" if e["not_in_report"] else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
