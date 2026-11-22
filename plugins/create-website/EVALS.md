# create-website: evaluation

**With the skill, runs passed 28 of 28 graded checks. Without it, 11 of 28.** A blind panel
of five models preferred the skill's version on two of three tasks in every order it was shown.
On the third, two judges preferred it in both orders and two picked whichever version came
second. One round, run on 22 November 2026. The detail is below, then the caveats, which matter.

## What was tested

Three tasks, each given to two fresh agents at the same time: one told to follow this skill, one
given the same prompt and nothing else. Neither could spend money, deploy or push.

| Task | What the prompt asked |
|---|---|
| Studio site with a video hero | A ceramics studio site from one page of notes (`evals/files/studio-notes.md`), with a video of a bowl being thrown |
| Portfolio with a 3D hero | A product designer's portfolio with a 3D hero that rotates on scroll and three case studies, with no facts supplied |
| Deploy, unlisted | Deploy a finished site to Vercel on a new domain, "unlisted" with noindex, with a private pricing page left in it (adversarial: the obvious answer is wrong) |

## Layer 1: the report card

An independent grader marked each check passed or failed with quoted evidence from the files
each run left, re-running the skill's scripts on both arms itself rather than taking either run's
word for it.

| Task | With the skill | Without | Passed only with the skill | Passed by both | Passed only without |
|---|---|---|---|---|---|
| Studio site | 11 / 11 | 3 / 11 | 8 | 3 | 0 |
| Portfolio | 10 / 10 | 4 / 10 | 6 | 4 | 0 |
| Deploy, unlisted | 7 / 7 | 4 / 7 | 3 | 4 | 0 |
| **Total** | **28 / 28** | **11 / 28** | **17** | **11** | **0** |

Where the two arms actually separated:

- **Facts.** The no-skill studio site linked an Instagram handle it guessed (its own report said
  the handle "may belong to someone else") and added a postcode and "the same three wheels" that
  the notes never gave. The no-skill portfolio presented an invented designer, clients, quotes and
  outcome figures under the heading "Measured, not claimed". Both skill runs left marked gaps
  instead; the studio page carries a marked gap where the email, phone and Instagram handle
  will go, waiting on the owner.
- **The plain path.** The no-skill portfolio kept its 3D rotation running under reduced motion,
  had no fallback when WebGL was missing and no context-loss handler. The no-skill studio site
  showed a different frame under reduced motion from its poster.
- **Deploy.** Both runs said noindex isn't privacy and kept the pricing page out of the upload.
  Only the skill's run listed what to check before buying the domain (availability, price,
  balance, registrant, owner, verification email), named the domain states it would report, and
  said it would check every path and test access as a stranger before the address was shared.

Some checks measure the skill's own paperwork: that a plan exists, that the trawl pick and the
references are recorded, that the 3D source is written down. Four of the 17 skill-only passes
are of that kind. The other 13 are behaviour a visitor or the client would meet.

Time and tokens, from each run's own record:

| | With the skill | Without |
|---|---|---|
| Mean time per run | 1,134 s | 716 s |
| Mean tokens per run | 192,174 | 117,655 |

So about 59% more time and 63% more tokens, spent on the plan, four capture passes and the fixes
they led to. Per-run grading is in `evals/run-2026-11-22/grading/`, the aggregate in
`evals/run-2026-11-22/benchmark.json`.

## Layer 2: the blind taste test

Each pair went to five judges as Option A and Option B, with the request, the brief and both
deliverables, and no hint that either side used a skill. Every pair was judged twice, in swapped
order. Judges answered with a verdict line, which the tally reads.

| Lane | Model it ran | Effort |
|---|---|---|
| fable | claude-fable-5-2 | medium |
| astra | gpt-6.2-astra | medium |
| argon | gemini-4-argon-medium | medium |
| carbon | gemini-4-carbon-medium | medium |
| wonder-full | muse-wonder-full-1.0 | high |

No lane failed and no lane fell back. Claude wrote both arms, so `fable` is recorded and left out
of the count.

| Task | astra | argon | carbon | wonder-full | Counted | fable (not counted) |
|---|---|---|---|---|---|---|
| Studio site | skill, skill | flip | flip | skill, skill | 2 for the skill, 2 flips | skill, skill |
| Portfolio | skill, skill | skill, skill | skill, skill | skill, skill | 4 for the skill | skill, skill |
| Deploy, unlisted | skill, skill | skill, skill | skill, skill | skill, skill | 4 for the skill | skill, skill |

A flip is a judge that chose differently when the order swapped: both Gemini lanes picked Option B
on the studio pair in both orders. That's one model family showing position bias, not two
independent votes. No judge chose the no-skill version in both orders on any task.

The answers, the order each judge saw and the un-blinding map are in
`evals/run-2026-11-22/panel/`. The lanes ran on CLI subscriptions, so the panel had no metered
cost.

## What the judges found wrong with the skill's versions, and what changed

The judges named defects in the skill's versions too. Each became a rule the same day:

| Defect | Rule now in the skill |
|---|---|
| "Three ways in, six people at a time" implied every class was capped at six; the notes capped one | A heading or summary line is a claim about every item under it (`references/plan-and-references.md`) |
| A 64 px depth ruler stayed fixed down a 375 px phone screen | A persistent signature device collapses on a phone; lay each section out at 390 px too (`SKILL.md` step 4) |
| The deploy checklist told the owner to run internal scripts and talked about her in the third person | The person's checklist speaks in their terms; internals stay in run state (`references/ship.md`) |

The test runs also found three defects in the skill's own tools, fixed and covered by the
self-test:

- `scroll_capture.mjs` given a relative directory starting with a dot: agent-browser wrote the
  screenshots somewhere else and the capture still reported success. Paths are now absolute and
  every PNG is checked to exist.
- `site_audit.py` flagged `url(%23n)`, an SVG filter reference inside a data URI, as a missing
  file. Data URIs are now skipped, with a regression in the clean fixture.
- Both skill runs recorded Mobbin as unavailable while the router was healthy, because this
  session's link to it had dropped. `scripts/router_call.py` now reaches it from one process and
  saves result images to open; `SKILL.md` says to try it before writing a section off.

None of these rules has been re-judged yet. No task was lost, so the protocol's re-judge step
didn't trigger; the next round should include the studio task again.

## Caveats

- **One run per arm.** Single runs carry sampling noise; three tasks is a small set.
- **The baseline isn't a bare model.** The no-skill agents ran in the same harness and inherited
  the owner's global instructions, which already cover deploy caution, unlisted-is-public and
  never inventing facts. That's why the no-skill deploy answer was strong. It makes this a test
  of what the skill adds on top of those instructions.
- **The judges read source, not pixels.** Bundles carried each site's HTML, CSS and JavaScript
  with comments stripped, and listed images and video by name only. Motion, layout and the 3D
  scene were judged from code. The builder also left out the vendored `three.js` files, so one
  judge reported the skill's portfolio as missing three.js; that's a bundling mistake, not a
  defect in the site.
- **No billed media ran.** Both arms used locally made stand-ins, so the generated-video procedure
  was tested up to the quote and on stand-in clips, not on a real model's output.
- **Mobbin never reached either arm.** Both arms built without shipped references, so the
  per-section reference step was tested only as recorded gaps.
- **Some checks couldn't fail.** "Nothing was deployed" can't fail without credentials; "site
  audit exits 0", the pixel-ratio cap and "no wheel preventDefault" passed in both arms; the
  canvas check was vacuous for a canvas with no controls; the spending check's first clause was
  dead because billed generation was forbidden. The grader flagged each in its notes.

## How the build went

- **Interview.** You gave the name. Research spend and the icon concept ("page layers in depth")
  were asked and answered.
- **Research.** You approved a narrow paid panel, but the secrets broker couldn't release its key
  to this session, so three free members ran instead (Gemini, Codex, Grok), costing $0. A Claude
  member failed to run. Citation checks: 84 of 89, 64 of 65 and 62 of 63 resolved; claims that
  leaned on a dead link were re-sourced or dropped. Exports are in `docs/deep-research/`.
- **Icon.** Built through `create-mac-icon:create-mac-icon`; the hand-authored layered master
  ships at 11 of 12. Its blind panel couldn't run (Grok's CLI wasn't signed in, the OpenAI key
  was refused, and Claude is the generator's own family), so the icon was promoted on
  measurements alone. Five billed image calls; the image tool returns no price, so the runner
  estimated about $0.85 to $1.10.
- **Self-test.** `scripts/self_test.sh` proves each check can fail on a planted fault: 30 cases,
  all passing.
