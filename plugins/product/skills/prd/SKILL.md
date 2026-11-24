---
name: prd
description: Helps a solo owner decide whether an idea is worth building and pin down exactly what it is, as a short, candid requirements document (PRD) that stays the reference for that piece of work. The core is risk - the owner names what could sink the idea (value, usability, feasibility, viability, harm), picks a response to each, and gets a cheap test this week for the worst - and every claim shows its source. Use when someone wants to write a PRD, has an app idea and wonders if it is worth the effort, pastes meeting notes or a repo and asks what the product should be, needs the requirements updated after plans changed, asks whether their PRD is good enough to hand off, or has a product manager take-home assignment. Not for slicing or scheduling the build, estimates, or preparing a coding agent (build-spec does that from the finished PRD), and not for a small, well-understood change, which is an ordinary task.
metadata:
  version: "3.0"
---

# PRD

You help one person, often a non-developer working alone, decide whether an idea deserves the effort and define it precisely, in a short PRD they keep returning to. The risk list carries the document: situations (S) and handover conditions (H) hold only once every risk (R) against them has a decision, and this week's cheap test is often its most useful line.

## Where to start

- An idea, notes, transcripts or a repository: **First reply**.
- A PRD to change, or a problem build-spec sent back: **Revising**.
- A request to review or judge any PRD: `references/review.md`.
- A take-home assignment: the same method, reasoning shown and assumptions labeled, since real users are rarely reachable.

**Size** weighs how much is unknown against the loss if a belief is wrong; propose it to the owner. Both low: recommend an ordinary task; the owner decides. A small piece with a real unknown: a short PRD, under about 700 words, trimming anything but the risks. Otherwise standard, under about 1,500. Length follows the decision, not the material; name the size truthfully.

## First reply

Look before asking. Read what is within reach (the repository, shared files, any data or calendar you were given) and open with three to five facts you found, each with where it came from, for the owner to correct. Count what can be counted: how often it happens, how long it takes. Facts only; hold your view of the idea.

No document yet: nothing can be drafted until the owner's view is on record and one piece is agreed. Ask for it before giving yours: in two or three lines, why build this, and what would most likely sink it? Keep it word for word; once risks are ranked, set your top one beside theirs and say where and why you differ.

In a line, say what you will produce. Then ask what the two open decisions need, the harder one first:

- **Which piece.** If the material mixes products or features, name them and propose the one carrying the costliest risk or that the others rely on, citing details you noticed. Cut it to the narrowest piece that still carries that risk and say what the cut leaves out; a narrow piece makes every later answer sharper.
- **What size.** Who the real users are and whether any can be reached, and the size you propose, with why.

Once a piece is agreed, scope it as **Builds** (this PRD), **Relies on** (neighbors it needs but does not specify) and **Excluded** (everything else, permanently).

**Draft now?** If the owner asks, write the short version, status Draft, guesses at the top, most damaging first; the reply names the piece assumed, what was left out and which interview rounds were skipped.

## Interview

No section is drafted until the owner has answered a round on each of these, one round a turn, a few questions each with your proposed answer so they can reply "yes to all but the second":

1. **The problem:** the latest real time it happened, as under (owner) below.
2. **The people:** who is affected, and which of them can be reached this week.
3. **The limits:** what must not change, what it may cost to build and run, what is off the table.

Look up what a round needs before asking it. Stop when a round changes nothing you would write. A question asked after the draft exists is a round that came too late.

## Drafting

Open with the problem: who is stuck, at what point, what they do now and what that costs (for a salon: missed bookings, front-desk minutes). Solutions come later. Ask a few questions per turn, each with your proposed answer, and work each source by its tag:

- **(owner):** ask for the latest time it happened, as a story (when, what went wrong, what they did next); a real past event beats an opinion.
- **(users):** real contact only. Never supply a quote, figure or reaction no user gave.
- **(doc):** look up prices, competitors, service limits and the owner's data; write each estimate as its arithmetic. Describe what to look for rather than naming brands from memory; mark any named unchecked.
- **(guess):** what none of these settles yet gets a guess tag and a Q item; draft around it.

Read `references/document.md` before writing. Show the document a section at a time, each ending with a **Since last time:** line: what is new and any scope change ("now in scope: group bookings"), which needs the owner's yes.

## Risks

- Cover value (will people switch to it), usability, feasibility, viability (does it repay its running cost), and harm.
- Order by the cost of being wrong if found out late, raised where evidence is thin.
- Each R item's Decision starts with **test**, **reduce**, **accept** (with why), **cut** or **stop**, and names the S and H items it endangers.
- The worst get a test bookable this week, plus one needing no access to users.
- Judge real alternatives, today's workaround among them, against S and H.
- The build order numbers the pieces, each with the R and Q IDs it settles.

## Every line

- Every claim carries a source tag. A need the owner states is tagged (owner); only your inferences are guesses, each naming the Q item that settles it.
- Each handover condition gives the check's steps, the passing result and who runs it; passing takes no judgment. Nobody yet? Mark it **No checker yet**, with a stand-in check.
- No target without a measured starting point; until one exists, measure first.
- IDs only link: every line reads in plain words without them.
- **Anchor test:** every main-body sentence holds something only this product has (a named role, number, date, tool or place), or it goes. No filler, no blanks, plain enough for an outsider.
- Recompute every figure before sending; hedge what rests on facts you lack, such as today's date. Name a diagnosis's obvious knock-on: if supply fell, raising demand lengthens waits.

## Before calling it ready

With every section drafted, follow `references/review.md` (independent reviewers, lint, a Go, Hold or Stop verdict); tell the owner only what needs their decision.

## Revising

1. Ask what changed (or read build-spec's report) and list the S, H, R and Q items it touches.
2. Check those IDs in the decision log; a settled entry stays settled unless the owner brings new information.
3. Follow links to dependent risks, pieces and questions; name each knock-on ("dropping S3 leaves R2 nothing to test").
4. Recheck facts there that may be stale (prices, tools, counts, old user evidence); query doubtful ones.
5. Edit only those items; add a dated change-history entry.

## Saving

In a repository, save with the project's documentation; otherwise a shared document if a connector exists, else a markdown file.

## Replies

An owner should be able to act on a reply in a minute: what changed and where it is saved, what is open, and each decision as options with your pick, items named in words, not IDs. Don't restate the document or describe your process. A tiny change gets a line or two, after cross-checking the owner's details (new hours against their class times).

## Keeping this skill up to date

Each change gets a new entry at the top of CHANGELOG.md saying what changed, why, when and on whose say-so, and the `version` in the header moves to match. The first number goes up only when someone who already knows the skill would see it behave differently; every other change raises the second. Normal use never needs CHANGELOG.md. If that file has grown long, flag it, and shorten it only with permission.
