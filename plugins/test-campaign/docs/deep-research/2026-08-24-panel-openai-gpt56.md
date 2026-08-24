## Executive Summary

- **(High Confidence)** <INFERENCE from="the 110-fault Android data-loss benchmark; TimeMachine’s state-restoration experiments; RegDroid’s cross-version results">The principal residual risk is **temporal and historical incompleteness**, not surface or requirement incompleteness: defects dependent on a journey prefix, lifecycle transition, prior server commit, old persisted data, navigation history, or event ordering can remain unreachable when each surface/state combination is tested from a prepared starting point.</INFERENCE> A benchmark contains 110 real lifecycle-related data-loss faults across 48 Android apps, 98 with automated oracles.[Riganelli et al., 2019](https://arxiv.org/abs/1905.11040) ([arxiv.org](https://arxiv.org/abs/1905.11040))

- **(High Confidence)** The strongest near-term additions are: **journey-prefix interruption/process-death tests; previous-build differential testing with an explicit change-intent manifest; and end-to-end journeys whose oracle reconciles UI, local persistence, server state, and externally committed effects**. <INFERENCE from="TimeMachine’s defect yield, RegDroid’s yield and triage data, and the lifecycle benchmark">These have the best-supported marginal yield per engineering effort for a campaign already strong on static factors and isolated effects.</INFERENCE>

- **(Medium Confidence)** Sequence covering arrays address a real hole that ordinary t-way factor sampling does not: they cover the relative order of every selected t-event subset. However, the empirical evidence is old and narrow. One analysis classified 49 of 592 Android vulnerabilities as sequence-triggered; about 90% were representable by three-event orderings and all by four-event orderings, assuming a correct event model.[Srinivasan, 2018 thesis](https://oaktrust.library.tamu.edu/server/api/core/bitstreams/63e58062-7474-48ec-830e-9b7324ebfb9c/content) ([oaktrust.library.tamu.edu](https://oaktrust.library.tamu.edu/server/api/core/bitstreams/63e58062-7474-48ec-830e-9b7324ebfb9c/content)) They do **not** guarantee adjacency, repeated-event, timing, concurrent-event, or omitted-event coverage.

- **(High Confidence)** Back-to-back testing against the previous build is effective for **unspecified regression behavior**, but raw differences are not suitable as blocking failures. RegDroid tested 121 adjacent Android release pairs and produced 205 reports: 73 were judged true positives and 132 false positives, a reported 64% false-positive rate; 93% of the false positives were intended feature additions/removals and 7% were bug fixes.[Xiong et al., ISSTA 2023](https://tingsu.github.io/files/ISSTA23-functional-bugs.pdf) ([tingsu.github.io](https://tingsu.github.io/files/ISSTA23-functional-bugs.pdf?utm_source=openai)) The same experiment found 14 unique functional bugs, including 10 previously unknown bugs that developers confirmed and fixed.

- **(High Confidence)** LLM/VLM methods show a genuine advantage where the oracle requires **semantic interpretation**—meaningful input generation, business-scenario navigation, non-text accessibility judgments, or judging whether a visual transition makes functional sense. GenA11y reported 95.2% precision and 87.69% recall, versus 12.74% recall for axe-core, but its principal recall corpus was a curated set of 148 accessibility-issue pages.[He, Huq and Malek, FSE 2025](https://doi.org/10.1145/3729371) ([github.com](https://github.com/seal-hub/GenA11y?utm_source=openai)) <INFERENCE from="95.2% precision">Its reported false-discovery share was approximately 4.8%; the class-conditional false-positive rate was not reported.</INFERENCE>

- **(High Confidence)** VLMs do **not** outperform deterministic oracles for exact geometry, transaction reconciliation, state equality, telemetry contracts, permission state, timing bounds, resource slopes, or known accessibility-tree invariants. VisionDroid’s earlier evaluation reported absolute precision of roughly 50–76% and recall of 42–64% over three mixed datasets.[Liu et al., VisionDroid](https://arxiv.org/abs/2407.03037) ([researchgate.net](https://www.researchgate.net/publication/381960311_Vision-driven_Automated_Mobile_GUI_Testing_via_Multimodal_Large_Language_Model?utm_source=openai)) <INFERENCE from="reported precision of 50–76%">That corresponds to a 24–50% false-discovery share, so a model-only release gate is not justified.</INFERENCE>

- **(High Confidence)** There is direct evidence for adding record/replay robustness and event-race perturbation. A 2025 study found that 17% of user scenarios, 38% of non-crashing bugs, and 44% of crashing bugs in its corpus could not be reliably recorded and replayed.[Song et al., 2025 preprint](https://arxiv.org/abs/2504.20237) ([arxiv.org](https://arxiv.org/abs/2504.20237?utm_source=openai)) An ISSTA 2024 technique reproduced 73 of 80 timing-dependent flaky Android tests from 22 apps by delaying a relevant event, requiring 1.71 runs on average.[Cai et al., ISSTA 2024](https://doi.org/10.1145/3650212.3680377) ([2024.issta.org](https://2024.issta.org/details/issta-2024-papers/120/Reproducing-Timing-Dependent-GUI-Flaky-Tests-in-Android-Apps-via-a-Single-Event-Delay?utm_source=openai))

- **(Low Confidence)** `<MISSING_DATA>[Controlled defect-yield-per-engineering-hour studies were not found for pseudo-localisation, clock/timezone/DST manipulation, offline/reconnect state machines, upgrade paths, aged accounts, telemetry correctness, or resource-slope soak testing. Product-specific benchmarks with seeded and historical faults, execution cost, and blinded triage would be needed.]</MISSING_DATA>` These remain technically well-motivated additions, but their ranking below is a decision estimate rather than an empirical league table.

---

## Detailed Findings

### 1. Answer this decisively: What classes of user-visible defect escape a mature, requirement-driven UI test campaign, and what is the published evidence on the methods that catch them?

#### 1.1 Residual defect taxonomy

**(High Confidence)** <INFERENCE from="the lifecycle, sequence, differential, accessibility, race, and scenario-testing studies reviewed below">The escaped defects fall into six broad classes:</INFERENCE>

1. **History-dependent reachability defects** — the current screen is wrong only because of what happened several steps, sessions, devices, or versions earlier.
2. **Distributed-state divergence** — the client, server, secondary surface, and external effect disagree after retry, interruption, or partial completion.
3. **Ordering and timing defects** — the same events and factor values behave differently under another order, adjacency, repetition, or schedule.
4. **Evolutionary defects** — old persisted data, old accounts, or behavior retained from the previous build exposes a regression absent on clean installs.
5. **Semantic and assistive-technology defects** — the UI is structurally valid but nonsensical, misleading, unusable through a screen reader, or inconsistent with conventional user expectations.
6. **Endurance and environment-state defects** — correctness decays with elapsed time, resource accumulation, timezone transitions, network reconnection, or capability revocation.

| Residual defect class | Why the described campaign can still miss it | Concrete detection mechanism | Evidence strength |
|---|---|---|---|
| **Accumulated journey state** | A t-way row normally selects a starting state; it does not prove that the state was reached through a semantically valid history or that each prefix preserved hidden state. | Execute a real goal from a realistic account state; checkpoint the UI, local store, server ledger and side effects after every material step. Re-enter selected prefixes through back, reload, relaunch and deep link. | **Medium–High** |
| **Interruption/process-death loss** | Fault injection may test component errors without destroying and reconstructing the whole UI/process at each journey prefix. | At every prefix: background/foreground, activity/window recreation, process kill, OS reclaim simulation, relaunch and deterministic state reconciliation. | **High** |
| **Partial completion after server commit** | A screenshot or local outcome can show failure while the server has already committed, producing duplicate retry, lost receipt or phantom success defects. | Inject disconnect/crash immediately before request, after server commit, before response, and during local persistence. Query an independent server/effect ledger and retry with the same idempotency key. | **Medium; direct UI-yield data missing** |
| **Back/forward and deep-link history** | Route enumeration proves destinations exist, but not that history stacks, cold/warm links and modal ancestry are correct after a realistic prefix. | Generate journey-derived re-entry variants: browser back/forward, app back, cold deep link, warm deep link, foreground deep link and link after authentication expiry. | **Medium** |
| **Cross-surface staleness** | Each surface can pass against its own fixture while another device, window or web/native surface remains stale after an actual write. | Write on surface A; assert monotonic read-after-write visibility on B/C under cache, reconnect and background transitions. | **Medium; mostly systems rationale** |
| **Aged-account state** | State/data-shape matrices rarely reproduce years of events, legacy flags, feature migrations, large tombstone sets or partly completed workflows. | Replay or synthesize an event history, not merely a final database fixture; compare with a freshly created account having nominally equivalent visible data. | **Low empirical support** |
| **Upgrade-path defects** | Clean installation bypasses schema migration, serialization compatibility, stale caches and old keychain/preferences. | Install an old build, create representative state, install-over to the candidate, then verify launch, migration, authentication and critical journeys. | **Low empirical support; high plausibility** |
| **Event order/adjacency/repetition** | Ordinary t-way sampling covers factor combinations, not permutations or adjacency of actions. | Sequence covering arrays plus explicit adjacent pairs, repeated events, double-submit and cancel/back-during-load patterns. | **Medium** |
| **UI/event races** | Even a covered sequence may execute under only one scheduler interleaving. | Delay selected callbacks, network completions and lifecycle events; run bounded schedule permutations around shared GUI data. | **High for reproducibility; medium for discovery** |
| **Unspecified regression** | Requirement and design-of-record comparisons have no oracle for behavior omitted from both. | Run identical traces on N−1 and N; compare semantic UI state, accessible state, navigation, effects and latency, then reconcile against declared change intent. | **High** |
| **Semantic/common-sense defect** | Presence, visual structure and even effect checks can all pass while a result is inappropriate: wrong sort order, misleading price, wrong destination or nonsensical label. | VLM/LLM candidate oracle, domain properties, or human review; require deterministic confirmation wherever possible. | **Medium** |
| **Actual screen-reader behavior** | axe-like engines inspect rules and markup, not the complete spoken sequence, focus recovery, rotor grouping, announcement timing or modal confinement. | Drive the critical journey through the platform accessibility API or real screen reader; capture focus and announcement transcripts. | **Medium rationale; thin yield data** |
| **Locale expansion and bidi behavior** | Testing several real locales may miss maximum expansion, forced accents, missing-resource markers and mixed-direction text. | Pseudo-locales, bidi stress strings and hard-coded-string detection. | **Low published yield data** |
| **Time/DST defects** | Freshness testing does not necessarily cross midnight, leap boundaries, DST gaps/folds or timezone changes while the session remains open. | Virtual clock and timezone matrix; cross boundaries with pending schedules, sessions, caches and relative-time labels. | **Low published yield data** |
| **Offline/reconnect divergence** | Generic fault injection may test request failure without the complete offline → queued → reconnect → duplicate/out-of-order response state machine. | Model the connectivity state machine and inject transition at each transaction boundary; assert eventual convergence and no duplicate effect. | **Low–Medium** |
| **Permission/capability revocation** | Initial role/permission matrices do not prove graceful degradation when OS permission, camera, microphone, file access or notification capability disappears mid-operation. | Revoke capability after check but before use, while backgrounded, and during an in-flight operation. | **High for Android permission risk** |
| **Resource-slope/endurance defect** | A short functional pass can miss leaks, cache growth, listener accumulation, progressive jank and degradation after thousands of transitions. | Repeated representative journeys with RSS/heap/FD/GPU-handle/latency slopes, plateau tests and change-point alarms. | **Low controlled yield evidence** |
| **Telemetry correctness** | A user-visible effect can be correct while analytics are missing, duplicated, sequenced incorrectly, emitted without consent or attached to the wrong identity. | Route telemetry to a test collector; reconcile each UI action/effect ID with a versioned event contract and consent state. | **Low UI-literature support; mechanically testable** |

#### 1.2 Multi-step journeys, lifecycle transitions and persistent history

**(High Confidence)** The Android data-loss benchmark is the clearest evidence that interruption-sensitive faults constitute a separate defect class. It contains 110 reproducible real faults in 54 releases of 48 apps; every fault had an immediately visible effect, and 98 had an automated oracle such as verifying that entered form text survived rotation or resumption.[Riganelli et al., 2019](https://arxiv.org/abs/1905.11040) ([arxiv.org](https://arxiv.org/abs/1905.11040)) This is a benchmark, not a comparative yield trial: it proves prevalence and reproducibility, not how often a new sweep will find a bug in a mature portfolio.

**(High Confidence)** TimeMachine provides stronger comparative evidence that preserving and revisiting deep states changes test yield. Its evaluation used 68 open-source apps, five repetitions and a six-hour budget per tool/app configuration.[Dong et al., ICSE 2020](https://abhikrc.com/pdf/ICSE20TM.pdf) ([abhikrc.com](https://abhikrc.com/pdf/ICSE20TM.pdf)) It achieved 54% average statement coverage versus 51% for Sapienz, 45% for Stoat and 44% for Monkey, and found 199 unique crashes versus 140, 121 and 48 respectively.[Dong et al., ICSE 2020](https://doi.org/10.1145/3377811.3380402) ([abhikrc.com](https://abhikrc.com/pdf/ICSE20TM.pdf)) On 37 closed-source industrial apps it found 281 crashes, compared with 183 for the closest baseline and 15 for simple restart-on-stall.[Dong et al., ICSE 2020](https://abhikrc.com/pdf/ICSE20TM.pdf) ([abhikrc.com](https://abhikrc.com/pdf/ICSE20TM.pdf))

Its limitations are directly relevant: it ran on Android-x86 rather than physical devices, detected crashes rather than non-crashing correctness defects, did not provide logged-in states for some apps, and restored only client state—not remote server state.[Dong et al., limitations section](https://abhikrc.com/pdf/ICSE20TM.pdf) ([abhikrc.com](https://abhikrc.com/pdf/ICSE20TM.pdf)) <INFERENCE from="the stated remote-state limitation">Client snapshots therefore cannot be used as a complete oracle for partial-commit or cross-device journeys; the server/effect ledger must remain outside the restored snapshot.</INFERENCE>

**(Medium Confidence)** The strongest recent scenario-level evidence is ScenGen. The final 2026 report evaluated 99 app-scenario tasks across 92 mobile apps and ten scenario types, reporting 86.87% scenario coverage, 84.85% completion, 106 scenario-related bugs and 4.71 minutes average test-generation time.[Yu et al., ACM TOSEM 2026](https://doi.org/10.1145/3816025) ([conf.researchr.org](https://conf.researchr.org/details/ase-2026/ase-2026-journal-first/24/Scenario-Guided-LLM-based-Mobile-App-GUI-Testing?utm_source=openai)) Its three-author unanimous manual judgments, English-language app selection and expert-chosen scenarios limit generalisation.[Yu et al., experimental method](https://arxiv.org/abs/2506.05079) ([arxiv.org](https://arxiv.org/abs/2506.05079))

`<CONFLICTING_EVIDENCE>[The 2025 arXiv version reports 339 target-scenario crash reports and an 85.84% developer confirmation/fix rate, whereas the final 2026 abstract reports 106 scenario-related bugs. The accessible final abstract does not explain whether the difference is deduplication, revised experiments or a changed bug definition; the 339 figure should not be used as the final paper’s defect count.]</CONFLICTING_EVIDENCE>`[2025 preprint](https://arxiv.org/abs/2506.05079)[2026 final article](https://doi.org/10.1145/3816025) ([arxiv.org](https://arxiv.org/abs/2506.05079))

**(Medium Confidence)** Deep-link-assisted exploration is promising for hidden/re-entry states. Delm, a 2024 preprint integrating deep links with Monkey, reported relative improvements of 27.2% in activity coverage, 21.13% in method coverage and 23.81% in crash detection over its baselines.[Hu et al., 2024 preprint](https://arxiv.org/abs/2404.19307) ([arxiv.org](https://arxiv.org/abs/2404.19307?utm_source=openai)) The result concerns reachability and crashes, not correctness of back stacks or link semantics, and has not been established on iOS, macOS or web history APIs.

##### Methodological Comparison — deep-state and journey methods

| Study/method | Corpus and methodology | Main measured result | Significance/effect reporting | Important limitations |
|---|---|---|---|---|
| **Data Loss Benchmark** — Riganelli et al. | 110 real faults, 48 F-Droid apps; reproducible Appium tests | 98/110 faults received automatic oracles | No p-values, CIs or comparative effect size; dataset contribution | Selected open-source Android apps; 2018-era platform; no yield-per-hour comparison |
| **TimeMachine** — Dong et al. | 68 open-source and 37 closed-source apps; five six-hour runs for open-source comparisons | 199 crashes; 54% coverage, exceeding three baselines | Ratios and absolute differences reported; no inferential statistics identified in the paper | Crash oracle; Android-x86; remote state not restored |
| **ScenGen** — Yu et al. | 99 tasks, 92 real apps, ten expert-selected scenarios; multimodal agents with shared history | 86.87% scenario coverage, 84.85% completion; final report: 106 bugs | No CI, p-value or calibrated oracle error reported in accessible final abstract | Manual expert judgment; model/provider dependence; English apps; selected scenarios |
| **Delm** — Hu et al. | Deep-link-enhanced exploration of Android apps | +27.2% activity, +21.13% method coverage, +23.81% crash detection | Relative improvements reported; full inferential details not available in accessible preprint summary | Preprint; reachability/crash measures rather than functional correctness |
| **TimeMachine snapshots** versus restart | Same corpus; state restore compared with restart-on-stall | 4.4× the unique crashes of restart baseline on 68 apps | Ratio reported; no confidence interval | Saved local state can diverge from already-mutated server state |

#### 1.3 Sequence and event-order coverage

**(High Confidence)** An ordinary covering array over `surface × state × viewport × …` does not imply coverage of `A before B`, `B before A`, or `A … C … B`. A sequence covering array of strength *t* covers every ordering of every *t*-event subset as a not-necessarily-contiguous subsequence.[NIST SP 800-142, sequence-covering arrays](https://www.govinfo.gov/content/pkg/GOVPUB-C13-PURL-gpo14815/pdf/GOVPUB-C13-PURL-gpo14815.pdf) ([govinfo.gov](https://www.govinfo.gov/content/pkg/GOVPUB-C13-PURL-gpo14815/pdf/GOVPUB-C13-PURL-gpo14815.pdf)) For ten events, NIST reports 14 tests for all three-event orderings and 72 tests for all four-event orderings, instead of 10! exhaustive permutations.[NIST sequence-array sizes](https://www.govinfo.gov/content/pkg/GOVPUB-C13-PURL-gpo14815/pdf/GOVPUB-C13-PURL-gpo14815.pdf) ([govinfo.gov](https://www.govinfo.gov/content/pkg/GOVPUB-C13-PURL-gpo14815/pdf/GOVPUB-C13-PURL-gpo14815.pdf))

**(Medium Confidence)** The best defect evidence remains limited:

- An operational eight-step system had approximately 7,000 valid non-redundant permutations; NIST reduced it to a 19-case constrained sequence suite.[NIST operational example](https://www.govinfo.gov/content/pkg/GOVPUB-C13-PURL-gpo14815/pdf/GOVPUB-C13-PURL-gpo14815.pdf) ([govinfo.gov](https://www.govinfo.gov/content/pkg/GOVPUB-C13-PURL-gpo14815/pdf/GOVPUB-C13-PURL-gpo14815.pdf)) The associated publication reports errors that could not be attributed to two-event subsequences.[Kuhn et al., Combinatorial Methods for Event Sequence Testing](https://citeseerx.ist.psu.edu/document?doi=616b282ab7c0e728da0e3aeb1589ae64f920fe9f&amp;repid=rep1&amp;type=pdf) ([citeseerx.ist.psu.edu](https://citeseerx.ist.psu.edu/document?doi=616b282ab7c0e728da0e3aeb1589ae64f920fe9f&repid=rep1&type=pdf&utm_source=openai))
- A later thesis inspected 592 Android vulnerability reports; 49, approximately 7.9%, were classified as event-sequence vulnerabilities. It found five lock-screen bypass vulnerabilities in two applications using sequence arrays.[Srinivasan, 2018](https://oaktrust.library.tamu.edu/server/api/core/bitstreams/63e58062-7474-48ec-830e-9b7324ebfb9c/content) ([oaktrust.library.tamu.edu](https://oaktrust.library.tamu.edu/server/api/core/bitstreams/63e58062-7474-48ec-830e-9b7324ebfb9c/content))

**(High Confidence)** Sequence arrays have several critical blind spots:

- The covered events need not be adjacent, so a defect requiring `A` immediately followed by `B` is not guaranteed to appear.
- Standard arrays use each named event once per permutation and therefore do not cover `submit, submit`, `open, close, open`, or retry loops.
- Unmodelled events are invisible. The lock-screen study explicitly describes vulnerabilities involving hardware controls and cross-app actions unlikely to have been included in the developer’s event model.
- They cover relative order, not scheduler interleavings or delays.
- Constraints and prerequisite chains can substantially alter the generated suite.

These limitations are stated or demonstrated in the Android sequence study.[Srinivasan, adjacency and omitted-event discussion](https://oaktrust.library.tamu.edu/server/api/core/bitstreams/63e58062-7474-48ec-830e-9b7324ebfb9c/content) ([oaktrust.library.tamu.edu](https://oaktrust.library.tamu.edu/server/api/core/bitstreams/63e58062-7474-48ec-830e-9b7324ebfb9c/content))

`<MISSING_DATA>[No controlled study was found that executed ordinary factor-wise t-way sampling and sequence covering arrays against the same modern web/iOS/macOS/Android UI fault corpus and reported incremental unique defects per execution-hour. Existing evidence consists of mathematical coverage results, one operational system, security-report classification and two Android lock-screen applications.]</MISSING_DATA>`

**Decision:** **(Medium Confidence)** <INFERENCE from="the definition and limited defect studies">Add sequence coverage as a separately declared dimension, not another factor inside the existing covering array.</INFERENCE> Mechanically gate **coverage accounting** for two-event order on critical event alphabets and selected three-event orderings. Add separate generators for adjacent pairs, repeated events and schedule perturbations.

#### 1.4 Previous-build differential testing and intended-change triage

**(High Confidence)** RegDroid is the most directly relevant published experiment. It executed equivalent randomly selected widget actions against adjacent versions on two identical Android devices. The evaluation covered five apps and 121 adjacent-version pairs; each pair received 50 tests of 100 events, taking roughly 12 hours per pair before parallelisation.[Xiong et al., ISSTA 2023](https://tingsu.github.io/files/ISSTA23-functional-bugs.pdf) ([tingsu.github.io](https://tingsu.github.io/files/ISSTA23-functional-bugs.pdf?utm_source=openai))

It found:

- 205 reports: 73 judged true positives and 132 false positives.
- 14 unique functional bugs; ten were previously unknown and all ten were confirmed and fixed by developers.
- Ten of the 14 unique bugs were not detectable by the existing techniques assessed in the study.
- 12 crashing bugs as a by-product.
- Less than one hour of manual inspection for all 205 reports, according to the authors.
- Of the false positives, 93% reflected intended feature changes and 7% reflected a bug fixed in the new version.[Xiong et al., 2023](https://doi.org/10.1145/3597926.3598138) ([research-collection.ethz.ch](https://www.research-collection.ethz.ch/handle/20.500.11850/623870?utm_source=openai))

No p-values, confidence intervals or controlled person-hour comparison were reported. The oracle—matching widget resource IDs and classes—was deliberately simple; random exploration and Android-only open-source subjects limit external validity.

**(Medium Confidence)** RippleGUItester represents the 2026 trajectory: it generates change-targeted scenarios, executes pre- and post-change versions, and interprets observed differences against natural-language change intent. Across hundreds of changes in Firefox, Zettlr, JabRef and Godot, it reported 26 previously unknown issues still present in current versions: 16 fixed, two confirmed, six under discussion and two judged intended.[Su, Pradel and Chen, ISSTA 2026](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/149/RippleGUItester-Change-Aware-Exploratory-Testing) ([conf.researchr.org](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/149/RippleGUItester-Change-Aware-Exploratory-Testing?utm_source=openai)) The accessible abstract does not report the total number of candidate diffs, precision, recall or reviewer time; it therefore cannot establish a false-positive rate.

**Decision:** **(High Confidence)** <INFERENCE from="RegDroid’s 64% false-positive rate and the dominance of intended changes among those false positives">Do not make every previous-build behavioral difference a blocking failure.</INFERENCE> Use three dispositions:

1. **Mechanical fail:** violation of a retained invariant, effect contract, accessibility invariant, security rule or undeclared removal.
2. **Mechanical accept:** diff matches a machine-readable change-intent declaration identifying affected surface, state and allowed semantic delta.
3. **Human/model triage:** all other behavioral or visual diffs, with duplicate clustering and code-change attribution.

The previous build is an excellent **candidate oracle** for unspecified behavior; it is not an authority on whether that behavior should remain.

#### 1.5 Where LLMs/VLMs genuinely help—and where they do not

| Task | Best-supported role for LLM/VLM | Measured evidence | Generalisation assessment | Gate disposition |
|---|---|---|---|---|
| **Scenario navigation and meaningful input** | Infer business intent, open hidden menus, generate semantically valid values, and preserve history across long workflows | ScenGen: 99 tasks/92 apps; 86.87% coverage and 84.85% completion | Real apps, but only ten curated scenario families and manual judgments | Use model to generate/repair traces; replay deterministically |
| **Semantic accessibility** | Judge alternative text, relationships and contextual appropriateness that rule engines cannot encode | GenA11y: 95.2% precision, 87.69% recall; axe-core recall 12.74% on reported benchmark | Strong relative result; principal recall corpus is curated/injected | Advisory unless converted to a deterministic predicate or independently confirmed |
| **Non-crashing visual-functional bugs** | Interpret screenshot sequences such as wrong sort order, wrong destination or missing post-action state | VisionDroid: initial report 50–76% precision and 42–64% recall; later evaluation references 590 non-crash bugs | Mixed historical, injected and curated datasets; model/provider dependence | Candidate generation and triage, not sole blocker |
| **Intended-change classification** | Compare observed delta with PR/issue/change description | RippleGUItester found real missed bugs across four systems | No published candidate-diff denominator or calibrated error rates in accessible report | Advisory triage |
| **Exact layout/geometry** | Little defensible advantage over deterministic DOM/accessibility-tree/quantised geometry or pixel methods | No controlled evidence that an LLM beats a stable exact oracle | LLM output adds nondeterminism | Deterministic gate |
| **Server/effect correctness** | Can suggest likely expected outcome but cannot prove commit, idempotency or cross-system state | No head-to-head evidence | Requires access to authoritative state | Deterministic ledger gate |
| **Timing/resource bounds** | Explain anomalies, cluster traces, suggest hypotheses | No credible precision/recall benchmark found | Numeric instrumentation is superior | Deterministic statistical gate |
| **Telemetry contract** | Interpret event names or identify likely omissions | No UI-specific controlled study found | Ground truth is a versioned event schema | Deterministic gate |

**(High Confidence)** GenA11y’s result is the clearest example of a learned semantic oracle outperforming fixed rules. Its recall table reports 87.61% overall recall, compared with 38.20% for IBM Equal Access, 22.41% for QualWeb, 12.74% for axe-core, 10.70% for A11yWatch and 18.85% for WAVE.[He, Huq and Malek, FSE 2025](https://ics.uci.edu/~seal/publications/2025_FSE_GenA11y.pdf) ([ics.uci.edu](https://ics.uci.edu/~seal/publications/2025_FSE_GenA11y.pdf?utm_source=openai)) The dataset’s 148 pages intentionally contain known accessibility issues, so this is closer to a conformance benchmark than the uncontrolled distribution of defects in production applications.[GenA11y artifact](https://github.com/seal-hub/GenA11y) ([github.com](https://github.com/seal-hub/GenA11y?utm_source=openai))

**(Medium Confidence)** VisionDroid’s data provenance is broader but more heterogeneous. Its initial study began with 3,128 open-source apps and 57,326 issue reports, randomly selected 6,000 reports from 576 apps, and classified 3,060 as non-crashing functional bugs.[VisionDroid study](https://arxiv.org/abs/2407.03037) ([researchgate.net](https://www.researchgate.net/publication/381960311_Vision-driven_Automated_Mobile_GUI_Testing_via_Multimodal_Large_Language_Model?utm_source=openai)) Its reported absolute precision and recall leave substantial residual error. The final report evaluates 590 non-crash bugs and reports large relative improvements over 12 baselines, but the accessible abstract does not provide absolute per-class precision, recall or false-positive rate.[Liu et al., ICSE 2026 journal-first](https://conf.researchr.org/details/icse-2026/icse-2026-journal-first-papers/26/Seeing-is-Believing-Vision-driven-Non-crash-Functional-Bug-Detection-for-Mobile-Apps) ([conf.researchr.org](https://conf.researchr.org/details/icse-2026/icse-2026-journal-first-papers/26/Seeing-is-Believing-Vision-driven-Non-crash-Functional-Bug-Detection-for-Mobile-Apps?utm_source=openai))

`<MISSING_DATA>[For both GenA11y and VisionDroid, calibrated class-conditional false-positive rates across live product changes, repeated-run variance, provider/model-version sensitivity and reviewer minutes per true defect were not available. Precision must not be relabelled as false-positive rate.]</MISSING_DATA>`

**Decision:** **(High Confidence)** <INFERENCE from="the semantic benchmark advantages and the residual false-discovery rates">The correct architecture is model-assisted and deterministically executed:</INFERENCE>

- Let the model **select journeys, generate meaningful data, interpret ambiguous semantics and rank diffs**.
- Record exact actions, prompts, screenshots and model version.
- Replay the resulting trace without the model.
- Require deterministic confirmation—state/effect query, property check, accessibility-tree invariant, exact text/order check, or human review—before a release-blocking defect is declared.

#### 1.6 Methods absent from the existing list

##### Record/replay and production-session trace mining

**(High Confidence)** Record/replay is valuable because production traces expose prefixes and data dependencies that a requirements inventory may not anticipate, but current tooling is not reliable enough to serve as proof by itself. The 2025 “Can You Mimic Me?” study evaluated one industrial and three academic tools over 34 scenarios from 17 apps, 90 non-crashing failures from 42 apps and 31 crashing bugs from 17 apps. It found that 17%, 38% and 44%, respectively, could not be reliably recorded and replayed, mainly because of timing resolution, API incompatibility and Android tooling limitations.[Song et al., 2025](https://arxiv.org/abs/2504.20237) ([arxiv.org](https://arxiv.org/abs/2504.20237?utm_source=openai)) No p-values or confidence intervals were reported in the accessible preprint summary.

**(Medium Confidence)** Video-to-replay systems expand the input channel. V2S+ was evaluated on 243 videos containing 4,028 GUI actions across more than 90 native and hybrid Android apps.[Moran et al., V2S+](https://arxiv.org/abs/2301.01191) ([arxiv.org](https://arxiv.org/abs/2301.01191?utm_source=openai)) This measures action translation rather than incremental defect discovery.

**Recommended mechanism:** privacy-filter production sessions into symbolic traces; cluster by state/action n-grams, abandonment and rare transitions; replay high-value clusters against current and previous builds. Mechanically gate only replayed deterministic outcomes. Treat unreplayable traces as evidence of a recorder gap, not a product pass.

##### UI concurrency and event-race detection

**(High Confidence)** Timing-dependent GUI failures require schedule perturbation, not merely sequence coverage. The ISSTA 2024 single-event-delay technique used stack traces and dynamic analysis to identify relevant event races; it reproduced 73 of 80 flaky tests from 22 Android apps in 1.71 runs on average and reproduced selected failures consistently over 20 runs.[Cai et al., 2024](https://doi.org/10.1145/3650212.3680377) ([2024.issta.org](https://2024.issta.org/details/issta-2024-papers/120/Reproducing-Timing-Dependent-GUI-Flaky-Tests-in-Android-Apps-via-a-Single-Event-Delay?utm_source=openai)) It is a reproduction study with already-flaky tests, not a prospective product-bug yield experiment.

**Recommended mechanism:** identify asynchronous boundaries touching GUI-observed data, then delay each producer/consumer and lifecycle callback around the boundary. Include double click, back/cancel during loading, completion after navigation away, completion after process recreation, and two results arriving in reverse order.

##### Screen-reader-driven accessibility

**(Medium Confidence)** Rule engines and semantic LLM analysis are complementary, but neither proves actual assistive-technology operation. Screen-reader-only failures include incorrect spoken order, loss of focus after refresh, inaccessible custom gestures, duplicate or stale announcements, modal focus escape and controls exposed without actionable names.

A 2026 CHI mixed-methods study explicitly compares automated interventions with actual mobile screen-reader task experience, supporting the distinction between detected violations and user-observed obstruction.[Bridging the Gap between Automated Intervention and Actual User Experience, CHI 2026](https://doi.org/10.1145/3772318.3791293) ([doi.org](https://doi.org/10.1145/3772318.3791293?utm_source=openai)) `<MISSING_DATA>[The accessible publication result did not expose enough sample and issue-level data to calculate incremental defect yield over axe or GenA11y.]</MISSING_DATA>`

**Recommended mechanism:** drive critical journeys solely through the platform accessibility focus model; record focus target, role, name, value, state and spoken announcement after every action. Mechanically gate exact invariants; retain disabled-user exploratory sessions for comprehension and workload judgments.

##### Mid-session permission and capability revocation

**(High Confidence)** Aper analysed 13,352 popular Android apps and found that 86.0% used dangerous APIs asynchronously after permission management and 61.2% used evolving dangerous APIs. On a benchmark of 60 real permission bugs it improved average F1 by 46.3% over two academic tools and Android Lint, then found 34 additional permission bugs in 214 open-source apps.[Wang et al., Aper, ICSE 2022](https://arxiv.org/abs/2201.12542) ([arxiv.org](https://arxiv.org/abs/2201.12542)) The paper is static-analysis-centred, but the underlying failure condition directly motivates dynamic revocation between check and use.

**Recommended mechanism:** revoke permission while the app is foregrounded, backgrounded and while an operation is pending; test “allow once,” restricted photo/file selection, notification denial, camera/microphone loss and capability restoration. Gate no-crash, honest explanation, safe cancellation and successful retry after restoration.

##### Pseudo-localisation, time, offline/reconnect, telemetry and endurance

**(Low Confidence)** These are technically straightforward but poorly measured in peer-reviewed UI-testing literature:

- **Pseudo-localisation:** accented expansion, forced 30–100% length growth, bidi mirroring, missing-string markers and locale-independent identifier checks.
- **Clock/timezone/DST:** virtual clock crossing midnight, month/year, leap day, DST gap/fold; timezone switch during a live session; client/server skew; expired sessions and recurring schedules.
- **Offline/reconnect:** disconnect at each transaction boundary; queue, replay, duplicate, reverse and expire responses; assert eventual convergence.
- **Telemetry:** independent collector with exact event name/schema/cardinality/ordering/identity/consent reconciliation.
- **Soak/resource slope:** repeat realistic journeys while measuring heap/RSS, descriptors, graphics resources, listener/subscription counts and p95/p99 interaction latency; require a plateau rather than merely staying below a one-time ceiling.

`<INSUFFICIENT_EVIDENCE>[No credible cross-product controlled studies were found that report defects discovered per test-hour for these five methods. They should be adopted from system risk and ease of mechanisation, not from unverified vendor yield claims.]</INSUFFICIENT_EVIDENCE>`

#### 1.7 Decision ranking: marginal defect yield per engineering effort

This is **not** a measured cross-study league table. **(Medium Confidence)** <INFERENCE from="reported defect yield, corpus size, implementation complexity and overlap with the existing campaign">The following is the best-supported portfolio ordering for incremental investment:</INFERENCE>

| Rank | New sweep/oracle | Estimated yield per effort | Recommended enforcement |
|---:|---|---|---|
| **1** | **Journey-prefix interruption and process-death matrix** | **High** — 110-fault benchmark; simple to layer onto existing critical journeys | **Mechanical gate** on state/effect reconciliation |
| **2** | **Previous-build semantic differential with change-intent manifest** | **High** — RegDroid found 14 unique functional bugs, ten new; triage can be clustered | Gate retained invariants and undeclared differences; raw diffs advisory |
| **3** | **Critical end-to-end journeys with server/effect ledger** | **High but medium–high setup** — directly targets partial commits and cross-surface divergence | **Mechanical gate** for the highest-value workflows |
| **4** | **Event-order, adjacency, repetition and race bundle** | **Medium–High** — sequence evidence plus strong race-reproduction result | Gate declared coverage and deterministic failures; schedule anomalies initially advisory |
| **5** | **Screen-reader-driven critical journeys plus semantic accessibility analysis** | **Medium–High** — rule engines demonstrably miss semantic criteria | Deterministic accessibility transcript invariants gated; LLM/human judgments advisory |
| **6** | **Permission/offline/time/pseudo-locale state-machine bundle** | **Medium** — low automation cost; permission evidence strong, other yield evidence thin | Mechanical where expected transitions are explicit |
| **7** | **Production trace mining and replay** | **Medium** — discovers real prefixes, but replay failure is common | Trace selection advisory; successful deterministic replays gated |
| **8** | **Upgrade and aged-account matrix** | **Medium, potentially high severity** — expensive data curation and weak published yield evidence | Gate selected supported upgrade paths and high-value account archetypes |
| **9** | **Telemetry contract reconciliation** | **Medium and inexpensive once a test collector exists** | Mechanical gate for consent, purchase, onboarding and experiment events |
| **10** | **Soak/resource-slope endurance** | **Portfolio-dependent** — higher value for native desktop, media, realtime and long-lived sessions | Advisory until variance and thresholds are calibrated; then gate strong monotonic leaks |

---

### 2. What is the current state, and what is the strongest supporting evidence for it?

**(High Confidence)** The current state in 2026 is that **reachability has advanced faster than trustworthy oracle generation**. History-aware exploration, scenario agents, deep links and state snapshots can reach more realistic workflows; deterministic effect and state oracles remain the reliable proof layer.

The strongest evidence by problem is:

| Problem | Current best-supported method | Strongest evidence |
|---|---|---|
| Deep or accumulated state | Checkpoint/state restoration and scenario-guided journeys | TimeMachine: 68 open-source plus 37 industrial apps; more crashes and coverage than major baselines |
| Lifecycle state loss | Prefix-level stop/start/recreate/process-death tests | Public benchmark of 110 real faults in 48 apps |
| Event ordering | Constrained sequence covering arrays plus adjacency/repetition supplements | NIST operational use and Android sequence-vulnerability study; evidence remains narrow |
| Unspecified regression | Previous-build differential execution | RegDroid: 14 unique functional bugs, ten new and fixed; 64% raw false positives |
| Semantic accessibility | LLM semantic analysis plus deterministic accessibility checks | GenA11y: 95.2% precision, 87.69% recall on its benchmark |
| Visual-functional logic | MLLM screenshot-sequence interpretation | VisionDroid: better than baselines, but only 50–76% precision and 42–64% recall in the initial evaluation |
| Event races | Relevant-event delay and schedule perturbation | 73/80 flaky failures reproduced in 1.71 runs on average |
| Real-user paths | Trace/video mining followed by replay | Large action corpora exist; 2025 study shows substantial replay unreliability |

**(High Confidence)** A large empirical study of 399 functional bugs across eight Android apps reinforces the oracle problem. Its authors built RegDroid after finding that app-specific functional behavior frequently evades generic crash, overlap, data-loss and freeze oracles.[Xiong et al., ISSTA 2023](https://doi.org/10.1145/3597926.3598138) ([github.com](https://github.com/Android-Functional-bugs-study/home?utm_source=openai)) Secondary analysis of its results reports that feature-agnostic oracle classes could theoretically address about 30% of the corpus, while existing tools detected only about 6%, and that 84% required visual inspection.[Duc, 2025 thesis summarising Xiong et al.](https://orbilu.uni.lu/bitstream/10993/57964/1/ChanhDuc_PhD_Thesis_Final.pdf) ([orbilu.uni.lu](https://orbilu.uni.lu/bitstream/10993/57964/1/ChanhDuc_PhD_Thesis_Final.pdf?utm_source=openai)) Because the latter percentages are taken from a thesis synthesis rather than the primary paper text available here, they should be treated as **Medium Confidence**.

#### Gate boundary

| Mechanically gate now | Keep advisory or require confirmation |
|---|---|
| Critical journey final effects and intermediate invariants | Raw previous-build visual or behavioral differences |
| Client/server/effect-ledger reconciliation | LLM/VLM semantic defect verdicts |
| Lifecycle reconstruction and process-death survival | Model-generated “scenario complete” judgments |
| Back-stack/deep-link destination and identity | Uncalibrated performance or resource anomalies |
| Permission/offline/time state-machine transitions with explicit expected outcomes | Human-language quality, common-sense appropriateness and subjective usability |
| Telemetry schema, identity, consent and cardinality | Mined production traces that cannot be replayed reliably |
| Selected screen-reader role/name/state/focus-order transcripts | Full screen-reader comprehensibility and cognitive workload |
| Sequence/adjacency/repetition coverage accounting | Choice of event alphabet and sequence strength |

**(High Confidence)** <INFERENCE from="the measured model precision, RegDroid triage data and deterministic race/lifecycle results">The safe architecture is therefore: probabilistic generation and prioritisation; deterministic execution, evidence capture and release disposition.</INFERENCE>

---

### 3. What are the contrasting viewpoints or competing evidence?

#### Broad exploration versus scenario-guided journeys

`<CONFLICTING_EVIDENCE>[TimeMachine shows broad state exploration can find 199 crashes across 68 apps and complements other tools because crash overlap was low. ScenGen shows scenario guidance reaches more target-business-path bugs than unguided tools within selected scenarios, but traditional tools find more total bugs across the whole app. The evidence supports combining—not replacing—broad exploration with critical scenario execution.]</CONFLICTING_EVIDENCE>`[TimeMachine](https://doi.org/10.1145/3377811.3380402)[ScenGen preprint](https://arxiv.org/abs/2506.05079) ([abhikrc.com](https://abhikrc.com/pdf/ICSE20TM.pdf))

#### Previous build as oracle versus intended evolution

`<CONFLICTING_EVIDENCE>[RegDroid demonstrates high unique-bug yield from version comparison, including ten new confirmed bugs, but 64% of raw reports were false positives and intended feature evolution caused 93% of those false positives. RippleGUItester argues that natural-language change intent can reduce this ambiguity, but its accessible report provides no overall precision or candidate-diff denominator.]</CONFLICTING_EVIDENCE>`[RegDroid](https://doi.org/10.1145/3597926.3598138)[RippleGUItester](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/149/RippleGUItester-Change-Aware-Exploratory-Testing) ([tingsu.github.io](https://tingsu.github.io/files/ISSTA23-functional-bugs.pdf?utm_source=openai))

#### Deterministic accessibility rules versus generative semantic analysis

`<CONFLICTING_EVIDENCE>[GenA11y greatly exceeded axe-core recall on its benchmark, supporting semantic model analysis. However, its benchmark is curated and issue-focused, while deterministic rules are reproducible, cheap and have effectively zero model-version drift for the criteria they encode. The evidence supports semantic augmentation, not replacement of axe or platform accessibility checks.]</CONFLICTING_EVIDENCE>`[GenA11y](https://doi.org/10.1145/3729371) ([ics.uci.edu](https://ics.uci.edu/~seal/publications/2025_FSE_GenA11y.pdf?utm_source=openai))

#### VLM oracle versus human or deterministic confirmation

`<CONFLICTING_EVIDENCE>[VisionDroid reports substantial improvements over prior visual and GUI-tree baselines, but its 50–76% precision and 42–64% recall imply material false discoveries and missed defects. It is effective as a search and candidate-oracle layer but does not meet the reliability expected of an autonomous release gate.]</CONFLICTING_EVIDENCE>`[VisionDroid](https://arxiv.org/abs/2407.03037) ([researchgate.net](https://www.researchgate.net/publication/381960311_Vision-driven_Automated_Mobile_GUI_Testing_via_Multimodal_Large_Language_Model?utm_source=openai))

#### Sequence covering arrays versus state/path models

**(Medium Confidence)** Sequence arrays provide a compact, measurable order criterion without requiring a complete state model. State/path models better represent prerequisites, repeated actions and reachable transitions, but can omit hidden entries or become inaccurate under app evolution. TimeMachine reports that model-driven tools can miss pages whose handlers cannot be triggered through the inferred model, while sequence arrays fail if the relevant event was omitted from the alphabet.[TimeMachine discussion](https://abhikrc.com/pdf/ICSE20TM.pdf)[Sequence study limitations](https://oaktrust.library.tamu.edu/server/api/core/bitstreams/63e58062-7474-48ec-830e-9b7324ebfb9c/content) ([abhikrc.com](https://abhikrc.com/pdf/ICSE20TM.pdf))

**Decision:** combine a constrained state model for reachability with explicit order, adjacency and repetition coverage over the critical event alphabet.

---

### 4. What changed recently, and what is the trajectory?

- **(High Confidence)** **2024:** research moved from broad code-coverage optimisation toward change-targeted and timing-aware execution. Hawkeye used historical event/activity models to direct Android exploration toward changed functions across ten open-source apps and one commercial app.[Peng et al., ICSE 2024](https://conf.researchr.org/details/icse-2024/icse-2024-software-engineering-in-practice/38/Hawkeye-Change-targeted-Testing-for-Android-Apps-based-on-Deep-Reinforcement-Learnin) ([conf.researchr.org](https://conf.researchr.org/details/icse-2024/icse-2024-software-engineering-in-practice/38/Hawkeye-Change-targeted-Testing-for-Android-Apps-based-on-Deep-Reinforcement-Learnin?utm_source=openai)) The single-event-delay work supplied strong evidence that race-aware perturbation can make elusive failures reproducible.[Cai et al., ISSTA 2024](https://doi.org/10.1145/3650212.3680377) ([2024.issta.org](https://2024.issta.org/details/issta-2024-papers/120/Reproducing-Timing-Dependent-GUI-Flaky-Tests-in-Android-Apps-via-a-Single-Event-Delay?utm_source=openai))

- **(High Confidence)** **2025:** LLMs began showing measurable value on semantic subproblems rather than generic “AI testing.” GenA11y demonstrated a large recall advantage on accessibility criteria requiring contextual interpretation.[He et al., FSE 2025](https://doi.org/10.1145/3729371) ([conf.researchr.org](https://conf.researchr.org/details/fse-2025/fse-2025-research-papers/54/Enhancing-Web-Accessibility-Automated-Detection-of-Issues-with-Generative-AI?utm_source=openai)) Record/replay research simultaneously documented practical limitations rather than treating recording as reliable ground truth.[Song et al., 2025](https://arxiv.org/abs/2504.20237) ([arxiv.org](https://arxiv.org/abs/2504.20237?utm_source=openai))

- **(Medium Confidence)** **2025–2026:** multimodal testing shifted from single screenshots to **sequences of screenshots plus execution history**, enabling scenario completion and non-crash functional judgments. ScenGen and VisionDroid exemplify this trajectory.[ScenGen](https://doi.org/10.1145/3816025)[VisionDroid](https://conf.researchr.org/details/icse-2026/icse-2026-journal-first-papers/26/Seeing-is-Believing-Vision-driven-Non-crash-Functional-Bug-Detection-for-Mobile-Apps) ([conf.researchr.org](https://conf.researchr.org/details/ase-2026/ase-2026-journal-first/24/Scenario-Guided-LLM-based-Mobile-App-GUI-Testing?utm_source=openai))

- **(Medium Confidence)** **2026:** change intent became part of differential-oracle triage. RippleGUItester combines code-change analysis, pre/post execution, visual difference interpretation and natural-language intent.[RippleGUItester, ISSTA 2026](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/149/RippleGUItester-Change-Aware-Exploratory-Testing) ([conf.researchr.org](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/149/RippleGUItester-Change-Aware-Exploratory-Testing?utm_source=openai))

- **(High Confidence)** <INFERENCE from="ScenGen’s deterministic executor, RippleGUItester’s intent-based differential analysis, GenA11y’s semantic advantage and VisionDroid’s residual error">The trajectory is toward hybrid systems: models supply semantic reachability and triage; deterministic components retain control of execution, provenance, measurements and final proof.</INFERENCE>

- **(High Confidence)** The literature remains heavily biased toward Android and web applications. `<MISSING_DATA>[Comparable corpora and measured tools for native iOS and macOS lifecycle, accessibility, windowing, upgrade and resource-endurance defects are largely absent from the reviewed evidence.]</MISSING_DATA>`

---

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| Lifecycle reconstruction faults are a distinct, reproducible user-visible class: 110 faults across 48 apps, 98 automated oracles. | Riganelli, Mobilio, Micucci, Mariani, *A Benchmark of Data Loss Bugs for Android Apps* | 2019-05-27 | Primary benchmark with faulty/fixed releases and executable tests; admitted despite pre-2020 date because it is the principal public lifecycle-fault corpus. | https://arxiv.org/abs/1905.11040 |
| Saving and restoring deep states increased coverage and crash discovery relative to major Android exploration tools. | Dong, Böhme, Cojocaru, Roychoudhury, *Time-travel Testing of Android Apps* | 2020-05 | Peer-reviewed ICSE primary experiment; 68 open-source and 37 closed-source apps. | https://doi.org/10.1145/3377811.3380402 |
| Sequence covering arrays cover all relative t-event orders with far fewer tests than exhaustive permutations. | NIST, *Practical Combinatorial Testing*, sequence-covering chapter | 2010/2012 methods | Authoritative government technical publication; admitted as foundational coverage definition and operational experience. | https://www.govinfo.gov/content/pkg/GOVPUB-C13-PURL-gpo14815/pdf/GOVPUB-C13-PURL-gpo14815.pdf |
| 49/592 Android vulnerability reports were classified as sequence-triggered; five lock-screen bypasses were found in two apps. | Srinivasan, *Event Sequence Testing of Android Applications* | 2018 | Primary thesis with public methodology and experiments; admitted with lower evidentiary weight because it is not a peer-reviewed multi-product trial. | https://oaktrust.library.tamu.edu/server/api/core/bitstreams/63e58062-7474-48ec-830e-9b7324ebfb9c/content |
| Differential execution found 14 unique functional bugs, including ten new confirmed/fixed bugs, but raw reports had 64% false positives. | Xiong et al., *An Empirical Study of Functional Bugs in Android Apps* | 2023-07 | Peer-reviewed ISSTA primary study; public 399-bug corpus and RegDroid artifact. | https://doi.org/10.1145/3597926.3598138 |
| Scenario-guided testing completed realistic multi-step tasks and found scenario-related bugs across 92 apps. | Yu et al., *Scenario-Guided LLM-based Mobile App GUI Testing* | 2026-06 | Peer-reviewed ACM TOSEM article; real-app evaluation, but curated scenarios and manual expert judgments. | https://doi.org/10.1145/3816025 |
| Semantic generative analysis substantially exceeded rule-engine recall on the evaluated accessibility benchmark. | He, Huq, Malek, *Enhancing Web Accessibility: Automated Detection of Issues with Generative AI* | 2025-07 | Peer-reviewed FSE primary experiment plus public 148-page artifact; curated-benchmark limitation explicit. | https://doi.org/10.1145/3729371 |
| Multimodal screenshot-sequence analysis can detect non-crashing functional bugs, but absolute precision/recall remain insufficient for autonomous gating. | Liu et al., *Vision-driven Automated Mobile GUI Testing via Multimodal Large Language Model / Seeing is Believing* | 2024–2026 | Primary preprint followed by journal-first publication; mixed real, historical and injected datasets. | https://arxiv.org/abs/2407.03037 |
| Record/replay failed reliably on meaningful fractions of scenarios, non-crash bugs and crash bugs. | Song et al., *Can You Mimic Me?* | 2025-04-28 | Primary empirical preprint evaluating one industrial and three academic tools; no peer-review status verified. | https://arxiv.org/abs/2504.20237 |
| Relevant-event delay reproduced 73/80 timing-dependent flaky tests in 1.71 runs on average. | Cai et al., *Reproducing Timing-Dependent GUI Flaky Tests in Android Apps via a Single Event Delay* | 2024-09 | Peer-reviewed ISSTA primary experiment on 80 tests from 22 apps. | https://doi.org/10.1145/3650212.3680377 |
| Runtime-permission evolution and asynchronous use are widespread; Aper found additional real bugs. | Wang et al., *Aper: Evolution-Aware Runtime Permission Misuse Detection for Android Apps* | 2022 | Peer-reviewed ICSE primary static-analysis and empirical study over 13,352 apps. | https://arxiv.org/abs/2201.12542 |
| Video recordings can be converted into replay-oriented scenarios at substantial corpus scale. | Moran et al., *Translating Video Recordings of Complex Mobile App UI Gestures into Replayable Scenarios* | 2023 | Primary research artifact/evaluation: 243 videos, 4,028 actions, over 90 apps. | https://arxiv.org/abs/2301.01191 |
| Change-intent-aware, pre/post GUI exploration found previously unknown bugs missed by CI and review. | Su, Pradel, Chen, *RippleGUItester* | 2026-08 | Peer-reviewed ISSTA 2026 primary study over real changes in four mature systems; accessible abstract lacks denominator and precision. | https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/149/RippleGUItester-Change-Aware-Exploratory-Testing |
| Automated findings do not fully represent actual screen-reader task obstruction. | *Bridging the Gap between Automated Intervention and Actual User Experience* | 2026 | Peer-reviewed CHI mixed-methods study with screen-reader users; detailed incremental yield was unavailable in accessible material. | https://doi.org/10.1145/3772318.3791293 |

---

## Knowledge Gaps

### Missing common benchmark

`<MISSING_DATA>[No benchmark applies journey testing, ordinary t-way sampling, sequence arrays, previous-build differential testing, VLM oracles, screen readers, race perturbation, offline/reconnect, permission revocation and soak testing to the same fault corpus. Consequently, published results cannot support a numerical defects-per-engineering-hour comparison.]</MISSING_DATA>`

### Missing longitudinal and distributed-state corpora

`<MISSING_DATA>[Public corpora were not found for client-failure-after-server-commit, cross-device stale reads, aged accounts, install-over upgrade paths, cache/schema migration, or multi-surface reconciliation. Required data would include old and new builds, versioned server snapshots, user-history traces, reproducible failure boundaries and independent effect ledgers.]</MISSING_DATA>`

### Oracle reporting deficiencies

`<MISSING_DATA>[Recent LLM/VLM papers frequently report task completion, relative improvement, precision or recall without class-conditional false-positive rates, repeated-run variance, calibration, model-version sensitivity, reviewer cost or live-product base rates.]</MISSING_DATA>`

### Curated-benchmark external validity

`<INSUFFICIENT_EVIDENCE>[GenA11y’s 148-page issue corpus and VisionDroid’s mixed historical/injected datasets establish feasibility but cannot establish production precision where genuine defects are rare and benign change is common.]</INSUFFICIENT_EVIDENCE>`

### Platform bias

`<MISSING_DATA>[Most measured evidence concerns Android; semantic accessibility evidence is primarily web. Native iOS and macOS evidence is insufficient for confident cross-platform yield estimates, particularly for window restoration, keychain migration, VoiceOver, background execution and app-update state.]</MISSING_DATA>`

### Thin evidence for operationally familiar sweeps

`<MISSING_DATA>[No independent controlled yield studies were located for pseudo-localisation, DST/timezone testing, offline/reconnect models, telemetry validation or resource-slope soak tests. Vendor claims were excluded because independent measurement was unavailable.]</MISSING_DATA>`

### Statistical reporting

**(High Confidence)** Most reviewed UI-testing studies report absolute counts, coverage changes and ratios rather than confidence intervals, p-values or effort-normalised effect sizes. Where no inferential statistics were available, none have been inferred in this report.

---

## Recommended Next Steps

1. **Build a journey-prefix lifecycle and commit-boundary benchmark.**  
   **Rationale:** This targets the best-supported residual defect class. Select 10–20 critical journeys and inject backgrounding, recreation, process death, disconnect-before-commit, disconnect-after-commit and cold/warm re-entry at every material prefix. Mechanically reconcile UI, local persistence, server ledger and external effects.

2. **Add previous-build differential testing with a required change-intent manifest.**  
   **Rationale:** RegDroid shows high unique-bug yield but unacceptable raw diff noise. Require each intended behavior change to declare affected journey/surface/state and permitted semantic delta. Gate invariant violations and undeclared changes; route remaining diffs through clustered triage.

3. **Introduce an explicit temporal-coverage layer.**  
   **Rationale:** Keep existing factor-wise t-way sampling, but separately measure: constrained two- and selected three-event order coverage, adjacent-pair coverage, repeated-event coverage, lifecycle-event insertion and bounded scheduler perturbation. Initially gate coverage completeness, not the choice of strength.

4. **Create a production-trace, upgrade and aged-account corpus.**  
   **Rationale:** Requirements and synthetic fixtures do not reveal real historical prefixes. Privacy-filter and symbolise sessions; preserve rare paths, abandonment points and long-lived account histories. Test prior-build install-over, stale caches, partially completed workflows and cross-surface reads.

5. **Run an internal blinded oracle benchmark before gating any LLM/VLM result.**  
   **Rationale:** Assemble real historical defects, benign intended changes and unchanged controls from your portfolio. Compare deterministic oracles, human reviewers and fixed model versions on precision, recall, false-discovery share, repeated-run stability, reviewer minutes and cost per unique defect. Promote a model finding to a mechanical gate only when it is transformed into, or independently confirmed by, a deterministic predicate.

## Sources

- [A Benchmark of Data Loss Bugs for Android Apps](https://arxiv.org/abs/1905.11040)
- [https://oaktrust.library.tamu.edu/server/api/core/bitstreams/63e58062-7474-48ec-830e-9b7324ebfb9c/content](https://oaktrust.library.tamu.edu/server/api/core/bitstreams/63e58062-7474-48ec-830e-9b7324ebfb9c/content)
- [An Empirical Study of Functional Bugs in Android Apps](https://tingsu.github.io/files/ISSTA23-functional-bugs.pdf?utm_source=openai)
- [GitHub - seal-hub/GenA11y · GitHub](https://github.com/seal-hub/GenA11y?utm_source=openai)
- [(PDF) Vision-driven Automated Mobile GUI Testing via Multimodal Large Language Model](https://www.researchgate.net/publication/381960311_Vision-driven_Automated_Mobile_GUI_Testing_via_Multimodal_Large_Language_Model?utm_source=openai)
- [Can You Mimic Me? Exploring the Use of Android Record & Replay Tools in Debugging](https://arxiv.org/abs/2504.20237?utm_source=openai)
- [Reproducing Timing-Dependent GUI Flaky Tests in Android Apps via a Single Event Delay (ISSTA 2024...](https://2024.issta.org/details/issta-2024-papers/120/Reproducing-Timing-Dependent-GUI-Flaky-Tests-in-Android-Apps-via-a-Single-Event-Delay?utm_source=openai)
- [https://abhikrc.com/pdf/ICSE20TM.pdf](https://abhikrc.com/pdf/ICSE20TM.pdf)
- [Scenario-Guided LLM-based Mobile App GUI Testing (ASE 2026 - Journal First) - ASE 2026](https://conf.researchr.org/details/ase-2026/ase-2026-journal-first/24/Scenario-Guided-LLM-based-Mobile-App-GUI-Testing?utm_source=openai)
- [LLM-Guided Scenario-based GUI Testing](https://arxiv.org/abs/2506.05079)
- [Enhancing GUI Exploration Coverage of Android Apps with Deep Link-Integrated Monkey](https://arxiv.org/abs/2404.19307?utm_source=openai)
- [SP101006](https://www.govinfo.gov/content/pkg/GOVPUB-C13-PURL-gpo14815/pdf/GOVPUB-C13-PURL-gpo14815.pdf)
- [Combinatorial Methods for Event Sequence Testing](https://citeseerx.ist.psu.edu/document?doi=616b282ab7c0e728da0e3aeb1589ae64f920fe9f&repid=rep1&type=pdf&utm_source=openai)
- [An Empirical Study of Functional Bugs in Android Apps](https://www.research-collection.ethz.ch/handle/20.500.11850/623870?utm_source=openai)
- [RippleGUItester: Change-Aware Exploratory Testing (ISSTA 2026 - Research papers) - ISSTA 2026](https://conf.researchr.org/details/issta-2026/issta-2026-research-papers/149/RippleGUItester-Change-Aware-Exploratory-Testing?utm_source=openai)
- [Enhancing Web Accessibility: Automated Detection of Issues with Generative AI](https://ics.uci.edu/~seal/publications/2025_FSE_GenA11y.pdf?utm_source=openai)
- [Seeing is Believing: Vision-driven Non-crash Functional Bug Detection for Mobile Apps (ICSE 2026 ...](https://conf.researchr.org/details/icse-2026/icse-2026-journal-first-papers/26/Seeing-is-Believing-Vision-driven-Non-crash-Functional-Bug-Detection-for-Mobile-Apps?utm_source=openai)
- [Translating Video Recordings of Complex Mobile App UI Gestures into Replayable Scenarios](https://arxiv.org/abs/2301.01191?utm_source=openai)
- [Bridging the Gap between Automated Intervention and Actual User Experience: A Mixed-Methods Study...](https://doi.org/10.1145/3772318.3791293?utm_source=openai)
- [Aper: Evolution-Aware Runtime Permission Misuse Detection for Android Apps](https://arxiv.org/abs/2201.12542)
- [GitHub - Android-Functional-bugs-study/home · GitHub](https://github.com/Android-Functional-bugs-study/home?utm_source=openai)
- [PhD-FSTM-2023-132](https://orbilu.uni.lu/bitstream/10993/57964/1/ChanhDuc_PhD_Thesis_Final.pdf?utm_source=openai)
- [Hawkeye: Change-targeted Testing for Android Apps based on Deep Reinforcement Learning (ICSE 2024...](https://conf.researchr.org/details/icse-2024/icse-2024-software-engineering-in-practice/38/Hawkeye-Change-targeted-Testing-for-Android-Apps-based-on-Deep-Reinforcement-Learnin?utm_source=openai)
- [Enhancing Web Accessibility: Automated Detection of Issues with Generative AI (FSE 2025 - Researc...](https://conf.researchr.org/details/fse-2025/fse-2025-research-papers/54/Enhancing-Web-Accessibility-Automated-Detection-of-Issues-with-Generative-AI?utm_source=openai)
