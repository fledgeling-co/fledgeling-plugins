# The video site

Step 7. A small static site is enough: a menu page, an overview page with the lead video and the shorts, and
whatever product pages the series supports. One build script renders every page from shared head, nav and footer,
so a fix to a label or a lockup lands on every page at once.

## 1. Pages

- **The overview page** leads with the overview player, then the shorts as a grid of thumbnails under one heading.
  Each short opens in a modal (§3), not on a page of its own, so a prospect moves through all of them without
  losing the page.
- **Link labels say what they open.** The owner in the source run renamed "Watch the videos" to "Video overview".
- Give the overview its own page with a way into the shorts, rather than one long gallery.

## 2. Players

- **Voiced only, or a switch.** Publish the voiced cut alone when the owner says so. Otherwise a switch swaps each
  player's `src` between the muted and voiced files and restores `currentTime`, which works because both cuts share
  one picture.
- Restoring the position needs a server that answers range requests with 206. Python's `http.server` answers 200
  and every switch restarts the video; test locally with `npx serve@14.2.4`.
- A scripted `play()` with sound is blocked without a real user gesture. Set `muted = true` before a scripted
  `play()`, and test sound-on autoplay with a real click from a browser driver, never `element.click()` in an eval.

## 3. The shorts modal

- A `<dialog>` opened with `showModal()`. The video frame grows from the thumbnail's rect to its own (translate
  plus scale through the Web Animations API, about 440 ms on `cubic-bezier(.2,.8,.2,1)`), and shrinks back to the
  thumbnail on close when that thumbnail is on screen, otherwise fades.
- The short autoplays on open. Previous and Next buttons step through the set, disabled at either end, and the
  arrow keys do the same.
- On open, move focus to the modal's wrapper (`tabindex="-1"`), not the video, or the arrow keys seek the video
  instead of stepping shorts. Close on Escape through the `cancel` event and on a press on the backdrop, pause and
  unload the video, and return focus to the thumbnail that opened it.
- Under `prefers-reduced-motion`, open and close without the morph.
- Check it on a phone width: the source run's modal measured 358 by 489 px at 390 px wide.

## 4. Thumbnails, posters and the share image

- Posters come from the rendered file (`ffmpeg -ss <t> -i film.mp4 -frames:v 1 -vf scale=1280:-1 -c:v libwebp
  -quality 82 poster.webp`), from a frame that is not the headline (`picture.md` §6).
- Thumbnails in a grid may be blurred lightly with a play button over them. The owner in the source run asked for
  this, then for less: 2 px of blur and a 0.08 navy overlay, down from 6 px and 0.18.
- The share image is 1200 by 630 from a current frame (`-vf "scale=1200:-2,crop=1200:630:0:<offset>"`). Remake
  it every round the picture changes. In the source run it still showed the first round's frame after the site
  had been rewritten three times.

## 5. File names and caches

- **A published name never changes**, because someone may already have linked to it. Keep every shared name in
  `published.txt`; `delivery.py check --published` fails when one disappears.
- **A republished file needs a new URL.** Every page reference carries `?v=` plus the first 10 hex digits of the
  file's SHA-1; `site_urls.py version` prints them for a build script. Without it, a browser or CDN that cached the
  old file serves it under the old name. In the source run a corrected voice line kept playing the old reading for
  exactly this reason, and looked like a voice bug.
- Serve the video folder with `Cache-Control: public, max-age=0, must-revalidate`, so even an unversioned request
  revalidates.
- After every page build, run `scripts/site_urls.py check site --origin <the site's URL>`. It fails on an
  unversioned media reference, a stale hash and a missing file, including references inside inline JSON and the
  share image's absolute URL.

## 6. Copy

Write page copy, short descriptions and the ask through the brand's voice skill, in the audience's English.

- **Leave out anything internal**: requirement counts, PRD ids, status tables, "what's built and what's waiting",
  tool and skill counts, build dates, test-run figures, the list of supported assistants as a matrix. A prospect
  reads these as a vendor's working notes.
- Leave out availability labels ("pilot", "later") when the owner says everything shown is available.
- State hosting the way the audience cares about it: "in the client's own country", not a city.
- Each short's description says what the viewer sees done, in one or two sentences, and carries any caveat the
  picture no longer shows (`brief-and-claims.md` §6).
- Close the page on one ask, from `BRIEF.md`.

## 7. Access

- A site for named prospects can be public with `robots.txt` disallowing everything and `X-Robots-Tag: noindex`.
- A password gate also blocks your own live checks: every live request answers 401, so playback, posters and the
  modal can only be verified on a local server or a preview. If the owner wants a gate, say that, and verify
  locally before each deploy.

## 8. Review and deploy

1. Build the pages through `design-craft:design-craft` and `ux-craft:ux-craft`, and run `design-review:design-review`
   on the rendered pages before the first deploy and after any layout change. Animated demos on a page can time out
   a review's capture pass; review a copy with the animation off and say so.
2. Run `site_urls.py check`. Exit 0 required.
3. Deploy when the user has authorized publishing this series. On Vercel, pin the CLI version
   (`npx -y vercel@<version> deploy --prod --yes`), retry on "temporarily throttled" after 90 s, and expect the
   live alias to answer with the previous deployment for a few seconds after READY.
4. Confirm the live site serves the new files: fetch each page and compare a `?v=` hash, and `curl -I` a republished
   video and compare its `content-length` to the file on disk.
