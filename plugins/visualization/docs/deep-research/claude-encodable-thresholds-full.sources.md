# Sources — visualisation and diagram quality: encodable thresholds

Retrieved 2026-08-30. Every entry below was fetched and text-extracted directly unless marked otherwise.
Retrieval method is recorded because it bounds how far a quoted number can be trusted.

## Retrieved as full text (curl + pdftotext, or W3C HTML)

| # | Source | Type | Retrieval | Used for |
|---|---|---|---|---|
| 1 | Szafir, "Modeling Color Difference for Visualization Design", IEEE TVCG 2018 — https://danielleszafir.com/colordiff_vis2017.pdf | Peer-reviewed | Full text | ND(50%) tables, per-mark regression models, 2:1 elongation asymptote, 461 participants |
| 2 | Petroff, "Accessible Color Sequences for Data Visualization", 2021 — https://arxiv.org/pdf/2107.02270 | Peer-reviewed | Full text | CAM02-UCS min distances 20/18/16, ΔJ′ 5.0/4.2/3.6, J′ ranges, Machado-on-linear-sRGB, WCAG-unfit-for-viz argument |
| 3 | Gramazio, Laidlaw & Schloss, "Colorgorical", IEEE TVCG 23(1) 2017 — https://gramaz.io/pdf/gramazio-2016-ccd.pdf | Peer-reviewed | Full text | ΔL/Δa/Δb noticeable-difference intervals, L*∈[25,85], dark-yellow exclusion, CIEDE2000 + Name Difference, 22-colour ceiling |
| 4 | Heer & Bostock, "Crowdsourcing Graphical Perception", CHI 2010 — https://www.cs.kent.edu/~javed/class-P2P12F/papers-2012/PAPER2012-2010-MTurk-CHI.pdf | Peer-reviewed | Full text | log-error measure, ranking replication, angle-vs-length non-result, 1:1 aspect ratio worst |
| 5 | Saket, Endert & Demiralp, "Task-Based Effectiveness of Basic Visualizations", TVCG 2019 — https://arxiv.org/pdf/1709.08546 | Peer-reviewed | Full text | Task-conditional effectiveness, perceived≠actual accuracy, pie-chart counter-literature |
| 6 | Correll, Bertini & Franconeri, "Truncating the Y-Axis: Threat or Menace?", CHI 2020 — https://arxiv.org/pdf/1907.02035 | Peer-reviewed | Full text | F(2,76)=89; F(1,38)=0.5 p=0.50; mitigation F(2,60)=3.1 p=0.05 |
| 7 | "Revisiting Categorical Color Perception in Scatterplots", 2024 — https://arxiv.org/pdf/2404.03787 | Peer-reviewed | Full text | Palette-family accuracies 91.44/86.78/86.67/82.56/81.11%; F(8,91)=20.68 |
| 8 | Crameri, Shephard & Heron, *Nature Communications* 11:5444, 2020 — https://www.nature.com/articles/s41467-020-19160-7.pdf | Peer-reviewed | Full text | Rainbow distortion, 0.5%/8% CVD prevalence, viridis/cividis/batlow |
| 9 | McNutt & Kindlmann, "Linting for Visualization", VisGuides @ IEEE VIS 2018 — https://c4pgv.dbvis.de/McNutt_Kindlmann_2018.pdf | Peer-reviewed workshop | Full text | Computational + algebraic rule taxonomy, vislint_mpl, worked failure example |
| 10 | McNutt, Kindlmann & Correll, "Surfacing Visualization Mirages", CHI 2020 — https://arxiv.org/pdf/2001.02316 | Peer-reviewed | Full text | Metamorphic testing families; Shuffle negative result; 600 simulated charts |
| 11 | Chen et al., "VizLinter", IEEE TVCG 2021 — https://arxiv.org/pdf/2108.10299 | Peer-reviewed | Full text | 41 rules from Draco, ASP + LP fixer, 20-participant study |
| 12 | Moritz et al., "Formalizing Visualization Design Knowledge as Constraints: Draco", InfoVis/TVCG 2019 — https://idl.cs.washington.edu/files/2019-Draco-InfoVis.pdf | Peer-reviewed | Full text | Hard/soft constraints, weights learned from perception experiments |
| 13 | Chen et al., "VisEval", IEEE VIS / TVCG 2024 — https://arxiv.org/html/2407.00981v1 | Peer-reviewed benchmark | Full text (HTML) | Per-model invalid/illegal/pass tables, checker architecture, judge validation + ablation |
| 14 | "VisCoder: Fine-Tuning LLMs for Executable Python Visualization Code Generation", EMNLP Findings 2025 — https://arxiv.org/pdf/2506.03930 | Peer-reviewed | Full text | Self-debug exec-pass deltas, error-type transitions |
| 15 | Yang et al., "MatPlotAgent / MatPlotBench", 2024 — https://arxiv.org/pdf/2402.11453 | Peer-reviewed | Full text | +12.30 / +13.21 agent gains; GPT-4V judge r=0.876 |
| 16 | Yang et al., "ChartMimic", ICLR 2025 — https://arxiv.org/pdf/2406.09961 | Peer-reviewed | Full text | Code-tracer low-level metrics, CLIP-Score rejection, GPT-4o 81.2 |
| 17 | "How Good (Or Bad) Are LLMs at Detecting Misleading Visualizations?", 2024 — https://arxiv.org/pdf/2407.17291 | Peer-reviewed | Full text | Precision/recall imbalance, 78% midpoint, 99% "misleading", 5→21 issue degradation |
| 18 | Ge, Cui & Kay, "CALVI", CHI 2023 — https://mucollective.northwestern.edu/files/2023-CALVI.pdf | Peer-reviewed | Full text | 11-misleader taxonomy with definitions, 45-item bank, ω=0.81, 497 participants |
| 19 | Lee, Pandey, Kwon & Ottley, "Mini-VLAT", EuroVis/CGF 2023 — https://washuvis.github.io/minivlat/Mini-VLAT_EuroVIS.pdf | Peer-reviewed | Full text | ω=0.72, CVR 0.6, 5 min vs 22 min, VLAT 53 items |
| 20 | Lundgard & Satyanarayan, "Accessible Visualization via Natural Language Descriptions", TVCG 2022 — https://arxiv.org/pdf/2110.04406 | Peer-reviewed | Full text | Four-level model, blind/sighted ranking divergence, 63% rejection of interpretation, ARIA L1–L2 recommendation |
| 21 | W3C, *Web Content Accessibility Guidelines 2.2* — https://www.w3.org/TR/WCAG22/ | W3C Recommendation (normative) | Fetched | 1.4.1, 1.4.3, 1.4.11, 1.4.13 verbatim |
| 22 | W3C, *WAI-ARIA Graphics Module 1.0* — https://www.w3.org/TR/graphics-aria-1.0/ | W3C Recommendation (normative) | Fetched | Three graphics roles, fallbacks, name/children-presentational semantics |
| 23 | Chartability POUR-CAF Workbook — https://chartability.github.io/POUR-CAF/ | Practitioner heuristic set, WCAG-derived | Fetched | 50 heuristics / 14 critical, all numeric criteria, 88% low-contrast failure rate |
| 24 | Ottosson, "A perceptual color space for image processing" (Oklab) — https://bottosson.github.io/posts/oklab/ | Author-published derivation with published error tables | Fetched | Space comparison table, CIELAB blue-hue defect, γ=0.323→1/3, matrices |
| 25 | Roselli, "WCAG 3 Contrast as of April 2026" — http://adrianroselli.com/2026/04/wcag3-contrast-as-of-april-2026.html | Practitioner analysis quoting the W3C Editor's Draft | Fetched | WCAG 3 contrast "yet to be determined"; APCA removal timeline |

## Retrieved as secondary summary only (lower confidence, flagged in the report)

| # | Source | Why it was used | Limitation |
|---|---|---|---|
| 26 | Elavsky, Bennett & Moritz, "How accessible is my visualization?", CGF 2022 — https://dig.cmu.edu/publications/2022-chartability.html | Per-system audit failure counts | Paper PDF not retrievable; arXiv identifiers tried resolved to unrelated papers. Counts marked `<CONFIDENCE:LOW>` |
| 27 | Purchase, "Which Aesthetic Has the Greatest Effect on Human Understanding?", GD 1997 — https://espace.library.uq.edu.au/view/UQ:8ead24b | Edge-crossing dominance for diagram layout | Springer chapter paywalled (303 to auth endpoint); mirrors returned non-PDF. Ranking used at Medium confidence, per-aesthetic statistics marked missing |

## Sources deliberately excluded

- Vendor blogs and BI tool comparisons (Tableau/Power BI/Looker) — out of scope per the brief. The Tableau Research blog post on y-axis truncation was skipped in favour of the CHI paper by the same author.
- SEO aggregators, "top 10 chart types" listicles, and design-tip blogs — no primary evidence.
- One search result on label-overlap thresholds returned an ungrounded model answer with no sources attached. It was discarded rather than cited, and the resulting hole is recorded as `<MISSING_DATA>` in the report.
- One search result on Oklab returned an ungrounded model answer; it was replaced by Ottosson's own post (#24) before any number was used.

## Retrieval failures worth recording

- `osf.io/preprints/psyarxiv/*/download` returned nothing for two attempted preprints; the arXiv versions were used instead.
- Several arXiv identifiers guessed from memory resolved to unrelated papers (astronomy, group theory, ML). Every downloaded PDF was header-checked before use, which is what caught them.
- `idl.uw.edu` paths for Kim & Heer (2018), "Assessing Effects of Task and Data Distribution on the Effectiveness of Visual Encodings", 404'd. That paper would have strengthened the task-conditional argument in §1 and is not represented.
