# lecturn.deck/1 — the structured-JSON target (and `.pptx` through it)

One canonical JSON structure for a deck: `presentation → slides → positioned elements`. Author the JSON, validate it, convert. Never hand-build OOXML — a `.pptx` is a zip of interdependent XML parts, and emitting it directly fails in ways nothing reports.

## Root shape

```json
{
  "schema": "lecturn.deck/1",
  "id": "deck_fy26",
  "title": "FY26 results",
  "canvas": { "w": 1280, "h": 720 },
  "theme": { "tokens": { } },
  "slides": [ ]
}
```

`canvas` is the coordinate space every element positions against. 1280×720 is the common choice; 1920×1080 works if you keep every size consistent with it. Element geometry is absolute inside that space.

An authored `theme.tokens` palette wins over a derived one — set it when you have a brand, and terminate every font stack with a generic (`Figtree, sans-serif`), because a bare family that fails to load falls back to serif and silently changes the deck's character.

## The element union

Elements are discriminated on `type`. The ones that render:

`text` · `stat` · `table` · `image` · `shape` · `line` · `chart`

Each carries an `id`, a `type`, and an absolute `layout` box (`x`, `y`, `w`, `h`) in canvas units, plus its own fields.

Three more types exist in the wider schema — `group`, `widget`, `embed`. Whether they survive depends on the consumer, and in the Diolog deck pipeline they are dropped outright. Compose with absolute `layout` boxes instead of grouping; you lose nothing, because geometry is absolute anyway.

## Validator rules that actually bite

These are the failures that recur, and each has a reason worth knowing:

- **`stat.value` is a figure, not prose — keep it ≤14 characters.** The renderer sizes a stat from its box, so a sentence there renders enormous and covers its neighbours. Words go in `label`. A value that can't fit its box width at a legible size wraps mid-figure, which looks like a rendering bug and reads as one.
- **No fully empty table rows.** An empty row is either missing data (fix the data) or spacing (use layout).
- **Text must fit its box at its stated `fontSize`.** The renderer does not shrink to fit. Either the box grows or the copy gets shorter — and the copy getting shorter is usually the better slide.
- **No two text-bearing elements overlapping by more than ~20% of the smaller box.** Overlap that reads as deliberate layering in your head reads as collision on screen.
- **Every slide needs at least one renderable element.** A slide holding only a `group` or nothing at all fails.
- **Element ids are unique across the deck**, not per slide.

## The converter

A stdlib-only Python converter (`deckconv`) does the round trip. Locate it rather than assuming a path — it ships inside a plugin, so its root varies:

```bash
CONV=$(find ~/.claude ~/Dev -maxdepth 8 -type d -name deckconv -path '*/src/*' 2>/dev/null | head -1)
export PYTHONPATH="$(dirname "$CONV")"
DECK="python3 -m deckconv"
```

If `${CLAUDE_PLUGIN_ROOT}` resolves to a plugin carrying `converter/src`, use `${CLAUDE_PLUGIN_ROOT}/converter/src` directly.

```bash
$DECK from-pptx deck.pptx -o deck.json   # import; extracts media to ./assets, prints a fidelity report
$DECK to-pptx   deck.json -o deck.pptx   # export; embeds images from the deck's directory
$DECK validate  deck.json                # strict structural validation; exit 1 + stderr on errors
$DECK inspect   deck.pptx | deck.json    # element census + fidelity counts
```

Python 3.11+ on PATH is the only requirement. If the converter genuinely isn't on this machine, say so plainly and deliver validated JSON rather than pretending a `.pptx` was produced.

## Workflow

**To create a `.pptx`:** author `deck.json` → `validate` → `to-pptx`. Validate after every edit, not once at the end; it is a strict linter (schema tag, required fields, discriminants, unique ids, non-empty slides) and its errors are cheap to fix while the slide is still in your head.

**To read or edit a `.pptx`:** `from-pptx` first, work on the JSON, `validate`, convert back. Read the fidelity report — it names what didn't survive import, and a construct that silently dropped on the way in will be missing on the way out.

**Round-trip fidelity is not total.** PowerPoint carries constructs this schema doesn't model. When the report flags losses, tell the user which ones rather than shipping a deck that quietly lost its animations or its master-slide inheritance.

## What the format doesn't do for you

Absolute geometry means nothing reflows. The layout you author is the layout that renders, at every size, forever. So the craft in SKILL.md §5 is doing more work here than in HTML: type sized for distance, one focal point, an accent spent once, parallel positions slide to slide. There is no cascade to save a slide whose boxes were placed by eye.

Sanity-check geometry as you go: a `w` that exceeds `canvas.w - x` is off-slide, and a `y` past `canvas.h` renders nothing at all with no error.
