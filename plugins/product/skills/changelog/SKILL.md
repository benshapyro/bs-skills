---
name: changelog
description: Keeps the change history of a Claude skill (CHANGELOG.md, a major.minor header version, the standard maintenance section) or a codebase (Keep a Changelog, Semantic Versioning, release notes). Use for "note this in the changelog", "bump the version", "which version is this now", "start a changelog for this repo", "tag a release" or "draft release notes", and whenever a skill is created or edited, even if nobody mentions history. Also checks a folder of skills, moves an old-format history into this layout, trims a long one, or combines two skills' histories. Not for commit messages or the skill edit itself.
metadata:
  version: "4.0"
---

# Changelog

A history tells a later reader, without the code or the conversations, what changed, when and why. First say whether the target is a skill (a folder built around SKILL.md) or a codebase (an app, library or tool). A repository of skills is both: each skill gets a skill history, the repository a codebase one. If unclear, ask.

## Replies

- Say what changed, show what you wrote, ask what must be asked, stop. When the user will save or apply the result, show the whole file; for a long one, the new top down to the first unchanged entry, saying exactly where it goes. A small change gets a one-line entry, a minor bump and a short reply.
- Run the check but don't paste its output; name only problems the user must act on. When the job is a check, give a table of problems.
- Mention the maintenance section only if it is missing or out of date.
- Fix or flag the skill in front of you; never propose editing this changelog skill.
- While waiting on an answer, hold the whole change, version included, or mark the draft provisional.

## Writing an entry

Before writing, compare the latest recorded version with the header (codebase: the package file). If they differ, ask the user what happened before going on; don't fix it quietly.

If you can't point to where a fact came from (a version, a date, who asked, why), ask or leave it out.

**Skill.** Edit a copy in your working folder, because an installed skill can't be changed in place; say so at the start. Then package it as `<name>.skill` (skill-creator's packager, or a zip) to install over the old one.

New entries go first in CHANGELOG.md, in the style the file already uses. With no entries yet, lead with the reason, then the change, and end with who asked:

```markdown
## 1.4 — 2026-11-11 14:05 PST

Breaking: <what stops working>. To fix: <steps>.
<Reason>, so <what a user of the skill now notices> (rather than <alternative>, because <why>).
- <other edit>, because <reason>
On <person>'s request.
```

Write the Breaking line only if something breaks, and the "rather than" only if a later editor might reopen the choice. A typo fix is one line: "Step 3 read as optional because of a typo; fixed. On Dana's request." Related edits share one entry. The time orders same-day entries. The requester is a person, never Claude; if unknown, ask.

**Codebase.** Work the way the repository does (a branch, plus a pull request if that's the habit). Each line under `## [Unreleased]` names the change as a user would describe it and links the pull request or issue behind it; Keep a Changelog's group headings sort it. Leave out who made it. Test: would a user notice it after upgrading? "Reports can be exported as CSV" passes; "moved the tests" and "fixed a bug in an unshipped feature" don't.

**Both.** Newest at the top, plain words, and nothing that names who the owner works for or with, or their internal systems. Whatever breaks an existing setup goes first in its entry or release, with how to fix it.

## Keeping the version

The version lives in one place only: a skill's header, or a codebase's package file (package.json, pyproject.toml…).

**Skill: major.minor.** Will someone who already relies on the skill have to act differently, or get a different kind of result? Then it's major (2.3 → 3.0): a new step they must take, a revised standard maintenance text, a job added or dropped, output in a new shape. Everything else is minor (2.3 → 2.4). If you can't tell, pick minor and say so.

**Codebase: Semantic Versioning,** from what's under Unreleased: anything breaking → major; Added or Deprecated → minor; else patch. While the version starts with 0, breaking moves the middle number and anything else the last.

## Starting a history

**New skill:** version 1.0 in this file's header shape; CHANGELOG.md starting with `# Changelog`, the line "A record of every change to this skill, most recent first." and one entry saying what the skill does; and, as SKILL.md's last section, this file's maintenance section, word for word.

**Existing skill with no history:** keep the version it claims (1.0 if none). Every time, ask whether to rebuild earlier changes from past conversations (`references/operations.md`). If not, the first entry says: "Changes before this entry were not written down; this file is complete only from here on."

**Codebase:** `references/operations.md`.

## Releasing a codebase

Only when asked, following `references/operations.md`. Never tag or publish without the owner's separate, explicit yes.

## Checks and rewrites (confirm before starting)

Rewrites move or reword history; they never drop any.

**Check skills** (changes nothing): `python3 scripts/check_skills.py <skill-or-folder>` reports version problems, entry order and dates, and the maintenance section's edition. Then look yourself for stray text, and for a CHANGELOG.md longer than its SKILL.md (`wc -w`). Fix only what the user picks, then rerun and say what's left.

**Check a codebase:** list user-visible commits since the latest tag (`git log --oneline <tag>..HEAD`) missing from Unreleased; match `git tag` against release headings both ways; check each bottom link compares the previous tag with this one (Unreleased: latest tag with HEAD); compare the package file's version with the latest release.

**Rebuild, convert, shorten, merge, revise the standard text:** `references/operations.md`.

## Keeping this skill up to date

Each change gets a new entry at the top of CHANGELOG.md saying what changed, why, when and on whose say-so, and the `version` in the header moves to match. The first number goes up only when someone who already knows the skill would see it behave differently; every other change raises the second. Normal use never needs CHANGELOG.md. If that file has grown long, flag it, and shorten it only with permission.
