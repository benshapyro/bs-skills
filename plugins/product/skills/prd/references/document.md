# The PRD document

Read this before writing or restructuring a PRD.

**What earns a place in the main body:** if deleting a passage would change neither the build-or-not call nor what a builder needs to start, it leaves. Appendices hold only real material (interview notes, a calculation, a data sample), never an empty one. Word limits (short about 700, standard about 1,500) exclude the logs and appendices.

## Header

Title, then `Status:` Draft, Hold (blockers listed by ID) or Go · `Size:` short or standard · `Updated:` date. Then three scope lines: `Builds:`, `Relies on:` (neighbors it needs but does not specify) and `Excluded:` everything else, permanently. Add "Self-reviewed: no independent reviewer" when that applies.

## Parts

Any order that reads well. A short PRD may cut Signals, Alternatives and Build order to a line each, never the risks.

- **Problem.** Who is stuck and at what point, what they do now and what that costs (for a salon: missed bookings, front-desk minutes), told through the latest real instance.
- **Evidence.** How directly the affected people were heard from ("owner's experience only", "4 users interviewed, 2026-10"). What people did outweighs what they said they would like.
- **Owner's view.** Their words on why to build and what would sink it, then one line setting it beside the risk ranking.
- **Situations (S).** Concrete cases with expected behavior, including at least one the product handles badly and what happens then.
- **Handover conditions (H).** What must hold at handover, plus where the data lives, who controls access and what already exists, so a builder never has to ask.
- **Signals.** An early sign (weeks), a later outcome (months), and what would make the owner stop or rethink. Each with a measured starting point and target, or "starting point unknown: measure first".
- **Left out on purpose,** each with why.
- **Risks (R),** worst first.
- **Alternatives,** judged against S and H, always including keeping today's workaround.
- **Build order.** Numbered pieces, each with the R and Q IDs it settles.
- **Open questions (Q).**
- **Decision log** (date, decision, options, choice, why) and **change history** (date, what changed, why).

## Source tags

In parentheses after every claim, firmest first. Never firm a tag up because the sentence sounds sure.

- `(users, <when>, <how many>)`: heard from real users; the date is required.
- `(doc: <which, with link>)`: a document, data you examined, or your own research.
- `(owner)`: the owner said so; a need they state is a requirement.
- `(guess → Q3)`: unknown; points to the Q item that will settle it.

## Item formats

`scripts/lint_prd.py` reads these: a list entry starting with the bold ID at the left margin, details indented below.

- R: `Type:` one or more of value, usability, feasibility, viability, harm; `Endangers:` S or H IDs, each with a short name; `Decision:` starting with test, reduce, accept, cut or stop. A test also needs `This week:` and `Without users:`.
- H: `Check:` steps and passing result; `Checked by:` who runs it, or `No checker yet:` why, plus a `Stand-in:` check.
- Q: `Answered by:` and `Due:` as YYYY-MM-DD.

```markdown
- **S1** A regular client rebooks her monthly cut from her phone on a Sunday evening. (users, 2026-10, 3 of 4 interviewed)
  - Expected: she sees open slots for her usual stylist, picks one, and gets a text confirmation.
- **S2** A group of six wants a wedding-morning block. (owner)
  - Not handled well: online booking takes single slots only, so it shows the phone number instead.

- **H1** A booking made online appears on the salon's calendar within one minute. (owner)
  - Check: make a test booking and time it until it shows on the calendar.
  - Checked by: the owner, at the front desk
- **H2** No-shows on online bookings are no higher than on phone bookings. (owner)
  - Check: compare no-show counts for both channels over the first four weeks.
  - No checker yet: nobody records no-shows today. Stand-in: start a paper tally at the front desk now, to get a starting point.

- **R1** Regular clients keep phoning instead of booking online. (owner)
  - Type: value · Endangers: S1 (phone rebooking), H1 (calendar sync) · Cost if wrong: the main reason to build disappears.
  - Decision: test. This week: put a "book online" link to a simple request form on the salon's page and count requests against calls. Without users: read the last 50 online reviews for complaints about booking.
- **R2** Clients will not pay a deposit online. (guess → Q1)
  - Type: value, viability · Endangers: H2 (no-show rate)
  - Decision: reduce. Launch without deposits; revisit once no-shows are measured.

- **Q1** Would regular clients accept a small deposit to hold a slot?
  - Answered by: the owner, asking at checkout · Due: 2026-11-20
```
