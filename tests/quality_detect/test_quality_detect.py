"""Tests for plugins/forge/skills/forge/scripts/quality_detect.py.

Run: python3 -m unittest discover tests/quality_detect -v
"""
import json
import os
import subprocess
import sys
import tempfile
import unittest

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
SCRIPT = os.path.join(ROOT, "plugins", "forge", "skills", "forge", "scripts", "quality_detect.py")


class DetectTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.repo = self.tmp.name

    def put(self, rel, text=""):
        p = os.path.join(self.repo, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "w") as fh:
            fh.write(text)

    def detect(self):
        r = subprocess.run([sys.executable, SCRIPT, self.repo, "--json"], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return json.loads(r.stdout)

    def check(self, data, command):
        for c in data["checks"]:
            if c["command"] == command:
                return c
        self.fail("no check %r in %s" % (command, [c["command"] for c in data["checks"]]))

    def test_ts_with_scripts(self):
        self.put("package.json", json.dumps({"scripts": {"lint": "eslint .", "typecheck": "tsc --noEmit", "test": "node --test"}}))
        self.put("tsconfig.json", "{}")
        self.put("eslint.config.js", "export default []")
        d = self.detect()
        self.assertIn("js-ts", d["profiles"])
        for cmd, kind in (("npm run lint", "lint"), ("npm run typecheck", "type"), ("npm test", "test")):
            c = self.check(d, cmd)
            self.assertEqual(c["source"], "script")
            self.assertEqual(c["kind"], kind)

    def test_ts_without_scripts_uses_default_tsc(self):
        self.put("package.json", json.dumps({"name": "x"}))
        self.put("tsconfig.json", "{}")
        c = self.check(self.detect(), "npx tsc --noEmit")
        self.assertEqual(c["source"], "default")
        self.assertEqual(c["available"], "no")          # no node_modules/.bin/tsc
        self.put("node_modules/.bin/tsc", "")
        self.assertEqual(self.check(self.detect(), "npx tsc --noEmit")["available"], "yes")

    def test_python_pyproject_config(self):
        self.put("pyproject.toml", "[tool.ruff]\nline-length = 100\n\n[tool.pytest.ini_options]\naddopts = \"-q\"\n")
        self.put("src/app.py", "x = 1\n")
        d = self.detect()
        self.assertIn("python", d["profiles"])
        self.assertEqual(self.check(d, "ruff check .")["source"], "config")
        self.assertEqual(self.check(d, "pytest")["source"], "config")

    def test_python_bare_unittest(self):
        self.put("src/app.py", "x = 1\n")
        self.put("tests/test_app.py", "import unittest\n")
        d = self.detect()
        c = self.check(d, "python3 -m unittest discover tests")
        self.assertEqual(c["source"], "default")
        self.assertEqual(c["available"], "yes")
        ruff = self.check(d, "ruff check .")
        self.assertIn(ruff["available"], ("yes", "no"))
        if ruff["available"] == "no":
            self.assertTrue(ruff.get("suggest"))

    def test_java_maven(self):
        self.put("pom.xml", "<project><build><plugins><plugin><artifactId>maven-checkstyle-plugin</artifactId></plugin></plugins></build></project>")
        d = self.detect()
        self.assertIn("java", d["profiles"])
        self.assertEqual(self.check(d, "mvn -q verify")["source"], "config")

    def test_gradle(self):
        self.put("build.gradle.kts", "plugins { java }")
        self.put("gradlew", "#!/bin/sh")
        d = self.detect()
        self.assertIn("java", d["profiles"])
        self.check(d, "./gradlew check")

    def test_migrations_add_database_profile(self):
        self.put("db/migrations/001_init.sql", "CREATE TABLE t (id int);")
        self.assertIn("database", self.detect()["profiles"])

    def test_ci_commands(self):
        self.put(".github/workflows/ci.yml", "jobs:\n  t:\n    steps:\n      - run: npm ci\n      - run: npm run lint\n")
        self.put(".gitlab-ci.yml", "test:\n  script:\n    - pytest -q\n")
        d = self.detect()
        self.assertEqual(self.check(d, "npm run lint")["source"], "ci")
        self.assertEqual(self.check(d, "pytest -q")["source"], "ci")
        self.assertIn(".github/workflows/ci.yml", d["ci"])

    def test_empty_repo(self):
        d = self.detect()
        self.assertEqual(d["profiles"], [])
        self.assertEqual(d["checks"], [])

    def test_text_output(self):
        self.put("src/app.py", "x = 1\n")
        r = subprocess.run([sys.executable, SCRIPT, self.repo], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0)
        self.assertIn("profiles: python", r.stdout)


if __name__ == "__main__":
    unittest.main()
