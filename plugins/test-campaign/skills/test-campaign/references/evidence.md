# Evidence — where each rule came from, and what it does not prove

Every load-bearing rule in this skill traces to something measured. This file
carries those measurements with their sources, the three places the research
disagrees with itself, and the two figures that were **withdrawn** after their
only source turned out not to exist.

Read it when you need to justify a rule, tune it, or argue against it. Not on
every run.

---

## How this was gathered

Three deep-research panels, run 2026-08-18, on the same four-part question
(coverage models and plan generation · agent-driven exploration · living evidence
dashboards · cross-platform capture). Reports are in `docs/deep-research/`, each
beside its own `.sources.md`.

A **fourth pass, 2026-08-19**, on native desktop verification, after a campaign
reported 100% checked over two desktop applications that had never drawn a window
(`on-glass.md` §1). It ran in two halves: a sweep of 452 existing reports in the
local research store for what was already known about macOS, and one new
deep-research run for Windows and Linux, where the sweep found **nothing usable
at all** — no UI Automation, no Windows capture semantics, no AT-SPI2, no
Wayland. That run is
`docs/deep-research/gemini-native-desktop-on-glass.md` (`dr_520a53de0ba977ac`,
max tier, 106 sources, ~$7).

Citations were dereferenced afterwards. **That check earns its place:** the
OpenAI report came back 83% live with its one 404 a moved NIST page whose claim
had other live sources, while the Gemini report came back with two figures whose
*only* source no longer exists. Those two are recorded below as withdrawn, and
neither appears anywhere in the skill.

The 2026-08-19 run came back **101 of 106 citations live**, with five that do not
resolve and two claims left with no surviving source. Both were chased by hand
rather than dropped or kept on trust, and the outcome is recorded under *Native
desktop* below: one turned out to be **better** sourced than the report had it,
straight from the vendor's own API reference; the other is withdrawn.

`live` means the URL resolves. It does not mean the source supports the claim
attached to it — that still needs a reader, and the numbers below were read.

---

## Coverage and sampling

| Finding | Number | Source | Standing |
|---|---|---|---|
| Combinatorial sampling reduces suites while approaching exhaustive fault detection | **20×–700×** | Raunak, Kuhn, Kacker, Lei (NIST), Feb 2024, peer-reviewed | High. General software, not UI-specific. |
| Higher-strength coverage on a DOM-driven system | **4-way found every fault exhaustive testing found, with 95% fewer tests; 2-way and 3-way found 37.5%** | NIST, *Combinatorial Testing Applied*, 2012 | High for the study, but 2012 and never replicated on a modern component stack. |
| A model built only from existing use cases | reproduces those use cases' blind spots | NIST combinatorial-testing guidance | The reason `project-comprehension.md` runs before enumeration. |

**Disagreement #1 — is pairwise enough?** Two of the three panels take pairwise
as the practical baseline on the general CIT result. The third treats the DOM
study as direct counter-evidence against calling it sufficient. Neither side has
a modern UI replication. The skill takes pairwise as the global floor and raises
strength locally on risk clusters, and says so as a judgement rather than a
finding (`coverage-model.md` §2).

---

## Generated test plans and generated tests

| Finding | Number | Source | Standing |
|---|---|---|---|
| LLM-generated QA scenarios classified by the application's own QA team | **27% valuable and new · 50.5% duplicates · 22.5% invalid or out of scope** | Mozilla Foundation / Mujahid et al., Jan 2026 | High. Primary industrial case study by the application owner. The single most useful number here. |
| Two-stage generation of executable acceptance tests | **60% usable as generated**; the rest needed repair, regeneration or disposal | Ferreira, Viegas, Faria, Lima, Apr 2025 | High. Industrial study/preprint. |
| LLM-generated unit tests | limited defect detection driven by **low validity**; chain-of-thought and generic RAG **did not help and sometimes hurt**; more surrounding context **reduced** effectiveness | Empirical study of 5 open-source code LLMs (7B–34B) vs GPT-4 and EvoSuite over 17 Defects4J projects, 2024 | High for unit tests. Extrapolation to UI is inference, and is labelled as such. |
| Generated tests can encode the bug | test generators validate faulty implementation behaviour | Ryan et al., Dec 2024 | High. The basis for "the model that wrote the code is not its oracle". |
| Faulty code in context biases later generation | measured | Konstantinou, Tambon, Papadakis, Jul 2026 | Preprint. Same direction as the above. |

**What these say together:** generation is worth doing, and roughly half of what
it produces is redundant. Deduplication against an explicit coverage model is
therefore most of the value, not a polish step.

---

## Exploration, and where it belongs

| Finding | Number | Source | Standing |
|---|---|---|---|
| LLM-driven Android exploration vs baseline | **+32% activity coverage, +31% bugs**; 53 new, 35 confirmed or fixed | GPTDroid, ICSE 2024 | High, peer-reviewed. Android. |
| Autonomous LLM agent exploration | **61% vs 51%** activity coverage; 317/547 tasks judged relevant | DroidAgent, ICST 2024 | High, peer-reviewed. Android. |
| Vision-model assistance inside a deterministic crawler | the VLM contributed **~5.28%** additional line coverage | VLM-Fuzz, *Empirical Software Engineering*, Feb 2026 | High. The number that decides the architecture: the crawler owns the state, the model is a sparse accelerator. |
| LLM as a non-crash functional oracle | **49%** detection over 71 bugs, with randomness and false positives | Ju et al., Jul 2024 | High. Why a model verdict never gates alone. |
| Exploratory GUI agent defect discovery | **48.90% F1 (Pass@3)** vs 33.35% baseline | GUITester, ACL Findings 2026 | High for the benchmark. Well short of a gate. |
| No exploration strategy dominates | model-based, RL and LLM strategies exposed **complementary** failure sets; state abstraction changed results materially; **code coverage correlated weakly with failure revelation** | Liu, Yang, Zhang, Xie, Jun 2026 | Preprint, listed as under review. |
| Random vs model-based, industrially | Monkey took highest method coverage on 22/41 apps and highest activity coverage on 35/68; **Stoat triggered the most unique crashes on 23** | Android industrial study, 68 apps, 2018 | High. Coverage and fault-finding are not the same axis — the empirical root of "coverage theatre". |

**Disagreement #2 — can an agent replace a scripted suite?** No panel found a
controlled comparison between autonomous agents and a mature human-authored
regression suite; every study compares agents against random, model-based or
other agents. The evidence supports agents as *complementary discovery*, and the
skill places them in scheduled runs feeding deterministic replays, never on the
pull-request path.

---

## Oracles

| Finding | Number | Source | Standing |
|---|---|---|---|
| UI component suites exercise behavioural relations far more than they validate them | **MR Cover 42.5%–47.6%** across 214 components | Pei, Zhang, Sohn, Papadakis, Aug 2026 | **Low–medium.** Very recent preprint, no independent replication. Directional only — it motivates the oracle ladder; it is not a threshold. |
| Property-based temporal UI testing | found bugs in almost half of the TodoMVC implementations evaluated | Quickstrom, Mar 2022 | Medium. Strongest directly applicable PBT-for-web work found, and it is four years old. |
| GUI-level metamorphic relations | detected five classes of real credential-handling vulnerability | 2025 study | High for its scope. Evidence that metamorphic relations reach defects functional checks miss. |

**Disagreement #3 — pixel diffing.** All three panels agree pixel comparison is
sensitive and noisy under font rendering, animation and dynamic content, and that
DOM-serialising cloud renderers trade that noise for a different failure — Percy
documents that re-rendering an already-formed DOM can lose runtime-only state
such as cleared inputs. Where they part is whether proprietary "visual AI"
resolves it: one panel reports vendor claims, the other two record that
independent comparative defect-yield evidence does not exist. The skill treats a
pixel diff as a tripwire rather than a verdict, and buys nothing on a vendor
claim.

---

## Evidence, identity and dashboards

- **Framework IDs are not semantic IDs.** Allure's `historyId` holds across runs
  of the same test with the same parameters and `testCaseId` across runs of the
  same test — but both are generated from files, titles, parameters and adapters,
  so they change when any of those do. Store them, and assign your own `CASE-*`
  identity that survives a harness or platform migration.
- **Playwright supplies the richest per-step evidence available for free**: trace
  DOM snapshots, screenshots, source locations, logs, network, attachments, and
  expected/actual/diff images for visual comparisons; ARIA snapshots serialise
  the accessibility tree as YAML with partial matching, which makes structural
  evidence assertable rather than merely viewable.
- **What makes a dashboard survive**, inferred consistently across all three
  panels from documented workflow characteristics rather than from any retention
  study: it is generated automatically, opens from CI and the pull request,
  deep-links stable IDs, answers "what changed and why", co-locates
  expected/actual/diff with the flow that produced it, exposes freshness and
  retry history, and requires no duplicate manual authoring. It is abandoned when
  it is a hand-updated status page, a screenshot gallery without state context,
  or an inventory that cannot open raw evidence.
- **No independent longitudinal study exists** comparing continued use versus
  abandonment of Allure, ReportPortal, Playwright, Storybook, Chromatic, Percy,
  Applitools, Testomat or Xray. The bullet above is inference, and is marked so.
- **No single product spans the required entities.** Requirements, component
  stories, flow execution, visual review and cross-platform evidence are
  fragmented across mature per-layer tools. Hence: own the manifest and the thin
  page; embed the commodity capabilities.

---

## Platform introspection ceilings

These are capability facts, and they set what a campaign can honestly claim per
lane (`harness-lanes.md` carries the operational version).

- **Web** — `getComputedStyle` returns *resolved* values after stylesheets apply:
  rendered results, not authored values and not design-token names. CDP's
  `DOMSnapshot` adds layout nodes, selected computed styles, rectangles and paint
  order. Full introspection, with the caveat that the token name is gone by the
  time you can read the value.
- **React Native** — DevTools exposes the rendered React component tree with
  props and state, but that tree is **not** the native rendering hierarchy: one
  component can collapse into or expand into several native views, and
  release builds expose different facilities than development ones. Capture the
  React identity *and* the platform accessibility hierarchy; do not derive one
  from the other.
- **SwiftUI / UIKit** — the supported automation abstraction is `XCUIElement`,
  which is accessibility-oriented. SwiftUI content can be hosted through
  `UIHostingController`, but Apple documents **no public API equivalent to the
  DOM** for enumerating an arbitrary SwiftUI `View` graph and its modifiers at
  runtime. A SwiftUI component catalogue comes from previews or a dedicated host
  plus a snapshot suite — never from a runtime style tree, because there isn't
  one.
- **Cross-platform reconciliation happens at the semantic contract**, not by
  pretending the runtime trees are equivalent. Two contracts, judged separately:
  *semantic parity* (role, accessible name, enabled state, action, data
  presentation, transitions) and *platform fidelity* (typography, spacing,
  safe-area, control conventions) against a platform-specific baseline. A single
  cross-platform pixel baseline is unreliable by construction — native controls,
  fonts, anti-aliasing and safe areas legitimately differ.

---

## Native desktop, and verification on glass

The operational version is `on-glass.md` and `harness-lanes.md`. What follows is
where each claim came from and how far it goes.

| Finding | Source | Standing |
|---|---|---|
| `SendInput` fails under UIPI, and **neither the return value nor `GetLastError` indicates UIPI as the cause**; injection is permitted only into applications at equal or lesser integrity | Microsoft's `SendInput` reference, `winuser.h` | **Highest in this section.** Verbatim from the vendor's own API documentation, fetched and read. The single best-evidenced silent-failure mode on any lane. |
| Deep UIA tree enumeration in WinUI 3 can raise a native `0xc0000005` in `Microsoft.UI.Xaml.dll`; the workaround is depth-capping plus per-node `try`/`catch` | `microsoft/microsoft-ui-xaml` issue 11028 | High. Vendor's own issue tracker, with the workaround stated there rather than inferred. |
| Qt's UIA backend (5.11+) distinguishes controls largely by `LocalizedControlType` rather than semantic control type, and does not raise some state-change events | `nvaccess/nvda` issue 8604 | Medium–high. A screen-reader project's issue tracker — a practitioner report rather than a vendor statement, and the practitioners in question are the ones who consume the API. |
| Windows has **no per-frame validity signal**; desktop duplication offers only dirty-rects and move-rects | Microsoft desktop-duplication API docs | High, and it is an *absence* — the strongest asymmetry with macOS in the whole matrix. |
| A minimised window has no current composition to capture; the compositor retains only the last bitmap it drew | vendor docs plus secondary corroboration | Medium. The behaviour is consistently reported and the mechanism is documented; the exact retention semantics are not stated in one authoritative place. |
| `WDA_EXCLUDEFROMCAPTURE` removes a window from all capture | Windows display-affinity docs | High for the API. One of the two sources attached to it in the report is dead; the surviving one is the vendor's. |
| Hybrid-GPU mismatch fails desktop duplication with `DXGI_ERROR_UNSUPPORTED` | practitioner write-up | Medium. Reproducible and widely reported, not vendor-confirmed in the material read. |
| GitHub's `windows-latest` runner provides an interactive desktop, and defaults to **1024×768** | `actions/runner-images` issue 2935 | High. The runner project's own tracker. The resolution is the number to act on. |
| Windows services run in Session 0 with no interactive desktop | Windows session-isolation docs | High, and long-standing. |
| Closing RDP locks the desktop and destroys the GUI context; `tscon %sessionname% /dest:console` is the documented workaround | test-tool vendor documentation | Medium–high. Vendor documentation for the technique rather than a Microsoft statement, and the technique is decades old. |
| Wayland removes X11's global capture and injection; automation goes through the XDG RemoteDesktop portal with `libei`, and the consent dialog blocks unattended runs without a cached `restore_token` | freedesktop portal docs, `libei` maintainer's write-up, tool issue trackers | High for the mechanism. That a CI environment can be provisioned with a token cleanly is explicitly **an open problem**, not a solved one. |
| `wlr-virtual-pointer-unstable-v1` and `wlr-screencopy-unstable-v1` bypass portal consent on wlroots compositors | Wayland protocol registry | High for the protocols' existence; whether a given compositor exposes them is per-compositor. |
| AT-SPI2 exposes a detailed GTK/Qt widget tree; sandboxed apps and custom renderers frequently do not implement it and are invisible | freedesktop AT-SPI2 documentation | High for the interface. "Frequently" is not quantified anywhere. |
| Xvfb proves the view layer renders without crashing, and does not prove compositor behaviour, hardware acceleration, or portal permission flows | tooling documentation plus reasoning | Medium, and partly inference — the inference is stated as such in `harness-lanes.md`. |
| jsdom places layout "outside the scope of jsdom" and returns "zeros for many layout-related properties" | jsdom's own README, fetched and read | High. Primary, from the project itself. |
| macOS: `SCFrameStatus` per frame; off-screen windows emit frames only under pointer movement; no supported way to composite an occluded window from outside it; a sandboxed app cannot use the accessibility API even with a user grant; no cross-process computed style | prior research corpus, Apple documentation and sample code | High for the documented parts. Two items remain open there and are flagged at the point of use: `SCStream` behaviour during **display sleep** has no authoritative source, and whether Secure Event Input degrades accessibility *reads* as distinct from event taps is untested. |

**Disagreement #4 — is SSIM the answer for native visual parity?** The
2026-08-19 run concludes that structural similarity "is the only mathematically
proven approach to measuring cross-platform geometry tolerances". The skill does
**not** adopt that, and the reason is evidence rather than preference. That
conclusion rests on a single hobby repository, not on a measurement. Against it
sits a directly relevant result from the earlier corpus: imperceptible
perturbations raised DISTS by up to 34.5%, LPIPS by 36.8%, VIF by 98.0% and
HaarPSI by 22.6% **while human opinion scores stayed flat or fell**, and every
metric tested was susceptible. SSIM and PSNR survived those particular attacks,
which is exactly what makes SSIM usable as a **tripwire** and still unfit as a
verdict — a threshold an implementation can be tuned toward without getting
better. So the skill keeps the quantised-geometry band it already had, and treats
a similarity score as a prompt to go and read the structure. `differential.md`.

**Withdrawn from the 2026-08-19 run.** One claim is dropped: that adjusting a
hosted Azure DevOps agent's resolution requires a specific marketplace task which
silently fails without interactive autologon. Its only citation 404s, and nothing
else in the report supports it. The *underlying* point — that a CI runner's
resolution is a campaign-relevant default — survives on the GitHub runner-images
issue instead.

**Promoted from the same run.** The UIPI silent-failure claim arrived as an
explicitly-marked inference whose only citation 404'd, which by the rule above
would have made it unusable. Fetching Microsoft's `SendInput` reference directly
found the vendor stating it outright, and more precisely than the report had.
Recorded here because it is the case that justifies chasing a dead citation
rather than deleting the claim attached to it.

---

## Withdrawn

Two figures appeared in one report and are **not used anywhere in this skill**.
Both cited a single secondary blog post as their only source, and that URL does
not resolve:

- "up to 75% of bugs missed by LLM-generated tests are missed because the inputs
  used are trivial"
- "34–62% of raw LLM-generated tests fail to compile outright"

Both are plausible and both may well be true. Neither is evidence at present. The
validity finding the skill *does* rely on is the 2024 unit-test study above,
which measured low validity directly and resolves.

A further set of URLs in the same report returned 404 only because a trailing
backtick from a markdown table was captured into the link. Those sources
(`arxiv.org/html/2608.03337v1`, `github.com/nalexn/ViewInspector`, and others)
are real; the citation formatting was broken, not the source. Recorded here so
nobody re-derives that conclusion from the raw checker output.

---

## Where each structural decision came from

The research above says what is true about UI testing. The other half of this
skill's design comes from running `acceptance-e2e`'s own method against a real
multi-day campaign and recording where it ran out — `docs/meta-pass-gap-analysis.md`
has each gap with its measurement. The trace:

| Gap measured | What closes it |
|---|---|
| The coverage denominator was prose; nothing gated it, and five of six screens were receiving no sweeps with nothing reporting it | `campaign.py check` — an exit code, not a feeling |
| A driving sweep wrote to a live tenant four times in one morning | write posture declared per pass; the refusal firewall in `sweeps.md` §C |
| Detector defects were rediscovered each engagement | `detector-defects.md`, and "prove the check can fail before trusting it passing" |
| The highest-value defect class had no name | `sweeps.md` §H, refusal honesty — the confident falsehood |
| Neither the review nor the suite compared the build to its design of record | `differential.md` as a phase |
| The deliverable was prose that rots | `evidence-page.py`, built from artifacts, with stable ids |
| Cross-platform was a paragraph per lane | `harness-lanes.md`, one capability matrix, plan to the lane's ceiling |
| Nothing proved the suite could fail | arming, counted separately and never summed with unarmed passes |
| Plan generation had no method | `coverage-model.md` |
| No component axis, so a shared-component defect was found once per page or never | `component` as an inventory kind and a page section |
| *(added by the requester)* nothing read what the project says it does | `project-comprehension.md`, and the requirement trace in the gate |
| A campaign reported 100% checked, 22 armed cases and 59 passing tests across two desktop apps, neither of which had ever drawn a window | `on-glass.md`; the `-glass` lane proof and the raster-artifact checks in `campaign.py`; the `visual` rung split; sweeps K and L |
| `visual` bought effect credit for a case asserting a title string, so the score rose while the coverage did not | `raster-visual` and `structural-visual` as separate rungs, with an evidence obligation on the first |
| A check that could not run and a check that passed arrived in the report identically | `inconclusive` and `blocked` as first-class blocking statuses, and observation coverage printed beside the verdict |

---

## Standing limits of the whole evidence base

Named plainly, because a campaign built on this should know where it is
extrapolating:

- **The quantitative evidence is Android-heavy.** GPTDroid, DroidAgent, VLM-Fuzz,
  GUITester, Monkey/Stoat/Sapienz — all Android. Substantial autonomous-testing
  benchmarks for React Native and SwiftUI/UIKit do not exist.
- **No direct study of LLM-generated *UI* tests.** The validity and duplication
  findings come from unit tests and from QA *plans*. The failure modes carry over
  in practice, and that carry-over is inference.
- **No reproducible cost data.** Published agent papers rarely report token
  usage, per-app spend, latency distributions or rate-limit effects. Any cost
  claim in this skill is measured locally or absent.
- **No longitudinal maintenance data.** How agent-generated flows age over six to
  twelve months of UI evolution is unmeasured. Related and measured: of 79
  documented reproducible bugs in one benchmark, only 9 still reproduced later,
  through selector drift, permission changes and dead services — which is why
  every flow versions its fixtures, accounts, permissions and environment
  alongside itself.
- **Two of the most load-bearing recent findings are unreplicated preprints** —
  the metamorphic coverage result and the no-strategy-dominates study. Both are
  used directionally and both are flagged at the point of use.
- **The desktop evidence is documentation, not measurement.** Everything in
  `harness-lanes.md`'s desktop matrix is an API contract, a vendor statement or an
  issue-tracker report: what the platform *can* do. None of it measures how often
  a given check catches a real defect, so sweeps K and L are justified by
  structure rather than by yield, and they say so. Specifically absent: any
  formal quantification of scaling-induced layout defects at particular DPI
  thresholds (searched for, and explicitly reported missing), and any
  vendor-independent flake data for agent-driven native desktop suites.
- **Nobody has published doing this.** Across all the material read, no first-hand
  account was found of anyone running a computer-use agent against an application
  as QA and reporting the results. The lane designs here are built from platform
  capability, not from somebody else's experience of using them this way.
