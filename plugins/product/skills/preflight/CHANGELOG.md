# Changelog

A record of every change to this skill, most recent first.

## v1.0 — 2026-11-24 09:25 PST

New skill. It checks a codebase before an AI coding agent works in it and, on the owner's say-so, closes the gaps as a tested local patch. Two modes: Check (read what exists, score it on a five-rung ladder, list gaps worst first, stop) and Set up (also build the fixes on a private branch, prove each lock, hand over a patch and a one-page before and after). It never pushes, never opens secret files and never rewrites the owner's instruction files.

Built from one private trial on a marketing site on 2026-11-18, where most of the usual setup already existed and the real gaps were the permission mode, the shell route around an existing file lock, feedback that arrived only at commit time, and no gate on "done". That is why Step 1 is "read what is already there". Includes a worked tripwire and check hook as a reference. Not yet run on a second repo; the sandbox step is untested. No test cases for the skill itself yet.
On Ben's request.
