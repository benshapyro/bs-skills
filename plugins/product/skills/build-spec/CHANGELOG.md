# Changelog

History of changes to this skill, newest first. See the maintenance note in SKILL.md for how to keep this file current.

## v3.0 — 2026-11-23 23:20 PST

Five changes from a trial that gave the same four jobs to this skill and four other toolsets. Directed by Ben Shapiro.

Decision: add a required spec section instead of leaving it to judgment. Options: a line of advice in SKILL.md, or a section the ready check enforces. Reason: on the largest job, three of five builds left an existing safety check pointed at the old data path, and advice alone gets skipped. The first number goes up because a spec written for v2.0 now fails the ready check until the section is added.

- New required section, **Rules that must still hold**: each check that works today and that the change could route around, the new path it must cover, and a test through the whole run. The ready check wants a filled row or "None found:" with what was searched. Four new test cases, each seen failing before the checker changed.
- The closing conversation asks which existing checks the change could route around, after looking in the code.
- A third pre-handover step for specs that change existing behavior: a bypass reader with one question.
- Two default agent rules in the template: write each piece's check before its code (it must still be seen failing against working code), and on a fix run reproduce the fault and name its cause first.
- The start command ends by listing every requirement that is not built, and the review compares requirements with the diff. In the trial no build said what it had left out.

## v2.0 — 2026-11-10 23:55 PST

Rewritten from scratch by an agent that never saw any earlier version, working only from a plain description of what the skill must do. Directed by Ben Shapiro.

Decision: rebuild instead of editing. Options: keep v1.1, or edit it. Reason: v1.1 was edited down from skills written at a former employer, so its text and design carried over; a rebuild makes the skill fully Ben's own.

- Shares no wording with any earlier version (0% of 8-word runs), and an independent comparison rated it clean against the former employer's copies.
- Tested blind on 12 invented scenarios against v1.1, the older launch-prep and no skill: 4.44 out of 5, against 4.27, 4.02 and 3.54. Replies are about 27% shorter than v1.1's.
- Smaller: five files and about 4,100 words, against about 9,800 in v1.1's 13 files. The readiness checker is now `scripts/ready_check.py`; it reads the actual start command and requires a cap the tool enforces.
- Known gaps: less help making checks pass-or-fail when output varies; the hand-over reply doesn't gather the assumptions it made into one list; no screen-states checklist; no pointer to code review before merge.
