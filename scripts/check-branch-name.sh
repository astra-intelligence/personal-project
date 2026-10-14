#!/bin/sh
# Shared by the pre-push hook and CI, so the branch naming rule lives in one place.
branch="$1"
pattern='^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)/[0-9]+-[a-z0-9]+(-[a-z0-9]+)*$'
if ! printf '%s' "$branch" | grep -Eq "$pattern"; then
  echo "Branch '$branch' must match <type>/<issue>-<short-description>, e.g. feat/12-hero-section"
  exit 1
fi
