# "True now" document template

**What it's for:** something that is true about the project today, such as how to run it, how it's built, or where its data comes from. **Who reads it:** a newcomer, human or AI, on their first day. **Where it goes:** `docs/current/<topic>.md`, named by topic only, no date. Update it in the same change that makes it untrue. It needs no `status` or `parent` labels.

Copy the block below. Delete sections that don't apply.

```markdown
# <Topic>

Last checked: YYYY-MM-DD, by <who>, by <how: ran it, read the code, ...>

## In one paragraph
<What this part is and why it exists.>

## How to run it
1. `<command>`: <what it does>

## How it fits together
<A short description, or a Mermaid diagram.>

## Gotchas
- <Thing that surprises people, and what to do about it>
```

## Example (made up)

```markdown
# Running the booking site locally

Last checked: 2026-11-12, by the site owner, by running every command below on a fresh copy.

## In one paragraph
The booking site is a small web app. Customers pick a time slot; the app stores it and emails a confirmation.

## How to run it
1. `npm install`: installs what the app needs.
2. `npm run dev`: starts it at http://localhost:3000.
3. `npm test`: runs the tests (about 40; all should pass).

## How it fits together
The page in `src/app/book/` calls `src/lib/slots.ts`, which reads and writes the bookings table. All times are stored in UTC; see `docs/decisions/2026-11-12-store-times-in-utc.md`.

## Gotchas
- Confirmation emails are only printed to the terminal locally; nothing is sent.
```
