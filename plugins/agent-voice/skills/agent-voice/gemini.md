# agent-voice, calibrated for Gemini

Read this once before Step 1, then run the skill as written with the overrides below; each names
the step it lands on. This target is the unusual case: its own `references/dialects.md` already
carries a Gemini section built from Google's published guidance, and that section is right —
count the categorical scope, name the verification step, constraints first, one delimiter family,
one task per prompt. So the usual work of a `gemini.md` is already done, as *content the skill
hands to its reader*. What is not done is the same discipline turned back on the skill's **own
run**: the routing decision, the two file loads, the register's length target and the lint
invocation are each stated once in prose, and a rule stated in prose is what this family
satisfies once and reports as complete.

## Epistemic status

| Tier | Used here for |
|---|---|
| `[docs]` | Google's published guidance, verbatim from `geminify/references/gemini-corpus.md`. Most of this file rests on it. |
| `[measured-family]` | Two recorded Gemini runs of *other* skills (`Egress Gemini` 2026-08-17, `COD Dossier` 2026-08-23), and the 106-task `diolog-2.0` benchmark. **n=1 each for the sessions; the bench is a rate.** Neither session invoked this skill. |
| `[measured-here]` | Commands run against this package on 2026-08-23 — `scan_skill.py`, `agent_voice_lint.py`, `check_examples.sh`, `check_package.sh`. Observations of the target's own scripts, **not a Gemini run of it**. |
| `[derived]` | My reasoning from those, said as such. |

**Which model the measured claims are about.** Every rate behind this file is flash-tier —
`gemini-3.7-flash`, plus one `gemini-3.7-flash-high` session. Do not project them onto the Pro
tier: there the overrides hold as `[docs]`-grounded discipline while every `[measured-family]`
number is an open question. Defaults have moved inside the family, which is why the level is
named rather than assumed — **[docs]** "If thinking_level is not specified, Gemini 3 will default
to high", then, from the 3.5 Flash release notes, "The default thinking effort is now medium,
changed from high in Gemini 3 Flash Preview."

**Unmeasured on this skill.** No Gemini run of `agent-voice` has been recorded, so nothing below
is measured on this target: not whether the base layer and the register file get loaded before
drafting, not whether `--format` matches the routed register, not whether the delivery note's
four items get filled, not whether a length warning gets read, and not whether a `gemini.md`
changes any of it. **[docs]** This file's own shape is also a defect Google names — "Avoid
writing a prompt with non-linear logic or conditionals that require the model to piece together
fragmented instructions from multiple different places in the prompt." Hence one pass, up front,
each override naming its landing site.

## No route-out block, and which shapes were dropped

The corpus behind C9 measures a model *building* a code artifact, and the four shapes it measured
far enough behind to name are `static-page`, `brownfield-integration`, `visual-design` and
`regression-sensitive`. This skill produces none of them: its deliverable is a prose piece and a
four-line note, and half its procedure — routing, linting, revising — is judging rather than
building, a class the corpus does not speak to and for which `lane_pick.py` returns the policy
answer unchanged. **[docs]** "Avoid using prompts that ask the model to perform a task for which
it has a known, fundamental limitation" has no row to fill here, so abstaining is honest.

## What transfers intact

- **The Gemini dialect is already written, from the same sources.** `dialects.md` carries the
  objective-constraint rule, the categorical count, the named verification step, constraints
  first, long context first and task last, one delimiter family, one task per prompt — each
  quoted from Google. Follow it as the skill's own content; nothing below contradicts it.
- **The lint is a real gate with a two-way control, and the rule that inverts is already a
  flag.** `[measured-here]` `--self-test` runs 18 fixtures, exit 0, checking both directions:
  `uncounted categorical: fails as expected` sits beside `categorical as subject only warns:
  clean as expected`. A gate proven able to fail is the `gate` module's hardest rule, shipped.
  And `--target gemini` keeps the verification step where `--target claude` hard-fails it.
- **The package does not shout.** `[measured-here]` 14 emphasis tokens across `SKILL.md` and the
  rule files, every one a mention — Anthropic's `CRITICAL: You MUST` line, cited as the register
  to replace. **[docs]** Where escalating language is used rather than cited, "foundation model
  performance will no longer improve and in many cases will get worse". Add none.
- **Several targets are already counts**, which is why they survive on this family: 15 and 30
  lines, 72 characters, 220 words, 300 lines in `agent-voice-lint.json`; 1–6, 5–20, 1–4 and 2–4
  lines in the registers. **[docs]** "Avoid using subjective or relative qualifiers that lack a
  concrete, measurable definition." These already are.
- **The counterweight protects you from your own default.** **[docs]** "By default, Gemini 3
  models provide direct and efficient answers." Brevity is the resting state here, so the base
  layer's rule that uncertainty, risk and verification-that-happened are content and never
  trimmed is what keeps a short piece from becoming a wrong one.

## C1 — the quota ledger, and why the scan came back nearly empty

`[measured-here]` `scan_skill.py` over `SKILL.md` and its four binding references (1,155 lines)
returned **25 categorical rows**. I bound **2** and dropped **23** as prose: 12 are the skill
quoting the measured Gemini failure back at its reader (`all surfaces` → 5, `all states` → 1), 6
are entries in the lint's own ban lexicon or the field guide's list of tells, 3 sit inside
`dialects.md`'s worked example, and 2 are prose in the evidence file. `qual skills 0` — the skill
composes no other skill, so there is no chain to convert.

`[derived]` The near-empty ledger is the finding: this package practises what it teaches, and its
remaining uncounted scopes are ones the regex cannot see, because their nouns are `rules`,
`pieces`, `cuts` and `registers` rather than surfaces and states. Write this table into the run
before drafting and report the fractions in Step 6; filled here from a revision of one 150-line
instruction file that also needed a reply:

| Scope, and where the skill states it | Denominator | Filled | Delivery line |
|---|---|---|---|
| `for every rule, ask whether a model could satisfy it and still produce something the author would reject` — SKILL.md:108–110 | rules in the file = **31** | 31 asked, 6 rewritten | `31/31 rules tested, 6 rewritten` |
| `Quote the evidence for any claim about a check` — SKILL.md:72 | claims about checks in the piece = **4** | 4 with pasted output | `4/4 claims carry their command` |
| `A request spanning registers is several pieces … route each and produce both` — SKILL.md:57–58 | registers the request spans = **2** (`skill`, `reply`) | 2 drafted, 2 linted | `2/2 pieces, each at its own format` |
| `Report what you cut and why` — SKILL.md:105 | cuts made = **9** | 9 named, grouped into 3 reasons | `9 cuts, 3 reasons, 0 caveats removed` |
| Every rule traces to a quoted line or a measurement — SKILL.md:173–175, `evidence.md:4` | rewritten rules needing a source = **6** | 5 sourced, 1 marked inference | `6/6 tagged: 5 sourced, 1 [Inference]` |
| The delivery note's own items — SKILL.md:146–148 | 4 cells | 4 | `4/4, nothing padded` |

**[measured-family]** Why cells rather than the sentence: on the recorded run every *enumerated*
requirement shipped — twelve named features — and every *categorical* one shipped once or not at
all. **[docs]** "make each step a prompt and chain the prompts together in a sequence" is how the
rows get filled: the count is read off the file first, then the rules are tested against it.

## `bounded-constraint` — the length target warns, it does not gate

This module fired on 7 triggers and matters most here, because this skill is almost entirely
bounds. **[measured-family]** On the 106-task bench, 58% of Gemini's failing UI assertions at
`medium` and 86% at `high` stated a bound rather than asking for a thing, against 8% for opus —
and the most-repeated rule failed on *every instance in its set* on a run that passed 37 of its
39 other assertions. A bound is violated by what you did not write, so it survives every check
that looks at what you did. `[measured-here]` And here the check does not catch it: a 40-line
reply linted at `--format reply` returns `warn 40 lines exceeds the 15-line target for 'reply'`,
then `RESULT: clean on the hard checks`, **exit 0**. The length bound is advisory in every
register, so the exit code is not the readback — the `info` and `warn` lines are. Fill this
before delivering, one row per bound that applies to the piece you actually wrote:

| Bound | Where it is stated | Readback | Observed | Within? |
|---|---|---|---|---|
| reply ≤ 15 lines (register target 1–6 for a plain question) | `agent-voice-lint.json` `formats.reply`; `terminal-reply.md:20` | the lint's `info N words, M non-empty lines` | 4 lines | yes |
| skill ≤ ~300 lines | `formats.skill`; `skill-and-instruction.md:65` | same `info` line | 150 lines | yes |
| commit subject ≤ 72 chars, no full stop | `formats.commit` | `awk 'NR==1{print length($0)}' msg.txt` | 58 | yes |
| delivery note 2–4 lines | SKILL.md:146 | `grep -c . note.md` | 4 | yes |
| one landing line per document | `agent-voice.md:173`; `ai-writing-signs.md:188` | count sentence-final quotable resolutions by hand | 1 | yes |
| one delimiter family per document | `agent-voice.md:141` | `grep -c '^<' draft.md` beside `grep -c '^#' draft.md` | 0 XML, 6 headings | yes |

Report `N of N bounds within limit`. **[docs]** Google treats these as a component in their own
right — "Restrictions on what the model must adhere to when generating a response, including what
the model can and can't do." — and the Recap component is where they go: a "Concise repeat of the
key points of the prompt, especially the constraints and response format, at the end of the
prompt." `[derived]` The table is that recap, carrying values instead of restating the rule. And
the trap worth naming: a bound written as a prohibition reads as taste. `no closing flourish` and
`never congratulate yourself` are counted properties the lint reads back; `prose by default` and
`one name per thing` are not. Convert the ones you rely on into a row rather than agreeing.

## C2 — verification is asked for, and the receipt is the output, not a sentence

**[docs]** "Include specific verification steps in either the system instructions or your prompts
directly", and from the agentic template, "Review your output against the user's task."

`[derived]` This reverses the house style deliberately: removing verification scaffolding is
correct for a model that over-verifies, and inheriting that removal here is the defect — though
this package is the one place where the reversal is already a flag rather than an argument.
**[measured-family]** What fills the vacuum is well-formed and false — a review naming a browser
engine that failed all four invocation attempts and never ran, a 100% contrast pass from a probe
never executed, and a deterministic auditor returning `0 error(s)` over an artifact whose two
prerequisite steps never happened.

Three receipts, and `check_package.sh` is the one the procedure does not name. Paste output, not
a claim about it, filled here from this session:

```
GATES — plugins/agent-voice/skills/agent-voice/
  agent_voice_lint.py --format skill --target gemini   exit 1   2 hard issue(s)
                      unmeasurable qualifier "robust" line 1; "thoroughly" line 1
                      re-run after fix                 exit 0   clean on the hard checks
                      warn: 40 lines exceeds the 15-line target for 'reply'  → bound ledger
  agent_voice_lint.py --self-test                      exit 0   18 passed, 0 failed
  check_examples.sh                                    exit 0   14 example(s) clean, 0 failing
  check_package.sh                                     exit 1   checks 1-3 pass; check 4 reports
                      35 quote(s) verified verbatim, 47 unverified (1 source file on disk)
                      REPORT SAYS: vendor quotes NOT fully checked — 3 of 4 sources absent
```

A denominator of zero is a gate that never ran, never a pass. `[measured-here]` **Read the exit
code, not the output** — piping `check_package.sh` through `tail` here returned status 0 while
the script itself exited 1 and its last line read `PACKAGE: at least one check failed.` Run it to
a file and echo `$?`. And name the axis the work is ungated on when a check could not run: check
4 skips when the vendor source copies are absent from `/tmp`, so a clean-looking package run can
mean the quotes were never verified.

## C7 — load, then answer, as two ordered steps (Step 1)

`Load references/agent-voice.md (always, the base layer) plus the one matching register file` is
SKILL.md:39, and it is the load this family skips. **[measured-family]** On `COD Dossier`, asked
a question naming three skills, the run answered from internal memory without loading any of
them; asked to fix that, it inverted the error and launched a skill instead of answering. The
same shape here is a draft written from a general sense of good writing, with the register file's
length target and hard-fail list never opened — and the inverse is running the lint instead of
producing the piece. `[derived]` Step 1's routing decision is its only artifact and Step 5
consumes it twice, so write it down where a skipped load shows:

```
ROUTED  register: skill-and-instruction   lint format: skill   target family: gemini
LOADED  references/agent-voice.md (236 lines)  references/registers/skill-and-instruction.md (150)
TARGET  under ~300 lines, from skill-and-instruction.md:65
```

`--format` has to be the routed register's key and nothing else: a wrong key runs a different set
of hard checks and still exits 0, a green gate over an unchecked piece. `--target` names who
*reads* the piece, not who wrote it — a Gemini runner drafting a `CLAUDE.md` for an Opus reader
passes `--target claude` — and it defaults to `claude`, so state it every time.

## `authorship` — the drafting pass gets the substance and nothing else (Steps 2–3)

The skill's own line is `The characteristic failure of this whole skill is a well-voiced piece
that invented its own completeness` (SKILL.md:78–79). **[docs]** Google supplies the mechanism as
a system instruction meant to be used verbatim, and its last clause is the operative one: "If the
exact answer is not explicitly written in the context, you must state that the information is not
available." Also "Do not assume or infer from the provided facts; simply report them exactly as
they appear." `[derived]` So run Step 3 against the Step 2 substance list alone — what happened,
what was observed, what the reader now owns, what is open — rather than against the transcript's
atmosphere, and write a missing item as missing. One carve-out: a ratio you computed from two
observations is *your* claim, so it carries how it was derived rather than the source's authority.

## `delegation` — the fork is a closed set, and this skill spawns nothing

`[derived]` This module fired on 3 triggers, all subject matter: the `brief` register teaches
delegation, the skill performs none. So the cap is **zero subagents for a run of this skill** —
routing and drafting one piece is a handful of reads, and a summary loses the sentences Step 3
needs to quote. The half that lands is the closed set. **[docs]** On a model that answered
correctly but "didn't stay within the bounds of the options", the remedy is that "you can
rephrase the instructions as a multiple choice question and ask the model to choose an option".
Step 1 already is one — seven registers, one of them — and so is `--target` with five values.
Write the chosen value down (the `ROUTED` block), and resolve a request straddling two registers
by producing two pieces rather than one hybrid.

## C3 and C5 — the retry ceiling, and one worked piece before the set

**[docs]** "you must change your strategy or arguments, not repeat the same failed call."
**[measured-family]** Four consecutive invocations of one absent tool with nothing changed
between them, and four consecutive `Read` calls against a hard token ceiling before pivoting. Two
attempts per command, then change approach; a permanent error gets one. `Fix and re-run until
clean` (SKILL.md:132–133) means editing the draft between runs — a second identical invocation
over an unedited file is the loop, not the fix. **[docs]** And "you can remove instructions from
your prompt if your examples are clear enough in showing the task at hand": where a request spans
registers, author the first piece at full fidelity — drafted, linted, bound ledger filled —
before starting the second, and treat it as the exemplar.

## `thinking_level`, and where the brevity default bites

**[docs]** `HIGH` is "suitable for complex prompts requiring deep reasoning, such as multi-step
planning, verified code generation, or advanced function calling scenarios", and Gemini 3.7 Flash
defaults to `MEDIUM`. `[derived]` Revising a long instruction file — 31 rules tested one by one
against the satisfiable-and-still-wrong question — is that shape; drafting a four-line terminal
reply is not, so raise the level for the `skill`, `brief` and `doc` registers and leave the
default for `reply`, `commit` and `review`. **[measured-family]** Raising it is not a remedy for
anything above: paired across 106 tasks, `high` beat `medium` on 24, lost on 24 and tied on 58,
mean −1.7 points. **[docs]** It does change tool volume — "Higher thinking levels encourage the
model to use more tools to explore and verify, so lowering the level can reduce tool calls." And
"If you need a more conversational or detailed response, you must explicitly request it in your
instructions" is where the brevity default bites: `[derived]` `brief` and `doc` have no brevity
rule by design, an underspecified brief is the expensive failure, and on those two the register's
floor is what to follow while the resting state is what to override.

## Modules deliberately not written

The scan fired four at the three-trigger threshold — `authorship`, `bounded-constraint`, `gate`,
`delegation` — all above. Six did not. **`visual`**: the skill renders nothing. **`states`**: it
enumerates registers, not unhappy paths. **`platform-values`**: it cites vendor *prose*, quoted
verbatim into `evidence.md` with a verifier behind it, rather than numeric platform metrics.
**`injection`**: the text it ingests is the user's own draft. **`count-contract`**: its counts
are folded into the bound ledger. **`emphasis`**: 14 tokens, all mentions inside citations.
