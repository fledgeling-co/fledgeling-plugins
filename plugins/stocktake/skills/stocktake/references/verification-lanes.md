# Verification lanes

> **Lane assignments are `defer`'s now.** Run
> `python3 <defer>/skills/defer/scripts/lane_pick.py --task <class>` for the model,
> the effort and the exact argv, or `lane_run.sh <class> "<prompt>"` to run and
> wire-verify it in one step. The classes are `implementation`, `completeness`,
> `general`, `referral`, `verification` and `design-review`. Three rules bind
> everywhere: `gpt-5.6-sol` never runs at `max` (it is the referral lane at
> `medium`, and other work goes to `gpt-5.6-terra` at `high`), Fable judges but
> never grades code or a ticket, and design review stays on Opus and Fable. What
> follows is this pipeline's reading of that policy, not a second copy of it.

## One judge, not a panel

The instinct is to ask several models and take the majority. **Do not.**

Measured across nine frontier judges from seven families (Kohli, arXiv 2605.29800):
they supply roughly **two effective independent votes**; panel accuracy falls **8–22
percentage points** short of what genuinely independent voting would give; the **best
single judge matches or outperforms the full panel across every condition tested**;
and established aggregation methods close **at most 11% of the gap even when given the
correct answers**. Robust across prompts, temperatures, chain-of-thought and
RewardBench.

So a panel costs N times as much, takes N times as long, and buys correlation. Use one
lane, the strongest available out of family, and spend the saved budget on giving it
better evidence.

**A panel is still right for one thing**: a genuinely open design fork where the split
itself is the answer. That is `clarify`'s job and it is a different question from
grading a verdict.

## Out of family, and why it is not optional

The judge must not come from the family that wrote the majority of the code. A
same-family judge shares the blind spot that produced the defect — that is the whole
mechanism, and it is why the ordering below starts elsewhere.

Suggested order, adjusted to what is installed and signed in:

1. A Google-family lane
2. An OpenAI-family lane
3. An xAI-family lane
4. Same-family, **recorded as `in-family (degraded)`** and given one extra adversarial
   round. A card does not reach a terminal column on a degraded verdict alone.

Probe each lane before the first use of a session and report which answered. A lane
that is rate-limited, signed out, or returns an empty output file with a clean exit is
a **lane failure**, not a quiet pass — substitute the next family and say so.

## The verdict shape

Ask for exactly this and nothing else, so the result is parseable and the judge cannot
drift into being agreeable:

```
VERDICT: CONFIRMED | PARTIAL | REJECTED
DEFECT <file:line> — a real bug the change introduces or leaves
RISK <file:line> — a hazard short of a bug
CLAIM-FALSE "<quoted claim>" — a statement the code contradicts
```

Two instructions that materially change what comes back: tell it to check load-bearing
claims **against the code rather than the diff narrative**, and tell it to **say what
it could not check** rather than assuming it holds. The second turns a confident wrong
answer into a scoped right one.

## Three operational facts that cost a run each

**Some lanes refuse concurrent instances.** Launching three at once has been observed
to leave one alive and kill the others silently, with empty logs and no error. Treat
the lane as serial: `scripts/verify_queue.sh` waits for any in-flight run before
starting the next, and reports a verdict or a no-verdict per card.

**Packets stop working somewhere around 50KB.** An 86KB whole-diff packet ran thirty
minutes without reaching a verdict; the same card re-sent as its four changed files
(~29KB) returned in minutes. Send the requirement list plus the changed files, not the
whole diff.

**A headless lane may need a permission it cannot prompt for.** One returns an empty
output file with exit code 0 when a tool it wants is auto-denied. Check the output is
non-empty before treating a lane as having answered, and never work around it by
granting blanket auto-approval in a repository holding production credentials.

## Reading the verdict honestly

A `CONFIRMED` with three `CLAIM-FALSE` blocks is not a pass. The verdict word grades
the change; the findings grade the *record*, and a record that misdescribes the change
is its own defect — the next reader acts on the description.

Findings about the author's own tests are the highest-value output of this whole step.
A verifier that reports "the assertion compares a value with itself" has found
something no green run ever will.
