#!/usr/bin/env bash
# Publish this project to https://github.com/XhuleMetaj
set -euo pipefail
cd "$(dirname "$0")/.."

echo "=== Sign in to GitHub as XhuleMetaj (not agaci1) ==="
gh auth login -h github.com -p https -w
gh auth switch -u XhuleMetaj

echo "=== Create repository and push ==="
gh repo create project-nested-structure-parser-with-pushdown-automata-XhuleMetaj \
  --public \
  --source=. \
  --remote=origin \
  --description "CEN350: Nested mathematical expression parser using a Pushdown Automaton (Project 93)" \
  --push

echo "Done: https://github.com/XhuleMetaj/project-nested-structure-parser-with-pushdown-automata-XhuleMetaj"
