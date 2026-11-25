# The video site

Step 7. A small static site is enough: an overview page with the lead video and the shorts, a shorts page, and
whatever product pages the series supports. `_kit/site/build_site.py <series> --posters` renders both video pages
from shared head, nav and footer, so a fix to a label or a lockup lands on every page at once. It is the source
series' own page, player and modal code, driven by `site.json`: the site's address and the ask's link, the nav, each
film's description, the shorts' order, each page's heading, lede and share text, the footer's disclosure, and the
poster times. It writes the posters and share image from the current films, `vercel.json` (videos revalidate on
every request, pages are never cached, nothing is indexed) and `robots.txt` when they are absent. A menu page or a
features page is written beside it, by hand or through design-craft, and joins the same `site_urls.py` check.

## 1. Pages

- **The overview page** leads with the overview player, then the shorts as a grid of thumbnails under one heading.
  Each short opens in a modal (§3), not on a page of its own. At 1440x900 and at 390 px wide, the lead player's top
  edge sits inside the first viewport and the headline runs to two lines at most.
- **The current round only.** Superseded rounds come off the site; kept "below", they read as working notes to a
  prospect. Before removing old files, `cmp` each against its delivery copy, `git rm` the posters, drop their names
  from the page sources, and keep every name in `published.txt` reachable or say it is gone.
- **Link labels say what they open.** The owner in the source run renamed "Watch the videos" to "Video overview".
- **Retire a page without breaking its links**: a `vercel.json` redirect and a forwarding page (meta refresh plus
  `location.replace`, keeping the hash), because a gate or a cached link can bypass the redirect.
- **A prospect's product page has a budget**: about 2,000 words, about ten sections, at most six nav links, one
  heading style, grids that fill their columns, and no split layout whose left column is a lone heading. The owner
  called a 6,313-word page "inanely complex to handover" and three of its layouts "terrible"; the rewrite was 1,959.

## 2. Players

- `preload="none" playsinline`, explicit width and height, the poster, an MP4 link as fallback, the play control at
  the bottom left so the poster's centre stays visible, and one shared `role="status"` region for load errors.
  Starting one player pauses the others. Test the failure path by breaking one `<source>`.
- **Voiced only, or a switch.** Publish the voiced cut alone when the owner says so (the source run ended there).
  Otherwise a switch swaps each player's `src` between the cuts and restores `currentTime`, which works because both
  share one picture; it needs range requests (206), so test with `npx serve@14.2.4`, not Python's `http.server`.
- Under each player, a "Read the voiceover" `<details>` built from `lines.json`, so the voiced cut has a text
  equivalent without captions in the picture.
- A scripted `play()` with sound is blocked without a real gesture: set `muted = true` for scripted plays, and test
  sound-on autoplay with a driver's real click.

## 3. The shorts modal

- A `<dialog>` opened with `showModal()`, `min(1120px, calc(100vw - 32px), calc((100vh - 250px) * 16 / 9 + 32px))`
  wide. The frame grows from the thumbnail's rect (a FLIP through the Web Animations API, 440 ms on
  `cubic-bezier(.2,.8,.2,1)`) and shrinks back on close when that thumbnail is on screen, otherwise fades. Under
  `prefers-reduced-motion`, no morph.
- The short autoplays. Previous and Next step through the set (out over 140 ms, in over 260 ms from 24 px to the
  side), disabled at the ends, and the arrow keys do the same. Focus the modal's wrapper (`tabindex="-1"`), not the
  video, or the arrows seek the video. Close on Escape (`cancel`) and on the backdrop, unload the video, and return
  focus to the thumbnail. Check a phone width: 358 x 489 px at 390.
- Thumbnails may carry a light blur and a play pill with the length: the owner asked for it, then for less (2 px and a
  0.08 overlay, down from 6 px and 0.18).

## 3b. An interactive demos page

When the series has a features page whose demos animate themselves, they share the films' scenario, evidence marks
and cursor. The rules the source run's owner settled:

- **The demo yields only to a press of its own controls**: a trusted `pointerdown`, or Enter or Space, on `button, a,
  input, textarea, select, [data-act]` inside that demo's frame. Never on hover, wheel, touch or an empty click: "when
  i hover over the first demo … the animation stops". Test with real driver input: hover, wheel, empty click and a
  button press should leave the cursor on, on, on and off.
- Always on, off under `prefers-reduced-motion`; no switch (the owner removed it). Start a tour when 35 % of its frame
  is in view (0.5 never fired for a frame below the fold).
- A tour is a list per demo: `['look', row]`, `['tap', '[data-act="…"]', {after: ms}]`, `['digits', '271836']`. The
  cursor is 26 px with a 40 px ring over 520 ms, glides in arcs timed by distance, types at a person's pace and holds
  before it sends, and rests on a row's icon, not over the words the row brings into focus. Rows not in focus sit at
  0.55 opacity with a 0.4 px blur.
- Tool lines narrate in the present tense; the evidence marks (`ev-ok` underline, `ev-bad` wave, `ev-src` tint) are the
  films' marks in one shared CSS source.
- When the owner asks for the product to be covered in full, take its record's "where each feature works" table as
  the list; otherwise list the uncovered rows in the report rather than building them.
- **Run every tour to its end** in a real browser before shipping: start a probe on `window.__probe`, poll for
  `window.__probeOut` every 30 s rather than awaiting it (a minutes-long eval times out), and require each tour's last
  card, its open panel and zero `window` errors. The source run found a tour that played a card that did not exist,
  and could never have finished.

## 4. Thumbnails, posters and the share image

- Posters come from the rendered file (`ffmpeg -ss <t> -i film.mp4 -frames:v 1 -vf scale=1280:-1 -c:v libwebp
  -quality 82 poster.webp`): sample the overview every 4-6 s and each short across its result, tile the candidates
  (`delivery.py sheet`), and pick. Never the headline frame and never a frame with half a caption. The source's
  defaults: the overview from the architecture (6.6 s), each short 0.5 s before its lockup bar.
- The share image is 1200 x 630 from the overview's poster frame: `scale=1200:-2,crop=1200:630:0:<(round(1200 x H/W)
  - 630)/2>`, which is 22 for 16:9. Its URL goes through the same versioning as every video (`build_site.py`'s `ver()`, or
  `site_urls.py version` for a page written by hand), never as a literal.
- **When the picture changes, regenerate every poster and the share image**, not only the ones you edited: after a
  switch to a real company all ten posters and the share image still showed the fictional one. When only a branded
  element changed, list which posters contain it and regenerate those plus the share image.

## 5. File names and caches

- **A published name never changes**, because someone may already have linked to it. Keep every shared name in
  `published.txt` (the video file names: `delivery.py check --published` fails when one disappears); posters and the
  share image keep their names too, and `site_urls.py check` sees them.
- **A republished file needs a new URL.** Every page reference carries `?v=` plus the first 10 hex digits of the
  file's SHA-1 (`site_urls.py version`). A corrected voice line kept playing the old reading for this reason, and
  looked like a voice bug.
- **Read the existing cache headers before the first republish.** The source run's `vercel.json` served `/films` with
  `private, max-age=86400`; set the video path to `public, max-age=0, must-revalidate`. An object store answers with
  its own: Vercel Blob sends `public, max-age=2592000` (30 days), so version every Blob URL or set the max-age at
  upload, and `curl -sI -H 'Range: bytes=0-1023'` must show 206 and the header you meant.
- After every page build, `site_urls.py check site --origin <the site's URL>`, over every page including hand-written
  ones: a hand-written menu page kept a stale poster hash after two republishes, and only this check saw it.

## 6. Copy

Write page copy, short descriptions and the ask through the brand's voice skill, in the brief's English.

- **Sweep for vendor apparatus before the owner has to.** The source run's owner removed, one note at a time: a hero
  row of tool, skill and view counts; "N of M requirements built" and test-run dates; per-section Copy text and
  Feedback buttons; Pilot and Later badges; a "which assistants" matrix; a build-status section; a catalogue whose
  examples came from another market; a risk-tier ladder; PRD references; items waiting on counsel. A prospect reads
  all of it as a vendor's working notes. "Confidential" in the footer of a public page belongs on the list too.
- One English variant, no switch. Convert shared source data at build time (word map, -ise to -ize, US date order)
  and grep the built page outside data blobs for the other variant's spellings, and for "film" in visible text for a
  US audience.
- Lint the brand voice over strings extracted from the demo JavaScript as well as the page HTML: a banned phrase sat
  in a JS string the page lint never saw.
- State hosting the way the audience cares about it ("in the client's own country"), and say in the report where it
  runs today, so the owner confirms what the prospect will be told.
- Each short's description says what the viewer sees done and carries any caveat the picture no longer shows; make
  the page build assert it (`brief-and-claims.md` §6). Keep the descriptions in one copy file the build reads by film
  title, failing on a missing one.
- Close the page on one ask, from `BRIEF.md`.

## 7. Access

- A site for named prospects can be public with `robots.txt` disallowing everything and `X-Robots-Tag: noindex`. A
  real company on a public page is the owner's call: ask (the source run's owner kept it public against a
  recommendation to gate it).
- A password gate blocks your own live checks: every live request answers 401. Verify locally before each deploy.
- Removing a gate: delete the middleware and its dependency, add a static `robots.txt`, `curl` every page and media
  file until all answer 200 (the first check after READY still answered 401), and sweep the copy for words from the
  gated period.

## 8. Review and deploy

1. Build the pages through `design-craft:design-craft` and `ux-craft:ux-craft`, and run `design-review:design-review`
   on the rendered pages before the first deploy and after any layout change. Review an animated page from a copy
   with its animation off and say so; attribute findings by diffing design-lint before and after the change
   (`git show HEAD:<page>`, then `comm`), and give the findings a served video site raises by design
   (`external-resource` on media, `default-font` when the brand font is Inter) a one-line disposition.
2. Measure what screenshots blur: every header row's items share one text baseline (`picture.md` §7, measured inside
   the text); the nav's `scrollWidth <= clientWidth` at 1440; the page's `scrollWidth` equals 390 at phone width. With
   agent-browser, pass `eval --stdin` an invoked async function, `(async () => {…})()`.
3. `site_urls.py check`. Exit 0 required.
4. Deploy when the user has authorized publishing this series. On Vercel, pin the CLI
   (`npx -y vercel@<version> deploy --prod --yes`), retry "temporarily throttled" after 90 s, and expect the alias to
   answer with the previous deployment for a few seconds after READY.
5. Confirm the live site serves the new files: range-fetch every page and media URL (206), compare each page's bytes
   or a `?v=` against the local build, and `curl -I` a republished video for `content-length` against the file.
