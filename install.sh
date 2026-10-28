#!/usr/bin/env bash
# Copy every India Trading Skill into ~/.claude/skills (existing copies are updated).
set -euo pipefail
cd "$(dirname "$0")"
DEST="${CLAUDE_SKILLS_DIR:-$HOME/.claude/skills}"
mkdir -p "$DEST"
for skill in skills/*/; do
  name="$(basename "$skill")"
  rm -rf "${DEST:?}/$name"
  cp -R "$skill" "$DEST/$name"
  echo "installed $name"
done
echo "Done. Open Claude Code and ask: \"Where do I start with Indian stock market?\""
