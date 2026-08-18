# Meta-pass — running `acceptance-e2e`'s own method on `acceptance-e2e`

The improve-skill pipeline asks for a meta-pass where the source skill's
methodology can be turned on itself. `acceptance-e2e`'s method is: enumerate the
acceptance criteria, map each to the evidence that verifies it, sweep for what no
criterion named, and promote every sweep to a gate.

Applied to the skill itself, its acceptance criteria are the claims its own
SKILL.md makes. This document is that matrix. **Every gap below was hit in a real
engagement**, not imagined: a multi-day campaign against the Diolog investor-portal
console, run to `acceptance-e2e`'s own instructions. Where a gap has a measurement,
the measurement is from that run.

---

## What the source skill gets right, and the successor must not lose

These are load-bearing and survive intact. Losing one would be a regression.

| Claim | Why it holds |
|---|---|
| **AC-first, never DOM-first** | "Driving coverage from the DOM ('I see a button, I'll test the button') instead of from the ACs" is its first named anti-pattern, and it is correct: DOM-driven coverage over-tests trivia and misses requirements. |
| **Assert the outcome, not the chrome** | "A chart renders" means the chart *draws geometry*, not that an element exists. This single rule is the difference between a suite and decoration. |
| **Green twice** | Flakes and isolation breaks only surface on run two. |
| **The proactive sweeps are where field defects live** | "A green AC run over an unswept feature certifies the happy path and nothing else." Measured true: the AC suite found nothing the sweeps did not. |
| **Guard promotion, with teeth** | "A gate the branch adds must be invoked by something" — a spec with no script, CI step or hook is documentation. |
| **Declare the axes you did not vary** | The 524-assertions-over-13-tenants example is the best single illustration of coverage theatre in any of these skills. |
| **Confirm at the API level before calling something a product bug** | Stops test artifacts being reported as defects. |

---

## Gap 1 — The coverage denominator is prose, and nothing gates it

`acceptance-e2e` makes the AC matrix "the suite's spine" and "the centerpiece", and
then leaves it as a markdown table. Nothing counts its rows, nothing fails when a
row is unfilled, and a partially-filled matrix renders identically to a complete
one.

`design-review` solved exactly this and the solution is mechanical:
`scripts/worklist.py check` exits non-zero while any cell is open, so *"the review
is finished" becomes a command's exit code rather than a feeling*. It also names
the failure precisely: **a partial review is formally indistinguishable from a
finished one** — same headings, same verdict line, and the reader cannot tell.

**Measured in the engagement.** The console's six screens were enumerated in prose
and five of them were receiving none of the eight sweep families. Nothing reported
that, because the sweep list was derived from a capture contract that deduped six
screens onto one route. A ledger with a denominator would have shown `1/6` on
sight.

**Successor requirement.** The coverage ledger is a file with a `check` command,
fixed before any capture, and every cell ends `done`, `n/a: <reason>` or `open`.
An unrecognised value counts as open.

---

## Gap 2 — Sweeps that drive the app can write to production, and nothing says so

`acceptance-e2e`'s interaction-integrity sweep enumerates every interactive element
and clicks it. Its isolation guidance covers *seeded data* ("mutating cases operate
on a disposable clone") but the sweep itself is not treated as a mutating case.

**Measured.** On a console whose controls are save buttons, that sweep placed a
section and set seven theme pairs on a live tenant record, four times in one
morning, because the development API writes to the production cluster. Nothing in
the skill anticipates that a *sweep* is a write.

The fix that keeps the check is not to skip write surfaces but to refuse the writes
locally: a control wired to a mutation still renders its refusal, so it still proves
it acted, while a control wired to nothing still reports dead. Two details are
load-bearing and both were found by measurement — non-GET is not "write" (the shell
posts to *read* chat statuses), and each refusal must be distinguishable or the
second write control on a screen reads as dead.

**Successor requirement.** Any driving pass declares its write posture, and a
write-bearing pass either runs against a disposable target or installs a refusal
firewall. Named as a phase precondition, not advice.

---

## Gap 3 — The detector defects are not catalogued, so each engagement rediscovers them

The skill catalogues *product* bug classes ("recurring real-bug classes") but not
*detector* defects — the ways a check reports a healthy app as broken or a broken
app as healthy.

**Measured, all four in one engagement:**

| Detector defect | Consequence |
|---|---|
| Dead-control check compared `document.body.innerHTML.length` | A working toggle that writes `aria-pressed="true"` on one control and `"false"` on another is **length-neutral**, so six working presets reported dead. |
| Region assumed to be `#main-content` | Surfaces that portal to `document.body` (a dialog) reported 0 characters while visibly rendering. |
| A predicate filtered on a field the probe never sets | Uniform zeros across every surface, forever. `design-review` names this and the defence: **print the denominator** (`examined=41 failures=0`), never the numerator alone. |
| Comparing a seeded mock against a live tenant | 137 "divergences", almost all of them the two fixtures holding different companies. |

**Successor requirement.** A `detector-defects` reference, and a standing rule:
**prove the check can fail before trusting it passing.**

---

## Gap 4 — No named vocabulary for the highest-value defect class it can find

The single most valuable class found in the engagement is not in the skill's
catalogue: **a refused write reported as a completed one.**

The mechanism is a client-library default — the browser GraphQL client resolves a
refusal instead of throwing, so every `try { await mutate() } catch {}` has a dead
catch and confirms work the server refused. Four instances were live in production
across three screens plus one card set that announced "Applied — on the record" the
moment it *stopped to ask* for a reason.

It is worth naming because of what it defeats: it is invisible to an
element-exists test, invisible to a screenshot, invisible to a visual judge, and
invisible to a green AC suite. Only a forced-refusal drive finds it.

**Successor requirement.** A first-class defect class — *the confident falsehood* —
with its detection mechanism (force the server to refuse, assert the screen says
so) promoted to a standard sweep rather than left to be rediscovered.

---

## Gap 5 — Visual is deferred entirely, and the deferral loses the differential

`acceptance-e2e` routes rendered judgment to `/design-review` and forbids judging
visual quality inside specs. Correct as far as it goes, and it leaves a hole:
**neither skill compares the build against its design-of-record on structure and
vocabulary.**

`design-review` judges a surface *on its own terms* (its own stage 9 admits this:
"a surface can be internally sound while being the wrong surface").
`mockup-fidelity` does compare against a mock, but is scoped to React/RN fidelity
rather than to a test campaign, and is not invoked by `acceptance-e2e` at all.

**Measured.** A vocabulary differential between the console and its design mock
produced 75 decided divergences, including a real capability gap — the design
offers placement at a position where the build offers one end-anchored add — that
every other layer was blind to, because each verifies the build against itself.

**Successor requirement.** The differential is a phase, and it is a *comparison of
what each screen names*, not a picture diff. The measurement traps are known and
must be carried: subtract shared chrome, template the tenant's own data out of
control names, serve fixtures for tables the live system leaves empty, and scope
interception to one endpoint.

---

## Gap 6 — No living artifact; the deliverable is prose that rots

The skill's deliverable is a test-plan markdown, spec files, and a report in the
reply. There is no single browsable surface where a person sees coverage, flows,
screenshots and components together, and nothing carries a stable identifier a
later conversation can point at.

The engagement had to build one from scratch (a storyboard page with a capture
contract, per-step screenshots, and an atom-level visual judge), and that artifact
is the one thing a non-author could actually read.

**Successor requirement.** A generated, self-contained evidence page is a
deliverable of the skill, built from artifacts on disk so it is regenerable and
diffable, with stable referenceable IDs throughout.

---

## Gap 7 — Cross-platform is prose, not a shared model

The "project-type lanes" section names macOS (proctor), iOS (Maestro), Windows and
MCP servers, but each lane is a paragraph. There is no shared artifact model, so
nothing lets a campaign report one coverage number across a web app and its native
siblings, and nothing states per lane **what can and cannot be observed**.

That last part is the expensive one. `proctor` is explicit that its iOS lane has
no accessibility tree, no elements, no geometry assertions and no tri-observer
check — *"a campaign that assumes parity with the macOS lane will spend itself
building a matrix it cannot run"*. `QA-PLAN.md` is explicit that SwiftUI has no
runtime style introspection, so the style layer must be triangulated rather than
read. Neither fact is reachable from `acceptance-e2e`.

**Successor requirement.** One capability matrix, per lane, stating what each
observation channel can establish — and a rule that a campaign plans to the lane's
ceiling rather than to the web lane's.

---

## Gap 8 — Nothing proves the suite itself can fail

The skill has an assertion-strength gate (a strong-model pass over the final suite,
asking whether each test asserts an outcome). That is a review, not a measurement.

**Measured.** Thirteen assertions in the engagement were armed by reverting the
behaviour each guarded and watching the test go red. Every one of the thirteen
passed that check — and it says nothing about the other 212, which is exactly the
honest limit to state.

**Successor requirement.** Arming is a named practice with a recorded count, and
the report distinguishes *armed* assertions from *unarmed* ones rather than
implying the suite bites uniformly.

---

## Gap 9 — Test-plan generation has no method

"Build the AC-traceability matrix FIRST" is the instruction; how to make that
matrix broad *and* deep is left to the model. The failure modes of a
model-generated plan — duplication, happy-path bias, asserting presence instead of
outcome, coverage theatre — are exactly what the skill warns about elsewhere but
does not engineer against at the point the plan is written.

**Successor requirement.** A stated coverage model with axes and a declared
sampling strategy, plus a depth manifest per surface so "match the density" is a
checkable count rather than a vibe. (This is the subject of the commissioned
research; the findings land in `coverage-model.md`.)

---

## Gap 10 — Component-level coverage is absent

`design-review` returns 40–90 distinct component types per screen and reports
coverage as a fraction of types opened. `acceptance-e2e` has no component axis at
all, so a defect that repeats across a shared component is either found once per
page or not at all.

**Successor requirement.** The component inventory is an enumerated axis, and the
evidence page carries a component atlas across every platform in scope.

---

## What this produces

Ten gaps, each with a measurement behind it. Every structural decision in the
successor skill traces to one of them, and the trace is recorded in
`references/evidence.md` alongside the research citations.
