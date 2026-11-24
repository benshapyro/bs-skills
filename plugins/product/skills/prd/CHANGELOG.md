# Changelog

History of changes to this skill, newest first. See the maintenance note in SKILL.md for how to keep this file current.

## v2.1 — 2026-11-23 14:20 PST

Saving now names the folder and top labels the filing skill uses, and says when a decision-log entry also needs a decision record, because the two skills described the same file in different words. On Ben's request.

## v2.0 — 2026-11-11 01:43 PST

Rewritten from scratch by an agent that never saw any earlier version, working only from a plain description of what the skill must do. Directed by Ben Shapiro.

Decision: rebuild instead of editing. Options: keep v1.1, or edit it. Reason: v1.1 was cut down from a skill written at a former employer, so its text and design carried over; a rebuild makes the skill fully Ben's own.

- Shares no wording with the former employer's version, and an independent comparison rated it clean.
- Tested blind on 12 invented scenarios against v1.1, the older agency version and no skill: 4.67 out of 5, against 4.27, 3.46 and 3.62. Replies are about 35% shorter than v1.1's.
- Five files and about 4,200 words, against seven files and about 5,000. Adds `scripts/lint_prd.py`, which checks that every guess has a question, every risk a decision and every hand-over condition a checker, and that each size stays under its word limit.
- Known gaps: on a PRD that is already solid it can pile on demands instead of saying it's ready; no way to record a risk nobody can test yet; no full worked example.
