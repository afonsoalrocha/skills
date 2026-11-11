#!/usr/bin/env bash
# Copy one plugin's skills into another project's skills directory.
# Usage: scripts/sync.sh <plugin> <dest>
# Writes <dest>/.skills-lock.json with the source commit and, when HEAD is
# exactly a tag, that tag. The lock records HEAD, so run it from the commit
# you mean to pin.
set -euo pipefail

if [[ $# -ne 2 ]]; then
  echo "usage: scripts/sync.sh <plugin> <dest>" >&2
  exit 2
fi

plugin="$1"
dest="$2"

if [[ ! "$plugin" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
  echo "error: plugin name must be kebab-case" >&2
  exit 2
fi

root="$(git -C "$(dirname "$0")" rev-parse --show-toplevel)"
plugin_dir="$root/plugins/$plugin"
source_dir="$plugin_dir/skills"

if [[ ! -d "$plugin_dir" ]]; then
  echo "error: unknown plugin '$plugin'" >&2
  exit 1
fi
if [[ ! -d "$source_dir" ]]; then
  echo "error: plugins/$plugin has no skills/ directory" >&2
  exit 1
fi

mkdir -p "$dest"
dest_real="$(cd "$dest" && pwd -P)"
source_real="$(cd "$source_dir" && pwd -P)"

case "$dest_real" in
  "$source_real" | "$source_real"/*)
    echo "error: destination is inside the plugin skills directory" >&2
    exit 1
    ;;
esac
case "$source_real" in
  "$dest_real"/*)
    echo "error: plugin skills directory is inside the destination" >&2
    exit 1
    ;;
esac

if [[ -n "$(git -C "$root" status --porcelain -- "plugins/$plugin/skills")" ]]; then
  echo "warning: plugins/$plugin/skills has uncommitted changes; the lock records HEAD, and the copy includes the working tree" >&2
fi

copied=()
shopt -s nullglob
for dir in "$source_real"/*/; do
  name="$(basename "$dir")"
  if [[ ! "$name" =~ ^[a-z0-9]+(-[a-z0-9]+)*$ ]]; then
    echo "error: skill directory '$name' is not kebab-case" >&2
    exit 1
  fi
  rm -rf "$dest_real/$name"
  cp -a "$dir" "$dest_real/$name"
  copied+=("$name")
done
shopt -u nullglob

if [[ ${#copied[@]} -eq 0 ]]; then
  echo "error: plugins/$plugin/skills has no skills" >&2
  exit 1
fi

commit="$(git -C "$root" rev-parse HEAD)"
tag="$(git -C "$root" describe --tags --exact-match 2>/dev/null || true)"
skills_blob="$(printf '%s\n' "${copied[@]}")"

PLUGIN="$plugin" \
  DEST="$dest_real" \
  COMMIT="$commit" \
  TAG="$tag" \
  SKILLS="$skills_blob" \
  SOURCE_URL="https://github.com/afonsoalrocha/skills" \
  python3 - <<'PY'
import json
import os
import re
import shutil
from pathlib import Path

dest = Path(os.environ["DEST"])
lock_path = dest / ".skills-lock.json"
plugin = os.environ["PLUGIN"]
skills = sorted(line for line in os.environ["SKILLS"].splitlines() if line)
tag = os.environ["TAG"] or None
kebab = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")

document = {"source": os.environ["SOURCE_URL"], "plugins": {}}
if lock_path.exists():
    try:
        current = json.loads(lock_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        raise SystemExit(f"error: {lock_path} is not valid JSON; refusing to overwrite")
    plugins = current.get("plugins") if isinstance(current, dict) else None
    if isinstance(plugins, dict):
        document["plugins"] = plugins

previous = document["plugins"].get(plugin, {})
previous_skills = previous.get("skills", []) if isinstance(previous, dict) else []
kept = set(skills)
if isinstance(previous_skills, list):
    for name in previous_skills:
        if not isinstance(name, str) or name in kept or kebab.fullmatch(name) is None:
            continue
        stale = dest / name
        if stale.is_symlink():
            stale.unlink()
        elif stale.is_dir():
            shutil.rmtree(stale)

document["plugins"][plugin] = {
    "commit": os.environ["COMMIT"],
    "tag": tag,
    "skills": skills,
}
lock_path.write_text(json.dumps(document, indent=2) + "\n", encoding="utf-8")
PY

echo "synced $plugin -> $dest_real"
