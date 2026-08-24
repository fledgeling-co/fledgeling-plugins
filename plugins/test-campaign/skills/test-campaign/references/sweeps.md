# Sweeps — the checks no requirement asked for

A requirement suite proves the product does what was asked. The sweeps prove it
survives what nobody asked about, and that is where most field defects live.

Each sweep is **driven and asserted**, scaled to the feature, and recorded as
`ran` / `skipped: <reason>` / `inconclusive: <reason>` — never omitted. Each
prints its denominator (`examined=41 failures=0`), because a predicate that
matches nothing returns clean and looks exactly like a clean surface. And a sweep
the instrument could not actually perform is `inconclusive`, not clean: those two
are the same shape of green and only one of them is a measurement.

Scale: a copy change gets none. A new data surface gets A–E. Anything
collaborative, permissioned, or that writes on behalf of a user gets A–J. **K**
applies to anything with a real window on a real display server, and **L** to
anything that is more than one process — neither is optional on a desktop app,
and neither can run at all on a lane that never attached. **M** applies to any
product whose documents claim an effect outside its own process, and it runs
twice: once at requirement time, and again before the campaign closes. **N to U**
are the history axis and apply to any product with a multi-step task a user can
leave and return to: **N** models the journey, **O** interrupts it at every
durable boundary, **P** replays it against the previous build, **Q** varies its
event order, **R** changes the world underneath it, **S** checks what it reported
about itself, **T** runs it until something accumulates, and **U** varies the
schedule rather than the order.

---

## A · State matrix

Force each state rather than waiting for it: empty, loading, partial, populated,
over-full, error, refused, stale. Interception and seeded fixtures, not luck.

Assert the **honest** component in each: an empty state that says what to do
next, a loading state that is a skeleton rather than sample data, an error that
names the fix. Then assert **recovery** — that the surface returns to populated
when the condition clears, in the same session.

The highest-yield axis by a distance, and the one most surfaces have only ever
been seen on one value of.

---

## B · Fault injection

Forced 4xx, 5xx, aborts, delays, offline. Retry works. No infinite spinner. A
partial failure degrades rather than blanks. A double submit fires once.

The assertion that finds real defects: **after the failure, is the UI's claim
true?** See sweep H — most of what this sweep catches is really an honesty defect
wearing a network costume.

---

## C · Interaction integrity

Enumerate every enabled control on the surface, activate it, and assert an
observable effect. A control with no effect is dead; a control that reports
success without one is worse.

Four mechanics, all of them learned the expensive way:

**Detect change with a content hash, not a length.** Choosing an option writes
`aria-pressed="true"` on one control and `"false"` on another — length-neutral,
so six working presets reported dead on a page where everything worked.

```js
const sig = () => { const s = document.body.innerHTML + location.href;
  let h = 0; for (let i = 0; i < s.length; i++) h = (h * 31 + s.charCodeAt(i)) | 0;
  return `${s.length}:${h}`; };
```

**Resolve the region; never assume it.** When a visible `[role="dialog"]` is
present, that **is** the region. Surfaces that portal their content outside the
main landmark report zero characters while rendering perfectly.

**A sweep that drives is a sweep that writes.** On a surface whose controls are
save buttons, enumerate-and-click is a mutation storm — measured: four runs in
one morning each wrote to a live tenant, because the development API pointed at
the production cluster. Do not skip the surface; **refuse the writes locally**, so
a control wired to a mutation still renders its refusal and still proves it acted,
while a control wired to nothing still reports dead.

Two details in that firewall are load-bearing:

- **Non-GET is not "write".** An app shell that POSTs to *read* its statuses
  produced six console errors on surfaces nobody had touched. Scope the refusal
  to the endpoints this surface can write through, and detect a GraphQL mutation
  from the **document**, not the method. A body that will not parse is refused —
  fail closed.
- **Number every refusal.** One fixed sentence makes the second write control on
  a screen look dead: the first renders the message, the second renders the
  identical message, and the page is byte-for-byte unchanged.

**Overlay lifecycle**, in the same sweep: open, close, Escape, backdrop click,
focus trap, focus restored to the trigger.

### The control census, and the two shapes a signature check misses

Enumerating from the accessibility tree finds the controls that are *there*. Two
defects survive that and both were measured on one application on 24 Aug 2026,
under a campaign reporting 32 of 32 cases passing and armed:

**A control whose only observable is the product saying it worked.** A folder
picker opened a real `NSOpenPanel`, set a banner reading *"Opened Downloads"*,
and read nothing. The content hash moves, so a change detector records the
control as live. Name, per control, the state its handler is supposed to change —
rows in the list, files parsed, bytes on the pasteboard, the sheet presented, the
request fired — and read that instead. A toast is admissible beside one of those,
never as the whole of it.

**A shell whose every destination renders one view.** Six sidebar items, one
detail view. Select each in turn and read back an identity that must differ: the
root view's type name or accessibility identifier, the detail region's accessible
name, the document title. Comparing captures is the exact version, and between
two destinations of one menu identical bytes are the defect rather than a share.

Record what the sweep covered in the registry, so the next run has a denominator
rather than a memory: `controls` on the surface, `actuates` on the case,
`destinationOf` on each destination surface. `campaign.py check` then prints
`Controls: 11 of 18 declared control(s) actuated` on every run and refuses to
clear on a surface whose declared controls no passing effect-rung case actuates.
`references/inert-ui.md` carries the measurement and the four configurations it
refuses.

### On a native lane

The mechanics above are browser-shaped; the rule transfers and the instrument
does not.

- **macOS** — drive through `proctor` against a live attached window or menu
  extra. A headless `swift test` running `SwiftUI.ImageRenderer` has no window
  server and no event loop, and `Menu` and `NSPopUpButton` fail silently to
  render their real AppKit geometry, so it is not visual proof of anything.
- **Reading the AX tree is not enough on its own.** An identifier can sit on a
  row's label rather than on the control that owns the tap: measured, 13 sidebar
  identifiers all resolved while the element carrying one of them was an
  `AXStaticText` with an empty actions list. `name of every action of e` must
  contain `AXPress` for anything interactive.
- **iOS** — Maestro flows on the Simulator, deep-link-first via
  `xcrun simctl openurl`; the Simulator exposes no accessibility tree, so plan to
  that ceiling (`harness-lanes.md`).
- **Windows** — WinAppDriver or UI Automation; `SendInput` fails under UIPI
  without saying so.

---

## D · Keyboard and the accessibility floor

The primary journey, completed with the keyboard alone. Then an automated rule
engine (axe on web; the platform audit on native) reporting zero serious or
critical — **per surface and per forced state**, measured on a settled page.

The per-state part is what makes this sweep worth running: an empty state, an
error banner and an open sheet each introduce their own contrast and naming
defects, and none of them exists in the populated screenshot everyone checks.

Rule engines catch a minority of real accessibility barriers. A clean axe run is
a floor, and the report says so rather than calling the surface accessible.

---

## E · Data-shape stress

Re-run the surface over the seeded edge shapes: zero, one, large, long string,
unicode and emoji, null-optional, malformed. Seeded through the API as
predicates — "a record with a 200-character name", created if absent — never as
proper nouns.

Assert: no crash, no `NaN`, no raw enum or token leaking into rendered text,
truncation that ellipsises rather than overflows, a bounded DOM on a long list,
and no horizontal scroll on the document.

---

## F · Security surface

A forged privileged action is rejected **server-side**, not merely hidden in the
UI. An IDOR probe against a neighbouring identifier. Realtime channel
authorisation. A scan of DOM, console and URL for secrets. One injection payload
rendered inert end to end.

---

## G · Multi-user and realtime

Two authenticated contexts. Live cross-account reflection without a refresh,
presence, share and revoke, a permission change taking effect in an open session.

---

## H · Refusal honesty

**The sweep this file exists for.** Force the server to refuse — a validation
error, a permission denial, a conflict, a quarantine — and assert that the
interface **says so**. Not that it fails silently, and above all not that it
reports success.

This is a defect class, not an edge case, and it is nearly invisible to every
other sweep because the surface looks perfect. One measured mechanism: a GraphQL
client configured with `errorPolicy: 'all'` **resolves** an awaited mutation when
the response carries errors, so

```ts
try { await mutate(); toast('Saved') } catch { /* never runs */ }
```

confirms work the server refused. Four live instances of exactly this shipped to
production in one console. A fifth reported "Applied — on the record" the moment a
reason picker opened, with nothing written.

Four assertions, each of which has caught a real one:

1. The refusal **reaches the screen**, and it is the server's sentence — not a
   hardcoded local one that drops `refusals[0]`.
2. The optimistic state **rolls back** visibly.
3. The success affordance is **not** shown.
4. Timing is asserted where it matters: one console showed the refusal *count*
   immediately and the refusal *sentence* thirteen and a half seconds later,
   against a ten-second assertion budget — so the test read as "never shows"
   while the product read as "eventually admits it".

Where the project's own guardrails forbid fabricated data or fallback copy, those
are honesty requirements too: force the absent figure and assert the em-dash,
force the missing source and assert the refusal to claim one.

---

## I · Metamorphic relations

Where an absolute expected value is expensive or unavailable, assert a relation
between two runs. Component suites **execute** these behaviours far more often
than they check them — validated in under half of the cases measured — so the
relation is usually free coverage on a path already exercised.

Relations that transfer across most products:

| Relation | Form |
|---|---|
| Inverse | an action followed by its undo restores the prior state |
| Count tracking | the rendered row count equals the store's, after any filter |
| Permutation | a sort reorders without adding, dropping or altering rows |
| Idempotence | applying the same setting twice changes nothing the second time |
| Locale invariance | changing locale preserves every affordance and their order |
| Theme invariance | changing theme preserves structure and accessible names |
| Role monotonicity | a lesser role never sees more than a greater one |

Each is one assertion, holds across the whole data axis, and does not need a
fixture to know the right answer.

---

## J · Freshness and provenance

Assert that evidence is younger than what it describes. A capture older than the
implementation revision it claims to show is stale, and a page that renders it
without saying so is lying quietly.

Of 79 documented reproducible bugs in one benchmark, **9 still reproduced** later
— selector drift, changed permissions, dead services. So every flow versions its
fixtures, accounts, permissions and environment alongside itself, and the sweep
checks that those still resolve before trusting anything downstream of them.

---

## K · Desktop shell, window and display invariants

**Only runs on a lane that is actually on glass**, and that is the sweep's first
finding either way: a headless lane cannot run any of it, so a campaign that
reports K as clean without an attached process is reporting on nothing.
`references/on-glass.md` has the attachment proof this sweep depends on.

When the product has a window and the signed app is not on disk, build it
and attach before skipping K. `skipped: no -glass lane attached` is a result
only after that build was attempted, or after a structural block that
survived it (no interactive desktop, no signing identity). A skip because
the binary was never compiled is the paper-versus-glass failure again.

Unlike sweeps A–J, none of the checks below rests on a published measurement of
how often they catch something. They are here because each one is a defect class a
window has and a viewport does not, and each is cheap to force. Treat them as a
checklist earned by structure rather than by evidence, and do not report a yield
figure the skill does not have.

| Check | Force it by | Assert |
|---|---|---|
| **Display scaling** | 100% · 125% · 150% · 200% | no clipped text, no overlapping controls, no control pushed outside its window |
| **Window size limits** | drag below the stated minimum, and to full screen | the window refuses below a usable size rather than collapsing its layout |
| **Menu-bar extra / tray popover** | open it from the status item | the popover is anchored to *its own status item*, not centred on the screen |
| **Runtime theme change** | toggle the OS appearance **while the app runs** | whatever the framework guarantees, and no stale palette left behind |
| **Multi-monitor move** | drag between displays of different scale factors | layout re-resolves rather than staying at the old scale |
| **Occlusion and workspace change** | cover the window, send it to another Space or virtual desktop, lock the screen | the app survives it, and the *campaign* notices its capture channel has stopped delivering frames rather than recording the last good one again |

Two mechanics that decide whether this sweep measures anything:

**A theme toggle is not a repaint, and "without a relaunch" is not a universal
expectation.** Writing the OS appearance setting is not enough on Windows: a
running app only re-themes when the change is *broadcast* to it, and while the
shell and modern frameworks reload immediately, a classic Win32 app may not
subscribe at all and structurally requires a relaunch. So establish what the
framework under test guarantees, assert that, and record the rest as a platform
fact rather than a defect. Where the lane exposes no resolved colour to assert
against — which is every native lane — this check is `inconclusive`, not clean.

Two further traps: the tray icon of a crashed app **stays in the notification
area** until something forces the shell to invalidate it, so a stale icon is a
real defect class rather than a rendering artefact; and a display-scaling change
moves the coordinate space, so a harness that is not scaling-aware will click
where the control used to be and report the control dead.

**Occlusion is where the sweep and the instrument collide.** A compositor is
entitled to stop drawing a window nobody can see, and on macOS there is no
supported way to force it from outside the app. So a capture taken during
occlusion may be a stale frame rather than a current one. Read the per-frame
status and mark the cell `inconclusive` when it is anything but complete; a stale
frame recorded as evidence asserts the previous state of the application. On
Windows there is no per-frame status to read at all, so the same situation is
undetectable from the image and has to be avoided rather than measured: never
capture a minimised window or one on an inactive virtual desktop, because both
return black without erroring.

---

## L · Live process and IPC chaos

For any product that is more than one process — a daemon, a helper, a service, a
menu-bar app talking to a background worker. This sweep exists because the
integration seam is the one place unit tests on both halves can both pass while
the product does not work.

| Check | Force it by | Assert |
|---|---|---|
| **Peer disappears** | kill the daemon while the UI is open | the UI transitions to a named degraded state, promptly, without crashing — and *says* the peer is gone rather than showing stale data as current |
| **Peer returns** | restart it | the client re-establishes its connection and resumes, inside a stated bound, with no user action |
| **Half-open connection** | drop the socket without closing it | the client notices, rather than waiting on a read that will never return |
| **Privilege separation** | send a supervisor-level command from an unprivileged client | refused **on the peer side**, not merely hidden in the UI |
| **Startup order** | launch the UI first, with no peer running at all | the first-run path is the degraded path, not a crash or an indefinite spinner |

The assertion that matters most here is the one shared with sweep H: **after the
peer goes away, is the interface's claim still true?** A client that keeps
rendering the last telemetry it received, with no staleness marker, is not
degrading — it is reporting a machine state that no longer exists. That is a
refusal-honesty defect wearing a process costume, and it is invisible to a test
that only checks the app did not crash.

Write posture applies as it does in sweep C: killing a real daemon on a shared
machine affects whoever else is using it. Run against a disposable target, or
against your own instance, and say which.

---

## M · Reality boundary and vacuity

For any product whose documents claim an effect outside its own process — a
subprocess, a socket, a packet filter, a multicast announcement, a file written
where something else will read it. This sweep exists because a requirement
constraining an effect is an implication, and an implication whose antecedent
never fires is true. `references/effect-boundary.md` carries the doctrine; this is
the sweep.

Run it twice. Once in phase 1, when the requirement inventory exists and no test
does, because it is three greps and it can end the campaign's most expensive
misunderstanding in the first hour. Once again before closure, because by then the
product has changed and a passing requirement may have stopped being backed.

| Check | Force it by | Assert |
|---|---|---|
| **Census** | declare an `effect` class on every requirement whose text names one | every declared class has a provider in the production dependency graph and the reachable call graph |
| **Reachability** | walk from each shipped entry point, not from the tests | a `pub fn` nothing calls is not an implementation; name-based tools over-credit, so the error runs toward reporting more reachable |
| **Witness** | drive the effect from a production entry point with a recorder attached | a non-zero count of the declared class, with the recorder named |
| **Sabotage** | deny the effect and re-run | the scenario fails; if it still passes, the witness was circumstantial |
| **Strengthening** | replace a passing constraint with a strictly harder one | the case goes red; a strengthened constraint that still passes proves the check reads nothing |
| **Blind mutation** | for each test that calls a mutating verb, look after the last such call | a reader appears; a test that mutates and never reads again can only be asserting the call's own return value |

Denominators, in the shape the rest of this file already demands:

```
effect requirements: examined=14 provided=9 unprovided=5
witnesses:           examined=9  counted=7  zero=2
mutating verbs:      examined=7  changed=4  unchanged=2 unoracled=1
test fns:            examined=164 mutating=21 re-read-after=4 blind=17
```

Two of these cost nothing and want running first. **Blind mutation** is a `grep`
over the test tree and needs no privilege, no lane and no instrument; on one suite
it returned 17 of 21 and found a daemon verb that reported success while changing
nothing. **Census** is a dependency-graph read. Reach for a tracer after those
two, not before — the instrument is the reflex and it is usually the third-cheapest
detector on the list.

The write posture in sweep C applies with more force here. This sweep's whole
point is that real effects happen: a witness run spawns real processes, opens real
sockets and may install a real packet filter. Run it against a disposable host, or
run only the classes whose blast radius you have bounded, and say which. A sweep
that installs a firewall rule on a daily-driver is a worse outcome than an unrun
sweep.

---

## N · Journey and history

The one axis that is not a state. Everything above quantifies over a product
frozen at an instant; this sweep is about order, accumulation, interruption,
elapsed time, and the difference from the last accepted build.
`references/journeys.md` carries the model, the generators, the ranked additions
and the measured ceiling on model-based oracles; this is the sweep.

Run it where the product has a multi-step task somebody can leave and come back
to — a wizard, a checkout, an editor with drafts, anything with a pending queue.
Five to eight journeys of six to twelve transitions is the first increment both
referral lanes proposed.

| Check | Force it by | Assert |
|---|---|---|
| **Order** | generate legal action sequences over an explicit journey state machine, sampled with sequence covering arrays rather than at random | the invariants hold on every ordering, and a failing sequence shrinks to a reportable one |
| **Re-entry** | capture each journey state's URL, cold-load it in a fresh profile; interleave Back and Forward mid-journey | the same logical entity and revision is reconstructed, or a conflict is disclosed |
| **Interruption** | cut after each durable boundary — request issued, server committed, provider effect landed, client persisted, user acknowledged | every accepted intent is committed exactly once, visibly pending, or visibly failed; no orphan queue work survives quiescence |
| **Context** | switch account, tenant or role immediately before a consequential action | work started in context A cannot mutate context B |
| **Provenance** | seed fields with canaries encoding entity, tenant, writer and revision | two surfaces agree because they read one revision, not because they render similar text |
| **Differential** | replay the same sequence against build N and N−1 from equivalent snapshots | every semantic difference maps to an entry in an expiring change manifest; an unmapped difference is a finding |
| **Time** | freeze client, server and job-runner clocks separately; move the OS timezone independently | instants persist as instants, one execution across a repeated local hour, elapsed time never negative |

Denominators, in the shape the rest of this file demands:

```
journeys:      examined=6  modelled=6  generated-traces=180
boundaries:    examined=34 cut=34 recovered=32 orphaned=2
differential:  steps=214 diffs=11 mapped=9 unmapped=2
```

Two preconditions. **The differential half needs the previous build reachable**
from equivalent backend state, and where it is not, say so rather than comparing
against a snapshot taken under different data. And **the previous build is a
witness rather than the specification**: run the requirement and effect
invariants against both builds, so two versions agreeing on a violation still
fails.

---

## O · Journey prefix, interruption and process death

Rank 1 of the panel's ten, and the one it puts a mechanical gate on. Sweep B
injects a fault per request and sweep L kills a process; this cuts at each
**durable boundary of a journey step** and asserts recovery at journey level.

Boundaries, in order: request issued · server committed · provider effect landed
· client persisted · user acknowledged. At each, one of: kill the process,
rotate or resize, background then relaunch by deep link, drop the network, revoke
a permission.

| Check | Force it by | Assert |
|---|---|---|
| **Intent conservation** | cut after each boundary, relaunch, read the server | every accepted intent is committed exactly once, visibly pending, or visibly failed — never zero, never two |
| **No orphan work** | let the app settle after the relaunch | nothing remains queued that nobody will drain |
| **Draft survival** | enter text, cut before persist, relaunch | the entered value survives, or its loss is disclosed rather than silent |

```
boundaries:  examined=34 cut=34 recovered=32 orphaned=2
```

The evidence, with its limits stated. The Android data-loss benchmark holds **110
reproducible real faults across 54 releases of 48 apps**, every one with a
visible effect and 98 with an automated oracle. That establishes prevalence and
reproducibility — it is **not** a yield trial, and it does not say how often this
sweep finds a bug in a mature portfolio. TimeMachine, which preserves and
revisits deep states, is the stronger comparative result: 68 apps, five
repetitions, six-hour budget, **199 unique crashes against 140 / 121 / 48** for
Sapienz, Stoat and Monkey, and 281 against 183 on 37 industrial apps.

**Its limitation decides your design**: TimeMachine restored client state only,
not remote server state. So a client snapshot is never a complete oracle for a
partial commit — the effect ledger stays outside the restored snapshot.

---

## P · Previous-build differential

Rank 2, and the one to price the triage cost of before adopting.

Run the same journey against build N and N−1 from equivalent backend snapshots
and compare a normalised semantic state vector after every action.

**RegDroid is the measured case**: five apps, 121 adjacent-version pairs, 50
tests of 100 events each. It produced **205 reports — 73 true positives and 132
false positives, a 64% false-positive rate** — from which came **14 unique
functional bugs, ten previously unknown and all ten fixed by developers**, ten of
which no other assessed technique detected. **93% of the false positives were
intended feature changes.** The authors report under one hour of manual
inspection for all 205. No p-values or controlled person-hour comparison, a
deliberately simple resource-id oracle, Android-only.

That 64% is why every difference may not block. Three dispositions, and they are
the whole method:

1. **Mechanical fail** — a retained invariant, effect contract, accessibility
   invariant or security rule violated, or an undeclared removal.
2. **Mechanical accept** — the diff matches a machine-readable change-intent
   declaration naming the surface, the state and the allowed semantic delta.
3. **Triage** — everything else, clustered by duplicate and attributed to a code
   change.

```
differential: steps=214 diffs=11 invariant-violations=2 declared=7 triage=2
```

**The previous build is a candidate oracle, never an authority on whether the
behaviour should remain.** Where both builds violate an independent invariant,
agreement still fails.

---

## Q · Event order, adjacency and repetition

Rank 4. An ordinary covering array over `surface × state × viewport × …` does not
imply coverage of `A before B`, `B before A`, or `A … C … B`. Sequence covering
arrays do: strength *t* covers every ordering of every *t*-event subset as a
not-necessarily-contiguous subsequence. NIST reports **14 tests for all
three-event orderings of ten events, and 72 for all four-event** — against 10!
exhaustive. One operational eight-step system went from ~7,000 valid permutations
to a **19-case constrained suite**.

Declare it as its own dimension rather than another factor inside the existing
array, and gate the **coverage accounting** for two-event order on the critical
event alphabet.

Five blind spots, each needing its own generator, and this is why the sweep is
four checks rather than one:

- **Non-adjacency.** Covered events need not be adjacent, so `A` immediately
  followed by `B` is not guaranteed. Generate adjacent pairs separately.
- **No repetition.** Standard arrays use each event once, so `submit, submit`,
  `open, close, open` and every retry loop are uncovered. Generate them.
- **Unmodelled events are invisible.** The lock-screen study found bypasses
  involving hardware controls and cross-app actions absent from the developer's
  event model.
- **Relative order is not interleaving.** Scheduler order and delay need
  perturbation, not permutation.
- **Constraints reshape the suite**, so a prerequisite chain changes what is
  generated.

Yield evidence is thin and says so: a thesis classified **49 of 592 Android
vulnerability reports (7.9%) as event-sequence vulnerabilities**. No controlled
study has run factor-wise t-way and sequence arrays against one modern
web/iOS/macOS corpus and reported incremental unique defects per hour.

---

## U · Event races and schedule interleaving

Sweep Q varies relative *order*; this varies the *schedule*, and they are not the
same axis. Every sweep above actuates serially, so a stale response overwriting a
newer edit is invisible to all of them.

**AjaxRacer is the strongest yield result anywhere in this file.** Two phases:
compute the event graph by dynamic analysis, then generate tests that trigger
potentially conflicting event pairs under controlled schedules and compare the
outcomes. Across 20 widely-used web pages it generated **152 tests, of which 65
indicated harmful races across 12 pages, with 7 false positives**. That is
roughly 60% of pages carrying an observable race and over 40% of generated tests
finding a harmful one, at a false-positive rate low enough that triage is not the
cost. PredRacer extends the shape to Android with reported high precision and
recall, though its numbers and dataset size were not in the accessible excerpt.

| Check | Force it by | Assert |
|---|---|---|
| **Conflicting pairs** | permute the completion order of two in-flight requests | the outcome does not depend on which returned first, or the later write wins by revision rather than by arrival |
| **Stale response** | delay one response past a newer one for the same entity | the stale response is discarded, never rendered |
| **Double actuation** | fire the primary mutation twice inside the debounce | exactly one effect, counted at the server |
| **Retry against reconnect** | reconnect while a retry is queued | one effect, not two, and the queue drains empty |

```
races: pairs=152 harmful=65 false-positive=7 pages-affected=12/20
```

Gate it for critical flows. This is the one addition where the published
false-positive rate is low enough to block on directly rather than triage first.

---

## R · Mid-session revocation, offline, time and pseudo-locale

Rank 6, bundled because each is cheap and they share a shape: a state machine
whose transition happens *during* a journey rather than before it.

| Check | Force it by | Assert |
|---|---|---|
| **Permission revoked mid-use** | `simctl privacy … revoke`, `adb pm revoke`, or the browser permission API, with a surface open | fail closed, no zombie UI over forbidden data, and a route back |
| **Token or role change mid-session** | expire the token, downgrade the role from another session | the next privileged action is refused server-side, not merely hidden |
| **Offline transition** | go offline mid-journey, act, reconnect | queued-or-refused visibly; on flush, no loss and no duplicate |
| **Clock** | freeze client, server and job-runner separately; move the OS timezone | instants persist as instants, one execution across a repeated local hour, elapsed time never negative |
| **Pseudo-locale** | an accented, 30–40% expanded, bracketed build; then one `dir=rtl` pass | no clipping, no concatenation fragments, no un-externalised strings, mirroring correct |

Pseudo-localisation is the cheapest whole-class sweep on this page: one build
run through the geometry checks sweep C already has.

---

## S · Telemetry contract

Rank 9, and the surface most products have no oracle for at all while making
decisions on its output.

Put an independent collector between the client and the analytics endpoint. For
each UI intent, assert the event schema, count, order, consent state, identity
transition and dedup key; then reconcile collector against provider against
warehouse.

```
telemetry: intents=48 events-expected=61 observed=59 schema-violations=1 duplicates=2
```

Gate consent, purchase, onboarding and experiment events; the ground truth is a
versioned event schema, so this is deterministic and belongs on the
`effect-witness` rung rather than with a model.

---

## T · Resource slope and endurance

Rank 10, portfolio-dependent — higher for native desktop, media, realtime and
long-lived sessions.

Repeat a logically reversible create/edit/navigate/delete cycle while sampling
post-GC retained heap, DOM and listener counts, RSS, handles, storage size, queue
depth, latency and dropped frames.

**Compress the time rather than spending it.** Override the clock and suppress
network delay, and a core loop — open and close a modal, create and delete a row
— runs hundreds of times in a few minutes rather than hours. Plot DOM nodes and
listener counts before and after 500 iterations: **a slope that climbs linearly
rather than reaching a ceiling is a leak**, and that shape is the assertion.

**Gate on the post-warm-up slope or a changepoint against N−1, never on a
maximum** — a ceiling passes a leak that has not yet reached it. Advisory until
the variance is calibrated on your own product; then gate strong monotonic
growth. Twenty to thirty minutes catches gross leaks; multi-hour runs are nightly.

Frame-time degradation across the soak is a correctness signal rather than a
performance one: jank eats input, and a control that misses clicks is broken.

---

## Promoting a sweep

A sweep that found something becomes a permanent case with an id, a requirement
link and an oracle rung. A sweep that found nothing stays a sweep.

Findings route exactly like a red assertion: characterise, do not assert-correct.
`test.fail()` is not the tool — it passes on *any* failure, including the wrong
one. Write the case that describes the behaviour as it is, name the defect with
its own `DEF-*` id, and let the fix flip the case.

Two rules decide whether the promotion is real, both carried over from
`acceptance-e2e`'s guard-promotion phase:

- **Something has to invoke it.** A spec or checker with no `package.json`
  script, CI job or pre-push hook running it is documentation. Point at the line
  that runs it, or wire it in as part of the same change.
- **New surfaces inherit by enumeration.** Derive the promoted sweep's subject
  list from the router, the surface map or the manifest rather than from a
  hand-written list, so a surface added next month is covered without anybody
  remembering. A hand-list is the mechanism by which coverage decays without a
  single test being deleted.
