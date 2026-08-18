---
title: "Methodology for Extracting macOS 27 Design Kit Specifications"
run_id: dr_849d0cf4fe1c8b97
question: "Three linked questions for a skill that maintains a persistent, machine-written design-knowledge corpus across many separate AI sessions, by digesting macOS application screenshots and official Apple UI kit files.\n\n(1) MACOS DESIGN LANGUAGE AS PRIMARY SOURCE: What are the authoritative, citable primary sources for the current macOS design language (Apple Human Interface Guidelines, Apple developer documentation, WWDC session material, Apple Design Resources UI kits) as of 2026 — specifically the material properties and usage rules of the current translucency/\"Liquid Glass\" material system, control metrics and type ramps, concentric corner-radius rules, sidebar and toolbar specifications, and how Apple's own published values are versioned so a claim can be dated. Which values are actually SPECIFIED in Apple's published resources versus which are only measurable from renders? Name the exact documents and their dates.\n\n(2) DESIGN FILE FORMAT STRUCTURE: How is the Sketch (.sketch) file format structured for programmatic extraction — the ZIP layout, document.json / meta.json / pages/*.json schemas, sharedSwatches, layerTextStyles, layerStyles, symbol naming conventions, and the encoding of corner radii including how fully-rounded (\"capsule\") radii are represented as sentinel float values. What is reliably extractable versus what requires rendering? Same question for Figma: what .fig files do and do not permit, and what the Figma REST API exposes about a published UI kit. Cite format documentation, open-source parsers, and reverse-engineering write-ups.\n\n(3) MACHINE-WRITTEN KNOWLEDGE CORPUS MAINTAINED ACROSS SESSIONS WITHOUT DRIFT: What evidence-backed techniques exist for keeping a knowledge base written incrementally by a language model correct and internally consistent over many sessions? Cover: provenance/confidence typing of individual facts and promotion rules between confidence levels; corroboration thresholds (how many independent sources before a claim is treated as established) and how independence is defined and defended against correlated sources; deduplication and content-addressed identity of ingested evidence; schema validation and machine-checkable invariants over a written knowledge store; detection of model-introduced drift, contradiction and confabulation accumulating across generations of self-read-and-rewrite; the documented failure mode where a model trained or conditioned on its own prior output degrades; and how knowledge-base and truth-maintenance systems handle contradiction without destroying the losing evidence. Include known failure modes and negative results, not only techniques.\n\nBound to 2023–2026 for (3) and current-version for (1) and (2). EXCLUDE: icon design and icon aesthetics surveys (owned elsewhere); general prompt engineering; general RAG retrieval-quality tuning except where it speaks directly to corroboration thresholds or provenance."
provider: openai
model: gpt-5.6-terra
tier: fast
archetype: technical
sources: 72
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 3.50
completed: 2026-08-18T01:52:40.032Z
---
## Executive Summary

- **(High Confidence)** Apple’s current primary design corpus is: the live Human Interface Guidelines (HIG), AppKit/SwiftUI API documentation, WWDC25 material introducing Liquid Glass, WWDC26 material documenting macOS 27 refinements, and Apple Design Resources. As of **August 18, 2026**, Apple’s resource page advertises a **macOS 27 UI Kit** for both Figma and Sketch; Apple announced those kits on **June 23, 2026**. [developer.apple.com](https://developer.apple.com/design/resources/) ([developer.apple.com](https://developer.apple.com/design/resources/)) [developer.apple.com](https://developer.apple.com/news/) ([developer.apple.com](https://developer.apple.com/news/?utm_source=openai))

- **(High Confidence)** Treat Apple’s semantic rules as specifications, but do **not** treat sampled pixel values as specifications. Apple specifies Liquid Glass’s hierarchy, allowed placement, regular/clear variants, a **35%** suggested dimming layer for clear glass over bright media, type sizes, and the concentric-radius calculation. It does **not** publish stable blur radii, opacity curves, lensing/refraction parameters, window radii, toolbar heights, sidebar widths, or fixed control-height tables for the new system. Those are adaptive runtime/render outputs. [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/materials) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/materials?utm_source=openai)) [developer.apple.com](https://developer.apple.com/documentation/swiftui/edge/corner/style/concentric) ([developer.apple.com](https://developer.apple.com/documentation/swiftui/edge/corner/style/concentric?utm_source=openai))

- **(High Confidence)** A `.sketch` file is an officially documented ZIP archive of JSON and binary assets. `meta.json`, `document.json`, and `pages/*.json` are reliable machine-extraction targets; shared swatches, layer/text styles, symbols, layer names, bounds, static fills, borders, text attributes, and declared corner-radius fields are extractable. Dynamic visual outcomes—including Apple’s adaptive glass behavior, platform font rasterization, and image-dependent blending—require rendering. [developer.sketch.com](https://developer.sketch.com/file-format/) ([developer.sketch.com](https://developer.sketch.com/file-format/?utm_source=openai)) [developer.sketch.com](https://developer.sketch.com/file-format/spec) ([developer.sketch.com](https://developer.sketch.com/file-format/spec?utm_source=openai))

- **(High Confidence)** There is **no formally specified universal Sketch “capsule sentinel float.”** The official schema declares `fixedRadius` and point-level `cornerRadius` merely as numbers, without a special-value definition. Therefore, a corpus must not canonize `999`, `9999`, `0.5`, or any other purported sentinel globally. The shipped extractor below supports an explicitly configured, evidence-stamped sentinel for a *specific verified kit version*, but defaults to geometry-based capsule detection and labels it as inferred rather than specified. [raw.githubusercontent.com](https://raw.githubusercontent.com/sketch-hq/sketch-document/main/packages/file-format/schema/layers/rectangle.schema.yaml) ([raw.githubusercontent.com](https://raw.githubusercontent.com/sketch-hq/sketch-document/main/packages/file-format/schema/layers/rectangle.schema.yaml)) [raw.githubusercontent.com](https://raw.githubusercontent.com/sketch-hq/sketch-document/main/packages/file-format/schema/objects/curve-point.schema.yaml) ([raw.githubusercontent.com](https://raw.githubusercontent.com/sketch-hq/sketch-document/main/packages/file-format/schema/objects/curve-point.schema.yaml))

- **(High Confidence)** Figma’s REST API is the supported path for published UI-kit content; it exposes a file’s document tree, component/style maps, node subsets, rendered images, and published-library metadata subject to permissions and rate limits. A local `.fig` file is an undocumented, reverse-engineered binary/container format; parsers can be useful acquisition tools but cannot be treated as a stable vendor contract. [developers.figma.com](https://developers.figma.com/docs/rest-api/file-endpoints/) ([developers.figma.com](https://developers.figma.com/docs/rest-api/file-endpoints/?utm_source=openai)) [developers.figma.com](https://developers.figma.com/docs/rest-api/component-types/) ([developers.figma.com](https://developers.figma.com/docs/rest-api/component-types/?utm_source=openai)) [madebyevan.com](https://madebyevan.com/figma/fig-file-parser/) ([madebyevan.com](https://madebyevan.com/figma/fig-file-parser/?utm_source=openai))

- **(High Confidence)** The corpus should use **atomic structured claims as the authority**, with Markdown as a generated projection. It needs a nine-mark provenance type system, immutable evidence blobs identified by hashes, explicit source-independence roots, temporal validity, contradiction sets, a strict three-independent-roots threshold for `CANON`, and an executable invariant checker. <INFERENCE from="[Sketch’s formal schema/versioning; provenance-management evidence; content-addressed data structures]">This architecture removes prose parsing and makes promotion, freshness, contradiction, and citation coverage testable.</INFERENCE> [link.springer.com](https://link.springer.com/article/10.1007/s13222-023-00463-0) ([link.springer.com](https://link.springer.com/article/10.1007/s13222-023-00463-0?utm_source=openai)) [spec.filecoin.io](https://spec.filecoin.io/libraries/ipld/) ([spec.filecoin.io](https://spec.filecoin.io/libraries/ipld/?utm_source=openai))

- **(High Confidence)** Do not let an LLM’s prior prose become evidence. Recursive use of model-generated material has documented degradation risks; independent research finds losses of diversity, distribution tails, or quality in self-consuming loops, while fresh real data and curation can mitigate but do not justify blind self-confirmation. [nature.com](https://www.nature.com/articles/s41586-024-07566-y) ([rivista.ai](https://www.rivista.ai/wp-content/uploads/2024/08/s41586-024-07566-y-1.pdf?utm_source=openai)) [arxiv.org](https://arxiv.org/abs/2311.16822) ([arxiv.org](https://arxiv.org/abs/2311.16822?utm_source=openai)) [proceedings.iclr.cc](https://proceedings.iclr.cc/paper_files/paper/2024/hash/ebc042e767de551803ccfcc45e2454f5-Abstract-Conference.html) ([proceedings.iclr.cc](https://proceedings.iclr.cc/paper_files/paper/2024/hash/ebc042e767de551803ccfcc45e2454f5-Abstract-Conference.html?utm_source=openai))

- **(High Confidence)** Every screenshot, `.sketch` archive, `.fig` archive, OCR string, and prior-session file is untrusted third-party input. Indirect prompt injection is empirically demonstrated in tool-integrated agents; persistent memory expands the attack surface. The ingestion pipeline must make source material **data-only**, prohibit it from authorizing actions or promotion, quarantine it before model exposure, and require deterministic validators before any corpus write. [aclanthology.org](https://aclanthology.org/2024.findings-acl.624/) ([aclanthology.org](https://aclanthology.org/2024.findings-acl.624/?utm_source=openai)) [arxiv.org](https://arxiv.org/abs/2607.14611) ([arxiv.org](https://arxiv.org/abs/2607.14611?utm_source=openai))

---

## Detailed Findings

### 1. MACOS DESIGN LANGUAGE AS PRIMARY SOURCE: What are the authoritative, citable primary sources for the current macOS design language, what is specified, what is measurable, and how should claims be dated?

**Decision:** use an authority ladder, not a single “Apple design language” document.

1. **Normative behavioral guidance:** Apple HIG.
2. **Implementation semantics and availability:** AppKit and SwiftUI API documentation.
3. **Rationale and system behavior not fully represented in APIs:** WWDC sessions.
4. **Concrete component geometry, names, and states:** Apple Design Resources files.
5. **Observed pixels only:** screenshots and rendered kit exports.

Apple’s current public Design Resources page labels the current desktop kit **“macOS 27”**, offering both Figma and Sketch UI kits. Apple’s news page dates the release of iOS, iPadOS, and macOS 27 design kits to **June 23, 2026** and says they include Liquid Glass updates, expanded component/state support, naming changes aligned with code, resizing improvements, and macOS Dark Mode. [developer.apple.com](https://developer.apple.com/design/resources/) ([developer.apple.com](https://developer.apple.com/design/resources/)) [developer.apple.com](https://developer.apple.com/news/) ([developer.apple.com](https://developer.apple.com/news/?utm_source=openai))

#### Authoritative Apple source register

| Document / artifact | Exact date available from Apple | Authority | What it establishes | Source-discipline justification |
|---|---:|---|---|---|
| **HIG: Materials** | Added/updated for Liquid Glass on **June 9, 2025**; live page retrieved August 18, 2026 | Normative design guidance | Liquid Glass hierarchy, regular/clear variants, forbidden/allowed placement, accessibility behavior | Official Apple HIG; direct primary guidance |
| **HIG: Typography** | Live page does not expose a stable publication date; retrieved August 18, 2026 | Normative metric table | macOS default/minimum text size and built-in text-style ramp | Official Apple HIG; direct primary guidance |
| **HIG: Toolbars** | Original Liquid Glass update **June 9, 2025**; page reports updated Liquid Glass guidance **December 16, 2025** | Normative behavior/layout guidance | Toolbar placement, groups, availability requirements | Official Apple HIG; direct primary guidance |
| **HIG: Sidebars** | Liquid Glass update **June 9, 2025** | Normative structural guidance | Sidebar function and floating-over-content model | Official Apple HIG; direct primary guidance |
| **Meet Liquid Glass — WWDC25, session 219** | **June 9, 2025** | Primary explanatory material | Lensing, adaptive behavior, hierarchy, use restrictions | First-party Apple session |
| **Build an AppKit app with the new design — WWDC25, session 310** | WWDC25, **June 2025** | Primary implementation material | macOS control behavior, toolbars, sidebars, glass APIs, control shapes | First-party Apple framework session |
| **Modernize your AppKit app — WWDC26, session 289** | WWDC26, **June 2026** | Current primary update | macOS 27 sidebar, toolbar, interactive-glass, and concentricity refinements | First-party Apple framework session |
| **AppKit: `NSGlassEffectView`** | Live API documentation; marked Beta on current page | API contract | Dynamic glass content view, corner radius, style, tint, interactive effect | Official API contract |
| **Apple Design Resources: macOS 27 UI Kit** | **June 23, 2026** announcement | Primary design artifact | Exact authored component structures and asset states in a specific kit revision | Official Apple-distributed kit |

[developer.apple.com](https://developer.apple.com/design/whats-new?q=vision) ([developer.apple.com](https://developer.apple.com/design/whats-new?q=vision&utm_source=openai)) [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/materials) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/materials?utm_source=openai)) [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/typography) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/typography?changes=_5&utm_source=openai)) [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/toolbars) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/toolbars?changes=_2&utm_source=openai)) [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/sidebars) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/sidebars?changes=_8&utm_source=openai)) [developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/219/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/219/?utm_source=openai)) [developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/310/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/310/?time=210)) [developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/289/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/289/?utm_source=openai)) [developer.apple.com](https://developer.apple.com/documentation/appkit/nsglasseffectview) ([developer.apple.com](https://developer.apple.com/documentation/appkit/nsglasseffectview?changes=_1&utm_source=openai))

#### Liquid Glass: specified rules versus rendered appearance

| Subject | Apple-specified rule or value | Classification | Do not infer as a constant |
|---|---|---|---|
| Layering | Liquid Glass is a functional layer for controls and navigation above content; do not use it as ordinary content-layer decoration. | **Specified** | Exact blur kernel, refraction strength, opacity |
| Variants | `regular` and `clear` variants exist; use clear only over visually rich backgrounds and only when legibility conditions are met. | **Specified** | Static light/dark color for either variant |
| Clear-glass dimming | For bright underlying content, Apple recommends considering a **35% opacity** dark dimming layer. | **Specified quantitative guidance** | That 35% applies universally or replaces contrast testing |
| Adaptivity | Glass adapts tint, shadows, dynamic range, and in some cases apparent light/dark character to underlying content and settings. | **Specified behavior** | A sample screenshot’s RGB, alpha, blur, or shadow values |
| Content hierarchy | Do not place glass within/on top of other glass; use sparingly; system components acquire the effect automatically. | **Specified** | The number of acceptable custom glass items |
| macOS standard materials | macOS retains semantic standard materials, vibrancy, and blending modes such as behind-window / within-window. | **Specified API category** | Pixel-equivalent visual output in every wallpaper/content state |
| Sidebar | Sidebars float above content in the Liquid Glass layer; content should extend beneath them. | **Specified behavior** | Fixed sidebar width, exact inset, fixed radius |
| Toolbar | macOS toolbars sit at the top of a window, below or integrated with titlebar; commands must also be available through menus. | **Specified behavior** | Fixed toolbar height or exact group gap |
| macOS 27 refinements | Sidebars extend to window edges; bordered toolbar items over a sidebar adopt Liquid Glass; interactive glass should be limited to interactive controls. | **Specified current behavior** | A permanent universal rendering appearance |
| Concentricity | Radius equals container radius minus the distance between corresponding corners, clamped at zero / practical geometric limits. | **Specified formula** | A universal fixed “Apple radius token” |

[developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/materials) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/materials?utm_source=openai)) [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/sidebars) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/sidebars?changes=_8&utm_source=openai)) [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/toolbars) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/toolbars?changes=_2&utm_source=openai)) [developer.apple.com](https://developer.apple.com/documentation/swiftui/edge/corner/style/concentric) ([developer.apple.com](https://developer.apple.com/documentation/swiftui/edge/corner/style/concentric?utm_source=openai)) [developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/289/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2026/289/?utm_source=openai))

Apple’s WWDC25 material says that large glass objects such as macOS sidebars use ambient environmental cues and that nearby colorful content can spill onto the surface and shadow. Apple’s wording is deliberate: this is a dynamic effect, not a token table. [developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/219/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/219/?utm_source=openai))

#### Control metrics and typography

Apple explicitly specifies the macOS typographic ramp below. The HIG states macOS’s recommended default size is **13 pt** and minimum is **10 pt**; macOS does not support Dynamic Type, although system font variants should be used to match system controls. [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/typography) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/typography?changes=_5&utm_source=openai))

| macOS text style | Weight | Size | Line height | Evidence status |
|---|---:|---:|---:|---|
| Large Title | Regular | 26 pt | 32 pt | Specified |
| Title 1 | Regular | 22 pt | 26 pt | Specified |
| Title 2 | Regular | 17 pt | 22 pt | Specified |
| Title 3 | Regular | 15 pt | 20 pt | Specified |
| Headline | Bold | 13 pt | 16 pt | Specified |
| Body | Regular | 13 pt | 16 pt | Specified |
| Callout | Regular | 12 pt | 15 pt | Specified |
| Subheadline | Regular | 11 pt | 14 pt | Specified |
| Footnote | Regular | 10 pt | 13 pt | Specified |
| Caption 1 | Regular | 10 pt | 13 pt | Specified |
| Caption 2 | Medium | 10 pt | 13 pt | Specified |

[developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/typography) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/typography?changes=_5&utm_source=openai))

Apple specifies **semantic control sizes**—mini, small, regular/medium, large, and extra large—but tells developers not to hard-code heights. WWDC25 says mini through medium became slightly taller in macOS 26; large and extra-large controls use capsules, while smaller sizes retain rounded rectangles. AppKit exposes `prefersCompactControlSizeMetrics` for pre-macOS-26-compatible metrics. This means observed control heights are versioned render behavior, not portable constants. [developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/310/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/310/?time=210)) [developer.apple.com](https://developer.apple.com/documentation/updates/appkit) ([developer.apple.com](https://developer.apple.com/documentation/updates/appkit?changes=latest_ma_3&utm_source=openai))

#### What must remain render-measured

| Candidate corpus field | Store as | Why |
|---|---|---|
| Glass blur, lensing, refraction, shadow hue, shadow opacity | `P3_PRIMARY_RENDER_MEASURED` | Apple describes adaptive behavior, not stable numerical optical constants. |
| Window radius and toolbar-shell radius | `P3_PRIMARY_RENDER_MEASURED` plus OS/build | Apple says radii vary by window style and can scale with toolbar geometry. |
| Sidebar width, toolbar height, item gap, exact capsule geometry | `P2_PRIMARY_ARTIFACT_EXTRACTED` if present in kit; otherwise `P3` | Not enumerated as universal HIG values. |
| Screen-pixel type measurements | `P3_PRIMARY_RENDER_MEASURED` | Retina scale, antialiasing, optical sizing, font substitution, and screenshot scaling contaminate inference. |
| “Apple style token” name from a layer name | `P2`, never `P0` | Layer naming is authored artifact metadata, not necessarily a normative public rule. |

<INFERENCE from="[Apple HIG Materials; WWDC25 AppKit session; SwiftUI concentric API]">The correct corpus distinction is not “official versus unofficial”; it is “normatively specified,” “officially authored artifact,” and “render-observed.” Combining these categories would manufacture false precision.</INFERENCE> [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/materials) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/materials?utm_source=openai)) [developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/310/) ([developer.apple.com](https://developer.apple.com/videos/play/wwdc2025/310/?time=210)) [developer.apple.com](https://developer.apple.com/documentation/swiftui/edge/corner/style/concentric) ([developer.apple.com](https://developer.apple.com/documentation/swiftui/edge/corner/style/concentric?utm_source=openai))

#### Dating and versioning Apple claims

Use this identity tuple for every Apple-derived fact:

```json
{
  "publisher": "Apple",
  "artifact_title": "Apple Design Resources — macOS 27 UI Kit",
  "artifact_kind": "official_design_kit",
  "announced_on": "2026-06-23",
  "retrieved_at": "2026-08-18T00:00:00Z",
  "source_url": "https://developer.apple.com/design/resources/",
  "source_sha256": "<downloaded-file-sha256>",
  "platform": "macOS",
  "platform_release": "27",
  "sdk_or_app_version": "<meta.json.appVersion>",
  "build": "<meta.json.build>",
  "fact_scope": "artifact-specific"
}
```

Apple’s HIG pages are live documents, not immutable versioned publications. Therefore, archive the fetched HTML/text, preserve Apple’s displayed change date where present, retain the retrieval timestamp, and hash the exact response. For downloaded Sketch kits, additionally preserve `meta.json.version`, `compatibilityVersion`, `appVersion`, `build`, `saveHistory`, and `commit` when present. [developer.apple.com](https://developer.apple.com/news/) ([developer.apple.com](https://developer.apple.com/news/?utm_source=openai)) [developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/toolbars) ([developer.apple.com](https://developer.apple.com/design/human-interface-guidelines/toolbars?changes=_2&utm_source=openai)) [developer.sketch.com](https://developer.sketch.com/file-format/) ([developer.sketch.com](https://developer.sketch.com/file-format/?utm_source=openai))

---

### 2. DESIGN FILE FORMAT STRUCTURE: How should Sketch and Figma kits be extracted, what is reliable, and what requires rendering?

#### Sketch `.sketch`: formal extraction surface

Sketch officially documents `.sketch` as a ZIP archive containing JSON plus assets. The stable archive-level targets are:

| ZIP entry | Reliable extraction | Notes |
|---|---|---|
| `meta.json` | document version, compatible version, app version/build, page/artboard index, fonts, save metadata | Best version/date anchor |
| `document.json` | common document data, shared styles, shared text styles, library references, swatches | Cross-page reusable definitions |
| `pages/*.json` | page/layer tree, frames, text, static styles, symbol masters/instances | One JSON document per page |
| `images/*` | imported bitmap bytes | Original imported scale may exceed displayed bounds |
| `previews/*` | preview bitmap | Convenience render, not semantic source |
| `user.json` / `workspace.json` | user/workspace state | Do not treat as visual specification |
| `userInfo` | arbitrary plugin/application metadata | Untrusted opaque data; never execute or promote automatically |

[developer.sketch.com](https://developer.sketch.com/file-format/) ([developer.sketch.com](https://developer.sketch.com/file-format/?utm_source=openai)) [npmjs.com](https://www.npmjs.com/package/%40sketch-hq/sketch-file-format) ([npmjs.com](https://www.npmjs.com/package/%40sketch-hq/sketch-file-format?utm_source=openai))

`document.json` contains `layerStyles`, `layerTextStyles`, optional `layerSymbols`, and optional `sharedSwatches`; Sketch’s own walkthrough identifies color variables as swatches under `sharedSwatches.objects`. Symbol masters carry a `symbolID`; names are ordinary strings, so slash-delimited naming may be a useful convention but is **not** a format-level semantic contract. [unpkg.com](https://unpkg.com/@sketch-hq/sketch-file-format@3.6.2/dist/file-format.schema.json) ([app.unpkg.com](https://app.unpkg.com/%40sketch-hq/sketch-file-format%403.6.2/files/dist/file-format.schema.json?utm_source=openai)) [sketch.com](https://www.sketch.com/blog/open-format-reading-sketch-file-sketch-to-json/) ([sketch.com](https://www.sketch.com/blog/open-format-reading-sketch-file-sketch-to-json/?utm_source=openai))

Sketch publishes its JSON schema and generated TypeScript types separately from the desktop app and advances the schema when document structure changes. Pin the parser/schema package version used for each ingestion run. [developer.sketch.com](https://developer.sketch.com/file-format/spec) ([developer.sketch.com](https://developer.sketch.com/file-format/spec?utm_source=openai)) [github.com](https://github.com/sketch-hq/sketch-document) ([github.com](https://github.com/sketch-hq/sketch-document?utm_source=openai))

#### Corner radii and capsules: exact finding

A rectangle can contain `fixedRadius`; curve points can contain `cornerRadius`; the schema declares both as numbers. Vector-point rounding additionally has a behavior enum: disabled, legacy, rounded, or smooth. The official schema does **not** define a global “capsule float sentinel,” a `999` convention, or a normalization rule that makes a magic number portable across all Sketch versions. [raw.githubusercontent.com](https://raw.githubusercontent.com/sketch-hq/sketch-document/main/packages/file-format/schema/layers/rectangle.schema.yaml) ([raw.githubusercontent.com](https://raw.githubusercontent.com/sketch-hq/sketch-document/main/packages/file-format/schema/layers/rectangle.schema.yaml)) [raw.githubusercontent.com](https://raw.githubusercontent.com/sketch-hq/sketch-document/main/packages/file-format/schema/objects/curve-point.schema.yaml) ([raw.githubusercontent.com](https://raw.githubusercontent.com/sketch-hq/sketch-document/main/packages/file-format/schema/objects/curve-point.schema.yaml)) [raw.githubusercontent.com](https://raw.githubusercontent.com/sketch-hq/sketch-document/main/packages/file-format/schema/enums/points-radius-behaviour.schema.yaml) ([raw.githubusercontent.com](https://raw.githubusercontent.com/sketch-hq/sketch-document/main/packages/file-format/schema/enums/points-radius-behaviour.schema.yaml))

<INSUFFICIENT_EVIDENCE>[A universal capsule-radius sentinel float for Sketch. The vendor schema supplies numeric fields but no special-value semantics. A verified set of reference `.sketch` files created in each target Sketch version, with inspector values and rendered exports, would be required to establish a version-scoped convention.]</INSUFFICIENT_EVIDENCE>

**Operational rule:** extract raw radius fields unchanged; infer `capsule_candidate` only if declared radius is at least half of the layer’s smaller dimension, or if a *kit-version-specific, independently verified* sentinel is supplied to the extractor. Never promote an inferred capsule to a normative Apple claim without render confirmation.

#### Shipped extractor: `extract_sketch.py`

The following is a standalone Python 3.11+ extractor. It is deliberately data-only: it does not evaluate layer names, `userInfo`, text, or plugin metadata; limits ZIP expansion; stamps freshness on its emitted file; captures raw values; and treats a configured sentinel as an explicit heuristic rather than a global Sketch rule.

```python
#!/usr/bin/env python3
"""
extract_sketch.py INPUT.sketch OUT_DIR [--capsule-sentinel FLOAT]

Emits OUT_DIR/sketch-extract.json with source hash, freshness stamp, raw
radius fields, shared styles/swatches, symbols, and a conservative capsule flag.
No document-derived string is interpreted as instructions or executed.
"""
from __future__ import annotations
import argparse, hashlib, json, os, sys, zipfile
from datetime import datetime, timezone
from pathlib import Path

MAX_MEMBERS = 100_000
MAX_UNCOMPRESSED = 2_000_000_000  # 2 GB safety ceiling
EPS = 1e-9
TOOL_VERSION = "1.0.0"

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()

def safe_members(zf: zipfile.ZipFile):
    infos = zf.infolist()
    if len(infos) > MAX_MEMBERS:
        raise ValueError("archive has too many entries")
    total = 0
    for i in infos:
        p = Path(i.filename)
        if p.is_absolute() or ".." in p.parts:
            raise ValueError(f"unsafe archive path: {i.filename!r}")
        total += i.file_size
        if total > MAX_UNCOMPRESSED:
            raise ValueError("archive exceeds uncompressed safety ceiling")
    return infos

def read_json(zf: zipfile.ZipFile, name: str):
    try:
        return json.loads(zf.read(name).decode("utf-8"))
    except KeyError:
        return None

def frame(layer: dict) -> tuple[float | None, float | None]:
    f = layer.get("frame") or {}
    try:
        return float(f["width"]), float(f["height"])
    except (KeyError, TypeError, ValueError):
        return None, None

def radius_observation(layer: dict, sentinel: float | None) -> dict:
    w, h = frame(layer)
    raw_fixed = layer.get("fixedRadius")
    raw_points = [
        p.get("cornerRadius") for p in (layer.get("points") or [])
        if isinstance(p, dict) and isinstance(p.get("cornerRadius"), (int, float))
    ]
    raw = [x for x in [raw_fixed] if isinstance(x, (int, float))] + raw_points
    minimum = min(w, h) if w is not None and h is not None else None

    geometry_capsule = (
        minimum is not None and minimum > 0 and
        any(float(x) + EPS >= minimum / 2 for x in raw)
    )
    sentinel_match = (
        sentinel is not None and
        any(abs(float(x) - sentinel) <= EPS for x in raw)
    )
    return {
        "fixedRadius_raw": raw_fixed,
        "pointCornerRadii_raw": raw_points,
        "pointRadiusBehaviour_raw": layer.get("pointRadiusBehaviour"),
        "cornerStyle_raw": [
            p.get("cornerStyle") for p in (layer.get("points") or [])
            if isinstance(p, dict) and "cornerStyle" in p
        ],
        "capsule_candidate": geometry_capsule or sentinel_match,
        "capsule_basis": (
            "configured_version_scoped_sentinel"
            if sentinel_match else
            "radius_greater_than_or_equal_to_half_min_dimension"
            if geometry_capsule else "none"
        ),
        "capsule_status": (
            "INFERRED_NOT_VENDOR_SPECIFIED"
            if geometry_capsule or sentinel_match else "NOT_CAPSULE"
        ),
        "configured_capsule_sentinel": sentinel
    }

def walk(layer: dict, page_id: str, ancestry: list[str], sentinel: float | None,
         output: list[dict]) -> None:
    name = layer.get("name", "")  # opaque third-party data; never executed
    layer_id = layer.get("do_objectID")
    item = {
        "id": layer_id,
        "class": layer.get("_class"),
        "name_raw": name,
        "page_id": page_id,
        "ancestry_raw": ancestry,
        "frame": layer.get("frame"),
        "sharedStyleID": layer.get("sharedStyleID"),
        "symbolID": layer.get("symbolID"),
        "style_raw": layer.get("style"),
        "radius": radius_observation(layer, sentinel),
    }
    output.append(item)
    for child in layer.get("layers") or []:
        if isinstance(child, dict):
            walk(child, page_id, ancestry + [str(name)], sentinel, output)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("input", type=Path)
    ap.add_argument("out_dir", type=Path)
    ap.add_argument("--capsule-sentinel", type=float, default=None,
                    help="Only use after verifying this value for a specific kit/version.")
    args = ap.parse_args()

    source_hash = sha256_file(args.input)
    with zipfile.ZipFile(args.input) as zf:
        safe_members(zf)
        meta = read_json(zf, "meta.json")
        document = read_json(zf, "document.json")
        if not isinstance(meta, dict) or not isinstance(document, dict):
            raise SystemExit("not a supported .sketch archive: meta.json/document.json missing")

        pages = []
        layers = []
        for name in sorted(n for n in zf.namelist()
                           if n.startswith("pages/") and n.endswith(".json")):
            page = read_json(zf, name)
            if not isinstance(page, dict):
                continue
            pages.append({"entry": name, "id": page.get("do_objectID"),
                          "name_raw": page.get("name")})
            walk(page, str(page.get("do_objectID")), [], args.capsule_sentinel, layers)

    emitted_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()
    result = {
        "schema": "design-corpus.sketch-extract/v1",
        "freshness": {
            "emitted_at": emitted_at,
            "source_sha256": source_hash,
            "tool_version": TOOL_VERSION,
            "stale_after": None
        },
        "trust_boundary": "THIRD_PARTY_UNTRUSTED_DATA",
        "source": {"filename": args.input.name, "sha256": source_hash},
        "meta_raw": meta,
        "document_assets": {
            "sharedSwatches_raw": document.get("sharedSwatches"),
            "layerTextStyles_raw": document.get("layerTextStyles"),
            "layerStyles_raw": document.get("layerStyles"),
            "layerSymbols_raw": document.get("layerSymbols"),
        },
        "pages": pages,
        "layers": layers
    }
    args.out_dir.mkdir(parents=True, exist_ok=True)
    out = args.out_dir / "sketch-extract.json"
    out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                   encoding="utf-8")
    print(out)

if __name__ == "__main__":
    main()
```

<INFERENCE from="[Sketch official ZIP/JSON format and schema; absence of vendor-defined sentinel semantics]">The extractor’s sentinel option is intentionally opt-in and version-scoped. This is safer than silently converting a common but undocumented value into a global design rule.</INFERENCE> [developer.sketch.com](https://developer.sketch.com/file-format/) ([developer.sketch.com](https://developer.sketch.com/file-format/?utm_source=openai)) [raw.githubusercontent.com](https://raw.githubusercontent.com/sketch-hq/sketch-document/main/packages/file-format/schema/layers/rectangle.schema.yaml) ([raw.githubusercontent.com](https://raw.githubusercontent.com/sketch-hq/sketch-document/main/packages/file-format/schema/layers/rectangle.schema.yaml))

#### Figma: supported API versus local `.fig`

| Capability | Figma REST API | Local `.fig` export |
|---|---|---|
| Vendor-supported structured contract | Yes | No public stable format specification |
| Document/node hierarchy | Yes, `GET /v1/files/:file_key` and node endpoints | Often recoverable through reverse-engineering |
| Components/styles | Yes; file response maps and published-library metadata endpoints | May be recoverable, but not a supported compatibility guarantee |
| Rendered assets | Yes, image export endpoint | Requires own renderer or reverse-engineered rendering |
| Exact local binary access | No | Yes, if export is available |
| Version stability | API version/scope/rate-limit governed | Internal format can change |
| Recommended use | Primary ingestion path for a published kit | Secondary acquisition / recovery path only |

Figma’s `GET file` endpoint is Tier 1, requires `file_content:read`, and returns document content plus component/style maps. Published component and style metadata are separately exposed through component/style endpoints. [developers.figma.com](https://developers.figma.com/docs/rest-api/file-endpoints/) ([developers.figma.com](https://developers.figma.com/docs/rest-api/file-endpoints/?utm_source=openai)) [developers.figma.com](https://developers.figma.com/docs/rest-api/component-types/) ([developers.figma.com](https://developers.figma.com/docs/rest-api/component-types/?utm_source=openai))

Figma’s rate limits changed on **November 17, 2025**. For Tier 1 file endpoints, documented Full/Dev-seat limits are **10/minute Starter**, **15/minute Professional**, and **20/minute Organization/Enterprise**; View/Collab seats may be limited to up to **6/month**, and a `429` includes `Retry-After`. [developers.figma.com](https://developers.figma.com/docs/rest-api/rate-limits/) ([developers.figma.com](https://developers.figma.com/docs/rest-api/rate-limits/?utm_source=openai))

Open-source `.fig` parsers describe modern files as ZIP containers that may include `canvas.fig`, `meta.json`, `thumbnail.png`, and images, with `canvas.fig` using a reverse-engineered `fig-kiwi` binary structure. This is useful evidence for extraction engineering but is not official Figma documentation; label all resulting data `S2_REVERSE_ENGINEERED_FORMAT` until corroborated by API export or rendering. [github.com](https://github.com/OpenFig-org/openfig-core/blob/main/README.md) ([github.com](https://github.com/OpenFig-org/openfig-core/blob/main/README.md?utm_source=openai)) [madebyevan.com](https://madebyevan.com/figma/fig-file-parser/) ([madebyevan.com](https://madebyevan.com/figma/fig-file-parser/?utm_source=openai))

#### Operational comparison

| Ingestion surface | Parameter Count | Context Window | Typical Latency | Cost | License / contract | Decision |
|---|---:|---:|---|---|---|---|
| Local Python Sketch JSON extractor | N/A; deterministic parser | N/A | Local I/O-bound | Compute only | Your code + Sketch file-format schema license | Use for `.sketch` |
| Sketch schema validator | N/A; deterministic JSON Schema | N/A | Local CPU-bound | Compute only | Sketch schema package | Pin version |
| Figma REST API | N/A | N/A | Network-bound; rate-limited | Plan/seat dependent | Figma developer terms/API scopes | Preferred for published Figma kit |
| Reverse-engineered `.fig` parser | N/A; deterministic parser | N/A | Local CPU-bound | Compute only | Parser-specific OSS license; unstable format | Secondary/quarantined ingestion |
| LLM extraction reviewer | <MISSING_DATA>[No model was selected in the decision record]</MISSING_DATA> | <MISSING_DATA>[Model-specific]</MISSING_DATA> | Model-dependent | Model-dependent | Model-dependent | Never authoritative; draft-only |

---

### 3. MACHINE-WRITTEN KNOWLEDGE CORPUS MAINTAINED ACROSS SESSIONS WITHOUT DRIFT: What evidence-backed techniques should be used?

**Decision:** adopt an **evidence ledger + atomic claim store + generated prose** architecture. Do not allow sessions to edit canonical Markdown directly.

A provenance-management framework for knowledge graphs supports reruns, altered reruns, undo, and provenance retrieval; provenance is needed for reproducibility and updateability. A separate provenance-verification pipeline, ProVe, specifically checks whether a knowledge-graph triple is supported by text in its documented provenance. These support claim-level evidence rather than document-level trust. [link.springer.com](https://link.springer.com/article/10.1007/s13222-023-00463-0) ([link.springer.com](https://link.springer.com/article/10.1007/s13222-023-00463-0?utm_source=openai)) [journals.sagepub.com](https://journals.sagepub.com/doi/10.3233/SW-233467) ([journals.sagepub.com](https://journals.sagepub.com/doi/10.3233/SW-233467?utm_source=openai))

#### The required nine-mark provenance type system

| Mark | Name | Meaning | Can support `CANON`? | Promotion rule |
|---|---|---|---|---|
| `P0` | `PRIMARY_NORMATIVE` | Explicit requirement/guidance from controlling authority | Yes, subject to threshold policy | Exact citation + scope/version |
| `P1` | `PRIMARY_API_CONTRACT` | Official API/schema contract | Yes | Pin API/schema version |
| `P2` | `PRIMARY_ARTIFACT_EXTRACTED` | Deterministic extraction from an official artifact | Yes, for artifact-scoped claims | Hash artifact + extractor version |
| `P3` | `PRIMARY_RENDER_MEASURED` | Deterministic measurement from official render/screenshot | No alone | Method, viewport, scale, build |
| `S0` | `FORMAT_SCHEMA` | Official third-party format/API schema | Yes for format claims | Pin schema package/version |
| `S1` | `PEER_REVIEWED_RESEARCH` | Peer-reviewed or proceedings research | Yes for empirical-method claims | Preserve paper DOI/version |
| `S2` | `REVERSE_ENGINEERED_OR_VENDOR_TECHNICAL` | OSS parser/vendor engineering documentation | No alone | Corroborate against primary artifact/API |
| `I0` | `DERIVED_INFERENCE` | Reasoned conclusion from cited claims | Never directly | Must list parent claim IDs |
| `U0` | `UNVERIFIED_OR_MODEL_OUTPUT` | Unverified statement, OCR, prior-session prose, model proposal | Never | Must be replaced or archived |

<INFERENCE from="[Provenance-management frameworks; ProVe’s triple-to-source verification; format schemas]">The mark is a type, not a scalar confidence score. It prevents a persuasive rendering measurement or LLM summary from masquerading as an explicit Apple requirement.</INFERENCE> [link.springer.com](https://link.springer.com/article/10.1007/s13222-023-00463-0) ([link.springer.com](https://link.springer.com/article/10.1007/s13222-023-00463-0?utm_source=openai)) [journals.sagepub.com](https://journals.sagepub.com/doi/10.3233/SW-233467) ([journals.sagepub.com](https://journals.sagepub.com/doi/10.3233/SW-233467?utm_source=openai))

#### Confidence and promotion rules

1. A claim begins `DRAFT` with one or more evidence records.
2. It can become `SUPPORTED` only when each citation has an extracted supporting span or deterministic extraction path.
3. It can become `CANON` only when it has **three independent evidence roots**, all current, and none are `U0` or unreviewed `I0`.
4. An explicit controlling-authority statement may be labeled `AUTHORITATIVE_SINGLE_SOURCE`, but remains below `CANON` under the strict corpus policy.
5. A claim with time-sensitive content must include `valid_from`, `valid_to` or `superseded_by`, and `freshness.stale_after`.
6. A contradiction never deletes losing evidence. It moves all competing claims into a `conflict_set`, records their scopes, and selects an active claim only under an explicit policy.

<INFERENCE from="[Evidence-dependence research; provenance and contradiction-management literature]">Three independent roots is a governance threshold, not an empirically universal law of truth. It is appropriate as a conservative canonicalization gate because it prevents one vendor assertion, one copied article, and one LLM paraphrase from counting as corroboration.</INFERENCE> [escholarship.org](https://escholarship.org/uc/item/7jt638nj) ([escholarship.org](https://escholarship.org/uc/item/7jt638nj?utm_source=openai))

#### Independence: how to avoid false corroboration

Two sources are **not independent** merely because they have different URLs. They share an `independence_root` if they derive from the same underlying assertion, data, editorial pipeline, press release, artifact, or model output.

Examples:

| Candidate evidence pair | Independent? | Reason |
|---|---|---|
| Apple HIG and Apple WWDC transcript | No, for external factual corroboration | Same publisher/control authority; useful triangulation, one root |
| Apple UI kit and extractor output from that kit | No | Extractor is a transformation of the same bytes |
| Figma REST response and the same file exported as `.fig` | No | Same document origin |
| Two articles repeating an Apple announcement | No | Likely shared press-release/root source |
| Apple HIG and an independently conducted reproducible measurement of a released app | Partially | Distinct observation pipelines; different claim types still matter |
| Two peer-reviewed experiments with distinct datasets and teams | Usually yes | Verify data/code lineage before counting |

Ignoring source dependence causes double counting and overconfidence; controlled evidence research explicitly warns that dependent evidence has less probative value than independent evidence. [escholarship.org](https://escholarship.org/uc/item/7jt638nj) ([escholarship.org](https://escholarship.org/uc/item/7jt638nj?utm_source=openai))

#### Deduplication and content-addressed evidence

Store every acquired input as immutable bytes under its SHA-256 digest, with normalized metadata stored separately. Content-addressed Merkle-DAG systems demonstrate the relevant principle: identity is content-derived and links are hashes, enabling reproducible references and tamper detection. [spec.filecoin.io](https://spec.filecoin.io/libraries/ipld/) ([spec.filecoin.io](https://spec.filecoin.io/libraries/ipld/?utm_source=openai))

Recommended identity fields:

```json
{
  "evidence_id": "sha256:...",
  "bytes_sha256": "…",
  "semantic_fingerprint": "…",
  "source_url": "…",
  "publisher": "Apple",
  "independence_root": "apple:hig:materials:2025-06-09",
  "retrieved_at": "…",
  "freshness": {
    "observed_at": "…",
    "stale_after": "…"
  },
  "trust_boundary": "THIRD_PARTY_UNTRUSTED_DATA"
}
```

Use two deduplication passes:

- **Byte identity:** SHA-256 of original asset/page/API body.
- **Semantic near-duplicate identity:** normalized claim tuple `(subject, predicate, object, qualifiers, temporal scope)`, but retain every original evidence object.

<INFERENCE from="[Content-addressed identity; provenance rerun/undo requirements]">Never merge away provenance merely because two claims normalize to the same semantic tuple. Deduplicate storage and retrieval; preserve evidentiary history.</INFERENCE> [spec.filecoin.io](https://spec.filecoin.io/libraries/ipld/) ([spec.filecoin.io](https://spec.filecoin.io/libraries/ipld/?utm_source=openai)) [link.springer.com](https://link.springer.com/article/10.1007/s13222-023-00463-0) ([link.springer.com](https://link.springer.com/article/10.1007/s13222-023-00463-0?utm_source=openai))

#### Executable invariant checker

The following checker validates the canonical JSON claim store. It intentionally does **not** parse prose to discover requirements. Markdown reports are generated outputs and may fail a freshness check, but they cannot create, promote, or delete knowledge.

```python
#!/usr/bin/env python3
"""
check_corpus.py CORPUS_DIR

Expected:
  evidence/*.json
  claims/*.json
  emitted/*.json

Each claim needs:
  id, statement, status, mark, evidence_ids, valid_from, freshness
Each evidence needs:
  id, bytes_sha256, independence_root, mark, trust_boundary, retrieved_at
"""
from __future__ import annotations
import json, sys
from datetime import datetime, timezone
from pathlib import Path

MARKS = {
    "P0", "P1", "P2", "P3", "S0", "S1", "S2", "I0", "U0"
}
CANON_ALLOWED = {"P0", "P1", "P2", "S0", "S1"}
UNTRUSTED = "THIRD_PARTY_UNTRUSTED_DATA"

def load_dir(path: Path):
    rows = {}
    for f in sorted(path.glob("*.json")):
        obj = json.loads(f.read_text(encoding="utf-8"))
        if obj.get("id") in rows:
            raise ValueError(f"duplicate id {obj['id']}")
        rows[obj["id"]] = obj
    return rows

def fail(errors, msg): errors.append(msg)

def has_freshness(obj):
    f = obj.get("freshness", {})
    return isinstance(f, dict) and bool(f.get("emitted_at") or f.get("observed_at"))

def main(root: Path):
    errors = []
    evidence = load_dir(root / "evidence")
    claims = load_dir(root / "claims")
    emitted = load_dir(root / "emitted")

    for eid, e in evidence.items():
        if e.get("mark") not in MARKS:
            fail(errors, f"{eid}: invalid evidence mark")
        if not e.get("bytes_sha256"):
            fail(errors, f"{eid}: missing immutable byte hash")
        if not e.get("independence_root"):
            fail(errors, f"{eid}: missing independence_root")
        if e.get("trust_boundary") != UNTRUSTED:
            fail(errors, f"{eid}: all ingested source data must be untrusted")
        if not e.get("retrieved_at"):
            fail(errors, f"{eid}: missing retrieval time")

    for cid, c in claims.items():
        if c.get("mark") not in MARKS:
            fail(errors, f"{cid}: invalid claim mark")
        if not c.get("statement") or not c.get("valid_from"):
            fail(errors, f"{cid}: missing atomic statement or temporal scope")
        if not has_freshness(c):
            fail(errors, f"{cid}: missing freshness stamp")

        refs = c.get("evidence_ids", [])
        if not refs or any(r not in evidence for r in refs):
            fail(errors, f"{cid}: missing or dangling evidence reference")
            continue

        roots = {evidence[r]["independence_root"] for r in refs}
        evidence_marks = {evidence[r]["mark"] for r in refs}

        if c.get("status") == "CANON":
            if len(roots) < 3:
                fail(errors, f"{cid}: CANON needs >=3 independent roots; got {len(roots)}")
            if c.get("mark") not in CANON_ALLOWED:
                fail(errors, f"{cid}: non-promotable claim mark cannot be CANON")
            if "U0" in evidence_marks or "I0" in evidence_marks:
                fail(errors, f"{cid}: CANON cannot depend on U0/I0 evidence")

        if c.get("mark") == "I0" and not c.get("derived_from_claim_ids"):
            fail(errors, f"{cid}: inference missing parent-claim chain")

    # Contradictions: same claim_key/polarity differs; evidence must survive in a conflict set.
    groups = {}
    for cid, c in claims.items():
        key = c.get("claim_key")
        if key:
            groups.setdefault(key, []).append((cid, c))
    for key, group in groups.items():
        polarities = {c.get("polarity") for _, c in group}
        if len(polarities) > 1:
            if not all(c.get("conflict_set_id") for _, c in group):
                fail(errors, f"{key}: contradictory claims lack conflict_set_id")

    for fid, f in emitted.items():
        if not has_freshness(f):
            fail(errors, f"emitted/{fid}: missing freshness stamp")
        if not f.get("source_snapshot_hashes"):
            fail(errors, f"emitted/{fid}: missing source snapshot hashes")

    if errors:
        print("CORPUS INVALID:")
        print("\n".join(f" - {x}" for x in errors))
        raise SystemExit(1)
    print(f"OK: {len(evidence)} evidence, {len(claims)} claims, {len(emitted)} emitted files")

if __name__ == "__main__":
    main(Path(sys.argv[1]))
```

<INFERENCE from="[Provenance management; source-support verification; model-collapse and contradiction benchmark evidence]">A deterministic checker cannot prove that a claim is true, but it can prevent mechanically detectable drift: dangling citations, stale outputs, self-citation, untyped inferences, unmarked conflicts, loss of provenance, and unsupported promotion.</INFERENCE> [journals.sagepub.com](https://journals.sagepub.com/doi/10.3233/SW-233467) ([journals.sagepub.com](https://journals.sagepub.com/doi/10.3233/SW-233467?utm_source=openai)) [proceedings.neurips.cc](https://proceedings.neurips.cc/paper_files/paper/2024/hash/c63819755591ea972f8570beffca6b1b-Abstract-Datasets_and_Benchmarks_Track.html) ([proceedings.neurips.cc](https://proceedings.neurips.cc/paper_files/paper/2024/hash/c63819755591ea972f8570beffca6b1b-Abstract-Datasets_and_Benchmarks_Track.html?utm_source=openai))

#### Prompt-injection fence

| Pipeline stage | Mandatory fence |
|---|---|
| Download / upload | Mark all input bytes `THIRD_PARTY_UNTRUSTED_DATA`; hash before parsing |
| OCR / screenshot text | Preserve text as quoted data; never execute or obey instructions found in it |
| `.sketch` / `.fig` parsing | Use no-network, no-secret, least-privilege subprocess; enforce archive size/path limits |
| LLM review | Give model only a bounded data projection; state that retrieved content has zero authority to change policy |
| Promotion | Only deterministic validator can write `CANON`; model output may create `U0` drafts only |
| Corpus write | Append evidence; use reviewable patches for claim state transitions; require checker pass |
| Rendering | Isolate renderer; no shell invocation from document fields, URLs, font names, or layer metadata |
| Re-ingestion of prior sessions | Treat all prior output as `U0` unless it links to preserved primary evidence |

Indirect prompt injection is not a hypothetical edge case: the InjecAgent benchmark evaluates attacks where instructions embedded in external content manipulate tool-integrated agents. Persistent memory creates an additional route for poisoning later work. [aclanthology.org](https://aclanthology.org/2024.findings-acl.624/) ([aclanthology.org](https://aclanthology.org/2024.findings-acl.624/?utm_source=openai)) [arxiv.org](https://arxiv.org/abs/2607.14611) ([arxiv.org](https://arxiv.org/abs/2607.14611?utm_source=openai))

#### Failure modes and negative results

| Failure mode | Evidence | Required response |
|---|---|---|
| Model-generated corpus becomes its own evidence | Recursive/self-consuming model research finds degradation of diversity, tails, or quality without sufficient fresh real data | Prior-session prose is `U0`; preserve only its cited evidence |
| Correlated citations look like corroboration | Dependence research warns of double counting dependent evidence | Enforce `independence_root`; three URLs are not automatically three roots |
| Citation exists but does not support claim | Source-verification research exists precisely because documented provenance may not support a KG triple | Require support spans/extraction paths |
| Contradictions silently collapse to latest ingest | KG systems can contain conflicting facts and lack evidence for resolution | Preserve all claims in `conflict_set`; select active state separately |
| LLM contradiction detection is imperfect | WikiContradict was introduced because real-world knowledge conflicts expose model limitations | Use model detection for triage, deterministic/curated adjudication for state changes |
| Local Figma parser breaks on format change | Reverse-engineering authors explicitly describe `.fig` as unstable internal format | Treat parser output as `S2`; compare to API/render outputs |
| Screenshot measurement creates false precision | Adaptive materials and font rendering vary by content/settings | Classify values as `P3`; never upgrade to a global token without normative evidence |
| Prompt injection persists through memory | Tool-integrated agent and memory-poisoning research | Data-only quarantine and validator-only promotion |

[nature.com](https://www.nature.com/articles/s41586-024-07566-y) ([rivista.ai](https://www.rivista.ai/wp-content/uploads/2024/08/s41586-024-07566-y-1.pdf?utm_source=openai)) [arxiv.org](https://arxiv.org/abs/2311.16822) ([arxiv.org](https://arxiv.org/abs/2311.16822?utm_source=openai)) [escholarship.org](https://escholarship.org/uc/item/7jt638nj) ([escholarship.org](https://escholarship.org/uc/item/7jt638nj?utm_source=openai)) [journals.sagepub.com](https://journals.sagepub.com/doi/10.3233/SW-233467) ([journals.sagepub.com](https://journals.sagepub.com/doi/10.3233/SW-233467?utm_source=openai)) [proceedings.neurips.cc](https://proceedings.neurips.cc/paper_files/paper/2024/hash/c63819755591ea972f8570beffca6b1b-Abstract-Datasets_and_Benchmarks_Track.html) ([proceedings.neurips.cc](https://proceedings.neurips.cc/paper_files/paper/2024/hash/c63819755591ea972f8570beffca6b1b-Abstract-Datasets_and_Benchmarks_Track.html?utm_source=openai)) [madebyevan.com](https://madebyevan.com/figma/fig-file-parser/) ([madebyevan.com](https://madebyevan.com/figma/fig-file-parser/?utm_source=openai)) [aclanthology.org](https://aclanthology.org/2024.findings-acl.624/) ([aclanthology.org](https://aclanthology.org/2024.findings-acl.624/?utm_source=openai))

---

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| Liquid Glass is for controls/navigation, not ordinary content-layer use; regular and clear variants exist | Apple HIG: Materials | June 9, 2025 update; live | Official normative guidance | https://developer.apple.com/design/human-interface-guidelines/materials |
| Clear Liquid Glass over bright content may need a 35% dark dimming layer | Apple HIG: Materials | June 9, 2025 update; live | Official quantitative guidance | https://developer.apple.com/design/human-interface-guidelines/materials |
| macOS type ramp includes Body 13/16 pt and minimum recommended size 10 pt | Apple HIG: Typography | n.d.; live | Official metric table | https://developer.apple.com/design/human-interface-guidelines/typography |
| Toolbars live at the top of macOS windows and cannot be sole command access | Apple HIG: Toolbars | Updated December 16, 2025 | Official normative guidance | https://developer.apple.com/design/human-interface-guidelines/toolbars |
| Sidebars float over content in Liquid Glass; content should extend behind | Apple HIG: Sidebars | June 9, 2025 update | Official normative guidance | https://developer.apple.com/design/human-interface-guidelines/sidebars |
| Concentric radius is container radius minus corner distance | Apple SwiftUI API: `Edge.Corner.Style.concentric` | n.d.; live | Official API contract | https://developer.apple.com/documentation/swiftui/edge/corner/style/concentric |
| macOS 26 controls gained extra-large size; mini/small/medium became taller; large/extra-large are capsules | WWDC25: Build an AppKit app with the new design | June 2025 | Official implementation session | https://developer.apple.com/videos/play/wwdc2025/310/ |
| macOS 27 adds interactive glass and AppKit concentricity API; sidebars reach window edges | WWDC26: Modernize your AppKit app | June 2026 | Official implementation session | https://developer.apple.com/videos/play/wwdc2026/289/ |
| macOS 27 Apple design kits for Figma and Sketch were announced | Apple Developer News | June 23, 2026 | Official release announcement | https://developer.apple.com/news/ |
| `.sketch` is ZIP + JSON/assets and uses `meta.json`, `document.json`, `pages` | Sketch Developer File Format | n.d.; live | Official format documentation | https://developer.sketch.com/file-format/ |
| Sketch schema/versioning is separately published and versioned | Sketch Developer Specification | n.d.; live | Official schema contract | https://developer.sketch.com/file-format/spec |
| `fixedRadius` and point `cornerRadius` are generic numbers, not formal sentinel values | Sketch schema repository | Current repository snapshot | Official schema source | https://github.com/sketch-hq/sketch-document |
| Figma file endpoint exposes document content and component/style maps | Figma REST file endpoints | n.d.; live | Official API contract | https://developers.figma.com/docs/rest-api/file-endpoints/ |
| Figma rate limits for file endpoints are tier-, plan-, and seat-dependent | Figma REST rate limits | Updated November 17, 2025 | Official API operational contract | https://developers.figma.com/docs/rest-api/rate-limits/ |
| `.fig` parsing is reverse-engineered and format stability is not guaranteed | Evan Wallace’s parser write-up | n.d.; live | Secondary technical reverse engineering | https://madebyevan.com/figma/fig-file-parser/ |
| Provenance supports KG rerun, undo, and retrieval | Kleinsteuber et al. | February 5, 2024 | Peer-reviewed research | https://link.springer.com/article/10.1007/s13222-023-00463-0 |
| Provenance can be checked for whether it supports KG triples | Amaral, Rodrigues, Simperl, ProVe | September 12, 2023 | Peer-reviewed research | https://journals.sagepub.com/doi/10.3233/SW-233467 |
| Dependent evidence can be double-counted and inflate belief | Strittmatter, Pilditch, Lagnado | 2024 | Academic research | https://escholarship.org/uc/item/7jt638nj |
| Recursive model-generated training can produce model collapse | Shumailov et al. | July 25, 2024 | Nature research | https://www.nature.com/articles/s41586-024-07566-y |
| Tool-integrated agents are vulnerable to indirect prompt injection in external content | Zhan et al., InjecAgent | 2024 | ACL Findings benchmark | https://aclanthology.org/2024.findings-acl.624/ |

---

## Knowledge Gaps

### Apple specification gaps

- `<MISSING_DATA>[A public Apple token table for Liquid Glass blur radius, refraction/lensing coefficients, shadow parameters, opacity curves, and exact dynamic tint rules. Apple publishes semantic behavior, not these constants.]</MISSING_DATA>`

- `<MISSING_DATA>[A stable public Apple control-height table for macOS 26/27 mini, small, regular, large, and extra-large controls. Apple explicitly advises avoiding hard-coded heights.]</MISSING_DATA>`

- `<MISSING_DATA>[Immutable HIG revision IDs and full page-by-page historical version archives. Apple exposes selected update dates but live pages are mutable.]</MISSING_DATA>`

### Sketch format gaps

- `<INSUFFICIENT_EVIDENCE>[A documented universal Sketch capsule-radius sentinel. Current official schema only specifies numeric fields; a version-specific corpus of verified source files and exports is required.]</INSUFFICIENT_EVIDENCE>`

- `<MISSING_DATA>[A vendor document mapping every historical Sketch document-version integer to all UI feature semantics.]</MISSING_DATA>`

### Figma gaps

- `<MISSING_DATA>[An official public `.fig` binary/container specification. Figma offers REST contracts, not a local file-format contract.]</MISSING_DATA>`

- `<INSUFFICIENT_EVIDENCE>[A stable guarantee that a local `.fig` parser reproduces Figma’s renderer exactly for all effects, fonts, masks, blend modes, variables, and prototypes.]</INSUFFICIENT_EVIDENCE>`

### Corpus-governance gaps

- `<INSUFFICIENT_EVIDENCE>[An empirical result proving that three independent sources is universally optimal. It is a conservative governance threshold, not a discovered natural constant.]</INSUFFICIENT_EVIDENCE>`

- `<CONFLICTING_EVIDENCE>[Recursive synthetic-data research finds collapse/degradation under some self-consuming regimes, whereas other work finds stability or mitigation when sufficient fresh real data, curation, or controlled mixture policies are present. This supports a no-self-certification policy, not a claim that all synthetic assistance is unusable.]</CONFLICTING_EVIDENCE>` [nature.com](https://www.nature.com/articles/s41586-024-07566-y) ([rivista.ai](https://www.rivista.ai/wp-content/uploads/2024/08/s41586-024-07566-y-1.pdf?utm_source=openai)) [openreview.net](https://openreview.net/forum?id=aw6L8sB2Ts) ([openreview.net](https://openreview.net/forum?id=aw6L8sB2Ts&utm_source=openai))

---

## Recommended Next Steps

1. **Download and hash the current macOS 27 Sketch and Figma kits; create an artifact manifest.**  
   **Rationale:** this converts Apple’s June 23, 2026 announcement into reproducible, version-scoped evidence and permits direct extraction of current names, component states, shared styles, and bounds. [developer.apple.com](https://developer.apple.com/news/) ([developer.apple.com](https://developer.apple.com/news/?utm_source=openai))

2. **Run a controlled Sketch radius experiment across the exact target Sketch version.**  
   Create rectangles and vector paths at known dimensions with inspector radii `0`, `r`, `min(width,height)/2`, greater-than-half, and any observed candidate sentinel; save, extract, render, and record behavior.  
   **Rationale:** this is the only defensible route to a version-scoped capsule encoding rule.

3. **Implement the evidence/claim store and invariant checker before allowing multi-session writing.**  
   **Rationale:** retrofitting provenance, conflict preservation, and freshness after prose accumulation is substantially harder than enforcing them at ingestion. [link.springer.com](https://link.springer.com/article/10.1007/s13222-023-00463-0) ([link.springer.com](https://link.springer.com/article/10.1007/s13222-023-00463-0?utm_source=openai))

4. **Create a Figma API collector with cache, `Retry-After` handling, and full response hashing.**  
   **Rationale:** Figma’s file APIs are the vendor-supported representation, but Tier 1 limits make request batching and cache-first collection operationally necessary. [developers.figma.com](https://developers.figma.com/docs/rest-api/rate-limits/) ([developers.figma.com](https://developers.figma.com/docs/rest-api/rate-limits/?utm_source=openai))

5. **Red-team ingestion with malicious layer names, OCR text, `userInfo`, URLs, and prior-session Markdown.**  
   **Rationale:** the corpus’s most credible integrity failure is not malformed JSON; it is third-party content persuading the agent to alter policy, leak data, or promote unsupported claims. [aclanthology.org](https://aclanthology.org/2024.findings-acl.624/) ([aclanthology.org](https://aclanthology.org/2024.findings-acl.624/?utm_source=openai))

## Sources

- [Apple Design Resources - Apple Developer](https://developer.apple.com/design/resources/)
- [Latest News - Apple Developer](https://developer.apple.com/news/?utm_source=openai)
- [Materials | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/materials?utm_source=openai)
- [concentric | Apple Developer Documentation](https://developer.apple.com/documentation/swiftui/edge/corner/style/concentric?utm_source=openai)
- [Sketch Developer — File format](https://developer.sketch.com/file-format/?utm_source=openai)
- [Sketch Developer — Specification](https://developer.sketch.com/file-format/spec?utm_source=openai)
- [https://raw.githubusercontent.com/sketch-hq/sketch-document/main/packages/file-format/schema/layers/rectangle.schema.yaml](https://raw.githubusercontent.com/sketch-hq/sketch-document/main/packages/file-format/schema/layers/rectangle.schema.yaml)
- [https://raw.githubusercontent.com/sketch-hq/sketch-document/main/packages/file-format/schema/objects/curve-point.schema.yaml](https://raw.githubusercontent.com/sketch-hq/sketch-document/main/packages/file-format/schema/objects/curve-point.schema.yaml)
- [Endpoints | Developer Docs](https://developers.figma.com/docs/rest-api/file-endpoints/?utm_source=openai)
- [Components and styles | Developer Docs](https://developers.figma.com/docs/rest-api/component-types/?utm_source=openai)
- [Figma .fig file format parser online](https://madebyevan.com/figma/fig-file-parser/?utm_source=openai)
- [Managing Provenance Data in Knowledge Graph Management Platforms | Datenbank-Spektrum | Springer ...](https://link.springer.com/article/10.1007/s13222-023-00463-0?utm_source=openai)
- [IPLD | Filecoin Spec](https://spec.filecoin.io/libraries/ipld/?utm_source=openai)
- [AI models collapse when trained on recursively generated data](https://www.rivista.ai/wp-content/uploads/2024/08/s41586-024-07566-y-1.pdf?utm_source=openai)
- [Large Language Models Suffer From Their Own Output: An Analysis of the Self-Consuming Training Loop](https://arxiv.org/abs/2311.16822?utm_source=openai)
- [Self-Consuming Generative Models Go MAD](https://proceedings.iclr.cc/paper_files/paper/2024/hash/ebc042e767de551803ccfcc45e2454f5-Abstract-Conference.html?utm_source=openai)
- [InjecAgent: Benchmarking Indirect Prompt Injections in Tool-Integrated Large Language Model Agent...](https://aclanthology.org/2024.findings-acl.624/?utm_source=openai)
- [Bad Memory: Evaluating Prompt Injection Risks from Memory in Agentic Systems](https://arxiv.org/abs/2607.14611?utm_source=openai)
- [What’s new - Design - Apple Developer](https://developer.apple.com/design/whats-new?q=vision&utm_source=openai)
- [Typography | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/typography?changes=_5&utm_source=openai)
- [Toolbars | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/toolbars?changes=_2&utm_source=openai)
- [Sidebars | Apple Developer Documentation](https://developer.apple.com/design/human-interface-guidelines/sidebars?changes=_8&utm_source=openai)
- [Meet Liquid Glass - WWDC25 - Videos - Apple Developer](https://developer.apple.com/videos/play/wwdc2025/219/?utm_source=openai)
- [Build an AppKit app with the new design - WWDC25 - Videos - Apple Developer](https://developer.apple.com/videos/play/wwdc2025/310/?time=210)
- [Modernize your AppKit app - WWDC26 - Videos - Apple Developer](https://developer.apple.com/videos/play/wwdc2026/289/?utm_source=openai)
- [NSGlassEffectView | Apple Developer Documentation](https://developer.apple.com/documentation/appkit/nsglasseffectview?changes=_1&utm_source=openai)
- [AppKit updates | Apple Developer Documentation](https://developer.apple.com/documentation/updates/appkit?changes=latest_ma_3&utm_source=openai)
- [@sketch-hq/sketch-file-format - npm](https://www.npmjs.com/package/%40sketch-hq/sketch-file-format?utm_source=openai)
- [UNPKG](https://app.unpkg.com/%40sketch-hq/sketch-file-format%403.6.2/files/dist/file-format.schema.json?utm_source=openai)
- [Open format: how to read Sketch files and convert to JSON · Sketch Blog](https://www.sketch.com/blog/open-format-reading-sketch-file-sketch-to-json/?utm_source=openai)
- [GitHub - sketch-hq/sketch-document: Monorepo for Sketch document JSON Schemas and TypeScript type...](https://github.com/sketch-hq/sketch-document?utm_source=openai)
- [https://raw.githubusercontent.com/sketch-hq/sketch-document/main/packages/file-format/schema/enums/points-radius-behaviour.schema.yaml](https://raw.githubusercontent.com/sketch-hq/sketch-document/main/packages/file-format/schema/enums/points-radius-behaviour.schema.yaml)
- [Rate Limits | Developer Docs](https://developers.figma.com/docs/rest-api/rate-limits/?utm_source=openai)
- [openfig-core/README.md at main · OpenFig-org/openfig-core · GitHub](https://github.com/OpenFig-org/openfig-core/blob/main/README.md?utm_source=openai)
- [ProVe: A pipeline for automated provenance verification of knowledge graphs against textual sourc...](https://journals.sagepub.com/doi/10.3233/SW-233467?utm_source=openai)
- [Reasoning about (In)Dependent Evidence: A Mismatch between Perceiving and Incorporating Dependenc...](https://escholarship.org/uc/item/7jt638nj?utm_source=openai)
- [WikiContradict: A Benchmark for Evaluating LLMs on Real-World Knowledge Conflicts from Wikipedia](https://proceedings.neurips.cc/paper_files/paper/2024/hash/c63819755591ea972f8570beffca6b1b-Abstract-Datasets_and_Benchmarks_Track.html?utm_source=openai)
- [Towards Theoretical Understandings of Self-Consuming Generative Models | OpenReview](https://openreview.net/forum?id=aw6L8sB2Ts&utm_source=openai)
