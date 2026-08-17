# Evidence

What this skill's claims rest on, and where each one runs out. Read this before
tagging anything `[measured-family]` — the tier means "observed on a Gemini run of
another skill", and this file is the whole of what that observation was.

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

## 2. Google's published guidance

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

## 3. The five hand-authored files this skill generalises from

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

## 4. This skill's own measurements

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

## 5. The two out-of-family consults behind this skill's design

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

## 6. What is not established

Say these out loud in any `gemini.md` this skill produces, in the
**unmeasured on this skill** list:

- **No rate for anything.** n=1 on one brief in one domain.
- **No evidence the fixes work.** The overrides are derived from Google's stated
  mechanisms and one observed failure. No Gemini run has been measured *with* a
  `gemini.md` in place against the same brief without one. That comparison is the
  obvious next measurement and has not been made.
- **Nothing about other Gemini versions.** The run was one model. The cutoff facts
  differ across the 3.x family, and `thinking_level` defaults differ.
- **Nothing about non-visual skills at all.** Every measured observation here comes
  from a build-a-UI brief. The core sections claim to generalise on the strength of
  Google's docs, not on measurement.
