# Output format

This file defines the only valid finding format, the report's structure, and the only valid verdict
lines. Deviation makes the report unparseable for downstream tooling and breaks a developer's
ability to triage at speed.

**Prepush mode** has its own leaner contract and verdict set (`PUSH` / `PUSH WITH CARE` /
`DO NOT PUSH`) in `prepush.md`. The finding schema below applies to prepush blockers; the header,
stats lines, coverage ledger and report-file rules do not.

## What this review may claim

A review is evidence for a decision, not the decision. Keep three tiers apart in your own head and
in the report's wording, because a report that reads as sign-off invites a reader to confirm rather
than to check.

- **The review closes:** structural conformance to a stated rule — a checklist item with a quoted
  line, a convention breach with the governing file quoted, a type-level or shape-level defect
  visible in the source. These report as findings with a fix.
- **A deterministic gate closes:** whether the branch typechecks, lints, passes its tests, and
  whether the contract guards still hold. The review runs those commands and reports their output;
  it does not substitute judgement for them.
- **A person keeps:** whether this is the right change, what the product owes its users, what risk
  is acceptable to ship, and how to weigh a `PLAUSIBLE` finding. None of these has an oracle in the
  repo.

Two consequences for wording. A `PLAUSIBLE` finding states what would confirm it rather than
asserting the failure, so the reader can disagree with the evidence rather than only with the
verdict — pre-populating a reviewer's queue with a machine verdict and asking for confirmation is
the one intervention the medical-imaging literature measures as making reviewers worse, with
specificity falling from 90.2% to 87.2% across 429,345 scans in one study and reader sensitivity
significantly lower with the aid in another. And the verdict line describes the findings, not the
merge decision — `BLOCK` means a CRITICAL finding exists, not that a human has decided.

## Severity taxonomy

| Tag | Meaning | Action |
|---|---|---|
| `CRITICAL` | Security vulnerability, data loss, a leaked secret, or a guaranteed crash on the happy path. Cannot ship as-is. | Block. |
| `HIGH` | A logic bug under realistic input; a cross-app contract broken without its twin and guard updated; missing authn or authz on a sensitive operation; a hydration mismatch guaranteed under SSR; a missing exhaustiveness check on a union the diff just extended; a guard test weakened in the same commit as the code it guards. | Request changes. |
| `MEDIUM` | An architectural smell that will compound (a new `any`, a third way of doing data fetching, a secret read in a Client Component file inside a function no client imports); missing test coverage on a non-trivial change; a performance bug under expected load. | Approve with comments. |
| `LOW` | A minor optimization or a readability improvement beyond what a linter catches. Use sparingly — more than two LOW findings in one review is over-reporting. | Optional. |

Calibration: between two tiers, take the lower one. Performance is not CRITICAL unless it is a
guaranteed denial of service, such as an unbounded loop on user input. Missing test coverage alone
is MEDIUM, never HIGH — HIGH is for code that misbehaves at runtime, not for absent verification.
Stylistic preferences are not a tier; they are not findings.

## Finding format

Each finding uses exactly this structure. The outer fence is `~~~` so the inner ` ```ts ` survives.

~~~
### [SEVERITY] One-sentence title in imperative mood

**File:** `path/to/file.ts:42` (or `:42-58` for a range)

**Issue:** Two or three sentences. Quote the exact problematic code inline where it fits on one
line. Name the rule violated and why it matters in this specific context.

**Fix:**
```ts
// the smallest code change that resolves the issue
```

**Verdict:** CONFIRMED · **Confidence:** 90
~~~

For a `PLAUSIBLE` finding, the verdict line carries the confirming step:

```
**Verdict:** PLAUSIBLE — confirm with `<the repo's own test command, scoped to the file>` · **Confidence:** 65
```

**Which fix snippet to use**, in order: the verifier's `fix_rewritten` if present; otherwise the
candidate's original `fix` when `fix_verified: true`. There is no third case — a candidate with
`fix_verified: false` and no `fix_rewritten` keeps its `**Issue:**` paragraph and replaces the fix
block with the italicised note *"No reliable fix — the original fix named a symbol that does not
exist. Issue confirmed; remediation needs further investigation."* Skipping `fix_rewritten` and
falling back to the finder's original nullifies Gate 4, which exists to stop proportionality
runaway in the report.

### Worked example

~~~
### [HIGH] `POST /api/ratings` writes the rating before checking the product exists

**File:** `src/api/ratings/route.ts:31-48`

**Issue:** The handler parses the body with `RatingBodySchema` and calls `Rating.create({ productId, userId, score })` before any lookup of `productId`. A client posting a well-formed body with a `productId` no product carries writes an orphan row, which `countVisibleReviews` (`src/lib/stats.ts:14`) then counts into the author's `reviewsCount` — the profile stat rises for a review attached to nothing. The schema declares `productId` as a plain string with no referential constraint, so nothing downstream rejects it.

**Fix:**
```ts
const product = await Product.findById(productId).select('_id').lean()
if (!product) return NextResponse.json({ error: 'not_found' }, { status: 404 })
await Rating.create({ productId, userId, score })
```

**Verdict:** CONFIRMED · **Confidence:** 90
~~~

The example is illustrative. What makes it a finding is the shape, not the stack: a quoted line, a
named consequence downstream of it, the reason nothing else catches it, and a fix no larger than the
change under review.

### Multiple-instance consolidation

The same rule broken in N places is one finding listing N locations.

~~~
### [MEDIUM] 4 route handlers read the request body without a schema parse

**File:** Multiple — see locations below.

**Issue:** Four handlers pass the parsed request body straight into a model write, so an unlisted field in the body reaches the document. `CONTRIBUTING.md` §6.1 requires a validated body before handler logic, and `src/lib/schemas.ts` already carries a schema for three of the four shapes.

- `src/api/me/route.ts:22` — `const body = await request.json()`
- `src/api/posts/route.ts:41` — same
- `src/admin/api/announcements/route.ts:18` — same
- `src/admin/api/moderation/route.ts:29` — same

**Fix:** Parse each body with the matching schema from `src/lib/schemas.ts` (`MeUpdateBody`, `CreatePostBody`, `AnnouncementBody`), and add a strict schema for the moderation shape, which has none. Strict rather than the default, so an unexpected key is rejected rather than silently dropped and re-added by a later refactor.

**Verdict:** CONFIRMED · **Confidence:** 95
~~~

## Report structure

In this order:

1. **PR header**, PR mode only:

   ```
   # Code Review — PR #<num>: <title>

   Base: <baseRef>  ·  Head: <headRef>  ·  Files changed: <count>  ·  CI: <PASS|FAIL|PENDING>
   ```

2. **The budget line** for the depth that ran. This is what actually executed, not what was
   requested — a degraded run says so here.

   ```
   standard → 8 angles × ≤6 candidates → 1-vote 3-state verify → ≤12 findings
   ```

3. **Run settings and verification stats**, always both lines:

   ```
   Mode: <review|prepush> · Depth: <quick|standard|deep> · Areas: <list|all> · Lenses: <list|defaults>
   Find: <total> candidates · Suppressed: <s> (prior runs) · Verify: <X> confirmed · <Y> plausible · <Z> refuted
   ```

   Omit the `Suppressed` segment when zero. Append `· <n> findings dropped by the cap` when the
   report cap cut findings. Emit both lines even for a small review where sharding was skipped and
   verification ran inline.

4. **The build line**, when Stage-2 ran (always at `deep`; at `standard` when `fileCount ≥ 30` or
   `locDelta ≥ 2000`; never at `quick` or prepush):

   ```
   Typecheck: <PASS|FAIL>  ·  Lint: <PASS|FAIL>  ·  Tests: <PASS|FAIL>
   ```

   Omit the line entirely when Stage-2 was skipped on purpose — do not emit `SKIPPED`. Breakage
   that pre-dates the diff gets a `(pre-existing CI red)` suffix rather than a finding.

5. **The findings**, ordered by severity then file path. CONFIRMED before PLAUSIBLE within a
   severity.

6. **The coverage ledger**, per `coverage.md` — every angle, checklist and gate that did not run,
   with its reason, and the count of those that did. Print the section even when nothing is
   outstanding, as `Not checked: nothing — every selected angle, checklist and gate ran.`

7. **Exactly one verdict line.** Nothing after it.

## Verdict line

Pick the first that matches:

| Verdict | When |
|---|---|
| `BLOCK` | At least one `CRITICAL` finding. |
| `WARNING` | Zero `CRITICAL`, at least one `HIGH`. |
| `APPROVE` | Zero `CRITICAL`, zero `HIGH`, at least one `MEDIUM` or `LOW`. |
| `LGTM — no high-severity issues identified.` | Zero findings of any severity. |

`LGTM` describes the findings, and the coverage ledger above it describes the search. Both are
needed for the reader to know what the absence of findings means.

Do not add a summary, closing thoughts, or recommended next steps after the verdict. The report
ends at the verdict line.

## Report file location

At `standard` and `deep`, write the report to disk as well as emitting it inline; a long report
scrolls off-screen and is hard to share. Exactly one file per run, at the first of:

1. A user-specified path. A directory-only path gets `code-review-<base>-vs-<head>.md` appended.
2. PR mode: `${CLAUDE_PROJECT_DIR}/code-review-PR-<number>.md`.
3. Local or branch-range: `${CLAUDE_PROJECT_DIR}/code-review-<base>-vs-<head>.md`.

Do not write a second copy under `.code-review/<run-id>/`; the JSONL artifacts there are the audit
trail, and the report belongs where the person will find it. Tell the user the absolute path in one
sentence and still emit the report inline in the same turn. If `Write` is denied, surface the
attempted path and ask rather than silently redirecting.

At `quick` and in prepush the report is inline only. End by offering to write a file; never write
one unasked.

## What the report does not contain

A summary or recap at the top. A "things I considered but did not flag" section. General advice
unattached to a line in the diff. A suggestion to adopt a library the repo's manifest does not
carry. A nice-to-have for a file outside the diff. Praise — "great error handling here" is noise,
and the coverage ledger is where the reader learns what was examined and came back clean. Markdown
tables of findings, because `### [SEVERITY]` headings are greppable and table rows are not.

## Why this is markdown rather than a `ReportFindings` call

Some harnesses expose a `ReportFindings` tool taking typed findings (`file`, `line`, `summary`,
`short_summary`, `failure_scenario`, `category`, `verdict`). This skill does not emit through it,
for three reasons. It is gated behind a harness flag and absent on the MCP-served path this skill
also runs on, so depending on it produces nothing on some install paths. Its entry shape carries one
line per finding with no severity, no consolidated multi-instance locations and no coverage ledger,
so the two things this review exists to deliver cannot be expressed in it. And its contract says not
to print the findings as text as well, which would delete the deliverable on any path where the tool
call is not rendered. A future schema carrying severity, multi-location findings and coverage would
be worth revisiting.
