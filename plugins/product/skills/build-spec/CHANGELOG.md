# Changelog

History of changes to this skill, newest first. See the maintenance note in SKILL.md for how to keep this file current.

## v2.1 — 2026-11-23 14:20 PST

The spec's place in a repository is named (`docs/work/<topic>/`, beside its PRD), matching the filing skill. On Ben's request.

## v2.0 — 2026-11-10 23:55 PST

Rewritten from scratch by an agent that never saw any earlier version, working only from a plain description of what the skill must do. Directed by Ben Shapiro.

Decision: rebuild instead of editing. Options: keep v1.1, or edit it. Reason: v1.1 was edited down from skills written at a former employer, so its text and design carried over; a rebuild makes the skill fully Ben's own.

- Shares no wording with any earlier version (0% of 8-word runs), and an independent comparison rated it clean against the former employer's copies.
- Tested blind on 12 invented scenarios against v1.1, the older launch-prep and no skill: 4.44 out of 5, against 4.27, 4.02 and 3.54. Replies are about 27% shorter than v1.1's.
- Smaller: five files and about 4,100 words, against about 9,800 in v1.1's 13 files. The readiness checker is now `scripts/ready_check.py`; it reads the actual start command and requires a cap the tool enforces.
- Known gaps: less help making checks pass-or-fail when output varies; the hand-over reply doesn't gather the assumptions it made into one list; no screen-states checklist; no pointer to code review before merge.
