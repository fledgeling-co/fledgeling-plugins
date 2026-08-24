<!--
Provenance. Out-of-family referral panel run 2026-08-24 on the question
"what user-visible defect classes still escape the test-campaign methodology".
Not a Dossier panel: the Dossier MCP was not attached to the session that ran
this, so these are single-shot CLI lanes rather than a multi-backend research
loop with a source registry.

  lane   : codex exec
  model  : gpt-5.6-sol
  effort : high
  prompt : docs/deep-research/gap-review-2026-08-24.prompt.md

Read the two together. They were run independently against the same prompt and
converge on the same first-ranked finding, which is the corroboration worth
having; where they disagree on a figure, the codex lane carries live citations and the
other flags its own numbers as recalled rather than looked up.
-->

*Research receipt: two independent review frames produced 15 candidates, consolidated to 12 mechanisms. A paired-build, stateful journey protocol was the clear winner; systematic schedule exploration is valuable but should follow it.*

The largest remaining blind spot is longitudinal causality. The campaign proves many states and effects, but it does not yet require one user intent to remain correctly bound to the same entity, version, tenant and completion state throughout a changing history.

## Ranked omissions

Effort: S ≈ 1–3 engineer-days; M ≈ 1–2 weeks; L ≈ multi-week. These are rough implementation priors, not published cost measurements.

| Rank | Escaping user-visible defect | Concrete detection mechanism | Yield / effort |
|---|---|---|---|
| 1 | Lost drafts, duplicate effects, stale context after Back, incorrect deep-link target, resumed workflow attached to the wrong record, cross-surface disagreement | **Paired-build stateful journey protocol.** Model `route/history`, logical entity and revision, workflow progress, pending operations, client persistence and external-effect ledger. Generate and shrink legal UI action sequences with Playwright plus `fast-check`, Hypothesis state machines, or GraphWalker. Run each trace against N and N−1 from equivalent backend snapshots; compare a normalized semantic state vector after every action. Require intended differences to appear in an expiring change manifest, while applying independent requirements/effect invariants to both builds. [`fast-check` supports generated, scheduled and shrinkable model commands](https://fast-check.dev/docs/advanced/model-based-testing/); [Hypothesis generates chained stateful actions](https://hypothesis.readthedocs.io/en/latest/stateful.html). | **Very high / M; high confidence** |
| 2 | Partial completion and broken recovery when connectivity, permission or process state changes halfway through an operation | **Boundary-indexed recovery testing.** Insert a cut after each durable boundary: request issued, server commit, provider effect, client persistence and user acknowledgement. Exercise online→offline→online, granted→revoked, foreground→suspended/killed→deep-link relaunch. Assert: every accepted intent is committed exactly once, visibly pending, or visibly failed; no orphan queue work remains after quiescence. Playwright exposes offline and permission control; iOS Simulator supports `simctl privacy … revoke`; Android needs `adb pm revoke` or a test capability provider. [Playwright context controls](https://playwright.dev/docs/api/class-browsercontext), [Apple’s `simctl` examples](https://developer.apple.com/videos/play/wwdc2020/10647/?time=1080). | **High / S–M** |
| 3 | Truncation, broken RTL, untranslated strings, wrong plural, malformed numbers/currencies, concatenation that becomes ungrammatical | **Pseudo-localisation lane with semantic assertions.** Run accented, bounded, double-length, tall and RTL pseudolanguages; detect untranslated resource keys, clipped text, incorrect mirroring and string concatenation. Then add representative real locales covering Arabic/Hebrew, CJK, complex plurals and comma-decimal input. Xcode provides these pseudolanguages directly. [Apple pseudolanguage documentation](https://developer.apple.com/documentation/xcode/preparing-your-interface-for-localization). A declared `locale` axis alone does not provide these transformations or oracles. | **High / S** |
| 4 | DST fold/gap errors, early/late expiry, duplicate scheduled action, midnight rollover, wrong “today”, changing timezone while open, clock rollback | **Dual-clock temporal testing.** Inject wall and monotonic clocks separately; freeze client, server and job-runner time; change the OS timezone independently. Generate transitions around DST gaps/folds, leap day, month/year boundaries, session expiry and tzdata-version changes. Assert persistence as instants, one execution across repeated local time, non-negative elapsed time and stable ordering after timezone changes. Playwright Clock controls browser `Date`, timers and performance time, but not the backend or OS timezone. [Playwright Clock](https://playwright.dev/docs/clock). | **High / S–M for time-sensitive products** |
| 5 | A UI that passes axe yet is impossible or misleading through a screen reader, switch or zoomed workflow | **Assistive-technology task execution.** Complete critical journeys using actual VoiceOver, NVDA, TalkBack and Switch Control—without DOM-direct activation or coordinates. Record focus order, spoken transcript, live-region announcements, modal escape, return focus and final effect. Add release-milestone testing by disabled users. Deque’s own audit dataset found axe-core could automatically identify 57.38% of recorded issues by issue count, leaving 42.62% requiring other methods; that is vendor data, not a universal sensitivity estimate. [Deque coverage report](https://accessibility.deque.com/hubfs/Accessibility-Coverage-Report.pdf), [Android’s TalkBack and Switch Access procedure](https://developer.android.com/guide/topics/ui/accessibility/testing), [Apple’s warning that an automated audit does not guarantee accessibility](https://developer.apple.com/documentation/accessibility/performing-accessibility-audits-for-your-app). | **High / M** |
| 6 | A functionally correct control that becomes too slow to use, misses clicks during jank, hangs after repeated navigation, or is killed after memory growth | **Performance as a correctness oracle.** Attach latency, frame/hitch, memory and responsiveness budgets to the journeys in rank 1 and compare robust distributions with N−1. Use release builds on representative low-end hardware. XCTest supplies hitch, memory, launch and CPU metrics; Android Macrobenchmark supplies frame timing and Perfetto traces. [XCTest performance metrics](https://developer.apple.com/documentation/xctest/performance-tests), [Android Macrobenchmark](https://developer.android.com/topic/performance/benchmarking/macrobenchmark-overview). | **Medium–high / S–M** |
| 7 | Upgrade loses in-progress work, migration binds data to the wrong account, a migration runs twice, notification/deep link enters an old schema | **In-place upgrade matrix.** Install N−1, create drafts, queues, auth state and cached entities through the UI, replace it with N without clearing storage, then enter through launcher, deep link and notification. Assert migration idempotence by launching twice; test rollback if supported; inject one corrupt row and storage-full failure. This is distinct from ordinary fresh-install execution-plane coverage. | **Medium–high / M; product-dependent** |
| 8 | Analytics duplicates, missing events, wrong attribution, consent leakage, dashboards reporting success where no effect occurred | **Telemetry contract testing.** Put an independent collector between the client and analytics endpoint. Correlate each UI intent with expected event schema, count, order, consent state, identity transition and deduplication key; then reconcile collector, provider and warehouse counts. Snowplow Micro is designed for this style of automated event validation. [Snowplow Micro automated testing](https://docs.snowplow.io/docs/testing/snowplow-micro/automated-testing/). | **Medium / S–M** |
| 9 | Stale response overwrites a newer edit, cancellation loses to a queued commit, retry races with reconnect, account switching races autosave | **Systematic UI schedule exploration.** Gate promises/coroutines, timers, network completions, store commits and lifecycle callbacks. For a short critical journey segment, enumerate both legal orders of dependent event pairs under a two-preemption bound; use partial-order reduction and persist minimized schedules. Assert revision monotonicity, context confinement, truthful pending state and at-most-once external effect. This adapts CHESS-style deterministic schedule control; ordinary load or repeated execution is much weaker. [CHESS paper](https://www.usenix.org/event/osdi08/tech/full_papers/musuvathi/musuvathi_html/index.html). Android APEChecker found 51 confirmed async defects from 61 reports across 40 apps, substantially outperforming general explorers, but that rate should not be generalized beyond its subjects. [APEChecker study](https://arxiv.org/abs/1808.03178). | **Medium–high / M–L; highest for autosave/realtime/offline products** |
| 10 | Unimagined long-tail histories: repeated reversal, stale-tab return, unusual recovery loop, hesitation followed by double submission | **Production-trace mining, not literal replay.** Capture consented, source-masked semantic events: stable control identity, route, history operation, lifecycle transition, network outcome and state fingerprint. Build a directly-follows/process model, compare it with test transition coverage, and promote high-volume or failure-associated uncovered traces into synthetic-data tests. rrweb supplies collection and masking, but DOM replay is evidence, not deterministic re-execution; Sentry explicitly says reconstructed replay is not pixel-perfect. [rrweb recording and privacy controls](https://github.com/rrweb-io/rrweb/blob/main/guide.md), [Sentry replay limitations](https://www.sentry.help/en/articles/13964404-session-replay-faq-web). | **Medium / M–L** |
| 11 | Gradual listener, DOM, heap, descriptor, GPU-resource or queue accumulation; correctness collapses only after hours | **Resource-slope endurance.** Repeat a logically reversible create/edit/navigate/delete cycle while sampling post-GC retained heap, DOM/node and listener counts, RSS, handles, storage size, queue depth, latency and dropped frames. Gate on post-warm-up slope or changepoint against N−1, not merely a maximum. A 20–30 minute presubmit loop catches gross leaks; multi-hour runs belong nightly. | **Medium / L** |
| 12 | Correct mechanics but dangerous mode confusion: wrong tenant, environment, document version or edit/view mode at commitment | **Mode-confusion and interruption study.** Seed near-identical entities; switch account, tenant, version or permission immediately before a consequential action. Assert that the active context is visible at the decision point and the effect remains confined to it. For high-consequence workflows, add moderated interruption/resumption trials and measure wrong-object actions and false belief in completion. Automation can enforce context confinement; only users can establish whether the context cue is actually understood. | **Product-dependent / M–L** |

Two further inexpensive omissions are worth adding where relevant:

- IME and editing semantics: composition events, dead keys, dictation, paste, selection replacement, emoji/grapheme deletion, drag-and-drop and undo/redo. Ordinary `fill()` calls do not exercise these paths.
- Rolling-version and feature-flag skew: client N/N−1 × service N/N−1 × remote-config changes during an active journey. A homogeneous test deployment misses these.

If sweeps G or L already systematically insert faults at every durable journey boundary or enumerate callback schedules, ranks 2 or 9 should be demoted. Their names alone do not imply those stronger mechanisms.

## What the journey protocol should assert

The valuable model is not just a screen graph. Its state needs at least:

```text
context = tenant/account + entity identity + authoritative revision
workflow = unstarted | partial | pending | committed | failed | compensated
history = route stack + deep-link origin
client = cache + draft + pending queue + idempotency key
external = durable record + provider-effect ledger
```

Four high-value properties are:

1. **Intent conservation:** every accepted intent becomes exactly one committed effect, a visibly pending operation, or a visible terminal failure.
2. **Re-entry equivalence:** Back, Forward, deep link and fresh-process relaunch reconstruct the same logical entity and revision—or disclose a conflict.
3. **Context confinement:** work started in context A cannot mutate context B after navigation or identity switching.
4. **Cross-surface provenance:** values agree because they came from the same entity/version, not merely because two surfaces display the same plausible text. Seed fields with semantic canaries encoding entity, tenant, writer and revision.

The previous build is only a differential witness. If both versions violate an invariant, agreement must still fail.

## LLM and vision-model oracles

There is a genuine but narrow advantage in **open-set perceptual triage**: unexpected occlusion, blur, missing imagery, nonsensical composition or an ambiguity that nobody encoded as a predicate.

The best concrete public measurements I found are specialised learned detectors, not general-purpose LLM judges:

- **OwlEye:** 85% precision and 84% recall on its labelled Android screenshot corpus. That means about 15% false discoveries among its alerts and 16% misses among actual defects on that corpus. It does **not** imply a 15% false-positive rate among all clean screens; specificity and prevalence are not supplied. [OwlEye paper](https://arxiv.org/abs/2009.01417).
- **Nighthawk:** 84% precision/recall for screen-level detection, but only 0.59 AP and 0.60 AR for localization. [Nighthawk paper](https://arxiv.org/abs/2205.13945).
- **dVermin:** its specialised metamorphic comparison of normal and enlarged display scales reported 97% precision/recall at page level and 84%/91% at view localization. That is stronger evidence for a narrow, relation-specific detector than for an unconstrained vision-language judge. [dVermin paper](https://arxiv.org/abs/2212.04388).

Good model roles are therefore:

- rank and describe unexplained screenshot changes;
- find gestalt anomalies where no golden image exists;
- cluster visually or behaviorally similar failures;
- propose candidate ambiguity, hierarchy or copy problems for human review.

The evidence says models should **not** replace deterministic checks for routes, text, geometry, accessibility semantics, state, effect counts, telemetry schemas, timing or exact design conformance. Nor should they predict whether users will succeed: WiserUI-Bench used 300 real A/B-tested UI pairs and found current MLLMs close to random on selecting the behaviorally superior design. [WiserUI-Bench paper](https://aclanthology.org/2026.acl-long.2049.pdf). UICrit improved model-generated critique by 55% through targeted prompting, but still reports that automatic evaluation does not match human evaluators; it is not a calibrated defect classifier. [UICrit paper](https://arxiv.org/abs/2407.08850). Dynamic GUI understanding is weaker still without operation histories or carefully chosen keyframes. [GUI-World](https://openreview.net/forum?id=SkZRB75Q3H).

Operationally, use a model as a non-blocking alarm until it passes a blinded, product-specific corpus with frozen model/prompt, precision and recall confidence intervals, and random review of model-negative cases. A seeded positive suite alone cannot estimate false negatives.

## Highest-yield addition

Add the **paired-build stateful journey protocol** first.

It subsumes the exact gap exposed by the placeholder-navigation/empty-closure incident, but advances beyond it: the new failure target is a product that works at every isolated checkpoint yet corrupts the relationship between those checkpoints.

A realistic first increment is:

- five to eight consequential journeys;
- six to twelve model transitions each;
- interruption cuts after request, durable commit and client persistence;
- fixed smoke seeds on every PR, 100–500 generated traces nightly;
- semantic comparison with N−1 plus independent invariants;
- mutation operators for stale response acceptance, omitted persistence, duplicate retry, wrong-context callback and missing idempotency.

Rough cost: **one to two engineer-weeks** if backend reset, effect recording and lifecycle controls already exist; **three to six weeks** if those seams must be created. Afterward, adding a journey is commonly one to three days. That cost is higher than another sweep, but it creates the reusable substrate for offline/reconnect, interruption, migration, session-trace promotion and schedule testing—the reason it has the best expected defect yield per unit effort.
