# Deck Craft

<p align="center">
  <img alt="Version 1.15.0" src="https://img.shields.io/badge/version-1.15.0-D33C21">
  <img alt="SWE skill: making" src="https://img.shields.io/badge/SWE_skill-making-434A55">
  <img alt="Gate assertions: 17 to 3" src="https://img.shields.io/badge/gate_assertions-17_to_3-756E60">
  <img alt="Blind panel: 2 families, 14 to 0" src="https://img.shields.io/badge/blind_panel-2_families_14_to_0-756E60">
  <img alt="License: MIT" src="https://img.shields.io/badge/license-MIT-A9A399">
</p>

A Claude Code plugin for slide decks: build, review, convert. **Self-contained: it needs no other skill installed.**

## Three targets, one body of craft

| Target | When | Output |
|---|---|---|
| **HTML** | Present it, share a link, open in a browser | One self-contained file, fixed 1920x1080 stage that scales and letterboxes rather than reflowing |
| **lecturn.deck/1 JSON** | A `.pptx` handoff, or an existing `.pptx` to read/diff/edit | Validated JSON, converted both ways by the stdlib-only `deckconv` |
| **Diolog templates** | ASX investor artifacts: results, 4C, AGM, board pack, roadshow, capital raising, IPO, investor day, ESG, M&A scheme, site visit | `lecturn.deck/1` assembled from 200 layouts in 27 families and 21 recipes, submitted to the deck producer |

The router picks the target from the *destination*, not the content. Each reference is self-contained, so only one is read per deck.

## What it carries

**Its own design layer** (`references/visual-craft.md`) rather than a dependency on a general design skill: how to consume a supplied `DESIGN.md` or token file as binding context; how to author a direction when no brand exists (scheme / formality / density, subject-mined palettes, a declared signature element, the swap test); typography sized for projection with tracking, leading and measure rules; colour strategy and accent budgets; five-vector hierarchy and cross-slide rhythm; anti-slop; and an accessibility floor calibrated for a projector rather than a monitor.

**Deck-specific narrative discipline.** The title sequence written before any slide, because the titles read in order are the deck's argument. Speaking-vs-reading density as an explicit fork. One idea and one focal point per slide. A named slide count treated as a contract. And the linear-flow usability rules a deck inherits from having no back button: the per-slide trunk test, recognition over recall, and an honesty gate on charts and claims that is compliance rather than taste in investor contexts.

**Verification that isn't ceremonial.** A per-slide gate while building, and one delivery pass at the end. Built on three rules: rendering an image is not seeing one; the question you bring to a capture determines what you find in it (ask "what is wrong with this?", never "is this done?"); and a clean gate means *no known defect is present*, never *verified*, reported as separate claims with a never-empty not-checked line.

**First-pass design resilience.** Pure deterministic SVG charts by default (eliminates external CDN failures), automated image downsampling and Base64 inlining for single-file portability, strict dual-theme contrast rules for dark bands, `IntersectionObserver` active slide tracking with sticky header offset guards, and clean card semantic discipline.

**A gate that cannot pass silently.** The preflight probe carries its own blocker/warning policy and a stated consequence for every finding, refuses a config key it does not recognise, and echoes its configuration back so the runner can prove the settings you asked for actually arrived. Only exit 0 is a pass: a probe that returned nothing, a config that did not land, a check that threw, and a run that examined zero slides each get their own exit code and their own refusal, because an absence of findings is not an absence of defects.

**Progressive direction-finding.** The template libraries on the machine are read as evidence, not menus: the bold pack's selection index before any `design.md`, two or three matching open-design systems, a named brand's portable design system. No bulk reads.

## Does it actually work

Half of the suite was run and half was not, so what follows is a report on the half that ran. Both records sit on disk under `skills/deck-craft/evals/results/`.

**The report card.** Seventeen structural assertions, each one an artifact check ("did the run produce X") rather than a rating, run over the same fixtures with the same flags against the version this replaces. The previous version passed **3 of 17**. This one passed **17 of 17**.

Some of what the previous version was doing while reporting a clean deck: a `--regulated` run printed PASS with all four disclosure checks unrun, a type-floor failure was computed and then ignored at exit 0, a misspelled config key was accepted so the probe silently ran on defaults, and a run that examined no slides at all still printed PASS.

Three of the seventeen rows pass on both sides, and the scorecard names them so nobody counts them as evidence: the clean-deck control, an empty-probe floor the previous version already held, and the regression guard over what it already did.

**The blind taste test.** Seven cases, each showing one input and two outputs from two versions of the same command-line checker, anonymised as Option A and Option B. Order was randomised per case from seed 1, with a deliberate 4 to 3 split so neither letter carried information, and no judge was told a skill existed or which option was newer. Two model families, Anthropic's fable-5 and Google's gemini-3.7, each picked this version on all seven cases: **14 verdicts to nil**, from both positions.

The tally is the less interesting half. Both families, having never seen each other's answers, nominated the same output as the worst thing in the whole bundle, which was a gate printing "PASS · 0 blockers across 0 slides" for a run that examined nothing. Gemini on the winner: it *"explicitly refuses to pass when zero slides match and provides actionable selector remediation, whereas Option B emits a false pass over a denominator of zero."*

**Two of the four judge families failed, and they are written up rather than dropped.** OpenAI's `gpt-5.6-sol` hit a usage limit with no other OpenAI lane configured on the machine, and xAI's `grok-4.6` was killed by a 900 second deadline with no output, its fallback harness out of usage. Neither was retried into the ground; both are retryable after 20 August 2026. So the panel is two independent families rather than four, and it is reported as two everywhere it comes up.

**What none of this establishes.** The scorecard is a record and not something you can re-run here: the previous version's snapshot was never committed, the runner's path to this version is hardcoded to the machine that ran it, and the raw rows behind the table were not kept, so only the rendered scorecard survives. Every graded assertion is about the preflight checker's behaviour, so nothing here says whether the decks this skill authors are any good. The three authoring prompts written to ask exactly that sit in `evals.json` with no outputs and no grading, and they point at paths outside this repository, which is the first thing to fix. And these are single runs, one per version per assertion and one judgement per family per case, so no number above is a rate.

The full tables, both judges' own words, the failed lanes and the rest of the caveats are in [EVALS.md](EVALS.md).

## Installation

```text
/plugin marketplace add fledgeling-co/fledgeling-plugins
/plugin install deck-craft@fledgeling-plugins
```

## Example invocations

```text
build a 9-slide investor update for ALFABS from these filings
turn this PRD into 10 slides for the engineering all-hands
make me a pptx board pack from the Q3 numbers
this deck looks AI-generated - fix it
```

## License

MIT
