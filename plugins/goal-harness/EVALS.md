# Evals: goal-harness

Run 2026-08-09 against Claude Code v2.1.226.

## What was measured

The honest baseline for a new skill is **not having it**. Each case was run
twice from an identical fixture repo: one arm with the skill loaded, one arm
with nothing loaded and instructed to answer as normal. Neither arm knew the
other existed.

Grading was done by an independent agent that saw each response **alone**, under
an anonymous id, with no arm label and no access to the mapping. Responses were
graded against pre-registered structural assertions from `evals/evals.json`,
each answered PASS/FAIL with the deciding sentence quoted, then the grader named
which of each pair it would rather have received.

Blinding by anonymous id rather than by redaction was deliberate: the skill arm
legitimately cites its own scripts, so stripping those names would have mangled
the text rather than concealed the arm.

## Result

| Case | What it probes | skill | baseline | preferred |
|---|---|---|---|---|
| G01 | Arming a backlog goal from a rough intent | **7/8** | 2/8 | skill |
| G02 | `/goal /create-fleet-goal`, where the condition is a command name | **3/3** | 0/3 | skill |
| G03 | "Why have you stopped?" | **4/4** | 1/4 | skill |
| G05 | A goal that runs `/code-review` every turn | 3/3 | 3/3 | skill |
| | **assertions** | **17/18** | 6/18 | |
| | **preference** | **4/4** | 0/4 | |

Combined with `loop-harness`, which ran the same protocol: **32/33 assertions
against 12/33, and 8/8 preferences.**

## Where the baseline held its own

**G05 tied at 3/3.** The baseline independently worked out that `/code-review`
is `disable-model-invocation`, that a read-only review cannot converge, and that
the fixture's clean tree would make a diff review vacuous. It read the docs and
got there. The grader still preferred the skill arm, but on secondary grounds (a
freshness gate so a stale clean verdict cannot satisfy the condition), not
because the baseline missed the trap.

That is worth stating plainly: on the `/code-review` case the skill's headline
claim is **not** what separates it. A capable model with the docs finds that one.

## The single assertion the skill arm failed

G01 #8, "shows a settings diff or explicitly withholds the write". That arm
applied the settings write and described it in prose afterwards rather than
showing the before/after first. The skill's step 5 requires the diff first, so
this is an adherence miss, not a missing rule.

## What the eval found in the skill itself

Three defects, all reported by arms that followed an instruction and hit the
edge rather than working around it:

1. **`goal-guard.sh` parsed UTC deadlines as local time.** `epoch_of()` stripped
   the trailing `Z` and handed the result to `date -j -f`, which on BSD reads
   its input as local. On `+1000` a UTC deadline landed ten hours in the past
   and the first Stop after arming disarmed the goal before a gate ran.
2. **`preflight.sh` blocked a legitimate plugin skill.** The built-in check
   matched when `plugin == name`, true both for a bare `/code-review` and for
   the plugin-qualified `code-review:code-review`.
3. **`loop-harness` step 4 pointed at a script that does not exist** (`arm.sh`).

All three are fixed. **The scores above were produced before those fixes**, so
they measure the skill as first written, not as it now stands.

Two further gaps came from arms doing the work rather than reading the docs: a
log filter cannot emit when a process dies without writing, so a liveness poll
belongs beside the tail; and a subagent's session id is not the driving
session's, so a guard armed from one is inert. Both are now in the skills.

## And what a code review found afterwards

A deep review of the ten scripts (`code-review-goal-loop-harness.md`) then found
eleven more, of which eight were confirmed by executing the scripts rather than
reading them. The two worst were both silent-success paths, which is the same
class of defect these skills exist to catch:

- `arm.sh` truncated an existing `settings.local.json` to **zero bytes** when
  that file was not valid JSON, taking the user's other hooks and permissions
  with it, and exited 0 printing `armed:` as though it had worked.
- The guard treated a `verify` field that was empty, `null`, a string or an
  object as **all gates green**, recording the goal as met on turn one without
  checking anything.

Also: a flag passed without its value spun four scripts forever; `verify[].timeout`
was unenforced on any machine without `timeout(1)`, which includes stock macOS;
a non-numeric `max_iterations` silently removed the iteration bound; and the
`--dry-run` preview omitted three keys the real write added. One candidate of
mine was refuted by an independent verifier.

All eleven are fixed in v1.0.1, each re-tested against the case that proved it.
The count is worth stating plainly: fifteen defects in roughly 400 lines of
bash, and the ones that mattered were not crashes but false reports of success.

## Limits of this run

- **4 of 6 cases per skill.** The four carrying the README's central claims.
  G04 (a judgment-shaped condition) and G06 (a blocked preflight) were not run.
- **The fixture is thin on purpose** and both arms spend real effort discovering
  that. For the knowledge-shaped cases (G02, G03, G05) that barely matters. For
  G01, the arming flow, it confounds: some of the gap is the skill grounding the
  condition, and some is the two arms reacting differently to a stub repo. Do
  not read G01's 7/8 vs 2/8 as a clean measurement of the arming protocol.
- **One grader, not a panel.** A multi-family blind panel would be stronger.
- **n=1 per cell.** No variance estimate; a single re-run could move a cell.

## Reproducing

```bash
# fixture, 16 run dirs, 8 cases x 2 arms, then anonymise and grade
python3 /tmp/gh-evals/anonymise.py   # deterministic ordering, no stored seed
```

The case prompts are in `evals/evals.json`. The baseline arm is the same prompt
with no skill loaded and an instruction not to read outside its run directory.
