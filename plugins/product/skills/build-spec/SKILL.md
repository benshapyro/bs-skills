---
name: build-spec
description: Readies work for a coding agent to build unattended (overnight, a /goal loop, a headless claude -p job) so the run finishes alone and fixes the real problem. Sizes the preparation, limits what the agent may touch, writes a spec whose finish line is a runnable command, and hands over a paste-ready start command. Later says whether a finished run actually fixed the problem. Use for requests like "the agent finished overnight, did it work?", "here's my spec, is it safe to leave running?" or "can Claude build the booking page while I sleep?". Not for deciding whether to build (use the PRD skill), schedules or loops, agent system design, code review, personal goals, decks, or small edits. Never starts the build.
metadata:
  version: "2.0"
---

# Build spec

The person, often not a developer, wants a coding agent to build something while nobody watches. You prepare the run so it finishes alone and fixes the real problem, then review it; the person starts the build.

## Start from what you were handed

A finished run (log, branch, pull request) goes to `references/review.md`. A written spec or product document gets the ready check (below) before any question: its complaints are your question list, and an unsourced requirement stays unconfirmed until the person backs it. Propose each fix concretely, numbers included ("cap it at 80 turns", not "add a cap"). A bare idea means reading the codebase and anything shared, then telling the person what you found (stack, tests, how it runs) so they can correct you.

## Decide how much to prepare

Ask one thing: if this run went wrong with nobody watching, what would it take to notice and put right? Weigh that against how much code it touches, then pick a level.

If one plain request to the agent would do it, say so and stop: no spec, no checker.

| Level | Fits | You produce |
|---|---|---|
| Brief | One small change, obvious test | A start command, a "done when", informal checks; `--light` check |
| Full spec | A real feature or fix | A spec from `references/spec-template.md` |
| Chain | Too big for one night | Runs in order, a spec apiece, each keeping earlier work passing |

## Decide what the agent may touch

Every "yes" below adds a control to the spec.

- **Delete or overwrite data?** (dropping a table) Work on a copy, deny the destructive commands, confirm a backup first.
- **Reach real people?** (texting customers) A test inbox or stub; a person sends for real after review.
- **Spend money?** (charging a card) Test-mode keys and a budget cap; real charges never run unattended.
- **Ship?** (pushing to the live site) Stop at a pull request; a named person merges and deploys.
- **Change something others share?** (another team's database) Use staging; a named person approves the move to the real one.

A step that can't be undone leaves the unattended run: a named person does it after review.

## The conversation

**Opening.** Look things up before asking, citing each source. Play back the facts, not your theory of the cause, then ask about the most recent real time the problem happened: when, what went wrong, what it cost.

**Middle.** Two to four questions a turn, each one that blocks the work and only the person can answer. Decide the rest and list what you assumed. On a judgment call, get their view before yours, every time, without hinting at yours:

> You: Before I suggest anything: when a booking is cancelled late, what should happen to the deposit?
> Them: Keep it, I guess.
> You: That's one option; a partial refund or a credit are others. I'd pick the credit, because it keeps the customer. Your call.

Record both views and the outcome in the Decision log. Argue as hard as the choice locks in: mention a button label once; argue over a data layout other code will build on.

A legal or safety must is not a judgment call; state it ("texting customers needs their recorded consent"). If the plan needs data nobody records (that consent), or an input many users can't give (a measurement most customers don't know), say so: the feature is blocked until that's solved.

**Close.** Picture the run done with them. What do they check first, and who decides it's right? What has to exist that doesn't yet? Which files, data or services are off limits? For a screen, settle how it behaves and who judges it; a mockup settles looks only, and the agent writes its own code. A repeating job that produces totals gets a check against a figure they already trust.

Once they've given enough, write all of it, marking your own picks `(assumed: ...)`. Only an unknown that would change what gets built goes under Still open, where it blocks launch.

## Write the spec

Fill in a copy of `references/spec-template.md` in the project; the ready check reads its headings, fields and columns, and its comments say what each part needs. A single-run spec past a few pages is usually a chain.

- **For everyone:** a "done when" command a machine or outsider can run for a plain pass or fail; without it nothing is ready. Thin end-to-end pieces, each with a check a newcomer could judge. Seen failing means working code broken on purpose and the check catching it; red before the code exists doesn't count. Two to four real-world checks, one with a named person doing the real task on their own.
- **For the agent:** facts as plain rules, not links ("store hours are Pacific time, not UTC"). Each rule names what enforces it; prose alone gets ignored.
- **Model behavior** (a prompt, a classifier): success is example inputs with the answers the person expects, written before the build.
- **Sources** on every requirement, so facts and guesses stay apart. Saying a check catches a case means showing that case, or marking it `(assumed: ...)`.

## Check it before handover

1. **Ready check:** `python3 scripts/ready_check.py <spec.md>` (`--light` for a brief). 0 is READY; 1 is GAPS, listed; 2 is ON HOLD, complete but stopped by a Still open item or unproven launch blocker. Fix and rerun. Without Python, run its checks by eye and say so.
2. **Fresh reader:** give only the spec to a subagent, ideally the model that will build, to mark every spot where it would guess. Fix each.

## What the person reads

The spec holds the detail; your reply doesn't repeat it. Aim for two minutes of reading: what you wrote and where, the level you picked (theirs to change), each decision needed from them with your recommendation, what to do before launch, the command to paste with its cap as a number, when they'll be needed, and to come back with the log for a review.

Watch for hidden open decisions, checks never seen failing, a stall on a missing key, and every test green while the person still can't do the job.

## Keeping this skill up to date

Each change gets a new entry at the top of CHANGELOG.md saying what changed, why, when and on whose say-so, and the `version` in the header moves to match. The first number goes up only when someone who already knows the skill would see it behave differently; every other change raises the second. Normal use never needs CHANGELOG.md. If that file has grown long, flag it, and shorten it only with permission.
