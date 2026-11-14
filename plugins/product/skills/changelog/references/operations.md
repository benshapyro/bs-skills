# Less common jobs

Each changes many lines: show one finished piece first and wait for a yes.

## Rebuilding a skill's past

Only after a yes. Use only what past conversations show about edits to this skill; a gap stays a gap. Write one block at the bottom of CHANGELOG.md, without version numbers, so none are made up:

```markdown
## Earlier history (reconstructed, approximate)

Put together on 2026-11-11 from past conversations. Rely on the entries above, which start at 1.3; anything never discussed in a conversation is missing here.

- 2026-09-14: <reason>, so <what changed>. On <person>'s request (if shown). Source: conversation of 2026-09-14.
```

The check ignores everything from a `## Earlier history` heading down, so this block comes last.

## Converting a skill history

1. Rewrite each entry into this layout, changing layout only. A group label such as "Fixed" starts its line ("Fixed: …"). A missing time stays missing: date alone, plus "(time not recorded)".
2. Count entries before and after; the numbers must match, and every fact in an old entry must appear in its new one.
3. Run the check. If a version is stored in a second place, ask which copy to keep (usually the header) before deleting either.

## Shortening a skill history

Only when asked; otherwise just say it's getting long.

1. Offer to keep the full text: copy the file word for word to `history/full-changelog.md` and link it from CHANGELOG.md.
2. Entries since the last major version stay whole (or the latest ten, if fewer).
3. Older entries become one line each: version, date, what a user noticed, and on whose say-so. Breaking changes keep their repair steps.
4. Show word counts before and after, plus a sample, before writing.

## Merging two skills

One skill keeps its name and CHANGELOG.md; the other is folded in.

1. Below the survivor's own entries, and below any reconstructed block, add `## Earlier history of <other-skill>`, one line on when and why, then the other skill's full CHANGELOG.md with its text as found. The check skips it.
2. Record the merge as a new top entry, a major version, telling the other skill's users what they must now do.
3. Don't touch the other skill's folder; deleting or archiving it is the user's job.

## Revising the standard maintenance text

`EDITIONS` in `scripts/check_skills.py` lists every edition, oldest first; the last is the standard.

- **New edition:** append the wording to `EDITIONS` (never edit an old one), make it this SKILL.md's last section, and give this skill a major version. The check then names every skill on an older edition.
- **Moving a skill to it:** replace its section word for word. Its version stays: add an entry at the current version whose first line is "Version unchanged: maintenance text moved to edition <N>." (the check allows a repeated version only with that line).
- **Matches no edition:** show the difference. If changed on purpose, it is that skill's own rule, and the change was major there; if not, restore the standard text.

## Starting a codebase history

1. If the repository already keeps a changelog, by hand or generated (for example from conventional commits), keep to that and stop.
2. Otherwise create CHANGELOG.md in Keep a Changelog 1.1.0 layout:

```markdown
# Changelog

All notable changes to this project are listed here. The format follows Keep a Changelog, and the project uses Semantic Versioning.

## [Unreleased]

### Added
- Reports can be exported as CSV ([#42](https://github.com/OWNER/REPO/pull/42))

## [1.2.0] - 2026-10-03

### Fixed
- Dates show in the reader's own time zone ([#38](https://github.com/OWNER/REPO/issues/38))

[unreleased]: https://github.com/OWNER/REPO/compare/v1.2.0...HEAD
[1.2.0]: https://github.com/OWNER/REPO/compare/v1.1.0...v1.2.0
```

3. Read the commits since the latest tag (`git log <latest-tag>..HEAD`); whatever passes SKILL.md's "would a user notice?" test goes under Unreleased.
4. Wherever this repository already keeps rules for contributors and agents, add: "A pull request that changes anything users see also adds a line to the Unreleased part of CHANGELOG.md."
5. Optional, offered last: one short linked line for each earlier release (`git tag --sort=-v:refname`, the hosting site's release pages), from its tag message or release page. If declined, add under the intro: "Releases before <version> aren't described here; their tags still exist."

## Releasing a codebase

Work on a branch. No tag and no publishing until the owner says yes.

1. Apply SKILL.md's version rule to the Unreleased lines; name the line that set the bump.
2. Move those lines under `## [X.Y.Z] - YYYY-MM-DD` (today), leaving an empty `## [Unreleased]` above, with any breaking change first. In the same commit, set the version in the package file (package.json, pyproject.toml…) to X.Y.Z.
3. Fix the links: `[unreleased]` compares `vX.Y.Z...HEAD`; the new `[X.Y.Z]` compares the previous tag with `vX.Y.Z`. Use the repository's own tag prefix.
4. Draft release notes for someone deciding whether to upgrade. If anything breaks, open with "Before you upgrade": what breaks and the steps to fix it. Then one sentence on why this release matters, the changes they'll notice in plain words, and a link to the changelog section. Then read the commits since the previous tag and add any user-visible change the notes lack.
5. If a release script exists, offer to have it take its version and notes from CHANGELOG.md.
6. Show the owner the diff and notes; ask before tagging or publishing.
