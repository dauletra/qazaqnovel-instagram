#!/usr/bin/env bash
# Render a post: bash render.sh posts/…/post.yaml [--sheet]
# Creates .venv in the repository root on first run.
set -euo pipefail

SKILL="$(cd "$(dirname "$0")/.." && pwd)"
ROOT="$(git -C "$SKILL" rev-parse --show-toplevel 2>/dev/null || pwd)"
VENV="$ROOT/.venv"

if [ ! -x "$VENV/bin/python" ]; then
  python3 -m venv "$VENV"
  "$VENV/bin/pip" install -q -r "$SKILL/scripts/requirements.txt"
fi

# A preinstalled Chromium (Claude Code cloud sessions) or Playwright's own.
if [ -z "${CHROMIUM:-}" ]; then
  if [ -x /opt/pw-browsers/chromium ]; then
    export CHROMIUM=/opt/pw-browsers/chromium
  elif ! ls "${PLAYWRIGHT_BROWSERS_PATH:-$HOME/.cache/ms-playwright}"/chromium* >/dev/null 2>&1; then
    "$VENV/bin/python" -m playwright install chromium
  fi
fi

exec "$VENV/bin/python" "$SKILL/scripts/render.py" "$@"
