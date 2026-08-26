# Changelog

## 0.1.0 - 2026-08-27

Initial release of `eli5`, a rebuild of the skill of the same name by Thariq Shihipar
in Anthropic's `claude-plugins-community` (MIT). The original is nine lines; this adds
the teaching research underneath it and a gate that fails.

### The pipeline

Five phases: deconstruct to the causal invariant and the misconception worth defeating;
map a structure-mapping analogy carrying a stated boundary; stage three disclosure tiers
around a Predict-Observe-Explain beat; draw against a declared geometry contract; gate.

### Grounded in a four-backend research panel

Commissioned across Gemini, Perplexity, xAI and Claude ($6.20; a fifth lane died at
startup for $0 and is recorded). Both load-bearing reports pass citation verification:
68 URLs checked, 0 fabricated, 0 dead. All four reports ship in `docs/deep-research/`,
and `references/evidence.md` traces every rule to a source, keeps the four places the
panel disagreed as open questions, and names the gaps that bound what the skill claims.

The rules that changed the most:

- **The analogy boundary**, on 4-of-4 convergence. Analogy-induced misconceptions are
  durable; the named mitigation is an explicit limits segment, reachable by tier 2.
- **The prediction beat.** Dragging a slider is Active engagement (d~0.20-0.40 over
  passive); committing a guess first is Constructive (d~0.40-0.60 over active).
- **Three tiers, no nesting**, because nested disclosure buries the caveats readers most
  need.
- **The geometry contract**, because models predict coordinate tokens and never render
  what they wrote, so valid SVG draws arrows through text.

### `scripts/lint_explainer.py`

20 checks across containment, geometry, interaction and pedagogy; exit 1 on any failure.
`--self-test` proves all 19 rules can fail against broken fixtures before a pass counts,
and caught a trailing `\b` in the network-call regex that made `fetch(` unmatchable.

### Proven against the original

Six hard topics, both skills, same model. Structural gate: 29 failures to 1. Blind panel
of three out-of-family judges in seeded-random order, never shown either skill: **18 of
18**. Honesty-about-limits and register were unanimous at 14-0.

The eval it first lost is in `EVALS.md` with the fix and the flip: an artifact with 25
controls and zero JavaScript, caught by the gate and independently diagnosed by a blind
judge that never saw the gate. Re-run and re-judged, 3 of 3 switched.

Where the original wins is in its own table: 352 words against 2,667.

### Two rules that came from grading the arms

- Tier 1 carries a 150-word budget, with a `length-budget` check. Progressive disclosure
  that front-loads nothing is a long document with headings.
- Never ship a dead control. A page that invites an action and does nothing is worse than
  an honestly static one.

### Brand

Cut-face icon at 1024, 256 and 128 with its layered SVG master and build script; an
`audit.html` scoring all four takes including the three that lost; a 3200x1040 banner
composed from the icon's own constants. LPIPS could not run (torch absent), so the
material rounds were judged by eye plus WCAG contrast, and the sheet says so.
