---
name: filing
description: Where a project's documents go and how they're named and kept, with templates. Use when creating, naming, moving, replacing or tidying any document in a project's docs/ folder (what's true now, a piece of work's PRD, spec or research, a decision record, a handover note), when starting a new project's docs, or when unsure where something belongs. Not for writing the content itself (PRDs, build specs and handover notes have their own skills) or for code comments and READMEs.
metadata:
  version: "4.1"
---

# Filing

How people and AI agents keep documents in every project, with any AI tool. Other skills point here instead of repeating it. If a skill and this page disagree, this page wins until one is fixed.

Templates with made-up examples: `references/decision-record.md` and `references/current-doc.md`. The handover note's template is in the handover skill; PRDs and build specs use their own skills' formats.

## Layout

Create a folder only when something goes in it. Add a new folder to this standard only after two real repos have needed it.

```text
docs/
  current/        what is true now, including how to run it
  work/<topic>/   one folder per piece of work
  decisions/      big, hard-to-reverse decisions
  handovers/      what happened, session by session
```

Instructions for agents stay in `AGENTS.md` at the repo root. Code comments and folder READMEs stay beside the code. Rough notes don't go in `docs/`.

## What goes where

| Thing | Home | Rule |
|---|---|---|
| A fact about the project, or steps to run it | `docs/current/<topic>.md` | Update it in the same change that makes it untrue |
| PRD | `docs/work/<topic>/PRD.md` | Why we're building it |
| Build spec and its files | `docs/work/<topic>/` | A second build on the same topic gets a subfolder named by date and topic |
| Research or images for that work | `docs/work/<topic>/` | Research that spans topics gets its own topic |
| A smaller decision | The PRD or build spec it belongs to | |
| A decision that's hard to reverse or affects many parts | `docs/decisions/<date-topic>.md` | See Decision records below |
| What happened in a session | `docs/handovers/<date-topic>.md` | Never edited. A new handover replaces it |
| A lesson | The handover's lessons section | Its fix goes in `AGENTS.md`, a skill, a hook, or `docs/current/` |

State each thing once and link to it elsewhere.

## Decision records

Write one when a choice is hard to undo or changes a promise people rely on: what data leaves their machine, a safety rule, a licence, a public name. A choice only one piece of work cares about goes in that work's PRD or build spec instead.

- Four short parts: the problem, the decision, the options turned down and why, and what it makes easier or harder. If it binds code, say how that's checked (a test, a lint, a review rule).
- Write for someone a year from now who wasn't there: full sentences, plain words, and the real event or number behind the choice. Keep it to about one screen. Longer usually means it holds research, results or a plan: put those in `docs/work/<topic>/` and link them.
- It starts as `proposed`. It becomes `active` only when the person who owns the decision approves the text itself, not just the idea; write who and when on the record. An agent never marks its own record active, and nothing built on it merges until then.
- Old text is never rewritten. A narrow change or addition is an amendment added at the end, headed with its date and topic, with its own status and approval. A reversal, or what would be a fourth amendment, is a new record that replaces the old one.
- Once there are more than five, keep `docs/decisions/README.md`: one line each with its status, updated in the same change.
- Point `AGENTS.md` at the records agents must follow, by link, rather than restating them.
- A project that already keeps records elsewhere (such as numbered files in `docs/adr/`) keeps that folder and its numbering; don't rename to match.

## Names

- Documents that happen once start with the date: `2026-11-09-refund-endpoint.md`. If the name is taken, add the time.
- Living documents use the topic only: `docs/current/architecture.md`.
- Use lowercase words with dashes. Fixed file names, such as `PRD.md`, keep their capitals.

## Top of each document

Everything except `docs/current/` and `docs/handovers/` starts with two labels. In a build spec folder, only the main spec needs them. A handover uses the handover skill's own header instead: it's never edited, so it has no status to change, and the note it replaces is named in its "Previous note" line.

```yaml
---
status: active
parent: docs/work/refunds/PRD.md
---
```

- `status` is `draft`, `active`, `done` or `replaced`. A decision record can also be `proposed`, waiting for its owner's approval.
- `parent` is the document this one came from, or `none`.

When a document is finished or replaced, set its status, add a one-line link to whatever replaced it, and leave it where it is.

## Keeping documents honest

- Label important claims **verified** (say how), **stated** (who and when), **inferred** (why) or **unknown**.
- A written status can be out of date. Check the code, tests or branch before relying on it.
- When documents disagree, trust running code and tests for what the system does, and the PRD for what it should do. Then fix the document that's wrong.
- Write diagrams as Mermaid text inside the document they explain.
- A link must still work in a fresh copy of the repo. Don't point to temporary folders or session files.

## Client and private work

- A client's material stays in that client's project.
- Each project is asked once whether handovers are committed. Git records the answer: tracked means committed, ignored through `.git/info/exclude` means private, and neither means ask.
- On a private project, a cloud session returns its handover in its final message.

## Keeping this skill up to date

Each change gets a new entry at the top of CHANGELOG.md saying what changed, why, when and on whose say-so, and the `version` in the header moves to match. The first number goes up only when someone who already knows the skill would see it behave differently; every other change raises the second. Normal use never needs CHANGELOG.md. If that file has grown long, flag it, and shorten it only with permission.
