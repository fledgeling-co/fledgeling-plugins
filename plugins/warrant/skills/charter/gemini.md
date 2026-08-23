# gemini.md — `charter`

Read this once, now, then read `SKILL.md` and follow it with the overrides below; each names the
section it lands on. `charter` is the outermost gate of the whole plugin and the only place a human
signature survives, which makes it the one skill here where the model's most useful act is to *stop*.
Four of the warrant's fields are judgements rather than facts about the repository, the draft leaves
them blank on purpose, and **[measured-family]** completing a requested shape whose procedure was not
specified is the exact failure one measured run recorded (`geminify/references/evidence.md` §1.1.2).

## Epistemic status

- **Tiers used:** `[docs]`, `[measured-family]`, `[derived]`. No `[measured-here]`: **no Gemini run of
  `charter` has been observed**, at any tier.
- **`[measured-family]` sources:** two single sessions (n=1 each) and a 106-task benchmark at two
  effort levels — `geminify/references/evidence.md`. None watched a model draft a policy file, and
  none touched a regulated-evidence domain.
- **The tier the evidence is about.** Every measured rate below was observed on `gemini-3.7-flash`
  (one session on `gemini-3.7-flash-high`) — flash-tier claims, **not** to be projected onto the Pro
  tier. **[docs]** The default drifts inside the family: *"If thinking_level is not specified, Gemini
  3 will default to high."* against, from the 3.5 Flash release notes, *"The default thinking effort
  is now medium, changed from high in Gemini 3 Flash Preview."* On Pro these overrides stand as
  `[docs]`-grounded discipline and every `[measured-family]` number is open.
- **Unmeasured on this skill:** no Gemini run of `charter` · no evidence a `gemini.md` fixes anything
  on either source · nothing measures this family filling or refusing to fill a risk-appetite field,
  proposing a tier, or handling paywalled standards text · the observed failures were on UI and
  research briefs, so their transfer to a TOML policy file is `[derived]`.
- **The self-limitation.** **[docs]** A conditional side file is the shape the checklist warns about:
  *"Avoid writing a prompt with non-linear logic or conditionals that require the model to piece
  together fragmented instructions from multiple different places in the prompt."* One pass, then work
  from `SKILL.md`.

## There is no route-out block here

geminify writes one only where the benchmark measured the work, and `charter` fails both conditions.
**Its work class is one the corpus abstains on:** the bench measures a model *building* an artifact,
while `charter` drafts a declarative policy file with a script and then runs a validator over it —
`verification`, where `lane_pick.py` returns the policy answer unchanged. **And none of the four
measured shapes is a thing it produces:** `static-page` and `visual-design` (nothing is rendered),
`brownfield-integration` (one file the script emits under a schema it fully controls, not a multi-file
repo edit under several acceptance criteria), `regression-sensitive` (there is no passing contract to
preserve; `charter_validate.py` is the contract). **[docs]** *"Avoid using prompts that ask the model
to perform a task for which it has a known, fundamental limitation."*

## What transfers intact, and what the scan found

**The scan returns 0 categorical rows and 0 bound rows** over 90 lines, with 4 loose distributives and
8 prose prohibitions counted rather than listed. `charter` is already written in numbers: `the four
fields the script cannot infer`, `Six failures`, `one block per lane`, and a tolerable error rate
bounded to `(0, 1)`. One row is added by hand below, because the scan's deliverable vocabulary has no
word for a lane — `Pin every lane` is a categorical scope over a countable artifact and it is exactly
the shape that collapses to one instance.

**The instruction that cuts against this model's resting style is correct here and stays.** **[docs]**
*"By default, Gemini 3 models provide direct and efficient answers. If you need a more conversational
or detailed response, you must explicitly request it in your instructions."* — `charter` requests it:
`a comment explaining why a class sits where it does is worth more than the three lines it costs`,
because `The audience is an auditor and a future owner`. Write the comments. Brevity trims preamble
here, never a rationale comment and never a validator's pasted output.

**Modules.** The scan fired none at its 3-trigger threshold. `gate` is written below on one trigger
(`scripts/`) because the target's own step 5 is `Gate on it.` with three exit codes and six named
refusals — a deterministic check whose output can be quoted is what the module is for, and the
threshold missed it on vocabulary rather than on substance. Nothing else is written: `visual`,
`states`, `platform-values`, `authorship` (its grounded clause is cited inside Override 1 rather than
as a section, because here it is core C2 applied to one field rather than a module), `delegation`,
`injection`, `bounded-constraint`, `count-contract`, and `emphasis` — **0** shouted tokens in 90 lines.

## Override 1 — the four judgement fields are not yours to fill (`### 2`)

This is the override the rest of the file is built around. `charter` says it plainly: `Each is a
judgement rather than a fact about the repository, so the draft leaves them blank and
charter_validate.py rejects the file until they are set.` A plausible number in
`lot.tolerable_error_rate` is a risk appetite nobody chose, and it silently sets the sample size and
therefore the human time the audit costs.

**[docs]** Adopt Google's strictly-grounded instruction for this step, and note its last clause:
*"If the exact answer is not explicitly written in the context, you must state that the information is
not available."* Also *"Do not assume or infer from the provided facts; simply report them exactly as
they appear."* The repository can supply surfaces, spec files and candidate classes. It cannot supply
an owner, an appetite, a promotion threshold or a staleness window.

So the run's deliverable at this step is the draft plus this block, filled, handed back:

| key | left blank because | what the answer costs |
|---|---|---|
| `owner.name`, `owner.email` | a person, not a role — `A role with no current holder is a warrant with no signature` | nothing to write; everything if wrong |
| `lot.tolerable_error_rate` | risk appetite in `(0, 1)` | it `sets the sample size and therefore the human time this costs` |
| `tiers.tier3_items`, `tiers.tier3_window_days` | how much closed volume earns tier 3 | `Too low and the ladder is decoration` |
| `staleness.days` | how stale a regression run may be before tiers lapse | tiers above 0 lapse at this age |

**[docs]** *"The response is correct, but the model didn't stay within the bounds of the options."* is
the failure Google names for a model asked an open question; the bound here is that there are no
options — these four come from the owner or the file stays invalid.

## Override 2 — every lane, pinned twice, and cross-checked against the warrant (`### 3`)

`Pin every lane` is the file's one unbounded scope. **[measured-family]** §1.1.1 (n=1): a run
delivered **12 of 12** requirements a brief *enumerated* and satisfied every requirement named
*categorically* with one instance or none — all surfaces → 5, all states → **1**, all menus → **0**.
**[docs]** *"Avoid using subjective or relative qualifiers that lack a concrete, measurable
definition."*

Count the lanes first, then fill one row each. Two of the six refusals live in this table:

| lane | role | model id | model version | in `warrant.toml`? |
|---|---|---|---|---|
| `grader` | grader | `gpt-5.6-sol` | `2026-07-14` | yes |
| `lens-lineage` | lens | `gemini-3.7-flash` | `3.7-flash-002` | yes |
| `lens-taxonomy` | lens | `gemini-3.7-flash` | `3.7-flash-002` | yes |
| `adjudicator` | adjudicator | `claude-opus-5` | `20260612` | yes |

Report `4 of 4 lanes pinned with id and version · 4 of 4 classes named in the warrant`. A version
column reading `latest`, `stable` or blank is the failure `C12` is about: an auditor may lean on last
period's testing of an automated control only where the control is verified not to have changed, and
a silently reversioned model cannot satisfy that. The inference is the plugin's, and
`references/admissibility.md` says so — carry the caveat, not just the rule.

## Override 3 — paste the validator, and name what it cannot see (`### 5`, `## What validation refuses`)

**[docs]** *"Include specific verification steps in either the system instructions or your prompts
directly."* and *"Verify your claims by quoting the exact applicable information (including policies)
when referring to them."* The delivery note ships filled:

```
init      charter_init.py --root .        → wrote .warrant/warrant.toml · 11 surfaces · 6 classes
validate  charter_validate.py --root .    → exit 2 · owner.name unset · lot.tolerable_error_rate unset
control   charter_validate.py --selftest  → exit 0 (every rule fired, pass and fail)
```

**[measured-family]** §1.2.2: an auditor validated everything it was written to validate, had no check
that its prerequisites existed, and returned exit 0 over two skipped steps. `charter_validate.py` has
the same blind spot by design, and the router names it: absent evidence is an unmet condition, which
makes `never measured` and `measured badly` identical to the validator. So a class sitting at tier 0
after a clean exit 0 is reported as *unexplained* until `rollup_classes.py` has run — running the
planes again will not tell you which it was.

Run `--selftest` before believing a clean gate. **[derived]** geminify's own quote gate went green
across every file after a change took its checked count to zero, caught only by re-running the
negative control (§5).

## Override 4 — three exit codes, three different actions, and no re-runs (`### 5`)

**[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same failed
call."* **[measured-family]** Both n=1 sessions ran the loop: four consecutive invocations of one
banned, absent tool with nothing changed between them (§1.1.2), and four consecutive `Read` calls
against a 25,000-token ceiling before pivoting (§1.2.3). `gemini-cli` ships a loop detector whose halt
message names *"repetitive tool calls"* (§7.2).

Here none of the three nonzero exits is transient, so none of them is retried:

- **exit 2** — `names the key and what would fix it`. Fix that key. A second run without an edit
  returns the same line.
- **exit 3** — `there is no warrant at all`. Run `charter_init.py`; re-running the validator cannot
  create one.
- **exit 1** — the script could not run: bad usage or unreadable input. That is a typo in your
  command, not a failed gate, and treating the two alike is the confusion the plugin's `_cli.py`
  overrides argparse to prevent.

## Override 5 — a proposal is a document to read, and a revocation is already applied (`## Constraints`)

The pressure this model is under at this step is to make the file validate. Two of the target's own
sentences forbid the two cheapest ways: `Treat a proposed tier promotion as a document to read rather
than a change to accept`, and `re-signing a revoked class back up without new evidence is the one edit
that makes the warrant a fiction`. Raising a tier is never the fix for a failing gate; it is the gate
removed.

**[docs]** *"Inhibit your response: only take an action after all the above reasoning is completed.
Once you've taken an action, you cannot take it back."* And **[docs]** *"Avoid premature conclusions:
There may be multiple relevant options for a given situation."* — the options at a failed validation
are: supply the missing evidence, lower the claim, or hand the proposal to the owner. Editing the tier
is not among them.

The commit is the signature, and it is authored by the owner. A run that commits `.warrant/warrant.toml`
under an agent identity has produced an artifact whose entire purpose — `git log` is where an auditor
reads the signature — is void. Stage it, say it is ready, and stop. `C11` is why: a Part 11 electronic
signature must be unique to one individual.

## Override 6 — the standards are read, never recalled (`# Charter`, `references/admissibility.md`)

**[docs]** *"Your knowledge cutoff date is January 2025."*, and from the 3.7 Flash model card, *"The
knowledge cutoff date for Gemini 3.7 Flash is March 2026 — users can expect updated information for
some domains while in others they may experience the model's knowledge is limited to January 2025 (in
line with the Gemini 3 Model Family)."* **[measured-family]** §1.1.4 is the shape to fear here: not a
guess, but a previous-generation published value returned confidently — eight metric errors in one
artifact, including an accent colour from the wrong OS generation.

Regulation is that failure mode with worse consequences. `C10` (DO-330) and `C13` (ISO/IEC 17025) are
**paywalled with their contents unread**, `C12`'s application to a reversioned model is the plugin's
own inference, and `admissibility.md` opens by saying `Nothing here is legal advice`. Read the row
before restating the rule, and carry its bound in the same sentence. **[docs]** *"Treat the provided
context as the absolute limit of truth; any facts or details that are not directly mentioned in the
context must be considered **completely untruthful** and **completely unsupported**."*

The same rule covers a file named in a prompt. **[measured-family]** §1.2.4 recorded both halves
failing in one session — answering from memory when three skills were named, then launching a skill
when an answer was wanted. `SKILL.md` names `references/admissibility.md` as a prerequisite: read it,
then write. Two ordered steps, neither substituting for the other.

## Override 7 — `thinking_level`, and what it is not for

**[docs]** `HIGH` is described as suitable for *"multi-step planning, verified code generation, or
advanced function calling scenarios"*; 3.7 Flash defaults to `MEDIUM`. `charter` is a draft, four
questions and a validator — run the default. **[measured-family]** Do not raise it as a remedy for
anything above: paired across 106 tasks, `high` beat `medium` on 24, lost on 24 and tied on 58, mean
−1.7 points (§2.3). **[docs]** *"Higher thinking levels encourage the model to use more tools to
explore and verify, so lowering the level can reduce tool calls."*

## Recap

**[docs]** *"Concise repeat of the key points of the prompt, especially the constraints and response
format, at the end of the prompt."*

1. Leave the four judgement fields blank and hand back the filled table of what each one costs; state
   the information as unavailable rather than supplying it.
2. Count the lanes, pin id **and** version on every one, cross-check each class against the warrant,
   and report `N of N` both ways.
3. Paste `charter_validate.py`'s exit code and lines; run `--selftest` before believing a pass; report
   a tier-0 class as unexplained until `rollup_classes.py` has run.
4. Exit 2 fix the key, exit 3 run `charter_init.py`, exit 1 fix your command. Re-run none of them.
5. Never raise a tier to make a gate pass, never re-sign a revoked class, and never author the
   signing commit — stage it and stop.
