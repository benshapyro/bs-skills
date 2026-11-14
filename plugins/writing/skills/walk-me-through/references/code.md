# Code walkthroughs

Use real code, copied exactly from the source. Never retype, tidy or shorten it without saying so. Say in the footer where it came from (repo, path, and version or commit).

## The pattern

One scene per file. Paste the file into `<pre class="code">`. The engine numbers the lines and colors them.

```html
<div class="sheet" data-scene="limit" data-label="p-limit/index.js">
  <pre class="code" data-lang="javascript">
…the file, HTML-escaped…
  </pre>
</div>
<div class="sheet" data-scene="queue" data-label="yocto-queue/index.js">
  <pre class="code" data-lang="javascript">…</pre>
</div>
```

- `data-lang` is the language name (javascript, typescript, python, go, rust, sql, bash, json and other common ones).
- `data-start="40"` numbers an excerpt from line 40, so slide line numbers match the real file.
- HTML-escape the code once (Python's `html.escape`, for example). Build the page with a script that reads the source file and escapes it; do not paste by hand. Then check that the page's code matches the source.
- The code colors come from tokens `k2` to `k5`, so set those even though there is no diagram. Leave `kinds` empty.

Slides point at lines:

```js
{ scene: 'limit', kicker: 'p-limit · lines 3–8', title: 'The limiter keeps one queue and one counter.', lines: [3, 8] },
{ kicker: 'p-limit · the loop', title: 'A finished task starts the next one.', lines: [[21, 26], [9, 16]] },   // same file: no scene needed
{ scene: 'queue', title: 'The queue is a linked list, so taking from the front is cheap.', lines: [20, 34] },
```

`lines` uses the numbers shown in the gutter. Set `scene` whenever the slide moves to another file.

## Walking through a change

Add `data-diff` and start each line with a space (unchanged), `+` (added) or `-` (removed). Added and removed lines are tinted.

```html
<div class="sheet" data-scene="fix" data-label="retry.py · the fix">
  <pre class="code" data-lang="python" data-diff data-start="12">
 def fetch(url):
-    return get(url)
+    return get(url, timeout=5)
  </pre>
</div>
```

## What makes a code walkthrough work

- **Follow one path through the code,** not the file from top to bottom. Start where a call comes in and follow it.
- **A slide covers 3 to 12 lines.** More than that and nothing is in focus. Split it.
- **The headline says what the lines do and why,** in words a newcomer to this code would understand. The body can name the function or variable to look at.
- **Three files at most.** Each file should stay up for several slides. If the story needs more, cut the story.
- **Use `explore: true`** in place of `details`, and set `exploreTitle` (for example "Read the files yourself"), so the last slide lets the reader browse the files.
- **One range per slide,** or two that sit next to each other. The view scrolls to span everything listed, so ranges far apart push one off screen.
- A phone shows about 10 to 15 lines, and long lines wrap. Keep ranges tight, and leave long comment blocks out of the range.
