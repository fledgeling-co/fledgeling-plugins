# Systematisation

Tier 1 mostly — measurable, deterministic. This is the version of the "does it look generic" question that survives the taste argument.

## The mechanism

Slop fills the gaps where design decisions were not specified. If a brief doesn't define typography, spacing, colour and motion, a generator infers them from general patterns and the result is generic — not because the tool has bad taste, but because nothing constrained it.

So measure **specification vs default**, not aesthetics. That check holds under both positions in the unresolved argument (see `reliability-envelope.md`): whether or not "slop" names a real property of artifacts, a surface whose values are ungrouped and undeclared is measurably less systematic than one whose values trace to tokens.

## Variance metrics

`scripts/analyze_styles.py` computes these from the extracted computed styles.

Count distinct values across the surface for:

| Property | Healthy | Flag | On Obscura |
|---|---|---|---|
| Font sizes | 4–8 site-wide, ≤3 above the fold | >10, or arbitrary values off-scale | computed |
| Font weights | 3 | >4, or a regular→medium→semibold→bold ladder | computed |
| Spacing values | multiples of 4 or 8 | any off-scale value (`7px`, `18px`, `13px`) | composed from longhands |
| Colours | 3–5 plus tints | 8+ distinct, or >12 raw hex outside `:root` | computed |
| Border radii | ≤3 | a 4th distinct value | **longhands** (the shorthand reads `0px`) |
| Shadows | 3–4 elevation levels | ad-hoc per-component shadows | **declared** (computed reads `""`) |
| Transition durations | a named set | mixed arbitrary values | **declared** (both longhands read `""`) |
| Content max-widths | 2–3 tiers | a 4th, or rails shifting between sections | computed |
| z-index values | tokenised scale | `9999`, or any ad-hoc ladder | computed |

For each, report the distinct set, the implicit scale it suggests, and the outliers.

**The right-hand column is why four of these rows once reported clean forever.** Radii, shadows, durations, the untracked-caps tell and the `transition: all` detector all read computed properties that return `0px` or `""` on the review engine whatever the CSS says. Measured 18 Aug 2026 on `evals/fixtures/landing.html`, which plants every one of them: `borderRadius` `0px` against `border-radius:24px`, `boxShadow` `""` against a real shadow, `textTransform` `""` against `uppercase`, both transition longhands `""` against `transition:all 0.3s ease-in`. A `0 distinct radii` result reads as a perfectly tokenised surface, and three of the nine rows above were structurally dead.

They are alive now, from two routes: compose the shorthand from longhands where those answer (radii, border widths, spacing, gap), and read the stylesheet declaration where they do not (shadows, text-transform, transition). `dumpStyles()` tags every value with its source and `analyze_styles.py` prints a measurability line before the metrics:

```
~ durations, radii, shadows, transition_all, uppercase_untracked recovered from the
  stylesheet rather than the computed cascade — counts reflect declared intent.
```

Two rules follow, and both matter when quoting these numbers:

- **Say "declared" when the value came from a declaration.** It reports what the author asked for, not what the cascade resolved. On an engine that answers both they agree; here only one answered.
- **A metric reported `UNMEASURABLE` is never printed as a count.** `audit_run.py capability` exits non-zero while any metric a report would quote is in that state. A count of zero from a dead channel is not a measurement of zero.

`scan_source.py` remains the independent path for the source side of these — `transition-all`, `ease-in-on-ui`, `outline-none` — and running both is the cheap cross-check: source says what was written, the declaration index says what the served page carries, and a disagreement between them is a build-step finding.

## Near-miss weighting

**A value within ~5% of an existing token is a *more* severe finding than one clearly different.**

Colour perception is non-linear, so "almost right" registers as more wrong than "obviously different". A blue 3% off the brand blue reads as a mistake; a clearly different blue at least might be deliberate.

Snap near-misses to the token. Only clearly-different values get to argue they were a choice.

Same logic applies to spacing (`15px` beside a 16px scale), radii, and durations.

## Token adherence

Where a token source exists — `tokens.css`, `theme.ts`, `_variables.scss`, `tailwind.config.js`, a DTCG JSON file, a `design.md`, or a live Figma MCP connection — compare it against the computed styles pulled from the render.

This is the single highest-value check available, because it converts a subjective question into a deterministic one:

> "Does this button look right?" → "Does this node's `border-radius` equal `$radius-md`?"

No model variance, no perceptual judgment, no false positives from rendering differences. Push as much of the review onto this comparison as the surface allows.

Report per violation: the node, the property, the actual value, the token it should have used, and the delta.

Also flag: unresolved `var(--*)` references (they silently fall back), inline styles carrying values that exist as tokens, and utility-class soup with no semantic grouping.

## The token nothing reads

A token that is **declared, emitted onto the page, and referenced by no rule** is a live defect, not tidiness. It passes every check a reviewer would think to run: it is in the contract, it is in the record, it is in the DOM, and `grep` finds it. What it is not is *applied* — so the value it was supposed to override is still being painted, and the surface looks exactly as it did before the token existed.

Measured: `--primary-on-dark` was carried by a multi-tenant contract, set by every tenant record, emitted by the style injector, and read by **no rule in the stylesheet**. Every accent word on every dark band painted in raw `--primary`. The house tier's 72px company name — the largest text on its own hero — sat at **2.14:1**.

`probeUnconsumedTokens()` (in `runAll().tokens`) collects every `--x` declared in a readable stylesheet or inline style, every `var(--x)` referenced by any rule, and returns the difference. Two limits, both reported beside the answer rather than hidden:

- **A cross-origin stylesheet cannot be read.** `unreadableSheets > 0` means the answer is partial and must be reported as partial.
- **A token read from JavaScript is invisible here** — `getComputedStyle(el).getPropertyValue('--x')` consumes it without any rule saying so. Grep the source before acting on an entry.

The converse finding is the more familiar one and is already covered above: a `var(--x)` that resolves to nothing silently falls back. Both are the same class — the declaration and its use drifted apart — and neither is visible in a render.

## Role adherence

A token scale with assigned semantic roles converts "use good colours" into a checkable rule. Vercel's Geist publishes one worth copying as a model:

| Steps | Role |
|---|---|
| 100–300 | Component backgrounds — default, hover, active |
| 400–600 | Borders — default, hover, active |
| 700–800 | High-contrast background and hover |
| 900 | Secondary text and icons |
| 1000 | Primary text and icons |

With roles declared, violations are mechanical: is a 900-step colour being used as a border? Is a 400-step being used as body text?

If the design system under review declares roles, check against them. If it doesn't, that absence is itself a finding — an unassigned scale can't be violated, which means it also can't be enforced.

## Cross-page drift

Sample multiple pages and measure variance between them.

Premium work shows tight adherence across pages; generated work shows drift. The documented cause: generating different sections in separate conversations produces inconsistent spacing, colours and typography, because each generation re-infers what wasn't specified.

Check: do the same components carry the same values on different pages? Does the type scale hold? Do the section rhythms match?

## DTCG conformance

Where a token file exists, check it against the Design Tokens Format Module **2025.10** — a W3C Community Group Report, not a Recommendation, so treat conformance as good practice rather than a standard obligation.

Basic types: `color`, `dimension`, `fontFamily`, `fontWeight`, `duration`, `cubicBezier`, `number`.
Composite types: `strokeStyle`, `border`, `transition`, `shadow`, `gradient`, `typography`.

Validators exist; a malformed token file is a deterministic finding.

## design.md conformance

Google Labs' `design.md` spec, currently `version: alpha`. YAML front matter carrying machine-readable tokens, plus a markdown body carrying human-readable rationale. Tokens are normative; prose gives context.

Schema shape:

```yaml
version: <string>          # optional, current: "alpha"
name: <string>
description: <string>      # optional
omitted: <string[]|OmittedSection[]>  # optional
colors:
  <token-name>: <Color>
typography:
  <token-name>: <Typography>
rounded:
  <scale-level>: <Dimension>
spacing:
  <scale-level>: <Dimension | number>
components:
  <component-name>:
    <token-name>: <string|token reference>
```

Token references use `{path.to.token}` and must resolve to a primitive, except inside `components` where composite references like `{typography.label-md}` are allowed.

Body sections are all `<h2>`, omittable, but present ones must keep this order: Overview, Colors, Typography, Layout, Elevation & Depth, Shapes, Components, Do's and Don'ts.

**Duplicate section headings are the one hard failure** — reject the file. Unknown headings, unknown token names and unknown component properties are preserved or warned, not rejected.

Two things worth checking beyond validity:

1. Is it referenced from `CLAUDE.md` / `AGENTS.md`? A design.md nothing points at never gets read. The wiring line is roughly *"When creating or modifying any UI, read and follow design.md."*
2. Does it point deeper? A lightweight design.md that references per-component metadata (sizes, variants, relationships, anti-patterns) holds more than one that tries to inline everything.

Rules in the register that works, drawn from a real generated example: "strict four pixel spacing", "weight 600 only", "don't introduce new hues", "don't use more than two font weights in a single region". Enforceable. Compare with "use sparingly", which is a decision deferred rather than made.

## Enforceable vs unenforceable rules

When reviewing a design system rather than a surface, this distinction is the finding.

An enforceable rule has a frequency, a role ban, or a forbidden value:

- *Frequency* — "one accent moment per viewport-and-a-half"
- *Role ban* — "the secondary accent is never a CTA; it is jewelry"
- *Forbidden value* — "pure white only as inverse text inside the dark panel, never on the paper ground"

"Use sparingly" is unenforceable and therefore not a rule. Flag unenforceable guidance as a system gap.

## Tier 3 — the tell-list

Everything below is a **prompt for human attention**, never a gate, never scored. It has no systematic evidence behind it; see `reliability-envelope.md`.

Use it two ways: to decide where to look more carefully, and as input to the systematisation checks above. Never as a finding on its own.

**Commonly named tells, per-tool where reported:**

- Purple / blue-violet gradients. The 2025-era marker
- Default Inter, Roboto, Arial or a bare system stack used without a reason. Space Grotesk specifically is what models reach for when asked to be *distinctive*, which makes it the opposite
- Emoji used as icons or bullets
- `border-radius: 12px; border-left: 4px solid` as the default card
- The ghost card: a `1px` border *plus* a soft wide shadow on the same element as decoration. Pick one elevation language
- Over-rounding: radius ≥24px on cards, sections or inputs
- Nested cards — a bordered card inside another card
- Pure `#FFFFFF` on `#000000`
- Fabricated social proof: round-number stats, "Trusted by" rows, invented testimonials
- 3-column feature grids with generic icons; bento grids with filler cells
- Fake dashboards built from `<div>` rectangles, with red/yellow/green/blue callouts
- Hand-drawn SVG illustrations of people or scenes
- Decorative status dots, scroll cues ("Scroll to explore"), version-label eyebrows, section-number eyebrows
- Gradient text, glow-for-emphasis, decorative grid-line backgrounds, `repeating-linear-gradient` stripes
- Imitation material: CSS bevels, embossing, faux letterpress, fake foil, stamped-metal or chalk effects claiming a material the page never renders. Partly greppable (`box-shadow: inset` + gradient + border stacked on one element to fake relief) and judged in `craft-visual.md` under Depth
- A system display face — Impact, Arial Black, the platform sans — carrying the *display* voice on a surface with its own identity. Workhorse system stacks for body and UI are legitimate; the tell is a display role never sourced
- Uniform section-reveal: one identical fade-up entrance applied to every section
- Unsplash stock imagery where the brand needs its own
- The three current default *looks*, which matter more than any single element: warm-editorial (cream `#F4F1EA` family background + serif display + terracotta accent), near-black with a single acid accent, and the broadsheet (hairline rules, zero radius, oversized serif masthead)

**Detect the warm-neutral band by value, not just hex family:** OKLCH lightness 0.84–0.97, chroma <0.06, hue 40–100 reads as cream/sand/paper regardless of what the token is called. Token names are tells too: `--paper`, `--cream`, `--sand`, `--bone`, `--linen`, `--parchment`, `--ivory`, `--wheat`.

**The second-order reflex check.** Avoiding the first default and landing on the predictable alternative is the same trap one tier deeper. "Fintech, but not navy → terminal dark." "AI tool, but not SaaS-cream → editorial-typographic." If someone could guess the chosen family from the category *plus the anti-references alone*, it's still a reflex.

**Two rules that keep this honest:**

Any one of these can be a deliberate, correct choice. All of them together, on a surface whose brief called for none of them, is the finding — and the finding is *"nothing here was specified"*, which is a systematisation observation, not an aesthetic one.

The brief's own words always win, including when the brief explicitly asks for one of these looks. The rule is only: don't spend a *free* axis on a default.
