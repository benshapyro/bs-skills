#!/bin/bash
# Turns the privacy check on for one repository: ./scripts/install-privacy-check.sh [repo-folder]
# It becomes that repository's own pre-commit hook. A global hook that hands off to
# repository hooks (as in the owner's dotfiles) will run it before its own checks.
set -euo pipefail
here="$(cd "$(dirname "$0")" && pwd)"
repo="$(cd "${1:-.}" && git rev-parse --show-toplevel)"
hook="$repo/.git/hooks/pre-commit"
if [ -e "$hook" ] && ! grep -q privacy-check "$hook"; then
  echo "This repository already has its own pre-commit hook: $hook" >&2
  echo "Add a line that runs $here/privacy-check.sh to it by hand." >&2
  exit 1
fi
printf '#!/bin/bash\n# Installed by learning-loop: blocks client names and home-folder paths.\n"%s/privacy-check.sh"\n' "$here" > "$hook"
chmod +x "$hook" "$here/privacy-check.sh"
echo "Privacy check on for $repo"
