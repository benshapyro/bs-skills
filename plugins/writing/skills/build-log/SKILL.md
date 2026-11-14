---
name: "build-log"
description: "Keeps a build log of lessons and insights learned while researching, designing, building and testing, in a Claude Doc. Use when asked to log a lesson, start, tidy or harvest a build log, or when a piece of work finishes and something worth telling happened, even if nobody says 'log'."
metadata:
  version: "1.0"
---

# Build log

Keeps one living log of what the work taught, so it can become posts, talks, demos and portfolio pieces later. It works at two speeds, like a field notebook and the write-up after the trip: **Capture** jots a lesson down on the spot, in the log itself; **Curate** later merges, promotes and summarizes.

The rule that matters most: a lesson is never only offered in a chat reply. It goes into the log's Inbox the moment it is captured, and the owner keeps or cuts it there.

## The bar

Would the owner tell it to a room of peers? A few lessons a week, not one per task.

Capture when:
- a measurement settled a decision or overturned a guess;
- a bug or result surprised everyone;
- the owner overruled Claude, or Claude caught itself carrying a stale assumption;
- the same fix worked across many cases, so a pattern showed up;
- a cheap check saved an expensive mistake;
- the owner points at something and says to log it.

Skip routine changes, what the docs or code already say, private details about other people, and anything secret. Never invent a number, link or date. A lesson with nothing measured yet goes in with Strength "Idea".

## When to run

- **Asked:** "log this", "add that to the build log", "anything here for the log?", a doc comment pointing at a passage, "start a build log", "tidy the log", "harvest".
- **A piece of work finishes:** a PR merges, an eval or test run reports, a research question is answered, a design or doc is signed off, a release ships. Look back over that piece and capture up to three candidates.
- **Mid-work:** a moment from the list above. Capture it then, in one line of the reply.

## Find the log (every job starts here)

1. Look for the log's link where the project keeps standing facts: project memory, the project instructions, or a `Build log: <link>` line in CLAUDE.md or AGENTS.md.
2. No link: ask once whether to start one (see Start). In a one-off chat, offer to keep the rows in the reply instead.
3. Read the log's current version before writing. The owner edits it too, and their edits win.

## Capture

1. Write the candidate in the entry format, with the real numbers and links from the work just done.
2. Search the log for the same point in other words. If it's there, add the new evidence to that row and raise its Depth. Don't add a second row.
3. If it's new, add it at the top of the Inbox with Status "Candidate" and its Source.
4. Say so in one line of the reply: "Added to the build log Inbox: *lesson*." For a deepened row: "Deepened in the build log: *lesson*."
5. If the log can't be reached, say so plainly and put the full rows in the reply as a ready-to-paste table, so nothing is lost silently.

**One writer per log.** In a project with several threads or workers, only the coordinator (or whoever the project names) writes to the log. Others put candidates in their report, one line of what happened plus the evidence, and the writer files them in the Inbox the same turn the report arrives.

## Curate

Run when asked, and suggest it once the Inbox holds about ten rows.

1. Go through the Inbox with the owner: keep, merge into an existing row, or cut. Kept rows move to Lessons. Don't cut without the owner's word.
2. Look for clusters: three or more lessons pointing the same way become a Framework row that names and links them.
3. Rebuild **At a glance** from the rows (never by hand on each write): lessons per theme and per depth, the date of this Curate, and the three strongest rows not yet used.
4. Update **Content ideas**: pieces the lessons could become, with the rows each draws on.
5. Report in a few lines: what moved, what merged, and the one or two rows ready to become content.

## Start

1. Create the log as a Claude Doc with the layout below. Title: "<Project> build log".
2. Save its link where the project keeps standing facts (project memory, project instructions, or CLAUDE.md / AGENTS.md), and tell the owner where.
3. Offer a Harvest (below).
4. Leave Themes empty. Propose themes after about ten lessons, from what the lessons actually cover.

## Harvest

A one-time read of the past, asked for first. Read conversations, commits, PRs, issues, design records and docs for candidates; merge near-duplicates before writing (expect several raw notes per lesson); add them to the Inbox in small batches; and record each source and what was read in **Sources read**, so nothing is read twice.

## Entry format

| Column | What goes in it | Filled by |
| --- | --- | --- |
| Date | The day it happened, like 11 Nov 2026 | Claude |
| Lesson | The point as one claim, under 15 words | Claude |
| Context | 3 to 5 sentences for someone who wasn't there: the situation, what happened with a number, why it matters | Claude |
| Evidence | Links to PRs, issues, docs, runs or conversations, added to as the idea grows | Claude |
| Kind | Lesson (one story) or Framework (a way of thinking built from several lessons, linking them) | Claude |
| Source | The thread, conversation or doc it came from | Claude |
| Theme | One of the log's own themes, blank until themes exist | Claude suggests, owner can change |
| Depth | Seed (one story and a number), Explored (several sources and numbers), Deep (enough for a full piece) | Claude |
| Strength | Strong (carries a piece alone), Supporting (true but well known: evidence inside a strong piece), Idea (nothing measured yet) | Claude suggests, owner decides |
| Angle | What it could become: a post, a demo, a talk, a portfolio piece | Claude |
| Used | "Not yet", or where it was used | Owner only |

Inbox rows also carry Status: Candidate. Write Context for a stranger: plain words, jargon explained, numbers with units.

## Log layout

1. **How this log works.** Three or four lines: what it's for, who writes, the bar, and that Used and Strength are the owner's.
2. **At a glance.** Rebuilt on each Curate.
3. **Inbox.** New candidates, newest first.
4. **Lessons.** Kept rows, newest first. Once a table passes about 25 rows, start a new one per month, which also keeps each write small.
5. **Frameworks.** Each with a short paragraph and links to its lessons.
6. **Themes.** Each with a short do and don't.
7. **Content ideas.** Piece, kind, built from, good for.
8. **Sources read.** What a Harvest covered.

## Where the log lives

| Setting | Where the link lives | Who writes |
| --- | --- | --- |
| A project with threads | Project memory plus one line in the project instructions | The coordinator; threads send candidates |
| A single repo | A `Build log:` line in CLAUDE.md or AGENTS.md | The session |
| A standalone chat with Claude Docs | The owner keeps the link; ask for it, or find "build log" in their artifacts | The chat |
| No Docs tools | Nowhere | Nobody: give ready-to-paste rows and say they weren't written |

One log per project. Don't mix projects in one log unless the owner asks.

## Rules

- Read before every write; never overwrite the owner's edits or their Used and Strength calls.
- Never invent evidence. Link the real source, or leave the row an Idea.
- Name no private people, clients or other users in a row; the log may become public content.
- Write a few rows per edit, not the whole log at once.

## Maintaining this skill (note v3)

CHANGELOG.md records this skill's history; don't read it during normal use. After any change, add an entry at its top (what changed, why, date and time, who directed it) and set the header `version` to match. Bump the first number only if a returning user would notice the skill works differently; otherwise bump the second. If CHANGELOG.md is getting long, say so, but don't condense it without asking.
