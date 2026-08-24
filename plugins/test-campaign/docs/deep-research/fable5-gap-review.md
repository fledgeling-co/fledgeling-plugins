<!--
Provenance. Out-of-family referral panel run 2026-08-24 on the question
"what user-visible defect classes still escape the test-campaign methodology".
Not a Dossier panel: the Dossier MCP was not attached to the session that ran
this, so these are single-shot CLI lanes rather than a multi-backend research
loop with a source registry.

  lane   : claude -p
  model  : claude-fable-5
  effort : high
  prompt : docs/deep-research/gap-review-2026-08-24.prompt.md

Read the two together. They were run independently against the same prompt and
converge on the same first-ranked finding, which is the corroboration worth
having; where they disagree on a figure, the codex lane carries live citations and the
other flags its own numbers as recalled rather than looked up.
-->

🫥 The unifying gap: everything in the methodology quantifies over *states* — the coverage model, the sweeps, the reconciliation are all combinatorics over a static product. What still escapes is anything that exists only as a *history*: order, accumulation, interruption, elapsed time, and drift between builds. Below, ranked; the single highest-yield addition is differential journey replay against the last accepted build (§4).

## 1. Journey-only defect classes

**1a. Sequence-dependent state corruption.** Step 3 of a wizard derives state from step 1; the user goes back, changes step 1, and step 3's derived state is stale. No per-surface sweep reaches this because the defect *is* the ordering. Mechanism: model the journey as an explicit state machine and drive it with stateful property-based testing — postconditions per transition plus global invariants, in the QuickCheck state-machine / Hypothesis `RuleBasedStateMachine` style, or a graph-walker (GraphWalker) over the model. For sampling order systematically rather than randomly, use **sequence covering arrays** (Kuhn et al., NIST, "Combinatorial Methods for Event Sequence Testing", 2012) — the sequential analogue of the t-way sampling you already declare, and its natural extension: your coverage model gains an *event-order* dimension.

**1b. URL/history desync and deep-link re-entry.** The property to mechanise: **the URL is a serialization of app state**. For every reachable journey state, capture the URL, cold-load it in a fresh profile, and assert structural-hash equivalence with the original state. Separately, fuzz the history API: random back/forward interleavings mid-journey with an invariant checker (no orphaned state, no double-mounted views). This is cheap once journeys exist and catches a class (restored-tab, shared-link, bookmark) that per-surface enumeration never sees.

**1c. Interruption and crash-resume.** At each journey step, SIGKILL the renderer/process (or discard the tab), relaunch, and assert the outcome is either a clean resume or an explicit fresh start — never a hybrid. This is crash-consistency testing borrowed from file systems (the CrashMonkey/B3 shape): checkpoint, kill at every boundary, verify recovery invariants. Your sweep L does process chaos; the difference is *positioning the kill at journey-step boundaries and asserting journey-level recovery*, not process-level survival.

**1d. Partial completion against a server that already committed.** Server accepted step 2's write; client died before step 3. On re-entry: resumable, duplicated, or wedged? Mechanism: your sweep-B fault injection repositioned — inject the failure *after* each side-effecting journey step (not per-request) and assert idempotent re-entry, with the effect-witness rung counting server-side records to prove no duplicate.

**1e. Same-user cross-surface staleness.** Sweep G covers multi-user realtime; the more common defect is single-user: edit on surface A, and a memoized selector, SWR cache, or denormalised counter on surface B shows the old value. Mechanism: derive a **fact→projection map** from your requirement inventory (every entity → every site that renders it), mutate through one site, assert all projections. It's metamorphic in shape, but it needs the site map to have a denominator — which your closed-world machinery can supply. Include the two-tabs-same-user case (storage events, conflicting edits), which is neither G nor single-surface.

**1f. Aged-state sensitivity.** Everything passes on fresh fixtures; breaks at 100 items, page boundary 2, archived entities, an account created under last year's schema. Mechanism: seeded aged-account fixtures plus — the real omission — **upgrade-path testing**: create state under build N−1, boot build N over that persisted data, replay the journeys. Sweep K covers the shell; migrated-data journeys are a classic desktop/PWA escape.

## 2. LLM/vision oracles — where the evidence points

Where a model genuinely outperforms deterministic checks:

- **Semantic content correctness** — is the error message actually explaining this error; is generated text on-topic, coherent, in the right language and register. No deterministic oracle exists for this at all, so the comparison is against *nothing*, and a screening LLM judge is strictly additive.
- **Novel gestalt breakage** — overlap, truncation, garbled rendering *of kinds you didn't write a rule for*. Deterministic layout-fault detectors exist and are precise for the faults they model (ReDeCheck, Walsh & McMinn, for responsive-layout failures), but they're closed-world; a VLM screen catches the unmodelled residue. Deep-learning display-issue detectors (**Owl Eyes**, Liu et al., ASE 2020; Nighthawk, TSE 2022) reported precision/recall in the mid-80s — on curated datasets, which overstates field performance.
- **Post-translation layout at scale** — per-locale golden screenshots are unmaintainable; a VLM "is anything clipped/overflowing" pass over 30 locales is tractable.

Where the evidence says it does not outperform:

- **Geometry, alignment, counting, small-magnitude diffs.** "Vision Language Models Are Blind" (Rahmanzadehgervi et al., 2024) documents VLMs failing trivial acuity tasks — counting intersections, nested shapes. Your quantised-geometry and resolved-style checks beat a VLM decisively here; do not let a VLM rung substitute for them.
- **Precision as a pass/fail oracle.** LLM-as-judge for task success in web-agent benchmarks runs roughly 80–85% agreement with humans (the Online-Mind2Web/WebJudge line of work reported ~85%; I'm moderately confident of the figure, less of the exact paper split). That's a useful screen and an unacceptable gate.
- The distinction the literature supports crisply: LLMs as **input generators/explorers** have measured, real coverage gains (GPTDroid — Liu et al., ICSE 2023 — roughly 30% higher activity coverage than the best non-LLM baseline on Android; QTypist similarly for text-input generation). LLMs as **oracles** have a precision problem. Generate with the model; judge with something harder.

If you add an LLM rung: it slots *below* your effect rungs as a screening oracle, it must itself pass your ARM discipline (seed a real defect, watch the judge catch it), its flake rate gets measured like any assertion (k-sample self-consistency to control variance), and a fail routes to a human or a harder oracle, never straight to red.

## 3. Absent methods, rapid-fire

- **Differential journey replay vs previous build.** Run identical journey scripts on build N−1 and N; diff structurally and rasterly at each step; every unexplained diff must map to a change-log entry. The previous accepted build becomes an oracle for *all* behaviour, specified or not — McKeeman's differential-testing insight applied to your own history. Your placeholder-app incident, in its regression form, is a giant structural diff here.
- **Record-replay of real sessions.** Capture with rrweb (DOM-level), distill recurring real-user paths into journey scripts ("test carving"), replay in CI. Weights coverage by actual usage. Infra- and privacy-heavy; selection-biased toward paths that already work. Lower yield-per-effort than the others, but it's the only method that tells you *which* journeys matter.
- **Soak + leak-as-correctness.** Loop the journeys for hours; heap-snapshot diffing per iteration. Meta's **MemLab** is the concrete tool — scenario replay with automated retainer-trace analysis for detached DOM and listener leaks. Frame-time degradation over the soak is a correctness signal (jank = missed input), not just perf.
- **Async race fuzzing.** A response-shuffling proxy that permutes completion order of in-flight requests, plus injected latency variance on timers — then assert invariants (last-writer-correctness on stale responses, no double-submit; every submit control gets an idempotency assertion under double-actuation). Academic grounding: **EventRacer** (Raychev, Vechev & Sridharan, OOPSLA 2013) found harmful DOM event races on real sites; the class is real and essentially untested by anything in your sweeps, which actuate serially.
- **Clock/timezone matrix.** Playwright's Clock API (1.45+) or libfaketime: TZ ∈ {UTC, UTC+14, UTC−11, Asia/Kathmandu +5:45}, DST transition instants, Feb 29, midnight rollover *during* a journey, client/server skew. Very cheap, very reliable defect source (date off-by-one, "today" in the wrong zone).
- **Pseudo-localisation + RTL.** One pseudo-locale build (30–40% expansion, bracket markers, accented glyphs) swept with your existing geometry checks catches truncation, concatenation (split marker fragments), and hard-coded strings; one `dir=rtl` smoke over every surface catches mirroring. formatjs/i18next ship pseudoloc. Half a day of setup.
- **Offline/reconnect semantics.** Not request-failure injection (sweep B) but the *transition*: go offline mid-journey, act, reconnect; assert queued-mutation semantics, no loss, no duplicate on flush. CDP network conditions script it.
- **Mid-session revocation.** Token expiry while a form is open; role downgraded by an admin in another session; OS permission (camera, notifications) revoked mid-use. Assert fail-closed, no zombie UI over forbidden data. Sweep F is almost certainly static authz; this is the temporal half.
- **Telemetry correctness.** Journeys run through an intercepting collector (snowplow-micro, or a plain beacon proxy); assert event schema, sequence, and dedup against a registry. Analytics is a product surface with zero oracles in most shops, and decisions get made on its output. Your effect-witness rung is the natural home; it's absent as a sweep.
- **Screen-reader-driven a11y.** Rule engines find roughly 30–57% of issues depending on how you count (Deque's own study claims ~57% by volume; the GOV.UK tool audit found far less per tool). Beyond the engine: **Guidepup** scripts real VoiceOver/NVDA and asserts *spoken output* — announcement of live-region updates, focus-order-vs-visual-order, post-interaction announcements. That's behavioural a11y, unreachable from axe.
- **Monkey with invariants.** Random actuation over sequences (gremlins.js, or Android Monkey lineage) with global invariants: no crash, no console error, no永-spinner, no write from a read-only role. Cheap background harvest of sequence bugs your one-actuation sweep C can't see.
- **Undo/redo round-trip.** For every mutating action with an undo affordance: do → undo → assert structural-hash restoration. A one-line property over your existing control census.
- **IME and input-boundary events.** Composition events (CJK IME breaking controlled React inputs is a perennial), 10k-char paste, Unicode confusables, emoji. Sweep E stresses data shapes *from the server*; this is the input-method side.

## 4. The single highest-yield addition

**Differential journey replay against the last accepted build**, because of a compounding argument: it requires journey scripts — which §1 needs anyway — and once they exist, it converts *every behaviour of the previous build* into an oracle at zero specification cost, covering exactly the unspecified-behaviour residue that your requirement-driven machinery structurally cannot see (a requirement inventory can only defend requirements someone wrote down). It is also the only method on this page whose oracle strength *grows* with the product.

Cost: journey scripting (shared with §1, the dominant cost — call it days per product area); a two-build runner and structural/raster step-diff tooling (small, you have the capture provenance machinery already); and the real ongoing cost, **triaging intentional-change diffs**, which is bounded by requiring every diff to map to a change-log entry — an unmapped diff is a finding, a mapped one is a one-click accept that becomes the new baseline. Flake is the tax; your existing stabilisation discipline and armed/unarmed accounting transfer directly.

Runner-up on absolute yield (not per-effort): the §1a state-machine model with sequence covering arrays — deeper, catches novel defects rather than regressions, roughly 3–5× the effort.

## Ranked summary (expected yield ÷ effort)

| # | Addition | Yield driver | Effort |
|---|---|---|---|
| 1 | Differential journey replay vs last build | Oracle-for-free over all prior behaviour | Low once journeys exist |
| 2 | Clock/TZ/DST matrix | Dense, deterministic defect class | Very low |
| 3 | Pseudo-loc + RTL smoke | Whole i18n class from one build | Very low |
| 4 | Journey state machine + sequence covering + kill/re-entry injection (§1a–d) | The user-visible class nothing else reaches | Medium-high |
| 5 | Race fuzzing (response-order proxy, double-submit) | Real, currently-untested class | Medium |
| 6 | Fact→projection consistency + aged/upgrade fixtures (§1e–f) | Common field escapes | Medium |
| 7 | Offline/reconnect + mid-session revocation | Temporal halves of sweeps B and F | Medium |
| 8 | Telemetry sweep | Unwitnessed product surface | Low-medium |
| 9 | Soak + MemLab leak detection | Degradation-over-time class | Medium |
| 10 | Screen-reader-driven a11y (Guidepup) | The ~half axe can't see | Medium |
| 11 | LLM/VLM screening rung (armed, k-sampled) | Semantic content; unmodelled gestalt | Medium, ongoing flake tax |
| 12 | Monkey-with-invariants | Cheap sequence harvest | Low |
| 13 | Real-session record-replay | Usage-weighted coverage | High (infra, privacy) |

Where I'm least certain: the exact published FP/FN figures in §2 — Owl Eyes' mid-80s and WebJudge's ~85% are from memory of curated-benchmark numbers and I'd verify both before quoting them in an evidence page; field precision for VLM oracles will be worse. The Deque 57% figure is vendor-published. Everything in §1 and §3 I'd defend as-is: the techniques, tools and papers named there (sequence covering arrays, EventRacer, MemLab, ReDeCheck, GPTDroid, rrweb, Guidepup, Playwright Clock) are real and shippable.
