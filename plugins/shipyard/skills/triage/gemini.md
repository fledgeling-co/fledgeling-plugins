# gemini.md — `triage`

Read this once, now, then read `SKILL.md` and its two references and run the stage as written.

`triage` is the pipeline's readiness gate, and almost everything it emits is **prose a human acts
on**: a verdict, a surface inventory a designer mocks from, an assumptions block whose whole purpose
is that an owner can veto a default knowingly. Nothing here compiles. What makes it the hardest
shape in this plugin for this family is that its most load-bearing rules are stated as prohibitions
— no file paths, no code identifiers, no architecture nouns, no lane accounting in the owner-facing
section — and a prohibition is a bound. Bounds are the measured failure direction. So the shape to
design against is a well-formed, confident triage section that reads like process notes, names three
of five touched surfaces, and cites a brief nobody can open.

## Epistemic status

- **Tiers used:** `[docs]`, `[measured-family]`, `[derived]`. No `[measured-here]` — **no Gemini run
  of `triage` has been observed**, at any tier. The `[measured-family]` sources are two single
  sessions (n=1 each) and a 106-task benchmark, in `geminify/references/evidence.md`.
- **The tier the evidence is about.** Every measured rate below was observed on `gemini-3.7-flash`
  (one session on `gemini-3.7-flash-high`) — **flash-tier claims, not to be projected onto the Pro
  tier.** **[docs]** The defaults drift inside the family: *"If thinking_level is not specified,
  Gemini 3 will default to high."* against, from the 3.5 Flash release notes, *"The default thinking
  effort is now medium, changed from high in Gemini 3 Flash Preview."* On Pro these overrides stand
  as `[docs]`-grounded discipline; every `[measured-family]` number is an open question.
- **Unmeasured on this skill:** **both measured sources watch a model *build* something; neither
  watches one review a spec**, so nothing here predicts verdict quality — the overrides are about
  the artifact's completeness and grounding, where the evidence does speak. Also unmeasured: the
  bound-following rate was observed on UI assertions, so its transfer to a word budget and a ban
  list is `[derived]`; and no run has been measured *with* a `gemini.md` against one without.
- **The self-limitation.** **[docs]** A conditional side file is the shape the health checklist
  warns about: *"Avoid writing a prompt with non-linear logic or conditionals that require the model
  to piece together fragmented instructions from multiple different places in the prompt."* Read it
  in one pass, before step 1, never mid-verdict.

## No route-out block, and which shapes were omitted

**[docs]** The health checklist says it outright: *"Avoid using prompts that ask the model to
perform a task for which it has a known, fundamental limitation."* No shape can honestly be named
here. This skill writes no code and `Never writes an implementation spec`; the four shapes the
corpus measured far enough behind to route — `static-page`, `brownfield-integration`,
`visual-design`, `regression-sensitive` — all describe *producing* an artifact, and `lane_pick.py`
returns the policy answer unchanged for `referral` anyway. `visual-design` is the closest near-miss
and still wrong: the UI & logic preview names surfaces in words for a designer. The one lane that
does bind is the skill's own — step 6's out-of-family review, `codex gpt-5.6-sol` at `medium` →
`agy` → `grok`. `[derived]` A Gemini agent here should **skip the agy lane**, since the point of
that gate is a reviewer outside the author's family and agy is inside yours; if codex and grok are
both down, record the fallback as a downgrade exactly as the skill already requires.

## What transfers intact

Three of this skill's rules are already written the way this family needs, and the overrides give
them denominators rather than new wording.

- **The essential-gap bar is a three-part AND with a stated default** — no safe internal default ·
  expensive to undo · genuinely the human's — and `Fail any one → it is internal`. **[docs]** The
  multiple-choice remedy: *"The response is correct, but the model didn't stay within the bounds of
  the options."*
- **`assuming X (rather than Y)`** forces every default to name what it beat — grounding stated as a
  format rather than an exhortation.
- **`Don't fabricate regulatory requirements`**, with its remedy of flagging a rule as needing Legal
  confirmation rather than asserting it, is **[docs]** the strictly-grounded instruction's last
  clause in this domain's words: *"If the exact answer is not explicitly written in the context, you
  must state that the information is not available."*

## The scan

`scan_skill.py` over `SKILL.md` and both references (489 lines): **12 quota candidates, 1 bound row,
46 relative qualifiers, 0 qualitative skill references, 0 shouted passages.** I bound **7** of the
10 listed rows into the six ledger rows below (rows 5 and 6 of the scan share a row, since both tag
the same finding set) and dropped **3** as prose — `the whole item` in the bias-to-push-through
rule, `every check it had passed all four` inside the brief-citation incident narrative, and `each
screen` inside a worked BAD example. The 46 relative qualifiers are the real finding on this target
and are handled in override 3 rather than listed.

Modules fired: `authorship` (6), `visual` (4), `bounded-constraint` (4). **`visual` is dropped and
not written**: all four hits are the UI & logic preview's vocabulary — surface, screen, mobile,
design reference — prose naming what a *designer* will later mock. This stage opens no capture and
judges no crop. Its one visual-adjacent rule, `(measured: <browser evidence>)` versus `(assumed from
source)`, is about what a claim may rest on and lands in override 2. `emphasis` did not fire.

## Override 1 — the quota ledger (steps 3–8, `spec-format.md` §UI & logic preview)

**[docs]** *"Avoid using subjective or relative qualifiers that lack a concrete, measurable
definition."* **[measured-family]** Why this is override 1: one run delivered **12 of 12**
requirements a brief *enumerated* and satisfied every requirement named *categorically* with one
instance or none — all surfaces → **5**, all states → **1**, all menus → **0**, all flows → **0**
(§1.1.1, n=1). Row 4 below is that failure with the roles swapped: the skill says `do not collapse
touched surfaces into one line, and never drop a touched surface to save space`, and its stated
consequence is `an unnamed surface is a screen the designer won't mock`. Write this before step 8,
report the fractions in the machine trailer and never in the owner-facing section; filled against a
three-surface feature, as the exemplar the rest are measured against:

| # | categorical, in the skill's words | denominator | filled | reported |
|---|---|---|---|---|
| 1 | `Locate every component, page, service, route the brief references` | 9 named surfaces | 8 located, 1 ambiguous match flagged | `8 of 9, 1 ambiguous` |
| 2 | `any claim about what the app currently shows` carries its tag | 6 on-screen claims | 2 `(measured: …)`, 4 `(assumed from source)` | `6 of 6 tagged` |
| 3 | `any surface inventory` lands in the verdict for the design stage | 3 surfaces + `platforms:` line | 3 carried, platforms line carried verbatim | `3 of 3` |
| 4 | `name every surface that changes`, one line each on what it gains | 3 surfaces | 3 lines: editor, slide builder, new report | `3 of 3 — 0 collapsed` |
| 5 | `Attribute each finding to its lens` and `Tag every finding` C/H/M/L | 11 findings | 11 lens-tagged; 2 High · 6 Medium · 3 Low | `11 of 11 tagged twice` |
| 6 | `For any path that mutates tenant data`, what an auditor must see | 4 auditable actions | 4 listed as plain inventory, no code refs | `4 of 4 inventoried` |

A cell that cannot be filled reads `n/a: <reason>` — **[docs]** *"provide instructions for handling
missing data rather than assuming inserted data will always be present and well-formed."* Row 4 goes
first: it is the row whose failure is invisible to every other check in the pipeline, because a
one-line preview reads as concise rather than as incomplete.

## Override 2 — a claim may not exceed its source (steps 3, 6, 8; `spec-format.md` §brief citation)

**[docs]** Google's strictly-grounded system instruction is meant to be used verbatim where output
must not exceed its sources, and its last clause binds here: *"If the exact answer is not explicitly
written in the context, you must state that the information is not available."* Also *"Your
knowledge cutoff date is January 2025."*, with the remedy *"Grounding with Google Search connects
the Gemini model to real-time web content, and should be enabled whenever the model may need to know
obscure or recent facts."*

**[measured-family]** Two shapes to design against. One run asserted a browser engine as verified
when it had failed all four invocation attempts and never ran, and a `100% pass rate on contrast`
from a probe never executed (§1.1.2, n=1) — a *shape* completed where the procedure was not. The
same run wrote **Windows 10's `#0078D4`** accent into a Windows 11 artifact: not a guess, a
previous-generation published value returned confidently (§1.1.4). A regulatory clause recalled the
same way would land in a triage section as fact. Four consequences for what this stage writes:

- **A surface claim is tagged or it is not made.** `(measured: <browser evidence>)` means a browser
  ran; anything else is `(assumed from source — verify before building on it)`, because `a false
  grounded claim in an Essential Question gets a confidently wrong answer the whole pipeline then
  builds on`.
- **A regulatory rule is read or flagged, never recalled** — `Needs Legal confirmation` is the
  admissible output when you are unsure a rule applies.
- **The brief citation resolves.** Take `<sha>` from `git log -1 --format=%h -- <path>` before the
  commit that deletes the file, never `git rev-parse --short HEAD`. One repository shipped four
  specs citing briefs the same commit had deleted and every check it had passed all four, `because
  presence and resolution are two claims and it only made the first`.
- **The gate accounting is a paste, not a claim.** Step 6's out-of-family review is a real
  invocation: wire-verified header lines, a **non-empty** output file, the accept/reject tally.

```
$ perl -e 'alarm shift @ARGV; exec @ARGV' 900 codex exec -m gpt-5.6-sol \
    -c model_reasoning_effort="medium" -s read-only -o /tmp/so-dio0412.md "<packet>" < /dev/null
  header  'model: gpt-5.6-sol' ✓   'reasoning effort: medium' ✓   /tmp/so-dio0412.md 3.4 kB ✓
  verdict 5 findings → 3 accepted (edited), 1 rejected (out of scope for triage), 1 escalated → EQ-2
$ grep -RIl 'ANTHROPIC-ONLY\|NO EXTERNAL MODEL CLIS' CLAUDE.md AGENTS.md  → no match (egress permitted)
```

`an absent or empty output file is a lane failure, not a quiet pass` — the skill's own rule, and the
reason the byte count sits on the header line.

## Override 3 — the bound ledger, and the ban list is a bound (Hard rules, `spec-format.md`)

**[measured-family]** This is the override the evidence points at hardest for this target.
Classifying every failing UI assertion by whether it states a **bound** (`exactly N`, `no`, `not`,
`only`) or asks for a **thing**: **58%** of Gemini's failures at `medium` and **86%** at `high` were
bound-shaped, against **8%** for opus and **6%** for the OpenAI lane; one rule failed on *every*
instance in its set on a run that passed 37 of its 39 other assertions (§2.2). A bound is violated
by what you did not write, so it survives every check that looks at what you did — and this skill's
central rules are bounds wearing prohibitions' clothes.

**[docs]** Google treats constraints as a component in their own right — *"Restrictions on what the
model must adhere to when generating a response, including what the model can and can't do."* — and
places them in the **Recap**: *"Concise repeat of the key points of the prompt, especially the
constraints and response format, at the end of the prompt."* Read each back off the written section,
not off the rule:

| bound, in the skill's words | countable property | readback | observed | within? |
|---|---|---|---|---|
| the ban list — no file paths, identifiers, library or architecture nouns | banned tokens in the triage section | grep the section for `.tsx`, `/`, `endpoint`, `schema`, `module`, `route` | **2** (`endpoint`, `route`) | **no — rewrite both** |
| the owner-facing section holds `zero commands, zero tool names, zero lane accounting` | accounting lines in the owner section | grep for `$ `, `codex`, `agy`, `verdict:` | 0 (all in the trailer) | yes |
| `Assign exactly one tier` | tiers named | count `S0..S3` in the verdict | 1 (S2) | yes |
| `≤15 words per assumption, ≤10 per rationale` | over-budget lines | word-count each assumption line | 6 of 7 within; 1 at 19 | **no — split row 5** |
| `≤6 words` short title · id zero-padded to **4 digits** | title words · id shape | read the ledger row back | 5 words · `DIO-0042` | yes |
| `up to ~3 short lines` of behaviour changes | behaviour lines | count them | 2 | yes |
| `Smallest number of questions possible`, `≤3` per clarify's shape | Essential Questions | count the numbered list | 1 | yes |

Report `5 of 7 bounds within, 2 breaches`. **One rule is deliberately *not* a bound and must not be
turned into one**: `Do not cap the number of assumptions. List every load-bearing default; never
drop a material one to shorten.` Trimming that list to look tidy is override 1's collapse arriving
through the back door. One more binds without being a count — **no `(Recommended)` mark unless the
action is unrecoverable**, where it goes on the *reversible* path, because a mark on the human's own
axis answers the question while appearing to ask it.

## Override 4 — the gate is a sequence of artifacts, not a standard to have met (steps 1–8)

The scan's `0 qualitative skill references` is what makes this necessary, not unnecessary.
**[measured-family]** §1.2.1 (n=1): a skill instructed that every design decision `goes through` two
named skills, and the run invoked neither — its own diagnosis being that the rules were already in
context and nothing downstream depended on a file only those skills produce. Corroborated outside
this repo (§7.2) by a Gemini 3 **Pro** transcript reclassifying a `GEMINI.md` rule as guidance, so
it binds on every tier. **[docs]** The remedy is the chain: *"make each step a prompt and chain the
prompts together in a sequence."*

```
1 read mode + whole thread   → the prior sections/answers, in hand   ; 3 grounds against them
3 grounding                  → located surfaces + tags               ; 4 lenses scan those
4 Sentinel                   → findings, lens- and severity-tagged   ; 5 resolves each
5 decision gate              → assumptions + surviving EQs           ; 6 reviews that text
6 out-of-family review       → /tmp/so-<id>.md, non-empty, headers   ; 7 reads the verdict
7 assumptions review         → per-assumption pass/convert            ; 8 writes what survived
8 write + move status        → the section, then the status
```

Two things the chain makes non-optional. **Step 5 runs before step 8**, so a question written
straight into the section skipped the gate that would have made it an assumption — run the
divergence test on the question list itself, because `a question whose recommended answer you would
proceed on either way is an assumption wearing a question's clothes`. And **step 6 produces a file**;
absent or empty, the gate did not run, whatever the transcript says.

## Override 5 — read the thread, then answer (step 1, Hard rules)

**[measured-family]** §1.2.4 (n=1) recorded both halves of this failing in one session: asked a
question naming three skills, the run answered from memory without loading any of them; asked to fix
that, it launched a skill instead of answering and had to be interrupted. There is no stable mapping
from *named in the prompt* to *loaded before the answer*, so make it two ordered steps. This stage's
rule is that ordering already: `Re-triage reads every prior section/comment — human answers are
authoritative; never re-ask an answered question`, and the ban on re-asking carries a worked BAD
example. Open the brief file, the whole spec or the full comment thread — on the tasks lane
`list_comments`, **all of it** — before a line of verdict is drafted. **[docs]** *"Your knowledge
cutoff date is January 2025."* A prior answer you remember is not a prior answer read.

## Override 6 — two attempts, then a different move (steps 2, 6)

**[docs]** *"On other errors, you must change your strategy or arguments, not repeat the same failed
call."* **[measured-family]** Both n=1 sessions ran the loop: one invoked a banned, absent tool four
consecutive times with nothing changed (§1.1.2); the other hit a 25,000-token `Read` ceiling and
retried four times with minor tweaks before pivoting to a Python split (§1.2.3). Three failures here
pivot on **attempt 1**: an **empty lane output file** is that lane's failure — log one line, take
the next lane, and `narrow the packet before you widen the deadline`; a **brief or thread over the
`Read` ceiling** takes line-ranged reads or a Python split; and a **fan-out wave returning `null`s**
is retried once in a smaller batch, never treated as a finding, with the wave capped at **≤4**.

## Override 7 — `thinking_level`, and what it is not for

**[docs]** `HIGH` is described as suitable for *"multi-step planning, verified code generation"*.
This stage is planning-shaped rather than code-shaped — grounding, five lenses, a decision gate, two
review rounds — so name `HIGH` and say the uplift is unmeasured on this corpus; Gemini 3.7 Flash
defaults to `MEDIUM`. **[measured-family]** Do not raise it as a remedy for anything above: paired
across 106 tasks, `high` beat `medium` on 24, lost on 24 and tied on 58, mean **−1.7 points**
(§2.3), and the bound-shaped share of failures *rose* from 58% to 86% — the wrong direction for a
target whose overrides are mostly bounds. **[docs]** On the register the section is written in,
*"By default, Gemini 3 models provide direct and efficient answers."* — which is what `Keep the
review short and non-technical` asks for, so the default helps here rather than hurting.

## Recap

**[docs]** *"Concise repeat of the key points of the prompt, especially the constraints and response
format, at the end of the prompt."*

1. Write the six-row ledger before step 8. Row 4 — one line per touched surface — silently collapses first.
2. Tag every on-screen claim measured-or-assumed; flag a regulatory rule rather than recalling it; make the brief citation resolve.
3. Read seven bounds back off the written section. The ban list is a bound; the assumptions count is deliberately not.
4. Each step opens the previous step's artifact; step 6 is a real invocation with a non-empty output file.
5. Read the whole thread before drafting; never re-ask an answered question. Running as Gemini, skip the agy lane at step 6.
