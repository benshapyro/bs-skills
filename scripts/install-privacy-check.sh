#!/bin/bash
# Turns the privacy check on for one repository:
#   ./scripts/install-privacy-check.sh [repo-folder] [names-file]
# It becomes that repository's own pre-commit hook, shared by all its worktrees.
# A global hook that hands off to repository hooks (as in the owner's dotfiles) runs it
# before its own checks. The optional names file (kept outside the repository) adds
# names to block; see privacy-check.sh.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
repo="$(cd "${1:-.}" && git rev-parse --show-toplevel)"
names="${2:-}"
if [ -n "$names" ]; then
  names="$(cd "$(dirname "$names")" && pwd)/$(basename "$names")"
  case "$names" in "$repo"/*)
    if ! git -C "$repo" check-ignore -q "$names"; then
      echo "The names file must live outside the repository, or in a folder git ignores." >&2; exit 1
    fi ;;
  esac
fi
hooks_dir="$(cd "$repo" && cd "$(git rev-parse --git-common-dir)" && pwd)/hooks"
hook="$hooks_dir/pre-commit"
mkdir -p "$hooks_dir"
if [ -e "$hook" ] && ! grep -q privacy-check "$hook"; then
  echo "This repository already has its own pre-commit hook: $hook" >&2
  echo "Add a line that runs $here/privacy-check.sh to it by hand." >&2
  exit 1
fi
{
  printf '#!/bin/bash\n# Installed by learning-loop: blocks client names, listed names and home-folder paths.\n'
  [ -n "$names" ] && printf 'export PRIVACY_NAMES_FILE="%s"\n' "$names"
  printf '"%s/privacy-check.sh"\n' "$here"
} > "$hook"
chmod +x "$hook" "$here/privacy-check.sh"
echo "Privacy check on for $repo${names:+ (with names list $names)}"
