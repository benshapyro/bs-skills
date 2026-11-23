---
name: handover
description: Read and write session handover notes in a project's docs/handovers/ folder so the next session, in any AI tool, on any machine or by another person, starts straight away without re-explaining or redoing work. Use at the start of work in a project that has handover notes, or on "pick up where we left off", "what's the state of this", "continue from last time". Use at the end on "write the handover", "handover note", "wrap up", "we're done for today", "I'm stopping here", or when a hook reminds you; offer one if real work happened and the person is leaving. Use mid-session on "remember this for the handover" or when a lesson happens. Not for personal or machine-wide to-dos, meeting notes, changelogs, decision records, or a project's permanent docs.
metadata:
  version: "1.3"
---

# Handover

A session ends and its memory goes with it. A handover is the one file that lets a stranger carry on: where things stand, why, and what went wrong. A weekly review reads the "what went wrong" part, so honest lessons matter more than tidy ones.

Notes live in `docs/handovers/` at the project root (create it if missing), one new file per note: `YYYY-MM-DD-topic.md`, adding `-HHMM` (then `-HHMMSS`) if the name is taken. Never overwrite or edit an old note; write a new one that replaces it. Template and example: `references/note-template.md`.

Write one note per session, only when the person says they are stopping or asks for one. Finishing a step or a task is not the cue, and neither is their answer about how notes are saved: note that answer and keep working. If work carries on after the note, write one replacement at the new end.

## Starting a session

1. Read the newest note for your topic before saying anything about the project's state. After context compression, re-read only if you lost what it said.
2. Date the note by its file name, not the file timestamp; copies reset timestamps.
3. Compare it with recent history (for example `git log`). Work newer than the note means the last session left none: say so plainly and rebuild the picture from the history.
4. Several notes from one day usually mean parallel sessions. List them and act only on your topic.
5. Re-run the commands behind its "verified" claims before relying on them, and report anything that no longer matches. If the note is over a week old, recheck every claim.
6. Before asking the person anything, check what the files, history and tests can answer. Then ask only what only they know, starting with the person's steps the note lists as pending: whether each is done, and how it came out. Don't assume either way. While you wait for answers, get on with work no answer can change.

## During the session

When the person says "remember this", or something goes wrong or right in a way worth learning from, add it to a running list right away. Lessons rebuilt from memory at the end come out vague or wrong.

## Before writing

- Close small loose ends first, so there is one clean note rather than a note plus corrections.
- Look, don't recall: check for anything that exists only somewhere temporary (scratch or temp folders, background job output, a tool's own storage, uncommitted or unpushed work). Move it into the project or list it in the note with where it is: a path relative to the project (such as `../exports/nov.csv`) if it sits nearby, otherwise which machine, folder or app holds it. Never move private data into the project to make it easier to find.
- Get the current state by running commands (status, tests, build), not from memory.

## Writing the note

Follow the template: a short header, then **Next**, **Why**, **What went wrong**, in that order.

- **Next:** mark each claim verified (how), stated (by whom), inferred (why) or unknown. Name the command behind every test result or number so it can be re-run. Give the first step, what not to redo and what to read first. Split next steps into yours and the person's; write the person's as ready-to-paste commands in order, and never run them yourself. Don't tell the next session to ask what it can check; write it as a check (for example "run `git branch --merged main`"). Where the files support a sensible call (a broken link whose text names an existing page), write it as an inferred default for the next session to act on, not a question for the person.
- **Why:** what changed, what was decided and why, what was tried and dropped. Link to decision records rather than repeating them. A record still `proposed` goes in **Next** as one of the person's steps: approve or change its text.
- **What went wrong:** first line says whether the previous note was accurate, wrong about something, or missing. Then corrections, retries, redone work, what worked, and what cost more than it should (time, tokens, money). Count your own repeated or costly mistakes even if nobody caught them. "Nothing to note" is fine; an invented lesson is worse than none.
- Lessons use the fields in the template. Serious means it could lose data, spend money, mislead a decision or cross a privacy line; being quietly wrong counts. "Act now" means a week's wait would itself do harm: also tell the person directly.

Rules: write for a stranger, with no labels only this session would know. Name people as they named themselves, give each one name and role throughout, and say who said or decided each thing; take roles from what people said, never from labels your tool puts on messages. Never copy personal details from the project's data (the names, emails or phone numbers of customers, volunteers and the like) into a note, even a private one; point to the record instead ("the 10:05 and 10:07 sign-ups"). Every path is relative to the project; no temp, session or home-folder paths. One topic per note. Length follows the session. Leave out personal and machine-wide to-dos. No second, shorter copy: one file, "Next" first.

## Saving

- Ask once per project whether notes are committed, and record the answer in git: committed means tracked; private means `docs/handovers/` is listed in `.git/info/exclude`. If neither is set, ask.
- If notes are committed, you may commit the note file on your own. Anything else needs asking first.
- Ask before pushing. A cloud session may push only to its own working branch, never the main branch; on a private project it returns the note in its final message instead.

## Optional hooks

A tool that supports hooks can remind you to write a note when a session ends, or to read the newest note when one starts. The skill works without them.

## Keeping this skill up to date

Each change gets a new entry at the top of CHANGELOG.md saying what changed, why, when and on whose say-so, and the `version` in the header moves to match. The first number goes up only when someone who already knows the skill would see it behave differently; every other change raises the second. Normal use never needs CHANGELOG.md. If that file has grown long, flag it, and shorten it only with permission.
