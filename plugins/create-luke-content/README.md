<div align="center">
  <img src="assets/banner.png" alt="create-luke-content banner" width="800" />
</div>

<div align="center">

[![Version](https://img.shields.io/badge/version-3.0.0-C4622D?style=flat-square)](plugin.json)
[![Evals](https://img.shields.io/badge/evals-9%20prompts%20%C2%B7%2098%25%20pass-1a1918?style=flat-square)](evals/EVALS.md)
[![Blind Panel](https://img.shields.io/badge/blind%20panel-20--7%20candidate%20win-1a1918?style=flat-square)](evals/EVALS.md)
[![Voice Lint](https://img.shields.io/badge/voice%20lint-zero%20em%20dashes%20%C2%B7%20AU%20spelling-027aff?style=flat-square)](skills/create-luke-content/scripts/voice_lint.py)

</div>

# create-luke-content

Write anything in Luke Rhodes' voice (CTO and co-founder of Diolog, an ASX-listed investor relations SaaS), with a proven B2B copywriting craft layer underneath.

---

## What changed in v3.0.0

The predecessor (`create-luke-content` 2.4.3 by DiologIR) wrote in Luke's voice well, but its marketing copy read wrong. The reason was structural: the LinkedIn route carried a bundled engagement research layer, while the marketing route carried no craft research at all. Its only worked evidence was a single consumer parenting-app release post.

This version bundles an empirical B2B copywriting evidence base from a five-backend Dossier deep-research panel (208 sources, 232k characters across OpenAI, Perplexity, Gemini, and Claude Code), rebuilds the marketing persona against it, and activates the deterministic lint configuration it previously shipped without.

```
┌──────────────────────────────────────────────────────────┐
│                   Voice Layer (Top)                      │
│   Evidence-anchored profile from Luke's writing corpus   │
│   Calm, direct, technically fluent, Australian spelling  │
├──────────────────────────────────────────────────────────┤
│             Copywriting Craft Layer (Underneath)         │
│   Outcome + mechanism pairing · Two-sided disclosures    │
│   Preserved domain vocabulary · Single semantic decision │
└──────────────────────────────────────────────────────────┘
```

---

## Comparison against predecessor

| Capability | Predecessor (v2.4.3) | Rebuild (v3.0.0) |
|---|---|---|
| **Marketing craft foundation** | None; single consumer parenting-app post | 208-source B2B SaaS copywriting research layer |
| **Message hierarchy** | Raw feature lists or adjectival claims | Outcome + named mechanism in opening message unit |
| **Claim substantiation** | Allowed vague claims without mechanisms | Concrete benchmarks, thresholds, and exact settings paths |
| **Limitation disclosure** | Omitted operational boundaries | Voluntary two-sided disclosure of rough edges in place |
| **Structural evals pass** | 85.5% (47/55 assertions) | **98.2%** (54/55 assertions) |
| **Blind quality panel** | 7 wins (25.9%) | **20 wins** (74.1%) across OpenAI, xAI, and Claude |
| **Voice lint configuration** | Missing; AU spelling and stylometrics disabled | Bundled `voice-lint.json` enforcing all rules |
| **Self-narrating meta-labels** | Passed clean despite claimed ban | Hard-fails in lint (phrases like brief version or honest one) |

---

## How it works

The skill routes a request to exactly one of six content personas, loads the base voice, and gates the finished draft on a deterministic voice lint:

1. **LinkedIn post & blog article:** Hook that earns the read in 140-200 characters, short paragraphs, at most one genuine closing question, and a Diolog graphic concept.
2. **Marketing content:** Product announcements, launch posts, landing page copy, release notes, and campaign emails. Pairs every operational outcome with its concrete mechanism and discloses rough edges in place.
3. **Code review:** Severity-calibrated candour. Real risks flagged plainly; preferences offered as thoughts.
4. **Slack & chat message:** Context first, then the ask (if one exists), then the genuine out. Zero manufactured asks on FYI updates.
5. **Short-form:** Tweets, comments, bios, and one-liners under 80 words.
6. **ADHD & book audience:** Conversational, structured tutorial prose.

---

## Installation

```bash
# Add the marketplace if you haven't yet
/plugin marketplace add fledgeling-co/fledgeling-plugins

# Install the plugin
/plugin install create-luke-content@fledgeling-plugins
```

---

## Provenance and credits

Successor to `create-luke-content` (v2.4.3) originally authored by **DiologIR**, whose evidence-anchored base voice extraction and core lexicon it retains. The copywriting research layer is exported in full under `docs/deep-research/`.
