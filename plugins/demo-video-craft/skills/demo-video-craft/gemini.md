# demo-video-craft, calibrated for Gemini

**Applicability:** the older runs named below calibrate this file; they do not establish Gemini 3.8
limits. Preserve an implementation lane the user selected. Apply the route-out advice only to the
measured model or to a limitation observed in the current run. Take every count from the current
series' own files; the reference series' numbers below are worked examples, not quotas.

Read this in one pass before *Two quick exits*, then follow `SKILL.md` with these overrides; each
names the step it lands on. Most of this skill already suits this family: the binding numbers are
written as numbers, and five of its scripts end on a verdict line with a denominator
(`delivery: PASS 10/10`, `compare: PASS 10/10`). The overrides below cover what is still prose: the
categorical scopes, the four binding numbers no script reads back, and the skill calls whose output
nothing downstream opens.

## Epistemic status

`[docs]` is Google's guidance quoted verbatim, the stronger tier. `[measured-family]` is Gemini runs
that were **not** this skill: two recorded sessions (a two-platform UI mock, a research-and-authoring
pipeline) and 106 benchmark tasks scored against `claude-opus-5`, all on `gemini-3.7-flash` (one
session at `3.7-flash-high`). None of those rates carries to the Pro tier or to 3.8, where these
overrides stand as `[docs]`-grounded discipline. `[derived]` is reasoning from the two. Facts about
the series this skill was built from come from its own `references/evidence.md`; that run was a
Claude session, so they show what the gates catch, not how Gemini behaves.

On `thinking_level`: **[docs]** `HIGH` is described as *"suitable for complex prompts requiring deep
reasoning, such as multi-step planning, verified code generation, or advanced function calling
scenarios"*, which fits planning a series. It is not a fix for anything below: paired across the 106
tasks, `high` beat `medium` on 24, lost on 24 and tied on 58.

**Unmeasured on this skill.** No Gemini run of `demo-video-craft:demo-video-craft` has been
recorded, so nothing here was observed on a series this skill built. The reference-input lever
(step 2) is `[docs]` only. Rounds (step 9) have no comparable shape in the corpus. **There is no
evidence that this file helps**: no run has compared the same work with and without it. **[docs]**
A side file is the shape the checklist warns about under **Conflicting internal references**:
*"Avoid writing a prompt with non-linear logic or conditionals that require the model to piece
together fragmented instructions from multiple different places in the prompt."* That is why this
file is read once, whole, before the procedure.

## Route out before you build

**[docs]** Under **Task outside of model capabilities**: *"Avoid using prompts that ask the model to
perform a task for which it has a known, fundamental limitation."* **[measured-family]** On benchmark
`diolog-2.0` the gap is not uniform, so the shape decides:

| shape | the work in this skill it describes | gem | opus |
|---|---|--:|--:|
| `visual-design` | step 4's judgement of a contact sheet, the lockup and the end slide | 35 | 63 |
| `regression-sensitive` | step 9: answer one note and every other film still gates as before | 42 | 65 |
| `brownfield-integration` | changing the engine in a series' `_kit/` fork, several files at once | 24 | 50 |

```bash
python3 <defer>/skills/defer/scripts/lane_pick.py --task implementation --shape regression-sensitive
```

**Omitted deliberately.** `static-page`: `build_site.py` writes the video pages from `site.json`,
and hand-written pages route to `design-craft:design-craft`, which has its own `gemini.md`. The
level shapes (`greenfield-module`, `algorithmic`, `accessibility`, `react-ui`) would route away work
done as well. Where the work stays anyway, the rows above say which output to distrust first.

## The quota ledger (steps 2, 4, 6, 7 and 9)

**[measured-family]** A recorded run delivered every requirement its brief *enumerated* (twelve named
features, all present) and one instance of each it named *categorically*: `all states` → 1,
`all menus` → 0, `all flows` → 0. **[docs]** Under **Ambiguity**: *"Avoid using subjective or
relative qualifiers that lack a concrete, measurable definition. Instead, provide objective
constraints (for example, "write a summary of 3 sentences or less" instead of "write a brief
summary")."*

This skill's categorical scopes, with the number each takes. The scan flagged 15 candidates: three
are the states and page-build rows below, two are figures and belong to the real-company section,
and ten are prose (`Every check that ran passed`, `read by every step`) and are dropped. The other
seven rows come from reading the procedure, where the scope is a film or a step, not a quantifier:

| Step | The skill says | The number comes from |
|---|---|---|
| 2 | the film table | `python3 films.py`: films listed |
| 4 | open `states/index.html` before building a scene | states in `states.py` |
| 4 | `hf.sh snapshot --at <every step boundary>` | step boundaries per film, summed |
| 4 | one line per workflow in `REVIEW.md` | workflows shown, one per short |
| 4 | every defect a sheet shows, under "Weakest shots" | sheets opened = films |
| 6 | read `sync_table.py films/<id>` for every film | films |
| 7 | `site_urls.py check` after every page build | page builds this round |
| 7 | when the picture changes, regenerate every poster and the share image (`site.md` §4) | films + 1 |
| 9 | search the series for a note's exact string | 5 surfaces: scripts, voice input, pages, posters, share image |

Write the ledger into `REVIEW.md` before step 4 and fill each cell from the run, real or
`n/a: <reason>`. Shown with the reference series' denominators (`kit/reference/`), as a complete run
reports them:

```
films      10 of 10 in the table      states   36 of 36 opened on states/index.html
sheets     10 of 10 opened            sync     10 of 10 tables read beside the picture
posters    10 of 10 + share image     lines    18 of 18 generated (gateway_audio.py, 2,566 chars)
note sweep 5 of 5 surfaces grepped    workflows 9 of 9 with a REVIEW.md line
```

## The bound ledger (*The numbers that bind*)

**[measured-family]** The benchmark's UI assertions, classified by whether each states a **bound**
(`exactly N`, `no`, `only`) or asks for a **thing**: Gemini's failures were 58% bound-shaped at
`medium` and 86% at `high`, against 8% for opus. One rule, `has exactly one soft elevation shadow`,
failed on every card in its set on a run that passed 37 of its 39 other assertions. The failure is a
default idiom supplying the value underneath a rule that was read and agreed with.

**[docs]** Google names constraints as a component, *"Restrictions on what the model must adhere to
when generating a response, including what the model can and can't do."*, and places a **Recap** of
them at the end: *"Concise repeat of the key points of the prompt, especially the constraints and
response format, at the end of the prompt."* The last section of this file is that recap.

Each binding number becomes a row per instance, read off the produced file. Most already have a
script; four have none, and those are the rows to fill by hand:

| Bound | Readback |
|---|---|
| overview 80-110 s, shorts 20-25 s | `python3 films.py` (the length gate; an override needs `why`) |
| a line ≤ 0.1 s past its scene, the last ≥ 0.6 s before the end | `build.py` narration gates |
| nothing still past 4 s, except a closing push from `settle_push` | `pop_scan.py <film> --json` → `still_runs` |
| -14 LUFS ±0.5, true peak ≤ -1 dBTP, one picture per film | `delivery.py check` |
| a 9:16 fact inside x 120-780, y 290-1250 | `hf.sh check` safe-zone warnings, each named |
| **overview ≤ 130 spoken words; a short's line 24-35** | **none**: count `lines.json` per film |
| **interface text the viewer reads ≥ 28 px at 1080p** | **none**: computed `fontSize` × the camera's scale at that time |
| **lockup and the text beside it share a baseline within 1 px** | **none**: measured inside the text (`picture.md` §7) |
| **end slide: mark held still 3-5 s** | **none**: the stage's last `in` to the film's end, from `films.py` |

A filled row set, from the source run's own record. The two `no` rows are real defects it shipped
and later fixed, which is what a row is for:

| instance | bound | readback | observed | within? |
|---|---|---|---|---|
| overview | 80-110 s | `films.py` | 101 s | yes |
| K07 voiced | ≤ -1 dBTP | `delivery.py check` | above the ceiling before `limit` 0.6; -3.6 after | **no**, then yes |
| `/features` header | baseline ≤ 1 px | measured in the text | 6.7 px | **no** |
| K02-K10 lockup bar | centred, baseline ≤ 1 px | snapshot at the bar + measured | off centre and off baseline on all nine | **no** |

Report `N of N instances within bound` per row in `REVIEW.md`. Three of the skill's prohibitions are
bounds in disguise, converted here: *never text partway through typing in* at frame 0 becomes
`snapshot --at 0` read for a complete line; *never on a card that repeats the headline* becomes the
last frame's text compared with the headline string; *no scene runs past 25 s* becomes the longest
scene in `films.py` output.

## Gates: paste the output, prove it can fail (steps 4, 6 and 7)

Every number in `REVIEW.md` or the report carries the command and its verdict line. A denominator of
zero is a gate that never ran: `delivery: PASS 0/0` over an empty `staging/` is a failure to render,
not a pass. **[docs]** *"Include specific verification steps in either the system instructions or
your prompts directly."*

Three checks in this skill's own history matched nothing while looking healthy, all caught by a
fixture rather than by re-reading:

- the voiced-cut check compared bytes, which always differ across encoders, so a voiced cut with no
  narration in it passed; it now compares momentary loudness (`delivery.py --self-test`, 9 cases);
- the step parser ignored `data-items`, so a scene reported `arrive 0 … 0 thread items` and ran
  empty; uniform zeros across varied films are the signature;
- a gate read through `| tail` reported tail's exit code. Read `echo rc=$?` on its own line.

Run each script's `--self-test` once per session before trusting its pass, or
`evals/run_mechanical.sh` for all nine. **Passive is not active:** `films.py` exiting 0 proves the
table is well formed, and `hf.sh check` with 0 errors proves the project lints; neither is a render.
`compare_films.py` against the previous published files is the readback for step 9: a note asked
for one film to change, and the others should hold at SSIM ≥ 0.98 (the reference rebuild held
0.9994-0.9998).

**A prerequisite check before step 6.** `render.py` does not look for `REVIEW.md`. Before rendering,
confirm the file exists and holds the quota ledger, the bound ledger, one line per workflow and a
"Weakest shots" entry per film (a defect with its time, or `none, sheet <path> opened`). If any is
missing, the render waits.

## Skill calls leave a file the next step reads (steps 1-8)

**[docs]** *"Chain prompts: For complex tasks that involve multiple sequential steps, make each step
a prompt and chain the prompts together in a sequence. In this sequential chain of prompts, the
output of one prompt in the sequence becomes the input of the next prompt."* **[measured-family]**
On one recorded run two prescribed skill calls were skipped because nothing downstream needed a
file only they produced. So each call here is discharged by the Skill tool call and the file it
leaves, never by output that merely follows the skill's rules:

| Step | Skill call | Leaves | Read by |
|---|---|---|---|
| 1 | `clarify:clarify` (before any question) | the answer, noted in `BRIEF.md` | step 2 |
| 2 | `motion-craft:motion-craft` | its base directory → `MOTION_CRAFT_SCRIPTS`; three storylines in `SERIES.md` | `render.py`, `hf.sh` |
| 3 | the brand's voice skill | `lines.json`, `respell.json`, `site.json` copy | steps 5 and 7 |
| 4 | `design-craft:design-craft` | `lockup.css`, the end slide's scene | every film, every page |
| 4 | `ux-craft:ux-craft` | one `REVIEW.md` line per workflow | the prerequisite check above |
| 7 | `design-review:design-review` | its findings, each with a disposition | the deploy |
| 8 | `status-update:status-update` | `.status/project.json`, `STATUS.html` | the reply |

Take `MOTION_CRAFT_SCRIPTS` from the base directory the loaded skill reports, not from memory, and
keep a receipt column (`Skill call, turn N`) beside the table.

## The contact sheet: describe before judging (step 4)

**[docs]** *"Ask the model to describe the images before performing the task in the prompt."* And:
*"To improve the response, point out which parts of the image are most relevant to the prompt."*

Open every sheet (films × step boundaries, counted in the ledger). For each frame, write what is in
it, then judge it against `picture.md` §9: the step, the visible text with its size, where the
cursor and marks sit, and whether the lockup bar is up. Then ask what is wrong with it. The shape of
an entry (the time and sizes here are illustrative, not measured):

```
K04 @ 14.2 s  step: panel.  Seen: side panel open on the filing card, cursor on "Apply", ev-ok
              underline on the revenue figure; body text measures 22 px after the 1.4x push.
              Defect: below 28 px. Fix: frame the panel at 0.7 of the width, not 0.62.
```

**[docs]** The launch post claims *"For UI generation, the model shows high design adherence and
parity based on a reference input, whether it's a screenshot, an image, or a full design system."*
This skill ships one: the reference series. Open `kit/reference/` and its states page before
building a new series' first scene, and match its frame sizes and holds unless `SERIES.md` says why
not. Unmeasured on this corpus with or without the reference.

## A real company on screen (step 1, `brief-and-claims.md` §4b)

The skill already says it: *Invent nothing about a real company.* For every figure, date and holder
on a screen or a page, adopt Google's strictly grounded instruction with `SOURCES.md` as the context.
**[docs]** Its last clause: *"If the exact answer is not explicitly written in the context, you must
state that the information is not available."* A figure missing from `SOURCES.md` is left off the
screen, not estimated. A ratio you computed from two filed figures is your claim; label it as one in
`SOURCES.md`. The screen builder's banned-name check (`assert_clean`) reads names, not figures.

## Retries and spending (steps 5 and 7)

**[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same
failed call."* Two attempts per tool, then change approach; a permanent error (`command not found`,
an unknown flag) gets one. Two cases specific to this skill:

- **A paid call is never retried blind.** `gateway_audio.py` spends on every attempt. On a failure,
  re-run `--dry-run`, show the user the cost again, and wait.
- **A transient one is retried on a clock.** `site.md` §8 names one: Vercel's `temporarily
  throttled`, retried after 90 s.

## Recall is not a source

HyperFrames flags, GSAP easing names, `hf.sh` options and the Vercel CLI version come from the loaded
skill and `--help`. A file this skill names is opened before the step it governs, in its own call.

## Recap: the delivery note

The report (step 8) carries each line with its command. Filled from the source series' last round
(render, names, site) and the reference rebuild (compare):

```
films       10 of 10 rendered          render.py → delivery: PASS 10/10
names       every published.txt name   delivery.py check --published published.txt → rc=0
compare     10 of 10 at SSIM ≥ 0.98    compare_films.py → compare: PASS 10/10, lowest 0.9985
site urls   70 of 70 fresh             site_urls.py check site → rc=0
bounds      word counts, text size, baseline, end hold: N of N each, read by hand (see REVIEW.md)
not checked nobody has listened to the mix at full speed on speakers
```
