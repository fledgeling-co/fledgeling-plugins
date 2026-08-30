# Evidence — what each change rests on

Every structural change in this skill traces to a measured result or a documented
failure in the predecessor. This file is the audit trail. Where a claim came from
a run, the command is here so it can be re-run.

The deep-research corpus that informed the design sits in `docs/deep-research/`,
exported in full with its source registries.

---

## 1. The series palette failed a perceptual gate in both modes

**Claim.** The predecessor's five hand-picked "desaturated, editorial-tone"
series colours cannot do the identity work a multi-series chart asks of them.

**How it was measured.** The data-visualisation method's own validator, run
against the predecessor's `style-guide.md` series tokens:

```bash
python3 scripts/validate_palette.py "#7c8f6f,#5e7a9b,#b8915a,#9c6b50,#6e6479" --mode light
python3 scripts/validate_palette.py "#9caf8f,#82a0c0,#d3ad7a,#b88670,#8d8298" --mode dark --surface "#2d3142"
```

**Result (light), exit 1:**

| Check | Verdict |
|---|---|
| Lightness band | PASS |
| Chroma floor | **FAIL** — 5 of 5 below 0.10 (0.035–0.086) |
| CVD separation | PASS — worst adjacent ΔE 8.5 protan |
| Normal-vision floor | **FAIL** — worst adjacent ΔE 10.3, floor 15 |
| Contrast vs surface | WARN — mustard 2.83:1 |

**Result (dark), with the accent included:** lightness band FAIL (4 of 6 outside
the band), chroma floor FAIL (5 of 5), normal-vision floor FAIL at ΔE 9.1.

**Reading.** The chroma failure is what "desaturated and editorial" means once
measured: a hue below the chroma floor has stopped encoding identity and is a
grey with a tint. The normal-vision failure says full-colour readers struggle
with the worst pair — this is not only a colour-vision-deficiency finding.

**What changed.** `references/series-palette.md` carries a replacement derived by
snap-to-passing on the same five hue families: step for chroma and band, then
enumerate orderings and keep a passing one, then re-step the slot the second mode
rejects. Both modes now exit 0, worst normal-vision ΔE 22.8 light / 23.2 dark.

**Held loosely.** The floor of 15 and the ΔE ≥ 8 CVD target come from the
data-visualisation method as shipped, calibrated to the Machado–Oliveira–Fernandes
2009 simulation at severity 1.0. The simulation model is part of the standard
rather than an implementation detail; a different model would move the numbers.

---

## 2. Twenty verifier scripts were cited but could not be run from an install

**Claim.** The predecessor's executable rigour was available to its repository
and not to the agent doing the drawing.

**How it was measured.** Counted the verifiers in the source repository against
those shipped inside the skill directory, then resolved every script path cited
in `SKILL.md` and `references/*.md` against the installed layout.

```
repo verifiers (verify-*.py, lint-*.py):   22
scripts shipped inside the skill:           3   (self_check, drawio_extract, mermaid_extract)
distinct script paths cited in the docs:   20
of those cited, present in an install:      0
```

Four passages gate a check behind the phrase "from a repository checkout".

**Reading.** An installed agent following the prose is told to run
`verify-geometry.py`, `verify-treemap.py`, `verify-dumbbell.py` and seventeen
others, and has none of them. The rules those scripts enforce degrade to prose
exactly where they were meant to be executable. Nothing warns anybody: the
checklist item can be reported as satisfied by reading the markup.

**Why it was fixable.** Every verifier is pure Python standard library — zero
third-party imports across all 22. The blocker was a path assumption
(`ROOT = Path(__file__).resolve().parent.parent` plus
`skills/diagram-design/assets`), not a dependency.

**What changed.** Twelve output-verifiers were ported into `scripts/` with the
path assumption rewritten to the installed layout, and the checks are named in
SKILL.md §8 as commands with exit codes rather than as prose. Verified against
the skill's own 155 assets from the install layout:

```
verify-geometry     148/148 pass    verify-treemap      OK, 3 files
self_check          148/148 pass    verify-sankey       OK, 3 files
verify-slopegraph   OK, 3 files     verify-beeswarm     OK, 3 files
verify-bubble       OK, 3 files     verify-bump         OK, 3 files
verify-ridgeline    OK, 3 files     verify-skin-polarity OK, 155 files
verify-dumbbell     OK (formula)    verify-motion       OK (--shipped)
```

The ten repo-maintenance gates (`verify-docs-sync`, `verify-plugin-package`,
`lint-skin`, `lint-render`, screenshot freshness and the import-structure
verifiers) were deliberately not ported: they check the repository, not a
generated file, and would be noise inside an install.

**Method note.** Two early runs of these gates were piped through `tail`, so the
`EXIT=` line reported `tail`'s status rather than the gate's. That is the exact
failure mode the marketplace's own build gate warns about, it happened here
during this rebuild, and it is why SKILL.md §8 and the taste gate both say to
read the exit code rather than the output.

---

## 3. The two skills disagreed about what colour is for

**Claim.** The merge is not additive — the predecessor and the
data-visualisation method hold incompatible defaults, and the conflict has to be
resolved rather than concatenated.

**The disagreement.**

| Question | Diagram system | Data-viz method | Resolved as |
|---|---|---|---|
| Default accent count | 1–2 focal, everything else recedes | as many slots as there are series | Diagram rule holds for diagrams; charts with ≥2 series go to the validated palette |
| Series colour | desaturated editorial tones | measured, gated, fixed order | Gate wins; hue families kept, steps and order changed |
| Hero figure typeface | Instrument Serif owns titles | never a serif — reads off-brand | Serif kept, scoped to the editorial page register and stated as a deliberate divergence |
| Legend placement | horizontal strip at the bottom | present for ≥2 series, position unspecified | Both — bottom strip, and mandatory at ≥2 series |
| Gridlines | faint hairlines | solid hairlines, never dashed | Merged; dashing reserved for meaning (optional, async, transit) |
| Interaction | static by default, motion opt-in | hover layer is part of the deliverable | Static default holds for diagrams; HTML charts get the hover layer, still rendering complete meaning without JavaScript |

**Reading.** The serif hero figure is the one place the merged skill knowingly
departs from the data-visualisation method. The method's reasoning is that a
display face on a dashboard number reads as off-brand decoration; this skill's
output is an editorial page where the serif is the brand. Recorded as a
divergence, not an oversight.

---

## 4. What the predecessor already did well, and is unchanged

The comparison would be dishonest without this. Both source gates pass 148/148
on the predecessor's own shipped examples:

```
self_check.py      PASS=148 FAIL=0
verify-geometry.py PASS=148 FAIL=0
```

So the weakness was never in what it checked — it was in who could run the check.
Kept intact: all 39 layout grammars and their type references, the six connector
rules, the semantic-pattern layer, the complexity budgets, the accessible-SVG
contract, the four-dial output spec, the draw.io and Mermaid import pipeline with
its fidelity ledger, the profiles and onboarding flow, and the three-variant
template set.

---

## Attribution

The diagram half of this skill is a rebuild of **diagram-design** by
**Cathryn Lavery** (<https://github.com/cathrynlavery/diagram-design>), MIT
licensed. The 39 layout grammars, the connector rules, the semantic patterns, the
import pipeline and the verifier implementations are that project's work, ported
and extended here. The chart method it merges with is the data-visualisation
skill that ships with Claude Code, whose validator and six-checks method are used
as the perceptual gate.
