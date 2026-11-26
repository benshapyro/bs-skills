#!/bin/bash
# Refuses a commit whose added lines name a client or include a home-folder path.
# Meant for shared and public repositories. Passwords and keys are caught separately
# by the global gitleaks hook.
#
# Client names are read fresh each run from the folder names in the clients folder
# (default ~/Projects/sharper; override with PRIVACY_CLIENTS_DIR), so no list is stored.
# A repository can also block its own extra names (colleagues, client team keys):
# set PRIVACY_NAMES_FILE to a file kept outside the repository, one name per line,
# lines starting with # ignored. If that variable is set but the file is missing,
# every commit is blocked, so a new machine can't skip the check by accident.
# Skip once, on purpose, with: SKIP_PRIVACY_CHECK=1 git commit ...
set -uo pipefail

[ "${SKIP_PRIVACY_CHECK:-}" = "1" ] && exit 0

names_file="${PRIVACY_NAMES_FILE:-}"
if [ -n "$names_file" ] && [ ! -r "$names_file" ]; then
  printf 'Commit blocked by the privacy check: its names list is missing (%s).\n' "$names_file" >&2
  printf 'Restore the list, or skip once on purpose with SKIP_PRIVACY_CHECK=1.\n' >&2
  exit 1
fi

clients_dir="${PRIVACY_CLIENTS_DIR:-$HOME/Projects/sharper}"
added="$(git diff --cached --no-color --unified=0 --diff-filter=ACMR | grep -E '^\+' | grep -vE '^\+\+\+ ')"
[ -z "$added" ] && exit 0

problems=""

# Home-folder paths: /Users/<name>/ (Mac), /home/<name>/ (Linux), or ~/ written out.
home_hits="$(printf '%s\n' "$added" | grep -nE '/Users/[A-Za-z0-9._-]+/|/home/[A-Za-z0-9._-]+/' | head -5)"
[ -n "$home_hits" ] && problems+=$'A home-folder path:\n'"$home_hits"$'\n'

# Client names: each folder name, also matched with its dashes or underscores as spaces or removed.
if [ -d "$clients_dir" ]; then
  for dir in "$clients_dir"/*/; do
    [ -d "$dir" ] || continue
    name="$(basename "$dir")"
    [ "${#name}" -lt 3 ] && continue
    spaced="${name//[-_]/ }"
    joined="${name//[-_]/}"
    pattern="$(printf '%s|%s|%s' "$name" "$spaced" "$joined" | sed 's/[.]/\\./g')"
    hits="$(printf '%s\n' "$added" | grep -inE "(^|[^A-Za-z0-9])($pattern)([^A-Za-z0-9]|$)" | head -3)"
    [ -n "$hits" ] && problems+="A client name ($name):"$'\n'"$hits"$'\n'
  done
fi

# Extra names from the repository's own list. Names aren't printed, only the line numbers.
if [ -n "$names_file" ]; then
  while IFS= read -r name || [ -n "$name" ]; do
    name="$(printf '%s' "$name" | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
    case "$name" in ''|'#'*) continue ;; esac
    [ "${#name}" -lt 3 ] && continue
    escaped="$(printf '%s' "$name" | sed 's/[][\.*^$()+?{}|/]/\\&/g')"
    lines="$(printf '%s\n' "$added" | grep -inE "(^|[^A-Za-z0-9])${escaped}([^A-Za-z0-9]|$)" | cut -d: -f1 | head -3 | tr '\n' ' ')"
    [ -n "$lines" ] && problems+="A name from the names list, in added line(s) $lines"$'\n'
  done < "$names_file"
fi

if [ -n "$problems" ]; then
  printf 'Commit blocked by the privacy check. Remove these and try again:\n%s' "$problems" >&2
  printf '(To skip once, on purpose: SKIP_PRIVACY_CHECK=1 git commit ...)\n' >&2
  exit 1
fi
exit 0
