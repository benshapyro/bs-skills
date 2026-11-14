# Spec: [[short name]]

<!-- scripts/ready_check.py reads the headings, "Field:" lines and table columns; keep them, fill every [[slot]]. Comments are ignored. Source each requirement: [src: file, link, or person + date] or [src: inferred, confirmed by <person>]. Outside comments, all-caps to-do words count as unfinished. Write a pipe in a table cell as \|. -->

<!-- Part 1. The target. -->

## Why this run
[[Who gets what, and the most recent real time the problem happened: date, what went wrong, what it cost.]] [src: [[...]]]

## Done when
```
[[one command that runs every check]]
```
Passes if: [[exact passing result]]
Seen failing: [[working code broken on purpose, what it printed, date]]

## Pieces
<!-- Thin slices in build order, each working end to end, each Check run on varied inputs. Full spec or chain: for each Check, write down the laziest code that would still pass it, then add an input that code gets wrong. Model-behavior work: piece 1 builds the example-case runner. -->
### 1. [[name]]
Gives: [[what a user can do once this is in]]
Check: [[command and expected result, judgeable with no context]]
Decided by: [[the script, or a named person plus written criteria]]
Seen failing: [[same; or: agent breaks it on purpose after it passes]]

## Real-world checks
<!-- Two to four. "Judge on": now, or a date after real use. Totals from a repeating job: compare with a figure the person already trusts. -->
| Check | Judged by | Judge on |
|---|---|---|
| [[check]] | [[person or script]] | [[now or 2026-12-01]] |

Hands-on test, with nobody helping:
Person: [[name and role]]
Task: [[the real job, start to finish]]
Judge on: [[now or a date]]

<!-- Part 2. For the agent. -->

## Baseline
`[[existing test command]]` passed [[N]] on [[date]]; the same must pass at the end. Existing tests change only with [[person]]'s approval.

## Facts to use
- [[A fact as a plain rule]] [src: [[...]]]

## Agent rules
| Rule | Enforced by |
|---|---|
| Report a failing check and stop; never weaken it or touch existing tests. | [[baseline in Done when + review]] |
| [[rule]] | [[deny rule / hook / test / prose only]] |

## Not in this run
- [[Something the agent must not attempt, even if it looks helpful]]

<!-- Part 3. For the person. -->

## Launch blockers
<!-- A row per command in Done when, Pieces and the start command: run at 3am with nobody awake, what would stop it? (A key on someone's laptop, a login wall, no test data, a screen the agent can't view.) Full spec or chain: also picture a failed night, ask why, add each likely cause. Keys come from a secret manager at run time. Proven: date and how, or "not yet, by <date>" (holds the launch). -->
| Command | Could stall on | Cleared by | Proven |
|---|---|---|---|
| [[command]] | [[blocker]] | [[person]] | [[2026-11-12: how it was shown to work]] |

## Settings to apply
[[Deny rules or hooks for the person to add before launch.]]

## Decision log
<!-- Small choices you settled yourself go here too. -->
| Question | Settled on | Settled by | Their first answer | Why |
|---|---|---|---|---|
| [[question]] | [[answer]] | [[person, or me]] | [[...]] | [[...]] |

## Still open
<!-- Only unknowns that would change what gets built, with who answers each. -->
- None

## Start command
<!-- The check parses this: claude -p, a tool-enforced cap, a permission mode, this file's path in the prompt, the full log saved. No double quotes inside the prompt. -->
```
claude -p --permission-mode auto --max-turns [[N]] --max-budget-usd [[USD]] --output-format stream-json --verbose "/goal
Read [[path to this file]] in full first. Done means its Done when command passes.
Build the pieces in order on branch [[name]], committing each once its check passes.
Run the baseline tests first and last. If [[cases where a person must step in]], stop and say why.
At the end, open a pull request and stop." > run-log.jsonl
```
