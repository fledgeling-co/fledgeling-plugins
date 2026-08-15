# Deck review — the per-slide gate and the pre-delivery pass

Two loops. The **per-slide gate** runs while you build, because a mistake on slide 2 propagates into every slide that copies its layout. The **delivery pass** runs once at the end and owns what a per-slide gate can't see: consistency *between* slides, the argument as a whole, the export.

**CRITICAL REQUIREMENT: Automatic Preflight & Review Execution is Mandatory.** You must execute `scripts/run-preflight.sh <url> [--regulated]` automatically on every deck build and revision. Never wait for or require the user to ask for preflight or review. Any non-zero blocker (`stageGeometry`, `textOverlaps`, `overflow`, `chromeCollisions`, `provenanceMissing`) blocks delivery (`fix` / `rebuild`).

## The per-slide gate

After drafting each slide, before starting the next. **Run `scripts/run-preflight.sh` first** — it settles the computable half in seconds and leaves the looking for what only an eye can judge. Then the cheap checks:

1. **Does it say one thing?** Name the slide's single claim out loud. If that takes two sentences joined by "and", it's two slides.
2. **Does every slot say something different?** A template with kicker / title / body / caption fills easily and empties nothing. The failure shape, measured on a real generated surface: eyebrow = the item's name, title = a truncated blurb ending mid-clause, body = *that identical string again*, caption = the eyebrow once more. Four slots, two pieces of information, and the hierarchy inverted — the name demoted to a label and a sentence fragment promoted to the headline. A slot with nothing of its own to say is left empty, not filled; and **a title is written short, never cut short** — a heading ending in an ellipsis is body copy in the title slot.
3. **Does the slide's payload restate its own title?** A three-row table under a headline that already states all three rows is a slide's worth of space carrying no information. Cut the table or cut the headline.
4. **Type on the scale & Two-Tier Floor (ISO 9241-303 / DISCAS).** Primary content at or above the distance minimum: ≥24px on a 1920 canvas (reading deck) or ≥44px (projected boardroom deck), with 68px–104px headlines and 96px hero metrics. Auxiliary metadata (eyebrows, table cells, chart ticks, legal footnotes) sits at 18px–20px without competing with primary body copy.
5. **Does the text fit its box and have zero overlaps?** Check for `textOverlaps: 0`. Ensure no flex column labels overflow upward into card headings. In an absolute-geometry format nothing shrinks to fit; in HTML nothing warns you.
6. **No synthetic AI human portraits of real named people.** Never use generative AI face images for real named directors, executives, or personnel. Verify leadership slides use structured typographic cards or authentic facility photos.
7. **Grounding & Regulatory Non-GAAP Prominence.** Every figure and claim traces to the source material. In IR and financial decks, verify that non-GAAP metrics (EBITDA, Underlying NPAT) are accompanied by statutory IFRS/GAAP measures with equal or greater prominence, and every chart carries an as-at date and disclosure provenance.
8. **Accent spent once & dual-theme contrast checked.** One thing carries the colour. On a dark ground, check the accent's *measured* contrast: ensure dark-band lifted tokens (`--color-primary-on-dark: #FF5A5F`) and high-contrast badge text (`#4ADE80`, `#60A5FA`) are used. Badges on photo scrims must use solid primary backgrounds with white text.
9. **Text over imagery is legible, judged on the composite.** A scrim declared in the stylesheet is not a scrim doing its job: check the rendered slide, at the point where the text actually sits, over the busiest part of the photograph rather than an average of it. Can you read every word over the image, and is the smallest text over it still above the type floor?
10. **Charts are deterministic pure SVG & IBCS compliant.** Bar and column charts start at zero baseline (Long & Kay 2024: truncation cannot be cured by footnotes). Asymmetric ROI/cost-benefit uses shared-scale horizontal comparison bars. All charts render inline with zero runtime CDN script dependencies.
11. **Assets are portable & inlined.** For standalone HTML presentations, generated multi-megabyte imagery is downsampled to 1600px JPEG and embedded as Base64 data URIs.
12. **Parallel with its neighbours.** Repeated elements in the same position; section headers identical to each other.
13. **Look at it.** Render the slide and open the capture — see below.

## Look wide, then filter — never both at once

A review has two passes and merging them lowers what you find. During the looking, record everything: the uncertain finding, the low-severity one, the suspicion you cannot yet prove. Ranking, merging and deciding what reaches the summary happen once, at the end.

This matters because suppressing a "minor" finding mid-pass loses it permanently, and because an instruction to be conservative gets followed literally: a brief that says "only flag serious issues" produces a *worse* review rather than a shorter one. If you delegate a lens, never ask it for restraint during the looking — ask for everything, and filter yourself.

## A fixed defect is not a fixed defect class

The most expensive pattern a deck review can fall into, and it is invisible from inside: a defect is found on one slide, repaired there, and the *same defect* ships untouched on another slide, because the fix was applied to an instance rather than to the rule that produced it.

Measured on a real deck. Its own validation pass found a table clipping against its container's right edge on slide 3, rewrote that slide's grid, and reported the issue resolved. On slide 8 an identical table clipped its last column by 24px — same cause, never looked at, because slide 3 was where the eye had been. The same pass reported a metric wrapping to two lines on slide 4, fixed it with a `white-space: nowrap` on that one class, and left every other metric and status badge in the deck able to wrap. And it reported a "vertical void" on slide 9, added content to fill it, and shipped voids of 200–330px on six other slides that were never measured.

So when a finding is repaired, ask the two questions that catch this:

1. **Where else does this shape exist?** Grep the class, not the slide. A fix applied to `.stat-number` on slide 4 belongs in the base stylesheet if slides 2, 5 and 7 also carry stat numbers.
2. **Would the check that found it have found the others?** If it was found by eye on one slide, the answer is no — so re-run it across the deck. This is exactly what `run-preflight.sh` is for: it reports every instance, with a denominator, rather than the one you were looking at.

A per-slide fix list against a deck-wide cause is how a review closes with everything ticked and the same defect still shipping.

## Looking is the part that gets skipped

Three rules make verification real rather than ceremonial:

**Rendering an image is not seeing one.** A screenshot tool returning success proves a file exists. The image enters your knowledge only when you *open* it. If you didn't open it, you didn't check it, and you may not say you did.

**An element capture cannot see the frame.** Screenshotting `.stage` renders that element's own box, so a stage clipped by the window, shifted off-centre, or sitting under floating chrome all capture as flawless slides. Every claim about how the deck *sits in its window* — clipping, letterboxing, chrome overlap — has to come from a viewport capture plus the edge measurement in `html-deck.md` Phase 8. Element captures are for cropping a component you have already located.

**The question you bring determines what you see.** Handed a capture and asked "do you see anything wrong with this?", you find the defect in seconds. Looking at your own render, the implicit question is "is this done?" and the answer comes back yes. Same pixels, opposite results. So ask literally: **"what is wrong with this?"** Answering "nothing" requires first naming the three most likely failure modes for that slide type — a void, a wrapped headline, a misalignment, an overlapping label, a contrast miss — and ruling each out by pointing at pixels.

**Inspect crops, not whole decks.** A full slide scaled into a review thumbnail is a resolution at which a 161px void reads as generous whitespace and an orphaned label is a few ragged pixels. Judging from thumbnails is looking at an image in which the defects cannot exist and concluding there are none. Crop to the region at DPR 2–3.

**Capture after the build-in has finished, and know that it has.** A slide with a staged reveal captures mid-animation as a slide missing half its content, and a colour measured mid-fade is not that element's colour — a contrast gate sampled 400ms into a 700ms entrance read a `#E85A2A` accent as `#6a2d18` and reported a fix making things worse. Drain `document.getAnimations()` before capturing, and if you are measuring rather than looking, record how many were still running.

**Suspect the engine before the page.** A rendering engine that is not packaged Chrome will diverge, and the divergence arrives looking exactly like a defect in your deck. Measured on Obscura, 14 Aug 2026: it resolves `height:84.0%` and `height:86.4%` to the *same* computed pixel value and returns a bounding rect matching neither, which turns a provably zero-based chart into a false axis-truncation finding; it drops single `l` glyphs from Figtree at some sizes, so "Complete" captures as "Comp ete" and "plan" as "p an" in decks whose source is correct; and `DOMMatrixReadOnly` is absent, so any probe constructing one throws and returns nothing. Before changing a deck on the strength of a capture, check the declared value in the source. Two decks showing the *same* anomaly is the tell: that is the engine, not two authors making one mistake.

Do this yourself. A deck is a handful of tool calls to walk, and delegating it costs a whole context to learn what a crop would have told you.

## The delivery pass

Once, before handing over. Walk the whole deck.

**The argument.** Read the titles in sequence — do they carry the whole thing? Is the grammatical style consistent? Are there filler slides to cut? Does slide 9 restate what a listener needs from slide 3 rather than assuming they held it?

**The direction, promise by promise.** Inventory what the deck actually shows in your own words *first*, then reread the direction contract (`visual-craft.md` §2) and walk its five blocks — THESIS, OWN-WORLD, STORY, COVER, FORM. Doing it in that order matters: a review anchored on the contract inherits whatever the contract's abstraction already dropped. Classify each committed element **match / acceptable adaptation / missing / contradicted**. Two rows are mandatory:

- **TYPE** — the display lettering's character, width, weight and contrast against what OWN-WORLD committed to. A face of a different character is *contradicted* however well the slides are laid out.
- **MATERIAL** — a surface rendered as flat colour or a CSS gradient where the direction committed to a photograph, a texture, or a real asset is *contradicted* regardless of composition. The medium is part of the promise, and faked physicality (see `visual-craft.md` §6) counts as contradicted on its face.

An adaptation is intentional only when it cites the thing that forced it — a user answer, a brand constraint, a validator cap, a missing asset. An uncited deviation is a defect, and a missing signature element outranks every craft point below.

**Consistency between slides.** Palette drift (a second blue that's 5% off the first is worse than a clearly different colour — it reads as almost-right and therefore wrong), type-scale drift, spacing drift, a footer that wanders, section headers that don't match each other.

**Overflow and collision.** Nothing escaping its slide bounds; no unintended overlap; long words and URLs wrapped; ellipses appearing where truncation was designed. In HTML, verify strictly at the **13" MacBook Air standard screen resolution (1470×956 / 1440×900)** — no need to test multiple arbitrary device viewports. Ensure the stage letterboxes cleanly, sits vertically centered, and has zero cutoff on the final slide. In an absolute-geometry format, check every element's box against the canvas: `x + w > canvas.w` is off-slide and `y > canvas.h` renders nothing at all, silently.

**Overflow and collision are two checks, not one.** "Nothing past the stage bounds" is silent about content that runs *into* the footer, the page number, or a section band — all of which sit inside the bounds. Measure content against the chrome as well as against the edge:

```js
const footEl = stage.querySelector('.foot');
const footTop = footEl.getBoundingClientRect().top;
[...stage.querySelectorAll('p,li,td,figure,table,h1,h2')]
  .filter(el => !footEl.contains(el))
  .map(el => (el.getBoundingClientRect().bottom - footTop) / scale)   // > 0 is a collision
```

A slide that gains two lines of body copy passes the overflow gate and quietly prints its last sentence through the footer rule.

**Full-bleed integrity.** Backgrounds, hero images and colour panels reach all four edges. A blank strip below a cover image means a wrapper collapsed (see `html-deck.md` Phase 4).

**Navigation and state**, for HTML: keyboard (arrows, space), click/tap, the counter increments correctly, the deck reloads to where it was, nothing throws in the console. A clean-looking deck with an uncaught exception is not verified.

**Contrast**, at the projected end of the range rather than your monitor's. Muted captions on tinted grounds are where this fails.

**The export.** If a `.pptx` or PDF is the deliverable, produce it and open it. A deck that renders in a browser and breaks in PowerPoint has not been delivered.

**Composition, judged as slides not as web.** `align-items: flex-start` with open space in the bottom third is correct slide composition, not a defect. If you feel the urge to change `flex-start` to `center`, that's the web-layout reflex — resist it. The open space is intentional.

**The last look is subtractive.** Remove one element the deck doesn't need. Review rounds accrete; this is the counterweight.

## What a clean gate proves

A passing check means **no known defect is present**. It never means *verified*. Every rule in any gate was written after someone met the defect it catches — it is structurally incapable of finding the one nobody has met yet, and a rule whose selector matches nothing passes silently rather than warning you.

So report the two claims separately, in these words:

```
Gates:       preflight 12/12 slides · 0 stage · 0 below type floor · 1 chart not zero-based
Looked at:   12 slide crops @2x, cover + section breaks, 1280 and 1920
Not checked: the PDF export, the chart's empty state
```

The first line is what a machine asserts, **and it carries its denominator** — `12/12 slides` is a result, `0 failures` on its own is not. A check reporting zero over a selector that matched nothing is indistinguishable from a clean deck, and that is how a whole sweep goes green forever. The second line is what *you* assert, and it's true only for captures you opened. The third is never empty — if you think it is, you've confused the scope of your checks with the scope of the deck.

## Convergence and the disposition

Treat fix-then-recheck as rounds, up to three. Each round's findings should be shorter than the last; a round producing more text than the previous one is churning rather than converging. **Stop the moment a round resolves nothing** — the round after it won't either.

Close every review with one computed word, not a felt one:

- **`rebuild`** — the rebuild condition below fired.
- **`fix`** — findings remain open.
- **`ship`** — nothing material is open.

Report that word verbatim. A deck with open material findings is never announced as a pass, and never under a softer label than the review produced — softening it is the one move that turns a review into theatre. If round three still doesn't clear the bar, deliver the best version under an honest word: "ships with two open items: …".

**The rebuild condition.** When the direction is contradicted across the deck rather than on a slide or two — the wrong type character throughout, the committed material absent everywhere, the cover carrying a different world than the body — the first fix is a **rebuild directive** naming the slides to re-derive and the assets to produce, not a list of cosmetic repairs. A patch list against a deck that failed wholesale launders the rejection into an approval, and on a twelve-slide deck it costs more than the rebuild. Where a fix requires *producing* something — a real photograph, a texture, a drawn icon set — say so explicitly ("produce: cover photograph, site at scale"), never phrased as a style adjustment that will get answered with a gradient.

## The verdict pass — score the fixes, don't re-hunt

After a repair batch, the job is scoring, not finding. For each item from the previous round, one line: **resolved**, **partial**, or **unresolved**, tied to what the new capture visibly shows.

**Your account of what you fixed is not evidence.** A fix you cannot see in the recapture is unresolved however confident the edit felt — the same rule as "rendering an image is not seeing one", applied one step later. A fix answered mechanically, where the element moved but the quality the finding named is still absent, is partial at best.

Then name at most three regressions the batch itself introduced, and nothing else. No new checks, no reopened hunt. Recompute the disposition against what stays open: unresolved or partial material findings can never recompute to `ship`.

## The summary

Short. What the deck is, then: the disposition word, caveats (placeholder imagery still needed, figures the source didn't support), open decisions the user should sign off (the direction, an aggressive hierarchy call), and what you didn't check. Not a slide-by-slide recap of what they watched you build.
