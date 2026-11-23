# Decision record template

**What it's for:** one big, hard-to-reverse decision, so a stranger can see what was chosen, what was turned down, and why. **Who reads it:** anyone about to undo or build on the decision. **Where it goes:** `docs/decisions/YYYY-MM-DD-topic.md`. It starts as `proposed` and becomes `active` when the decision's owner approves the text. Old text is never rewritten: a narrow change is a dated amendment added at the end, with its own approval (example below); a reversal is a new record, and the old one gets `status: replaced` and a link to the new one.

Copy the block below. Keep each part to a few lines.

```markdown
---
status: proposed
parent: none
---

# <Decision, as a short statement>

Date: YYYY-MM-DD · Decided by: <who> · Approved: <who, when, or "waiting">

## Problem
<What forced a choice, in two or three sentences.>

## Decision
<What was chosen.>

## Options turned down
- <Option>: <why not>

## What it changes
- Easier: <...>
- Harder: <...>
```

## Example (made up)

```markdown
---
status: active
parent: docs/work/booking-page/PRD.md
---

# Store all booking times in UTC

Date: 2026-11-12 · Decided by: the site owner

## Problem
Bookings made near midnight showed on the wrong day for customers in other time zones, and the database held a mix of local and UTC times.

## Decision
Every time is stored in UTC and converted to the customer's time zone only when shown.

## Options turned down
- Store local time plus a zone name: every report would need converting, and two old reports already got it wrong.
- Leave it and fix the display only: the mixed data would keep causing the same bug.

## What it changes
- Easier: reports, reminders and comparing times across zones.
- Harder: anyone reading the database directly sees UTC, not local time.
```

## Amendment example (made up)

Added at the end of the record above, months later:

```markdown
## Amendment, 2027-02-03: recurring bookings

*Status: active. The site owner approved this text on 2027-02-03.*

**Problem.** Weekly classes repeat at the same local time, which moves in UTC when clocks change.
**Decision.** A recurring booking also stores its zone name, and each repeat is worked out from local time. One-off bookings stay as they are.
**What it changes.** Harder: the reminder job must read the zone for repeats.
```
