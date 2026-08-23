# gemini.md — `ratchet`

Read this once, now, then read `SKILL.md` and follow it with the overrides below; each names the
section it lands on. `ratchet` is the shortest file in this set because it is the least ambiguous
skill in the plugin: the work is `python3 scripts/ratchet.py --root <repo>`, and everything else is
reading what it printed. Its own constraint says why that matters more than it looks — `A model
deciding its own authority is the one structure that makes every other guarantee here
unfalsifiable`. The whole risk on this family is being helpful in exactly the place the skill asks
you not to be.

## Epistemic status

- **Tiers used:** `[docs]`, `[measured-family]`, `[derived]`. No `[measured-here]`: **no Gemini run of
  `ratchet` has been observed**, at any tier.
- **`[measured-family]` sources:** two single sessions (n=1 each) and a 106-task benchmark at two
  effort levels — `geminify/references/evidence.md`. Neither watched a model read a control chart or
  apply a revocation.
- **The tier the evidence is about.** Every measured rate below was observed on `gemini-3.7-flash`
  (one session on `gemini-3.7-flash-high`) — flash-tier claims, **not** to be projected onto the Pro
  tier. **[docs]** The default drifts inside the family: *"If thinking_level is not specified, Gemini
  3 will default to high."* against, from the 3.5 Flash release notes, *"The default thinking effort
  is now medium, changed from high in Gemini 3 Flash Preview."* On Pro these overrides stand as
  `[docs]`-grounded discipline and every `[measured-family]` number is open.
- **Unmeasured on this skill:** no Gemini run of `ratchet` · no evidence a `gemini.md` fixes anything
  on either source · the fabricated-verification and retry-loop observations were made on a UI mock
  and a research pipeline, so their transfer to a tier table is `[derived]` · nothing measures this
  family reading a Westgard multirule chart, or the `C12`/`C1` evidence the ladder rests on.
- **The self-limitation.** **[docs]** A conditional side file is the shape the checklist warns about:
  *"Avoid writing a prompt with non-linear logic or conditionals that require the model to piece
  together fragmented instructions from multiple different places in the prompt."* One pass, then
  work from `SKILL.md`.

## There is no route-out block here

geminify writes one only where the benchmark measured the work, and `ratchet` fails both conditions.
**Its work class is one the corpus abstains on:** deciding what a class has earned is `verification`,
where `lane_pick.py` returns the policy answer unchanged. **And none of the four measured shapes is a
thing it produces:** it authors no page (`static-page`), renders nothing to judge (`visual-design`),
writes only into `.warrant/` rather than editing a repo (`brownfield-integration`), and breaks no
passing contract (`regression-sensitive`). **[docs]** *"Avoid using prompts that ask the model to
perform a task for which it has a known, fundamental limitation."*

## Nothing to quota, nothing to bound

`scan_skill.py` returned **0** categorical quantifiers, **0** bounds, **0** relative qualifiers, **0**
qualitative skill references and **0** shouted tokens across all 92 lines. That is a real result
rather than a scan failure, and it says what this skill is: every quantity `ratchet` handles already
exists as a number in a file — `tiers.tier3_items_closed_min`, `tiers.tier3_window_days`,
`[staleness] calibration_max_days`, `[oracle] coverage_min` — read by a script that computes the
answer. **[measured-family]** §2.1 is the reason that matters: the one work bucket where this family
matches opus is optimality, 74.7 against 75.0, on tasks whose brief already states the bound. There
is no ledger to write here, and inventing one would be a worse file.

**Modules written:** `gate` only, added by hand. `scan_skill.py --refs` globs
`<skill>/references/*.md` and this plugin keeps its references one level up, so `gate` reported two
triggers on `SKILL.md` alone — this skill writes `Exit 4` rather than the trigger's literal `exit
code` — and three once `references/tiers.md`, `references/measurement.md` and
`references/script-contract.md` are included. **Not written:** `bounded-constraint`, which also
reaches three across those files but whose bounds are all enforced by `charter_validate.py` and
`ratchet.py` rather than restated for a reader; `visual`, `states`, `platform-values`, `authorship`,
`injection`, `delegation` and `count-contract`, all under threshold; `emphasis`, **0** tokens.

## Override 1 — the tier table is the script's output, not yours (`## Output`)

**[measured-family]** §1.1.2 (n=1): a run wrote its own verification document as five well-formed
rows, all `PASS`, naming a browser engine as verified when it had failed all four invocation
attempts, `100% pass rate on contrast` from a probe never executed — measured afterwards, every
primary button 3.65:1 and one glyph 1.00:1, invisible — and `Interactive Targets Audited: 47`, a
number nothing produced. The reading in `references/evidence.md` §1.1.2 is the one to carry here:
that is a model completing a requested **shape** when the shape was specified and the procedure was
not. `ratchet.py prints the tier held and the tier earned per class` — a two-column table, with an
obvious shape, that a capable model can fill in from the ladder and the six triggers without running
anything.

So no row is typed by hand. **[docs]** *"Include specific verification steps in either the system
instructions or your prompts directly."* and *"Verify your claims by quoting the exact applicable
information (including policies) when referring to them."* Ship the transcript filled:

```
ratchet   ratchet.py --root .                 → exit 4 · revocation applied
          disclosure-figures  held 2  earned 0  REVOKED (oracle coverage 0.81 < 0.95)
          tenant-isolation    held 1  earned 1
          copy-and-labels     held 0  earned 1  PROPOSAL written, unsigned
westgard  westgard.py --series corpus-history.json  → exit 2 · rule 4-1s on runs 7–10
control   ratchet.py --selftest                     → exit 0 · every rule fired
inputs    suite-health.json · oracle-coverage.json · escapes.jsonl · warrant.toml · lanes.toml
          rollup_classes.py last run: 2026-08-23T09:14Z (before this ratchet)
```

**[docs]** *"When model outputs must be machine-readable or follow a specific format, use a widely
recognized standard like JSON, XML, Markdown or YAML that can be parsed by common libraries."* — use
`--json`, and remember `In --json mode, stdout carries the JSON object and nothing else`, so count
over stdout in Python rather than by eye over the stderr summary. **[docs]** *"Gemini's code
execution tool enables the model to generate and run Python code, and should be enabled whenever the
model needs to perform any kind of arithmetic, counting, or calculation."*

## Override 2 — run the prerequisite, then read the receipt (`## Procedure`, step 1)

**[measured-family]** §1.2.2 is this skill's exact failure mode one level up: an auditor validated
its final properties thoroughly, had **zero** checks that its prerequisite artifacts existed, and
returned exit 0 over two skipped upstream steps. `ratchet.py` reads six state files, and one of them
is written by a step that is easy to skip — `rollup_classes.py` maps per-surface measurements onto
defect classes, and `warrant`'s own map says `Without it every class reads as having no evidence`.

A ratchet run over unrolled state therefore produces a clean, well-formed, wrong table: every class
earning tier 0, no revocation firing, exit 0. **Read the receipt before the verdict** — check that
`.warrant/oracle-coverage.json` and `.warrant/suite-health.json` each carry a `classes` block newer
than the last `oracle` and `assay` run, and say so in the note. **[docs]** *"provide instructions for
handling missing data rather than assuming inserted data will always be present and well-formed."*

And prove the gate can fail before believing it green. **[derived]** geminify's own quote gate went
green across every file after a change took its checked count to zero, caught only by re-running the
negative control (§5). The script contract already ships one, and it is not a smoke test:

```bash
python3 scripts/ratchet.py --selftest   # exit 0 only if every rule fired
```

## Override 3 — exit 4 is the success case, and none of these exits is a retry (`## Procedure`, step 2)

**[docs]** *"On *other* errors, you must change your strategy or arguments, not repeat the same
failed call."* **[measured-family]** Both n=1 sessions ran the loop: four consecutive invocations of
one banned, absent tool with nothing changed between them (§1.1.2), and four consecutive `Read` calls
against a 25,000-token ceiling before pivoting to a Python split (§1.2.3). `gemini-cli` ships a loop
detector whose halt message names *"repetitive tool calls"* (§7.2).

`ratchet` inverts the usual reading of a nonzero exit, and getting this wrong is the expensive
mistake:

| exit | means | what to do |
|---|---|---|
| 0 | nothing changed, or a promotion was proposed | read the proposal; it is unsigned and stays that way |
| 1 | the script could not run — bad usage, unreadable input | fix the invocation; this is the only retryable one |
| 2 | a check ran and failed (`westgard.py` names the rule) | read the rule that tripped, not the threshold |
| 3 | a precondition is absent: no warrant, no ledger, no corpus | run `charter` or the missing plane; re-running changes nothing |
| 4 | **a revocation fired and has already been applied** | report it; do not re-run, and do not undo it |

Exit 4 is not an error to clear. `Apply a revocation before reporting it` is deliberate ordering, and
the script contract's reason generalises: `A writer that has already had an external effect does not
throw`, because raising invites a retry that does it twice. A second `ratchet.py` run after an exit 4
is a retry of a completed write.

## Override 4 — the one edit that is never yours (`## Constraints`)

`Never restore a tier as part of a revocation run. Promotion is a separate act, by a person, in
warrant:charter, reading the evidence that earned it.` `references/tiers.md` states the consequence
more sharply: re-signing a revoked class back up without new evidence `is the one edit that turns the
warrant into a fiction`.

This is the prohibition most likely to be read as style advice, because asked to fix a failing run,
editing `.warrant/warrant.toml` is the shortest path to a green one. Convert it to a closed set with
one option removed: on an exit 4, the available actions are report it, run the plane that would
re-earn the tier, or run `revoke.py` with a written reason — and editing the warrant is not on the
list. **[docs]** Google's remedy for a model answering outside a closed set is to state the set:
*"The response is correct, but the model didn't stay within the bounds of the options."* **[docs]**
*"Inhibit your response: only take an action after all the above reasoning is completed. Once you've
taken an action, you cannot take it back."*

The same holds for `revoke.py --reason`, which the skill requires because `A revocation with no
recorded reason is indistinguishable later from a mistake.` Write what you observed, not what you
inferred — `references/measurement.md` asks for that in general: `Where a number is an inference
rather than a measurement, say so in the same sentence.`

## Override 5 — thresholds and rule names get read, not recalled (`## The six revocation triggers`, step 3)

**[docs]** *"Your knowledge cutoff date is January 2025."* Two families of value here are the kind
that come back confidently wrong. **[measured-family]** §1.1.4 is what that looks like: a
previous-generation published accent colour returned as current, an old fact rather than a guess.

- **The warrant's own thresholds** — `[oracle] coverage_min`, `tiers.tier3_items_closed_min`,
  `tiers.tier3_window_days`, `[staleness] calibration_max_days`. Read them out of `.warrant/warrant.toml`.
  `references/tiers.md` notes the older spelling `tier3_items` is still read, which is exactly the
  kind of detail a recalled schema loses.
- **The Westgard rule names** — `1-3s, 2-2s, R-4s, 4-1s and 10-x` are a published multirule set, and
  `westgard.py exits 2 naming the rule that tripped`. Report the rule the script named. The
  interesting case is the one the skill and `references/measurement.md` both single out: `a corpus
  pass rate that slides from 100% to 94% over ten runs never trips a threshold and is exactly what a
  reversioning model looks like` — so a 10-x on a series that never breached a limit is a finding,
  not a false alarm.

The claim ids behind the triggers — `C12` on benchmarking an automated control across periods, `C1`
on the absent reader study — resolve in `docs/deep-research/claims.json` and
`references/evidence.md`. **[measured-family]** §1.2.4 recorded a run answering a question that named
three skills from memory without loading any of them, then over-correcting by launching a skill when
an answer was wanted. Read, then answer, as two ordered steps.

## Override 6 — `thinking_level`, and what it is not for

**[docs]** `HIGH` is described as suitable for *"multi-step planning, verified code generation, or
advanced function calling scenarios"*; 3.7 Flash defaults to `MEDIUM`. `ratchet` is none of those —
it is one script invocation and a read of a table — so run the default. **[docs]** *"Higher thinking
levels encourage the model to use more tools to explore and verify, so lowering the level can reduce
tool calls."* Here that is the wrong direction twice over: more exploration on a skill whose
correctness depends on not reasoning about the answer. **[measured-family]** And it buys nothing
anyway — paired across 106 tasks, `high` beat `medium` on 24, lost on 24 and tied on 58, mean −1.7
points (§2.3).

## Recap

**[docs]** *"Concise repeat of the key points of the prompt, especially the constraints and response
format, at the end of the prompt."*

1. Run the script; every tier, class and revocation in your report is copied from its output with the
   command beside it.
2. Confirm `rollup_classes.py` ran first, or the clean table you get back is a table about nothing.
3. Exit 4 means the revocation already applied — report it, never re-run it. Only exit 1 is
   retryable.
4. Never restore a tier: report, re-earn, or `revoke.py --reason`. Editing `warrant.toml` is not on
   the list.
5. Read thresholds out of `warrant.toml` and report the Westgard rule the script named; a slow drift
   that never breaches a limit is the finding, not the false alarm.
