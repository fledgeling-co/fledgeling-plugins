# Template assembly — the bundled-library target

Build a `lecturn.deck/1` deck from the bundled library: **200 layouts in 27 families**, with **21 recipes** giving an ordered spine per occasion. Referencing a template costs ~80 output tokens where authoring the same slide's geometry costs ~800 — the pipeline expands `{templateId, slots}` into full geometry, z-order, element ids and theme bindings at apply time.

## Read order — and stop when you have what you need

The library is bundled. Two files, in this order:

1. **`recipes.md`** — 21 spines with when-to-use and signal words. Match the brief; take at most one.
2. **`template-catalogue.md`** — 200 layouts in 27 families with their jobs and slots. Read the families the deck needs.

`slot-contract.md` when a gate rejects something. That is the whole read set — author after it.

**No open-ended exploration.** No `ls -R`, no repo-wide grep, no reading a reference "to be sure", and no going after an external deck-schema specification: in a measured run that detour cost four extra tool calls, ~90 seconds, 17k tokens of prompt, and produced a deck with *less* content than the run that skipped it. If something seems missing, hand-author the slide — always permitted, and far cheaper than a discovery sweep.

The upstream generated tree (`scripts/generated/diolog-slide-templates-skill/` in the product repo, `/work/.claude/skills/diolog-slide-templates/` in the runner container) is the source these were folded from. Read it only to run its validator.

## Templates are a base structure, not a form

A recipe is an optional spine: add, drop, reorder, replace or ignore its steps. A template is a starting composition: bend it, or ignore the library and author the slide from nothing. Both are first-class and no gate penalises hand-authoring.

Emit either shape, mixed freely in one deck:

```json
{ "id": "sld_3", "templateId": "kpi-row-3up",
  "slots": {
    "title": "FY26 highlights",
    "kpi.1": { "label": "Revenue", "value": "$48.2m", "delta": "+12%" },
    "kpi.2": { "label": "EBITDA",  "value": "$7.1m" }
  } }
```

```json
{ "id": "sld_4", "elements": [ /* absolute-positioned elements */ ] }
```

Templates expand server-side at apply — never expand one yourself.

Match a template to the slide's **job**, not merely its shape. When the point of the slide needs a composition no template provides, hand-author it.

## The slot contract

Full contract and every validator rule: `slot-contract.md`. In brief — required `!` slots must be present, an unfilled optional slot removes its element and the layout closes up, `max N` caps are refused rather than overlapped, `SOURCE` templates need a `source` slot, `CAVEAT` templates carry a footnote you may reword but not remove, and templates carry no colour or font because the theme resolves those.

## The job envelope, inside the deck producer

The envelope is the contract, not a suggestion.

- `USER_REQUEST.title` is the deck's title, verbatim. The queue/display `JOB.title` is never the
  artifact title.
- Emit only `stage:"planning"` and a short statement of working assumptions. Do **not** emit deck
  structure or content events yourself — the deterministic finalizer streams those from the
  validated bytes, and a second source of truth desynchronises the live view.
- Apply the selected deck template id and its complete `templateInstructions` as binding composition
  direction when the operator selected one.

## Deck root and transport metadata

```json
{
  "schema": "lecturn.deck/1",
  "id": "…", "title": "…",
  "canvas": { "w": 1280, "h": 720 },
  "theme": { "tokens": { } },
  "slides": [ ],
  "x": { "diolog": {
    "recipeId": "fy-results",
    "structure": [
      { "id": "sld_1", "kind": "cover", "label": "FY26 results",
        "bullets": ["Company and reporting period", "The year's defining line"] }
    ]
  } }
}
```

Derive `theme.tokens` from the supplied design system — an authored palette wins over the derived one, and the apply step only fills what you leave absent. Terminate font stacks with a generic (`Figtree, sans-serif`).

**Take sizes from `theme.tokens.typography.scale` when the theme carries one.** It is a named ladder
in px — `display`, `title`, `stat`, `headline`, `sub`, `lead`, `body`, `small`, `overline` — derived
from the brand's own stated type scale. PICK a step; do not invent a number per element. A
hand-authored deck of the same brief ships exactly such a ladder and every element selects from it,
which is why its hierarchy is identical on all nine slides. A producer that re-derived sizes per
slide shipped 17 arbitrary steps in one run and 0 in the next.

The size field is **`fontSize`** (the adapter also accepts lecturn's `size`). State it on every text
element: omit it and the renderer draws one default size for everything, and labels collide with the
copy beneath them.

`x.diolog.structure` carries exactly **one entry per slide, in the same order, with `id` equal to the slide's `id`**. `kind` is one of `cover | stat | chart | split | title`; `label` is the visible slide title; `bullets` holds 2–5 grounded outline beats. This lets the deterministic finalizer paint the live skeleton without a second model pass — a missing or misordered entry costs a whole extra pass.

## Element vocabulary that survives apply

`text` · `stat` · `table` · `image` · `shape` · `line` · `chart`.

Do **not** author `group`, `widget` or `embed` — they have no deck mapping and are dropped. Compose with absolute `layout` boxes instead.

## Hard rules the validator enforces

Per-element: `stat.value` ≤14 characters and figure-shaped; a stat must fit its box width or it wraps mid-figure; no fully empty table rows; text must fit its box at its stated `fontSize`; nothing past the 1280×720 frame; no two text-bearing elements overlapping by >20% of the smaller box.

Deck-level, and these exist only in the validator — an author working from the catalogue alone will not know them: a headline figure authored as `text` at ≥40px must be a `stat`; four or more slides on one ground fails; fewer than four distinct font sizes across the deck fails. Arithmetic and rationale in `slot-contract.md`.

## Look at it before you finish

**Inside the deck producer, `render_deck` is mandatory and it is the highest-leverage step in this
file.** It stages `deck.json`, renders every slide through the SAME adapter and renderer the apply
path uses, and returns per-slide findings — `blocker` (broken) and `craft` (reads poorly).

```
render_deck({ deckPath: "deck.json", themeTokens })
```

- Call it after your first write. Always, before `submit_artifact`.
- Fix every `blocker`, call it again, repeat until `blockerCount` is 0.
- Then act on the `craft` findings that make the deck read better, and re-render.
- Pass the same `themeTokens` the apply step will bake. Omit them and the preview is not the deck
  that ships — the bake resolves ground, ink, accent and the type face.

This **overrides the write-once discipline**: an edit driven by a render finding is required, not
waste. The one-write rule exists to stop blind second-guessing of copy you already sourced, not to
stop you repairing something you can see is broken.

Measured, on the same brief: a producer with no render made 13 tool calls, never saw its output,
and shipped stat figures wrapping mid-number ("3,000sqm" as "3,0 / 00s / qm"), table rows drawn
blank, 23 stray pale rectangles, and a whole deck set in Times. With the loop, the same brief
reached 0 blockers across 6 render cycles, two grounds, 17 type steps and nothing off-canvas.

Standalone (no `render_deck` available), do the equivalent by hand: render, screenshot every slide,
and open every capture. A screenshot you generated but didn't look at is not evidence.

## Finishing

Write the finished artifact once. Depending on how you were invoked:

- **Inside the deck producer**, finish with one by-reference call — `submit_artifact({artifact:{kind:"deck", deckPath:"deck.json"}})`. It reads the file, runs the strict template-union and deckconv gates, streams structure/status/content from the validated bytes, and persists exactly those bytes. Don't run or read the validator yourself.
- **Standalone**, run the bundled validator and fix every error it prints:
  ```bash
  node scripts/generated/diolog-slide-templates-skill/scripts/validate-deck.mjs deck.json
  ```

Either way a validation error is a real authoring error. Repair `deck.json` and retry; never bypass the gate, and never downgrade a slide to a weaker template merely to satisfy it — that trades the deck's content for a green check.

## Craft still applies

The template library decides composition, not quality. `references/visual-craft.md` governs the theme tokens, the accent budget, the type ramp and the anti-slop rules; SKILL.md §4 governs the title sequence; and the grounding rule bites hardest here — every figure on an investor slide traces to the supplied company material. An unsourced number is a defect regardless of how good the slide looks, and in this context it is compliance exposure rather than a style note.
