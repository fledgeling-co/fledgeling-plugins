# Does design-review actually work? The suite is written down and has not been run

**Nothing in this file is a measured result from design-review's own eval suite.** No
pass rates, no scores, no judge verdicts, no costs. No runner and no panel has been
pointed at `skills/design-review/evals/evals.json`, which holds **13 task evals and
98 checkable assertions**, or at `trigger-evals.json`, which holds **32 queries** for
tuning when the skill fires.

There is also no harness. The three sibling skills with graded suites in this
marketplace each ship a `run-evals.sh` beside their eval set; this plugin's `evals/`
directory holds the two JSON files and the fixtures and nothing that runs them.

One thing about this skill **has** been measured, in another skill's eval run, and the
next section separates that from everything else so a reader can tell which is which.
Below that is what was verified mechanically, including one eval whose assertions are
fully checkable without a browser and which passes all five of them.

## The one measured result, and exactly how far it reaches

`shipyard`'s eval suite was run on 2026-08-15 and graded, and one of its nine evals
puts this skill in the tested arm.

The eval is `conductor-design-gates` in `plugins/shipyard/evals/evals.json`. It asks a
model to lay out the stage sequence for a feature shipping on four platforms and to
specify what the design stage produces and what gates it must pass. One of its five
assertions reads:

> design-review and be-my-witness (or equivalently-named rendered-review gates) are
> named as gates on the mocks

The new arm passed it. From `plugins/shipyard/evals/records/grading-main.json`, the
grader's quoted evidence:

> "Two gates run on the rendered mock set ... 1. `design-review`, worklist-tracked per
> surface ... 2. `be-my-witness` on the same rendered set, dual-oracle"

The old arm failed the same assertion, and the grader's evidence for the failure is
the sharper half: in the predecessor, `be-my-witness` was absent and design-review was
*explicitly not a gate*. The new arm took that eval 5 of 5 and the old arm 4 of 5,
with this the only difference.

**What that establishes and what it does not.** It establishes that a pipeline skill
routes rendered-mock review to this skill by name, and that its predecessor did not.
That is evidence about shipyard's routing. It is not evidence that this skill's gates
are correct, that its findings are useful, or that it catches anything. No assertion in
that eval, or in any run eval anywhere in this repository, examines a review this skill
produced.

For completeness, the other places the name appears in committed eval material are all
unrun. `plugins/proctor/evals/evals.json` names design-review in three assertions about
routing aesthetic judgement away from a screenshot impression, and proctor's suite has
produced no result. `plugins/ship-feature/evals/evals.json` names it too, and that
skill's own EVALS.md opens by saying its suite has never been run.

## What the eval set actually holds

Thirteen evals, 98 assertions. Every assertion is a checkable property of the written
review, never a rating.

| Eval | Assertions | What it targets |
|---|---:|---|
| 0 `seeded-landing-page` | 24 | The flagship. A fixture seeded with Tier 1 gate failures plus contrast traps, where the 72px white hero heading **must not** be reported as failing: the previous build reported it at 1.0:1 because an unreadable background-image channel read as "no image" |
| 1 `no-browser-available` | 6 | No engine, so the review must say so rather than produce findings that read as measured |
| 2 `clean-surface-restraint` | 10 | A surface with nothing wrong. Padding it with invented nits is the failure |
| 3 `scoped-diff-review` | 4 | A review scoped to a diff stays scoped |
| 4 `imitation-material-rules-fire` | 5 | The faux-letterpress and faked-bevel rules fire on the defects and not on the honest ones |
| 5 `coverage-contract-multi-surface` | 6 | The denominator across several surfaces |
| 6 `worklist-gate-blocks-partial-report` | 6 | A partial review cannot report as a complete one |
| 7 `band-voids-and-unread-tokens` | 7 | A band rendering no ink, and a token declared and consumed by nothing, with a clean control beside it |
| 8 `implicit-grid-tracks` | 6 | A grid spilling an implicit row, with a clean control beside it |
| 9 `divider-gutter-and-clipping` | 6 | Ink crowding a rule, with a clean control, and clipped-text detection declared as a floor rather than a census |
| 10 `claims-must-trace-to-the-run` | 6 | Every number in the report traceable to what the run recorded |
| 11 `runner-completes-and-marks-the-ledger` | 5 | The runner finishes and the coverage ledger reflects it |
| 12 `a-blind-sub-check-must-not-read-as-clean` | 7 | **The adversarial case.** A sub-check that examined nothing must not serialise like a sub-check that found nothing |

Three of the thirteen ship a deliberately clean control beside the seeded fixture, and
the control is the more interesting half of each: a review that pads it with invented
nits has failed. Every one of those three also carries an assertion that the review
must *state* the control returned zero, as its own evidence that the probes
discriminate.

The trigger set is 32 queries, **15 that should fire the skill and 17 that should
not**, and its own note says why the negatives matter more: a description tuned only
on things that should trigger drifts wide and fires on every mention of CSS.

## What was checked by hand, on 2026-08-18

### Eval 4 passes, mechanically, all five assertions

Eval 4 is the only one of the thirteen whose assertions can be settled without a
browser and without a model, because it is entirely about what the source scanner
reports. Run against `evals/fixtures/imitation-material.css`:

| Eval 4's assertion | What the scanner printed |
|---|---|
| Reports `stacked-inset-bevel` with 2 hits | `stacked-inset-bevel`, 2 hits, at lines 12 and 19 |
| Reports `letterpress-text-shadow` with 3 hits | `letterpress-text-shadow`, 3 hits, at lines 24, 25 and 26 |
| Both at Tier 2, not as blocking gates | Both printed under the scanner's `TIER 2` heading, which it labels "findings (judged, need evidence)", and the run summary reads `0 gate hits · 5 findings · 0 prompts` |
| Neither rule reported against the layered `.card` shadow or the `.glass` inset highlight | Neither appears. `.card` is at line 31 and `.glass` at 37, and no finding names either |
| `letterpress-text-shadow` not reported against the blurred `.hero-caption` or `.overlay-text` | Neither appears. They are at lines 49 and 50 |

Five of five. The negative assertions are the ones worth having: the fixture
deliberately puts honest material effects beside the imitation ones, and a rule that
fired on both would pass a naive check and be useless in a review.

### The other checks

| Check | Result |
|---|---|
| `scripts/scan_source.py` on the pricing-page fixture repo | Fires as intended: `4 gate hits · 0 findings · 1 prompts`. It catches `outline: none` with no replacement at `pricing.css:24` and `role="button"` on a div at `PlanCards.tsx:19`, and it puts the round-number "Trusted by 10,000+ teams" claim in **Tier 3 prompts** rather than treating it as a gate, which is the tiering the skill's own severity rules ask for. |
| `scripts/scan_source.py` on the checkout fixture repo | Fires as intended: `4 gate hits · 10 findings · 0 prompts`, including `type="number"` on both a postcode and a card number, and the placeholder-only inputs. |
| Does the coverage gate fail closed | **Yes, demonstrated in both directions.** `worklist.py init` over two surfaces creates 2 by 8 equals 16 cells, all open. `worklist.py check` then **exits 1** and prints every open cell with the three ways to close it honestly (finish, mark `n/a` with a reason, or declare the stop). With all 16 marked done it **exits 0** and prints `Surfaces: 2 of 2 complete`. Reopen one cell and it **exits 1** again. |
| Is the source scanner a gate | **No, and it is worth stating.** `scan_source.py` exits 0 whether or not it reports gate hits: it is a reporter that feeds the review, and the gates in this plugin are the worklist ledger and `audit_run.py`. Reading its exit code as a verdict would be a mistake. |
| All seven scripts byte-compile | Passes: `analyze_styles.py`, `annotate.py`, `audit_run.py`, `run_review.py`, `scan_source.py`, `worklist.py`, and `probes.js` parses under `node --check`. |
| `skills/design-review/SKILL.md` frontmatter parses | Passes. `name: design-review` matches the directory and the plugin manifest. |
| SKILL.md against the 500-line conformance ceiling | Passes, at 395 lines. |
| Every `references/` and `scripts/` path named in SKILL.md resolves | Passes, all 22. |
| Everything the plugin claims to ship exists | Passes. Fourteen references, seven scripts, a `gemini.md`, ten fixture files plus two fixture repositories, four deep-research reports with their source lists. |
| The README's counts | Substantiated. "Thirteen task evals plus a 32-query trigger set" matches the files exactly, as does "three of them ship a deliberately clean control". |
| The README's incident claim | Traceable. The contrast probe that sampled 400ms into a 700ms entrance, read an `#E85A2A` accent as `#6a2d18`, and reported one surface going from 13 failures to 28 after a fix that provably removed them is written up in full in `references/gates-accessibility.md`. |
| Does the README claim any eval result | **No**, correctly. It describes the eval set and claims nothing from it, so there is no unsupported evidential sentence to correct. |
| Version agreement | Passes. `plugin.json` and `marketplace.json` both say 2.0.0. |
| Conformance | One failure that is not an evals failure: `assets/icon.png` is missing, which the repository gate reports separately. |
| Is there a runner | **No.** There is no script in `evals/` that executes the thirteen prompts, collects outputs, or writes a grading file. |

## What would settle it

Three runs, cheapest first.

1. **Write the runner, then run evals 4, 7, 8 and 9 against their committed
   fixtures.** These four are the cheapest real measurements available: every fixture
   is on disk, three of them ship a clean control, and the assertions are about numbers
   the probes print. Eval 4 already passes on the scanner half, so the work is the
   browser half. Grade with an independent agent that never sees the skill, one pass or
   fail per assertion with quoted evidence, into a `grading.json` beside the eval set.
   This is also what tells you whether the clean controls discriminate, which is the
   single most load-bearing property in the suite.
2. **Run eval 0 and eval 12 with the skill and with no skill.** There is no
   predecessor to compare against, so the honest baseline is the same prompt with
   nothing loaded. Eval 0 is the flagship, with 24 assertions and a fixture built to
   punish both error directions: it has real contrast failures to find and one white
   hero heading that must not be reported. Eval 12 is the adversarial case. If a
   no-skill arm passes an assertion in either, that assertion is measuring the model
   rather than the skill and gets rewritten or dropped with the change recorded.
3. **Run the 32-query trigger set.** It needs no fixtures and no browser: put each
   query to a fresh session and record whether the skill fired. The 17 negatives are the
   half that matters, because a description that fires on every mention of CSS costs
   every unrelated session context it does not need.

## Caveats, in advance of any run

- **A single run per arm carries sampling noise**, so the first grading will be a set
  of observations rather than a rate. That matters more here than in most suites,
  because a review is a long generated document and the assertions are properties of
  its prose.
- **A blind panel would score content only.** If one is ever run on this skill's
  reviews, the probes, the coverage ledger, the audit gate and the fixtures earn
  nothing there by design, and the reverse holds: judges preferring one review is not
  evidence that its measurements are right.
- **The engine bounds what any of it can claim.** The skill's own references record
  that the sanctioned browser accepts `Emulation.setEmulatedMedia` and does nothing,
  that shorthand computed styles read as `0px` while the longhands are correct, and
  that clipped-text detection under-reports. Eval 9 already carries an assertion that
  the clipped-text count must be declared a floor rather than a census, which is the
  right shape, and it means several of this skill's checks can only ever be reported as
  bounded rather than verified.
- **The one measured result is about routing, not quality.** It is reported above with
  that boundary drawn explicitly, because a reader who skims it would otherwise credit
  this skill with a result belonging to shipyard.
