# Product tours

A tour explains a product from screenshots: what each part of a screen is for, in the order a new user meets it. It is a page about the product. It does not run inside the product.

## Get real screenshots

Use real screenshots only. Never draw a screen and present it as the product.

1. **Capture them** if this session has a browser tool that can open the product. Otherwise ask the user for screenshots.
2. **Use one size for every screen,** about 1280 to 1440 wide for desktop products. For a product people use on phones, capture at phone size.
3. **Get region positions from the page, not by eye.** While capturing, ask the browser for each element's box and multiply by the screenshot's scale factor. If you only have image files, look at each image before placing regions, and check the result once.
4. **Capture the state you will talk about.** Click, scroll or fill in the page first, so the screenshot shows the product in use. Size the window so the screen fits without being cut off.

With Playwright, at scale 1 so one screenshot pixel is one viewBox unit:

```python
page = browser.new_page(viewport={"width": 1280, "height": 900}, device_scale_factor=1)
page.goto(url); page.click("#next")                      # get to the state you want
page.screenshot(path="inbox.png")
box = page.eval_on_selector("#search", "e => { const r = e.getBoundingClientRect(); return [r.x, r.y, r.width, r.height] }")
# pad each box by about 6px and clip it to the image
```
5. **Leave out private data.** Use a demo account or sample data, or ask before showing real names and numbers.

## The pattern

One scene per screen. Each region you will talk about is a clickable box over the image. The engine numbers the regions in order, shades everything outside the ones a slide lists, and zooms to them.

```html
<svg class="flow" data-scene="inbox" data-label="Inbox" viewBox="0 0 1440 900" preserveAspectRatio="xMidYMid meet" role="img" aria-label="The inbox screen">
  <image href="data:image/png;base64,…" x="0" y="0" width="1440" height="900"/>
  <g class="node" data-part="inbox-search" tabindex="0" role="button" aria-label="Search"><rect class="region" x="320" y="24" width="560" height="56" rx="6"/></g>
  <g class="node" data-part="inbox-filters" tabindex="0" role="button" aria-label="Filters"><rect class="region" x="0" y="96" width="240" height="704" rx="6"/></g>
</svg>
<svg class="flow" data-scene="detail" data-label="Message" viewBox="0 0 1440 900" …>…</svg>
```

- The viewBox is the image size in pixels, and regions use those pixels.
- Part ids must be unique across all screens, so prefix them with the screen.
- List the regions in the order the slides discuss them. They are numbered in that order.
- A region must be a `rect.region` inside a `g.node`, as shown. The numbers, shading and zoom all depend on it.
- `kinds` and `lineKey` are for diagrams. Leave them empty for a tour.
- Embed each image as a data URI. Keep the page under about 8 MB: use JPEG or a smaller capture if needed.
- `data-markers="off"` on the svg hides the numbers.

Slides list regions the same way as any other part:

```js
{ kicker: 'Inbox · 1', title: 'Search looks through every message, not only this folder.', on: ['inbox-search'], focus: ['inbox-search'] },
{ scene: 'detail', kicker: 'Message', title: 'Opening a message marks it read for the whole team.', on: 'all' },
```

## What makes a tour work

- **Follow one job the user wants done,** from first screen to result. A tour of every feature teaches nothing.
- **One region per slide, sometimes two.** The headline says what the user does there and what they get.
- **Show each screen whole once** (`on: 'all'`) when it first appears, so the reader has their bearings, then go region by region.
- **Four screens at most.** Each should stay up for several slides.
- **Add `details`** for the regions and leave `items` out, so the explore view works as a labeled map of each screen. It opens on the first screen, and the tabs switch screens.
- **Light regions that sit close together.** The zoom fits everything a slide lists, so two regions on opposite sides of the screen show the whole screen, small. Give far-apart regions their own slides.
- On a phone, wide regions get small. Prefer regions under half the screen's width, or capture at phone size.
