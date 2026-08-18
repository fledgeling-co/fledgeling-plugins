# Evidence — where these numbers come from, and where they disagree

Every rule in this skill that carries a number is either **measured on this machine**, **derived from
a published standard**, or **taken from a regulator's own text**. This file records which, so a later
maintainer editing `bodyFloor: 24` knows whether they are adjusting a taste value or breaking a
closed-form derivation. It also records the places the evidence contradicts itself, because a
skill that silently resolves a conflict has decided something on the reader's behalf without saying so.

The research corpus is committed under `docs/deep-research/` — three independent backends, 67 cited
sources across 46 registrable domains, 3% source overlap. Fabrication check on all three: **0
fabricated citations of 69 checked, 0 dead links.** Where a claim below has one backend behind it,
it says so; one backend is uncorroborated rather than wrong.

---

## 1. The type floor

**`bodyFloor: 24` on a 1920 canvas is derived, not chosen.** `investor-relations.md` §1.1 solves it
from a minimum visual angle at a stated viewing ratio: `font_px = (arcmin × VR) / 2.228`.

The corpus corroborates the method and disagrees on the floor:

| source | absolute floor | comfortable | found by |
|---|---|---|---|
| Extron, *Font Size and Legibility for Videowall Content* | 10 arcmin ("barely legible, may cause eyestrain") | 15–20 arcmin | xai and perplexity (one source, two backends) |
| ISO 24509:2019 via a legibility calculator | 16 arcmin | 20–22 arcmin | gemini |
| this skill, citing ISO 9241-303 | 16 arcmin | — | — |

**Hold this loosely: the two backends name different ISO standards.** This skill cites **ISO
9241-303**; gemini's report cites **ISO 24509:2019** ("Ergonomics — Accessible design — Method for
estimating minimum legible font size"), which is arguably the more directly on-point document. Both
are real standards and both were reached through a secondary calculator rather than the standard's
own text, so neither citation has been read at source. The *number* is stable across them at 16
arcminutes; the attribution is not. Treat 24px as well-supported and the standard number as
unverified until someone reads the standard.

Two independent framings worth having, neither currently in the skill's arithmetic:

- **Extron's field rule**: 1 inch of on-screen text height per 15 ft of maximum viewing distance.
  At 30 ft that is 2 inches ≈ 74px ≈ 58pt in authoring tools. A useful sanity check on a room, and
  it makes the same point as the skill's `≥44px for a projected boardroom deck`.
- **The 8H rule**: the farthest viewer sits no more than 8× the screen height away *(xai only,
  presentationguild.org — a practitioner source)*.

**A conflict to keep scoped rather than resolve.** xai's report recommends **≤3 type sizes per
slide**. This skill's `slot-contract.md` requires **≥4 distinct font sizes per deck**, and its own
A/B measured 19 distinct sizes on the better deck against 13 on the worse one. These are not in
conflict once scoped — few sizes *per slide*, a full ramp *per deck* — and the skill's own
measurement is the stronger evidence for the deck-level claim, being a direct observation rather than
a practitioner guideline.

## 2. Charts and axes

**Zero-baselined bars.** The evidence is strong and comes from three independent lines:

- Yang et al., *Anchors and ratios to quantify and explain y-axis distortion effects*
  (psycnet.apa.org, 2025): truncation causes observers to **overestimate** differences, expansion at
  either end causes them to **underestimate**, and the effect survives moderate truncation. Bar
  height and area act as anchors, which is why bars specifically cannot tolerate it. *(perplexity)*
- Correll, Bertini and Franconeri, *Truncating the Y-Axis: Threat or Menace?*, CHI 2020
  (DOI 10.1145/3313831.3376222): truncated baselines **systematically bias judgments even when the
  axis labels are clearly visible**, and most severely for lay audiences making rapid assessments.
  *(perplexity; the DOI is registered, the publisher 403s an automated fetch)*
- Schober et al., *Choice of y-axis can mislead readers* (PMC7419489): default the y-axis to 0 for
  ratio variables and justify any departure explicitly. *(perplexity)*

**The skill's own citation for this rule is unverified.** `deck-review.md` item 10 attributes it to
"Long & Kay 2024" with a distortion formula of `100/(100−t)`. Nothing in 67 sources across three
backends corroborates that attribution. The *claim* is well-supported by the three sources above —
including the specific point that footnotes do not cure truncation — so the rule stands; the
citation should be replaced with one of the three above rather than repeated.

**`ratioDrift <= 0.02` is defensible and slightly stricter than the published bound.** Tufte's Lie
Factor — the ratio of the effect shown to the effect in the data — is conventionally held inside
0.95–1.05 *(gemini, infovis-wiki and edwardtufte.com)*. A ratio drift of 0.02 across a bar group is
tighter than that. Note that the Lie Factor's own arithmetic is contested: Tufte computes it by
dividing percentages, `(b−1)/(a−1)`, while others argue for `b/a` *(gemini, edwardtufte.com)*. The
gate uses neither, measuring `length / value` constancy across a group, which is why the check states
its own method rather than claiming a Lie Factor number.

**Dual axes are the misleader this skill was missing.** Added 18 Aug 2026 on the strength of:

- *Misviz*, "Is this chart lying to me? Automating the detection of misleading visualizations"
  (arXiv 2508.21675): defines truncated axis as any sorted vertical axis starting above 0, plus
  inverted axes, dual axes, inconsistent tick intervals, inconsistent binning and inappropriate
  temporal ordering — and **detects them from axis metadata rather than from the underlying data**,
  which is precisely what a DOM probe can reach. This is the method the new check copies.
  *(perplexity)*
- gemini reports dual axes reducing viewer accuracy to **0.161** against a 0.808 non-misleading
  baseline, with truncated bars at 0.610 — so dual axes measure as the *worse* distortion.
  **Single-sourced (escholarship, a citation that 403s), so the numbers are held loosely.** The
  direction is independently corroborated by perplexity's discussion of false visual correlation,
  and the direction is what the check rests on.

**Length beats area, and by a measured margin.** Length perception is near-linear (R² = 0.997);
area is not (R² = 0.636) *(gemini, single-sourced)*. Just-noticeable-difference work adds that bar
spacing materially affects discrimination — closer bars hide small differences *(perplexity,
computer.org)*. Together these support "bar length is the encoding" and the preference for bar and
line over pie and bubble, which one efficacy study measured as lower search time and more efficient
retrieval *(perplexity, sciencedirect)*.

## 3. Regulated disclosure

This is the best-sourced block in the corpus: primary regulator text, found independently by two
backends.

**SEC Regulation G and Item 10(e) of Regulation S-K** require any non-GAAP measure to be accompanied
by the most directly comparable GAAP measure **with equal or greater prominence**, plus a
**quantitative reconciliation**. **ASIC RG 230** requires the same of non-IFRS information: clear
labelling, reconciliation where material, equal prominence, and explanation. *(xai and perplexity,
both from sec.gov and asic.gov.au)*

**The December 2022 Compliance & Disclosure Interpretations, Question 102.10, are what made the
per-slide check possible.** They enumerate what "more prominent" means, and several of the examples
are mechanical rather than interpretive: the non-GAAP measure presented **before** the GAAP one, the
GAAP measure **omitted**, the non-GAAP measure styled in **bold or a larger font**, a **chart for the
non-GAAP measure with no corresponding visual** for the GAAP one, and superlatives such as "record"
or "exceptional" applied to the non-GAAP measure without equal characterisation of the GAAP one.
*(perplexity, from sec.gov and Jones Day)* The gate implements the first three; the chart-parity and
superlative tests are available and unbuilt.

**Forward-looking measures are treated differently, and getting this wrong is a false finding.**
Reconciliation may be omitted for a forward-looking non-GAAP measure only where it is impracticable,
**provided the unavailable information and its probable significance are disclosed**. *(xai and
perplexity)* This is why the check tests a forward-looking slide for that disclosure rather than for a
reconciliation it is not required to carry.

**Non-GAAP measures are the second most commented topic in SEC comment letters, year after year**,
alongside MD&A *(perplexity, finrep.ai — a secondary source)*. Volume has fallen since 2019–2021 but
letters have become more targeted.

**Both regimes reach investor presentations, not just filings.** Regulation G applies to any public
disclosure containing a non-GAAP measure, earnings releases and investor presentations included
*(perplexity)*. That is the reason `--regulated` exists as a mode rather than a filing-only concern.

## 4. Why a gate must distinguish "clean" from "did not run"

perplexity's report arrives independently at the design this rebuild implements, which is the
strongest corroboration in the corpus because nothing in the brief described the mechanism:

> a preflight gate should explicitly distinguish between three states: passed checks (where specific
> rules were executed and no defects found), failed checks (where rules detected defects), and
> unexecuted checks (where rules could not run due to missing inputs or unsupported content types).
> … so that a "clean pass" is not conflated with "no checks run" or "some checks run."

It names two failure modes the rebuild now refuses by construction. **Zero-over-nothing**: a check
that runs against an empty set and reports no violations. **Partial coverage**: a chart pasted as a
static image exposes no axis metadata, so the axis check silently does not apply to it — which is
exactly what `chartGroupsUnverified` reports, and why it is now printed with its denominator.

**One claim from this area is deliberately not used.** gemini reports, at High Confidence, that
unattended AI agents fabricate success at **25.05%**, falling to **0.95%** under a deterministic
finite-state gate, citing arXiv 2606.11688. It is not repeated in this skill, for three reasons: it
is single-sourced; the surrounding citations in that section are a cluster of unrelated agent-CLI
tooling that reads as retrieval noise; and xai's report states directly that **no post-2019 studies
of silent-pass rates in presentation QA gates were located**, which is a negative finding about the
same literature. The *principle* — that a gate outside the model's own claim is what makes the claim
checkable — is this skill's existing doctrine and needs no borrowed number.

Relatedly, gemini presents `exit 3` as an industry convention for a zero-denominator error, citing a
single GitHub repository. It is not a convention. This runner uses 4, 5, 6 and 7 for four distinct
not-a-pass conditions, and documents them, which is the part that matters.

## 5. Slide structure and retention

**Slides can compete with the speaker, and it has been measured.** Savoy, Proctor and Salvendy found
students retained roughly **15% less of the information delivered verbally** when lectures were
PowerPoint-supported, while preferring PowerPoint *(perplexity, sciencedirect — 403 to an automated
fetch)*. This is direct evidence for the speaking-versus-reading fork in §2 and for one idea per
slide: a dense slide does not merely fail to help, it takes from the spoken half.

**Assertion-Evidence beats bullets, on a real study.** A declarative sentence headline supported by
dominant visual evidence outperformed conventional bullet slides on comprehension, misconceptions,
delayed recall and perceived cognitive load, tested on 110 engineering students at Penn State
*(gemini, single-sourced)*. High text volume correlates negatively with comprehension; number of
images and maximum font size correlate positively.

**This partly cuts against §4's advice, and the tension is real.** §4 says pick one grammatical style
— noun phrase or declarative — and hold it, treating the choice as stylistic. The AE evidence says
declarative-plus-evidence is measurably better than a bulleted alternative. Both can hold: AE argues
for choosing the declarative option on any slide carrying evidence, and against text-only slides
generally; §4's consistency rule then applies within that choice. What neither supports is a deck of
declarative titles with no evidence under them, which is the punchline-title failure §4 already bans.

**Available and unbuilt, from this section:** all-caps passages slow word recognition by removing the
ascender/descender variance readers use *(perplexity, trainingindustry.com)* — mechanically checkable
by counting uppercase characters per run, and deliberately not gated here because decks legitimately
set eyebrows in caps and the check would need a length exemption to avoid becoming noise. WCAG
contrast floors (4.5:1 normal, 3:1 for large text at ≥18pt regular or 14pt bold) and WCAG 2.2 text
spacing thresholds are both computable and both currently prose rather than gate.

**Weakly sourced, direction only.** The 60-30-10 surface split and a "15% accent saturation" ceiling
come from design-studio blogs rather than measurement *(gemini, amaca.design and letsgroto.com)*.
They point the same way as this skill's accent rule, which is stricter and backed by its own
measured A/B, so the rule stands on the measurement rather than on these.

---

## What this file is not

None of the above makes a passing gate a verification. Every check in `deck-preflight.js` was written
after someone met the defect it catches, so the set is structurally blind to the defect nobody has
met yet — and the sourcing above raises confidence in the *thresholds*, not in the *coverage*. The
honest report shape in `references/deck-review.md` exists because those are two different claims.
