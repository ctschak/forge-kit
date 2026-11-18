#!/usr/bin/env python3
"""Detect a repo's quality checks (lint, types, format, tests, build) without running them. Python 3.9+, stdlib.

Prefers what the project already defines (package scripts, CI steps, tool config) over forge defaults.
Reports tools that are configured-by-default but missing as `available: no` with a suggestion — it never
installs anything (rules/quality.md QG5).

Usage: python3 quality_detect.py <repo> [--json]
"""
import argparse
import json
import os
import re
import shutil
import sys

SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "dist", "build", "target", "__pycache__", ".next", "coverage"}
RANK = {"script": 0, "ci": 1, "config": 2, "default": 3}


def walk(repo, limit=4000):
    out = []
    for root, dirs, files in os.walk(repo):
        dirs[:] = [d for d in dirs if d not in SKIP_DIRS]
        for f in files:
            out.append(os.path.relpath(os.path.join(root, f), repo))
            if len(out) >= limit:
                return out
    return out


def read(repo, rel):
    try:
        with open(os.path.join(repo, rel), encoding="utf-8", errors="replace") as fh:
            return fh.read()
    except OSError:
        return ""


def kind_of(cmd):
    c = cmd.lower()
    if re.search(r"\b(eslint|ruff check|flake8|pylint|checkstyle|spotbugs|pmd|lint)\b", c):
        return "lint"
    if re.search(r"\b(tsc|mypy|pyright|typecheck|type-check|check-types)\b", c):
        return "type"
    if re.search(r"\b(prettier|black|ruff format|spotless|format)\b", c):
        return "format"
    if re.search(r"\b(audit|bandit|safety|snyk|trivy)\b", c):
        return "security"
    if re.search(r"\b(test|pytest|jest|vitest|playwright|unittest|mvn .*verify|gradlew? .*check|e2e)\b", c):
        return "test"
    return None


def detect(repo):
    files = walk(repo)
    names = {os.path.basename(f) for f in files}
    has = lambda pat: any(re.search(pat, f) for f in files)  # noqa: E731
    checks = {}

    def add(name, kind, command, source, available, suggest=None):
        cur = checks.get(command)
        if cur and RANK[cur["source"]] <= RANK[source]:
            return
        c = {"name": name, "kind": kind, "command": command, "source": source, "available": available}
        if suggest:
            c["suggest"] = suggest
        checks[command] = c

    profiles, languages = [], []

    # --- JS / TS
    pkg_raw = read(repo, "package.json")
    if pkg_raw or "tsconfig.json" in names or has(r"\.(ts|tsx)$"):
        languages.append("typescript" if ("tsconfig.json" in names or has(r"\.tsx?$")) else "javascript")
        profiles.append("js-ts")
        try:
            scripts = json.loads(pkg_raw).get("scripts", {}) if pkg_raw else {}
        except ValueError:
            scripts = {}
        nm = os.path.isdir(os.path.join(repo, "node_modules"))
        bin_ok = lambda t: "yes" if os.path.exists(os.path.join(repo, "node_modules", ".bin", t)) else "no"  # noqa: E731
        kinds_by_script = set()
        for s in sorted(scripts):
            k = kind_of(s) or kind_of(scripts[s] or "")
            if s in ("test",):
                k = "test"
            if not k:
                continue
            cmd = "npm test" if s == "test" else "npm run %s" % s
            add(s, k, cmd, "script", "yes" if nm else "unknown")
            kinds_by_script.add(k)
        if "tsconfig.json" in names and "type" not in kinds_by_script:
            add("tsc", "type", "npx tsc --noEmit", "default", bin_ok("tsc"),
                None if bin_ok("tsc") == "yes" else "add `typescript` dev dependency (version per project runtime) — with approval")
        eslint_cfg = any(n.startswith((".eslintrc", "eslint.config")) for n in names)
        if "lint" not in kinds_by_script:
            add("eslint", "lint", "npx eslint .", "config" if eslint_cfg else "default", bin_ok("eslint"),
                None if bin_ok("eslint") == "yes" else "add ESLint + typescript-eslint flat config (versions per project runtime) — with approval")
        if any(n.startswith(".prettierrc") or n.startswith("prettier.config") for n in names) and "format" not in kinds_by_script:
            add("prettier", "format", "npx prettier --check .", "config", bin_ok("prettier"))

    # --- Python
    py = read(repo, "pyproject.toml")
    if py or any(n.startswith("requirements") and n.endswith(".txt") for n in names) or "setup.py" in names or has(r"\.py$"):
        languages.append("python")
        profiles.append("python")
        which = lambda t: "yes" if shutil.which(t) else "no"  # noqa: E731
        if "[tool.ruff" in py:
            add("ruff", "lint", "ruff check .", "config", which("ruff"))
        else:
            add("ruff", "lint", "ruff check .", "default", which("ruff"),
                None if which("ruff") == "yes" else "add Ruff as dev dependency + `[tool.ruff]` — with approval")
        if "[tool.mypy" in py or "mypy.ini" in names:
            add("mypy", "type", "mypy .", "config", which("mypy"))
        if "[tool.black" in py:
            add("black", "format", "black --check .", "config", which("black"))
        if "[tool.pytest" in py or "pytest.ini" in names or "conftest.py" in names:
            add("pytest", "test", "pytest", "config", which("pytest"))
        elif has(r"(^|/)tests?/test_.*\.py$"):
            tdir = "tests" if os.path.isdir(os.path.join(repo, "tests")) else "test"
            add("unittest", "test", "python3 -m unittest discover %s" % tdir, "default", which("python3"))

    # --- Java
    if "pom.xml" in names or any(n.startswith("build.gradle") for n in names):
        languages.append("java")
        profiles.append("java")
        if "pom.xml" in names:
            mvnw = os.path.exists(os.path.join(repo, "mvnw"))
            add("maven", "build", "./mvnw -q verify" if mvnw else "mvn -q verify", "config",
                "yes" if mvnw or shutil.which("mvn") else "no")
        else:
            gw = os.path.exists(os.path.join(repo, "gradlew"))
            add("gradle", "build", "./gradlew check" if gw else "gradle check", "config",
                "yes" if gw or shutil.which("gradle") else "no")

    # --- Database
    if has(r"(^|/)migrations?/.*\.sql$") or has(r"(^|/)(alembic|flyway|liquibase)/") or "schema.prisma" in names or has(r"\.sql$"):
        profiles.append("database")

    # --- CI
    ci = sorted(f for f in files if re.match(r"^\.github/workflows/.+\.ya?ml$", f) or f in (".gitlab-ci.yml", "Jenkinsfile", "bitbucket-pipelines.yml"))
    for f in ci:
        text = read(repo, f)
        cmds = re.findall(r"^\s*-?\s*run:\s*([^|>\n][^\n]*)$", text, re.M)
        cmds += re.findall(r"^\s*-\s+([^\n:#][^\n]*)$", text, re.M) if f != "Jenkinsfile" and not f.startswith(".github") else []
        cmds += re.findall(r"sh\s+['\"]([^'\"]+)['\"]", text) if f == "Jenkinsfile" else []
        for cmd in cmds:
            cmd = cmd.strip().strip("'\"")
            k = kind_of(cmd)
            if k:
                add(cmd.split()[0], k, cmd, "ci", "unknown")

    out = sorted(checks.values(), key=lambda c: (["lint", "type", "format", "security", "test", "build"].index(c["kind"]), RANK[c["source"]], c["command"]))
    return {"languages": languages, "profiles": profiles, "ci": ci, "checks": out}


def main(argv=None):
    p = argparse.ArgumentParser(prog="quality_detect.py")
    p.add_argument("repo")
    p.add_argument("--json", action="store_true")
    a = p.parse_args(argv)
    d = detect(a.repo)
    if a.json:
        print(json.dumps(d, indent=2))
        return 0
    print("profiles: %s" % (", ".join(d["profiles"]) or "none"))
    print("ci: %s" % (", ".join(d["ci"]) or "none"))
    for c in d["checks"]:
        line = "%-8s %-40s source=%-7s available=%s" % (c["kind"], c["command"], c["source"], c["available"])
        if c.get("suggest"):
            line += "  → " + c["suggest"]
        print(line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
