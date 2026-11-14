# Note template

Copy the block below into `docs/handovers/YYYY-MM-DD-topic.md`. Delete lines that don't apply; write "unknown" for header facts you can't find. Keep it as short as the session was.

```markdown
# <Topic> — handover <YYYY-MM-DD HH:MM>

- Project / branch: <project> / <branch>
- Person: <name as they gave it, and role>
- Others mentioned: <name: role, one line each, or none>
- Tool: <Claude Code, Cowork, Codex, ...>
- Models: <main model; helper agents' models>
- Versions: handbook "Last changed" <date from the global agent instructions file>; skills/plugins <name version, ...>

## Next

State (each marked verified: how / stated: by whom / inferred: why / unknown):
- <claim> — verified: `<command>` <result>

First step: <one action>
Don't redo: <work already done and checked>
Read first: <relative paths>
Outside the project: <item: where it is (relative path, or machine/app), and why it stays there; or none>

AI next steps:
1. <step>

Person's next steps (paste in order; the AI does not run these). Next session: ask whether each is done.
1. `<command>`

## Why

- Changed: <what>
- Decided: <what and why, or link to the decision record>
- Tried and dropped: <what and why>

## What went wrong

Previous note: <accurate / wrong about X / missing / none>

- Corrections from the person: <...>
- Took more than one try / redone: <...>
- Worked well: <...>
- Cost more than it should: <...>

### Lesson: <short name>
- What happened:
- Lesson:
- Applies when / doesn't apply when:
- Caught by: <person / test / luck>
- Severity: <low / medium / serious / act now>
- Belongs in: <global instructions / a skill / a project file / an automatic block / unsure>
- Seen before: <relative link to earlier note, or none>
```

## Example (made up)

```markdown
# Booking page — handover 2026-11-12 17:40

- Project / branch: booking-site / feature/booking-page
- Person: Mina, the site owner
- Others mentioned: Raj: runs the staging server
- Tool: Claude Code
- Models: main model unknown; one helper agent, model unknown
- Versions: handbook "Last changed" 2026-11-01; skills: handover 1.0

## Next

State:
- Form validation is done and its tests pass — verified: `npm test -- booking` (14 passed)
- Staging deploy is not set up — stated: by Raj, via Mina
- Time-zone bug is in `src/lib/slots.ts` — inferred: only that file converts times

First step: write a failing test for a booking made at 23:30 local time.
Don't redo: form validation (finished and tested).
Read first: `src/lib/slots.ts`, `docs/decisions/0003-store-times-in-utc.md`
Outside the project: the client's real bookings export, `../exports/bookings-nov.csv` (private data, stays out of the repo)

AI next steps:
1. Fix the time-zone bug, then re-run `npm test -- booking`.

Person's next steps (paste in order; the AI does not run these):
1. `git push -u origin feature/booking-page`

## Why

- Changed: added validation to the booking form.
- Decided: store all times in UTC; see `docs/decisions/0003-store-times-in-utc.md`.
- Tried and dropped: a date-picker library; it failed the keyboard-access check.

## What went wrong

Previous note: wrong about one thing — it said all tests passed; two were skipped.

- Corrections from the person: wanted plain-language error messages, not field codes.
- Took more than one try: the slot test, written twice before it actually failed.

### Lesson: skipped tests read as passing
- What happened: the last note counted skipped tests as passed.
- Lesson: report passed, failed and skipped counts separately.
- Applies when / doesn't apply when: any test result in a note / not to build output.
- Caught by: a test run at the start of this session
- Severity: serious (quietly wrong)
- Belongs in: this skill
- Seen before: none
```
