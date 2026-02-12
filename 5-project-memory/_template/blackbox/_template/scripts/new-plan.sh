#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=lib.sh
source "$SCRIPT_DIR/lib.sh"

if [[ $# -lt 1 ]]; then
  echo "Usage: $0 <goal/title...>" >&2
  exit 1
fi

goal="$*"
timestamp_dir="$(now_timestamp_dir)"
timestamp_human="$(now_timestamp_human)"

slug="$(slugify "$goal")"

dest=".blackbox/.plans/${timestamp_dir}_${slug}"
template_dir=".blackbox/.plans/_template"

if [[ -e "$dest" ]]; then
  echo "Plan already exists: $dest" >&2
  exit 1
fi

mkdir -p "$dest"

# Copy templates and remove .template extension
for template_file in "$template_dir"/*; do
  if [[ -f "$template_file" ]]; then
    filename="$(basename "$template_file")"
    dest_file="$dest/${filename%.template}"
    cp "$template_file" "$dest_file"
  fi
done

# Recursively copy subdirectories
find "$template_dir" -mindepth 1 -maxdepth 1 -type d | while read -r subdir; do
  subdirname="$(basename "$subdir")"
  dest_subdir="$dest/$subdirname"
  mkdir -p "$dest_subdir"

  find "$subdir" -type f | while read -r subfile; do
    relative_path="${subfile#$subdir/}"
    dest_file="$dest_subdir/${relative_path%.template}"
    mkdir -p "$(dirname "$dest_file")"
    cp "$subfile" "$dest_file"
  done
done

if [[ -f "$dest/README.md" ]]; then
  sed_inplace "s/<short title>/${goal//\//\\/}/g" "$dest/README.md"
  sed_inplace "s/<YYYY-MM-DD HH:MM>/${timestamp_human}/g" "$dest/README.md"
fi

# Seed status timestamp if present.
if [[ -f "$dest/status.md" ]]; then
  sed_inplace "s/<YYYY-MM-DD HH:MM>/${timestamp_human}/g" "$dest/status.md"
fi

echo "Created plan: $dest"
