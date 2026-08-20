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
twice: once at requirement time, and again before the campaign closes.

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

## Promoting a sweep

A sweep that found something becomes a permanent case with an id, a requirement
link and an oracle rung. A sweep that found nothing stays a sweep.

Findings route exactly like a red assertion: characterise, do not assert-correct.
`test.fail()` is not the tool — it passes on *any* failure, including the wrong
one. Write the case that describes the behaviour as it is, name the defect with
its own `DEF-*` id, and let the fix flip the case.
