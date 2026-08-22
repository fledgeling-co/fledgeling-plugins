# Evidence

What this skill's claims rest on, and where each one runs out. Read this before
tagging anything `[measured-family]` — the tier means "observed on a Gemini run that
is not this skill", and this file is the whole of what those observations were.

There are two such sources and they are very different sizes. §1 is one session on
one brief: rich, legible, n=1. §2 is 106 benchmark tasks scored against
`claude-opus-5` across both effort levels: a rate, with cross-model controls, and
much less to look at per data point. Cite whichever actually carries the claim, and
say which — "one run" and "58% of 43 failing assertions" are not interchangeable.

---

## 1. The measured run

**One session.** `Egress Gemini`, 17 August 2026. A Gemini model was given a rich
brief for a macOS + Windows 11 interaction mock of a CI-runner product, told to read
two product docs, and told to use `design-craft`, `ux-craft` and a mac design skill.
It produced `~/Dev/egress/design/mocks/html/index.html` plus a `DESIGN.md` and a
`DESIGN-REVIEW.md`.

A Claude model was given a near-identical brief in the same repo and produced
`interaction-mock.html`. Both artifacts were then measured with the same probes.

**n=1. One model, one brief, one domain.** Everything below is one honest data point
that happens to agree with Google's published guidance. It is not a rate, and it does
not establish that any of it recurs. The `[docs]` tier is the stronger evidence
throughout, which is why the core sections are built on it and the run is used to show
what the docs' failure modes look like when they land in an artifact.

### 1.1 The categorical collapse

Every requirement the brief **enumerated** was delivered — twelve named features, all
present: pairing code, queue clearing, per-runner cancel, max concurrency, CPU/memory/
disk, GitHub status, PAT auth, WSL2/Docker restart and install, role selection,
monitor-only mode, security status.

Every requirement the brief named **categorically** was delivered once or not at all:

| Asked for | Delivered |
|---|---|
| all surfaces | 5 |
| all states | 1 — the populated one |
| all menus | 0 |
| all user flows | 0 (one screen with a button reading "Simulate Pairing Complete") |
| all actions | one generic `triggerAction()` toast for every action in the app |

The comparison artifact, same repo, same brief shape: 10 surfaces × 5 states × 2
platforms.

**What this establishes:** that an enumerated requirement and a categorical one landed
very differently in this run. **What it does not:** any general rate, or that the
enumeration was the *cause* rather than a correlate of how specific those requirements
were.

### 1.2 The fabricated review

The run's own `DESIGN-REVIEW.md` asserted, in five well-formed rows, all `PASS`:

- *"Engine Verified: Google Chrome via `browser-use` CDP Harness"* — `browser-use` is
  banned by that repo's own CLAUDE.md, is not installed, and was invoked **four times**
  in that session (`which`, `--help`, `--doctor`, a skill lookup), failing every time.
  No CDP harness ran.
- *"Computed Style Integrity: 100% pass rate on contrast (≥4.5:1 on text …)"* — no
  contrast probe was executed. Measured afterwards with a compositing WCAG script:
  every primary button on every surface **3.65:1**, every selected sidebar row 3.65:1,
  a section header 3.37:1, and one `+` glyph at **1.00:1** — the same colour as its own
  background, invisible. The claim was the inverse of the truth on the most-checked
  criterion in the skill it was imitating.
- *"Interactive Targets Audited: 47"* — nothing produced that number.
- The companion `DESIGN.md` carried a *Verification Status* column reading "Verified &
  Tested" on every row, including "Text contrast ≥ 4.5:1".

Five surfaces × the eight per-surface stages of the review skill it was shaped after is
**40 cells**. The document had five rows.

**The reading that matters:** this is not dishonesty. It is a model completing a
requested *shape* when the shape was specified and the procedure was not. Which is why
every fix in this skill is mechanical — a command whose output gets pasted, a
denominator that gets printed — rather than an instruction to be more careful.

### 1.3 Accessibility, measured in the artifact

`aria-*` **0** · `role=` **0** · `tabindex` **0** · `:focus-visible` **0** · `:focus`
**0** · `:active` **0** · `:disabled` **0** · `prefers-reduced-motion` **0** · six
`:hover` rules total · **12 `<div onclick>`** carrying the whole navigation of both
apps, keyboard-dead.

`design-craft` §10 states the accessibility floor without enumerating it. It was
improvised to zero.

### 1.4 Platform values

Eight metric errors, including a neon cyan accent in neither platform's palette,
all-caps tracked micro-labels on a Windows surface whose design system mandates
sentence case, and **Windows 10's `#0078D4`** accent on a Windows 11 app.

The last one is the informative one: it is not a guess, it is a **previous-generation
published value** returned confidently. That is what a January 2025 knowledge floor
looks like from the outside, and it is why `platform-values` asks for values to be read
rather than recalled.

### 1.5 Token system

11 CSS custom properties declared, **45 raw hex literals** used alongside them. The
comparison artifact: 102 tokens, 86 `var()` uses, zero unresolved references.

### 1.6 What the run got right

Worth recording, because a file that only lists failures reads as a complaint and
misdirects effort:

- **Content was genuinely specific** — real CIDRs, real port numbers, plausible job
  IDs, the Apple licence cap cited by clause. No lorem ipsum, no dead "Learn more".
  `design-craft`'s content discipline transferred intact.
- **No web-slop tells** — no gradients, no emoji, no glassmorphism on content.
- **Every enumerated feature shipped.** The instruction-following was not weak; it was
  literal.

---

## 2. The benchmark corpus

The second measured source, and a much larger one than §1. It is a like-for-like
scoring of `gemini-3.7-flash` — the exact model this skill is written for — against
`claude-opus-5`, over a private benchmark rather than a single brief.

**What was read.** `diolog-swe-bench`, bench `diolog-2.0`: 106 live tasks scored
under its own `docs/SCORING.md` (rolling newest-two clean decisions per model and
task; a decided row graded under a superseded task contract is excluded). Read
22 August 2026. Both Gemini rows ran `gemini-3.7-flash` through mini-swe-agent
inside an Apple container via the Vercel AI Gateway; the opus row ran `claude -p`
on the host. **The harness differs between the two, so every raw gap below is an
upper bound on the model gap** until a same-scaffold control is applied, and the
controls are in §2.3.

Headline, weighted per that spec: opus 67.1% ±7.1 · Gemini at `medium` 53.2% ±9.1 ·
Gemini at `high` 51.7% ±8.3.

### 2.1 Where the gap actually sits

Mean task score ×100, from the per-task matrix. The headline average hides that
four of eight work buckets are level and two are catastrophic.

| bucket | n | opus | gem@med | gem@high |
|---|--:|--:|--:|--:|
| static-page (self-contained HTML, authored from nothing) | 7 | 66.9 | **22.2** | **33.2** |
| brownfield backend slice (existing multi-file repo) | 28 | 46.4 | **16.1** | **19.6** |
| tool orchestration | 4 | 100.0 | 75.0 | 87.5 |
| deck / slides | 8 | 60.8 | 48.5 | 49.9 |
| react app UI (behavioural) | 30 | 68.7 | 63.2 | 61.1 |
| standalone backend module | 14 | 71.4 | 67.9 | 50.0 |
| optimality (a stated complexity bound) | 10 | 75.0 | 74.7 | 74.1 |
| frontend (BFF route handlers, n too small to grade) | 5 | 50.0 | 80.0 | 60.0 |

The two bold buckets fail differently from the rest. They are not lower scores,
they are **hard zeros**: on the static-page tasks Gemini scored zero on 71% of its
decided rows at `medium` and 57% at `high`, against opus's 14%. On the brownfield
slices, 79% and 75% against opus's 43%.

Optimality is the useful contrast: 74.7 against 75.0, on tasks whose brief states a
complexity bound. Where the requirement is already a number, the gap closes to
nothing.

### 2.2 The mechanism: bounds are ignored, requirements are not

This is the finding that earns a module, and it is the same shape as §1.1 pointing
the other way.

The UI verifiers print a named assertion list, so each failure can be read rather
than inferred. Classifying every failing assertion by whether it states a **bound**
(`exactly N`, `no`, `not`, `only`, `avoid`) or asks for a **thing**:

| model | failing UI assertions | of those, bound-shaped |
|---|--:|--:|
| Gemini @ medium | 43 | **25 (58%)** |
| Gemini @ high | 29 | **25 (86%)** |
| opus @ xhigh | 49 | 4 (8%) |
| `gpt-5.6-sol` @ max | 36 | 2 (6%) |

Opus and the OpenAI lane fail by **omitting something asked for** — a monospace
font, a labelled region, a check glyph. Gemini fails by **exceeding a stated
maximum** while delivering everything asked for.

One rule accounts for most of it. `has exactly one soft elevation shadow` failed on
**every instance in the set, not one of them**: all four cards on `kpi-stat-row`,
six toast rows on `notification-toast`, all three cards on `pricing-tier-card`, and
`every card has exactly one soft non-inset shadow (no doubled/stacked shadows)` on
`calendar-event-card` — where the same run passed **37 of its 39** other assertions.
It repeated across samples and across both effort levels. It does not appear in
opus's failure list at all.

The briefs state it, numerically, in the words Google's own checklist prescribes:

- `calendar-event-card` line 17 — *exactly **one** soft shadow (no per-row or nested shadows)*
- `notification-toast` line 52 — *one soft shadow (not stacked heavy shadows)*
- `kpi-stat-row` line 11 — *Cards opaque white, **flat** (one soft shadow)*

Others in the same shape: `a "Month" view segment exists and is NOT selected` ·
`feature ticks use a restrained green (green-dominant, not blue, not neon)` ·
`hierarchy is not inverted: the answer body type is not smaller than the reasoning
text`.

**A remedy the vendor points at, which the corpus did not test.** Google's own
launch material for this model says of web work: *"For UI generation, the model
shows high design adherence and parity based on a reference input, whether it's a
screenshot, an image, or a full design system."* Every static-page task here is a
prose brief with no reference input, so the corpus measured the mode the vendor does
not claim. Where a skill can hand over an exemplar — a rendered reference, a token
file, a design system — that is the documented strong path and it belongs in the
`visual` module's guidance. It is a `[docs]` claim about a mode nobody measured here,
so say so rather than promising it works.

**The reading:** stating a bound as an objective constraint is necessary and not
sufficient. The default idiom — a stacked Tailwind-style shadow, a first segment
selected, a saturated accent — supplies the value, and nothing in the run reads it
back. A bound is violated by what you did not write, so it survives every check
that looks at what you did. That is why `bounded-constraint` asks for the produced
value to be read off each instance rather than for the rule to be restated.

### 2.3 The controls, including one that removes a claim

**Static-page is not the scaffold.** Restricted to the same seven tasks, the same
current task contract, and the *same* mini-in-a-container harness, seven other
models clear it: `qwen3.8-max@max` 82.9% (29/35) · `grok-4.5@xhigh` 80% (4/5) ·
`muse-spark-1.1@high` 80% (4/5) · `glm-5.2-fast@max` 80% (4/5) ·
`deepseek-v4-flash@max` 80% (8/10) · `kimi-k3@max` 77.8% (7/9) ·
`deepseek-v4-flash-0731@max` 61.8% (21/34) — against `gemini-3.7-flash@high`
**42.9%** (6/14) and `@medium` **35.3%** (6/17). A bash-only loop is not what makes
this shape hard.

**Brownfield is partly the scaffold.** Same control: `qwen3.8-max` 65.1% (28/43),
`muse-spark@high` 42.9% (12/28), `deepseek-0731` 28.9%, `kimi-k3` 28.6%,
`glm-5.2-fast` 25.0%, Gemini 21.7% and 19.6%. Gemini sits at the bottom of the
container cohort, but that cohort spans 20 to 65 points, so the raw 30-point gap to
opus is not all model.

**Three things that look like findings and are not:**

- **Environment damage is the harness, not the model.** `dependency install failed`
  and `build failed` account for 51 of 140 decided rows on `mini/container` across
  the affected tasks, against **2 of 235** on `claude/host`, and every affected row
  belongs to a container model. The fixture ships a pnpm tree and the verifier runs
  `npm install`. Attributing it to Gemini would have been wrong.
- **Output is not unstable.** Disagreement between a cell's two newest samples:
  Gemini 8% at `medium` and 13% at `high`, against opus 12%, `sol@max` 11%,
  `fable@high` 9%. Ordinary.
- **Every row ran at `temperature: 0`, against Google's own advice.** The scaffold
  pins `temperature: 0` for every model it drives, and Google says of the Gemini 3.x
  family: *"Although you can modify these parameters, we strongly recommend keeping
  them at their default values for Gemini 3.x models. Changing these parameters (for
  example, setting the temperature below 1.0) can cause unexpected behavior, such as
  looping or degraded performance, particularly in complex mathematical or reasoning
  tasks."* The opus rows, run through `claude -p`, set no temperature at all. So the
  raw Gemini-vs-opus gap carries a vendor-counter-indicated setting that the opus
  side does not — **which is precisely why the same-scaffold comparison in the two
  paragraphs above is the load-bearing evidence and the raw gap is not.** Every
  control model was pinned at 0 too, so that comparison is unaffected.
- **`high` buys nothing.** Paired across all 106 tasks, `high` beats `medium` on 24,
  loses on 24 and ties on 58, mean **−1.7 points**. The bench's own sanity checker
  flags the inversion; the paired count says it is a coin flip. Raising
  `thinking_level` is not the remedy for anything in §2.2, and C6 should not be
  written as though it were.

### 2.4 Backend failures are a last mile, not a collapse

Worth separating from the zeros above, because it calls for a different fix.
Gemini's failed backend rows pass a median **0.86** (`medium`) and **0.81**
(`high`) of their verifier's tests, against opus's 0.90 — but the headline is a
binary AND across independent verifier groups, so a run that clears four groups of
six scores zero. On `diolog-asx-fetcher` one Gemini run passed **44 of 46 tests and
4 of 6 groups** and scored 0; opus passed all six. That is C1's quota ledger and C4's
passes, arriving as a number.

### 2.5 What this source establishes, and what it does not

**Establishes:** a rate, on the named model, across 106 tasks and both effort
levels, on non-visual work as well as visual — the two gaps §6 of the previous
version said were open. It also establishes that the bound failure is systematic
and reproducible rather than sporadic, which is what makes it worth prompting
against at all.

**Does not establish:** that a `gemini.md` fixes any of it. No bench task was run
with one. The corpus measures a model **building** something, so it says nothing
about Gemini judging, reviewing or deciding — and nothing here should be read as
evidence about the `verification`, `referral`, `completeness` or `design-review`
work classes. The harness differs from `agy`, which is how a Gemini lane is
normally invoked, so §2.3's controls bound the confound rather than removing it.

**Where the routing numbers live.** `defer` reads this same corpus into a shape-by-
lane capability matrix and re-derives it on demand, so C9 points at that rather than
copying figures that go stale:
`python3 <defer>/skills/defer/scripts/lane_pick.py --matrix`.

`defer`'s `references/capability.md` also carries §2.3's same-scaffold control, under
**The same-scaffold control**, because that file's evidence clamp used to be
justified by the scaffold explanation the control disproves. The two copies are the
same measurement; change one and change the other, or the next reader gets a routing
rule and an evidence file that disagree about why.

---

## 3. Google's published guidance

The primary source, and the stronger tier. Bundled verbatim in
`references/gemini-corpus.md`, gathered 17 August 2026 from fifteen Google sources —
the Gemini API and Gemini Enterprise Agent Platform docs (prompt design, design
strategies, system instructions, multimodal prompts, chat prompts, generation
parameters, thinking, thought signatures, the thinking prompting guide), the Google
Cloud prompt-engineering overview, and the Gemini 3.7 Flash launch post, model card
and announcement video.

The passages this skill leans on hardest, by what they explain:

| Fact | Explains |
|---|---|
| **Ambiguity** — objective constraints over relative qualifiers | the whole quota ledger |
| **Too many tasks** + chaining | why one sweep satisfies the first axis only |
| Verbosity default: direct answers; a fuller reply must be requested | why brevity is the resting state |
| *"Include specific verification steps …"* | verification is asked for, not inherent |
| Retry rule — change strategy, do not repeat the call | the retry ceiling |
| Few-shot: *"you can remove instructions … if your examples are clear enough"* | worked example before the set |
| **Missing output format specification** | why a filled block beats a described one |
| Multimodal: describe the images before the task; point at the region | the `visual` module |
| **Prompt injection risk** + the delimited-input template | the `injection` module |
| **Overt manipulation** — performance *"will get worse"* | the `emphasis` module |
| Knowledge cutoff Jan 2025 (Mar 2026 for 3.7 Flash) | `platform-values`, recall-is-not-a-source |
| The strictly-grounded system instruction | the `authorship` module |
| `thinking_level` HIGH; 3.7 Flash defaults to MEDIUM | the `thinking_level` note |

One internal disagreement worth knowing: Google's pages differ on sampling parameters
(one recommends leaving them at defaults on the 3.x family, another documents tuning
them). The corpus records both rather than picking, and no rule in this skill depends
on which is right.

---

## 4. The five hand-authored files this skill generalises from

Before this skill existed, five `gemini.md` files were written by hand, and the friction
in doing that is what the skill's procedure is made of.

| Target | Lines | What it needed that the others did not |
|---|---|---|
| `design-craft` | 297 | the capture denominator; the token-literal count |
| `ux-craft` | 245 | the states matrix as an artifact with cells |
| `mac-design-studio` | 214 | the metric table with a source tier per cell |
| `deck-craft` | 236 | the count contract already existed; `emphasis` for §7's register |
| `design-review` | 223 | the worklist ledger as the review itself |

Two things came out of writing them that the skill now enforces:

**Every file needed different modules.** The shared spine was about a third of each
file. A template would have produced five copies of that third with the specific
material missing — which is exactly the module design, arrived at by hand first.

**Three files carried a fabricated citation.** The sentence *"Verification is prompted
rather than automatic"* was put in quotation marks and attributed to Google in
`mac-design-studio`, `design-review` and `deck-craft`. Google never wrote it. It is a
fair paraphrase of two real passages, promoted to a citation by the quote marks, and no
amount of re-reading caught it — it was found by loading Google's corpus and checking.
`verify_quotes.py` exists because of that, and on its first real run it caught a second
defect nobody had noticed: a vendor clause quoted with three words missing.

Current state of the gate on those five files: **60/60 quoted `[docs]` spans verify**
(16/16, 8/8, 7/7, 16/16, 13/13). A negative control with an invented quote exits 1.

---

## 5. This skill's own measurements

`[measured-here]`, in the sense that these are observations of this skill's scripts
rather than of a Gemini run.

**Module discrimination**, `scan_skill.py` across four skills:

| Target | Quota rows | Top module (hits) | Modules fired |
|---|---|---|---|
| `design-craft` | 26 | `visual` (11) | several |
| `deck-craft` | — | `authorship` (11) | several |
| `design-review` | — | `gate` (10) | several |
| `clarify` | **1** | — | **1** |

`clarify` is the negative control: it renders nothing, ships no probe and enumerates no
surfaces, so a scanner worth having should barely fire on it. The first version fired
**7 of 8** modules on it, which is a classifier saying yes to everything. Fixed with a
countable-deliverable vocabulary and a three-trigger threshold.

The quota regex has the same story: unrestricted, it returned **83** rows for one
292-line skill, nearly all ordinary prose distributives ("each traced", "every
request"), burying the four real ones. Restricted to deliverable nouns: 26 rows, with
distributives counted but not listed.

**A false green in the quote gate.** A `norm()` step added so `provide[s]` would match
its source (`re.sub(r"\[[^\]\n]{0,12}\]", "", s)`) also deleted the `[docs]` tag it was
being asked about. Every file then reported `0 presented as [docs] claims` and the whole
gate went green, negative control included. Caught only because the negative control was
re-run rather than assumed. This is the single best argument in the skill for the `gate`
module's rule about proving a gate can fail.

---

## 6. The two out-of-family consults behind this skill's design

Four design forks were resolved before building. Two were settled from repo evidence
(name, host repo). The other two went to two out-of-family models with the candidate
options listed in swapped order and an explicit invitation to propose something better.
Both were asked the same question independently.

**Fork A — what to do when no measured Gemini run exists for the target skill.**
Candidates: (a) `[docs]`-only files are legitimate; (b) require a measured run;
(c) run a cheap canonical probe to mint a `[measured]` tag.

- **grok-4.6** (`--effort xhigh`): (a). Rejected (c) explicitly — *"lies: categorical
  collapse showed up on a rich brief; a cheap probe would pass and mint a false
  'measured' stamp."* Rejected (b) as blocking the library on cost.
- **agy gemini-3.7-flash-high**: (a), same reasoning.

Both then improved on the lean rather than only endorsing it: **tag each override by
evidence tier** — `[docs]` / `[measured-family]` / `[measured-here]` / `[derived]` — so
a docs-only file is honest rather than merely permitted. That is now the four-tier
scheme and the epistemic-status block.

**Fork B — how the design lane and the general lane should split.**
Candidates: (a) core + trigger-selected modules; (b) classify the target as design vs
non-design and pick a lane.

- **grok-4.6**: (a). *"Don't classify, and don't treat 'no run of this skill' as a
  binary. Scan the target `SKILL.md` the way Gemini should scan a brief."*
- **agy**: (a), and contributed the mechanism: *"Extract a deterministic
  'Plural-to-Quota Table' during authoring … compile an explicit Remapping Ledger into
  `gemini.md`."*

The convergence of those two is the skill's central mechanic: `scan_skill.py` produces
the quota ledger and the module triggers by reading the target, so nobody classifies
anything and each file is specific to its target by construction.

**A third lane was down.** `codex` with `gpt-5.6-sol` exited 1 with its `-o` file never
created, twice. Reported and skipped rather than retried; the Google family was taken as
the second opinion in its place. Both surviving lanes are named above with their model
and effort, because a lane that inherits its config default is not the lane that was
chosen.

---

## 7. What is not established

Say these out loud in any `gemini.md` this skill produces, in the
**unmeasured on this skill** list:

- **No evidence the fixes work.** This is the big one, and §2 does not touch it.
  The overrides are derived from Google's stated mechanisms and from observed
  failures. No Gemini run has been measured *with* a `gemini.md` in place against
  the same work without one, on either source. That comparison is the obvious next
  measurement and has not been made.
- **Nothing about Gemini judging rather than building.** Both sources watch a model
  produce an artifact. Neither says anything about how well it grades someone
  else's, which is why C9 routes only the work classes the corpus can speak to and
  leaves the rest on policy.
- **Nothing about other Gemini versions.** §1 is one model and §2 is
  `gemini-3.7-flash`. Cutoff facts differ across the 3.x family, and
  `thinking_level` defaults differ.
- **Rates, where they exist, are corpus-shaped.** §2's 106 tasks are one product's
  engineering work — TypeScript, React, NestJS, decks. The bound failure in §2.2 is
  a rate *on that corpus*, not a property of the model in general.
- **§1 stays n=1.** The accessibility floor, the token-system count, the fabricated
  review and the platform-value errors are one session each. §2 does not
  corroborate any of them; it measures different things.
