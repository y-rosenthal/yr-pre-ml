#!/usr/bin/env bash
# build_book.sh: build the book's website (Jupyter Book v1) into jb/_build/html, as the GitHub Action does.
# The build runs every notebook (jb/_config.yml: execute_notebooks: force). A warning fails the build.
#   tools/build_book.sh [--clean] [--open]
#   --clean     delete the old build first (do it after a change to jb/_toc.yml or jb/_config.yml)
#   --open      open jb/_build/html/index.html in the browser at the end
#   -h, --help  show this help and stop
# It uses the jb of .venv (see README.md), or of the environment in YR_PRE_ML_VENV, else the jb on PATH (as in the
# GitHub Action). It puts tools/localdata on PYTHONPATH, so the data URLs read the CSV files in data/
# (tools/localdata/sitecustomize.py).
set -euo pipefail
case "${1:-}" in -h|--help) sed -n '2,/^[^#]/{/^#/s/^# \{0,1\}//p}' "$0"; exit 0 ;; esac
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
VENV="${YR_PRE_ML_VENV:-$ROOT/.venv}"
JB="$VENV/bin/jb"
[ -x "$JB" ] || JB="$(command -v jb || true)"
[ -n "$JB" ] || { echo "build_book.sh: no jb in $VENV or on PATH: make the environment (README.md)" >&2; exit 2; }
CLEAN=0; OPEN=0
for arg in "$@"; do
  case "$arg" in
    --clean) CLEAN=1 ;;
    --open) OPEN=1 ;;
    *) echo "build_book.sh: unknown option $arg (--help)" >&2; exit 2 ;;
  esac
done
export PYTHONPATH="$ROOT/tools/localdata${PYTHONPATH:+:$PYTHONPATH}"
[ "$CLEAN" = 1 ] && "$JB" clean "$ROOT/jb"
"$JB" build "$ROOT/jb" -W -n --keep-going
echo "The book: $ROOT/jb/_build/html/index.html"
[ "$OPEN" = 1 ] && xdg-open "$ROOT/jb/_build/html/index.html" >/dev/null 2>&1 || true
