---
title: "Evidence-based architecture for AI-driven UI testing"
run_id: dr_e1a6f1bf30fd2156
question: "How should an AI coding agent generate and execute a genuinely comprehensive UI test suite for an application, and what does the evidence say about the techniques that work versus the ones that only appear to?\n\nCover four subtopics specifically:\n\n1. COVERAGE MODELS AND TEST-PLAN GENERATION. What formal or semi-formal models exist for enumerating a UI's correctness space (surface x state x viewport x theme x role x locale x data-shape x input-modality), and what evidence exists about combinatorial sampling strategies (pairwise/t-way, risk-weighted, equivalence partitioning) for UI specifically? What makes an automatically generated test plan broad and deep rather than shallow and repetitive? Known failure modes of LLM-generated test plans: duplication, happy-path bias, asserting presence instead of outcome, coverage theatre.\n\n2. AGENT-DRIVEN EXPLORATORY AND FLOW-DISCOVERY TESTING. Techniques for autonomously discovering user flows and screens (crawlers, state-machine/GUI-ripping approaches, model-based testing, property-based UI testing, metamorphic testing for UI), and measured results on defect-detection yield versus scripted suites. What are the reliability and cost characteristics as of 2024-2026?\n\n3. LIVING TEST DOCUMENTATION AND EVIDENCE DASHBOARDS. Prior art and evidence on single-pane test/coverage/flow/screenshot browsers (Allure, ReportPortal, Playwright HTML reporter, Storybook, Chromatic, Percy, Applitools, Testomat, Xray). What makes such an artifact actually get used versus abandoned? Evidence on stable referenceable test identifiers, traceability from requirement to test to evidence, and presenting screenshot/visual evidence alongside structural coverage.\n\n4. CROSS-PLATFORM COMPONENT AND SCREEN CAPTURE. Current practical techniques for capturing and cataloguing rendered components and screens across web (DOM/computed style), React Native, and SwiftUI/UIKit, including what runtime introspection each platform does and does not offer, and how teams reconcile a component catalogue across those three.\n\nFor each subtopic give evidence-backed techniques AND documented failure modes, with numbers where they exist."
provider: openai
model: gpt-5.6-sol
tier: max
archetype: technical
sources: 46
tools: [google_search, url_context, code_execution]
estimated_cost_usd: 9.00
completed: 2026-08-18T01:00:26.833Z
---
## Executive Summary

- **(High Confidence)** A genuinely comprehensive UI-testing skill should **not** ask one model to “test the app.” It should run a gated pipeline: inventory surfaces and states → construct a constrained coverage model → generate test intentions independently of implementation → deduplicate and lint the plan → produce deterministic scripts → execute structural, behavioral, accessibility and visual checks → run separate exploratory agents → replay and minimize findings → publish immutable evidence. <INFERENCE from="NIST combinatorial evidence; Mozilla Firefox test-plan study; GUITester; VLM-Fuzz; Playwright and Allure documentation">This separation prevents high test counts, screenshots and model confidence from being mistaken for actual assurance.</INFERENCE>

- **(High Confidence)** Model the correctness space as a **constrained product**, not a flat checklist: `surface × semantic-state × transition × viewport × theme × role × locale × data-shape × input-modality × oracle`. Cover every factor value, all valid pairs, and risk-selected 3–4-way combinations; reserve higher strengths for critical clusters. NIST reports 20×–700× suite-size reductions from combinatorial testing generally, while a directly UI-adjacent DOM study found that 4-way tests exposed all seeded faults with 95% fewer tests than the exhaustive suite; 2-way and 3-way suites found only 37.5% of those faults. [csrc.nist.gov](https://csrc.nist.gov/pubs/journal/2024/02/combinatorial-testing-for-building-reliable-system/final) [tsapps.nist.gov](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=913806) ([csrc.nist.gov](https://csrc.nist.gov/pubs/journal/2024/02/combinatorial-testing-for-building-reliable-system/final?utm_source=openai))

- **(High Confidence)** Unsupervised LLM test plans are useful for discovery but generate substantial waste. In Mozilla’s 2026 Firefox study, 27% of generated cases were valuable missed scenarios, 50.5% duplicated existing cases, and 22.5% were invalid or out of scope. In a 2025 industrial web-acceptance study, 60% of executable cases were usable as generated, while 40% needed fixes, regeneration or disposal. [mozillafoundation.org](https://www.mozillafoundation.org/en/research/library/using-llms-to-bridge-the-gaps-in-qa-test-plans-at-firefox/) [arxiv.org](https://arxiv.org/abs/2504.07244) ([mozillafoundation.org](https://www.mozillafoundation.org/en/research/library/using-llms-to-bridge-the-gaps-in-qa-test-plans-at-firefox/?utm_source=openai))

- **(High Confidence)** Autonomous exploration adds defect yield but is not reliable enough to be the sole CI gate. GPTDroid reported 32% higher activity coverage and 31% more bugs than its strongest baseline across 93 Android apps; newer GUITester work still found the strongest baseline at only 33.35% F1 under three attempts, with GUITester reaching 48.90%. Agent findings should therefore remain non-blocking until converted into a deterministic, independently-oracled replay. [doi.org](https://doi.org/10.1145/3597503.3639180) [aclanthology.org](https://aclanthology.org/2026.findings-acl.946/) ([portal.fis.tum.de](https://portal.fis.tum.de/de/publications/make-llm-a-testing-expert-bringing-human-like-interaction-to-mobi/?utm_source=openai))

- **(High Confidence)** The strongest current architecture is **hybrid search plus selective semantic reasoning**: deterministic graph exploration tracks visited states and transitions; an LLM/VLM chooses semantic goals, supplies context-sensitive input and proposes oracles; a separate monitor checks every transition; a separate verifier attributes anomalies. VLM-Fuzz’s selective GPT-4o use produced only a 5.28% line-coverage gain over its non-VLM variant in its small ablation, illustrating that the search/state machinery—not the model alone—does most of the systematic work. [link.springer.com](https://link.springer.com/article/10.1007/s10664-026-10816-4) ([link.springer.com](https://link.springer.com/article/10.1007/s10664-026-10816-4))

- **(High Confidence)** Build the living dashboard as a **thin, vendor-neutral evidence SPA over a canonical manifest**, while embedding vendor-native reports. Use explicit semantic IDs for requirements, surfaces, states, flows, test cases, runs and artifacts. Playwright contributes web traces and DOM snapshots; Allure contributes cross-run identity/history; Storybook/Chromatic contributes component baselines; ReportPortal contributes failure triage; Xray/Testomat contributes governed requirement traceability. No single product adequately models all of these across web, React Native and SwiftUI.

- **(High Confidence)** Cross-platform reconciliation must occur at the **semantic-contract layer**, not by pretending the three platforms expose equivalent runtime component trees. Web exposes DOM, CSSOM, layout and accessibility structure; React Native development builds expose the React component tree and props/state but ultimately render platform-native views; XCUITest exposes an accessibility-oriented element hierarchy, while SwiftUI does not provide a supported public API for enumerating its original declarative `View` tree at runtime. [chromedevtools.github.io](https://chromedevtools.github.io/devtools-protocol/tot/DOMSnapshot/) [reactnative.dev](https://reactnative.dev/docs/react-native-devtools) [developer.apple.com](https://developer.apple.com/documentation/xcuiautomation/xcuielement) ([chromedevtools.github.io](https://chromedevtools.github.io/devtools-protocol/tot/DOMSnapshot/))

- **(High Confidence)** The skill should explicitly refuse: raw Cartesian explosion; pairwise-only “completeness”; presence-only assertions for outcome-bearing flows; screenshot-only testing; silent selector self-healing; automatic baseline acceptance; tests generated solely from current implementation behavior; CI failures based only on a stochastic model verdict; and coverage claims based on test counts, screen counts or code coverage alone.

---

## Detailed Findings

### 1. How should an AI coding agent generate and execute a genuinely comprehensive UI test suite, and what does the evidence say about techniques that work versus those that only appear to?

#### 1.1 Recommended phase and gate structure

<INFERENCE from="NIST combinatorial testing; Mozilla Firefox LLM planning study; industrial acceptance-test generation; GPTDroid; GUITester; VLM-Fuzz; Playwright; Allure">The skill should implement the following phase structure. Each phase must emit machine-readable artifacts and must be independently rerunnable; prose documents are rendered from those artifacts, not treated as the source of truth.</INFERENCE>

| Phase | Output and reference IDs | Promotion gate | Explicit failure conditions | Confidence |
|---|---|---|---|---|
| **0. Application reconnaissance** | `SURF-*`, component inventory, routes/screens, role gates, locales, themes, device profiles, data fixtures | Every discovered surface has provenance and an owner/platform | Unreachable surfaces silently omitted; inventory based only on screenshots; no authenticated-role setup | High |
| **1. State and flow model** | `STATE-*`, `TRANS-*`, `FLOW-*`; state-transition graph; preconditions and reset operations | Critical flows have start state, transitions, observable outcome and cleanup | “Screen visited” used as proof of flow correctness; no reset strategy | High |
| **2. Coverage-space construction** | Factor/value model, constraints, equivalence classes, risk scores, t-way obligations | All factor values represented; all valid pairs covered; risk-selected 3–4-way obligations generated | Raw Cartesian product; pairwise advertised as exhaustive; invalid combinations dominate plan | High |
| **3. Test-intention generation** | `CASE-*` specifications independent of test code | Each critical requirement maps to at least one outcome-bearing test and one relevant negative/boundary test | Duplicates, implementation-derived expectations, visibility-only assertions, inaccessible preconditions | High |
| **4. Plan linting and challenge** | Duplicate clusters, orphan requirements, weak-oracle report, missing-state report | No unexplained duplicates or orphaned critical obligations; every test declares an oracle type | LLM self-approves its own plan without deterministic checks | High |
| **5. Deterministic test generation** | Platform-native executable tests and fixtures | Tests compile, discover selectors deterministically, reset state and attach evidence | Silent self-healing, arbitrary sleeps, selectors invented without runtime validation | High |
| **6. Deterministic execution** | `RUN-*`, per-step logs, traces, screenshots, accessibility/structure snapshots | Reproducible results under pinned environment; critical outcomes confirmed | Agent changes assertion to match implementation; flaky passes counted as success | High |
| **7. Visual/fidelity execution** | `ART-*` baseline, actual, diff, masks, viewport/theme metadata | Reviewed baseline and bounded, explainable diff | Auto-approving first render, hiding dynamic regions without justification, pixel diff as sole oracle | High |
| **8. Exploratory/agent runs** | New transitions, hypotheses and `FIND-*` candidates | Finding replays at least once with recorded preconditions; blocker status requires deterministic conversion | Model-only verdict, non-reproducible anomaly, agent bypasses defect to finish its task | High |
| **9. Evidence publication** | Static SPA, graph manifest, deep links, provenance and freshness | Every reported pass/fail links to evidence and commit/environment | Manually maintained dashboard; broken or mutable evidence links | High |
| **10. CI promotion** | Stable deterministic regression subset | Only reproducible, bounded-runtime tests with stable oracles enter PR CI | Open-ended crawling, stochastic LLM judgments or unreviewed visual changes block PRs | High |

**(High Confidence)** The division between test intention and executable script is evidence-backed. The 2025 industrial acceptance-test study used a two-step process—Gherkin scenarios from user stories, followed by Cypress scripts grounded in page HTML—and reported that generated scenarios were helpful 95% of the time. Of the executable cases, 60% were directly usable, 8% needed minor fixes, 24% needed regeneration with more information, and 8% were discarded. [arxiv.org](https://arxiv.org/abs/2504.07244) ([arxiv.org](https://arxiv.org/abs/2504.07244?utm_source=openai))

**(High Confidence)** The model that generated or modified application code should not be treated as an independent test oracle. Recent studies report that test-generation tools can validate faulty behavior and that erroneous generated code can bias later test generation toward mutually consistent but incorrect implementation/test pairs. [arxiv.org](https://arxiv.org/abs/2412.14137) [arxiv.org](https://arxiv.org/abs/2607.05139) ([arxiv.org](https://arxiv.org/abs/2412.14137?utm_source=openai))

<INFERENCE from="LLM code/test error-propagation studies">For agentic development, create the test-intention artifact before exposing the tester to changed implementation code where practical. Otherwise, use a separate context or model instance given requirements, public contracts and approved design evidence—not implementation output—as its primary oracle source.</INFERENCE>

---

#### 1.2 Coverage models and test-plan generation

##### Formal coverage model

<INFERENCE from="covering-array models, GUI state models, property-based UI testing and UI metamorphic-relation research">Represent the test space as:</INFERENCE>

\[
\Omega =
S \times Q \times E \times V \times T \times R \times L \times D \times I \times O
\]

Where:

- `S` = surfaces: components, screens, overlays, system dialogs and cross-screen flows.
- `Q` = semantic states: initial, loading, empty, partial, populated, error, stale, disabled, offline, unauthorized, conflict and recovery states.
- `E` = transitions or event sequences, not merely static states.
- `V` = viewport/device classes, safe-area and orientation variants.
- `T` = theme and contrast mode.
- `R` = user role, entitlement and permission state.
- `L` = locale, text direction, text expansion and formatting rules.
- `D` = data-shape equivalence classes and boundary values.
- `I` = input modality: pointer, keyboard, touch, screen reader/accessibility action and hardware/system events where applicable.
- `O` = oracle facet: outcome, state transition, persistence, accessibility structure, visual layout, error handling, security boundary or metamorphic relation.

Apply a constraint set `C` to remove invalid combinations and a risk function `ρ` to elevate high-impact interactions.

**(High Confidence)** Covering arrays are appropriate after factor values have been partitioned into meaningful equivalence classes. NIST warns that the input model itself is a significant undertaking and recommends partitioning large value domains rather than attempting to enumerate them. NIST also advises against deriving the model only from existing use cases, because doing so repeats the blind spots of those use cases. [csrc.nist.gov](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software/faqs) [csrc.nist.gov](https://csrc.nist.gov/Projects/automated-combinatorial-testing-for-software/software-testing-methodology/dos-and-don-ts-of-testing) ([csrc.nist.gov](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software/faqs?utm_source=openai))

##### How much t-way coverage?

| Scope | Recommended sampling | Rationale | Confidence |
|---|---|---|---|
| All valid factors | 1-way/value coverage plus all-pairs | Establishes representation of every value and common interactions | High |
| High-risk clusters, such as role × state × data-shape × operation | 3-way or 4-way | Pairwise can miss defects dependent on several simultaneous conditions | High |
| Safety-, payment-, privacy- or data-loss-sensitive clusters | Consider 5–6-way, constrained to a small local factor set | NIST’s broad evidence places almost all observed interaction faults at strengths of six or below | Medium |
| Full UI factor set | Do not generate global 5–6-way arrays blindly | Cost and oracle burden can become disproportionate; UI-specific modern evidence is sparse | High |
| Invalid combinations | Constraints, not test cases | Prevents plans being dominated by states that cannot occur | High |

**(High Confidence)** General combinatorial evidence is strong but not UI-specific. NIST’s 2024 synthesis reports 20×–700× suite-size reductions while retaining fault detection close to exhaustive suites across studied systems. [csrc.nist.gov](https://csrc.nist.gov/pubs/journal/2024/02/combinatorial-testing-for-building-reliable-system/final) ([csrc.nist.gov](https://csrc.nist.gov/pubs/journal/2024/02/combinatorial-testing-for-building-reliable-system/final?utm_source=openai))

**(Medium Confidence)** The closest direct UI-oriented quantitative evidence is older. In NIST’s DOM-events case study, a 4-way suite exposed all faults found by exhaustive testing while using 95% fewer tests; 2-way and 3-way suites detected only 37.5% of those faults. This is strong evidence against treating pairwise as sufficient, but it is one implementation domain and predates the requested horizon. [tsapps.nist.gov](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=913806) ([tsapps.nist.gov](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=913806&utm_source=openai))

<INSUFFICIENT_EVIDENCE>[No broad 2023–2026 replication was found that compares pairwise, 3-way and 4-way sampling across modern React, React Native and SwiftUI applications using real UI defects. Contemporary guidance should therefore treat all-pairs plus risk-selected higher-order coverage as an evidence-informed policy, not a proven universal optimum.]</INSUFFICIENT_EVIDENCE>

##### Coverage metrics that resist “coverage theatre”

<INFERENCE from="NIST interaction coverage; GUI state exploration research; GUITester defect benchmarks; UI MR coverage">A comprehensive plan should report at least these independent adequacy dimensions:</INFERENCE>

1. **Inventory coverage:** proportion of known surfaces, roles, states and transitions represented.
2. **Factor-value coverage:** every modeled value exercised.
3. **Tuple coverage:** valid 2-way and selected t-way obligations covered.
4. **State-transition coverage:** nodes, edges, edge pairs and risk-critical bounded paths.
5. **Flow-depth coverage:** outcomes reached through meaningful multi-step sequences rather than isolated clicks.
6. **Oracle coverage:** which obligations have explicit outcome assertions rather than only execution.
7. **Metamorphic-relation coverage:** relations validated across transformed runs.
8. **Accessibility-semantic coverage:** expected roles, names, values, focus order and actions.
9. **Visual-state coverage:** reviewed baselines by surface/state/context, not screenshot count.
10. **Evidence coverage:** each requirement and test result has a usable artifact.
11. **Defect-sensitivity coverage:** mutation score or seeded-fault detection for the test harness itself.
12. **Duplicate-adjusted coverage:** distinct obligation count after semantic deduplication.

**(Medium Confidence)** A very recent August 2026 preprint evaluated 214 components from four UI libraries and distinguished merely exercising a behavioral relation—“Touch”—from explicitly validating it—“Cover.” MR Cover remained between 42.5% and 47.6% across three model configurations, showing that substantial behavior can be executed without being meaningfully asserted. The inferred MR sample had 88.6% manual usability; test-to-relation alignment reached 96.6% F1 for Touch and 89.7% F1 for Cover. [arxiv.org](https://arxiv.org/abs/2608.03337) ([arxiv.org](https://arxiv.org/abs/2608.03337))

<INFERENCE from="UI MR Touch-versus-Cover results">The plan linter should classify every test as `touch-only`, `structural-oracle`, `outcome-oracle`, `metamorphic-oracle` or `visual-oracle`. Critical-flow tests that are only `touch-only` or presence-based should fail the planning gate.</INFERENCE>

##### What makes generated plans broad and deep?

| Broad rather than repetitive | Deep rather than superficial |
|---|---|
| Generated from an explicit factor model, state graph and requirements—not only source files or visible UI | Asserts a user-observable outcome, persisted state or externalized side effect |
| Contains positive, negative, boundary, recovery and interruption families | Traverses prerequisites and verifies postconditions after navigation or reload |
| Deduplicated by normalized obligation tuple and semantic intent | Includes state restoration and verifies reversibility where promised |
| Covers roles, locales, data shapes, themes and modalities systematically | Checks intermediate transitions when those transitions are contractually meaningful |
| Includes constraints and equivalence classes | Uses metamorphic relations across context transformations |
| Links each case to a requirement or exploratory hypothesis | Can fail when the implementation is subtly wrong, not only absent |

**(High Confidence)** Mozilla’s Firefox study quantifies the need for deduplication and scope validation: of LLM-generated cases across eight features, 27% represented useful scenarios missed by the human plans, 50.5% repeated existing cases, and 22.5% were invalid or out of scope. [mozillafoundation.org](https://www.mozillafoundation.org/en/research/library/using-llms-to-bridge-the-gaps-in-qa-test-plans-at-firefox/) ([mozillafoundation.org](https://www.mozillafoundation.org/en/research/library/using-llms-to-bridge-the-gaps-in-qa-test-plans-at-firefox/?utm_source=openai))

<INFERENCE from="Mozilla plan-generation results">The LLM should be treated as a candidate generator. Deterministic tooling should perform constraint validation and exact duplicate detection, while a second semantic pass clusters near-duplicates and identifies which additional obligation—if any—justifies each variant.</INFERENCE>

##### Documented LLM-plan failure modes

| Failure mode | Evidence or mechanism | Required countermeasure | Confidence |
|---|---|---|---|
| Duplication | Firefox study: 50.5% replicated existing cases | Normalize by precondition, action, expected outcome and coverage tuple; cluster semantic near-duplicates | High |
| Invalid/out-of-scope cases | Firefox study: 22.5% | Validate reachability, selectors, role and data preconditions before accepting | High |
| Happy-path/workflow-confirmation bias | UI manuals and implementation artifacts encourage confirmation of represented flows | Generate from intent/rules first; require negative and invariant families | Medium |
| Presence instead of outcome | Recent MR study found behavior exercised much more often than explicitly validated | Oracle linter rejects visibility assertions when a state or side effect is the requirement | High |
| Faulty-code anchoring | LLM-generated tests can reproduce implementation errors instead of detecting them | Independent requirements/design context; mutation or seeded-fault challenge | High |
| Coverage theatre | Code, activity and screen coverage do not strongly predict failure revelation | Multi-dimensional adequacy dashboard and defect-sensitivity checks | High |
| Self-healing hides product failures | Navigation agents can route around a broken action to complete the task | Never heal across semantically different actions; preserve and report failed primary action | High |

---

#### 1.3 Agent-driven exploratory and flow-discovery testing

##### Techniques and current evidence

| Technique | What it discovers | Oracle strength | Quantitative evidence | Practical verdict |
|---|---|---|---|---|
| Random/Monkey exploration | Crashes and shallow unexpected states | Crash/log oracle | Common baseline; generally weaker than recent model-based and hybrid techniques | Keep as cheap diversity source, never primary coverage method |
| GUI ripping/model-based DFS/BFS | Runtime states, actionable widgets and transitions | Usually crashes plus generic invariants | VLM-Fuzz shows systematic search remains central even when VLM reasoning is added | Core discovery mechanism |
| LLM intent-driven exploration | Semantically plausible tasks and deep workflows | Depends on separate monitor | DroidAgent: 61% activity coverage versus 51% baseline; 317 of 547 generated tasks judged realistic/relevant | Useful for semantic goal generation; needs filtering |
| VLM-assisted hybrid fuzzing | Complex visual widgets, context-sensitive input, deep transitions | Crash logs and optional semantic oracle | VLM-Fuzz: 68.5% class, 53.2% method and 46.5% line coverage over 59 apps | Strongest practical research pattern: deterministic search with selective VLM calls |
| LLM/VLM as functional oracle | Non-crash functional errors | Semantic judgment | OLLM: 49% detection on 71 documented NCF bugs; false positives and randomness remained | Candidate oracle only; require corroboration |
| Property-based UI testing | Long generated interaction traces checked against invariants | Strong when property is valid | Quickstrom found bugs in almost half of tested TodoMVC implementations | High value where temporal properties can be authored |
| Metamorphic UI testing | Cross-run relational errors under controlled transformations | Strong for invariant/monotonic relations | Emerging 2026 component evidence; relation coverage identifies weak oracles | Promote as plan-adequacy and oracle technique |
| Multi-agent exploratory testing | Defect exposure, monitoring and attribution | Better than monolithic navigator | GUITester: 48.90% F1 Pass@3 versus 33.35% strongest baseline | Promising but not CI-blocking maturity |

**(High Confidence)** GPTDroid’s ICSE 2024 evaluation covered 93 Google Play apps, reported 32% greater activity coverage and 31% more bugs than the strongest baseline, and identified 53 new bugs, 35 of which were confirmed and fixed. [doi.org](https://doi.org/10.1145/3597503.3639180) ([arxiv.org](https://arxiv.org/abs/2310.15780?utm_source=openai))

**(High Confidence)** DroidAgent averaged 61% activity coverage against 51% for compared state-of-the-art techniques on 15 apps. Manual review judged 317 of its 547 generated tasks realistic and relevant—about 58%, meaning a substantial minority still lacked practical value. [doi.org](https://doi.org/10.1109/ICST60714.2024.00020) ([research.chalmers.se](https://research.chalmers.se/en/publication/542878))

**(High Confidence)** OLLM detected 49% of 71 documented non-crash functional bugs and reported 24 previously unknown bugs across 64 apps, four of which were confirmed or fixed. Its authors explicitly identified performance degradation, inherent randomness and false positives as limitations. [arxiv.org](https://arxiv.org/abs/2407.19053) ([arxiv.org](https://arxiv.org/abs/2407.19053))

**(High Confidence)** GUITester provides the clearest current warning against a single navigation agent. Its benchmark contains 143 tasks across 26 defects from 12 Android applications. The strongest tested baseline reached 22.95% F1 on one attempt and 33.35% over three attempts; GUITester reached 48.90% over three attempts. Its architecture deliberately separates planning, execution, monitoring and reflective defect attribution. [aclanthology.org](https://aclanthology.org/2026.findings-acl.946/) ([arxiv.org](https://arxiv.org/abs/2601.04500))

**(High Confidence)** GUITester documents two particularly important failure mechanisms:

1. **Goal-oriented masking:** a task-completion agent routes around a broken operation rather than reporting it.
2. **Execution-bias attribution:** the agent assumes that a failure is caused by its own bad click rather than the product.

It also reports slow-loading pages of 6–7 seconds being misclassified as defects and documents a preset 3-second response buffer in one failure case. [aclanthology.org](https://aclanthology.org/2026.findings-acl.946/) ([arxiv.org](https://arxiv.org/abs/2601.04500))

##### Why hybrid exploration currently wins

**(High Confidence)** VLM-Fuzz combines manifest/static information, runtime hierarchy XML, multiple entry points, recursive depth-first search, local exploration and selective GPT-4o calls. Over 59 apps it averaged 68.5% class, 53.2% method and 46.5% line coverage. Relative to APE, gains were 9.0%, 3.7% and 2.1% respectively; relative to DeepGUI they were 10.7%, 5.2% and 2.8%. Tests used a 60-minute budget per app and were repeated five times. [link.springer.com](https://link.springer.com/article/10.1007/s10664-026-10816-4) ([link.springer.com](https://link.springer.com/article/10.1007/s10664-026-10816-4))

**(High Confidence)** The VLM was only invoked on complex screens and the system fell back to static/heuristic interaction when model actions were ambiguous. In a five-app ablation, the VLM increased line coverage by 5.28%; in some apps it provided no gain. [link.springer.com](https://link.springer.com/article/10.1007/s10664-026-10816-4) ([link.springer.com](https://link.springer.com/article/10.1007/s10664-026-10816-4))

<INFERENCE from="VLM-Fuzz architecture and ablations">A reusable skill should use the LLM as a sparse semantic accelerator, not as its state store or coverage engine. The crawler owns the graph, visited set, action ledger, budgets and constraints; the model proposes goals, values and hypotheses.</INFERENCE>

##### Defect yield and benchmark fragility

**(High Confidence)** VLM-Fuzz induced 52 unique crashes across 12 manually confirmed buggy recent apps, compared with 14 for APE. On the Themis benchmark it induced 140 undocumented crashes versus 11 for APE, but only three documented Themis bugs were reproduced by each. Critically, Themis’s own reproduction scripts triggered only 9 of 79 documented bugs due to selector drift, permissions and dead backend services. [link.springer.com](https://link.springer.com/article/10.1007/s10664-026-10816-4) ([link.springer.com](https://link.springer.com/article/10.1007/s10664-026-10816-4))

<INFERENCE from="Themis reproduction decay">The skill must version application binaries, fixtures, backend stubs, accounts, permissions and environment setup alongside every flow. A replay script without its dependency state is not durable evidence.</INFERENCE>

**(Medium Confidence)** Quickstrom represents the strongest directly applicable property-based web UI work found, although published in 2022. It uses finite Linear Temporal Logic properties and hundreds of generated interactions, and reported bugs in almost half of evaluated TodoMVC implementations. [arxiv.org](https://arxiv.org/abs/2203.11532) ([arxiv.org](https://arxiv.org/abs/2203.11532?utm_source=openai))

**(High Confidence)** A June 2026 web-GUI study comparing model-based, reinforcement-learning and LLM-based exploration found no universally superior approach. Strategies exposed complementary failure sets; state abstraction materially changed results; concise functionality-level history worked best for the LLM approach; and code coverage was weakly correlated with failure revelation. [arxiv.org](https://arxiv.org/abs/2606.16650) ([arxiv.org](https://arxiv.org/abs/2606.16650))

<MISSING_DATA>[Direct 2023–2026 controlled comparisons between autonomous exploratory agents and mature, human-authored scripted UI suites were not found. Most papers compare agents against random, model-based or other autonomous baselines, not against an organization’s curated regression suite. Evidence therefore supports agents as complementary discovery mechanisms, not replacements for scripted suites.]</MISSING_DATA>

##### Reliability, latency and cost characteristics

| Approach | Model/parameter dependency | Context representation | Reported execution budget or latency | Monetary cost | License/delivery |
|---|---|---|---|---|---|
| Deterministic Playwright suite | None | Explicit fixture and test state | Suite-dependent; traces are opt-in and often captured on retry | Compute/storage | OSS; exact license not re-verified in this pass |
| Model-based crawler | None or local algorithm | Explicit state graph | Research evaluations commonly use 30–60-minute application budgets | Compute/emulator time | Usually research OSS; varies |
| VLM-Fuzz | GPT-4o; parameter count undisclosed | Screenshot, UI hierarchy, manifest and exploration stack | 60 minutes/app, five repeats in evaluation; loading indicators monitored up to 60 seconds | API cost not published | Research prototype |
| GUITester | UI-TARS variants plus GPT-4o monitor and Qwen-based reflector | Full action trajectory with planner/monitor/reflection roles | 3-second response buffer documented in a failure case; 6–7-second loads produced false positives | API/GPU cost not published | Research code available; license not re-verified |
| Hosted visual clouds | Proprietary service | DOM/page assets or screenshots plus baselines | Build-dependent | Subscription plus browser/render usage | Commercial |

<INSUFFICIENT_EVIDENCE>[Published GUI-agent papers rarely report reproducible per-test API spend, token counts, end-to-end latency distributions or provider rate-limit effects. Model aliases, prices and service limits also change during longitudinal studies.]</INSUFFICIENT_EVIDENCE>

<INFERENCE from="reported 30–60-minute research budgets, model stochasticity and missing cost data">Open-ended agent exploration belongs in scheduled/nightly discovery, not the pull-request critical path. PR CI should run bounded deterministic replays derived from earlier discoveries.</INFERENCE>

---

#### 1.4 Living test documentation and evidence dashboards

##### Recommended artifact architecture

<INFERENCE from="Playwright trace/reporting, Allure identifiers/history, Storybook story IDs/baselines, ReportPortal attachments and Percy DOM snapshots">Build a static single-page evidence application over a normalized JSON manifest. Do not attempt to make a single vendor’s internal model the canonical representation.</INFERENCE>

```text
REQ.AUTH.LOGIN
SURF.AUTH.LOGIN
STATE.AUTH.LOGIN.DEFAULT
STATE.AUTH.LOGIN.ERROR.INVALID_CREDENTIALS
TRANS.AUTH.LOGIN.SUBMIT_VALID
FLOW.AUTH.LOGIN.SUCCESS
CASE.AUTH.LOGIN.SUCCESS.WEB.CHROMIUM
CASE.AUTH.LOGIN.SUCCESS.IOS
RUN.2026-08-18.COMMIT-8F31
ART.RUN-...SCREEN-ACTUAL
ART.RUN-...SCREEN-DIFF
FIND.AUTH.LOGIN.017
```

Recommended canonical entities:

```json
{
  "id": "CASE.AUTH.LOGIN.SUCCESS.WEB.CHROMIUM",
  "kind": "test-case",
  "title": "Valid credentials create an authenticated session",
  "verifies": ["REQ.AUTH.LOGIN"],
  "exercises": [
    "SURF.AUTH.LOGIN",
    "TRANS.AUTH.LOGIN.SUBMIT_VALID",
    "STATE.AUTH.HOME.AUTHENTICATED"
  ],
  "dimensions": {
    "platform": "web",
    "viewport": "desktop-medium",
    "theme": "light",
    "role": "standard-user",
    "locale": "en-US",
    "dataShape": "valid-existing-user",
    "modality": "keyboard"
  },
  "oracle": {
    "type": "state-and-persistence",
    "expectedState": "STATE.AUTH.HOME.AUTHENTICATED"
  },
  "evidence": ["ART.RUN-...TRACE", "ART.RUN-...SCREEN-ACTUAL"],
  "source": {
    "commit": "8f31...",
    "requirementRevision": "REQ.AUTH.LOGIN@4"
  }
}
```

**(High Confidence)** Playwright’s HTML reporter produces a self-contained report folder and supports JSON, JUnit and mergeable blob outputs. Its trace viewer records per-action DOM snapshots, screenshots, source locations, logs, network information and attachments; visual-comparison attachments include expected, actual and diff images. [playwright.dev](https://playwright.dev/docs/test-reporters) [playwright.dev](https://playwright.dev/docs/trace-viewer) ([playwright.dev](https://playwright.dev/docs/test-reporters))

**(High Confidence)** Playwright ARIA snapshots serialize the accessibility tree as YAML and can use partial matching, making them useful as structural-semantic evidence beside pixel output. [playwright.dev](https://playwright.dev/docs/aria-snapshots) ([playwright.dev](https://playwright.dev/docs/aria-snapshots))

**(High Confidence)** Allure’s result schema includes `uuid`, `historyId`, `testCaseId`, `fullName`, `name` and links. The same test with the same parameter set retains its `historyId`, while runs of the same test retain the same `testCaseId`. [allurereport.org](https://allurereport.org/docs/how-it-works-test-result-file/) ([allurereport.org](https://allurereport.org/docs/how-it-works-test-result-file/))

<INFERENCE from="Allure identifier semantics">Framework-generated IDs should be stored, but the skill must also assign its own semantic `CASE-*` identifier. Framework IDs can change when files, titles, parameters or adapters change; the semantic ID must remain stable across framework and platform migrations.</INFERENCE>

##### Tool comparison

| Tool | Strongest role | Reference/evidence capability | Principal failure mode | Delivery |
|---|---|---|---|---|
| **Playwright HTML/Trace** | Web execution debugging | DOM snapshots, screenshots, source, network, logs, attachments and diffs | Run-centric; weak requirement and cross-platform governance | OSS |
| **Allure** | Cross-framework reporting/history | Stable run/test identity fields, labels, links and attachments | History must be persisted correctly; generated identity is not a substitute for business-semantic IDs | OSS core |
| **ReportPortal** | Large-suite failure triage | Launches, attachment previews, retries, pattern and auto-analysis | Retention can delete evidence; statistics and analysis may emphasize the last invocation | OSS/commercial services |
| **Storybook** | Component-state catalogue | Stable/customizable story IDs and isolated component states | Does not prove integrated flow behavior or production state reachability | OSS |
| **Chromatic** | Hosted Storybook visual review | Component baselines, change approval and PR workflow | Component-centric; commercial baseline governance; detailed official page could not be fetched | Commercial |
| **Percy** | Web visual regression | Captures DOM and assets; renders the same snapshot at configured widths | Serialized DOM can lose runtime-only state; web-specific | Commercial |
| **Applitools** | Managed visual comparison | Visual baselines, regions and cross-browser rendering | Independent defect-yield evidence unavailable; vendor performance claims are promotional | Commercial |
| **Testomat** | Test-management layer | Requirements, test cases, runs and automation import | Raw trace quality depends on integrated runner and artifact links | Commercial |
| **Xray** | Jira-native governance | Requirement-test-defect traceability | Screenshot/trace browsing is secondary to Jira issue workflow | Commercial |

**(High Confidence)** Storybook permits a statically readable custom story `id`, and its visual workflow creates baseline snapshots from the first build for future comparisons. [storybook.js.org](https://storybook.js.org/docs/writing-stories/) [storybook.js.org](https://storybook.js.org/docs/writing-tests/visual-testing) ([storybook.js.org](https://storybook.js.org/docs/writing-stories/))

**(High Confidence)** Percy captures a DOM snapshot in the test browser and can render the stored DOM and page assets at multiple responsive widths. Its own documentation warns that serializing and rerendering an already-formed DOM can cause redirects or loss of serialized state such as cleared inputs. [browserstack.com](https://www.browserstack.com/docs/percy/integrate/percy-sdk-workflow) [browserstack.com](https://www.browserstack.com/docs/percy/visual-testing-workflows/view-percy-build-results/responsive-testing) ([browserstack.com](https://www.browserstack.com/docs/percy/integrate/percy-sdk-workflow?utm_source=openai))

**(High Confidence)** ReportPortal supports attachment previews and automatic/pattern-based failure analysis. Its documentation also notes that statistics and auto-analysis consider the last invocation, creating a risk that retry history is deemphasized unless the dashboard exposes it explicitly. [reportportal.io](https://reportportal.io/docs/work-with-reports/ViewLaunches) [reportportal.io](https://reportportal.io/docs/analysis/AutoAnalysisOfLaunches/) ([reportportal.io](https://reportportal.io/docs/analysis/AutoAnalysisOfLaunches/?utm_source=openai))

**(Low Confidence)** Applitools documents visual-comparison and root-cause-analysis capabilities, but the retrieved material was vendor promotional rather than an independent benchmark. No comparative defect-yield number is accepted here. `[SECONDARY: promotional]` [applitools.com](https://applitools.com/wp-content/uploads/2020/03/Applitools_eBook_Achieving_visual_perfection.pdf) ([applitools.com](https://applitools.com/wp-content/uploads/2020/03/Applitools_eBook_Achieving_visual_perfection.pdf?utm_source=openai))

<INSUFFICIENT_EVIDENCE>[No independent longitudinal study was found comparing continued team use versus abandonment of Allure, ReportPortal, Playwright, Storybook, Chromatic, Percy, Applitools, Testomat and Xray. Claims about adoption drivers are therefore inferred from documented workflow characteristics, not measured product retention.]</INSUFFICIENT_EVIDENCE>

<INFERENCE from="stable IDs, trace attachments, baseline workflows, retention controls and requirement links documented by the tools">A dashboard is likely to remain useful when it is generated automatically, opens from CI and pull requests, deep-links to stable IDs, answers “what changed and why?”, co-locates expected/actual/diff with the triggering flow, exposes freshness and retry history, and requires no duplicate manual authoring. It is likely to be abandoned when it is a manually updated status page, a screenshot gallery without state context, or a separate test-management inventory that cannot open raw evidence.</INFERENCE>

##### Dashboard views to implement

1. **Overview:** release gate, critical uncovered obligations, new findings and stale evidence.
2. **Coverage matrix:** surface/state/context tuples, pairwise/t-way completion and risk gaps.
3. **Flow browser:** storyboard frames connected to recorded actions and transitions.
4. **Test case view:** requirement, preconditions, actions, oracle, platform variants and history.
5. **Evidence view:** expected/actual/diff, DOM or native hierarchy, accessibility snapshot, console/logs and trace.
6. **Component catalogue:** semantic component IDs, variants and platform implementations.
7. **Findings view:** anomaly, reproductions, minimization status, linked defect and promotion state.
8. **Provenance view:** commit, build, environment, device/browser, fixture and baseline revision.
9. **Freshness view:** evidence older than relevant implementation or requirement revisions.
10. **Integrity view:** artifact content hashes and missing/broken evidence links.

---

#### 1.5 Cross-platform component and screen capture

| Platform | Runtime structure available | Style/layout introspection | Pixel capture | What is not reliably available | Recommended catalogue source |
|---|---|---|---|---|---|
| **Web** | DOM, accessibility tree, event/attribute state and browser layout tree | `getComputedStyle`, CDP computed-style whitelist, DOM rectangles and paint order | Browser screenshot and trace filmstrip | Original design-token name, logical React component boundary, canvas/WebGL semantics, some cross-origin content | Storybook plus production DOM fingerprints |
| **React Native** | React component tree, props and state in development; platform accessibility/native hierarchy through automation drivers | React props plus platform-native attributes; not CSSOM-equivalent | Device/emulator screenshot | Guaranteed production React tree; one-to-one React-component/native-view mapping | React Native Storybook plus semantic IDs/test IDs |
| **UIKit** | In-process `UIView` hierarchy; XCUITest accessibility-oriented hierarchy out of process | Frames, constraints and view attributes in app/debug process | XCTest/XCUITest screenshot | Source-level component semantics unless instrumented | Preview/demo host plus snapshot suite |
| **SwiftUI** | Accessibility-oriented XCUITest hierarchy; hosting boundary through `UIHostingController` | No supported generic public API for enumerating the original declarative `View` graph and all modifiers | XCTest/XCUITest screenshot | Stable original `View` tree and source modifier identity at runtime | Xcode previews or dedicated component host plus snapshot suite |

**(High Confidence)** On web, `getComputedStyle()` returns a live read-only object containing resolved CSS property values after active stylesheets and computations are applied. Those values are rendered results, not necessarily the original authored values or design tokens. [developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/API/Window/getComputedStyle) ([developer.mozilla.org](https://developer.mozilla.org/en-US/docs/Web/API/Window/getComputedStyle))

**(High Confidence)** Chrome DevTools Protocol’s `DOMSnapshot` domain can return DOM nodes, layout-tree nodes, selected computed styles, DOM rectangles and optional paint-order information. [chromedevtools.github.io](https://chromedevtools.github.io/devtools-protocol/tot/DOMSnapshot/) ([chromedevtools.github.io](https://chromedevtools.github.io/devtools-protocol/tot/DOMSnapshot/))

**(High Confidence)** React Native DevTools exposes the rendered React component tree and allows runtime inspection and modification of component props and state. [reactnative.dev](https://reactnative.dev/docs/react-native-devtools) ([reactnative.dev](https://reactnative.dev/docs/react-native-devtools))

**(Medium Confidence)** That React tree should not be treated as the complete native rendering hierarchy. React components can collapse into, expand into or coordinate several native views, and release/test environments may expose different debugging facilities. <INFERENCE from="React Native’s documented React-component inspector and its native-rendering architecture">Capture both the semantic React component identity and the platform accessibility/native hierarchy rather than trying to derive one from the other.</INFERENCE>

**(High Confidence)** XCUITest’s supported abstraction is `XCUIElement`, representing UI elements exposed to automation. SwiftUI can be hosted in UIKit through `UIHostingController`, but Apple does not document a public production API equivalent to the browser DOM for enumerating an arbitrary SwiftUI source `View` tree. [developer.apple.com](https://developer.apple.com/documentation/xcuiautomation/xcuielement) [developer.apple.com](https://developer.apple.com/documentation/swiftui/uihostingcontroller) ([developer.apple.com](https://developer.apple.com/documentation/xcuiautomation/xcuielement))

##### Reconciling catalogues across the three platforms

<INFERENCE from="different platform introspection capabilities">Define a platform-neutral semantic component contract:</INFERENCE>

```yaml
componentId: DS.BUTTON.PRIMARY
role: button
variants:
  size: [small, medium, large]
  emphasis: [primary]
  state: [default, pressed, focused, disabled, loading]
  theme: [light, dark, high-contrast]
  contentShape: [short-label, long-label, icon-leading]
  modality: [pointer, keyboard, touch, accessibility-action]
platformImplementations:
  web:
    storyId: design-system-button--primary
    selectorContract: '[data-ui-id="DS.BUTTON.PRIMARY"]'
  reactNative:
    storyId: ds-button-primary
    testID: DS.BUTTON.PRIMARY
  ios:
    accessibilityIdentifier: DS.BUTTON.PRIMARY
```

**(High Confidence)** Cross-platform fidelity should be evaluated as two separate contracts:

1. **Semantic parity:** role, accessible name, enabled/disabled state, action, data presentation and state transitions.
2. **Platform fidelity:** typography, spacing, safe-area behavior, control conventions and platform-specific interaction behavior against a platform-specific baseline.

<INFERENCE from="web, React Native and SwiftUI rendering differences">A single cross-platform pixel baseline is unreliable because native controls, fonts, anti-aliasing, safe areas and interaction conventions legitimately differ. Share tokens and semantic IDs, but maintain platform-specific rendered references.</INFERENCE>

##### Cross-platform capture bundle

For every catalogued state, capture:

```text
manifest.json
screen.png
accessibility-tree.json|yaml
structure.json              # DOM/CDP, RN semantic tree, or XCUITest hierarchy
style-or-layout.json        # platform-dependent
interaction-trace.json
console-or-device.log
expected.png
actual.png
diff.png
provenance.json
```

**(High Confidence)** The `structure.json` schema must be explicitly platform-tagged. A DOM snapshot, React component tree and XCUITest accessibility hierarchy are not interchangeable observations.

---

### 2. What is the current state, and what is the strongest supporting evidence for it?

| Capability | State as of August 18, 2026 | Strongest evidence | Confidence |
|---|---|---|---|
| LLM-assisted test-plan ideation | Production-useful with review and deduplication | Firefox: 27% valuable new scenarios, 50.5% duplication, 22.5% invalid/out-of-scope | High |
| Executable web acceptance-test generation | Useful under structured two-stage workflows | Industrial study: 60% usable directly; remaining 40% needed intervention or disposal | High |
| Systematic coverage-space reduction | Mature generally; limited modern UI-specific validation | NIST general reductions of 20×–700×; older DOM 4-way result | High general / Medium UI |
| Autonomous semantic exploration | Effective complement to crawlers and scripts | GPTDroid and DroidAgent coverage/task results | High for Android research |
| Autonomous non-crash oracle | Experimental | OLLM 49% detection with randomness and false positives | High |
| Fully autonomous exploratory defect discovery | Promising but not trustworthy enough for blocking CI | GUITester 48.90% F1 Pass@3 | High |
| Hybrid VLM/search exploration | Current strongest research architecture | VLM-Fuzz systematic search, selective VLM and measured gains | High |
| Property-based UI testing | Technically strong but sparsely adopted/evaluated | Quickstrom TodoMVC study | Medium |
| UI metamorphic adequacy | Emerging | August 2026 MR Cover/Touch study | Medium; preprint |
| Living execution reports | Mature per framework | Playwright, Allure, ReportPortal | High |
| Unified cross-platform evidence graph | Requires custom integration | No single tool spans all required entities and platform artifacts | High inference |

**(High Confidence)** The strongest overall evidence supports **augmentation, not replacement**. LLMs find scenarios and semantic flows that deterministic techniques miss, but they also duplicate cases, invent invalid scenarios, miss most benchmark defects, misattribute anomalies and lack stable independent oracles. ([mozillafoundation.org](https://www.mozillafoundation.org/en/research/library/using-llms-to-bridge-the-gaps-in-qa-test-plans-at-firefox/?utm_source=openai))

<INFERENCE from="the complementary strengths observed across combinatorial, state-based, property-based, LLM and visual techniques">“Comprehensive” should be defined as the union of independently measured adequacy dimensions, not the output of one generator or the use of one test framework.</INFERENCE>

---

### 3. What are the contrasting viewpoints or competing evidence?

#### Pairwise is enough versus higher-order coverage

**(High Confidence)** Pairwise is inexpensive and captures many common interactions, but the NIST DOM study is direct counter-evidence to treating it as sufficient: 2-way and 3-way tests detected only 37.5% of the study’s faults, while 4-way detected all faults found by exhaustive testing. [tsapps.nist.gov](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=913806) ([tsapps.nist.gov](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=913806&utm_source=openai))

**(Medium Confidence)** Conversely, global high-strength covering arrays can generate excessive cost and oracle work. <INFERENCE from="NIST’s need for equivalence partitioning and the lack of broad modern UI replication">Use higher strengths locally on risk clusters, not globally across every UI dimension.</INFERENCE>

#### Structural/code coverage versus defect yield

**(High Confidence)** Higher structural coverage can improve reach but does not prove useful assertions or failure detection. The 2026 web study found weak correlation between code coverage and failure revelation, while the 2026 MR study found that behavioral relations were frequently exercised without being explicitly validated. [arxiv.org](https://arxiv.org/abs/2606.16650) [arxiv.org](https://arxiv.org/abs/2608.03337) ([arxiv.org](https://arxiv.org/abs/2606.16650))

**(High Confidence)** Structural metrics should therefore remain diagnostic rather than serve as sole release gates.

#### LLM reasoning versus deterministic crawling

**(High Confidence)** LLMs can create realistic goals and discover distinctive failures, as GPTDroid and DroidAgent show. Deterministic search remains more systematic and less expensive per action, as VLM-Fuzz’s architecture and ablation show. [doi.org](https://doi.org/10.1145/3597503.3639180) [doi.org](https://doi.org/10.1109/ICST60714.2024.00020) [link.springer.com](https://link.springer.com/article/10.1007/s10664-026-10816-4) ([portal.fis.tum.de](https://portal.fis.tum.de/de/publications/make-llm-a-testing-expert-bringing-human-like-interaction-to-mobi/?utm_source=openai))

<INFERENCE from="complementary measured strengths">The correct contest is not “LLM versus crawler”; it is “LLM-owned exploration” versus “crawler-owned exploration with selective LLM assistance.” The latter currently has stronger reliability evidence.</INFERENCE>

#### Pixel diff versus semantic/AI visual comparison

**(High Confidence)** Pixel diffs are transparent and sensitive but noisy under font rendering, animation, dynamic content and environmental variation. DOM-based cloud rendering improves reproducibility but can lose runtime-only state, as Percy documents. [browserstack.com](https://www.browserstack.com/docs/percy/integrate/percy-sdk-workflow) ([browserstack.com](https://www.browserstack.com/docs/percy/integrate/percy-sdk-workflow?utm_source=openai))

**(Low Confidence)** Proprietary “visual AI” may reduce irrelevant differences, but independent comparisons using representative application defects are scarce. Vendor claims should not determine CI policy without an internal seeded-fault evaluation.

#### Buy a dashboard versus build one

**(High Confidence)** Existing products are mature within their own layer but fragmented across requirements, component stories, flow execution, visual review and cross-platform evidence.

<INFERENCE from="tool capability boundaries">Build the canonical manifest and thin evidence SPA; buy or embed expensive commodity capabilities such as hosted browser rendering, visual review and enterprise Jira governance when they are operationally justified.</INFERENCE>

<MISSING_DATA>[The target team size, regulated-industry obligations, existing Jira/TestRail investment, expected test volume and acceptable SaaS spend were not supplied. A precise build-versus-buy recommendation requires those inputs.]</MISSING_DATA>

---

### 4. What changed recently, and what is the trajectory?

**(High Confidence)** In 2023–2024, the main advance was semantic exploration: GPTDroid and DroidAgent showed that LLM memory and app semantics could produce deeper, more realistic interactions than traditional crawlers. Non-crash functional oracles remained weak and stochastic. [doi.org](https://doi.org/10.1145/3597503.3639180) [doi.org](https://doi.org/10.1109/ICST60714.2024.00020) [arxiv.org](https://arxiv.org/abs/2407.19053) ([portal.fis.tum.de](https://portal.fis.tum.de/de/publications/make-llm-a-testing-expert-bringing-human-like-interaction-to-mobi/?utm_source=openai))

**(High Confidence)** In 2025–2026, the architecture shifted from monolithic prompting toward explicit state, memory and role separation: VLM-Fuzz combines deterministic DFS and selective vision calls; GUITester separates planner, executor, monitor and reflector; 2026 web evidence emphasizes state abstraction and concise functionality-level history. [link.springer.com](https://link.springer.com/article/10.1007/s10664-026-10816-4) [aclanthology.org](https://aclanthology.org/2026.findings-acl.946/) [arxiv.org](https://arxiv.org/abs/2606.16650) ([link.springer.com](https://link.springer.com/article/10.1007/s10664-026-10816-4))

**(Medium Confidence)** By August 2026, adequacy research is beginning to move beyond execution coverage toward explicit behavioral-relation coverage. The new UI metamorphic-relation work is promising, but remains a preprint and has not yet established independent replication or industrial maintenance cost. [arxiv.org](https://arxiv.org/abs/2608.03337) ([arxiv.org](https://arxiv.org/abs/2608.03337))

<INFERENCE from="the 2023–2026 sequence of results">The trajectory is toward a layered test agent whose durable intelligence resides in explicit models, graphs, contracts and evidence—not in ever-larger prompts. Models will increasingly propose semantics and evaluate ambiguous evidence, while deterministic infrastructure owns coverage accounting, replay, identity and release gates.</INFERENCE>

---

## Evidence Table

| Claim | Primary Source | Publication Date | Evidence Type | URL |
|---|---|---:|---|---|
| General combinatorial testing can reduce suites 20×–700× while approaching exhaustive fault detection | Raunak, Kuhn, Kacker, Lei / NIST | February 5, 2024 | Peer-reviewed journal article; authoritative primary synthesis | https://csrc.nist.gov/pubs/journal/2024/02/combinatorial-testing-for-building-reliable-system/final |
| DOM 4-way testing found all studied faults with 95% fewer tests; 2/3-way found 37.5% | NIST, *Combinatorial Testing Applied* | 2012 | Primary empirical UI-adjacent case study; retained as foundational exception | https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=913806 |
| LLM Firefox plans: 27% useful new, 50.5% duplicate, 22.5% invalid/out of scope | Mozilla Foundation / Mujahid et al. | January 16, 2026 | Primary industrial case study by application owner | https://www.mozillafoundation.org/en/research/library/using-llms-to-bridge-the-gaps-in-qa-test-plans-at-firefox/ |
| Two-stage acceptance generation: 60% executable cases directly usable | Ferreira, Viegas, Faria, Lima | April 9, 2025 | Primary industrial study/preprint | https://arxiv.org/abs/2504.07244 |
| GPTDroid: +32% activity coverage, +31% bugs; 53 new, 35 confirmed/fixed | Liu et al., ICSE 2024 | May 20, 2024 | Peer-reviewed conference paper; primary empirical benchmark | https://doi.org/10.1145/3597503.3639180 |
| DroidAgent: 61% versus 51% activity coverage; 317/547 tasks relevant | Yoon, Feldt, Yoo, ICST 2024 | 2024 | Peer-reviewed conference paper; primary empirical study | https://doi.org/10.1109/ICST60714.2024.00020 |
| LLM non-crash oracle: 49% detection on 71 bugs; randomness and false positives | Ju et al. | July 26, 2024 | Primary empirical preprint | https://arxiv.org/abs/2407.19053 |
| GUITester: 48.90% F1 Pass@3 versus 33.35% baseline | Gao et al., ACL Findings 2026 | July 2026 | Peer-reviewed conference findings; primary benchmark | https://aclanthology.org/2026.findings-acl.946/ |
| VLM-Fuzz coverage and defect results across 59 apps | Demissie et al., *Empirical Software Engineering* | February 2026 | Peer-reviewed journal article; primary empirical study | https://link.springer.com/article/10.1007/s10664-026-10816-4 |
| No exploration strategy dominates; state abstraction and functionality history matter | Liu, Yang, Zhang, Xie | June 15, 2026 | Primary empirical preprint; under-review status noted | https://arxiv.org/abs/2606.16650 |
| Property-based temporal UI tests found bugs in almost half of TodoMVC implementations | O’Connor, Wickström | March 22, 2022 | Primary property-based UI study; foundational exception | https://arxiv.org/abs/2203.11532 |
| UI MR Cover 42.5%–47.6% across 214 components | Pei, Zhang, Sohn, Papadakis | August 4, 2026 | Very recent primary preprint; no independent replication yet | https://arxiv.org/abs/2608.03337 |
| LLM test generators can validate faulty implementation behavior | Ryan et al. | December 18, 2024 | Primary empirical preprint | https://arxiv.org/abs/2412.14137 |
| Faulty generated code can bias subsequent test generation | Konstantinou, Tambon, Papadakis | July 6, 2026 | Primary empirical preprint | https://arxiv.org/abs/2607.05139 |
| Playwright HTML, JSON, JUnit and blob report capabilities | Microsoft Playwright documentation | Living docs, accessed August 18, 2026 | Official product documentation; mechanism only | https://playwright.dev/docs/test-reporters |
| Playwright traces expose DOM snapshots, screenshots, source, logs and attachments | Microsoft Playwright documentation | Living docs, accessed August 18, 2026 | Official product documentation; mechanism only | https://playwright.dev/docs/trace-viewer |
| Playwright ARIA snapshots represent the accessibility tree as YAML | Microsoft Playwright documentation | Living docs, accessed August 18, 2026 | Official product documentation | https://playwright.dev/docs/aria-snapshots |
| Allure `historyId` and `testCaseId` semantics | Allure documentation | Living docs, accessed August 18, 2026 | Official schema documentation | https://allurereport.org/docs/how-it-works-test-result-file/ |
| Storybook custom story IDs and visual baselines | Storybook documentation | Living docs, accessed August 18, 2026 | Official documentation | https://storybook.js.org/docs/writing-stories/ |
| Percy captures and rerenders DOM snapshots at responsive widths | BrowserStack Percy documentation | Living docs, accessed August 18, 2026 | Official vendor documentation; mechanism only | https://www.browserstack.com/docs/percy/integrate/percy-sdk-workflow |
| ReportPortal attachment preview and auto-analysis behavior | ReportPortal documentation | Living docs, accessed August 18, 2026 | Official documentation | https://reportportal.io/docs/work-with-reports/ViewLaunches |
| Web resolved-style inspection | Mozilla MDN | Living docs, accessed August 18, 2026 | Authoritative web-platform documentation | https://developer.mozilla.org/en-US/docs/Web/API/Window/getComputedStyle |
| CDP can return DOM, layout nodes, computed styles, rectangles and paint order | Chrome DevTools Protocol | Living docs, accessed August 18, 2026 | Official browser protocol schema | https://chromedevtools.github.io/devtools-protocol/tot/DOMSnapshot/ |
| React Native DevTools exposes React component tree and props/state | Meta React Native documentation | Living docs, accessed August 18, 2026 | Official framework documentation | https://reactnative.dev/docs/react-native-devtools |
| XCUITest exposes automation elements through `XCUIElement` | Apple Developer Documentation | Living docs, accessed August 18, 2026 | Official platform documentation | https://developer.apple.com/documentation/xcuiautomation/xcuielement |
| SwiftUI content can be hosted through `UIHostingController` | Apple Developer Documentation | Living docs, accessed August 18, 2026 | Official platform documentation | https://developer.apple.com/documentation/swiftui/uihostingcontroller |

---

## Knowledge Gaps

### UI-specific empirical gaps

- <MISSING_DATA>[A contemporary cross-platform study comparing pairwise, 3-way and 4-way sampling on real defects in React, React Native and SwiftUI. Required: common seeded and historical defect corpus, identical equivalence partitions and controlled oracle quality.]</MISSING_DATA>
- <MISSING_DATA>[Direct defect-yield comparisons between autonomous agents and mature human-authored scripted regression suites. Existing papers primarily compare autonomous techniques with other automated explorers.]</MISSING_DATA>
- <MISSING_DATA>[Substantial autonomous-testing benchmarks for React Native and SwiftUI/UIKit. Current quantitative evidence is heavily Android-centric.]</MISSING_DATA>

### Operational gaps

- <MISSING_DATA>[Reproducible token usage, per-app API spend, latency distributions and rate-limit effects for published LLM/VLM testing agents.]</MISSING_DATA>
- <MISSING_DATA>[Longitudinal maintenance cost for agent-generated flows after six to twelve months of UI evolution.]</MISSING_DATA>
- <MISSING_DATA>[Target team size, test volume, current test-management stack, SaaS constraints and regulated evidence-retention requirements; these are required for a precise build-versus-buy decision.]</MISSING_DATA>

### Dashboard and product-comparison gaps

- <INSUFFICIENT_EVIDENCE>[No independent longitudinal evidence was found showing which named evidence dashboards are actively used versus abandoned after deployment.]</INSUFFICIENT_EVIDENCE>
- <INSUFFICIENT_EVIDENCE>[Independent comparative defect-yield evidence for proprietary visual-AI products remains limited. Vendor claims should be validated with the team’s own visual-fault corpus.]</INSUFFICIENT_EVIDENCE>
- <MISSING_DATA>[Current plan-specific API rate limits and storage-retention limits for Chromatic, Percy, Applitools, Testomat and Xray were not verified and should not be hard-coded into the skill.]</MISSING_DATA>

### Research maturity gaps

- <CONFIDENCE:LOW>[The August 2026 UI metamorphic-relation findings are directionally important but remain a recent preprint without independent replication.]</CONFIDENCE:LOW>
- <CONFIDENCE:LOW>[The June 2026 web exploration/state-abstraction study is useful current evidence but was still listed as under review rather than a final peer-reviewed publication.]</CONFIDENCE:LOW>

---

## Recommended Next Steps

1. **Build a seeded-fault benchmark for the skill.**  
   **Rationale:** Evaluate at least one web, React Native and SwiftUI application with known behavioral, visual, accessibility, persistence and state-transition faults. Measure distinct fault detection, false-positive rate, deterministic replay rate, runtime and maintenance—not only generated test count or code coverage.

2. **Specify the canonical evidence-manifest and stable-ID contract before implementing the dashboard.**  
   **Rationale:** Requirement, surface, state, transition, flow, case, run, artifact and finding IDs are the integration boundary across Playwright, Storybook, XCUITest, Android tooling and third-party reporting products. Retrofitting stable identity later will be expensive and break references.

3. **Prototype the hybrid explorer, not an end-to-end free-form agent.**  
   **Rationale:** Implement a deterministic state graph, action ledger, reset engine, tarpit detection and coverage accountant first. Add an LLM/VLM only for semantic goal ranking, input generation and anomaly hypotheses. Use separate planner, executor, monitor and verifier contexts.

4. **Implement a plan-adequacy challenge suite.**  
   **Rationale:** Automatically inject UI mutants or controlled faults—disabled action, wrong destination, lost persistence, stale data, clipped text, inaccessible name, theme contrast failure—and verify that generated tests fail. This directly detects presence-only assertions, implementation anchoring and coverage theatre.

5. **Run a build-versus-buy evidence-dashboard spike.**  
   **Rationale:** Generate the canonical static SPA and embed Playwright/Allure artifacts. In parallel, test one hosted visual product and the organization’s likely test-management product. Compare review time, artifact retention, deep-link stability, false-positive triage and recurring cost using the same benchmark rather than vendor demonstrations.

## Sources

- [Combinatorial Testing for Building Reliable Systems | CSRC](https://csrc.nist.gov/pubs/journal/2024/02/combinatorial-testing-for-building-reliable-system/final?utm_source=openai)
- [Using LLMs to Bridge the Gaps in QA Test Plans at Firefox - Mozilla Foundation](https://www.mozillafoundation.org/en/research/library/using-llms-to-bridge-the-gaps-in-qa-test-plans-at-firefox/?utm_source=openai)
- [Make LLM a Testing Expert: Bringing Human-Like Interaction to Mobile GUI Testing via Functionalit...](https://portal.fis.tum.de/de/publications/make-llm-a-testing-expert-bringing-human-like-interaction-to-mobi/?utm_source=openai)
- [VLM-Fuzz: Vision language model assisted recursive depth-first search exploration for effective G...](https://link.springer.com/article/10.1007/s10664-026-10816-4)
- [Chrome DevTools Protocol - DOMSnapshot domain](https://chromedevtools.github.io/devtools-protocol/tot/DOMSnapshot/)
- [Acceptance Test Generation with Large Language Models: An Industrial Case Study](https://arxiv.org/abs/2504.07244?utm_source=openai)
- [Design choices made by LLM-based test generators prevent them from finding bugs](https://arxiv.org/abs/2412.14137?utm_source=openai)
- [Combinatorial Methods for Trust and Assurance | CSRC](https://csrc.nist.gov/projects/automated-combinatorial-testing-for-software/faqs?utm_source=openai)
- [Combinatorial Testing Applied](https://tsapps.nist.gov/publication/get_pdf.cfm?pub_id=913806&utm_source=openai)
- [Assessing Behavioral Validation in UI Component Test Suites Using Inferred Metamorphic Relations](https://arxiv.org/abs/2608.03337)
- [Make LLM a Testing Expert: Bringing Human-like Interaction to Mobile GUI Testing via Functionalit...](https://arxiv.org/abs/2310.15780?utm_source=openai)
- [Intent-Driven Mobile GUI Testing with Autonomous Large Language Model Agents](https://research.chalmers.se/en/publication/542878)
- [A Study of Using Multimodal LLMs for Non-Crash Functional Bug Detection in Android Apps](https://arxiv.org/abs/2407.19053)
- [GUITester: Enabling GUI Agents for Exploratory Defect Discovery](https://arxiv.org/abs/2601.04500)
- [Quickstrom: Property Based Acceptance Testing with LTL Specifications](https://arxiv.org/abs/2203.11532?utm_source=openai)
- [Understanding Automated Web GUI Testing: An Empirical Study Across Exploration Strategies and Sta...](https://arxiv.org/abs/2606.16650)
- [Reporters | Playwright](https://playwright.dev/docs/test-reporters)
- [Snapshot testing | Playwright](https://playwright.dev/docs/aria-snapshots)
- [Allure Report Docs – Test result file](https://allurereport.org/docs/how-it-works-test-result-file/)
- [How to write stories | Storybook docs](https://storybook.js.org/docs/writing-stories/)
- [Percy SDK and screenshot capture workflow | BrowserStack Docs](https://www.browserstack.com/docs/percy/integrate/percy-sdk-workflow?utm_source=openai)
- [Auto-Analysis of launches | ReportPortal Documentation](https://reportportal.io/docs/analysis/AutoAnalysisOfLaunches/?utm_source=openai)
- [Achieving visual](https://applitools.com/wp-content/uploads/2020/03/Applitools_eBook_Achieving_visual_perfection.pdf?utm_source=openai)
- [Window: getComputedStyle() method - Web APIs | MDN](https://developer.mozilla.org/en-US/docs/Web/API/Window/getComputedStyle)
- [React Native DevTools · React Native](https://reactnative.dev/docs/react-native-devtools)
- [XCUIElement | Apple Developer Documentation](https://developer.apple.com/documentation/xcuiautomation/xcuielement)
