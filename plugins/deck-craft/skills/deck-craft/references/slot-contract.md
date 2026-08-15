# Slot contract and validator rules

What a template expects, and what the gate rejects. Every rule below was measured against a real generated deck — the rationale in each case is the defect it caught.

## Slot contract

Slot kinds: `text` · `stat` · `list` · `tableRows` · `chartSeries` · `imageRef` · `widgetConfig`.

- **Required slots (`!`) must be present.** An unfilled *optional* slot removes its element and the layout closes up — that is how a 4-up row honestly shows three figures instead of padding a fourth.
- **Respect `max N`.** More list entries than a layout holds is refused rather than overlapped.
- **Never invent data for a chart or table.** Bind real figures from the brief or attached documents. If the data isn't there, pick a template that doesn't need it — an empty series is refused.
- **`SOURCE` templates need a `source` slot**, because they present figures the company didn't produce: a registry's vote count, a broker's target, a peer set's multiples.
- **`CAVEAT` templates carry a mandatory footnote.** Reword it; you cannot remove it.
- **Templates carry no colour and no font.** The theme resolves those. Never put a colour in a slot value.

A templated slide is `{id, templateId, slots}`; a hand-authored one is `{id, elements}`. Mix both freely in one deck. Templates expand to geometry server-side — never expand one yourself.

## Per-element rules

**`stat.value` is a figure, ≤14 characters.** The renderer sizes a stat from its box, so prose there renders enormous and spills over its neighbours. Words go in `label`.

**A stat must fit its box width.** The gate runs the same arithmetic as the renderer:

```
size = max(16, min(120, box.h * 0.72, (box.w / (len * 0.62)) * 0.94))
fails if len * size * 0.62 > box.w
```

Measured failure: `"3,000sqm"` in a narrow box wrapped mid-figure to `3,0 / 00s / qm`. Widen the box or shorten the figure.

**No fully empty table rows.** An empty row renders as a blank band. Fill it or drop it.

**Text must fit its box at its stated `fontSize`.** Capacity estimate, deliberately generous — it catches text that *cannot* fit, not tight-but-fine copy:

```
perLine  = floor(box.w / (fontSize * 0.58))
lines    = floor(box.h / (fontSize * 1.2))
capacity = perLine * lines
fails if text.length > capacity * 1.15
```

**Nothing extends past the 1280×720 frame.** A deck has no scroll, so anything past the edge is simply invisible. Measured: an 8-row table ran to `y=745`; the rows past the edge and the footnote they overlapped were both absent from the render, and neither the text-fit check nor the overlap check caught it — both judge elements against each other rather than against the frame.

**No two text-bearing elements overlapping by more than 20% of the smaller box.** Only `text`/`stat`/`table` pairs count; a shape behind its own caption is normal composition. Two text elements on top of each other print one across the other.

## Deck-level floors

These are properties of the **set**, invisible to any per-slide check. They are in the validator and nowhere else — an author working from the catalogue alone will not know they exist.

**1. A headline figure authored as `text` is just a word.** At `fontSize ≥ 40` with ≤14 characters matching a figure shape (`$48.2m`, `~90%`, `150t+`, `2M+`, `1986`), it must be a `stat`. Measured: a deck carried 2 stats and 94 texts, and not one number read as a number — a text figure never takes the accent colour and is never sized to its box.

**2. Four or more slides on one ground is a document, not a deck.** Vary it — cover, section breaks and closer against the dense content slides — so the deck has rhythm when paged through. The ground is the slide's own `background`, else a full-bleed shape (≥90% of canvas) behind everything.

**3. Fewer than 4 distinct font sizes across the whole deck fails.** A deck with no type range has no hierarchy. Measured: one run shipped 180 elements at a single size because every `fontSize` was dropped, and every label collided with its copy. Pick steps from the theme's type scale — display / title / heading / body / caption.

## Running the gate

Inside the deck producer, finish with `submit_artifact({artifact:{kind:"deck", deckPath:"deck.json"}})` — it runs the template-union and deckconv gates against the validated bytes and persists exactly those. Don't run or read the validator yourself.

Standalone, the bundled validator is:

```bash
node <templates-skill>/scripts/validate-deck.mjs deck.json
```

It needs `deckconv` for the hand-authored branch; point `STUDIO_DECK_CONVERTER_ROOT` at a checkout containing `src/deckconv/__main__.py` if the default path doesn't exist on the machine.

A validation error is a real authoring error. Repair the deck and retry. Never bypass the gate, and never downgrade a slide to a weaker template merely to satisfy it — that trades the deck's content for a green check.

## What the gate does not prove

It is arithmetic over boxes. It cannot see whether the deck reads well, whether the accent lands, whether the titles carry the argument, or whether a figure is *right* — only that it fits. A clean gate means **no known defect is present**, never *verified*; see `deck-review.md` for the pass that needs eyes.
