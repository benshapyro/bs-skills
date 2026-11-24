# Review and readiness

Read once every section is drafted, or when asked to judge any PRD, including one written elsewhere.

## Independent reviewers

A solo owner has nobody to argue with; reviewers fill that gap. Each is a subagent given the PRD file and one brief, and nothing else: not the conversation, your notes or another reviewer's output, because a reviewer who has seen your reasoning tends to adopt it. Run them at the same time.

Briefs (all four for a standard PRD; 1 and 3 for a short one):

1. **Premortem.** A year from now this has failed. Tell the most likely story of why. Which causes are missing from the R list, or ranked too low?
2. **Evidence audit.** For each claim a decision rests on, is the tag as firm as the evidence behind it? Which big decision rests on a guess, or on what someone said rather than did? Which target lacks a starting point?
3. **Handover dry run.** Try to begin a build spec for the first piece. Note every point where you would have to stop and ask: where the data is, an H that takes judgment to pass, an unclear finish.
4. **Cost and harm.** Who pays, in money and hours, to keep this running, and does it repay that? Who could be hurt, misled or shut out, and what happens on the day it breaks?

Send each: "Read <path>. Review it as <brief>. Up to eight findings, worst first. For each: the exact words concerned in quotes (or 'missing:' and what), what is wrong, and a proposed fix. No praise, no summary."

## Sorting findings

Sort findings by the ID they touch; the kind of item decides who may change it:

- **S and H:** wording, tags and checks are yours if the meaning holds; what the product does is the owner's.
- **R:** a missing Type or Endangers link is yours; the Decision, its test and the ranking are the owner's.
- **Q:** the answer is the owner's; Answered by and Due are yours only if they already named who.
- **No ID** (scope, a missing risk or situation): the owner's.

Drop findings whose quote is not in the PRD or that it already settles. Log your fixes as one change-history entry naming the IDs; bring the owner's calls as options with your pick. Only those reach the reply.

**No subagents?** Work the briefs yourself, put "Self-reviewed: no independent reviewer" in the header, and tell the owner in one line.

## Lint

`python3 scripts/lint_prd.py <prd.md>` exits 0 when clean, or 1 with each problem and its line. It checks blanks, IDs, required fields, links and length, not quality. Fix what it finds; without Python, check the same by eye.

## Readiness

Confirm that:

- Every main-body passage earns its place (see `document.md`), passes the anchor test, and fits the stated size.
- The problem is told through a real, recent instance, with the workaround's cost, and it is plain how directly users were heard from.
- At least one S is handled badly, with what happens then.
- Each H gives the check's steps, the passing result and who runs it (or No checker yet, with a stand-in); a builder can find the data and knows what finished means.
- Signals give an early sign, a later outcome and a stop condition, with targets only beside measured starting points.
- Risks span all five types, are ranked, and each has a Decision verb and S or H links; the worst have a this-week test and one without users. The owner's view sits beside the ranking.
- Alternatives include keeping today's workaround; the build order lists the R and Q IDs each piece settles, with no estimates or dates.
- No guess lacks a Q item, and each Q says who answers and by when.

## Verdict

- **Go:** the PRD becomes build-spec's input. Build-spec treats an untagged requirement as unconfirmed, so tags matter.
- **Hold:** list each blocker by the ID it concerns and what clears it ("H2: name who counts no-shows"; "R2: Q1 answered, due 2026-11-20"). If someone outside must act, cite their Q item.

- **Stop:** the evidence says not to build this, or not now: the worst risk has no response the owner can afford, or today's workaround beats it against S and H. Say so in the first line of the reply, with the R item and what would reopen the question.

Write the verdict into the Status line. A Hold is advice: if the owner builds anyway, record that in the decision log and keep the blockers in the header.
