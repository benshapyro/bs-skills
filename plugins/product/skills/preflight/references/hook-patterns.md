# Hook patterns

Two worked hooks from the first run of this skill, made generic. They are examples to adapt to the repo's own language, paths and checks, not files to paste. Check the hook input format against the current Claude Code docs first.

Both were smoke-tested in this generic form in a scratch repo in November 2026, with the cases listed at the end.

## Wiring in `.claude/settings.json`

```json
{
  "permissions": {
    "defaultMode": "acceptEdits",
    "ask": ["Bash(git push:*)"],
    "deny": ["Read(./.env)", "Read(./.env.*)"]
  },
  "hooks": {
    "PreToolUse": [
      { "matcher": "Bash", "hooks": [{ "type": "command", "command": "node \"$CLAUDE_PROJECT_DIR\"/scripts/guard-bash.mjs" }] }
    ],
    "PostToolUse": [
      { "matcher": "Edit|Write|MultiEdit", "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/scripts/hook-check.sh" }] }
    ],
    "Stop": [
      { "hooks": [{ "type": "command", "command": "\"$CLAUDE_PROJECT_DIR\"/scripts/hook-check.sh" }] }
    ]
  }
}
```

Add the repo's own merge and deploy commands to `ask`, and its read-only and check commands to `allow`.

## Shell tripwire: `scripts/guard-bash.mjs`

Change the blocked commands to the ones this repo's rules forbid, and point `readList` at the list the existing Edit and Write lock already uses.

```js
#!/usr/bin/env node
// PreToolUse hook for the Bash tool: a tripwire for shell commands the project's rules forbid.
// Reads the tool input JSON on stdin. Exit 2 blocks the command and stderr is shown to the agent.
// Exit 0 lets the normal permission flow continue.
//
// This matches the text of the command, so it catches honest mistakes, not a determined
// workaround (a script file, bash -c, a renamed binary). The real limit is the sandbox.
import fs from 'node:fs';
import path from 'node:path';
import { pathToFileURL } from 'node:url';

const WRITE_RE = /(^|[\s;&|(])(sed\s+(-[A-Za-z]*i|--in-place)|perl\s+-[A-Za-z]*i|tee\b|mv\b|cp\b|rm\b|truncate\b|dd\b|git\s+(checkout|restore|rm|mv)\b)|>{1,2}/;

function readList(root, file) {
  try {
    return fs.readFileSync(path.join(root, file), 'utf8').split('\n').map((l) => l.trim()).filter((l) => l && !l.startsWith('#'));
  } catch {
    return [];
  }
}

/** Returns a block reason, or null when the command may proceed. Pure, so tests can import it. */
export function check(command, { protectedFiles = [] } = {}) {
  const c = String(command || '');
  if (/\bgh\s+pr\s+merge\b/.test(c)) return 'Blocked: merge through the project merge script, not gh pr merge.';
  for (const seg of c.split(/&&|\|\||;|\n/)) {
    if (!/\bgit\b[^|]*\bpush\b/.test(seg)) continue;
    if (/(^|\s)(--force|-f)(\s|$)/.test(seg) && !/--force-with-lease/.test(seg)) {
      return 'Blocked: git push --force. Use --force-with-lease on your own branch.';
    }
    if (/(^|[\s:+])(main|master)(\s|$)/.test(seg.replace(/^.*\bpush\b/, ''))) {
      return 'Blocked: git push to the default branch. Push a branch and open a pull request.';
    }
  }
  if (/\bgit\b[^|;&]*\bcommit\b[^|;&]*(--no-verify|\s-[A-Za-mo-z]*n[A-Za-z]*(\s|$))/.test(c)) {
    return 'Blocked: git commit --no-verify skips the commit checks. Fix the problem and commit normally.';
  }
  // Redirects that write nothing to the repo (2>&1, >/dev/null) are not writes.
  const w = c.replace(/\d*>&\d/g, ' ').replace(/[0-9&]*>{1,2}\s*\/dev\/null/g, ' ');
  if (WRITE_RE.test(w)) {
    const p = protectedFiles.find((f) => c.includes(f));
    if (p) return `Blocked: this command writes near ${p}, a protected file. Use the Edit tool so the change is checked.`;
  }
  return null;
}

function main() {
  let input = {};
  try {
    input = JSON.parse(fs.readFileSync(0, 'utf8'));
  } catch {
    process.exit(0);
  }
  const command = input?.tool_input?.command;
  if (!command) process.exit(0);
  const root = process.env.CLAUDE_PROJECT_DIR || process.cwd();
  // One list: the same file the Edit/Write lock reads.
  const reason = check(command, { protectedFiles: readList(root, 'scripts/protected-files.txt') });
  if (reason) {
    console.error(reason);
    process.exit(2);
  }
  process.exit(0);
}

if (import.meta.url === pathToFileURL(process.argv[1] || '').href) main();
```

## Check after each edit, and done-gate: `scripts/hook-check.sh`

One script serves both events. Set `CHECK` to the repo's own fast check and `SCOPE_RE` to the folders it applies to.

```bash
#!/usr/bin/env bash
# PostToolUse (Edit|Write): runs the project's fast check on the one file just edited.
# Stop: runs it on every changed or new file, so the agent cannot finish with a failure in place.
# Exit 2 with the findings on stderr. Exit 0 means nothing to report.
set -u
INPUT=$(cat)
ROOT="${CLAUDE_PROJECT_DIR:-$PWD}"
cd "$ROOT" || exit 0
CHECK="scripts/fast-check.sh"          # the project's own check: takes file paths, exits non-zero on a failure
SCOPE_RE='^(src|content|pages)/'       # the folders the check applies to
[ -x "$CHECK" ] || exit 0

field() { printf '%s' "$INPUT" | node -e 'let s="";process.stdin.on("data",d=>s+=d).on("end",()=>{try{const j=JSON.parse(s);const v=process.argv[1].split(".").reduce((o,k)=>o&&o[k],j);process.stdout.write(v==null?"":String(v))}catch{}})' "$1"; }

if [ "$(field hook_event_name)" = "Stop" ]; then
  # Already continued once because of this hook: let the agent stop and report instead of looping.
  [ "$(field stop_hook_active)" = "true" ] && exit 0
  FILES=$( { git diff --name-only HEAD 2>/dev/null; git ls-files --others --exclude-standard 2>/dev/null; } | sort -u | grep -E "$SCOPE_RE")
else
  FILE=$(field tool_input.file_path)
  [ -z "$FILE" ] && exit 0
  REAL_ROOT=$(pwd -P)
  FILES=$(printf '%s\n' "${FILE#"$REAL_ROOT"/}" | grep -E "$SCOPE_RE")
fi
[ -z "$FILES" ] && exit 0

OUT=$(printf '%s\n' "$FILES" | tr '\n' '\0' | xargs -0 "$CHECK" 2>&1)
if [ $? -ne 0 ]; then
  { echo "Check failed. Fix these before finishing:"; printf '%s\n' "$OUT" | tail -25; } >&2
  exit 2
fi
exit 0
```

## Cases to pin as tests

Write these in the repo's own test runner, driving the real hook process with JSON on stdin.

Tripwire, must block (exit 2):

- `gh pr merge 3`
- `git push origin main` and `git push origin HEAD:main`
- `git push -f origin x` and `git push --force origin x`
- `git commit -nm x` and `git commit -m x --no-verify`
- `echo a > <protected file>` and `sed -i s/a/b/ <protected file>`

Tripwire, must pass (exit 0). These matter as much as the blocked ones:

- `git push -u origin feat` and `git push --force-with-lease origin feat`
- `git commit -am fix` and `git commit -m "note on main branch"`
- `cat <protected file> 2>/dev/null` and `sed -n 1,20p <protected file>`
- `git log main -3` and `git fetch origin main && git diff main...HEAD`
- A build with output thrown away, followed by a read of a protected file
- Input that is not JSON

Check hook:

- PostToolUse on a failing file in scope: exit 2, findings on stderr
- PostToolUse on a clean file, and on a file out of scope: exit 0
- Stop with a failing new file: exit 2. After the fix: exit 0
- Stop with `stop_hook_active` true and a failing file: exit 0

## Known limits

- The tripwire reads text. A script file, `bash -c "..."`, or a variable holding the path gets past it.
- The write test is broad on purpose. A command that both writes somewhere harmless and mentions a protected path is blocked. That is the safe side to err on, and why the message tells the agent to use the Edit tool.
- The done-gate only sees files git reports as changed or new. A check that depends on the whole project (a type check, a build) needs its own gate and a time budget.
