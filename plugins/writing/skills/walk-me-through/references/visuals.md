# Visuals other than a diagram

Each pattern replaces the `<svg>` in section 2 of the template. Slides use `on`, `focus` and `hot` exactly as they do for a diagram.

## More than one visual

A walkthrough can use a few visuals, called scenes: several files, several screens, or a diagram and then a table. Give each one `data-scene="id"` and `data-label="Name on its tab"` in place of `id="flow"`. Part ids must be unique across scenes. A slide's scene is worked out from its `on` or `focus`; set `scene` when a slide uses `on: 'all'` or `lines`. Keep it to a few scenes, and let each stay up for several slides.

## Chart

A chart is an svg like a diagram. Wrap each series, bar, axis and annotation in its own `<g data-part="...">`. Draw to scale from the real numbers. The engine zooms and dims as usual.

## Image with regions (photo, scanned page, mockup, screenshot)

Put the image in an svg and lay invisible rectangles over the regions you will talk about. The engine numbers the regions, shades everything outside the ones in `on`, and zooms to them. The full pattern, and how to capture screenshots, is in `product-tour.md`. You must be able to see the image to place regions. Never guess coordinates.

## Table

The stage scrolls to the row or cell in `focus` (or the first id in `on`) and fades the rest.

```html
<div class="sheet" id="flow" role="table" aria-label="What the table shows">
  <table>
    <thead><tr data-part="head"><th>Line</th><th class="num">Amount</th></tr></thead>
    <tbody>
      <tr data-part="revenue"><td>Revenue</td><td class="num">1,000</td></tr>
      <tr data-part="costs"><td>Costs</td><td class="num">(600)</td></tr>
    </tbody>
  </table>
</div>
```

- Put `data-part` on rows, or on single cells when one number is the point.
- Add the header row to `on` on most slides, so columns stay labeled.
- Add class `node`, `tabindex="0"` and `role="button"` to a row to make it clickable in the explore view.

## Prose (a contract, a policy, a letter)

One `data-part` per paragraph or clause.

```html
<div class="sheet" id="flow" aria-label="What the text is">
  <p data-part="c1">1. The supplier delivers within 30 days.</p>
  <p data-part="c2">2. Late delivery reduces the price by 2% per week.</p>
</div>
```

For code, read `code.md`.

## Notes for table and text

- Set `focus` on every slide. The stage scrolls to the first id in `focus`.
- A phone shows about five rows at a time, so keep each slide to a few neighboring rows.
- The explore view works with `details` alone. Leave out `items`, `kinds` and `lineKey` when there is no flow to trace.
- A row is clickable only if a slide has it first in `focus`. Leave `node` off rows with no slide of their own.
- Styles for your table or text go in section 1b of the template.
- There is no zoom. The stage is a scrolling box, so long content is fine.
- `status` and node colors (`data-kind`) apply to diagrams only.
- Keep rows and lines short enough to read at phone width.
