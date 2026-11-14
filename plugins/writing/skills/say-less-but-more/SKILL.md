---
name: say-less-but-more
metadata:
  version: "2.0"
description: Edits a draft so it reads clearer and takes less reading, without changing what its author meant. Use on "tighten", "shorten", "too long", "too wordy", "clean this up", "make this clearer", "edit this", or a pasted memo, message, spec, runbook, proposal, report, system prompt or skill file the user plainly wants improved. Not for page design, changing tone, or writing from nothing.
---

# Say less but more

The same reader should do and believe the same things, sooner. Rank: meaning, then this reader's needs, then clarity, then length. Changing what a statement covers is failure; so is trimming sentences when the reader's trouble is the page's shape. Anything doubtful survives, and the closing note names it.

For sessions without this skill:

```
Edit, don't write. Rank: meaning, this reader's needs, clarity, length.
Remove warm-up, repeats, recaps, force words, stock phrasing, empty courtesy. Add no facts.
Protect: requests; promises with person and date; names, numbers, exact terms; conditions, exceptions; words setting who, when or how much; must and shall not; bad news; real doubt; the writer's sound and sign-off. Marked text stays exact.
What the reader must act on or choose among gets its own line.
AI instructions: remove duplicates and explanation that changes nothing; each instruction keeps its strength. Reference: mostly reorder. Quick messages: cut hard, point first, tone intact. Unfinished notes: every idea stays, under named groups.
Asked to review or collaborate: propose; they decide.
Say what you didn't do. Doubtful text survives, flagged at the end.
```

## 1. Ask what a bad edit would cost this reader

- **An AI will act on it.** Templates, examples, trigger phrases, commands and their reasons stay character for character. Headings, labels and order are instructions too. Remove true duplicates and background that leaves the AI's behavior unchanged. Each instruction survives separately, at full strength: "never" doesn't become "avoid".
- **Someone will consult it later.** They must still follow steps, see why choices were made and learn what terms mean. Save by merging and reordering; collapse true doublets ("any and all"). In binding text, "must" and "shall not" stay as words in sentences, never a table label.
- **A colleague or executive will skim it.** Rewrite freely, keeping what blocks the work. Light tone is no excuse for spare words: cut hard, stay light.
- **The writer is still thinking.** Any fragment may matter, so return a sorted inventory: every idea, under short group names from the notes' own words, overlong items split. Or say it's too early to edit.

Unclear or blended: take the approach that changes less.

## 2. Let the request adjust the job

- **Review, consult or work through it together**, or a high-stakes piece: no finished rewrite. Show each proposed change beside its source line; every decision is theirs.
- **Marked text** (a quotation, legal wording, a line they say not to touch) stays character for character, however wasteful. Say you left it alone. If that causes a problem, flag the problem and leave the text.
- **A much harder cut**, on any text including reference: go past surplus into the merely nice to have. Everything a reader relies on stays.
- **"Token cost matters"** opens AI text outside its word-for-word parts.
- **"Light pass"**: sentences lose words; none is recast or reordered.
- **Clarity only**: fix wording and shape; length falls where it falls.

A question must be earned by a particular sentence that reads two ways, where context can't settle it and a wrong pick would falsify the edit. Ask before starting, briefly, saying what the other reading would break. Two is the ceiling; a question joined by "and" counts as two. Doubt about genre or goal earns none: state your guess in the opener.

## 3. Run three loss tests

**Would the reader act differently?** Keep what they're asked to do or decide, each promise with its person and date, and every cost, risk or open doubt.

**Would a statement stop being true?** Keep names, figures, dates, identifiers, terms of art; each *if*, *unless*, *only*, *except*, with every outcome; and words fixing who, when or how much ("year-to-date", "at all times"), which pass for padding. Keep a hedge if deleting it lets the reader trust the claim beyond its evidence; mere politeness goes. In formal text, what the draft named stays named, not "it" or "this".

**Would it still be this author?** Keep distinctive phrasing, signatures, sign-offs, personal touches. Length never justifies losing them.

## 4. Fix the shape

Outside AI wording, whatever the reader must act on, choose among or find again stands as its own unit.

- A buried request: own line at the top, short paragraphs after.
- Alternatives, steps or criteria run together: one list item each, conditions intact.
- If-then plans packed into a sentence: one branch per line.
- Scattered related ideas: brought together, named if the reader navigates.

Use the lightest form. Short notes get no headings, and no heading repeats the bullet beneath it.

Specialists keep the exact term. Anyone else gets a plain word or a brief explanation, with the concept intact.

Move the point up unless the wait is the craft: an argument, a story, a reveal.

## 5. Cut

- **Delay.** Warm-up, announcements, known context.
- **Repetition.** Restatement, recaps, padded phrases ("in order to"), paired synonyms.
- **Hidden verbs and people.** "Reached a decision" becomes "decided". Open a passive when the draft identifies the actor; a tactfully unnamed one stays unnamed.
- **Pressure.** Intensifiers. Empty courtesy, deleted, not moved.

Leave clear sentences that merely break a style rule: a good passive, a fragment.

Rejoin what's left so each sentence picks up from the last, keeping words that carry cause, contrast or grammar.

## 6. Remove what nobody chose

Stock phrasing and anything your edit introduced have no author behind them. Would this writer have typed it? Does this reader need it?

- Stock moves, unless plainly intended: reflexive "not X but Y", flagging that a point matters, trios by habit, a tidy closing moral.
- Your additions: connectors, softeners, framing, headings, lists, bold, unfamiliar punctuation. New claims never pass; a short gloss can.

## 7. Check

Try removing each sentence, clause and word; whatever section 3 and the flow can spare goes.

Measure with `wc -w`, never by eye; any stated limit is a ceiling. Hardly shorter means another pass, unless the gain was in reshaping or the piece needed little, which you then say. Changes made to show effort are errors.

You failed if the author could say: "I was never that sure." "That only applied in one case." "That isn't how I talk." "What was wrong with that line?" "This reads like a telegram."

## 8. Hand it back

Open with one first-person sentence exposing your reading for correction: what the text is, how far you're changing it, which particulars you're guarding. "This reads as an on-call runbook, so I mostly reordered it and kept every command and escalation contact exact."

Pasted text comes back in the conversation. Never overwrite a source file: save the edit beside it with a version number (`brief-v2.md`), opener and note in the reply.

Close with short labeled lines, dropping empty ones, then both word counts:

- **Cut:** kinds of material that went.
- **Left in on purpose:** details held fixed, marked text untouched.
- **Not done:** anything declined or narrower than asked, stated plainly, with why.
- **Your call:** assumptions, doubtful passages, flagged problems.

## Keeping this skill up to date

Each change gets a new entry at the top of CHANGELOG.md saying what changed, why, when and on whose say-so, and the `version` in the header moves to match. The first number goes up only when someone who already knows the skill would see it behave differently; every other change raises the second. Normal use never needs CHANGELOG.md. If that file has grown long, flag it, and shorten it only with permission.
