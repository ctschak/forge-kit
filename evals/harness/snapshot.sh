#!/bin/bash
# Copy a forge plugin version to test against (so later edits don't change a running eval).
# usage: snapshot.sh <dest-dir> [git-ref]   — no ref = current working tree
set -eu
DEST=$1; REF=${2:-}
ROOT=$(cd "$(dirname "$0")/../.." && pwd)
[ -e "$DEST" ] && { echo "dest exists: $DEST" >&2; exit 1; }
mkdir -p "$DEST"
if [ -n "$REF" ]; then
  git -C "$ROOT" archive "$REF" plugins/forge | tar -x -C "$DEST"
  mv "$DEST/plugins/forge" "$DEST/forge" && rmdir "$DEST/plugins"
else
  cp -R "$ROOT/plugins/forge" "$DEST/forge"
fi
grep '"version"' "$DEST/forge/.claude-plugin/plugin.json"
echo "plugin dir: $DEST/forge"
