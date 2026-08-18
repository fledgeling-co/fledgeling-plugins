# Deck Craft

A Claude Code plugin for slide decks — build, review, convert. **Self-contained: it needs no other skill installed.**

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

**Verification that isn't ceremonial.** A per-slide gate while building, and one delivery pass at the end. Built on three rules: rendering an image is not seeing one; the question you bring to a capture determines what you find in it (ask "what is wrong with this?", never "is this done?"); and a clean gate means *no known defect is present*, never *verified* — reported as separate claims with a never-empty not-checked line.

**First-pass design resilience.** Pure deterministic SVG charts by default (eliminates external CDN failures), automated image downsampling and Base64 inlining for single-file portability, strict dual-theme contrast rules for dark bands, `IntersectionObserver` active slide tracking with sticky header offset guards, and clean card semantic discipline.

**A gate that cannot pass silently.** The preflight probe carries its own blocker/warning policy and a stated consequence for every finding, refuses a config key it does not recognise, and echoes its configuration back so the runner can prove the settings you asked for actually arrived. Only exit 0 is a pass: a probe that returned nothing, a config that did not land, a check that threw, and a run that examined zero slides each get their own exit code and their own refusal, because an absence of findings is not an absence of defects.

**Progressive direction-finding.** The template libraries on the machine are read as evidence, not menus — the bold pack's selection index before any `design.md`, two or three matching open-design systems, a named brand's portable design system. No bulk reads.

## Installation

```text
/plugin marketplace add DiologIR/diolog-plugins
/plugin install deck-craft@diolog-plugins
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
