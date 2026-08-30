# Research findings — the panel, and what changed because of it

A four-backend Dossier deep-research panel ran against one brief covering
graphical perception, colour thresholds, accessibility, automated linting,
LLM failure modes and evaluation protocols. Three members completed; the fourth
(Antigravity CLI) refused to start on a binary-identity check and cost nothing.

Full reports and their source registries are in `../../docs/deep-research/`.

| Lane | Model | Sources | Fabrication check | Cost |
|---|---|---|---|---|
| OpenAI | gpt-5.6-sol | 81 | **PASS** — 0 fabricated, 0 dead | $9.00 |
| Gemini | deep-research-max-preview | 72 | ATTENTION — 1 of 72 dead (a Vega-Lite schema URL with a stray backtick) | $7.00 |
| Claude Code CLI | local, subscription | 27 | not run (report written to disk, recovered) | $0.00 |
| Antigravity CLI | — | — | did not start | $0.00 |

Report the panel's cost honestly: **$16.00 committed at band top, reconciled to
$16.00 actual.**

---

## What changed in the skill because of the panel

These are the findings that contradicted what was already built. Each became a
rule rather than a citation.

### 1. A palette-level colour check is not sufficient — mark geometry moves the threshold

**Finding.** Colour difference required for discrimination increases as mark size
decreases; points are more sensitive than elongated bars and lines. Szafir's
TVCG 2018 models give per-mark, per-size thresholds — a 6px scatter point needs
ΔE 8.37 on L\* but 19.46 on b\*, and a 2px line needs 19.47 on b\*. Both the
OpenAI and Claude lanes reported this independently.

**Why it matters here.** The validator this skill inherits checks the palette in
isolation. A palette that passes can still paint marks a reader cannot
discriminate, because a 2px line and a 24px bar are not the same perceptual
problem.

**What changed.** `series-palette.md` now carries a mark-size caveat: the gate is
necessary, not sufficient, and thin marks (2px lines, small scatter dots) need
either a heavier mark or secondary encoding regardless of a passing palette. The
per-mark thresholds are recorded as the direction of travel rather than encoded,
because encoding them needs the smallest rendered dimension per series read out
of the SVG, which is a verifier this skill does not yet have. Named in
`Known limits` rather than claimed.

### 2. "Bars must start at zero, lines are fine" is too simple, and axis-break glyphs do not rescue a truncated bar

**Finding.** The truncation effect is large and persistent: across five studies,
83.5% of participants judged differences in truncated charts as larger, and
warning them reduced but did not eliminate it. The Claude lane reports the
mitigation test directly — broken-axis and gradient treatments at F(2,60)=3.1,
p=0.05, which is not a fix. A 2026 CHI study adds task dependence: truncation
increases ratio-calculation error but can *improve* value retrieval or filtering,
and direct labels materially mitigate.

**What changed.** `chart-honesty.md` now states the scoped rule rather than the
dogma. A non-zero baseline is an error for magnitude, ratio and proportional
comparison; it is permitted only with direct labels on every mark, a conspicuous
break indicator, the full numeric range shown, and a declared
retrieval/filtering task. For line and scatter, a non-zero domain is a warning
rather than a failure provided the axis minimum, maximum, ticks and units are
visible. And a break glyph is explicitly **not** accepted as remediation on its
own, which is the part that contradicts the intuition.

### 3. Alt text has an inverted preference, and an LLM optimising for "good alt text" gets it backwards

**Finding.** Blind readers rank contextual/domain-insight descriptions **least**
useful; sighted readers rank them **most**. 63% of blind participants were
emphatic that descriptions must not editorialise. This is a systematic,
checkable failure direction rather than a matter of taste.

**Why it matters here.** The predecessor's `<desc>` rule says "describe the
content, not the geometry", which is right, and stops one step short: a model
told to write a useful description will happily add interpretation, which is the
error blind readers named.

**What changed.** SKILL.md §9 and `taste-gate.md` now say the `<desc>` states
what is shown and does not editorialise, interpret or draw the conclusion for
the reader. The chart's takeaway belongs in the title or the surrounding prose,
where a sighted reader also has to read it.

### 4. Deterministic pre-checks are what make a model judge usable

**Finding.** VisEval's browser-simulated layout check scored 100% against
experts. Its GPT-4V readability rating reached SRCC 0.843 **with** those
deterministic checks and 0.507 without: roughly half the rank correlation for
about half the tokens.

**What changed.** This is the strongest external support for the skill's central
structural decision — shipping twelve runnable gates rather than citing them.
Recorded here because it justifies the architecture, and because it says the
gates should run *before* any judged or eyeballed pass, which is now the order
SKILL.md §8 states.

### 5. Hidden hallucinations: execution success is not data fidelity

**Finding.** The most dangerous LLM failure is a chart that renders perfectly
from mis-extracted numbers. DeepChart scored an execution rate of 78.2% against
a visual-accuracy score of 44.7% on the same set. VisEval found a 6% direct
hallucination rate in rendered data despite 95.4% execution success. The
mitigation both lanes name is a staged extract → reason → visualise pipeline
with the intermediate data written down and auditable.

**What changed.** `chart-honesty.md` gains the rule that the numbers a chart
draws must be traceable to what was supplied — stated values in the table view,
derived values shown as derived. This skill does not adopt a full ERV pipeline
with a typed intermediate schema; that is a structural change beyond this
rebuild, and it is recorded as the next thing worth doing rather than claimed.

---

## Where the panel disagreed

Carried forward as unresolved rather than silently reconciled.

**The categorical ΔE threshold.** OpenAI's lane recommends minimum pairwise
ΔE₀₀ ≥ 10, from a six-class map experiment (211 online plus 32 lab participants)
where ΔE₀₀=10 gave >95% accuracy and ΔE₀₀=2 gave <80%, and explicitly tags it as
scoped rather than universal. Gemini's lane recommends ΔE > 10 for categorical
pairs but sets the **CVD** failure threshold at ΔE < 5. This skill's inherited
validator uses OKLab ×100 with a target of 8 and a floor of 6 under CVD, plus a
normal-vision floor of 15.

These are three different metrics in three different spaces, so the numbers are
not directly comparable, and converting between them is not something either
report licenses. What they agree on: a single palette-level number cannot
guarantee separation across mark types, backgrounds and displays, and redundant
encoding stays mandatory even when the threshold passes. The skill keeps its
inherited thresholds — they are what the shipped validator actually computes —
and records that the published evidence is scoped rather than universal.

`<INSUFFICIENT_EVIDENCE>` from the OpenAI lane, quoted because it is the honest
position: no corroborated peer-reviewed evidence establishes a universal ΔE
threshold guaranteeing categorical separation under simulated protan, deutan and
tritan vision across chart types, mark sizes, backgrounds and displays.

**The CVD simulation model.** Gemini's lane names Viénot 1999 and Brettel 1997
as the empirical standards and treats Machado 2009 as also acceptable,
particularly for anomalous trichromacy. OpenAI's lane and the shipped validator
both use Machado at full severity. Unresolved, and it matters: the thresholds
are calibrated to the model, so the model is part of the standard.

**Chart-form ranking.** Cleveland and McGill's ordering is broadly replicated but
not stable pair-by-pair; later work found area worse than angle, and did not
establish angle as reliably worse than length. Gemini's lane cites hierarchical
modelling suggesting only 3–4 statistically distinct accuracy tiers. Both lanes
land in the same place for engineering purposes: treat position and length as the
primary quantitative encodings and the rest as a partial ordering, which is what
`choosing-a-form.md` does.

---

## What the panel could not answer

- **No published label-occlusion threshold exists.** VisEval validates a *binary*
  overlap check, so zero-tolerance plus an OCR round-trip is the defensible
  design; inventing a percentage would be fabrication. `verify-geometry.py`
  already implements the binary form.
- **No benchmark exists for diagram-as-code substrates.** Every LLM chart
  benchmark targets Python plotting or Vega-Lite. Whether findings transfer to
  hand-authored SVG is plausible and unmeasured.
- **Layout engines.** Gemini's lane recommends delegating spatial coordinates to
  a Sugiyama implementation (Dagre, ELK) rather than having a model place nodes,
  on the grounds that LLM spatial reasoning fails. This skill deliberately
  hand-authors coordinates, because reproducing a layout engine's output is one
  of its named anti-patterns and the editorial layout is the product. The
  tension is real and unresolved: the finding is about reliability, the skill's
  position is about craft, and no evidence here settles which wins for
  hand-authored editorial diagrams.
