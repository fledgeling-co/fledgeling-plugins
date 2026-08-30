# The taste gate — what no script can see

Run before producing any visual. The twelve checkers in `scripts/` catch what is
computable; this catches what isn't. Both are required.

## Form fit

- [ ] Is this a chart, a diagram, or neither? (`choosing-a-form.md`)
- [ ] Would a table or a paragraph do the same job better? If yes — don't draw.
- [ ] If behaviour is load-bearing, was one semantic pattern chosen *before* the
      visual type, and `semantic-patterns.md` loaded?
- [ ] Right form for the data's job, not the first form the request named?
- [ ] Type reference loaded before drawing?
- [ ] Form, size preset, and planned cuts stated before drawing — confirmed, or
      assumptions noted beside the deliverable?
- [ ] If this is an import: format, size, detail and audience dials set;
      `viewBox` and type ramp match the preset; fidelity ledger ready to report?

## The remove test

- [ ] Can any node come out and the reader still understand?
- [ ] Can any two nodes merge? (Do they always travel together?)
- [ ] Can any arrow come out? (Is the relationship obvious from layout?)
- [ ] Can any label come out? (Does shape or position already say it?)

## Signal

- [ ] Accent on ≤2 elements? If more, which actually deserve focal status?
- [ ] Legend covers every type used — and nothing extra?
- [ ] Inside the type's complexity budget?
- [ ] For a chart with ≥2 series: legend present, and identity not resting on
      colour alone?

## Chart honesty

Only for quantitative output. Full rules in `chart-honesty.md`.

- [ ] Length encodings (bar, column, area) start at zero?
- [ ] No second y-axis?
- [ ] One shared scale per axis, and both ends of any paired mark labelled?
- [ ] Area encodes by area, not by radius?
- [ ] Sampled data drawn as polyline, not smoothed?
- [ ] Gaps in the data drawn as gaps?
- [ ] Missing values disclosed rather than imputed or silently dropped?
- [ ] Row order stated (by endpoint, signed change, absolute change, or a
      supplied order)?
- [ ] No more significant figures than the measurement carries?
- [ ] Multi-series palette validated — and the **exit code** read, not the
      piped output?
- [ ] Thin marks (2px lines, small dots) carrying identity given a heavier mark
      or secondary encoding, since a passing palette does not cover them?
- [ ] Every drawn value traceable to the source; derived values shown as derived?
- [ ] If a length encoding has a non-zero baseline: direct labels on every mark,
      a break indicator, the full range visible, AND a declared retrieval task?
- [ ] Table view present?

## Technical

- [ ] `<svg>` carries `role="img"` and a resolving `aria-labelledby`?
- [ ] `<title>` is the first child, before `<defs>`; both `<title>` and `<desc>`
      filled?
- [ ] IDs prefixed per diagram and variant — never bare `title` / `desc`?
- [ ] `<desc>` describes the content, not the geometry?
- [ ] `<desc>` states what is shown without editorialising, interpreting, or
      drawing the conclusion for the reader?
- [ ] Arrows drawn before boxes?
- [ ] Every off-axis connector a rounded elbow — no diagonal slants?
- [ ] Every arrow label masked, with a visible 6–10px gap above its stroke?
- [ ] No two connectors overlapping, sharing a path, or hiding one another?
- [ ] Shared edges fanned, ≥12px between attach points?
- [ ] No connector behind a non-endpoint box, except the unavoidable case —
      dashed, labelled at the visible end?
- [ ] No label mask overlapping a node drawn after it?
- [ ] Legend a horizontal bottom strip, not floating?
- [ ] No vertical `writing-mode` text?
- [ ] `viewBox` expanded ~60px for the legend strip?
- [ ] Every font size, coordinate, width and gap divisible by 4 — except data
      coordinates, which round rather than snap?
- [ ] `python3 scripts/self_check.py <file>` exits 0?
- [ ] `python3 scripts/verify-geometry.py <file>` exits 0?
- [ ] The type's own verifier run, where one exists?
- [ ] If animated: complete static frame, reduced-motion honoured, controller
      copied verbatim from `assets/template-motion.html`, `verify-motion.py`
      exits 0?

## Typography

- [ ] Brand match uses exact public families and weights, verified via
      `getComputedStyle`; fallbacks disclosed?
- [ ] Human-readable names in sans, not mono?
- [ ] Technical sublabels (ports, commands, URLs, field types) in mono?
- [ ] Page title in the serif; italic serif reserved for annotation callouts?
- [ ] No JetBrains Mono anywhere?
- [ ] Hangul at 12px or larger, with the Korean stack extended on that `<text>`?
- [ ] Large standalone numbers in proportional figures, `tabular-nums` only where
      columns align?

## Before handing it over

- [ ] Every gate that applies actually **run**, with its exit code read?
- [ ] Fidelity ledger reported if anything was cut?
- [ ] Assumptions stated where the user wasn't reachable to confirm?
