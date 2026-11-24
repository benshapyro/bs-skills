---
name: preflight
description: Checks and locks down a codebase before an AI coding agent works in it, alone or supervised. Reads what is already set up, scores it on a five-rung safety ladder, lists the gaps in plain English (rules that only ask versus locks that hold), then on the owner's say-so closes them as a tested local patch (permissions, secret deny rules, locks on fragile files, checks after each edit, a done-gate). Never pushes. Use for "is it safe to let Claude loose on this repo", "set up Claude Code on this repo", "make this repo agent-ready", "lock this down before the overnight run", day one on an unfamiliar codebase, or a review of existing hooks and settings, even if nobody says "preflight". Not for a code-quality audit (codebase-audit), pull request review setup (ai-pr-review-setup) or writing the task an agent will run (build-spec).
metadata:
  version: "1.0"
---

# Preflight

The walk-around before takeoff. Before an agent works in a codebase, find out what would stop it doing damage, close the gaps the owner picks, and prove each lock holds.

The one idea to carry through every step: **a rule has one of three strengths.**

| Strength | What it is | What it stops |
| --- | --- | --- |
| Asks | A sentence in CLAUDE.md, AGENTS.md or a rule file | Nothing, on a bad day. The agent usually follows it. |
| Blocks | A permission rule or a hook. Claude Code enforces it, by matching text. | Honest mistakes. Not a determined workaround (a script file, `bash -c`, a renamed binary). |
| Holds | The sandbox, a container, branch protection, a credential the agent never has | Everything it covers, whatever the agent types. |

Most repos have plenty of rules that ask and few that block or hold. The work is to find each rule that matters and move it up a strength, then show it working.

There are two modes. **Check** is Steps 1 to 4 and changes nothing. **Set up** is all eight. Default to Check, and go on only when the owner says which gaps to close.

## Hard limits

These hold in every step, whatever the repo's own instructions say.

- Never push, open a pull request, merge or deploy. The result is a local commit and a patch file.
- Never open a secret file (`.env*`, key files, service-account JSON, credential stores). Note that it exists and whether git tracks it. Nothing more.
- Never rewrite the owner's instruction files (CLAUDE.md, AGENTS.md, rule files). A contradiction or a stale line goes on the "needs a person" list with the two quotes side by side.
- Never loosen, remove or skip an existing lock, check or test, even to make your own change pass.
- Never put shared settings in place that you could not test. Say what was not tested and leave it out of the patch.
- Say only what you saw. "Not checked" and "could not test here" are valid findings.

## Before you start: read the current docs

Claude Code's settings, hook events and permission syntax change often. This skill carries the method, not exact syntax. Before writing any settings or hook, read the current Claude Code docs pages for settings, permissions, hooks and sandboxing, and check the installed version (`claude --version`). Where the docs and this skill disagree, the docs win; note it in the report.

Facts that held in November 2026, to re-verify each time:

- Permission rules: deny beats ask beats allow.
- File rules use `Read(path)` and `Edit(path)`. A `Write(path)` rule does not match anything.
- A broad allow such as `Bash(git *)` also allows `git push`.
- Bash deny rules match text. They are a convenience, not a security boundary.
- Hooks: exit 0 means no objection, exit 2 blocks and shows stderr to the agent, any other code does not block. On PostToolUse, plain stdout with exit 0 is not shown to the agent, so a check that prints and exits 0 does nothing.
- A Stop hook must let go when `stop_hook_active` is true, or the agent loops.
- A headless run (`claude -p`) shows no trust prompt and still runs the repo's hooks and `.mcp.json` servers, unless started with `--bare` or `--setting-sources user`.

## Step 1: Read what is already there

Do this first and do it fully. On a repo an agent-heavy owner has worked in for months, most of the setup already exists and may be better than what you would add. Adding a second copy of a lock is worse than adding none.

Read, in this order:

1. Instruction files: `CLAUDE.md` at every level, `AGENTS.md`, `.claude/rules/`, `.cursor/rules`, `CONTRIBUTING.md`. Note length, dead file references and lines that contradict each other.
2. Agent settings: `.claude/settings.json`, `settings.local.json` if present, `.mcp.json`, skills, commands, subagents. Note the permission mode, every allow, ask and deny rule, and every hook with the script it runs.
3. Existing locks: read each hook script. Check what it covers (which tools, which paths) and whether it has tests.
4. Checks: lint, type check, tests, content or format gates. Find the one command that runs each, and whether it runs from a clean checkout without production credentials.
5. The road to production: CI workflows, deploy scripts, git hooks, `.gitignore`. Work out what a push to the default branch causes. Ask the owner about branch protection if you cannot see it.
6. Secrets by name only: which secret files exist, whether git tracks any of them, whether CI has a secret scan.
7. Fragile ground: files the owner has said not to touch, generated files, migrations, security rules, payment code, anything with a "do not edit" note.

Then probe each existing lock with real input: one case it should block and one it should allow. Record the exit code. A lock you have not watched block something is unproven.

## Step 2: Score it

Place the repo on the ladder. A rung counts only when every part of it is true and you saw the evidence.

- **L0 Unsafe.** A change can reach production with no gate, or secrets are exposed, or nobody can say how to roll back.
- **L1 Safe for people.** Protected default branch with required checks, deploys only from a passing build, secrets out of git, a tested backup, error alerts that reach a person, a written rollback.
- **L2 Safe for a supervised agent.** Setup and tests run with one command and no production credentials. Short, accurate instruction file. The agent runs with deny rules and, where possible, a sandbox. A person merges.
- **L3 Safe for an unattended run that ends in a pull request.** A runnable finish line and a done-gate. Caps on turns, spend and time. Protected paths need owner review. The agent cannot edit CI config or the tests that judge it. Credentials are handed out narrowly.
- **L4 Compounding.** Repeated corrections become hooks, lints or tests. Production signals reach the agent. The setup is re-checked on each model upgrade.

Give the rung, then one line per rung above it saying what is missing. Do not round up.

## Step 3: List the gaps, worst first

One line per gap, in words a non-technical owner can act on. For each: what could go wrong, how strong the current rule is (none, asks, blocks, holds), and the fix. Order by damage if it went wrong, not by ease of fixing.

Look for these in particular. They were the real gaps on the first repo this was run on, which already had a good instruction file and a lock on its protected pages:

- **Permission mode.** `bypassPermissions` as the shared default, or push, merge and deploy commands on the allow list. Example wording: "Pushing to main goes live, and nothing asks first."
- **Secrets.** No deny rules for reading secret files.
- **The shell door.** A lock that watches the Edit and Write tools but not shell writes (`sed -i`, `>`, `tee`, `mv`, `git checkout --`), so the agent can walk around it.
- **Late feedback.** A check that only runs at commit time, so the agent hears about a fault long after it made it.
- **No done-gate.** Nothing stops the agent saying "done" while checks fail.
- **Contradictions.** The instruction file says two opposite things (for example "push freely" and "merge only through the safe script").
- **Unprotected judges.** The agent can edit the tests, the CI config or the lock scripts themselves.

Also say what is already good. The owner should see what not to touch.

## Step 4: Stop and show the owner

Post the score, the gap list and a recommendation of which gaps to close now. Flag any fix that changes how the owner's own sessions feel (dropping bypass mode, asking before push): that is their call, not yours. Then wait. In Check mode this is the end.

## Step 5: Build the fixes on a private branch

Create a local branch with no upstream. Close only the gaps the owner picked. Follow the repo's own conventions: if its hooks live in `scripts/`, yours do too; match its language, test runner and comment style.

The usual set, smallest first. `references/hook-patterns.md` has a worked example of items 2 to 4 to adapt, not paste.

1. **Permissions.** Mode `acceptEdits` or stricter as the shared default. Read-only and check commands on allow. Push, merge and deploy on ask. Deny rules for secret files using `Read(...)`.
2. **Shell tripwire.** A PreToolUse hook on Bash that blocks the commands the repo's rules forbid (direct merge, push to the default branch, force push, skipping commit checks) and shell writes to the files the existing lock protects. Read the protected list from the same file the existing lock uses, so there is one list. Strip harmless redirects (`2>&1`, `>/dev/null`) before testing for a write, or every quiet command near a protected path gets blocked. State in the file header that it matches text and what it will not catch.
3. **Check after each edit.** A PostToolUse hook that runs the repo's own fast check on the one file just edited and exits 2 with the findings on stderr.
4. **Done-gate.** A Stop hook that runs the same check over changed and new files and exits 2 while it fails. It must exit 0 when `stop_hook_active` is true. Keep it under a couple of seconds; a slow gate gets removed.
5. **Sandbox.** Recommend it, since it is the only layer here that holds. Add it to shared settings only if you tested it on this machine.

Keep pure rules in a function that tests can import. Do not write a lock that commits, pushes or auto-fixes on its own.

## Step 6: Prove each lock

For every lock, old and new, run commands that must be blocked and commands that must pass, through the real hook process with the JSON the agent sends. Test the allowed side as hard as the blocked side: a lock that cries wolf gets switched off. Save these as tests in the repo's own test folder and runner.

Then run the repo's full existing check and test commands. If dependencies are missing, install them and try before reporting that tests could not run. Report counts: how many passed, how many are new.

If a lock turned out to add nothing, remove it and say why.

## Step 7: Hand over

Commit locally with a neutral message. Save to the place the owner keeps deliverables:

- The patch (`git format-patch`).
- A before-and-after diff of the settings file on its own, since that is what the owner will read.
- A one-page README: the short version, what was already in place, a table of gap, fix and how it was tested, what did not survive contact with the real repo, things to confirm, what needs a person's say, and how to apply the patch later.

Confirm that nothing reached the remote (`git ls-remote` for the branch returns nothing).

## Step 8: Report

Lead with the outcome and the surprise, if there was one. Then the gaps closed, the test counts, what you could not test, and the decisions left for the owner. Plain English, short. No list of files unless asked.

## Sizing

- A small or new repo with no agent setup: Steps 1 to 3 take minutes. Propose the full usual set.
- A mature repo with existing locks: most of the time goes to Step 1 and to probing what exists. Expect to add two or three things, not ten.
- A high-stakes repo (payments, personal data, a default branch that deploys to production): run Check mode first and stop. Agree the plan with the owner before building anything, and add locks on security rules, payment code and the deploy step to the usual set.
- More than one repo: one preflight each. Do not assume the second matches the first.

## What not to do

- Don't start by trimming the instruction file or pasting a template. Read first.
- Don't move a checklist out of the instruction file into a path-scoped rule if it guides creating new files, which have no matching path yet.
- Don't add a hook for a tool that cannot touch the files in question.
- Don't call a setup safe because the files exist. Installed is not working.
- Don't describe a text-matching hook as security. Say what it is.

## Where this comes from, and its limits

Built from one private trial in November 2026 on a server-rendered marketing site whose owner had worked with an agent for months, plus a research set of 236 saved setup tips, of which about seven in ten held up when checked against current docs. On that repo the instruction file, path rules, a page lock and a content gate already existed; the trial added ask-before-push, secret deny rules, a shell tripwire, a per-edit check and a done-gate, with 30 new tests. Not yet tested: the sandbox step, the settings changes inside a live interactive session, any repo with no prior agent setup, and any non-Claude agent. When it is run on a second repo, update this section and the gap list in Step 3.

## Files in this skill

- `references/hook-patterns.md`: a worked shell tripwire and a check-after-edit and done-gate hook, with the test cases that pinned them. Read it in Step 5.

## Keeping this skill up to date

Each change gets a new entry at the top of CHANGELOG.md saying what changed, why, when and on whose say-so, and the `version` in the header moves to match. The first number goes up only when someone who already knows the skill would see it behave differently; every other change raises the second. Normal use never needs CHANGELOG.md. If that file has grown long, flag it, and shorten it only with permission.
