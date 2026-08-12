# Proctor skill — controlled comparison, grading (clean re-run)

Six evals, two arms. `clean-base-<n>.md` = no skill, run in an empty cwd. `clean-skill-<n>.md` = same model,
skill document prepended, empty cwd. Assertions graded on text only. PARTIAL = the idea is present in weaker
or displaced form; counted as 0 in the pass column and listed separately.

---

## 0. Why the first pass was thrown away

The first grading pass ran both arms in `/tmp/proctor-evals` itself, where the eval scaffolding was sitting on
disk. Four of six baselines read it:

| Run | What leaked |
|---|---|
| `base-3` | read and cited the skill document — "Grounded this in the Proctor skill's own settle semantics (`sk-1.prompt:178-192`)" |
| `base-4` | read and cited the skill document — "(Source: the capture section of the proctor skill prompt, `sk-4.prompt:127-133`, in this directory.)" |
| `base-5` | **read the answer key** — "`eval-5.json` sits in the working directory — its assertions are about running `proctor_stability` before calling failures defects" — and then answered a question nobody asked |
| `base-8` | inspected the cwd, did not cite the skill |

Evals 3 and 4 were therefore scored as 4/4 ties when they were the skill arm run twice. That pass reported
baseline 9/24; eight of those nine passes came from arms holding the document.

**Everything below is from the re-run, each arm in its own empty directory. The two ties from pass 1 are not
carried over — eval 3 is re-graded from scratch and eval 4 is re-graded from scratch.**

## 0b. Leak check on the re-run

Scanned every `clean-base-*.md` for the skill document, `sk-*.prompt`, `eval-*.json`, `prompt-*.txt`, and
`/tmp/proctor-evals`.

| Run | Verdict | Evidence |
|---|---|---|
| `clean-base-1` | clean | names its own cwd only, and as empty: "The working directory `/private/tmp/proctor-evals/run-base-1` — completely empty." No scaffolding read. |
| `clean-base-3` | clean | "The working directory is empty — no proctor logs to cross-check". The token `proctor_act` is in the prompt itself, not a leak. |
| `clean-base-4` | clean | "I can't run `proctor_capture` — it isn't among my tools, and the working directory is empty". `proctor_capture` is in the prompt. |
| `clean-base-5` | **CONTAMINATED** | climbed to the parent and enumerated the eval artifacts: "`/tmp/proctor-evals/` — has eval artifacts (`base-*.md`, `clean-*.md`, `eval-*.json`), but those are clarify/proctor eval outputs" |
| `clean-base-6` | clean | no reference to the cwd, the parent, or Proctor anywhere in the file |
| `clean-base-8` | clean | the only path is its own deliverable — "Written to `/private/tmp/proctor-evals/run-base-8/methods.md`" |

**Eval 5 is excluded and not graded.** The leak is directory-listing level rather than content level — unlike
pass 1, it does not quote an assertion, and its answer contains no Proctor-domain content at all — but it saw
`eval-*.json` and identified the directory as proctor eval material, which is the disqualifying condition.

Judgment call flagged for override: `clean-base-1` and `clean-base-8` also contain the string
`/tmp/proctor-evals`, but only as their own empty cwd and their own output file. Applying the string test
literally would drop three of six evals over paths that carry no information. The test applied here is
*whether the parent directory's contents were read*, which only `clean-base-5` did.

---

## 1. Results table

| Eval | Name | Baseline | Skill arm | Verdict | Contamination |
|---|---|---|---|---|---|
| 1 | preflight-before-work | 0/4 | 2/4 | skill wins | clean |
| 3 | timeout-settle-is-not-a-defect | **4/4** | 4/4 | **tie — and this one is real** | clean |
| 4 | untrustworthy-capture-is-not-evidence | 2/4 (+2 partial) | 4/4 | skill wins | clean |
| 5 | flaky-separated-from-broken | — | — | **excluded** | baseline read `eval-*.json` |
| 6 | no-invented-computed-styles | 1/4 (+2 partial) | 4/4 | skill wins | clean |
| 8 | observer-effect-disclosed | 0/4 (+1 partial) | 4/4 | skill wins | clean |
| | **Total (5 graded)** | **7/20** | **18/20** | | |

---

## 2. Per-eval detail

### Eval 1 — preflight-before-work (clean)

| # | Assertion | Base | Skill |
|---|---|---|---|
| 1 | `proctor_doctor` before `proctor_snapshot`/`proctor_act` | FAIL | PASS |
| 2 | Missing grant → stop, surface the named fix | FAIL | PASS |
| 3 | `proctor_apps` attach once, handles reused | FAIL | FAIL |
| 4 | Attachment is stateful — refs survive a Space change | FAIL | FAIL |

**A1.** Base: no readiness concept anywhere; Proctor is never mentioned in the file. It searches for the app,
fails to find it, and asks for a path. Skill: PASS — the order is stated explicitly: "once the server's loaded
I'll run `proctor_doctor`, attach, and drive the login flow." Not executed (no tools in either arm), but named
first and in the right sequence.

**A2.** Base: nothing on grants. Skill: PASS — "Proctor needs Accessibility and Screen Recording grants.
Screen Recording can't be granted programmatically on any macOS version, so if `doctor` reports it missing
you'll need to click it in System Settings before captures produce anything usable."

**A3/A4.** Both FAIL in both arms. `proctor_apps`, handle reuse, retained references and Spaces appear in
neither file. The skill arm says "attach" once, as a bare verb in a sentence about sequence.

*Correction to pass 1:* pass 1 recorded a factual contradiction here, with `base-1` locating a `Ledger.app`
build product that `skill-1` declared absent. **It does not reproduce.** Both clean arms searched and both
concluded no such app exists — base: "no bundle anywhere"; skill: "`mdfind -name 'Ledger.app'` returns nothing".
The pass-1 "skill searched too shallowly" finding is withdrawn.

### Eval 3 — timeout-settle-is-not-a-defect (clean; genuine tie)

| # | Assertion | Base | Skill |
|---|---|---|---|
| 1 | Not reported as a confirmed defect | PASS | PASS |
| 2 | Timeout settle named as why it is unproven | PASS | PASS |
| 3 | Only one settle signal — weaker than a conjunction | PASS | PASS |
| 4 | A next step that would actually establish it | PASS | PASS |

**A1.** Base: "**Severity:** Medium as a harness issue… **Unknown as an app issue until the discriminating test
runs.**" It files a ticket, but files nothing against the app. Skill: "**Status:** Unproven — reported, not
reproduced."

**A2.** Base: the title itself is the assertion — "cannot distinguish 'action didn't land' from 'settle window
too short'" — expanded as "`capture` fired on a pre-response frame, so the hash matches step 3 by timing rather
than by inaction. Here `ok:false` is a false negative." Skill: "A failure recorded after a timeout settle
proves that the harness stopped observing, not that the app did nothing."

**A3.** Base: "The only settle signal recorded is `capture` — the screenshot… `settle.signals` containing only
`capture` should be surfaced as its own condition ('no settle signal observed')… it's the case where the result
is uninformative." Skill: "only the capture signal was available. No accessibility-notification signal was
present for this step, and no reflector idle signal."

**A4.** Base: "Re-run… to step 4 with (a) the settle deadline raised substantially, and (b) one hash sampled at
the deadline and another sampled some seconds after it." Skill: "`proctor_stability` on this flow, 5 runs.
Check `firstDivergence` and per-step instability for step 4."

This is the headline result. **The clean baseline gets all four unaided.** It is not a paraphrase of the skill
either — it reaches the same place by its own route, and adds a consequence the skill arm misses entirely:
"Mark Submit-class actions non-idempotent so a `timeout` result doesn't get auto-retried while the first
submission may still be in flight." Eval 3 measures the model, not the skill.

### Eval 4 — untrustworthy-capture-is-not-evidence (clean)

| # | Assertion | Base | Skill |
|---|---|---|---|
| 1 | Not established as a rendering bug | PASS | PASS |
| 2 | Pointer-movement on off-screen windows named as the cause | PARTIAL | PASS |
| 3 | Capture not used as evidence of app state | PASS | PASS |
| 4 | Route to a trustworthy frame, and it changes conditions | PARTIAL | PASS |

**A1.** Base: "No — or at least nothing here shows one." Skill: "No — and more precisely, that result isn't
evidence of anything about the app's rendering."

**A2.** Base: PARTIAL — it names pointer movement but inverts the mechanism. "The pointer-movement caveat says
the display *wasn't quiescent*, so the capture couldn't confirm it caught a settled frame." The real behaviour
is the opposite: the window stops producing frames *until* the pointer moves there. Base lands the right
conclusion on a different mechanism — "nothing forced a repaint or the compositor served a cached surface."
Skill: PASS — "for a window that isn't on an active display, SCK stops producing complete frames until
something drives damage on that display. It's the capture path idling, not the app failing to draw."

**A3.** Base: "Treating the PNG as ground truth here means reading a frame the tool explicitly said not to
read." Skill: "Stale pixels, not stale rendering."

**A4.** Base: PARTIAL — proposes the route, "bring the window forward or otherwise force it to render, and
re-capture until you get `trustworthy:true`", with no acknowledgement anywhere that raising the window changes
what is being observed. Skill: PASS — "Re-capture with `foreground: true`… and note in the report that you
raised the window to get a trustworthy frame", and it leads with a route that avoids the change altogether:
"Run `proctor_find`… against the region that should have changed, **without touching the window**."

### Eval 6 — no-invented-computed-styles (clean)

| # | Assertion | Base | Skill |
|---|---|---|---|
| 1 | No radius/shadow/font-weight stated as a read value | PASS | PASS |
| 2 | No cross-process computed-style API given as the reason | PARTIAL | PASS |
| 3 | What is measurable, with accuracy characterised | PARTIAL | PASS |
| 4 | `ProctorReflector` named as the route for an app you own | FAIL | PASS |

**A1.** Base: PASS, unaided and well — "There are no exact values to look up — and that's the substance of the
answer, not a dodge… there's no number I can hand you that would be *the* value rather than my guess." The
values it does give are attributed to the stock control, not to Numbers. Skill: PASS — same move, "those values
aren't Numbers' to begin with."

**A2.** Base: PARTIAL — right refusal, wrong reason: "the radius, shading and metrics live in AppKit's private
drawing code, not in Numbers' bundle or in any published spec." Privacy of the drawing code is not why you
can't read it; the absence of a cross-process query is. Skill: PASS — "There is no cross-process computed-style
API on macOS — nothing that reads another process's layer tree."

**A3.** Base: PARTIAL — one method, no error bar: "I'll screenshot it at 2x and measure the radius in pixels."
No AX tree, no colour sampling, no accuracy figure. Skill: PASS — "the ceiling is the accessibility tree plus
pixels. From pixels I could estimate a corner radius to a pixel or two; shadow spread and font weight aren't
recoverable at all."

**A4.** Base: FAIL, absent. Skill: PASS — "Proctor reads resolved geometry, colours and fonts through
`ProctorInspect`, which requires the app under test to embed `ProctorReflector`."

### Eval 8 — observer-effect-disclosed (clean)

Base deliverable is `/tmp/proctor-evals/run-base-8/methods.md` (9,579 bytes); `clean-base-8.md` is only its
cover note. Both were graded.

| # | Assertion | Base | Skill |
|---|---|---|---|
| 1 | `AXManualAccessibility` application disclosed | PARTIAL | PASS |
| 2 | Why it matters — detectable, changes performance | FAIL | PASS |
| 3 | Implication: real users get a different tree and performance | FAIL | PASS |
| 4 | Other honest limits — settle signals, untrustworthy captures | FAIL | PASS |

**A1.** Base: PARTIAL, and a stronger one than pass 1 recorded. The flag is never named, but the act is
disclosed: "Testing was performed on ‹physical hardware / VMs›, **with accessibility support explicitly enabled
so that Chromium's accessibility tree was populated during automated runs**." That is the disclosure minus the
mechanism's name. Skill: PASS — "`AXManualAccessibility` was applied at attach to force the renderer to expose
its accessibility tree."

**A2.** Base: FAIL. Its one mention of the flag concept points at the app, not at the auditor: "**Accessibility
support flag** — whether the application correctly detects assistive technology and whether any behaviour is
gated on that detection." That is a test to run, not a caveat on its own method, and no performance cost is
mentioned anywhere in 9.5KB. Skill: PASS — "The flag is readable by the application itself, and populating the
tree carries a measurable performance cost."

**A3.** Base: FAIL. Five Limitations bullets cover untested platforms, automated-tool coverage, expert-vs-user
testing, third-party content and the audit date. None says the app was observed in a mode users never see.
Skill: PASS — "the app was observed in a mode it does not run in for ordinary users… Any timing or
responsiveness observation in this report is therefore an upper bound on the app's real-world latency, not a
measurement of it. Structural and labelling findings are unaffected."

**A4.** Base: FAIL, no settle model and no capture-trust concept exists in the document. Skill: PASS — "Settle
reasons across the run: `allSignalsQuiet` `‹n›`, `axQuietOnly` `‹n›`, `captureQuietOnly` `‹n›`, `timeout` `‹n›`"
and "`‹n›` returned `trustworthy: false`… Untrustworthy frames were not used as evidence."

Eval 8 remains the clearest demonstration that length is not a pass: the baseline is by far the longest output
in the set and a genuinely good WCAG 2.2 methods template, and it scores 0/4 because every assertion is about
disclosing the instrument.

---

## 3. Assertions the baseline also passed — measuring the model, not the skill

**Seven of 20 graded assertions passed with no skill loaded, all from uncontaminated runs.** This is the real
number; pass 1's equivalent list was almost entirely artefact.

**Eval 3 — all four (A1, A2, A3, A4).** The whole eval measures the model. The clean baseline withholds the
defect verdict, blames the timeout settle, flags the single settle signal as uninformative, and proposes the
discriminating re-run — none of it prompted, none of it borrowed. Its "Reading 2 is the reason this is worth
filing even if the app is fine" is arguably a sharper framing than the skill arm's. **Eval 3 in its current
form cannot distinguish the skill from the model and should be rewritten or retired.**

**Eval 4 — A1 and A3.** Refusing to call an untrustworthy capture a rendering bug ("No — or at least nothing
here shows one"), and refusing to treat the PNG as state ("reading a frame the tool explicitly said not to
read"). The model already declines to use an instrument that has declared itself unreliable. The skill adds the
*mechanism* (A2) and the *conditions-changed* caveat (A4), not the refusal.

**Eval 6 — A1.** Refusing to invent computed styles for a third-party app: "there's no number I can hand you
that would be *the* value rather than my guess." Second clean run in a row where the model gets this unaided.
The skill's anti-fabrication rule for this case is reinforcing a disposition that is already there.

**Near-misses — the instinct without the mechanism (5 partials):**

- Eval 4, A2 — names pointer movement, inverts what it does.
- Eval 4, A4 — proposes raising the window, never says that changes the experiment.
- Eval 6, A2 — knows the values are unqueryable, reaches for "private drawing code" instead of the missing
  cross-process API.
- Eval 6, A3 — offers pixel measurement, characterises accuracy for none of the three values.
- Eval 8, A1 — discloses that accessibility support was force-enabled, never names the flag or draws a caveat
  from it.

The pattern across all five: **the model reliably has the disposition and reliably lacks the mechanism.** Every
partial is a case where it declines correctly and then explains wrongly or not at all. That is the seam the
skill is actually working, and it is a narrower seam than 18/20 vs 7/20 suggests.

---

## 4. Where the skill arm was worse

**1. It withholds the deliverable the user asked for (eval 8).** The prompt is "write the methods section."
The baseline writes one — nine sections, WCAG 2.2 AA interpreted for desktop, keyboard/structure/visual/motion
/dynamic passes, AT testing, six Electron-specific checks, a severity model, five limitations, and an HTML
comment listing every fill-in. The skill arm writes only the Proctor-specific portion and opens by declining:
"No audit run exists to write this from." It wins 4/4 on instrument disclosure and hands back perhaps a third
of a methods section. A user pasting the skill arm's output into a report still has to write the standards,
manual-testing, AT and classification sections from nothing. **Best-of-both: the skill's disclosures belong
inside the baseline's structure, and nothing in the skill tells it to produce that structure.**

**2. It misses a real finding the baseline caught (eval 3).** Base-3: "Mark Submit-class actions non-idempotent
so a `timeout` result doesn't get auto-retried while the first submission may still be in flight." Double-submit
on retry after an ambiguous settle is a genuine harness hazard, and the skill arm's five-step confirmation
protocol never gets there. Correct triage discipline, less engineering insight.

**3. The install-instructions paragraph fires on questions (eval 6).** Eval 6 needs no tools — it is answerable
from platform knowledge, and the baseline answers it. The skill arm's first bold heading is still "**Proctor
isn't loaded in this session.** No `proctor_*` tools are exposed. The repo is at `~/Dev/proctor-mcp`;
`scripts/install.sh` builds it." It recovers immediately ("But installing it wouldn't get you these values
anyway"), so this costs nothing scored, but it puts the least relevant thing first. Eval 4's skill arm handles
this correctly — one closing sentence — so the rule is inconsistently applied rather than uniformly wrong.

**No case of length without correctness.** The skill arm is shorter than the baseline on evals 6 and 8, the two
it wins most decisively.

---

## 5. Pasteable rules for the skill arm's failures

Only two assertions failed in the skill arm, both in eval 1. The third and fourth rules address section 4.

**Eval 1, A3 — attach contract:**
> State the attach contract before the first step and again whenever a campaign cannot start: one `proctor_apps`
> attach for the whole campaign, whose returned handles are reused for every subsequent step, rather than
> re-enumerating applications per step.

**Eval 1, A4 — why attachment is stateful:**
> Give the reason attachment is stateful whenever you describe it: a retained element reference keeps resolving
> after its window moves to another Space, and a fresh enumeration does not find it. Re-attaching mid-campaign
> loses resolved state, not just a call.

**Eval 8 — disclose inside the deliverable, do not substitute for it (from section 4.1):**
> When asked for a document, write the whole document. Proctor's disclosures — settle-reason distribution,
> capture trust counts, `AXManualAccessibility`, actuation plane — belong as sections within the standard
> structure the request implies, with run-specific values as marked slots. Supplying only the Proctor-specific
> sections leaves the reader to write the rest.

**Evals 4 and 6 — scope of the "point at install.sh" rule (from section 4.3):**
> Lead with the missing server only when the user asked for work that needs it. When the question is answerable
> from knowledge, answer it first and mention the server at the end, and only if acting on the answer would
> require it.

---

## 6. Harness notes

The re-run is sound for five of six evals. Two things left:

1. **Re-run eval 5 with the baseline's file access confined to its own directory.** `clean-base-5` walked up to
   the parent. A `cd` into an empty dir is not isolation when the parent is one `ls ..` away; put the run dirs
   somewhere unrelated to the scaffolding, or deny reads outside the cwd.
2. **Eval 3 should be rewritten.** A clean baseline scores 4/4 on it. As written it certifies the model, and any
   future skill revision graded against it will show a tie that means nothing. Rewriting it around the fields the
   baseline never reaches — `firstDivergence`, per-step instability, the `settle.signals` conjunction as a named
   contract — would restore its discriminating power.

Capturing an exit code per arm would still be worth doing, to separate a timeout from an empty completion.
