#!/usr/bin/env bash
# Auto-sync hook: commits and pushes any uncommitted changes to GitHub
# after each Claude Code turn. Stays silent on no-op and on push errors
# (e.g. offline) so it never blocks responses.

repo="$(git rev-parse --show-toplevel 2>/dev/null)" || exit 0
cd "$repo" || exit 0

if [ -z "$(git status --porcelain)" ]; then
  exit 0
fi

git add -A
git commit -m "Auto-sync: Claude Code update" >/dev/null 2>&1 || exit 0
git push >/dev/null 2>&1 || true
exit 0
