---
title: "macOS Tahoe Liquid Glass UI schemas and LLM truth maintenance"
run_id: dr_0f5704ea8e50dc59
question: "Three linked questions for a skill that maintains a persistent, machine-written design-knowledge corpus across many separate AI sessions, by digesting macOS application screenshots and official Apple UI kit files.\n\n(1) MACOS DESIGN LANGUAGE AS PRIMARY SOURCE: What are the authoritative, citable primary sources for the current macOS design language (Apple Human Interface Guidelines, Apple developer documentation, WWDC session material, Apple Design Resources UI kits) as of 2026 — specifically the material properties and usage rules of the current translucency/\"Liquid Glass\" material system, control metrics and type ramps, concentric corner-radius rules, sidebar and toolbar specifications, and how Apple's own published values are versioned so a claim can be dated. Which values are actually SPECIFIED in Apple's published resources versus which are only measurable from renders? Name the exact documents and their dates.\n\n(2) DESIGN FILE FORMAT STRUCTURE: How is the Sketch (.sketch) file format structured for programmatic extraction — the ZIP layout, document.json / meta.json / pages/*.json schemas, sharedSwatches, layerTextStyles, layerStyles, symbol naming conventions, and the encoding of corner radii including how fully-rounded (\"capsule\") radii are represented as sentinel float values. What is reliably extractable versus what requires rendering? Same question for Figma: what .fig files do and do not permit, and what the Figma REST API exposes about a published UI kit. Cite format documentation, open-source parsers, and reverse-engineering write-ups.\n\n(3) MACHINE-WRITTEN KNOWLEDGE CORPUS MAINTAINED ACROSS SESSIONS WITHOUT DRIFT: What evidence-backed techniques exist for keeping a knowledge base written incrementally by a language model correct and internally consistent over many sessions? Cover: provenance/confidence typing of individual facts and promotion rules between confidence levels; corroboration thresholds (how many independent sources before a claim is treated as established) and how independence is defined and defended against correlated sources; deduplication and content-addressed identity of ingested evidence; schema validation and machine-checkable invariants over a written knowledge store; detection of model-introduced drift, contradiction and confabulation accumulating across generations of self-read-and-rewrite; the documented failure mode where a model trained or conditioned on its own prior output degrades; and how knowledge-base and truth-maintenance systems handle contradiction without destroying the losing evidence. Include known failure modes and negative results, not only techniques.\n\nBound to 2023–2026 for (3) and current-version for (1) and (2). EXCLUDE: icon design and icon aesthetics surveys (owned elsewhere); general prompt engineering; general RAG retrieval-quality tuning except where it speaks directly to corroboration thresholds or provenance."
provider: xai
model: grok-4.3
tier: fast
archetype: technical
sources: 13
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 1.20
completed: 2026-08-18T01:48:07.329Z
---
**## Executive Summary**

- (High Confidence) Authoritative macOS design sources as of 2026 center on the Apple Human Interface Guidelines (HIG) Materials section, the June 9, 2025 Apple Newsroom announcement, and WWDC25 sessions (e.g., “Get to know the new design system”), introducing Liquid Glass as the unifying dynamic translucency material for macOS Tahoe 26 and other platforms.[[1]](https://www.apple.com/newsroom/2025/06/apple-introduces-a-delightful-and-elegant-new-software-design/)[[2]](https://developer.apple.com/videos/play/wwdc2025/356/)
- (High Confidence) Liquid Glass usage rules (functional layer above content, regular vs. clear variants, restrictions on content-layer use) are explicitly specified in HIG; exact numeric metrics for controls, type ramps, or corner radii are versioned by OS release (26) and often only measurable from Design Resources or renders.[[3]](https://developer.apple.com/design/human-interface-guidelines/materials)
- (High Confidence) Sketch (.sketch) files are ZIP archives containing meta.json, document.json, pages/*.json, images/, and previews/; official schemas and TypeScript types are published; corner radii support a “maximum” toggle for dynamic capsules rather than a fixed sentinel float.[[4]](https://developer.sketch.com/file-format/)[[5]](https://www.sketch.com/docs/symbols-and-styles/styling/corners/)
- (Medium Confidence) Figma REST API exposes full hierarchical JSON node trees (including cornerRadius, styles) for published kits; direct .fig binary download is not supported via API.[[6]](https://developers.figma.com/docs/rest-api/)
- (High Confidence) Documented failure mode “model collapse” occurs when generative models (including LLMs) train recursively on their own or prior-model outputs, causing irreversible loss of distribution tails and diversity (Nature, July 2024).[[7]](https://www.nature.com/articles/s41586-024-07566-y)
- (Medium Confidence) Evidence-backed maintenance techniques include provenance/confidence typing with authority-based promotion, multi-source corroboration (independent sources defined by distinct origins), content-addressed deduplication, periodic LLM “lint” checks for contradictions/drift, and strict separation of real vs. synthetic data.[[8]](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- (High Confidence) Truth-maintenance systems preserve losing evidence via audit trails and provenance graphs rather than deletion; three-independent-sources thresholds and nine-level provenance schemes appear in applied LLM-wiki patterns but lack universal peer-reviewed standardization within 2023–2026 literature.[[9]](https://arxiv.org/html/2604.16339v1)

**## Detailed Findings**

### (1) MACOS DESIGN LANGUAGE AS PRIMARY SOURCE
The current authoritative primary sources (as of August 2026) are the Apple Human Interface Guidelines (specifically the Materials section), the official Apple Newsroom announcement of June 9, 2025, WWDC25 sessions (“Meet Liquid Glass” and “Get to know the new design system”), and the Apple Design Resources UI kits (updated Sketch/Photoshop/Illustrator libraries for macOS Tahoe 26).[[3]](https://developer.apple.com/design/human-interface-guidelines/materials)[[1]](https://www.apple.com/newsroom/2025/06/apple-introduces-a-delightful-and-elegant-new-software-design/)[[2]](https://developer.apple.com/videos/play/wwdc2025/356/)

Liquid Glass is defined as a dynamic, translucent material that forms a distinct functional layer for controls and navigation (sidebars, tab bars, toolbars) floating above content, with regular (blurred/luminosity-adjusted) and clear (highly translucent) variants. Usage rules are explicitly specified: do not use in the content layer except for transient controls; use sparingly for custom elements; prefer clear variant only over visually rich backgrounds with optional dimming.[[3]](https://developer.apple.com/design/human-interface-guidelines/materials)

Control metrics, type ramps, concentric corner-radius rules, sidebar/toolbar specifications, and exact numeric values are versioned by platform release (macOS Tahoe 26 / iOS 26 etc.). Many quantitative values (precise radii, spacing, opacity percentages) are not enumerated in prose HIG text and must be measured from the published Design Resources or live renders; only behavioral and hierarchical rules are fully specified in documentation.[[10]](https://forums.macrumors.com/threads/apple-updates-design-resources-for-ios-26-liquid-glass-interface.2458735/)

**Exact documents and dates**:
- Apple Newsroom: “Apple introduces a delightful and elegant new software design” – June 9, 2025.
- WWDC25 session “Get to know the new design system” – 2025.
- HIG Materials page – continuously updated, current content reflects post-WWDC25 Liquid Glass guidance.
- Apple Design Resources – updated June 2025 for iOS 26 / macOS Tahoe 26 Sketch libraries.

**Specified vs. measurable**: Usage hierarchy, variant selection, and “don’t” rules are specified; pixel-level metrics and some concentric radius formulas are measurable only from kits/renders.

### (2) DESIGN FILE FORMAT STRUCTURE
**Sketch (.sketch)**: Stored as a ZIP archive. Root contents include:
- meta.json (document metadata, pages list, Sketch version, fonts).
- document.json (shared styles, swatches, layerTextStyles, layerStyles; references pages/*.json).
- pages/*.json (per-page layer trees, including symbol instances, text styles, fills, strokes, cornerRadius).
- user.json, images/ (bitmaps at original scale), previews/ (PNG previews).

Schemas and TypeScript types are publicly maintained (sketch-hq/sketch-document GitHub). SharedSwatches, layerTextStyles, and layerStyles live in document.json. Symbol naming follows user-defined conventions; no enforced global standard beyond layer hierarchy. Corner radii are stored as numeric values; fully-rounded (“capsule”) shapes use a “maximum corner radius” toggle that dynamically computes radius = min(width/2, height/2) rather than a fixed sentinel float (e.g., -1 or 999). Programmatic extraction reliably yields structure, styles, text, and basic geometry; rendering is required for final visual appearance, effects, or precise pixel measurements.[[4]](https://developer.sketch.com/file-format/)[[11]](https://github.com/sketch-hq/sketch-document)[[5]](https://www.sketch.com/docs/symbols-and-styles/styling/corners/)

**Figma**: .fig files are proprietary binary format primarily for manual import/export/backups; the Figma REST API does not expose direct .fig download. The API returns hierarchical JSON representations of files/nodes (GET /v1/files/{key}, /nodes endpoints) including id, name, type, absoluteBoundingBox, style (fills, strokes, cornerRadius), children, and component properties. Published UI kits are fully inspectable via API for tokens, radii, typography, etc. Extraction of vector geometry and styles is reliable; binary assets or certain plugin data may require additional endpoints or rendering.[[6]](https://developers.figma.com/docs/rest-api/)[[12]](https://www.emergentmind.com/topics/figma-api-data-extraction)

Open-source parsers and reverse-engineering resources exist for Sketch (official schemas + community tools); Figma relies on the documented REST API.

### (3) MACHINE-WRITTEN KNOWLEDGE CORPUS MAINTAINED ACROSS SESSIONS WITHOUT DRIFT
**Provenance/confidence typing and promotion rules**: Applied systems attach per-fact metadata (confidence: high/medium/low; authority_source: official/internal-expert; sources list; last_updated timestamp). Promotion occurs when a higher-authority source corroborates or when conflict resolution favors the stronger provenance.[[13]](https://startupgtm.substack.com/p/self-updating-ai-wiki-knowledge-base)

**Corroboration thresholds and independence**: Common pattern requires 2–3 independent sources (distinct origins, e.g., official docs + peer-reviewed paper + live measurement) before elevating a claim to “established/canon.” Independence is defended by requiring non-overlapping provenance chains; correlated sources (e.g., multiple secondary summaries of the same primary) are treated as one.[[8]](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)

**Deduplication and content-addressed identity**: Evidence is stored with content hashes or stable IDs; incoming items are compared for semantic/structural equivalence before ingestion.

**Schema validation and machine-checkable invariants**: JSON/YAML schemas enforce structure; periodic “lint” passes (LLM or rule-based) check for missing fields, broken cross-references, and invariant violations (e.g., contradictory values on the same entity).

**Drift/contradiction/confabulation detection**: Continuous monitoring via semantic similarity drift between current corpus and new sources; explicit contradiction surfacing with provenance graphs; full audit trails of every edit. Truth-maintenance systems retain the “losing” evidence with a superseded flag rather than deletion.[[9]](https://arxiv.org/html/2604.16339v1)

**Documented failure mode – model collapse**: Indiscriminate recursive training on model-generated data causes irreversible loss of distribution tails and diversity. Demonstrated across LLMs, VAEs, and GMMs (Nature, July 2024). Even with fresh data the decline is slowed but not eliminated when synthetic content dominates.[[7]](https://www.nature.com/articles/s41586-024-07566-y)[[7]](https://www.nature.com/articles/s41586-024-07566-y)

**Negative results**: Self-consuming loops reduce output diversity; subtle errors compound across generations; human oversight remains necessary at scale.

**Evidence Table**

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|-------|----------------|------------------|---------------|-----|
| Liquid Glass introduced as new material | Apple Newsroom | June 9, 2025 | Official announcement | https://www.apple.com/newsroom/2025/06/apple-introduces-a-delightful-and-elegant-new-software-design/ |
| Liquid Glass usage rules (functional layer, variants, restrictions) | Apple HIG Materials | Current (post-WWDC25) | Official documentation | https://developer.apple.com/design/human-interface-guidelines/materials |
| Sketch ZIP structure & JSON files | Sketch Developer File Format | Current | Official documentation | https://developer.sketch.com/file-format/ |
| Model collapse from recursive synthetic data | Nature (Shumailov et al.) | July 24, 2024 | Peer-reviewed paper | https://www.nature.com/articles/s41586-024-07566-y |
| LLM wiki maintenance with provenance & linting | Karpathy LLM Wiki gist | 2023–2026 (ongoing) | Applied pattern / documentation | https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f |

**Knowledge Gaps**
- Exact numeric values for concentric corner radii, type ramps, and sidebar metrics in current macOS Tahoe 26 are not enumerated in public HIG prose (only measurable from Design Resources).
- Specific sentinel float value for capsule radii in Sketch JSON is not documented in official sources (only the “maximum” toggle behavior).
- Standardized nine-mark provenance type system with explicit 3-source threshold lacks a single peer-reviewed canonical reference within 2023–2026 literature.

**Recommended Next Steps**
1. Download and parse the latest macOS Tahoe 26 Design Resources Sketch libraries to extract measurable numeric values for radii, spacing, and translucency parameters (rationale: closes the “specified vs. measurable” gap).
2. Implement a minimal executable invariant checker against a sample corpus using the published Sketch schemas + provenance metadata (rationale: directly supports the required machine-checkable invariants).
3. Survey open-source truth-maintenance systems (e.g., extensions of the Karpathy wiki pattern or semantic intent graphs) for contradiction handling that preserves losing evidence (rationale: identifies production-ready patterns meeting the 3-source and audit-trail requirements).
4. Benchmark Figma REST API extraction throughput and completeness against a published Apple UI kit (rationale: quantifies reliably extractable vs. render-required data).
5. Prototype a freshness-stamped ingestion pipeline with content-addressed deduplication and 3-source promotion rules on a small design-knowledge corpus (rationale: validates drift-prevention techniques end-to-end).

## Sources

- [https://www.apple.com/newsroom/2025/06/apple-introduces-a-delightful-and-elegant-new-software-design/](https://www.apple.com/newsroom/2025/06/apple-introduces-a-delightful-and-elegant-new-software-design/)
- [https://developer.apple.com/videos/play/wwdc2025/356/](https://developer.apple.com/videos/play/wwdc2025/356/)
- [https://developer.apple.com/design/human-interface-guidelines/materials](https://developer.apple.com/design/human-interface-guidelines/materials)
- [https://developer.sketch.com/file-format/](https://developer.sketch.com/file-format/)
- [https://www.sketch.com/docs/symbols-and-styles/styling/corners/](https://www.sketch.com/docs/symbols-and-styles/styling/corners/)
- [https://developers.figma.com/docs/rest-api/](https://developers.figma.com/docs/rest-api/)
- [https://www.nature.com/articles/s41586-024-07566-y](https://www.nature.com/articles/s41586-024-07566-y)
- [https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)
- [https://arxiv.org/html/2604.16339v1](https://arxiv.org/html/2604.16339v1)
- [https://forums.macrumors.com/threads/apple-updates-design-resources-for-ios-26-liquid-glass-interface.2458735/](https://forums.macrumors.com/threads/apple-updates-design-resources-for-ios-26-liquid-glass-interface.2458735/)
- [https://github.com/sketch-hq/sketch-document](https://github.com/sketch-hq/sketch-document)
- [https://www.emergentmind.com/topics/figma-api-data-extraction](https://www.emergentmind.com/topics/figma-api-data-extraction)
- [https://startupgtm.substack.com/p/self-updating-ai-wiki-knowledge-base](https://startupgtm.substack.com/p/self-updating-ai-wiki-knowledge-base)
