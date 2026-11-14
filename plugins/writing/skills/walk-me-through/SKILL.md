---
name: walk-me-through
description: Build an interactive HTML walkthrough that explains something dense one idea at a time, keeping the visual on screen and focusing the part being discussed. Covers diagrams and processes, charts, tables, documents, code walkthroughs (files or a change), and product tours from screenshots. Use for "walk me through", "explainer", "interactive slides", "explain how X works to the team", "walk through this code or PR", "tour of the product", even if "walkthrough" isn't said. Not for talks with no visual (use presentation-composer and slides) or tours that run inside a live product.
metadata:
  version: "1.0"
---

# Walkthrough

A walkthrough is a set of slides over one visual, or a few. Each slide makes one point. The visual stays on screen, and the part the slide is about is brought into focus while the rest fades. The reader always knows where to look.

Every slide points at something on a visual. That is the test for whether this skill fits.

Dense material fails because it shows everything at once. This fixes that by controlling attention, not by removing content.

## Decide first

Answer these before writing anything. They set the look and shape, so two walkthroughs should rarely come out alike.

- **Who reads it, and on what?** A team on laptops, a client on a phone, a room on a projector. This sets length, text size and how much each slide carries.
- **What is the visual?** A diagram, chart, image, table, prose, code files, or product screens. Prefer one. Use a few (files, screens) only when the subject is spread across them, and let each stay up for several slides. If the points don't live on any visual, this is the wrong skill.
- **Whose look is it?** Use, in order: the user's or organization's brand (check for a brand or design skill, a tokens file, or a stated palette), then colors and type that fit the subject, then the template's defaults as a last resort. Set them in the template's token block. Fonts are set in two places: the font link at the top and the font tokens.
- **What leads, the words or the visual?** `side: 'text-first'` is the default, because the headline is the point and the visual is the evidence. Use `'visual-first'` when the visual is the subject and the reader already knows the argument.

## How to build one

1. **Write the points.** List 8 to 14 sentences, one per slide, in the order a newcomer needs them. Each is a slide headline. If you can't state a slide as a sentence, it isn't a slide yet.
2. **Make the visual** that the points live on. Read the reference for its kind first:
   - `references/code.md` for code files or a change
   - `references/product-tour.md` for product screens
   - `references/visuals.md` for a chart, image, table or prose, and for using more than one visual
3. **Copy `assets/template.html`** and change its three marked sections: tokens, visual, content. Leave the engine alone. The template's comments are the reference for every field. The file is a page fragment for the Artifact tool, which adds the outer page.
4. **Look at it once** at laptop and phone width (the file opens directly in a browser), then publish it as an HTML artifact. Build in a folder of your own, so other work can't overwrite your files.

## What makes it work

- **The headline is the point.** "A second agent's only job is to cut", not "Review step". Keep it under about 14 words so it fits a phone. The body is one or two sentences.
- **The same visual, never a new picture per slide.** Seeing the same thing each time is how the reader builds the whole.
- **Connections get their own slides.** In a diagram, lines are what dense pictures lose. When a connection is the point, highlight it with `hot` and say what moves along it.
- **One real example per slide at most.** Use real items, quotes and numbers from the source, and say where they came from. A made-up example is labeled as made up, in its `verdict` line.
- **Color means one thing,** and so does line style. Usually color is who or what acts; solid and dashed can separate two flows over the same boxes. Name both in `kinds` and `lineKey`.
- **Say what is real.** Mark planned, untested or assumed parts with `status` and in the detail rows.
- **Open on text.** Use `layout: 'text'` for the first slide. End on the explore view so readers who want detail can get it.
- **Plain words.** Write for someone who was not in the room. Explain terms the reader may not know.

## Phones and other layouts

You don't design a separate phone version.

- **Focus is computed from `on`.** For a diagram, chart or image the engine zooms to the listed parts, fitted to the shape of the screen. For a table or text it scrolls to them. Set `view` by hand only when the automatic zoom is wrong.
- **Under 860px wide** the visual sits on top, the text below, and the buttons stay pinned at the bottom. Swiping changes slides.
- **A second visual** appears as a tab above the first. The engine switches when a slide moves to it.
- **Three layouts per slide:** `split` (default), `text` (no visual), `wide` (visual above the text).

What you control is the visual. Keep a diagram compact and roughly as tall as it is wide. List only the parts a slide is about in `on`. If a slide needs more than about five parts, split it. The exception is a slide about the whole: use `on: 'all'`, and let `hot` and `status` show where to look.

The explore view is added after your slides and does not count toward the 8 to 14.

## Checks before publishing

- Reading only the headlines in order tells the story.
- Every id in `on`, `focus`, `hot`, `status`, `details` and `path` exists as a `data-part`.
- The colors and fonts were chosen for this reader and subject, not left at the defaults by accident.
- Nothing overflows or is cut off, and the focused parts are readable at phone width.

## Keeping this skill up to date

Each change gets a new entry at the top of CHANGELOG.md saying what changed, why, when and on whose say-so, and the `version` in the header moves to match. The first number goes up only when someone who already knows the skill would see it behave differently; every other change raises the second. Normal use never needs CHANGELOG.md. If that file has grown long, flag it, and shorten it only with permission.
