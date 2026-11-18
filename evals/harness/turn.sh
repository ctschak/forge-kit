#!/bin/bash
# One headless turn of a forge eval scenario. Resumes the run's session if one exists.
# usage: turn.sh <run-dir> <plugin-dir> "<user message>"
# env:   FORGE_EVAL_BUDGET (USD per call, default 3)
set -u
RUN=$1; PLUG=$2; MSG=$3
cd "$RUN" || { echo "no run dir: $RUN" >&2; exit 1; }
ARGS=(-p --setting-sources project --plugin-dir "$PLUG" --add-dir "$PLUG" --permission-mode acceptEdits
      --allowedTools "Bash(python3:*)" "Bash(npm:*)" "Bash(node:*)" "Bash(npx:*)"
      --max-budget-usd "${FORGE_EVAL_BUDGET:-3}" --output-format json)
[ -f .session ] && ARGS+=(--resume "$(cat .session)")
START=$(date +%s)
claude "${ARGS[@]}" "$MSG" > .last.json 2> .last.err
END=$(date +%s)
python3 - "$RUN" $((END - START)) <<'PY'
import json, sys
run, secs = sys.argv[1], sys.argv[2]
with open(run + "/.last.json") as fh:
    d = json.load(fh)
with open(run + "/.session", "w") as fh:
    fh.write(d["session_id"])
with open(run + "/.log.md", "a") as fh:
    fh.write("\n---\nturn secs=%s cost=%s\n\n%s\n" % (secs, d.get("total_cost_usd"), d["result"]))
print(d["result"])
print("\n[secs=%s cost=%s]" % (secs, d.get("total_cost_usd")))
PY
