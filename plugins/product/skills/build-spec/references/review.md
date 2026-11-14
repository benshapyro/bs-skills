# Reviewing a finished run

Answer one question: is the problem this run was for actually fixed? Gather your own evidence; the run's own account (last message, pull request text) is a claim to read last, noting where the record disagrees. Review, don't repair.

## The table

Work back from the goal: a row per real-world check (hands-on test included), then Done when, then each piece.

| Check | What you saw | Settles / leaves open | Ever failed? | Result |
|---|---|---|---|---|

- **What you saw:** output you reran, quoted; else a cited line from `run-log.jsonl`, the diff, git history or CI; for a row the person judges, their own words. Note what it never touched ("tests pass; nothing opened the real export screen").
- **Ever failed?** No, unless the spec recorded working code broken on purpose. If a break is cheap, make it now, watch the check fail, revert.
- **Rows the person judges:** send each alone, "Please [task]. It passes if [what to look for]. What happened?", and wait before the next. Never do the hands-on test for them.
- **Missing evidence:** mark "no evidence", name the file that would settle it, carry on.

Result: pass, fail, later (date and judge; offer a reminder), or no evidence.

Then scan the log and diff for choices the spec never covered (a new library, a skipped edge case, a file outside scope); the person accepts or rejects each that matters.

## The answer

**Fixed?** comes from the real-world rows: **yes** if every one judgeable now passes; **no** if any fails; **too early** if the deciding rows are dated later, and then say what is already shown and which row, judge and date settle the rest. Caveats, listed apart: checks that never failed, silent decisions, missing evidence, piece failures that don't change the answer.

## When a row fails

Say where the evidence points; that tells the person if the miss came from the build or the plan.

- **At a piece** (the spec asked for it; the diff doesn't do it): the build. Offer a fix run, naming its pieces, the checks it must pass and its cap as a number. Write it only after a yes, as a new spec, ready-checked.
- **At the spec** (a wrong fact, a silent spot, or all pieces pass and the "Why this run" problem remains): the plan. Draft edits to "Why this run", Facts to use or the real-world checks, ready-check them, and show the person the changed lines before any new code.
- **At the check** (it passed something bad): strengthen it and rerun before blaming either.

## Reply shape

Only what the person can act on; a long table goes in a file.

```
Fixed? yes / no / too early: one sentence why (too early: what's shown, what decides, when)
Misses: one line each, from the build or the plan
Caveats: ...
Needs your call: silent decisions, rows waiting on you
Next: e.g. "Want me to write a fix run for pieces 2 and 3, capped at 60 turns?"
```
