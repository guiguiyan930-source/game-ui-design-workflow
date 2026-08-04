#!/bin/sh

set -eu

SCRIPT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
SOURCE_DIR="$SCRIPT_DIR/skills"
MODE=""
PROJECT_PATH=""
FORCE=0
DRY_RUN=0

usage() {
  cat <<'EOF'
Usage:
  ./install.sh --project /path/to/project [--force] [--dry-run]
  ./install.sh --personal [--force] [--dry-run]

Options:
  --project PATH  Install into PATH/.cursor/skills
  --personal      Install into ~/.cursor/skills
  --force         Replace existing skills with the same names
  --dry-run       Print actions without writing files
  -h, --help      Show this help
EOF
}

fail() {
  printf 'ERROR: %s\n' "$1" >&2
  exit 2
}

while [ "$#" -gt 0 ]; do
  case "$1" in
    --project)
      [ "$#" -ge 2 ] || fail "--project requires a path"
      [ -z "$MODE" ] || fail "choose exactly one installation mode"
      MODE="project"
      PROJECT_PATH=$2
      shift 2
      ;;
    --personal)
      [ -z "$MODE" ] || fail "choose exactly one installation mode"
      MODE="personal"
      shift
      ;;
    --force)
      FORCE=1
      shift
      ;;
    --dry-run)
      DRY_RUN=1
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    *)
      fail "unknown option: $1"
      ;;
  esac
done

[ -n "$MODE" ] || fail "choose --project PATH or --personal"
[ -d "$SOURCE_DIR" ] || fail "skills directory not found: $SOURCE_DIR"

if [ "$MODE" = "project" ]; then
  [ -d "$PROJECT_PATH" ] || fail "project directory not found: $PROJECT_PATH"
  TARGET_DIR="$PROJECT_PATH/.cursor/skills"
else
  [ -n "${HOME:-}" ] || fail "HOME is not set"
  TARGET_DIR="$HOME/.cursor/skills"
fi

if [ "$DRY_RUN" -eq 0 ]; then
  mkdir -p "$TARGET_DIR"
fi

installed=0
skipped=0
for source in "$SOURCE_DIR"/*; do
  [ -d "$source" ] || continue
  name=$(basename "$source")
  destination="$TARGET_DIR/$name"
  if [ -e "$destination" ] && [ "$FORCE" -eq 0 ]; then
    printf 'SKIP: %s already exists (use --force to replace)\n' "$destination"
    skipped=$((skipped + 1))
    continue
  fi
  if [ "$DRY_RUN" -eq 1 ]; then
    printf 'WOULD INSTALL: %s -> %s\n' "$source" "$destination"
  else
    if [ -e "$destination" ]; then
      rm -rf "$destination"
    fi
    cp -R "$source" "$destination"
    printf 'INSTALLED: %s\n' "$destination"
  fi
  installed=$((installed + 1))
done

printf 'Done: %s installed, %s skipped. Target: %s\n' \
  "$installed" "$skipped" "$TARGET_DIR"
