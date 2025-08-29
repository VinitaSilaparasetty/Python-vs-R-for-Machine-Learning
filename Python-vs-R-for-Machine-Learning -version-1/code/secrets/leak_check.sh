#!/usr/bin/env bash
set -euo pipefail

git init -q .
echo "API_KEY=topsecret" > .env
echo ".env" > .gitignore

# Simulate accidental force add
git add -f .env || true

if git status --porcelain | grep -q ".env"; then
  echo "WARNING: .env staged!"
else
  echo "OK: .env not staged"
fi

grep -R "API_KEY=" -n . | sed 's/^/HINT: /' || true
