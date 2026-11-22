# Product Demo: Staged Product UI for Landing Pages, Features and Bento Tiles

Use this file when a surface needs to **show the product working** rather than describe it: a hero demo, a feature-card animation, a bento tile with UI in it, a faux-UI still for docs, or a looping walkthrough of one action. It replaces the two failures that ship by default. A pasted screenshot gives the visitor a whole interface to read, so they read none of it. A demo drawn from memory is a generic dashboard that resembles no real product and carries animation with no cause.

The procedure is adapted from **Stageshow** by Benji Taylor, head of design at X (MIT, `github.com/benjitaylor/skills/tree/main/stageshow`; write-up at `benji.org/stageshow`). His governing line is the bar for every decision below:

> It reads as a real product, simplified to what the viewer needs, framed with intent, and every motion has a cause.

**When the Stageshow skill itself is installed, use it.** If the session's skill list includes Stageshow (installed with `npx skills add benjitaylor/skills --skill stageshow`), invoke it by the exact identifier the list shows rather than a guessed one: it ships about 40 gold examples, a React kit, and filming scripts this file can only describe. This file is the procedure for when it is absent, and the house rules (direction contract, visitor mode, lookalike gate) still apply on top of it either way.

## The five failure modes

Name which one a draft is closest to before you fix anything. Each has a different fix, and a fix aimed at the wrong one makes the draft worse.

| Failure | What it looks like | Fix |
|---|---|---|
| **Too much** | Real text in every row, numbers everywhere, every cell filled. More detail reads as more generated. | Cut real words to the budget below; render the rest as filler bars. |
| **Wireframe** | "Two gray blobs and a button." Too small, or stripped of what made the product recognisable. | Rebuild at a real size with the product's chrome, icons and one real content moment. |
| **Boxed** | The whole window shrunk into a card with even margins on four sides, so it reads as a pasted screenshot. | Let the window fill at least two thirds of the stage and run off an edge. |
| **Flat** | Every object at equal weight in identical bordered cards, so the eye has no landing point. | Pick one focal object; quiet everything else to grey. |
| **Bland** | A generic grey window and a cursor, ignoring the brief's look and energy. | Apply the committed direction in full, inside the rules. |

The shared fix: a full, structured screen in quiet greys, with real words only where the story is. Empty corners, a void under a list, stretched rows, or a window floating on a plate all read as unfinished rather than calm.

## The seven steps — plan first, build second

Write steps 1–3 as a short plan before any markup. Most of the decisions that show on screen are made here, and a crop settled after building wastes the work that lands outside it.

### 1. Medium and place

- **Still or animation**, and if animated: loop, once when scrolled into view, or on hover.
- **Size by placement:** hero beside copy about 720×340; full-width hero 900–1100 wide; card 400×300 at 1:1. A demo is never under about 320 wide; bento tiles and satellites may be smaller.
- **Phone gets its own design.** Anything that can land in a phone column ships a compact composition at 358 wide, "a redesign not a squeeze": rearranged for the column, not scaled down.
- **Bento grids are planned as one set.** A third to a half of the tiles show UI, window chrome appears once across the grid, and no two adjacent tiles are the same kind. Cell count equals content count (`ai-slop-check.md` §11).

### 2. Look

- **Map the product's own tokens first** — colours, type, radii, icon set, real window chrome. Use the product's real components inside the stage when the codebase has them. Chrome must match the product: an address bar on a native Mac app reads as made up.
- Without a product system, choose a theme (light, dark, blueprint, glass), a palette (accent or mono) and a **fidelity**: `minimal` (all bars), `standard` (words where they carry meaning, bars elsewhere — the default), or `realistic` (real content throughout — for hero scale, a named real product, or list and page stills).
- A brief that names a style gets that style in full, still inside these rules.

### 3. Story

- **One action, 3–5 beats plus a payoff, over 10–16 seconds.** Shapes: how it feels to use, a flow, or what the system does on its own.
- No unexplained cursor move. Data never rewinds in view without a visible cause.
- When richer story and calmer frame conflict, the calmer frame wins.
- Keep requests this small: "a looping hero demo: someone assigns an issue to a teammate" — one interaction, one product, one size.

### 4. Start from an example

Rules alone get an agent part of the way; an example gets it the rest. Stageshow's author found that an agent told to run a window off the frame edge barely did it, and one shown an example that did got it right. So before drafting:

- **With the Stageshow skill installed:** film its closest gold and copy its folder, keeping its stage size, crop and bleed, row and type sizes, spacing, beats and kit parts. Then replace the look and content; changing only the name does not count.
- **Without it:** run `mobbin-trawl.md` checkpoint **M2** for the closest shipped screen of the same job (`search_screens`, `limit` 4–6, naming the product category and the one action). Take its frame and proportions as your starting structure and record the gold in the ledger.
- **Framing in short:** one gutter, either full or well past; only filler bleeds; whatever opens stays in frame; windows keep their shape; no plate under a hero on a white or dark page; no window shown whole with air on all four sides; no dead corners.
- Film a still at both widths beside the gold and fix the frame **before** adding motion.

### 5. Screen

- **Budget 3–7 real strings on the whole screen.** It is a budget for words, not for elements: rows, avatars and controls stay; their text becomes filler bars unless it carries the story.
- Fit every control's text before anything moves. A label that overflows its button at rest overflows worse mid-animation.
- Mark cursor targets in markup (`data-target`) and measure their boxes at runtime with `getBoundingClientRect()`; never hard-code a cursor position, because a font substitution or a width change moves the target and leaves the cursor clicking air.

### 6. Choreograph

- Build on the timeline engine in `make-an-animation.md` Phase 2, so every frame is a pure function of `t` and the `window.__animStage.setTime()` bridge can seek it. That bridge is also what makes step 7 possible.
- Keep appearing elements mounted and toggle them, so exits animate rather than vanish. When a button's label changes, change it on the same element instead of swapping elements.
- Animate relationships: a new row pushes the rows below it; a resized surface does not stretch its text.
- The cursor moves like a hand — shallow arcs timed by distance, visible presses — in one cursor style per site.
- Overlap beats, stagger groups, hold the payoff. The loop ends where it began, or resets with a visible cause.
- Reduced motion shows the poster frame (step 7) and nothing moves.

### 7. Rehearse — film the motion, not the rest state

Reading the code back or screenshotting the finished state misses the frames in between, which is where demo bugs live: a 4px hop as a row slides in, one frame where everything has faded out at once. So:

1. **Set the poster first.** It is the frame most people see — thumbnails, reduced motion, screenshots. It tells the story alone, is never caught mid-change, and leaves the result on screen.
2. **Film a contact sheet.** Seek the timeline at a fixed interval (every 250ms across one full loop gives 40–64 frames) through the `setTime` bridge, capture each frame at the shown width and at 390, and tile them in order onto one sheet. Use Obscura's capture interface, or agent-browser's (`eval` the seek, then `screenshot`) when Obscura fails; `make-an-animation.md` Phase 4 has the seek-and-capture loop for both.
3. **Measure what the sheet cannot show at a glance**, from the same seek loop: for each frame, record the bounding box of every `data-target` and every text node. Flag (a) a box whose position changes by more than 2px between consecutive frames when no beat is scheduled to move it — a one-frame jump; (b) text whose `scrollWidth` exceeds its box — an overflow; (c) a frame where the summed opacity of the focal elements falls below a third of the poster's — the everything-faded-at-once frame; (d) frame 0 and the last frame differing at the loop seam without a scripted reset.
4. **Fix in order: framing, then hierarchy, then motion, then polish.** Re-film after each fix. The biggest fault is whichever "no" comes first in `mobbin-trawl.md` M5's five pairs, asked of the sheet against the gold.
5. **Hand over only when the measured checks print nothing.** A clean run rules out the four measured faults and nothing more: the checks catch mistakes, not dull ideas, so say in the handover that a person still has to watch the loop.

Step 7 counts as one round of the skill's bounded verification, not an extra loop on top of it.

## Recurring faults to check on the sheet

Content that swaps instead of moving · grey filler bars exactly where the eye lands · a plate behind the window, or a floating window · empty bands, cut controls, clipped shadows · stock AI looks and invented logos (sparkles, purple, a letter in a coloured square) · busy rows and uneven insets · long holds and resets with no cause · a text selection not under the I-beam · a hand-drawn status bar or home indicator · an amount centred together with its currency sign.

## Hand over with `REHEARSAL.md`

Write it beside the component, at 10–20 lines:

```
REHEARSAL — hero-assign-demo
  gold        Stageshow `issue-assign` | Mobbin <mobbin_url> (M2)
  changed     look → product tokens (slate/indigo, 6px radii); content → 5 real strings
  size        720×340 desktop · 358 compact · poster at beat 4 (assigned state)
  checks      48 frames @ 250ms × 2 widths · jumps 0 · overflow 0 · seam clean
  not checked whether the idea is engaging (watch it) · Safari timing · real fonts if the engine substituted
```

When the user corrects something about a demo, fix it, then offer to add the correction as a rule here so the next demo does not repeat it. That loop — run fresh, note the fault, change the procedure, re-run — is how Stageshow's own rules were written.
