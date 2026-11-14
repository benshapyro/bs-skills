#!/bin/bash
# Checks the two hooks without running Claude: ./tests/test_hooks.sh
# The reminder must fire in one situation and stay silent in five others.
set -u
here="$(cd "$(dirname "$0")/.." && pwd)"
nudge="$here/plugins/learning-loop/hooks/handover_nudge.py"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/repo" "$tmp/data"; cd "$tmp/repo"
git init -q && echo a > a.txt && git add a.txt && git -c user.name=t -c user.email=t@t commit -q -m init
sleep 1
say() { printf '{"type":"user","message":{"role":"user","content":"%s"}}\n' "$1" > "$tmp/$2.jsonl"; }
run() { printf '{"session_id":"%s","transcript_path":"%s","cwd":"%s","stop_hook_active":%s}' "$1" "$tmp/$1.jsonl" "$tmp/repo" "${2:-false}" | CLAUDE_PLUGIN_DATA="$tmp/data" /usr/bin/python3 "$nudge"; }
fails=0
expect() { # expect <name> <block|silent> <output>
  if { [ "$2" = block ] && [[ "$3" == *'"decision": "block"'* ]]; } || { [ "$2" = silent ] && [ -z "$3" ]; }; then echo "ok    $1"; else echo "FAIL  $1"; fails=$((fails+1)); fi
}
echo b >> a.txt
say "Great, I'm stopping for the day." s1; expect "stopping, work done, no note" block "$(run s1)"
expect "same session a second time" silent "$(run s1)"
say "Now add the VAT column please." s2; expect "not stopping" silent "$(run s2)"
say "That's it for today, thanks." s3; expect "already continuing from a hook" silent "$(run s3 true)"
mkdir -p docs/handovers && echo n > docs/handovers/2026-01-01-x.md; expect "note written this session" silent "$(run s3)"
rm -rf docs
say "Now add the VAT column please." s5
printf '{"type":"user","isMeta":true,"message":{"role":"user","content":[{"type":"text","text":"Base directory for this skill... write the handover note"}]}}\n' >> "$tmp/s5.jsonl"
expect "skill text that mentions handover notes" silent "$(run s5)"
git checkout -q a.txt
say "ok I'm stopping here" s4; expect "no work done" silent "$(run s4)"
out="$(/usr/bin/python3 "$here/plugins/learning-loop/hooks/compact_keep.py" </dev/null)"
[[ "$out" == *"Do not write a handover note"* ]] && echo "ok    compaction instructions" || { echo "FAIL  compaction instructions"; fails=$((fails+1)); }
[ "$fails" -eq 0 ] && echo "All hook checks passed." || { echo "$fails check(s) failed."; exit 1; }
