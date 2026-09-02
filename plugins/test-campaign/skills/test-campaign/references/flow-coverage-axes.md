# Flow coverage — eight axes, and the two conditions that make one enforceable

Use this file when a campaign is asked to cover the journeys a user can take, and
somebody will read a coverage figure off it. It is the model behind
`schemas/coverage-axes.schema.json`; conform to that schema and a generic reader can
consume the result.

Everything here is measured on one campaign: a Next.js app taken from 52 journeys run
to a 925-journey catalogue over four days, ending 2026-09-02. Sources and quoted lines
are in `../../../docs/evidence-2026-09-02-ui-flow-campaign.md`.

## 1 · Why one percentage is the wrong answer

The owner's statement of the goal was one sentence: *"automated user flows for every
task that include screenshots of the steps in the flow, and then have an ai model
verify that nothing looks wrong in the model and have the automated user flows
programmatically check for the outcome that's expected."*

That is five conditions per journey, not one. A journey is finished when a spec names
it; that spec runs and is observed passing; a screenshot exists for each step; a
judge records that nothing looks wrong in that picture; and the programmatic assertion
checks the named outcome **and can fail a build**.

At the moment that campaign published its first figure, four of the five stood between
45% and 100% and the fifth stood at 2%. A single blended number reports the mean of
those and hides the 2%. So the rule is:

**Publish a denominator per axis. Never publish one combined percent.** The blend hides
whichever axis is weakest, and the weakest axis is the only one worth acting on. When a
reader is shown eight rows they read the low one, which is the behaviour the model is
for — the campaign's own reader did exactly that, quoting the 45.2% and the ~51-of-5,621
rows back and writing *"this seems very low considering our aim for 100% coverage."*

## 2 · The eight axes

Measured over 925 flows (292 p0, 451 p1, 182 p2) and 6,056 cases. `start` is the same
axis at the start of that day, kept because a delta is the only thing that shows a
campaign moving.

| # | axis | what it counts | end | start |
|---|---|---|---|---|
| 1 | `named_any_mention` | a spec file mentions the flow id anywhere, comment prose included | 925/925 | — |
| 2 | `bound_to_a_test_title` | a `test` or `describe` **title** carries the id | 889/925 | 689 |
| 3 | `ci_enforced_blocking` | in a CI step that can fail a build, and that step's filter selects it | 552/925 (p0 130/292) | 418 (p0 30) |
| 4 | `report_mode_only` | runs in CI and cannot fail a build | 185 | — |
| 5 | `in_no_ci_step` | never executed by CI at all | 188 (p0 45) | 293 |
| 6 | `distinct_recorded_passes` | a case id observed passing in a recorded run | 1,160 of 6,056 **cases** | 123 |
| 7 | `frames_captured` | a screenshot exists, filed under a flow | 3,217 frames over 593 flows | 0 |
| 8 | `surfaces_judged` | a judge verdict recorded against a frame | 75 of 593 | 3 |

Three properties travel with the table, and they are the load-bearing part:

- **Every axis is a lower bound on coverage and an upper bound on nothing.** The schema
  fixes `isFloor: true` so this cannot be dropped in transit.
- **Axis 1 is published beside axis 2, never instead of it.** 36 flows were named only in
  prose. A figure that absorbs `named` into `bound` reports imagination as coverage.
- **The axes count four populations against four denominators** — flows, p0 flows, cases,
  frames — so averaging any two destroys the only information they carry. 925 flows and
  6,056 cases are different things and the row says which.

## 3 · Four distinctions the axes rest on

**Named is a claim; bound is a binding.** A flow id in a comment is somebody asserting
coverage. A flow id in a test title ties a case to the journey. Only a binding can be
counted, screenshotted or promoted. Blending them over-reported by 18 cards in one lane,
and the same session recorded four separate occasions of counting prose as code — 12
`.auth/` hits in spec files that were all comments (true count zero), a
`blob\.example\.com` grep that matched an allow-list argument, and 9 of 244 `test.skip`
hits that were comment text. **Strip comments before counting anything.**

**Wired is not enforceable.** §4 has the mechanics; it is axis 3 and it is where the
arithmetic goes wrong.

**A park at the declaration is not a runtime guard.** `test.skip('title', fn)` never
runs. `test.skip(expression, reason)` inside a body is a guard that runs and decides.
They look identical in a title-reading count and mean opposite things: the first is lost
coverage, the second is a case declining a precondition it correctly checked. In that
campaign 200 cases were inert by construction (185 `test.fixme`, 15 `test.skip`, over 97
files) against 641 conditional skips working as intended. Banning `test.skip` outright
was floored on this: 52 legitimate runtime guards had just been built.

Runtime behaviour is worth establishing once rather than assuming: `test.fixme(title,
body)` skips before the body runs, verified by writing a marker file from inside the
body and observing `1 skipped` with the marker absent.

**A title is not a check.** Two shapes pass every title-reading instrument:

- a parked or live declaration whose **body has zero statements** once comments are
  stripped — 29 of the 97 inert cases were this, and the live variant is the worse one
  because a runner counts it as a pass;
- a case whose **body computes and asserts nothing** — a reader skimming the file sees a
  populated test, and no product change can make it fail.

A waiver is the third shape: an `existingCoverage` entry claiming `covered` and naming a
file whose only case is parked. Both halves read as fine in isolation; only following the
pointer shows the hole. 198 of 292 such waivers in that campaign pointed at a file where
no unparked case carried the journey, which is why the schema requires a non-empty
`specFiles` for `status: "covered"` and records the result of following the pointer in
`waiverAudit`.

## 4 · The two mechanical conditions for enforceability

A test is **enforced** only when both hold:

1. its file is in a **blocking** step's explicit file list, and
2. that same step passes a filter — a project, tag, suite or grep argument — that
   selects the file.

A **blocking** step is any CI unit whose non-zero exit fails the build. Generalise past
one CI product: a GitHub Actions step without `continue-on-error: true`, a GitLab job
without `allow_failure: true`, a Jenkins stage not wrapped in `catchError`, a shell
target in a chain that runs under `set -e`. A step that runs and cannot fail is axis 4,
not axis 3 — **a spec in report mode finds a defect only when a person opens the report.**

Both conditions are evaluated **per step**, and the file set a filter selects is its
**match pattern minus its ignore pattern**.

That one number was measured wrong four times in a single day, each reading plausible
and each published. What each mistake reported:

| mistake | what it reported |
|---|---|
| **Condition 2 alone — a matching project treated as proof CI runs it.** | A whole project's specs counted as enforced while `--project=spreadsheets` was never passed anywhere in the workflow file. |
| **Filters read as the union of two steps.** | Specs counted as enforced that no single step both listed and selected; the checker unioned both steps' `--project=` flags, so a file listed in step A and selected in step B passed. |
| **Match pattern read without ignore pattern.** | 24 files in the blocking step reported as running when they resolve to zero tests — the broad `tests/.*\.spec\.ts` match against an ignore list excluding nine directories. It inflated CI-enforced from 434 to 460. |
| **Steps located by line position rather than by name.** | `max()` over path lines landed on the last step in the file, so 15 demoted specs were filed under a 2-flag report-mode step instead of the 16-flag one, and were just as inert either way. **Find steps by name.** |

The published cost: one commit stated CI-enforced 460/925 and p0 57/292 when the true
figures were 434 and 55.

**A step name that states its own counts drifts silently.** One blocking step's name
claimed 515, then 532, 545, 589 and 601 while listing something else — four drifts in one
day. The fix that holds is a check comparing the claimed number against the parsed
workflow, and it fired on the very next edit after it was written.

## 5 · Two further model rules

**Weak oracles are found by reading, not by matching.** 63 flows whose bound case holds
only part of its oracle surfaced as a side effect of reading each oracle against its
assertions during the binding pass. The instrument built to find them by matcher name
returned 3 of 3 false positives, because the dominant idiom puts the literal in the
locator and a structural matcher on the end. Budget the reading pass; do not expect a
grep to replace it.

**Blocked is a third class.** A journey nobody could measure is not a pass and not a
failure. Record it with its lifting condition and its owner, and keep a belief that
turned out wrong visible rather than deleting it — that campaign's axes file still
carries `"secure_context": "CI runs on http://localhost:3100 which IS a secure context,
so this is NOT a blocker — recorded because it was wrongly believed to be one"`, which is
what stops the next lane re-deriving it.

## 6 · Sequencing

**Author no more flow specs while the current ones are not known to run.** This is the
single most transferable ordering rule from the campaign: axis 2 moved 200 in one day
while axis 6 sat at 2%, which is a growing catalogue of journeys nobody has watched pass.

And **run before wiring.** Five specs that looked like free coverage — already written,
just not in CI — returned 11 failed and 8 passed when run. Wiring them first would have
turned a green build red for eight reasons nobody had read.
