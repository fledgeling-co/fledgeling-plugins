# Claude Code built-in code-review prompts

> Extracted from the Claude Code CLI binary at `~/.local/share/claude/versions/2.1.237` on 20 August 2026 with `strings`, then unescaped. This is the architecture the `code-review` skill's depth tiers, finder angles, three-state verify and gap sweep are adapted from. It is not published anywhere; this file is the only citable copy.

```
${t}`;return[{type:"text",text:n}]}})}var kWE="Claude in Chrome browser tools are enabled for this session, but they are not part of this agent context (its tool set was fixed before the browser connection completed, or its agent type does not include them). Do not attempt mcp__claude-in-chrome__* tool calls here — complete the task with the tools this context does have, or report back so the main conversation can drive the browser.",AWE="Claude in Chrome is enabled for this session, but the browser connection is not working (it failed or was disabled), so mcp__claude-in-chrome__* tools are not available. Do not attempt them. Continue the task without browser tools (WebFetch and WebSearch cover read-only web content), or ask the user to perform browser steps manually. The user can retry the connection with /chrome (Reconnect extension).",RWE;var $3g=w(()=>{dU();N3g();KKn();Bxe();Ye();lS();RWE=new Set(["failed","disabled","needs-auth"])});function B3g(e,t){let r=e.trim(),n=r.split(/\s+/,1)[0]??"",o=new Set,i=r;for(let s of t){let a=i.replace(new RegExp(`(?:^|\\s)--${OH(s)}(?=\\s|$)`,"g"),"");if(a!==i)o.add(s),i=a.trim()}return{rawFirstToken:n,flags:o,rest:i}}var U3g=w(()=>{Fr()});function V_s(e){if(e.agentContext&&qk(e.agentContext)>=Iq())return!1;let t=e.options?.tools;if(!t)return!0;return t.some((r)=>ol(r,Ei))}var H8e="## Phase 0 — Gather the diff

Run `git diff @{upstream}...HEAD` (or `git diff main...HEAD` / `git diff HEAD~1`
if there's no upstream) to get the unified diff under review. If there are
uncommitted changes, or the range diff is empty, also run `git diff HEAD` and
include the working-tree changes in scope — the review often runs before the
commit. If a PR number, branch name, or file path was passed as an argument,
review that target instead. Treat this diff as the review scope.
",yEo=`Flag new code that re-implements something the codebase
already has — Grep shared/utility modules and files adjacent to the change,
and name the existing helper to call instead.
`,H0t=`### Simplification
Flag unnecessary complexity the diff adds: redundant or derivable state,
copy-paste with slight variation, deep nesting, dead code left behind. Name
the simpler form that does the same job.
`,N0t=`### Efficiency
Flag wasted work the diff introduces: redundant computation or repeated I/O,
independent operations run sequentially, blocking work added to startup or
hot paths. Also flag long-lived objects built from closures or captured
environments — they keep the entire enclosing scope alive for the object's
lifetime (a memory leak when that scope holds large values); prefer a
class/struct that copies only the fields it needs. Name the cheaper
alternative.
`,ehn=`### Conventions (CLAUDE.md)
Find the CLAUDE.md files that govern the changed code: the user-level
~/.claude/CLAUDE.md, the repo-root CLAUDE.md, plus any CLAUDE.md or
CLAUDE.local.md in a directory that is an ancestor of a changed file (a
directory's CLAUDE.md only applies to files at or below it). Read each one
that exists, then check the diff for clear violations of the rules they state.
Only flag a violation when you can quote the exact rule and the exact line
that breaks it — no style preferences, no vague "spirit of the doc"
inferences. In the finding, name the CLAUDE.md path and quote the rule so the
report can cite it. If no CLAUDE.md applies, return nothing for this angle.
`,F0t=`### Altitude
Check that each change is implemented at the right depth, not as a fragile
bandaid. Special cases layered on shared infrastructure are a sign the fix
isn't deep enough — prefer generalizing the underlying mechanism over adding
special cases.
`;var _Eo=w(()=>{Ts();YJe();ey();gh()});function b3c({tag:e,leadIn:t,angleCount:r,angles:n,cap:o,output:i,sweepFocus:s}){let a=s?`
## Phase 3 — Sweep for gaps
Take one more pass yourself (same context, no subagent) as a fresh reviewer
who has the deduplicated list. Re-read the diff and enclosing functions
looking ONLY for defects not already listed: ${s}
`:"";return``${e}`
${UWE}
${H8e}## Phase 1 — Find candidates (${r} angles, single pass)
Work through **${r} angles** yourself, in sequence, in this same
context — do not spawn subagents. Each surfaces candidate findings with
`file`, `line`, a one-line `summary`, and a concrete `failure_scenario`.
${JEr}
## Phase 2 — Dedup and self-check (no subagent verify)
Dedup near-duplicates (same defect, same location, same reason → keep one).
Re-check each remaining candidate yourself against the diff before keeping it.
${i(o)}${jWE}`}var PWE=`### Angle A — line-by-line diff scan
Read every hunk in the diff, line by line. Then Read the enclosing function for
each hunk — bugs in unchanged lines of a touched function are in scope (the PR
re-exposes or fails to fix them). For every line ask: what input, state, timing,
or platform makes this line wrong? Look for inverted/wrong conditions,
off-by-one, null/undefined deref, missing `await`, falsy-zero checks,
wrong-variable copy-paste, error swallowed in catch, unescaped regex metachars.
`,OWE=`### Angle B — removed-behavior auditor
For every line the diff DELETES or replaces, name the invariant or behavior it
enforced, then search the new code for where that invariant is re-established.
If you can't find it, that's a candidate: a removed guard, a dropped error
path, a narrowed validation, a deleted test that was covering a real case.
`,DWE=`### Angle C — cross-file tracer
For each function the diff changes, find its callers (Grep for the symbol) and
check whether the change breaks any call site: a new precondition, a changed
return shape, a new exception, a timing/ordering dependency. Also check callees:
does a parallel change in the same PR make a call unsafe?
`,MWE=`### Angle D — language-pitfall specialist
Scan for the classic pitfalls of the diff's language/framework — for example:
JS falsy-zero, `==` coercion, closure-captured loop var; Python mutable default
args, late-binding closures; Go nil-map write, range-var capture; SQL injection;
timezone/DST drift; float equality. Flag any instance the diff introduces.
`,LWE=`### Angle E — wrapper/proxy correctness
When the PR adds or modifies a type that wraps another (cache, proxy, decorator,
adapter): check that every method routes to the wrapped instance and not back
through a registry/session/global — e.g. a caching provider holding a
`delegate` field that resolves IDs via `session.get(...)` instead of
`delegate.get(...)` will re-enter the cache or recurse. Also check that the
wrapper forwards all the methods the callers actually use.
`,_3c,z3g,HWE,q3g,JEr="Cleanup, altitude, and conventions candidates use the same
`file`/`line`/`summary` shape; in `failure_scenario`, state the concrete
cost (what is duplicated, wasted, harder to maintain, or which CLAUDE.md rule
is broken) instead of a crash. Correctness bugs always outrank cleanup,
altitude, and conventions findings when the output cap forces a cut.
",NWE=`- **CONFIRMED** — can name the inputs/state that trigger it and the wrong
  output or crash. Quote the line.
- **PLAUSIBLE** — mechanism is real, trigger is uncertain (timing, env,
  config). State what would confirm it.
- **REFUTED** — factually wrong (code doesn't say that) or guarded elsewhere.
  Quote the line that proves it.`,FWE=`**PLAUSIBLE by default** — do not refute a candidate for being "speculative" or
"depends on runtime state" when the state is realistic: concurrency races,
nil/undefined on a rare-but-reachable path (error handler, cold cache, missing
optional field), falsy-zero treated as missing, off-by-one on a boundary the
code does not exclude, retry storms / partial failures, regex/allowlist that
lost an anchor. These are PLAUSIBLE.
**REFUTED** only when constructible from the code: factually wrong (quote the
actual line); provably impossible (type/constant/invariant — show it); already
handled in this diff (cite the guard); or pure style with no observable effect.`,W3g,$WE,G3g=`moved/extracted code that dropped a guard
or anchor; second-tier footguns (dataclass default evaluated once, `hash()`
non-determinism, lock-scope shrink, predicate methods with side effects);
setup/teardown asymmetry in tests; config defaults flipped.`,BWE,V3g=(e)=>`## Output
Return findings as a JSON array of at most ${e} objects:
```json
    "file": "path/to/file.ext",
    "line": 123,
    "summary": "one-sentence statement of the bug",
    "failure_scenario": "concrete inputs/state → wrong output/crash"
```
Ranked most-severe first. If more than ${e} survive, keep the ${e} most
severe. If nothing survives verification, return `[]`. Do not call the
${j7} tool even if it is available - this review's
output contract is the JSON block above.
`,K3g=(e)=>`## Output
Call the ${j7} tool once to report this review's results
with `{level, findings}`. `findings` is at most ${e} entries ranked
most-severe first; each entry has `file`, `line`, `summary`,
`short_summary` — the claim compressed to ≤60 characters, no rationale
or consequence clause — `failure_scenario`, and `category` — a short kebab-case slug for the angle
that produced it (`correctness`, `simplification`, `efficiency`,
`reuse`, `altitude`, `conventions`, or a more specific slug like
`test-coverage` when one fits better) — plus `verdict` when a verify pass
produced one. If more than ${e} survive, keep the ${e} most severe. If
nothing survives verification, call it with an empty array. Do not also print
the findings as text, and do not create or publish an artifact of the review -
the tool call is the report.
`,Y3g=(e)=>``low effort → 1 diff pass → no verify → ≤4 findings`
## Turn 1 — read
One tool call: read the unified diff (`git diff @{upstream}...HEAD; git diff HEAD`
to cover both committed and uncommitted changes, or `git diff main...HEAD` /
the target passed as an argument). Skip test/fixture
hunks (`test/`, `spec/`, `__tests__/`, `*_test.*`, `*.test.*`,
`fixtures/`, `testdata/`) — test-file changes are not reviewed at this level.
No subagents, no full-file reads.
## Turn 2 — findings
Flag runtime-correctness bugs visible from the hunk alone: inverted/wrong
condition, off-by-one, null/undefined deref where adjacent lines show the value
can be absent, removed guard, falsy-zero check, missing `await`,
wrong-variable copy-paste, error swallowed in a catch that should propagate.
Also flag — still from the hunk alone — new code that duplicates an existing
helper visible in the diff context, and dead code the diff leaves behind.
Do **not** flag style, naming, perf, missing tests, or anything outside the
${e?`Report at most **4 findings**, most-severe first, in one
${j7} call with `{level, findings}` — each entry has
`file`, `line`, `summary`, `short_summary` (≤60 characters), and
`failure_scenario`. If nothing qualifies, call it with an empty findings
array. Do not also print the findings as text.
`:`Output at most **4 findings**, most-severe first, one line each:
`path/to/file.ext:123 — what's wrong and the concrete failure`. If nothing
qualifies, output exactly `(none)`. Do not call the
${j7} tool even if it is available.
`}`,J3g=(e)=>``low effort → 1 diff pass → no verify → ≥min(files,4) findings`
## Turn 1 — read
One tool call: read the unified diff (`git diff @{upstream}...HEAD; git diff HEAD`
to cover both committed and uncommitted changes, or `git diff main...HEAD` /
the target passed as an argument). Skip test/fixture
hunks (`test/`, `spec/`, `__tests__/`, `*_test.*`, `*.test.*`,
`fixtures/`, `testdata/`) — test-file changes are not reviewed at this level.
No subagents, no full-file reads.
## Turn 2 — findings
Flag runtime-correctness bugs visible from the hunk alone: inverted/wrong
condition, off-by-one, null/undefined deref where adjacent lines show the value
can be absent, removed guard, falsy-zero check, missing `await`,
wrong-variable copy-paste, error swallowed in a catch that should propagate.
Also flag — still from the hunk alone — new code that duplicates an existing
helper visible in the diff context, and dead code the diff leaves behind.
Do **not** flag style, naming, perf, missing tests, or anything outside the
${e?`Target **min(files_changed, 4) findings**, most-severe first, reported
in one ${j7} call with `{level, findings}` — each
entry has `file`, `line`, `summary`, `short_summary` (≤60 characters),
and `failure_scenario`. If you have fewer, do one more pass focused on the
largest changed file and on any **removed** code blocks. Call it with an
empty findings array only if the diff is trivially correct after that pass.
Do not also print the findings as text.
`:`Target **min(files_changed, 4) findings**, most-severe first, one
line each: `path/to/file.ext:123 — what's wrong and the concrete failure`.
If you have fewer, do one more pass focused on the largest changed file
and on any **removed** code blocks. Output `(none)` only if the diff is
trivially correct after that pass.
`}`,K_s,UWE,jWE,X3g=(e,t=!0)=>{if(!t)return b3c({tag:`medium effort → ${Ei} tool unavailable → single-pass inline → ≤8 findings`,leadIn:`You are reviewing for **precision** at medium effort: every finding you surface
should be one a maintainer would act on.`,angleCount:8,angles:K_s,cap:8,output:e});return``medium effort → 3+5 angles \xD7 6 candidates → 1-vote verify → ≤8 findings`
You are reviewing for **precision** at medium effort: every finding you surface
should be one a maintainer would act on.
${H8e}
## Phase 1 — Find candidates (3 correctness angles + 3 cleanup angles + 1 altitude angle + 1 conventions angle, up to 6 each)
Run **8 independent finder angles** via the ${Ei} tool. Each
surfaces **up to 6 candidate findings** with `file`, `line`, a one-line
`summary`, and a concrete `failure_scenario`. ${_3c}
${K_s}
${JEr}
Pass every candidate with a nameable failure scenario through — finders that
silently drop half-believed candidates bypass the verify step and are the
dominant cause of misses.
${W3g}
${e(8)}`},Z3g=(e,t=!0)=>{if(!t)return b3c({tag:`high effort → ${Ei} tool unavailable → single-pass inline → ≤10 findings`,leadIn:`You are reviewing for **recall** at high effort: catch every real bug a careful
reviewer would catch in one sitting. At this level, catching real bugs matters
more than avoiding false positives. Err on the side of surfacing.`,angleCount:8,angles:K_s,cap:10,output:e});return``high effort → 3+5 angles \xD7 6 candidates → 1-vote verify (recall-biased) → ≤10 findings`
You are reviewing for **recall** at high effort: catch every real bug a careful
reviewer would catch in one sitting. At this level, catching real bugs matters
more than avoiding false positives. Err on the side of surfacing.
${H8e}
## Phase 1 — Find candidates (3 correctness angles + 3 cleanup angles + 1 altitude angle + 1 conventions angle, up to 6 each)
Run **8 independent finder angles** via the ${Ei} tool. Each
surfaces **up to 6 candidate findings** with `file`, `line`, a one-line
`summary`, and a concrete `failure_scenario`. ${_3c}
${K_s}
${JEr}
Pass every candidate with a nameable failure scenario through — finders that
silently drop half-believed candidates bypass the verify step and are the
dominant cause of misses.
${$WE}
${e(10)}`},j3g,Q3g=(e)=>(t,r=!0)=>{if(!r)return b3c({tag:`${e} effort → ${Ei} tool unavailable → single-pass inline → ≤15 findings`,leadIn:`You are reviewing for **recall** at ${e==="max"?"maximum":"extra-high"} effort: catch every real bug. At
this level, catching real bugs matters more than avoiding false positives — a
missed bug ships. Err on the side of surfacing.`,angleCount:10,angles:j3g,cap:15,output:t,sweepFocus:G3g});return``${e} effort → 5+5 angles \xD7 8 candidates → 1-vote verify → sweep → ≤15 findings`
You are reviewing for **recall** at ${e==="max"?"maximum":"extra-high"} effort: catch every real bug. At
this level, catching real bugs matters more than avoiding false positives — a
missed bug ships. Err on the side of surfacing.
${H8e}
## Phase 1 — Find candidates (5 correctness angles + 3 cleanup angles + 1 altitude angle + 1 conventions angle, up to 8 each)
Run **10 independent finder angles** via the ${Ei} tool. Each
surfaces **up to 8 candidate findings**. Do NOT let one angle's conclusions
suppress another's — if two angles flag the same line for different reasons,
record both. ${_3c}
${j3g}
${JEr}
${W3g}
This is recall mode — a single non-REFUTED vote carries the finding. Do NOT
drop on uncertainty.
${BWE}
${t(15)}`},ezg,tzg;var S3c=w(()=>{ey();_Eo();_3c=`If the ${Ei} tool is not available in your current tool set, do not error — perform each angle (and each verification) yourself, sequentially, in this context.`,z3g=`${PWE}
${OWE}
${DWE}`,HWE=`${z3g}
${MWE}
${LWE}`,q3g=`### Reuse
The angles above hunt for bugs; this one and the next two hunt for cleanup in
the changed code. ${yEo}`,W3g=`## Phase 2 — Verify (1-vote, 3-state)
Dedup candidates that point at the same line/mechanism, keeping the one with
the most concrete failure scenario. For each remaining candidate, run **one
verifier** via the ${Ei} tool: give it the diff, the relevant
file(s), and the candidate, and have it return exactly one of:
${NWE}
Keep candidates where the vote is CONFIRMED or PLAUSIBLE.
`,$WE=`## Phase 2 — Verify (1-vote, recall-biased)
Dedup near-duplicates (same defect, same location, same reason → keep one). For
each remaining candidate, run **one verifier** via the ${Ei} tool:
give it the diff, the relevant file(s), and the candidate; it returns exactly
one of **CONFIRMED / PLAUSIBLE / REFUTED**.
${FWE}
Keep **CONFIRMED and PLAUSIBLE**. Drop REFUTED.
`,BWE=`## Phase 3 — Sweep for gaps
Run **one more finder** as a fresh reviewer who has the verified list. Re-read
the diff and enclosing functions looking ONLY for defects not already listed.
Do not re-derive or re-confirm anything already there — the job is gaps. Focus
on what the first pass tends to miss: ${G3g}
Surface **up to 8 additional candidates**, each naming a defect not already on
the list. If nothing new, return an empty sweep — do not pad.
`,K_s=`${z3g}
${q3g}
${H0t}
${N0t}
${F0t}
${ehn}`,UWE=`The ${Ei} tool isn't available in this context, so the usual
multi-agent fan-out and subagent verify pass can't run. Work through every
angle below yourself, in this same context, in one pass — do not skip angles
for lack of fan-out. Re-check each candidate against the diff before keeping
it; drop anything you can't back up with a concrete failure scenario.
`,jWE=`
State clearly in your summary that this was a single-pass review done without
the ${Ei} tool, not the full multi-agent fan-out, so whoever reads
it isn't misled about what actually ran.
`;j3g=`${HWE}
${q3g}
${H0t}
${N0t}
${F0t}
${ehn}`,ezg=Q3g("xhigh"),tzg=Q3g("max")});var rzg=`### Reuse
The angles above hunt for bugs; this one and the next two hunt for cleanup in
the changed code. Flag new code that re-implements something the codebase
already has — Grep shared/utility modules and files adjacent to the change,
and name the existing helper to call instead.
`,nzg=(e)=>``low effort → 1 diff pass → no verify → ≤8 findings`
## Turn 1 — read
One tool call: read the unified diff (`git diff @{upstream}...HEAD; git diff HEAD`
to cover both committed and uncommitted changes, or `git diff main...HEAD` /
the target passed as an argument). No subagents, no full-file reads.
## Turn 2 — findings
Flag runtime-correctness bugs visible from the hunk alone: inverted/wrong
condition, off-by-one, null/undefined deref where adjacent lines show the value
can be absent, removed guard, falsy-zero check, missing `await`,
wrong-variable copy-paste, error swallowed in a catch that should propagate.
Also flag — still from the hunk alone — new code that duplicates an existing
helper visible in the diff context, and dead code the diff leaves behind.
Do **not** flag style, naming, perf, missing tests, or anything outside the
${e?`Report at most **8 findings**, most-severe first, in one
${j7} call with `{level, findings}` — each entry has
`file`, `line`, `summary`, `short_summary` (≤60 characters), and
`failure_scenario`.
Target at least min(files_changed, 4) findings — if you see fewer, widen to other hunks in the same diff before stopping. If fewer than 4 genuine findings exist, report what you have. Do not also print the findings as text.
`:`Output at most **8 findings**, most-severe first, one line each:
`path/to/file.ext:123 — what's wrong and the concrete failure`.
Target at least min(files_changed, 4) findings — if you see fewer, widen to other hunks in the same diff before stopping. If fewer than 4 genuine findings exist, emit what you have.
`}`,ozg=(e)=>(t)=>e(t).replace(`## Output
`,`## Output
Target **at least ${Math.floor(t/2)} findings**. If fewer genuine findings exist, emit what you have — do not invent to hit the floor.
`).replace(/nothing survives verification/g,"nothing survives"),izg=`### Angle A — line-by-line diff scan
Read every hunk in the diff, line by line. Then Read the enclosing function for
each hunk — bugs in unchanged lines of a touched function are in scope (the PR
re-exposes or fails to fix them). For every line ask: what input, state, timing,
or platform makes this line wrong? Look for inverted/wrong conditions,
off-by-one, null/undefined deref, missing `await`, falsy-zero checks,
wrong-variable copy-paste, error swallowed in catch, unescaped regex metachars.
### Angle B — removed-behavior auditor
For every line the diff DELETES or replaces, name the invariant or behavior it
enforced, then search the new code for where that invariant is re-established.
If you can't find it, that's a candidate: a removed guard, a dropped error
path, a narrowed validation, a deleted test that was covering a real case.
### Angle C — cross-file tracer
For each function the diff changes, find its callers (Grep for the symbol) and
check whether the change breaks any call site: a new precondition, a changed
return shape, a new exception, a timing/ordering dependency. Also check callees:
does a parallel change in the same PR make a call unsafe?
`,szg=(e,t,r)=>(n)=>``${e}`
${H8e}
## Phase 1 — Find candidates (3 correctness angles + 3 cleanup angles + 1 altitude angle + 1 conventions angle, up to 6 each)
Run **8 independent finder angles** in sequence yourself, in THIS context — do NOT spawn subagents for them. Each
surfaces **up to 6 candidate findings** with `file`, `line`, a one-line
`summary`, and a concrete `failure_scenario`.
${izg}
${rzg}
${H0t}
${N0t}
${F0t}
${ehn}
${JEr}
Pass every candidate with a nameable failure scenario through — finders that
silently drop half-believed candidates are the dominant cause of misses.
## Phase 2 — Dedup only (no verify)
Pool all candidates. Dedup near-duplicates only (same defect, same location, same reason → keep one). Do NOT run verifiers; do NOT re-judge. Sort by severity.
${ozg(n)(r)}`,azg,lzg,zWE=(e)=>``xhigh effort → 10 inline angles → dedup (no verify) → sweep → ≤15 findings`
You are reviewing for **recall** at extra-high effort: catch every real bug. At
this level, catching real bugs matters more than avoiding false positives — a
missed bug ships. Err on the side of surfacing.
${H8e}
## Phase 1 — Find candidates (5 correctness angles + 3 cleanup angles + 1 altitude angle + 1 conventions angle, up to 8 each)
Run **10 independent finder angles** in sequence yourself, in THIS context — do NOT spawn subagents for them. Each
surfaces **up to 8 candidate findings**. Do NOT let one angle's conclusions
suppress another's — if two angles flag the same line for different reasons,
record both.
${izg}
### Angle D — language-pitfall specialist
Scan for the classic pitfalls of the diff's language/framework — for example:
JS falsy-zero, `==` coercion, closure-captured loop var; Python mutable default
args, late-binding closures; Go nil-map write, range-var capture; SQL injection;
timezone/DST drift; float equality. Flag any instance the diff introduces.
### Angle E — wrapper/proxy correctness
When the PR adds or modifies a type that wraps another (cache, proxy, decorator,
adapter): check that every method routes to the wrapped instance and not back
through a registry/session/global — e.g. a caching provider holding a
`delegate` field that resolves IDs via `session.get(...)` instead of
`delegate.get(...)` will re-enter the cache or recurse. Also check that the
wrapper forwards all the methods the callers actually use.
${rzg}
${H0t}
${N0t}
${F0t}
${ehn}
${JEr}
## Phase 2 — Dedup only (no verify)
Pool all candidates. Dedup near-duplicates only (same defect, same location, same reason → keep one). Do NOT run verifiers; do NOT re-judge. Sort by severity. Do NOT drop on uncertainty.
## Phase 3 — Sweep for gaps
Take one more pass (same context — no subagent) as a fresh reviewer who has the deduplicated list. Re-read
the diff and enclosing functions looking ONLY for defects not already listed.
Do not re-derive or re-confirm anything already there — the job is gaps. Focus
on what the first pass tends to miss: moved/extracted code that dropped a guard
or anchor; second-tier footguns (dataclass default evaluated once, `hash()`
non-determinism, lock-scope shrink, predicate methods with side effects);
setup/teardown asymmetry in tests; config defaults flipped.
Surface **up to 8 additional candidates**, each naming a defect not already on
the list. If nothing new, return nothing from this phase — do not pad.
${ozg(e)(15)}`,czg;var uzg=w(()=>{S3c();_Eo();azg=szg("medium effort → 8 inline angles → dedup (no verify) → ≤8 findings",`You are reviewing for **correctness bugs**: surface every plausible bug. At this
level, catching real bugs matters more than avoiding false positives — err on
the side of surfacing.`,8),lzg=szg("high effort → 8 inline angles → dedup (no verify) → ≤10 findings",`You are reviewing for **recall** at high effort: catch every real bug a careful
reviewer would catch in one sitting. At this level, catching real bugs matters
more than avoiding false positives. Err on the side of surfacing.`,10),czg=zWE});var dzg;var pzg=w(()=>{dzg=``minimal prompt → single careful diff pass → ≤15 findings`
You are reviewing a pull request for real bugs. Run `git diff @{upstream}...HEAD` (or `git diff main...HEAD` / `git diff HEAD~1`
if there's no upstream) to get the unified diff under review. If there are
uncommitted changes, or the range diff is empty, also run `git diff HEAD` and
include the working-tree changes in scope — the review often runs before the
commit. If a PR number, branch name, or file path was passed as an argument,
review that target instead. Treat this diff as the review scope.
Review the diff as a careful senior engineer would: read every hunk, open the surrounding files for context as needed (Read, Grep, git log/blame/show), and hunt for correctness issues — wrong or inverted conditions, off-by-one, null/undefined dereference, missing `await`, dropped error handling, removed guards or validations, broken callers of changed functions, races. Prefer real failure modes over style; every finding needs a concrete scenario in which the code misbehaves.
When you are done, submit at most 15 findings via the ${j7} tool, filling its fields as defined — for each: the file path and start line, a severity, and a comment that states the issue and the concrete scenario in which the code misbehaves. Quality over quantity: include everything you genuinely believe is a real issue, and nothing you don't.
After the tool call, also restate the findings in your final reply — one line each, `file:line — summary` — so they stay visible in sessions that do not render tool output.
`});function qWE(e){return Object.hasOwn(thn,e)}function J_s(e){let t=e?Do(al(e)):void 0;return t&&qWE(t)?t:"default"}function T3c(e,t){let r=thn[e][t];return r.modelEffort==="typed"?t:r.modelEffort}function KWE(e,t,r=!0,n=!1){switch(e){case"low":return Y3g(n);case"low-sonnet5":return J3g(n);case"medium":return X3g(t,r);case"high":return Z3g(t,r);case"xhigh":return ezg(t,r);case"max":return tzg(t,r);case"o48-low-v1":return nzg(n);case"o48-med-v1":return azg(t);case"o48-high-v1":return lzg(t);case"o48-xhigh-v1":return czg(t);case"o5-bmin":return dzg}}function mzg(e){if(e.options?.isSkillPreload)return!1;let t=Zxs();if(t==="text"||t==="json")return!1;return Boolean(G.CLAUDE_CODE_REPORT_FINDINGS)&&Boolean(e.options?.tools?.some((r)=>ol(r,j7)))}function XWE(e){return`
## Applying fixes (--fix)
The `--fix` flag was passed. After producing the findings list, apply the
findings to the working tree instead of stopping at the report: fix each one
directly — correctness bugs and reuse/simplification/efficiency cleanups alike.
Skip any finding whose fix would change intended behavior, require changes well
outside the reviewed diff, or that you judge to be a false positive — note the
skip rather than arguing with it. ${e?`Then ${hzg}; after the call, give one line per skipped finding saying why.`:`Finish with a brief summary of what was fixed
and what was skipped.`}
`}async function QWE(e){if(e.options?.isSkillPreload)return"";if(!VLr())return"";let t=e.options?.tools;if(t&&!Smt()&&!t.some((n)=>ol(n,th)))return"";return(await T2t(el())).some((n)=>n.name===Ipe)?ZWE:""}function v3c(e){let[t="",...r]=e;return[t.replaceAll("`","").replace(/^#/,""),...r].filter(Boolean).join(" ")}function Y_s(e){let{rawFirstToken:t,flags:r,rest:n}=B3g(e,["comment","fix","post","no-post"]),o=r.has("comment"),i=r.has("fix"),s=r.has("post"),a=n.split(/\s+/).filter(Boolean),l=a[0]??"";if(t.toLowerCase()==="ultra")return{explicit:void 0,target:v3c(a.slice(1)),comment:o,fix:i,post:s,unrecognizedLevel:void 0,ultraFallback:!0};let c=l.toLowerCase()==="ultra"?void 0:PZt(l);if(c!==void 0)return{explicit:c,target:v3c(a.slice(1)),comment:o,fix:i,post:s,unrecognizedLevel:void 0,ultraFallback:!1};let u=eGE.test(l);return{explicit:void 0,target:v3c(a),comment:o,fix:i,post:s,unrecognizedLevel:u?l:void 0,ultraFallback:!1}}function tGE(){let e=ar().codeReviewLastEffort;return e!==void 0&&hpe(e)?e:void 0}function rGE(e,t){sn((r)=>r.codeReviewLastEffort===e?r:{...r,codeReviewLastEffort:e},t)}function w3c({explicit:e,ultraFallback:t},r){if(r?.options?.isSkillPreload)return;return e===void 0&&!t?tGE():void 0}function nGE(){let e=Air()?`; ultra: deep multi-agent review in the cloud${Are()?"":" (requires claude.ai account access)"}`:"",t=Air()?" For ultra on a GitHub.com PR target, --post asks to post the finished review’s findings to the PR as a single comment from the user’s GitHub account (not a review; the launch dialog still confirms in interactive sessions, while non-interactive mode posts on the flag alone) and --no-post hides that option.":"";return`Review the current diff, or a PR number/branch/path target, for correctness bugs and reuse/simplification/efficiency cleanups at the given effort level (low/medium: fewer, high-confidence findings; high→max: broader coverage, may include uncertain findings${e}); with no level given, it reuses the level you typed last. Pass --comment to post findings as inline PR comments, or --fix to apply the findings to the working tree after the review.${t}`}function oGE(){return`[${Air()?`${bEo.join("|")}|ultra`:bEo.join("|")}] [--fix] [--comment] [<pr#>|<branch>|<path>]`}async function iGE(e,t){let r=Y_s(e),{explicit:n,target:o,comment:i,fix:s,post:a,unrecognizedLevel:l,ultraFallback:c}=r,u=w3c(r,t),d=gzg(r,t),p=t.options?GD(t):void 0,f=J_s(p),m=t.options?.isSkillPreload&&WWE.has(f)?"default":f,h=thn[m][d],g=mzg(t),y=!g,_=g?K3g:V3g,S=h.cell==="o5-bmin",v=!y&&!h.measuredExternal?await QWE(t):"",E=lGE({ultraFallback:c,fix:s,post:a,comment:i,unrecognizedLevel:l,lastUsed:u,level:d,willRunAsFork:y,context:t}),C=V_s(t),k={text:""};if(!t.options?.isSkillPreload){if(C)k=await sGE(p,d,o);let I=n??u;N("tengu_code_review_routed",{effort_level:me(d),effort_source:me(n!==void 0?"explicit":u!==void 0?"last_used":c?"ultra_fallback":"session"),routed_to_workflow:!1,uses_report_findings_tool:g,has_fix:s,has_comment:i,has_target:o.length>0,is_ultra_fallback:c,low_variant:d==="low"?me(GWE[m]??"default"):void 0,model_family:me(m),finder_budget:k.budget,agent_tool_available:C,threaded_effort:I!==void 0?me(T3c(m,I)):void 0})}let A=t.options?.isSkillPreload||t.agentId!==void 0||c||y||h.measuredExternal?null:ehm(),R=A!==null?`
After you finish the review, end your response with this exact line on its own:
${A}`:"",P=o?`Review target: `${o}`
`:"";return[{type:"text",text:`${E}${P}${k.text}${KWE(h.cell,_,C,g)}${i?YWE:""}${s?XWE(g):""}${g&&!S?JWE:""}${v}${R}`}]}async function sGE(e,t,r){if(!thn[J_s(e)][t].finderBudgetHint)return{text:""};let n=await aGE(r);if(n===void 0)return{text:""};let o=Math.max(2,Math.min(8,Math.ceil(n/150)));if(!r)return{text:`The committed diff (@{upstream}...HEAD) is about ${n} lines. Uncommitted changes aren't counted here, so treat this as a floor — start with about ${o} finder subagents (min 2, max 8) and scale up if Phase 0 finds additional working-tree scope.
`,budget:o};return{text:`This diff is about ${n} lines. Spawn about ${o} finder subagents (min 2, max 8) — scale your investigation depth to the diff size rather than using a fixed large fleet.
`,budget:o}}async function aGE(e){let t;if(!e)t="@{upstream}...HEAD";else if(e.length<=256&&/^[@\w][@\w./~^-]*\.\.\.?[@\w][@\w./~^-]*$/.test(e))t=e;else return;try{let{stdout:r,code:n}=await Kn(Ho(),["-c","core.hooksPath=/dev/null","-c","core.fsmonitor=","-c","core.askPass=","diff","--no-ext-diff","--no-textconv","--numstat","--end-of-options",t,"--"],{timeout:5000,useCwd:!0,env:{...process.env,[["SELF_HOSTED","RUNNER_POOL_SECRET"].join("_")]:void 0,[["SELF_HOSTED","RUNNER_ENVIRONMENT_SECRET"].join("_")]:void 0,GIT_ALLOW_PROTOCOL:"none",GIT_NO_LAZY_FETCH:"1",GIT_SSH_COMMAND:"ssh -o BatchMode=yes",GIT_TERMINAL_PROMPT:"0"}});if(n!==0)return;let o=0;for(let i of r.split(`
`)){let s=i.match(/^(\d+)\t(\d+)\t/);if(s)o+=Number(s[1])+Number(s[2])}return o>0?o:void 0}catch{return}}function gzg(e,t){let{explicit:r,ultraFallback:n}=e,o=n?"max":r??w3c(e,t),i=t.options?GD(t):void 0,s=i?RX(i,o??PS(t))??o:o??PS(t);return s===void 0?"medium":l4e(s)}function lGE({ultraFallback:e,fix:t,post:r,comment:n,unrecognizedLevel:o,lastUsed:i,level:s,willRunAsFork:a,context:l}){let c=(p)=>r?n?`${p}(The typed `--post` applies only to the `/code-review ultra` cloud review and was ignored — when the target is a GitHub PR, your `--comment` is what posts the findings as inline PR comments. Tell the user this in one short line.)
`:`${p}(The typed `--post` applies only to the `/code-review ultra` cloud review and was ignored — this local review will not post to GitHub; `--comment` is the flag that posts local findings as inline PR comments. Tell the user this in one short line.)
`:p;if(e){if(!Are()){if(t)return c(`(Running a local ${s}-effort review and applying its findings.)
`);if(Air()){if(l.options?.isNonInteractiveSession){let f=wdi();if(f)return c(`(${f} Falling back to a local ${s}-effort review.)
`)}return c(`(ultra (cloud review) requires claude.ai account access this session doesn't have — see https://code.claude.com/docs/en/ultrareview. Falling back to a local ${s}-effort review.)
`)}return c(`(ultra (cloud review) isn't available in this environment — see https://code.claude.com/docs/en/ultrareview. Falling back to a local ${s}-effort review.)
`)}let p=l.options?.commands?.some((f)=>f.name==="ultrareview"&&PO(f))??!1;if(t)return c(p?`(Claude can't launch the cloud review directly — type `/code-review ultra --fix` to review in the cloud and apply the findings locally when it completes. Running a local ${s}-effort review and applying its findings for now.)
`:`(Running a local ${s}-effort review and applying its findings.)```
