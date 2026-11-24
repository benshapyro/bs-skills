# Changelog

History of changes to this skill, newest first. See the maintenance note in SKILL.md for how to keep this file current.

## v3.0 — 2026-11-23 23:20 PST

Five changes from a trial that gave the same product question to this skill and four other toolsets. Directed by Ben Shapiro.

Decision: make the interview a named step with a rule, instead of rewording the existing advice. Options: reword "ask a few questions per turn", or add a step that blocks drafting. Reason: the advice was already there and the trial run still drafted first and asked at the end. The first number goes up because a returning user now gets facts and questions before any draft.

- **Look before asking:** the first reply opens with facts found in the material within reach, each with its source, and counts what can be counted.
- **Interview:** no section is drafted until the owner has answered a round each on the problem, the people and the limits.
- The agreed piece is cut to the narrowest one that still carries the costliest risk.
- **In short:** up to six plain lines under the header, with no IDs, so an owner who reads only that can decide. The trial's PRD was the hardest of five write-ups to read.
- **Stop** joins Go and Hold as a verdict, for when the evidence says not to build.

## v2.0 — 2026-11-11 01:43 PST

Rewritten from scratch by an agent that never saw any earlier version, working only from a plain description of what the skill must do. Directed by Ben Shapiro.

Decision: rebuild instead of editing. Options: keep v1.1, or edit it. Reason: v1.1 was cut down from a skill written at a former employer, so its text and design carried over; a rebuild makes the skill fully Ben's own.

- Shares no wording with the former employer's version, and an independent comparison rated it clean.
- Tested blind on 12 invented scenarios against v1.1, the older agency version and no skill: 4.67 out of 5, against 4.27, 3.46 and 3.62. Replies are about 35% shorter than v1.1's.
- Five files and about 4,200 words, against seven files and about 5,000. Adds `scripts/lint_prd.py`, which checks that every guess has a question, every risk a decision and every hand-over condition a checker, and that each size stays under its word limit.
- Known gaps: on a PRD that is already solid it can pile on demands instead of saying it's ready; no way to record a risk nobody can test yet; no full worked example.
