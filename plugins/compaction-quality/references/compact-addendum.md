# The compaction addendum — v1

Everything between the fences is the literal. A harness sitting on the wire (Perch/Relay does this)
splices it into Claude Code's `/compact` summarisation instruction, immediately **before** the
user's own `Additional Instructions:` block if there is one, and otherwise before the
`REMINDER: Do NOT call any tools.` trailer. Auto-compaction and a typed `/compact` are byte-identical
on the wire, so one splice covers both.

It is an **addition, not a replacement**. Claude Code's nine-section prompt stays intact, including
its existing instruction to preserve security-relevant constraints verbatim. Replacing that prompt
means restating everything it relies on — see `SKILL.md` and the note in `references/evidence.md`
that the Messages API's `instructions` field replaces the default prompt rather than supplementing
it.

It is a **literal**. No interpolation, no clock, no session id, no counter.

## Provenance

The paragraph is the `pinning` arm of `scripts/benchmark_vs_compact.py`, verbatim — the arm
described there as "the minimum change that might capture the gain". In the head-to-head over six
transcripts it was the only arm to score 3/3 on user corrections (built-in and skill-pointer arms
both scored 2/3). That sample is small and carried no constraint or rejected-approach spans at all,
so treat it as the reason this text was chosen over the alternatives, **not** as evidence the
addendum works. The 121-event retention figures in `SKILL.md` are what motivate the change; nothing
here has yet measured the fix.

Deliberately **not** included, though `SKILL.md` argues for all of them: the two-tier framing, the
keep/drop rule, the anti-paraphrase examples, and extract-then-compress-then-verify. The measured
arm was one paragraph, and instruction-following degrades as instruction count rises. Adding them is
a change to test, not a free improvement.

## Editing this block

Changing the text means bumping the version in the fence **and** in the marker line, and updating
the pinned byte count in whatever test guards the consuming copy. Unlike a system-prefix block, this
one carries no prompt-cache cost: it lands in the final user turn of a one-shot request, past the
newest cache breakpoint, so it never rewrites a warm prefix and needs no per-conversation pinning.

```text
One addition: open with a PINNED block reproducing VERBATIM, word for word, every standing
constraint, every user correction, and every rejected approach with its reason. Quote them; do not
paraphrase them. Everything else may be summarised normally.

End the summary with this line exactly: _Compacted with Relay · compaction-quality addendum v1._
```
