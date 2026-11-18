#!/bin/bash
# Build a fresh fixture repo for a scenario.
# usage: setup.sh <variant> <dest-dir>
# variants: empty · projapp · projapp-independent · projapp-prd-input · shelftrack · webapp · webapp-lint
set -eu
VARIANT=$1; DEST=$2
HERE=$(cd "$(dirname "$0")/.." && pwd)
F=$HERE/fixtures
[ -e "$DEST" ] && { echo "dest exists: $DEST (pick a new dir)" >&2; exit 1; }
mkdir -p "$DEST"
case "$VARIANT" in
  empty)               echo "# scratch" > "$DEST/README.md" ;;
  projapp)             cp -R "$F/projapp/." "$DEST/" ;;
  projapp-independent) cp -R "$F/projapp/." "$DEST/"; printf "forge-review: independent\n" > "$DEST/CLAUDE.md" ;;
  projapp-prd-input)   cp -R "$F/projapp/." "$DEST/"; mkdir -p "$DEST/docs"; cp "$F/inputs/prd-export.md" "$DEST/docs/prd-export.md" ;;
  shelftrack)          cp -R "$F/shelftrack/." "$DEST/" ;;
  webapp)              cp -R "$F/webapp/." "$DEST/" ;;
  webapp-lint)         cp -R "$F/webapp/." "$DEST/"
                       python3 - "$DEST/src/cart-badge.ts" <<'PY'
import sys
p = sys.argv[1]
with open(p) as fh:
    s = fh.read()
s = s.replace("export function cartBadge(count: number): Badge {\n",
              "export function cartBadge(count: number): Badge {\n  console.log(\"badge\", count);\n")
with open(p, "w") as fh:
    fh.write(s)
PY
                       ;;
  *) echo "unknown variant: $VARIANT" >&2; exit 1 ;;
esac
cd "$DEST"
git init -q
git add -A
git -c user.name=fixture -c user.email=fixture@example.com commit -qm "fixture: $VARIANT"
echo "ready: $DEST ($VARIANT @ $(git rev-parse --short HEAD))"
