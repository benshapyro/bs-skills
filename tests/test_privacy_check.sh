#!/bin/bash
# Checks the privacy check without touching any real repository: ./tests/test_privacy_check.sh
set -u
here="$(cd "$(dirname "$0")/.." && pwd)"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/clients/acme-co" "$tmp/lists"
printf '# names to block\nZanzibar Quill\nteam-kx9\n' > "$tmp/lists/names.txt"
git init -q "$tmp/repo" && cd "$tmp/repo"
git -c user.name=t -c user.email=t@t commit -q --allow-empty -m init
export PRIVACY_CLIENTS_DIR="$tmp/clients"
"$here/scripts/install-privacy-check.sh" . "$tmp/lists/names.txt" >/dev/null
hook="$(git rev-parse --git-common-dir)/hooks/pre-commit"
fails=0
check() { # check <name> <block|pass> <text>
  printf '%s\n' "$3" > f.txt; git add f.txt
  out="$("$hook" 2>&1)"; code=$?
  if { [ "$2" = block ] && [ $code -ne 0 ]; } || { [ "$2" = pass ] && [ $code -eq 0 ]; }; then echo "ok    $1"; else echo "FAIL  $1"; fails=$((fails+1)); fi
  git reset -q f.txt
  LAST="$out"
}
check "clean text passes" pass "nothing private here"
check "client folder name blocked" block "met acme co today"
check "listed name blocked" block "spoke with Zanzibar Quill"
[[ "$LAST" != *Zanzibar* ]] && echo "ok    listed name not printed" || { echo "FAIL  listed name printed"; fails=$((fails+1)); }
check "listed key blocked" block "moved to TEAM-KX9"
home_sample="/Us""ers/someone/file"  # split so this file doesn't trip the check itself
check "home-folder path blocked" block "see $home_sample"
mv "$tmp/lists/names.txt" "$tmp/lists/gone.txt"
check "missing names list blocks" block "nothing private here"
mv "$tmp/lists/gone.txt" "$tmp/lists/names.txt"
git worktree add -q "$tmp/wt" -b wt 2>/dev/null && cd "$tmp/wt"
[ "$(git rev-parse --git-common-dir)/hooks/pre-commit" -ef "$hook" ] 2>/dev/null || [ -x "$(cd "$(git rev-parse --git-common-dir)" && pwd)/hooks/pre-commit" ]
check "worktree uses the same hook" block "spoke with Zanzibar Quill"
[ "$fails" -eq 0 ] && echo "All privacy checks passed." || { echo "$fails check(s) failed."; exit 1; }
