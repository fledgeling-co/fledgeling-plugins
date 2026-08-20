# Verification — six gates, three verdicts

Every candidate is verified before it can reach the report. The verifier's job is to **refute**;
confirmation is what remains after refutation fails. A verifier that confirms everything has
moved the confirmation bias to a second model rather than removing it.

Two structural choices, both load-bearing:

1. **A different agent verifies than the one that found the candidate.** The agent that
   pattern-matched a bug is the wrong agent to ask whether it is real. At `quick` depth the
   orchestrator self-verifies as an explicit cost trade-off, and compensates with deliberate
   skepticism.
2. **Confidence filtering runs after the verifier, never before.** Surfacing a borderline
   candidate costs almost nothing when a verifier refutes it; silently dropping a real bug in
   Find cannot be recovered.

## One verifier, not a panel

Each candidate gets **one** verifier vote. That is a deliberate choice, not a budget compromise.

Measured on a reward-modelling and NLI benchmark, nine frontier judges spanning seven model
families behaved as roughly **two** effective independent votes; panel accuracy ran 8 to 22
percentage points below what genuinely independent voting would have produced, and **the best
single judge matched or beat the whole panel in every tested condition**. Established aggregation
methods closed at most 11% of that gap even when given the correct answers. The result has prior
art: 27 independently written versions of one specification, tested about a million times in 1986,
failed in correlated ways and rejected the independence hypothesis outright.

Correlation is worse here than in that benchmark, because a second verifier would receive the same
candidate, the same file, and the same controls map. Agreement between readers sharing a brief and
a source pool is not corroboration — in one recorded case three research backends converged
unanimously on a claim that a single first-party check falsified.

Spend the budget on gates and evidence instead of on voters. Where a candidate genuinely turns on
something no reader can settle from the repo, that is a `PLAUSIBLE` verdict or a `no-oracle` row in
the coverage ledger, not a tie-break.

## The three verdicts

- **CONFIRMED** — you can name the inputs or state that trigger it, and the wrong output or crash
  that results. Quote the line.
- **PLAUSIBLE** — the mechanism is real; the trigger is uncertain (timing, environment, config,
  data shape). State what would confirm it.
- **REFUTED** — factually wrong (the code does not say that), provably impossible from a type,
  constant or invariant, already guarded in this diff or by a global control, or pure style with no
  observable effect. Quote the line that proves it.

**PLAUSIBLE is the default for realistic-but-unproven.** Do not refute a candidate for being
speculative or depending on runtime state when the state is reachable: a concurrency race,
undefined on a rare-but-reachable path (an error handler, a cold cache, an absent optional field),
a falsy zero treated as missing, an off-by-one on a boundary the code does not exclude, retry
storms and partial failures, a regex or allowlist that lost an anchor. Those are PLAUSIBLE.

**REFUTED requires something constructible from the code.** Quote the actual line, show the type or
constant that makes it impossible, cite the guard, or name the style rule it reduces to.

Keep CONFIRMED and PLAUSIBLE. Drop REFUTED.

A PLAUSIBLE finding reports with its uncertainty stated and the confirming step named. It is a
terminal state that routes to the developer, not a retry condition — re-running the same verifier
against the same evidence produces the same answer at twice the cost.

## The gates

Run them in order per candidate. The first gate that fails decides the verdict; passing all six
gives CONFIRMED.

### Gate 1 — API existence

If the candidate's proposed `fix` names a function, method, type, hook, import path, or package,
verify it exists for this project.

```bash
Grep -rn "<symbolName>"      # the whole workspace, not the package
Read <manifest>              # package.json, Cargo.toml, pyproject.toml, go.mod
```

No in-project usage and not exported by a declared dependency means the fix is hallucinated:
`REFUTED`, `refutation_class: "one-off"`, evidence citing the failed grep and its scope. Grep the
whole workspace before concluding — a symbol often lives in a sibling package.

**The absent-framework refutation.** The repo profile from Phase 1 carries an `ABSENT` line naming
the frameworks, ORMs and APIs the repository does not contain. A candidate whose claim or fix names
one fails this gate immediately, without a grep, because the fix cannot be applied here whatever
the pattern resembled. This is the cheapest refutation in the pipeline and it is why the profile is
inlined into every verifier prompt.

The mechanism has a worked case. A checklist item matching on shape rather than on stack proposed a
guard from one framework in a repo built on another, run after run, until the verifier prompt was
told the framework was absent. A verifier that does not know what is missing cannot refute on it —
so establish the absences in discovery, and pass them down. Where a package is present but unused
on the changed paths, that is not an absence: let Gate 5 handle it as reachability.

### Gate 2 — Version compatibility

If the `claim` cites version-sensitive framework behaviour, confirm the installed version supports
it. Read the relevant app's `package.json`; versions differ per app.

| Claim | Requires |
|---|---|
| `await cookies()`, `await headers()`, `await params` is mandatory | Next.js ≥ 15 |
| `GET` Route Handlers default to dynamic; default `fetch()` is no longer cached | Next.js ≥ 15 |
| `middleware.ts` should be named `proxy.ts` | Next.js ≥ 16 |
| `useActionState` replaces `useFormState`; `ref` is a regular prop and `forwardRef` is unnecessary | React ≥ 19 |
| `setQueryData(key, undefined)` does not clear the entry | `@tanstack/react-query` ≥ 5 |
| `app.enableCors()` / `ValidationPipe` options behave as described | the installed `@nestjs/*` major |
| An ORM method, migration flag or raw-query escape hatch behaves as described | that ORM's installed major |

Two version claims are always repo-local rather than ecosystem-wide, and the profile decides them:
**which tool the gate script actually runs** (a `typecheck` script can be `tsc`, `tsgo`, `vue-tsc`
or a project-references build, and they differ), and **any config branch keyed on an environment
variable**, where a local run and a CI run take different paths through the same file.

A claim the installed version does not support is `REFUTED` or downgraded. A version claim you
cannot resolve is `PLAUSIBLE` with the unresolved version named.

### Gate 3 — Mitigation elsewhere

When the claim is "X is missing", **read the entire file**, not just the cited lines, and check the
mitigating-controls map the orchestrator supplied. The thing the finder thought was missing is
frequently:

- Already imported at the top of the file, or declared 30 lines above the cited range.
- Provided by a global control in the map: a schema parser at the route boundary, the shared
  session or auth helper, a global validation pipe or guard, whatever preamble runs before handler
  logic on a public mutation, a constraint declared on the data model.
- Provided by a parent layout, a wrapper, or a shared handler the route composes.

Two checks before refuting on a control that lives elsewhere. **A route-level control satisfied in
middleware or a proxy is defence in depth, not the control** — a matcher change or a moved handler
silently removes that coverage, so confirm at MEDIUM rather than refute. And **a constraint claimed
on the schema has to be read on the schema**: a declared unique index, enum, `NOT NULL` or check
constraint is a real control; one assumed and never declared is not.

Satisfied anywhere: `REFUTED` with `refutation_class: "globally-mitigated"`, or `"by-design"` when
the behaviour is an intentional convention the repo documents. A tolerant consumer that renders a
fallback rather than throwing is the common by-design case — the instruction files or the contract
doc say so, and where nothing says so it is a finding rather than a convention.

**Say what you read.** Absence of a guard in the file you opened is *not found in what I read*, not
*not present*. Cite the file and the range.

### Gate 4 — Proportionality

If the proposed fix is dramatically larger than the change under review — a new abstraction the
project does not have, renaming or moving several files, over 50 lines for a 10-line diff, a new
dependency in `package.json` — then downgrade `final_severity` and write the smallest incremental
fix into `fix_rewritten`. The report prefers `fix_rewritten` over the original when present, so
skipping it nullifies this gate.

Never refute on Gate 4 alone. The underlying issue may still be real; only the fix was too big.

### Gate 5 — Reachability

Confirm the flawed code is reachable: the function has callers, the route is registered, the
component is rendered, the export has importers.

A real flaw in unreachable code is not a runtime risk — downgrade `final_severity` to LOW and note
"unreachable" in evidence; the dead code itself may warrant a `dead-code` lens finding. Do not
refute on Gate 5 alone.

Framework-magic reachability — all reachable with no direct caller, and all a recurring source of
false "dead code": file-based routes and layouts (Next.js `page`/`route`/`proxy`, Remix, SvelteKit,
Expo Router), decorator or annotation registration (NestJS controllers and providers, Spring beans,
pytest fixtures), DI container registrations, scheduled jobs and queue consumers declared in
deployment config, ORM model registration, and entries in a plugin, command or tool registry. Check
the repo profile before calling any of these unreachable.

### Gate 6 — Observable

**A finding that claims runtime behaviour names the observation behind it.** Either you ran a
command and can quote its invocation and output, or the finding is `PLAUSIBLE` with the confirming
command named.

This gate exists because a declaration and a served result are different things, and reading the
declaration is exactly what proves nothing. `nextjs-checklist.md` §9.7 is the worked case: a `Vary`
header configured in `next.config.ts` that the framework overwrites, invisible in source and
obvious in one `curl -I`. The general rule is that a tool returning success is not evidence the
effect happened.

What counts as an observation for a read-only review: the output of the repo's own typecheck, lint
or test script, a `git` command, a `grep` with its pattern and scope stated, a `curl -I` against a
locally served build. What does not count: a claim that a test would fail, a claim about production
config, an inference from a config file about what is served. Those are `PLAUSIBLE`.

Redact before quoting. Any command output going into the report has secrets replaced with
`<REDACTED>` — cite `file:line` and credential type, never a value. If a redacted output is not
enough to support the finding, say so rather than pasting the unredacted version.

## The verifier's reply

**Reply discipline.** No narration between tool calls, no restating the candidate, no recap before
the JSON. The JSON is the artifact. The one exception is `evidence`, which stays full prose (one to
three sentences citing `file:line`) because the orchestrator copies it verbatim into a report a
person reads.

One JSON line per candidate, in input order, valid NDJSON when batched:

```json
{
  "id": "<id from input>",
  "verdict": "CONFIRMED|PLAUSIBLE|REFUTED",
  "evidence": "<1-3 sentences, cite file:line of what you checked>",
  "confirming_step": "<only when verdict is PLAUSIBLE — the command or observation that would settle it>",
  "final_severity": "CRITICAL|HIGH|MEDIUM|LOW",
  "final_confidence": 90,
  "fix_verified": true,
  "refutation_class": "by-design|globally-mitigated|one-off|null",
  "fix_rewritten": "<only when Gate 4 rewrote the fix — omit the key otherwise>"
}
```

`refutation_class` is `null` unless the verdict is `REFUTED`. `by-design` means an intentional
documented convention; `globally-mitigated` means a repo-wide control covers it, typically a Gate 3
hit; `one-off` means a wrong line, a misread, or a hallucinated fix. The orchestrator persists
`by-design` and `globally-mitigated` to `.code-review/suppressions.jsonl`; it never persists
`one-off`, because a wrong line number today would mask a real bug at that location tomorrow.

`final_confidence` reflects what the verifier learned. The finder's number is a starting point to
raise or lower on evidence.

## Verify only what could reach the report

Verify exactly the candidates that would survive the report threshold if confirmed: CRITICAL and
HIGH at `confidence ≥ 60`, MEDIUM at `≥ 80`, LOW at `≥ 85`. Verifying below-threshold candidates
spends agent budget for zero report impact, and the rule is deterministic — two runs over the same
`candidates.jsonl` verify the same subset.

## Verifier model and fan

Pass `model: "sonnet"` on every verifier call. The work is bounded: read one file, grep one or two
symbols, apply the gates, return JSON. The failure mode at this stage is a missing grep, not
shallow reasoning. Omitting the parameter silently inherits the orchestrator's model and overspends
with no error. If you find yourself arguing that a case is subtle enough to need a larger verifier,
surface it as `PLAUSIBLE` with the confirming step named instead.

Run verifiers in waves of 5 to 8 concurrent `Agent` calls, appending each wave's replies to
`verifications.jsonl` before launching the next. Keep the fan small on purpose: one measured run
went from 23 descendant processes to 74 with three subagents and to 266 with twenty, and resident
memory from 0.2 GiB to 11.7 GiB. Shipped concurrency defaults are ceilings, not recommendations.

## Stage-2 typecheck and gates

Runs after the report filter and before the report, per the depth table in `SKILL.md`. The
orchestrator runs it once against the diff's head, not per verifier. Never at `quick` or prepush,
and always skipped for doc-only diffs (`.md`, `.mdx`, `.txt` with no source change).

Run **the repo's own gate commands**, taken verbatim from the Phase 1 profile — the `scripts`
entries of the touched packages, routed through the task runner where the repo has one:

```bash
<pm> turbo run typecheck --filter <touched-package>...     # a Turborepo workspace
<pm> run typecheck && <pm> run lint && <pm> test           # a single-package repo
cargo check && cargo clippy && cargo test                  # a Rust workspace
```

Invoking a compiler or linter directly gates on a different tool than CI does. `"typecheck": "tsgo
--noEmit"` and `"typecheck": "tsc --noEmit"` are different compilers; `oxlint` and `eslint` catch
different things. Read the script, then run the script.

Diff-introduced type errors become one HIGH finding, "TypeScript errors introduced by the diff",
listing up to 5 representative `file:line: error` tuples and the total count. Lint failing while
typecheck passes is one MEDIUM of the same shape. Do not attempt fixes; the report is read-only.

Pre-existing breakage is not a finding. Confirm it against the base ref before deciding, and suffix
the report's build line `(pre-existing CI red)` instead.

## Anti-patterns in verification

Verifying inside the orchestrator's working memory at `standard` or `deep` — the fresh context is
the mechanism, and a verifier that shares the finder's context is not one. Skipping verification
for an obvious finding, when the most common hallucinations are about things that seem obvious.
Reporting the verification process to the reader rather than the surviving findings plus the stats
line. Using `PLAUSIBLE` as a hedge for "I did not check" — that is a `not-checked` row in the
coverage ledger, and the two mean different things. Padding the verdict with verification
metadata; the verdict is one line and the report ends there.
