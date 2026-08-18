# Sweeps — the checks no requirement asked for

A requirement suite proves the product does what was asked. The sweeps prove it
survives what nobody asked about, and that is where most field defects live.

Each sweep is **driven and asserted**, scaled to the feature, and recorded as
`ran` / `skipped: <reason>` — never omitted. Each prints its denominator
(`examined=41 failures=0`), because a predicate that matches nothing returns
clean and looks exactly like a clean surface.

Scale: a copy change gets none. A new data surface gets A–E. Anything
collaborative, permissioned, or that writes on behalf of a user gets all of them.

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

## Promoting a sweep

A sweep that found something becomes a permanent case with an id, a requirement
link and an oracle rung. A sweep that found nothing stays a sweep.

Findings route exactly like a red assertion: characterise, do not assert-correct.
`test.fail()` is not the tool — it passes on *any* failure, including the wrong
one. Write the case that describes the behaviour as it is, name the defect with
its own `DEF-*` id, and let the fix flip the case.
