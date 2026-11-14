# Changelog

A record of every change to this skill, most recent first.

## 1.0 — 2026-11-13

Built from the automatic PR review set up, tuned and tested on one of Ben's repos on 2026-11-12, so the method can be reused on any project. It carries the method and the tests rather than fixed settings, because the Claude GitHub Action changes often: read current docs, survey the project, tune what the installer left, add a diff-only review for later pushes, merge before testing, and prove it with a three-push planted-fault test. Includes the tested push-review instruction, planted faults by stack, the tuned workflows as an example with versions removed, a script that checks workflow files against the checklist, and three test cases. Dry-run on three unlike cases with and without the skill: every check passed with it, 63% without. A 20-query trigger test found no false triggers but only about one in three should-trigger queries fired, and five rounds of rewriting the description didn't improve that, so the original description was kept. Not yet run end to end on a second real repo.
On Ben's request.
