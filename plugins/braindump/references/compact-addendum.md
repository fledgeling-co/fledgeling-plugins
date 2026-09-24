# The compaction addendum — v4

Everything between the live fence is the literal. A harness sitting on the wire (Perch/Relay does
this) splices it into Claude Code's `/compact` summarisation instruction, immediately **before** the
user's own `Additional Instructions:` block if there is one, and otherwise before the
`REMINDER: Do NOT call any tools.` trailer. Auto-compaction and a typed `/compact` are byte-identical
on the wire, so one splice covers both.

It is an **addition, not a replacement**. Claude Code's nine-section prompt stays intact, including
its existing instruction to preserve security-relevant constraints verbatim. Replacing that prompt
means restating everything it relies on — see `SKILL.md` and the note in `references/evidence.md`
that the Messages API's `instructions` field replaces the default prompt rather than supplementing
it.

It is a **literal**. No interpolation, no clock, no session id, no counter.

## The live literal — v4

Exactly one fence in this file may be tagged `text`, and it is the one below. Perch's drift test
finds the consuming copy by splitting on that fence opener and fails the build if it finds two, so
superseded versions live under a different tag. That is also why the tag name is kept out of the
prose here.

```text
One addition: open with a short PINNED block noting the task state a fresh session
needs to continue. Keep it small: at most 12 items, about 3 KB in total, one or two
lines each.

Include only items that still matter. Standing constraints and corrections the user
stated may use the user's own words, each under 300 characters. Rejected approaches
become one-line outcomes: what was tried, and the short reason it was ruled out. Never
quote assistant-written text; restate outcomes in fresh words. Use exact spelling only
for identifiers: file paths, commands, flags, ids, error codes. Keep an item only if
its absence would cause wrong work; leave out file contents, code blocks, text that
hooks or instruction files injected (list those files under REREAD instead), this
instruction itself, regenerable output, and exploration that found nothing. Leave out reasoning and thinking, transcript passages,
and any credentials or secret values. If an earlier pinned block is present, carry
forward only the items that still apply, restated under these same rules.

Close the pinned block with a REREAD list: the path of every CLAUDE.md, SKILL.md, plan,
spec or rules file whose instructions were steering this session, one per line. The next
session re-reads those files before continuing.

End the summary with this line exactly: _Compacted with Relay · compaction-quality addendum v4._
```

1,385 UTF-8 bytes. Unlike a system-prefix block, this one carries no prompt-cache cost: it lands in
the final user turn of a one-shot request, past the newest cache breakpoint, so it never rewrites a
warm prefix and needs no per-conversation pinning. A change therefore applies to the very next
compaction and costs nothing on any conversation.

## Why v4 exists

v4 keeps the same mechanism — a short pinned block up front, a path-only reread list —
but states it as ordinary task-state summarisation. The block is capped (at most 12
items and about 3 KB, one or two lines each), keeps user-stated constraints and
corrections in the user's own words within that budget, and reduces rejected approaches
to one-line outcomes. Exact spelling applies only to identifiers; assistant-written text
is never quoted; reasoning, transcript passages, and credentials stay out. Earlier
pinned items carry forward only while they still apply. The keep/drop rule joins the
literal, leaving the two-tier framing and extract-then-compress-then-verify still
deliberately out.

## Why v3 exists

v2 pinned what was *said* — constraints, corrections, dead ends — and said nothing about what was
*loaded*: the CLAUDE.md chain, a SKILL.md mid-procedure, the plan being implemented. Those leave the
context with the compaction like everything else, and a successor that resumes without them follows
the summary's paraphrase of the rules instead of the rules. The REREAD paragraph routes whole
instruction files around the lossy channel the same way the pinned block routes constraints: by
reference instead of restatement. Anthropic's prompting guidance names compaction as a hydration
point ("inject … during context compaction"), so the mechanism is the documented one.

The IFScale caveat from v2 still compounds: v3 adds a fourth paragraph to an instruction whose one
measured virtue at v1 was being short. The specific thing to watch for is unchanged — the new
paragraph degrading the classes the earlier ones handled — and the `pinning2`/`pinning3` arms of
`scripts/benchmark_vs_compact.py` exist to catch it.

## Why v2 existed — what v1 did in the field

`references/case-study-paired.md` is the first observation of this mechanism against a real
compaction rather than a benchmark harness. One session, so it is an existence proof, not a rate.

**v1 worked, and by the intended mechanism.** The spliced compaction opened with a pinned block
carrying seven rejected approaches with reasons, several standing constraints quoted, and a
peer-agent correction — against an untouched `/compact` earlier in the same session that carried
one buried fragment out of fifteen traceable dead ends. On the class this skill exists to rescue,
the gap between the two is not marginal.

**And it had one specific, reproducible failure: the sweep stopped at recency.** Every dead end it
pinned came from the last two hours of a fourteen-hour session. Eight older ones — all
product-and-architecture decisions rather than method lessons — were dropped, with a fully-formed
pinned block containing every one of them sitting in the same context window, written eleven
minutes earlier by this skill run in-session. The items were not unreachable. The sweep simply
terminated where the material was densest.

Two things v1 did not say, and the omissions map exactly onto what was lost:

- **Where to look.** "Every rejected approach" does not say *over what span*, and an unguided sweep
  of a long window returns the recent end of it.
- **That there are two kinds.** Method dead ends (how to work) and product dead ends (what to
  build) sit in different regions of a transcript. Asked for one undifferentiated class, the model
  returned whichever pile was nearer.

v2 added one paragraph addressing both, plus the instruction to carry an earlier pinned block
forward rather than rebuild from scratch — which is what would have saved all eight.

## What v3 is, and is not, evidence for

**It is not measured.** v1's text was the `pinning` arm of `scripts/benchmark_vs_compact.py`,
chosen because in a six-transcript head-to-head it was the only arm to score 3/3 on user
corrections. v2 and v3 have no equivalent behind them: each is a targeted fix for an observed
failure, shipped on the operator's decision rather than on a benchmark. The `pinning2` arm exists
so that gap can be closed after the fact — `--arms cli,pinning,pinning2` runs the comparison.

Still deliberately **not** included: the two-tier framing and extract-then-compress-then-verify,
though `SKILL.md` argues for both. Same reason, now with less headroom than v1 had. The keep/drop
rule joined the literal in v4; the anti-paraphrase examples left with the phrasing they
illustrated.

## Editing this block

Changing the text means bumping the version in the marker line **and** in `version`, updating
`pinnedUTF8Count`, and retagging the fences here so exactly one stays live. Keep the superseded
literal below, under a non-live tag, so a summary found months later can be matched to the text
that produced it.

## Superseded — v3

Shipped as `version = 3`, 1,099 UTF-8 bytes. A summary ending
`_Compacted with Relay · compaction-quality addendum v3._` was produced by this text.

```superseded
One addition: open with a PINNED block reproducing VERBATIM, word for word, every standing
constraint, every user correction, and every rejected approach with its reason. Quote them; do not
paraphrase them. Everything else may be summarised normally.

Sweep the whole conversation for that block, starting from its oldest turn. Rejected approaches
come in two kinds and sit in different places: how to work (a check that lies, a command that
silently fails) and what to build (an architecture, library or approach ruled out, and why). A
correction from a subagent or peer agent counts as a correction. If an earlier pinned block is
already in the conversation, carry every item it holds.

Close the pinned block with a REREAD list: the path of every CLAUDE.md, SKILL.md, plan, spec or
rules file whose instructions were steering this session, one per line. These files leave the
context with the compaction, so the next session re-reads them before continuing; a path cannot
mutate, a paraphrase can.

End the summary with this line exactly: _Compacted with Relay · compaction-quality addendum v3._
```

## Superseded — v2

Shipped as `version = 2`, 786 UTF-8 bytes. A summary ending
`_Compacted with Relay · compaction-quality addendum v2._` was produced by this text.

```superseded
One addition: open with a PINNED block reproducing VERBATIM, word for word, every standing
constraint, every user correction, and every rejected approach with its reason. Quote them; do not
paraphrase them. Everything else may be summarised normally.

Sweep the whole conversation for that block, starting from its oldest turn. Rejected approaches
come in two kinds and sit in different places: how to work (a check that lies, a command that
silently fails) and what to build (an architecture, library or approach ruled out, and why). A
correction from a subagent or peer agent counts as a correction. If an earlier pinned block is
already in the conversation, carry every item it holds.

End the summary with this line exactly: _Compacted with Relay · compaction-quality addendum v2._
```

## Superseded — v1

Shipped as `version = 1`, 349 UTF-8 bytes. A summary ending
`_Compacted with Relay · compaction-quality addendum v1._` was produced by this text.

```superseded
One addition: open with a PINNED block reproducing VERBATIM, word for word, every standing
constraint, every user correction, and every rejected approach with its reason. Quote them; do not
paraphrase them. Everything else may be summarised normally.

End the summary with this line exactly: _Compacted with Relay · compaction-quality addendum v1._
```
