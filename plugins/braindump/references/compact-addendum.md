# The compaction addendum — v2

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

## The live literal — v2

Exactly one fence in this file may be tagged `text`, and it is the one below. Perch's drift test
finds the consuming copy by splitting on that fence opener and fails the build if it finds two, so
superseded versions live under a different tag. That is also why the tag name is kept out of the
prose here.

```text
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

786 UTF-8 bytes. Unlike a system-prefix block, this one carries no prompt-cache cost: it lands in
the final user turn of a one-shot request, past the newest cache breakpoint, so it never rewrites a
warm prefix and needs no per-conversation pinning. A change therefore applies to the very next
compaction and costs nothing on any conversation.

## Why v2 exists — what v1 did in the field

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

v2 adds one paragraph addressing both, plus the instruction to carry an earlier pinned block
forward rather than rebuild from scratch — which is what would have saved all eight.

## What v2 is, and is not, evidence for

**It is not measured.** v1's text was the `pinning` arm of `scripts/benchmark_vs_compact.py`,
chosen because in a six-transcript head-to-head it was the only arm to score 3/3 on user
corrections. v2 has no equivalent behind it: it is a targeted fix for a failure observed once,
shipped on the operator's decision rather than on a benchmark. The `pinning2` arm exists so that
gap can be closed after the fact — `--arms cli,pinning,pinning2` runs the comparison.

**The risk it carries is named in `evidence.md`:** instruction-following degrades as instruction
count rises (IFScale), and v2 roughly triples the sentence count of a paragraph whose one measured
virtue was being short. The specific thing to watch for is v2 doing *worse* than v1 on the classes
v1 already handled — constraints and corrections — while improving the rejected-approach sweep.
If that shows up, the fix belongs in the skill rather than on the wire.

Still deliberately **not** included, though `SKILL.md` argues for all of them: the two-tier framing,
the keep/drop rule, the anti-paraphrase examples, and extract-then-compress-then-verify. Same
reason, now with less headroom than v1 had.

## Editing this block

Changing the text means bumping the version in the marker line **and** in `version`, updating
`pinnedUTF8Count`, and retagging the fences here so exactly one stays live. Keep the superseded
literal below, under a non-live tag, so a summary found months later can be matched to the text
that produced it.

## Superseded — v1

Shipped as `version = 1`, 349 UTF-8 bytes. A summary ending
`_Compacted with Relay · compaction-quality addendum v1._` was produced by this text.

```superseded
One addition: open with a PINNED block reproducing VERBATIM, word for word, every standing
constraint, every user correction, and every rejected approach with its reason. Quote them; do not
paraphrase them. Everything else may be summarised normally.

End the summary with this line exactly: _Compacted with Relay · compaction-quality addendum v1._
```
