#!/usr/bin/env sh
set -eu

if [ "$#" -ne 1 ]; then
  echo "Usage: $0 /path/to/blender-source-v4.5.9" >&2
  exit 2
fi
PROJECT_ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
SOURCE_ROOT=$(CDPATH= cd -- "$1" && pwd)
EXPECTED=$(python3 -c 'import pathlib,tomllib; print(tomllib.loads(pathlib.Path("'"$PROJECT_ROOT"'/upstream.lock").read_text())["commit"])')
ACTUAL=$(git -C "$SOURCE_ROOT" rev-parse HEAD)
if [ "$ACTUAL" != "$EXPECTED" ]; then
  echo "Refusing to patch source at $ACTUAL; expected pinned Blender commit $EXPECTED" >&2
  exit 1
fi
git -C "$SOURCE_ROOT" apply --check "$PROJECT_ROOT/patches/0001-topbar-language-selector.patch"
git -C "$SOURCE_ROOT" apply "$PROJECT_ROOT/patches/0001-topbar-language-selector.patch"
echo "Applied the prototype patch to Blender $ACTUAL. This does not build or test Blender."
