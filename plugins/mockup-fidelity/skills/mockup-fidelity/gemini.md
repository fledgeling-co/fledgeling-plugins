# Running `mockup-fidelity` on Gemini

Read this once, whole, before the SKILL.md — every override names the section it lands on.
**[docs]** the health checklist warns against a prompt "with non-linear logic or
conditionals that require the model to piece together fragmented instructions from multiple
different places in the prompt", which is what a conditional side-file becomes unless it is
read up front.

The canon transfers; the assumption that a rule stated in prose gets executed does not. This
skill's central promise is categorical — **every** element of the mock lands in one of three
states, present, divergent or absent — and a categorical promise collapses to whatever
happened to get looked at, producing a ledger of agreements that reads complete.

## Epistemic status

| Tier | Here | Meaning |
|---|---|---|
| `[docs]` | throughout | Google published it; verbatim from `geminify/references/gemini-corpus.md` |
| `[measured-family]` | **n=1** | one recorded Gemini run of *other* skills, 17 Aug 2026 |
| `[measured-here]` | **none** | no Gemini run of `mockup-fidelity` exists |
| `[derived]` | yes | my reasoning from the above, marked as such |
| `[target-measured]` | yes | this skill's own harness numbers, from its `EVALS.md` (18 Aug 2026) — facts about Obscura and `capture.mjs`, carrying no evidence about Gemini. Outside geminify's four tiers, named so it cannot be mistaken for one. |

**Unmeasured on this skill.** Never observed of Gemini running it: whether the Phase 3A
ledger gets filled for every affordance or only the first few; whether `inconclusive` is
read before `findings` with the nine `reason` strings relayed verbatim; whether the exit
code is quoted rather than an impression of the report; whether an authored justification
passes as a citation under THE LAW rule 5 (`EVALS.md` names it as the prompt that would
settle this, and records that none of its eight eval prompts has run on any model); anything
about React Native, Metro/CDP or a real browser engine; and whether these overrides help at
all.

## What transfers intact

- **The three-valued vocabulary** (SKILL.md:379-386) — `DEFECT` / `INTENTIONAL — <citation>`
  / `INCONCLUSIVE — <capability>` / `✓ fixed+reverified` is already the slot a "could not
  run" needs to survive in; most skills have none.
- **The exit code as the gate** (SKILL.md:204) and **the artifact precondition**
  (SKILL.md:192-202) — "no artifact, no verdict" is a precondition, not an exhortation.
- **The untrusted-content sentence** opening every sub-agent brief (SKILL.md:417-418): the
  delimited-data guard Google's structured template prescribes, already written.
- **Reference immutability** (SKILL.md:312), and **the two ask gates** (SKILL.md:64-74):
  **[docs]** the agentic template prefers "calling the tool with the available information
  over asking the user" on low-risk reads, which is the rest of this skill — these two are
  the genuinely high-risk cases.

## C1 · The quota ledger — 15 categorical scopes, each with a number

**[docs]** From the checklist under **Ambiguity**: "Avoid using subjective or relative
qualifiers that lack a concrete, measurable definition."

**[measured-family]** n=1: a run delivered 12 of 12 *enumerated* features, and of the
requirements named categorically, "all states" → 1, "all menus" → 0, "all flows" → 0. The
enumerated ones all landed.

That is this skill's exposure, at SKILL.md:322 — *for every affordance the reference shows,
mark its state in the target*. Write this into `.mockup-fidelity/LEDGER.md` **before** the
first capture; a scope with no number gets satisfied once. Fifteen scopes bind; the eight
that gate a verdict are tabled, and seven more (all 7 phases at SKILL.md:266, surface→file
map, control anchors, content-store findings, fan-out items, per-row why, per-control
states) take the same shape.

| Categorical scope (line) | Number | Report as |
|---|---|---|
| `Every capture` probes per detector class — 130 | 9 classes | `9 probed · R ran · S silenced` |
| `Inventory EVERY frame` — 244 | F frames, incl. every `· empty` / `· dark` / `(sheet)` suffix | `F frames · A audited · X excluded with reason` |
| `Every screen`'s measurement on disk — 197 | 4 artifacts × A | `4A of 4A` |
| `each cell` from structure artifacts — 323 | C affordances per frame | `C of C cells, 0 TODO` |
| every mock affordance class — 232-236 | **11** named: header element, button, card, section, eyebrow, badge, chip, search field, meaningful icon, list row, CTA | `11 of 11 swept per frame` |
| `every element` the app renders that the mock does not — 254 | E per matched region | `E extras across R regions` |
| `each control` × `each state` probed — fidelity-probe.md:5,15,22 | C × S | `C×S probes, 0 unopened` |
| `Every cell` / `every row` cites two artifact values — 199, 441 | Rw ledger rows | `Rw of Rw cite artifacts` |

**The exemplar, filled** — the skill's own shipped fixture pair, so these are real numbers.
`[target-measured]`, from `EVALS.md`:

```
screen   evals/fixtures/reference.html → target-10-defects.html
frames   1 of 1 audited · 0 excluded          artifacts  4 of 4 on disk
classes  9 probed · 0 ran · 9 silenced        findings   49 (26 high)
planted  10 · caught 8 · inconclusive 2 · false pass 0
score    83 — not quotable bare: scoreCovers.fraction = 0
exit     3 (inconclusive), not 0
```

**[docs]** The same **Ambiguity** entry is why the last three lines matter: a number without
its denominator is a relative qualifier wearing a digit, and 83 beside nine closed shutters
reads as 83% right.

`count-contract` (3 hits) extends this rather than taking a section: **derive** the count
when the brief omits one — three named screens still have F frames, C affordances and S
states, taken from the reference, not the request — and **cover the cells**, not the
top-level items.

## C2 · Verification is asked for, not assumed

**[docs]** "Include specific verification steps in either the system instructions or your
prompts directly", and from the agentic template, "Verify your claims by quoting the exact
applicable information (including policies) when referring to them."

**[measured-family]** n=1: the same run wrote itself a review naming a browser engine that
failed all four invocation attempts and never ran, and a 100% contrast pass rate from a
probe never executed. Measured after: every primary button 3.65:1, one glyph at 1.00:1.

SKILL.md:211-213 already forbids this — a tool that cannot run is a blocker to report,
quoting what the tool said. Mechanically:

- Every number carries its command and that command's pasted output; no output, no number. A
  denominator of zero is never a pass — `scoreCovers.fraction = 0` means the score is about
  nothing.
- Relay each `reason` string byte-for-byte (SKILL.md:136-140). A paraphrase is how "this
  layer cannot run here" becomes "the shadows match".
- **This engine cannot return 0.** `[target-measured]` all nine probed classes are silenced
  on Obscura 0.2.0, so `--assert` exits 3 even on a byte-identical control. The honest
  verdict is INCONCLUSIVE with nine ledger rows; a report claiming exit 0 here is fabricated
  by arithmetic.

`[derived]` This reverses the house style deliberately. Stripping verification scaffolding
is right for a model that over-verifies; inheriting that removal here is the defect.

## C3 · Two attempts per tool · C4 · Passes, not one sweep

**[docs]** "you must change your strategy or arguments, not repeat the same failed call."
**[measured-family]** n=1: four consecutive invocations of one absent, repo-banned tool with
no change between them, then a review asserting it had run.

Two attempts on `capture.mjs`, `obscura serve`, `axe describe-ui` or a Metro CDP attach; a
permanent error (`command not found`, a `--help` that errors) gets one; then file the
blocker. `feature-check.mjs` gets **zero** against an Obscura capture — its verdict inverts.

**[docs]** Under **Too many tasks**, "Break the requests into separate prompts", and the
remedy, "make each step a prompt and chain the prompts together in a sequence." The phases
are that chain: breadth ledger, then structure, then style (SKILL.md:221-236). One sweep
satisfies the first axis and reports the rest clean.

## C5 · One worked screen first · C6 · `thinking_level`

**[docs]** "We recommend to always include few-shot examples in your prompts", and under
**Missing output format specification**, "use a clear, explicit instruction to specify the
format and show the output structure in your few-shot examples." Audit **one** frame end to
end — inventory row, 4 artifacts, filled 3A ledger, structure and style findings, quoted
exit code, functional-gaps row — as the exemplar; a later frame with a shorter ledger was
not audited. **[docs]** `HIGH` "Allows the model to use more tokens for thinking and is suitable for
complex prompts requiring deep reasoning, such as multi-step planning, verified code
generation, or advanced function calling scenarios." Gemini 3.7 Flash defaults to `MEDIUM`;
`[derived]` this skill is all three of those at once, so run it at `HIGH`.

## C7 · Recall is not a source — capability facts included

**[docs]** "Your knowledge cutoff date is January 2025." **[measured-family]** n=1: a run
put Windows 10's published accent colour on a Windows 11 surface — not a guess, a
previous-generation published value returned confidently.

`platform-values` fired (3 hits) and folds in here, because this skill reads token values
rather than recalling them (SKILL.md:289-293). The live version of the risk is engine
capability, and `references/engine-capability-matrix.md` says so itself: every row is a
measurement, not an architectural truth. So read `summary.capabilities` off the run you just
did — never from memory of the matrix, which is one reading, 18 Aug 2026, Obscura 0.2.0.

## Module `visual` (14 hits — the highest of any target scanned)

**[docs]** "Ask the model to describe the images before performing the task in the prompt."
"To improve the response, point out which parts of the image are most relevant to the
prompt." And on a failure: "A prompt can fail because the model did not understand the image
at all, or because it did not perform the correct reasoning steps afterward."

The skill is stricter and right to be — SKILL.md:168-170 puts frontier multimodal recall
near 40% on fine-grained UI differences and under 23% on hard cases. So a screenshot never
closes a row; it is the trigger to go and measure, and every `✓` cites two artifact values.
The capture denominator is frames × gated states, all opened in one session
(fidelity-probe.md:22), fraction reported. Describe a crop before judging it, Set-of-Marks
numbering on both images first (SKILL.md:172); when a finding looks wrong, ask what is in it.

## Module `gate` (9 hits)

**[docs]** Under **Non-standard data format**: "When model outputs must be machine-readable
or follow a specific format, use a widely recognized standard like JSON, XML, Markdown or
YAML that can be parsed by common libraries." And on arithmetic, Gemini's "code execution
tool enables the model to generate and run Python code, and should be enabled whenever the
model needs to perform any kind of arithmetic, counting, or calculation."

Paste the harness output; cite fields of `target.findings.json`, not impressions of it, and
print the denominator with every fraction. **Prove the gate can fail before trusting it
passing** — `[target-measured]` the fixture pair is that control, 0 findings on the
byte-identical target and 49 on the ten-defect one; uniform numbers across varied inputs are
the signature of a predicate matching nothing. `--allow-inconclusive` is unavailable until
every silenced class has a ledger row naming where it was confirmed in a real browser, and
by whom (THE LAW rule 7).

## Module `states` (4 hits)

**[docs]** Under **Underspecified task**: "provide instructions for handling missing data
rather than assuming inserted data will always be present and well-formed."

**[measured-family]** n=1: 1 of 6 named states delivered, and zero focus, active or disabled
rules — from a skill that named the six *and* stated a completeness condition in prose.
`[derived]` So a frame suffixed `· empty`, `· dark`, `(drill-in)`, `(sheet)` or `Composer`
is its own inventory row with its own four artifacts; SKILL.md:244 already bans "minor
sub-state of X" as a reason to drop one, and that ban has to become a row count to survive.
A conditionally rendered element is graded only in its **populated** state — unreachable
means `pending`, never `✓` (SKILL.md:439-440).

## Module `delegation` (9 hits)

**[docs]** On a model that answered correctly but "didn't stay within the bounds of the
options", the remedy is to rephrase as multiple choice.

**Cap the fan-out**: SKILL.md:409 says waves of ≈5, a ceiling never widened to finish
sooner. **Never delegate a check of your own output** — the completeness critic in
`references/measurement-enforcement.md` works because it is blind to the app and the mock.
Resolve every fork the skill offers (auto-fix vs reviewed plan, embed vs StyleX, sequential
vs N-lane) to one option written into `PROJECT.md` before work starts, and carry THE LAW and
the preflight rule into every brief (SKILL.md:420) — the sub-agent cannot see this file.

## Module `authorship` (8 hits)

The ledger and the functional-gaps doc leave the terminal and become tickets (SKILL.md:388),
so a reader acts on them. **[docs]** adopt the last clause of Google's strictly-grounded
system instruction verbatim for both: "If the exact answer is not explicitly written in the
context, you must state that the information is not available."

`[derived]` The context is the artifact set, so a `Current state` cell you cannot draw from
an artifact reads `not measured`, not `visual only`. THE LAW rule 5 is the same rule from the
other side: if the only thing backing "intentional" is your own reasoning, it is a `DEFECT`.

## Module `emphasis` (10 tokens)

The SKILL.md shouts — `⛔ THE LAW`, `MANDATORY`, `EVERY`, `banned`. Read those passages as
plain rules of equal weight to the rest, and give the capitals no extra force. **[docs]**
under **Overt manipulation**, escalating instructions no longer help: "foundation model
performance will no longer improve and in many cases will get worse". Also "Avoid
unnecessary or overly persuasive language."

`[derived]` The trap is urgency read as a substitute for the run: THE LAW's capitals do not
make the breadth ledger exist, filling 40 cells does. Nor reproduce the register downstream —
briefs, ledger rows and ticket text get plain declaratives.

## What I did not write, and why

- **`injection`** did not fire and gets no section: the skill already ships the guard
  sentence at SKILL.md:417-418, listed under *transfers intact*. **`platform-values`** fired
  (3 hits) and folds into C7, because a separate section would restate the core on a skill
  that reads values rather than recalling them.
- **35 categorical candidates scanned; 15 bound, 20 dropped as prose** — anti-pattern
  narration (*measuring one element's pixels exhaustively*, SKILL.md:95), doc-about-the-doc
  lines (`issue-to-check-map.md:4`), quoted mock copy, critic-prompt wording. The 308
  distributives the scanner counted but did not list went unreviewed.
- **Nothing in the skill was changed.** One item belongs to `improve-skill`: `EVALS.md`
  records that `grade.py` reads `out-old/` and `out-new/` directories existing nowhere in the
  repo, so the answer key cannot be invoked as shipped.
