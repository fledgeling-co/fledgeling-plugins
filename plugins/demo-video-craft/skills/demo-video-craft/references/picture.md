# Picture

Steps 2 and 4. The films are HyperFrames compositions built and rendered through motion-craft; this file covers
what a demo series needs on top of motion-craft's own references (`saas-films.md`, `craft.md`, `engine.md`), which
still apply. Every number here is a default the starter kit (`kit/`) already carries; the file says where it came
from and when to move it.

## 0. Start from the kit

`scripts/new_series.py <dir> --fetch` copies the kit into `<dir>/_kit/` and an example series beside it (see
`kit/README.md`). Replace the example's scenario, screens and workflows; keep the engine. How close a new series comes
to the source run depends on the engine's values (fills, eases, holds, the pace function) far more than on prose, and
the source run's first round, built from prose, came out with 12-16 px text and a 54 s opening scene.

## 1. The film table

Keep the whole series in one data file the build reads (`films.py`, summarised in `SERIES.md` for people), so one
edit rebuilds every film: in the source run the shorts' retiming and every fix to all nine went through one table.
Per film: `id`, title and the outcome line; scenes in order, each with its own length and its steps in scene seconds;
effect beats (`pop`, `click`, `whoosh`, `chime`); voice placements `[line, scene, offset]`; switches `lockbar` (the
short's 3.2 s lockup bar; the overview carries none) and `labels`; and `tempo`, the narration's own speed (ffmpeg
`atempo`, 0.92-1.08; line ends become duration / tempo, and past 1.08 shorten the line instead).

**The pace factor** sits at the top of the table and slows a film by dwelling rather than by moving through syrup.
`films_engine.pace()` scales step times, scene lengths, effect beats, voice offsets, typing ends, label holds and dot
flows by the full factor; per-op durations (found through `DUR_AT`, each op's duration argument) by at most 1.25x;
entrances, exits, travel and wire draws by at most 1.2x. The opener takes its own factor. Start at 1.3 for the
overview, 1.22 for the shorts and 1.15 for the opener: the owner in the source run called factor 1.0 "very fast,
… hard to keep track of" and approved those. Once the picture slows, put the narration tempo back to 1.0.

**The length gate.** `write_series` prints every film's length and every scene's before anything is written, and fails
when a film is outside `series.json`'s range or a scene runs past 25 s. Round 1 of the source run built to 126.85 s
with a 54 s opening scene before anyone noticed.

After regenerating the table, rebuild every film, not only the ones you edited, then `git diff` the projects: a
regeneration rewrote the clips and dropped `lock.html` from five of them in the source run. Fork the kit per round
only when the round changes the engine, and record the live fork in `SERIES.md`; two kit copies is how the page and
film lockups diverged.

## 2. Picture first

Every scene has its own length and its own steps. Narration is placed afterwards at a scene offset and never moves
the picture, so one render serves both cuts: the muted master is the film, the voiced cut is the same picture with a
second soundtrack. It survives the note that arrives in most series, "remove the narrator", followed a round later by
"show it with and without". No scene's length may come from a voice line: round 1 of the source run placed scenes at
`line.start - pre`, and unpicking that cost a round.

## 3. The host-app frame

When the product lives inside another app, keep the films inside that app, because "the tools you already use" is
the point. A reference film's motion transfers into the host window; its staging does not: isolated components on a
plain ground are for the opener and the architecture only. The source run wrote a whole stage-only plan and threw it
away when the owner asked for the workflows "inside the Claude mockup".

- **Build the product's screens from its own kit.** When it has a features or marketing page, lift that page's CSS by
  component prefix with its base resets, port its card and row builders into `states.py`, and open
  `states/index.html` to look at every state before building a scene. Live HTML stays sharp at a 2-3x push, and a
  copy fix is a text edit.
- **The host's frame is a lookalike in a native sans.** A serif in a chat mockup reads as a broken font; the owner in
  the source run asked twice for every serif to go, and one survived on disk after the note. `series_lint.py serif`
  over the kit, the screens and the page sources is the gate. This overrides any project memory that says a host uses
  a serif. The brand's own wordmark may keep its serif (pass its file with `--allow`).
- **Tool lines use the product's real tool names**, grepped from its own source, and narrate in the present tense
  while they run ("Reading the newest 13G filings…"), then finish. In a muted cut that status line is the narration:
  every workflow takes three beats, the request, the status, the result with its number.
- **Prompts are one sentence of 6-14 words**, with a file chip above when a file is carried in.
- **The person signed in is a role** ("Investor relations", "CFO · Enterprise"): a company plus a role overflowed the
  sidebar by 83 px.
- **Identity labels go top left** (`LBL = [40, 30]`), never in the composer's band at the bottom, and only when they
  name who acts ("<Claude mark> Dana Ruiz · advisor, in Claude"). Disclaimers are the owner's call (`brief-and-claims.md` §6).
- **The hosts' real marks, when the owner asks for them.** Take them from Wikimedia Commons ("Claude AI symbol.svg",
  CC0, fill #D97757; "ChatGPT-Logo.svg", public domain, trademarked, ink #0D0D0D), drop them in `marks/` as
  `claude.svg` and `chatgpt.svg`, and set `host_marks` in `series.json`. Sizes at 1080p: window wordmark 22 px (gap
  9), card label 16 px (gap 7), identity label 24 px, stage chip 20 px or 34 px, stage heading 32 px (gap 12).
  Credit the trademarks on the page.
- **Open on content**: earlier messages already in the thread, not an empty window filling up.
- **Prefix every film class** (`k-`, `k3-`) and run `series_lint.py collisions --product <the product's own CSS and
  page> --film <the kit CSS>`: a film class `.end` once turned every row end in the product's markup into a grey
  overlay. Give every window `isolation: isolate`.

**The camera.** With no captions the stage is the whole frame (1920x1040, centre y 520); a caption band takes its
height back (round 1 used 1920x860 at y 452). `K.frame` fills a target to a fraction of the stage width, capped at
0.92 of its height and 3.2x: a chat exchange at 0.62, a card at 0.7, a deck slide 0.76, a table 0.84, the composer
0.9. That puts body text at about 27-28 px at 1080p. Frame by a measured selector, clamped to the window's edges,
never by a fixed rect; a whole window appears only to orient, at 1.12 for 2-4 s.

### 3b. A real client's theme

When the screens show a real company (`brief-and-claims.md` §4b), the deck and documents the assistant builds for it
wear its brand. Take the logo SVG from its corporate site's header (`obscura fetch <url> --dump html`, grep for
`logo`), split the mark from the wordmark by x-range (the mark is the path or paths at the left), take the mark's
colour from a colour version if the site's file is monochrome, and add `marks/<client>.svg` and
`marks/<client>-full.svg` (wordmark in `currentColor`). Set `--cl-mark` to the mark colour and `--cl-ink` to the
wordmark's; the kit's deck has a white header with a 3 px rule in the mark colour, figures in the wordmark ink, and a
"<client> theme" pill at a 12 % tint.

A figure the product checked keeps neutral ink when the number is bad news for the company (`lead()` class `chk`);
green is for "matches its source", never for the figure itself. In the source run a real fall in comparable sales was
about to render green.

## 4. Motion

The grammar that served the source run, taken from a calm finance-sector reference film and measured from its frames:

- **Arrivals** blur in and rise: a thread item from `blur(8px)`, 16 px, 0.6 s `expo.out`; a stage component from 10 px,
  18 px. Exits are shorter: 0.3 s `power2.in`, blurring out. A scene enters through `blur(14px)` from ±240 px or a 0.94
  push over 0.5 s and leaves the same way in 0.3 s; never a hard cut.
- **The cursor** is a navy arrow with a 2.6 px white keyline and `drop-shadow(0 4px 8px rgba(10,23,51,.28))`, 40 px in
  a window and 46 px on the stage. It glides in a shallow arc (x on `power2.inOut`, y on `power1.inOut`, 0.6-0.75 s)
  only toward what it is about to use, and presses: the control to 0.965 for 0.09 s, back over 0.22 s, with a ring of
  56 px (64 on the stage), 2 px at 50 % of the accent, from scale 0.2 and opacity 0.6 to 1 and 0 over 0.5 s
  `power2.out`.
- **Focus** (`wheel`): the focused row scales to 1.025 over 0.42 s with a `0 6px 18px -8px` shadow; the others take
  opacity `max(.3, 1 - .36d)` and blur `min(2.2, .9d)` px by their distance d. Every focus gets its release
  (`unwheel`): a row left lifted was the most repeated contact-sheet defect.
- **Continuity**: one component grows out of the one before it, or travels to a twin's position (`moveTo`, 0.8 s
  `power3.inOut`); hide the twin until the traveller lands and swap in one frame, or the two overlap (`hf.sh check`:
  content_overlap). A state swap fades the old state out over 0.22 s first; a `display: none` then fade-in flashes, and
  `pop_scan` shows it as a spike near 6.7x.
- **Stage components** are enlarged with CSS `zoom` and centred with GSAP `xPercent/yPercent -50`, never
  `transform: scale`, so their text is laid out sharp rather than stretched.

## 5. Holds and pace

- Something changes every 1-3 s: a typed line, a card landing, a count ticking, a mark drawing, the camera pushing in.
  A stage scene needs it too: the kit's architecture walks a focus down the sources every 0.8 s, pulses the node to
  1.04 and pushes the next scene's chip to 1.12, and the overview's 4.7 s still run in the source run went to 0.
- **Typing**: 52 characters a second, hold 0.6 s, cursor lead to send 0.6 s (`ask()`). 34 cps with a 1.5 s hold drew
  "long typing animations" from the owner. A prompt already present when its scene opens is written whole at frame 0
  and held 1.0 s (`pre=True`); a drag that opens a scene shows the file and the cursor at frame 0.
- **Reading**: hold a line 0.5 s plus 0.3 s a word from when it lands, citations and outputs included.
- **The highlight** is a tint behind the words (`rgba(31,63,166,.13)`, radius 3, `mix-blend-mode: multiply`, padded
  2 px sideways only), never an outlined box over them, and it lives in the row it marks so it lifts, dims and scrolls
  with that row (`K.ink` parents it; give the row `position: relative`). Put marked text in `.tx` spans so the mark
  draws to the words. Mark the claim, not its grey source line: a tint over a small caption failed contrast (4.15:1).
  The other marks: a 2 px green underline for "matches", a wavy red one for "differs", and `inkTo` turns a red mark
  green when the figure is fixed.
- **A short's final result** holds with a slow push (`settle_push`): from max(last frame + 1.4 s, end - 4.6 s) to the
  end + 0.6 s, at the last fill x 1.07 (at most 0.97), where end excludes the lockup bar. `pop_scan.py` still reports
  about 5 s as a still run on most shorts, because a slow push changes too few pixels; disclose it as accepted rather
  than chase it.
- **To lengthen a short, take the workflow one step further**: save the result into the product, open the product's
  view of it, show the corrected document. Holding longer is not lengthening; the source run took nine shorts from
  about 15 s to 21-25 s this way.

## 6. Openings and endings

**The overview opens** (`intro_scene`, 11.5 scene seconds, 13.2 s at 1.15) on the lockup above the complete headline
from frame 0, with a row of host chips under it arriving 0.13 s apart. No type-on: in the source run the first film
opened partway through a line typing in, and the owner caught it at once. At 3.65 s the headline leaves, the lockup
travels into the architecture's centre node over 0.75 s and the chips travel to their ports; five sources slide in
from the left 0.14 s apart, wires draw 0.07 s apart, dots (r 6) run every 0.55 s with 0.8 s of travel, the focus walks
the sources, and at 10.05 s the first chip pushes to 1.12 and then fills the frame (scale 7, blur 8, 0.6 s
`power3.in`) into the first workflow. Hold the headline until its narration ends: the source run's intro grew from 8.6
to 11.5 s for exactly that.

**The overview ends** on an end slide (`outro_scene`, 4.4 scene seconds): the lockup at y 330, the opening headline
again at y 540 (600 80px Inter Tight, one accent word), the ask at y 760 ("Book a demo" as a 36 px button, the URL
beside it), entering at 0.2, 0.55 and 1.05 s. Give the scene before it an exit. The owner asked for it after a round
without one.

**A short** reaches the product within about 2 s, shows the ask, the product working and the result, and ends on the
result under the lockup bar: a 260 px scrim band (the ground at 0 → 0.94 by 46 % → 1 by 70 %, marked
`data-layout-ignore` with its reason), a white bar 40 px from the bottom with radius 16, the lockup at 44 px and the ask
and URL at 28 px, the band in over 0.5 s and the bar over 0.6 s `expo.out`. No end card repeating the headline.

**The poster frame** is never the headline frame: the page already shows the title and the play button covers its
middle. Take the overview's from the architecture and each short's 0.5 s before its lockup bar (duration - 3.7 s).

## 7. The lockup

When the brand mark appears beside a product name ("acme | Record"), it has one source: the series' `lockup.css` and
`marks/mark.svg`, which `build.py` copies into every film and the site's pages load. Neither keeps a copy: in the source
run the page fix never reached the films, because the films had their own px-based copy, and the front colour lived in
three more places.

- **Measure it from the brand's own site**, by pixel rows at 3x or more, against the reference at the same scale: where
  the mark's top sits against the ascenders, how far its tail drops below the baseline, each part's colour. CSS alone
  misses all three, and a downscaled crop missed them too; the owner's note was "did you even look at this?". The
  source's measured spec, carried in the kit's `lockup.css`: everything aligned on the baseline (never on centres),
  mark .93 x .86 em with its top at the ascenders and its tail .21-.22 em below the baseline, gap .4 em, hairline
  .72 em, product name at .7 em in the interface face.
- **Size it by `font-size` alone**: 60 px on the opener and the end slide, 58 in the architecture node, 44 in the bar,
  22-24 in a page header. A placement that re-sets a child in px is how a second spec starts.
- **Pick colours that read on every ground** the mark sits on: a tint chosen for one ground vanished on another.
- **Align it with its neighbours on the text baseline.** In a page header beside nav links, or in the lockup bar beside
  "Book a demo", the row aligns its items on their baselines, not their boxes: centring boxes put the wordmark 4.4-6.7 px
  off the links on the source run's pages and about 5 px off the button text in every short, and the owner's note was
  "this alignment is bad". Measure a baseline inside the text: a zero-size inline-block appended to a flex container
  becomes a centred flex item and reports the box's centre instead (wrap the text node first).
- **Check it where it is seen**: `delivery.py sheet --at <time> --crop <x,y,w,h>` on the rendered opener, the node, the
  end slide and a short's bar, and the page headers at 2x. When the lockup changes, `series_lint.py retired --term
  <old hex>` over every kit, generator and page source must find nothing.

## 8. HyperFrames traps from production

Each of these cost a debugging round:

- A template-literal selector (`` querySelector(`#${id}`) ``) crashes the HTML bundler. Use string concatenation.
- A font with no `@font-face` falls back silently; a system mono stack (`ui-monospace, SFMono-Regular`) is not bundled
  either. Declare every face.
- Scenes not on screen are `display: none`, so their rects measure zero and the camera parks at maximum zoom. The kit
  shows the ancestors while measuring, and draws a red error on the frame when a scene fails to build, so a broken
  scene cannot render clean.
- The runtime parks inactive scenes by removing their markup: put `data-hf-scene-no-swap` on each scene host. A scene
  whose id equals the root's renders static. CSS transitions run on the browser clock: none in films.
- Opening a side panel reflows the main column: measure in the open layout (`open: True`). A folding sidebar clips
  text unless its children fade over half the fold. A step that targets a panel the state lacks fails only at render
  ("no .pv"): give the state its panel.
- A camera that travels between two windows needs both inside its canvas: widen `.k-cam` (2940 px for two).
- `hf.sh check --json` prints text after the JSON; parse with `json.JSONDecoder().raw_decode`. Its
  `container_overflow` on `div.k-cam` during a push is the camera doing its job; every other overflow is a defect.
- GSAP owns an element's transform: a `gsap.set` that names `xPercent: 0` cancels a CSS `translateX(-50%)`. Every
  short's lockup bar in the source run sat with its left edge at the frame's centre for two rounds because of it.
- A stage `to` step's `dur` and `ease` are the step's: the kit strips them before passing the rest to GSAP, which
  otherwise warns "Invalid property dur" on every one.
- A word beat names a word the line contains (`v4.word:figures+0.2`, `#1` for the second); an alphanumeric token such
  as `close-out` does not parse.
- Run the table generator on its own and read its exit before any build: `films.py | tail && build.py` hid a
  SyntaxError and built ten films from stale plans. Edit a render script by rewriting it, never with a `sed` that may
  match nothing.

## 9. Before rendering

1. `hf.sh check` on every film. Its readability warnings (`line_unread`, `text_below_floor`, `content_overlap`,
   `text_occluded`) are defects in a demo: a split screen at half width runs its card text at about 21 px.
2. `hf.sh snapshot --at <every step boundary> -o <dir>` for each film, then open the sheet and ask what is wrong
   with it. In the source run, sheets caught marks running past their text, cards framed too small, a blank beat, an
   empty frame while a prompt typed and a scene that failed to build, all before a single render.
3. `series_lint.py serif` and `collisions`, and `retired` for any value or name the round retired.
4. After the voice is placed, `sync_table.py films/<id>` for every film (`voice-and-music.md` §4).
5. Confirm every must-carry fact reaches a frame whole, at reading size, with no composer or toolbar over it.
6. After the render, `pop_scan.py --json`: tile the frames around any pop (`ffmpeg -vf "select='between(n\,a\,b)',
   tile=4x2"`) before changing anything; a pop at a scene seam is usually the blur-in, and the slow push reads as a
   still run.
