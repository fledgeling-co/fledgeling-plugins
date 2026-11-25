# Picture

Steps 2 and 4. The films are HyperFrames compositions built and rendered through motion-craft; this file covers
what a demo series needs on top of motion-craft's own references (`saas-films.md`, `craft.md`, `engine.md`), which
still apply.

## 1. The film table

Keep the whole series in one data file the build reads (`SERIES.md` for people, a `plan.json` or Python table for
the build), so one edit rebuilds every film. Per film:

- `id`, title, and the outcome line that names what the viewer sees done;
- scenes in order, each with its own length in scene seconds and its steps timed in scene seconds;
- effect beats (`pop_*`, `click_*`, `whoosh_*`, `chime_*`, `rise_*`) in scene seconds;
- voice placements as `[line id, scene, offset in seconds]`;
- switches: `lockbar` (the small lockup bar on the last 3.2 s) and `labels`.

Two series-wide knobs sit at the top: the **pace factor** and the **label switch**. The pace factor multiplies step
times, camera moves, typing and holds in one place, voice offsets included, so retiming never drifts narration off
its picture. Cap the stretch on short motion: per-operation durations at 1.25x and entrances, exits and travel at
1.2x, so the films slow by dwelling longer rather than by moving through syrup.

## 2. Picture first

Every scene has its own length and its own steps. Narration is placed afterwards at a scene offset and never moves
the picture. This is what lets one render serve both cuts: the muted master is the film, and the voiced cut is the
same picture with a second soundtrack. It also survives the note that arrives in most series, "remove the
narrator", followed a round later by "show it with and without".

## 3. The host-app frame

When the product lives inside another app, keep the films inside that app, because "the tools you already use" is
the point.

- Draw a lookalike frame of the host (Claude, ChatGPT, an inbox, an editor) carrying its name, with no vendor
  logos. Use a native-looking sans throughout: a serif in a chat mockup reads as a broken font, and the owner in the
  source run asked twice for every serif to go.
- Build the product's own cards, panels and views as live HTML from its interface kit, ported into the film, not
  as screenshots. Live HTML stays sharp when the camera pushes in 2-3x, and a copy fix is a text edit.
- Use the product's real mark wherever the host shows the product (tool lines, connector chips, notifications).
- Open on content: earlier messages already in the thread, not an empty window filling up.
- Prefix every film class (`k-`) so it cannot collide with the product's own CSS. In the source run a film class
  `.end` turned every row end in the product's markup into a grey overlay.
- Give every window `isolation: isolate`, or a product view's `z-index` escapes its window and draws over the next.

## 4. Motion on the stage

The opener, the architecture visual and chapter moments sit on a plain ground rather than in a window. The grammar
that served the source run, taken from a calm finance-sector reference film:

- Components arrive alone, from `blur(8-14px)` to sharp with `expo.out` over 0.5-0.6 s and a 16 px rise. They leave
  in 0.3 s on `power2.in`, blurring out.
- One component grows out of the one before it, or travels to a twin's position (`moveTo`), rather than cutting.
- A receding list keeps the focused row sharp and the rest blurred and smaller. A carousel wheels options past a
  fixed point.
- The cursor is a 40-46 px navy arrow with a white keyline and a soft shadow, and a ring lands on each press. It
  moves only toward what it is about to use.
- A status pill above a card can narrate in present tense, a new phrase every 1.5-3 s.

## 5. Holds and pace

- Something changes every 1-3 s: a typed line, a card landing, a count ticking, a mark turning green, the camera
  pushing in. Nothing holds still past 4 s except a short's final result.
- Type prompts at 40-90 characters a second, then hold the finished prompt for 0.5 s plus 0.3 s a word so it can
  be read. Hold citations and completed outputs the same way.
- A short's final result holds about 5 s with a slow push-in (`settle_push`). motion-craft's `pop_scan.py` reports
  that hold as a still run, because a slow push changes too few pixels; disclose it rather than hide it.
- Start slow. The owner in the source run asked for more pace in round 2 and called round 3 "very fast, they were
  hard to keep track of what was going on". The fix was the pace factor, not a re-edit.

## 6. Openings and endings

**The overview.** Open on the full headline already set, held 2-3 s, with the brand mark above it and a small
row of the host apps (for example Claude, ChatGPT, the user's own workspace) underneath. No type-on: in the source
run the first film opened partway through a line typing in, and the owner caught it at once. Then a quick
architecture visual (the customer's sources flowing through the product into the AI tools), then the
demonstrations, then the end slide: the lockup, one line, the ask as text, the mark still for 3-5 s while the music
resolves. The owner in the source run asked for the end slide after a round without one.

**A short.** Reach the product within about 2 s. Show what the person asked, the product working, and the result,
and end on the result. Nothing after it except the small lockup bar over the last 3.2 s. No end card repeating the
headline, no "Book a demo" panel taking over the frame.

**The poster frame** is never the headline frame, because the page already shows the title and the play button
covers its middle. Take the overview's poster from the architecture visual and each short's from its result.

## 7. The lockup

When the brand mark appears beside a product name ("acme | Guardian"), write the lockup once and use it on the pages
and in the films.

- Measure it from the brand's own site: capture its header at 2x and read pixel rows for where the mark's top sits
  against the wordmark's ascenders, how far its tail drops below the baseline, and the colours of each part. CSS
  alone misses all three. The source run's first lockup put the mark too high and used a washed-out front colour,
  and the owner's note was "did you even look at this?".
- Write it in `em` so one `font-size` sizes it everywhere: mark width and height, its vertical offset, the
  wordmark, the hairline, the product name's size and colour.
- Check it in a crop of a rendered frame from each place it appears (the opener, the architecture node, the end
  slide, the lockup bar), not in the stylesheet. The page fix in the source run never reached the films, because
  the films had their own copy of the lockup CSS.

## 8. HyperFrames traps from production

Each of these cost a debugging round:

- A template-literal selector (`` querySelector(`#${id}`) ``) crashes the HTML bundler. Use string concatenation.
- A font with no `@font-face` falls back silently in the render. Declare every face, or drop it.
- Scenes not yet on screen are `display: none`, so every rect measured inside them is zero and the camera parks at
  maximum zoom. Force the ancestors visible while measuring, then restore.
- The runtime parks inactive scenes by removing their markup; scripts then target detached elements. Put
  `data-hf-scene-no-swap` on each scene host.
- A scene whose id equals the root composition's id renders static. Name scenes distinctly (`clip`, not `main`).
- CSS transitions run on the browser clock and cannot be seeked; set `transition: none` in films.
- Opening a side panel reflows the main column, so rects measured before it opens are stale. Measure in the open
  layout.
- A camera that must travel between two windows needs both inside its canvas: widen it.
- `hf.sh check --json` prints text after the JSON. Parse with `json.JSONDecoder().raw_decode`.
- After regenerating the plans, rebuild every film, not only the ones you edited, or shared pieces (the lockup
  bar) go missing from the rest.

## 9. Before rendering

1. `hf.sh check` on every film. Its readability warnings (`line_unread`, `text_below_floor`, `content_overlap`,
   `text_occluded`) are defects in a demo.
2. `hf.sh snapshot --at <every step boundary> -o <dir>` for each film, then open the contact sheet and ask what
   is wrong with it. In the source run, sheets caught marks running past their text, cards framed too small, a
   blank beat and an empty frame while a prompt typed, all before a single render.
3. Confirm every must-carry fact reaches a frame whole, at reading size, with no composer bar or toolbar over it.
