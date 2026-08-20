# Prepush — the gate on the outgoing diff

The token-light variant. One question, answered fast: **is it safe to push the commits about to
leave this machine?** Not a review — a blocker scan. Target a few minutes of wall clock, zero
subagents, zero artifacts.

Triggered by "pre-push check", "can I push this?", "check the diff before I push", "is this safe to
push", a `prepush` keyword, or invocation from a pre-push hook.

## What makes this mode cheap

- **No `Agent` calls.** No sharding, no verifier fan-out. You find and self-verify inline.
- **No JSONL artifacts and no report file.** Verdict and blockers are inline only. Write a file if
  the user asks; never by default.
- **No full checklist loads.** The blocker list below is the whole rulebook, plus
  `security-checklist.md` only when the diff touches auth, session or payment code.
- **The mechanical half is a script.** `scripts/prepush-scan.sh` resolves the outgoing range and
  greps categories 1, 2, 3 and 8 in one pass, emitting `RULE<TAB>file:line<TAB>note` rows and never
  a matched value. Run it first, then read the rows and spend your own reading on categories 4 to
  7, which need judgement. Where the script is unavailable, do all nine by hand from the diff.
- **Read budget.** Read in full only the files carrying blocker-suspicious hunks; review the rest
  from the diff text.
- **Depth keywords are ignored.** `prepush deep` is a contradiction — run a standard review instead
  and say so.

## The outgoing diff

The unit under review is **unpushed commits**, not the working tree.

```bash
scripts/diff-range.sh --outgoing        # resolves @{push} → @{upstream} → default branch
scripts/prepush-scan.sh                 # the mechanical categories, values never printed
```

By hand, when the scripts are unavailable:

```bash
git diff @{push}..HEAD 2>/dev/null \
  || git diff @{upstream}..HEAD 2>/dev/null \
  || git diff origin/$(git symbolic-ref --short refs/remotes/origin/HEAD | sed 's|origin/||')...HEAD
git log @{push}..HEAD --oneline 2>/dev/null || git log @{upstream}..HEAD --oneline
```

No upstream at all: diff against the default branch's merge base and note that the whole branch is
being gated. **Zero outgoing commits:** say so and stop — there is nothing to gate. **A dirty
working tree:** note in one line that uncommitted changes are not covered, and do not review them.

## Blocker checklist

Scan the outgoing diff in order. Categories 1 to 7 produce blockers; 8 and 9 produce notes.

1. **Secrets** — added lines carrying API keys, tokens, private keys, connection strings or
   passwords; `.env` or `.env.*` or credential files newly tracked (`git diff --stat` plus
   `git status` over the range). Never quote the value: cite `file:line` and type, and say the
   pushed secret must be rotated, not just removed.
2. **Debug leftovers** — `debugger` statements; `console.log` dumping payloads in server code; test
   focus or skip markers added (`.only`, `.skip`, `it.todo`); a verbose or debug flag flipped on in
   config.
3. **Accidental payload** — large binaries or generated directories newly tracked; lockfile churn
   with no manifest change; editor or OS junk; another branch's files swept in, which the commit
   list usually reveals.
4. **Broken contracts** — an exported symbol's signature or behaviour changed in the range: grep its
   callers across the whole workspace, not the package, and treat any call site not updated in the
   same range as a blocker. Where the repo has a contract document, a schema both sides consume, or
   a hand-mirrored type, check that the twin side and its guard test moved in the same range.
5. **A guard test weakened beside the code it guards** — an exact match that became `toContain`, a
   `rejects.toThrow` that became a resolved value, a `.strict()` that became `.passthrough()`, a
   key-set list that lost an entry. The source hardening while its assertion loosened in the same
   commit is the shape (`logic-bugs-checklist.md` §4.1).
6. **Auth or validation regressions** — an endpoint, Server Action or mutation touched in the range
   that lost, or never gained, its auth guard or its Zod parse; a user or visibility scope dropped
   from a query.
7. **Destructive data changes** — a migration or backfill script in the range that drops or renames
   a field, or a `deleteMany` with no guard, with no backfill note.
8. *(note)* **Markers** — TODO, FIXME, HACK, XXX added in the range, consolidated into one line.
9. *(note)* **Type safety** — when the touched package typechecks in under about 30 seconds, run
   the repo's own typecheck script scoped to it and report diff-introduced errors as a blocker.
   Otherwise skip and record it as `not-checked` in the notes rather than passing it silently.

Gate 3 still applies before you report a blocker: read enough of the file to confirm the guard is not
30 lines above the hunk, or provided by a shared wrapper. A false `DO NOT PUSH` erodes trust in the
gate faster than a missed LOW.

Gate 6 applies too. A blocker claiming runtime behaviour names the command you ran; without one, say
so in the finding rather than asserting.

## Output

No report file, no stats line. Emit exactly:

```
Prepush gate — <n> commit(s), <fileCount> file(s), +<ins>/−<del> vs <base-ref>

<### [SEVERITY] findings for blockers only, standard finding format, fix optional>

Notes (non-blocking): <one line per category-8/9 note, or omit the section>
Not checked: <one line, or "nothing">

<verdict>
```

The `Not checked` line is the same discipline as a full review's coverage ledger, at prepush scale:
the typecheck you skipped, the file you did not read, the callers you could not grep. A gate that
reports clean without saying what it looked at is indistinguishable from a gate that did not run.

Verdict, exactly one of:

- `DO NOT PUSH — <n> blocker(s).` — any CRITICAL or HIGH finding above.
- `PUSH WITH CARE — no blockers; <n> note(s) above.` — only non-blocking notes.
- `PUSH — outgoing diff is clean.` — nothing found.

MEDIUM and LOW observations that would appear in a normal review are out of scope: cap yourself at
the two most useful as notes and drop the rest. If the outgoing diff genuinely warrants a full
review — 3,000 lines of new auth code, a contract boundary rewritten — say so in one sentence after
the verdict and offer `standard` or `deep`. Do not escalate on your own.
