# Changelog

## 4.1 — 2026-11-25

Handovers are exempt from the `status` and `parent` labels and use the handover skill's header instead, since they're never edited. The weekly review of 2026-11-23 found the two skills disagreed (15 of 16 new notes had no labels). Approved by Ben (25 Nov 2026).

## 4.0 — 2026-11-23

Decision records gain a `proposed` status that only the decision's owner moves to `active`, dated amendments added at the end (a reversal, or a fourth amendment, is a new record), an index once there are more than five, and a pointer from AGENTS.md; a project that already keeps records in a folder such as `docs/adr/` keeps it. The template starts at `proposed`, records who approved it, and shows an amendment. Records are written for a reader a year later and kept to about one screen, with research and results linked rather than included (Tycho's longest records had grown to 150-175 lines by holding measurements and plans). Why: a review of the Tycho project's 19 decision records found the owner's approval step and add-only amendments were what made them safe for AI agents to build on, and "never edited" was not how they were kept. On Ben's request (23 Nov 2026).

## 3.0 — 2026-11-12

Turned the docs standard (version 2, 2026-11-09) into a skill in the learning-loop plugin, so agents in any project, tool or machine can load it when they file a document, instead of it sitting in one repository's folder. The two templates moved in as references. The rules themselves are unchanged. On Ben's request; the global handbook keeps its five short filing lines and now points here.
