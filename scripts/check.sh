#!/usr/bin/env bash
# Structural checks for the forge plugin. Exit 0 = all pass.
# Usage: bash scripts/check.sh   (from repo root or anywhere)

set -u
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
PLUGIN="$ROOT/plugins/forge"
SKILL_DIR="$PLUGIN/skills/forge"
SKILL="$SKILL_DIR/SKILL.md"
MAX_SKILL_LINES=150
fails=0

fail() { echo "FAIL: $1"; fails=$((fails + 1)); }
pass() { echo "ok:   $1"; }

# 1. Manifests parse
for f in "$ROOT/.claude-plugin/marketplace.json" "$PLUGIN/.claude-plugin/plugin.json"; do
  rel="${f#$ROOT/}"
  if [ ! -f "$f" ]; then fail "$rel missing"; continue; fi
  if python3 -m json.tool "$f" >/dev/null 2>&1; then pass "$rel parses"; else fail "$rel invalid JSON"; fi
done

# 2. plugin.json required fields
PJ="$PLUGIN/.claude-plugin/plugin.json"
if [ -f "$PJ" ]; then
  python3 - "$PJ" <<'PY' || fails=$((fails + 1))
import json, sys
d = json.load(open(sys.argv[1]))
missing = [k for k in ("name", "version", "description") if not d.get(k)]
if d.get("name") != "forge":
    missing.append("name!=forge")
if missing:
    print("FAIL: plugin.json missing/invalid: " + ", ".join(missing)); sys.exit(1)
print("ok:   plugin.json fields")
PY
fi

# 2b. Official validator (if claude CLI present)
if command -v claude >/dev/null 2>&1; then
  for target in "$ROOT" "$PLUGIN"; do
    rel="${target#$ROOT}"; rel="${rel#/}"; rel="${rel:-.}"
    out=$(claude plugin validate "$target" 2>&1)
    if echo "$out" | grep -q 'Validation passed'; then
      pass "claude plugin validate $rel"
      echo "$out" | grep '❯' || true
    else
      fail "claude plugin validate $rel"; echo "$out"
    fi
  done
else
  echo "skip: claude CLI not found, official validator not run"
fi

# 3. SKILL.md frontmatter + size
if [ ! -f "$SKILL" ]; then
  fail "SKILL.md missing"
else
  head -1 "$SKILL" | grep -q '^---$' || fail "SKILL.md no frontmatter"
  grep -q '^name: forge$' "$SKILL" || fail "SKILL.md frontmatter name != forge"
  grep -q '^description: ' "$SKILL" || fail "SKILL.md frontmatter description missing"
  lines=$(wc -l < "$SKILL" | tr -d ' ')
  if [ "$lines" -lt "$MAX_SKILL_LINES" ]; then pass "SKILL.md $lines lines"; else fail "SKILL.md $lines lines (max $((MAX_SKILL_LINES - 1)))"; fi
fi

# 4. Every referenced rules/stages/domains/templates file exists
if [ -d "$SKILL_DIR" ]; then
  refs=$(grep -rhoE '(rules|stages|domains|templates)/[a-z0-9-]+\.md' "$SKILL_DIR" 2>/dev/null | sort -u)
  for r in $refs; do
    [ -f "$SKILL_DIR/$r" ] || fail "broken ref: $r"
  done
  [ -n "$refs" ] && pass "refs checked ($(echo "$refs" | wc -l | tr -d ' '))"
fi

# 4b. Every routed stage/rule/template exists (SKILL.md routes some via patterns)
EXPECTED="stages/onboard.md stages/ai-readiness.md stages/design.md stages/architect.md
stages/impl-plan.md stages/develop.md stages/test.md stages/review.md
stages/discover.md stages/spec.md rules/contract.md templates/spec.md scripts/spec_check.py
rules/guardrails.md rules/doc-style.md rules/api-standards.md rules/code-standards.md
rules/test-standards.md rules/security-checklist.md rules/diagrams.md
templates/design.md templates/impl-task.md templates/ledger.md templates/review.md
templates/understanding.md templates/health.md templates/tasks-index.md
domains/crm.md domains/voice-message-agents.md domains/ecommerce.md"
missing=0
for e in $EXPECTED; do [ -f "$SKILL_DIR/$e" ] || { fail "expected file missing: $e"; missing=1; }; done
[ "$missing" -eq 0 ] && pass "all expected files present"

# 4c. Validator unit tests
log=$(mktemp)
if python3 -m unittest discover -s "$ROOT/tests/spec_check" >"$log" 2>&1; then
  pass "spec_check tests ($(grep -o 'Ran [0-9]* tests' "$log"))"
else
  fail "spec_check tests"; cat "$log"
fi
rm -f "$log"

# 5. No placeholders left in skill files
if [ -d "$SKILL_DIR" ]; then
  hits=$(grep -rnE '\b(TODO|TBD)\b' "$SKILL_DIR" 2>/dev/null)
  if [ -n "$hits" ]; then fail "placeholders:"; echo "$hits"; else pass "no TODO/TBD"; fi
fi

echo "---"
if [ "$fails" -eq 0 ]; then echo "PASS"; exit 0; else echo "$fails check(s) failed"; exit 1; fi
