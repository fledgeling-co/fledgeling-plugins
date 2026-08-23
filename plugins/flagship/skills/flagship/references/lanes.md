# Lanes — probe, then route

`defer` is the routing policy and you should call it. Its report is **plan utilisation, not
reachability**, and those are indistinguishable when a lane is absent: "nobody has used it" and
"it is not installed" produce the same number, so **the tool is most confident exactly where it
is least grounded.**

Measured 2026-08-22: `lane_pick.py --report` advertised a lane at 16.6% used — the highest
headroom of any non-Claude family — while no binary for it existed on `PATH` and no reference
existed in the Claude config. Three sessions probed independently and got the same answer. The
operator's own decision panel had also attempted that lane twice.

## Probe first

```bash
for b in codex agy grok cursor-agent glm claude; do
  command -v "$b" >/dev/null && echo "$b present" || echo "$b ABSENT"
done
```

Then hold four facts, each measured rather than assumed:

- **A meter can be optimistic.** A lane reported at 84% used returned `402 Payment Required —
  usage balance exhausted` on both its CLI and its documented fallback harness.
- **An empty output file is the failure, not the exit code.** A CLI has printed a correct model
  header and produced nothing; another refused with "Not inside a trusted directory" while
  exiting cleanly.
- **A lane can answer the wrong question and look right.** Called from a repo cwd without
  `--new-project` while another instance was live on the same machine, one lane returned a
  fully-formed acceptance verdict for a **different project's item** — foreign id, foreign
  platform captures, a confident verdict, nothing flagging it. Six sessions re-audited their
  existing verdicts on this; one re-ran a grade outright. Mandate `--new-project` from a
  neutral cwd, and **read every reply for your own subject before believing it** — an answer
  naming an id, platform or file that is not yours is a lane failure, not a verdict.
- **A one-shot cannot execute.** When the surviving out-of-family lane is a single call from a
  neutral cwd, it cannot run a suite, walk a diff or reproduce a defect. So split the verify
  stage: mechanical verification on a fresh-context agent that did not build the work,
  out-of-family judgement over the artifacts, and the single lane **logged as a downgrade per
  item**. An agent briefed to do both does the half it can and reports the whole.

## Never pattern-kill a lane

A runner hunting its own reviewer ran `pgrep -f "<model flag>"` and killed the first match —
another session's live review, on the only out-of-family lane on the machine. The victim sees an
empty output file and no reason. A conductor hit a sharper version: two processes both matched
the brief filename it had itself written into two worktrees an hour apart, and only cwd
separated them.

**A pid obtained from a pattern is not yours.** You must be able to name the process from its
full command line first; `pgrep -x` plus `lsof` on cwd is an identification, a pattern is a
candidate. On a machine running sixteen sessions against one shared lane, a pattern match is a
cross-session weapon.

## Report the substitution

When a lane is down, say which family answered instead, and log a single-lane verdict as a
downgrade in the artifact rather than passing it silently. `claude-fable-*` does not satisfy
out-of-family when the writer was Opus — different model, same family. One verifier had
presented it as its deciding second opinion and corrected the report before committing.

## Hand a one-shot reviewer whole regions, not tight excerpts

Once the split stage makes the out-of-family lane a judge over *artifacts* rather than over a
tree, the packet's boundaries become part of the verdict — and they are **invisible in the
reply.** Measured: a reviewer marked one of three code sites `UNPROVEN` while accepting the
other two, and the cause was that the excerpt handed to it **began one line below the
`do`/`catch` that made the site total.** The lane was healthy and on-subject — it cited the
right tests and the right file range, and returned `OVERALL: ACCEPT`. The finding still arrived
looking like a code finding rather than a packet finding.

So: hand whole regions. A reviewer reading an excerpt is only as right as its boundaries, and
nothing in its answer will tell you the boundary was wrong.

---

## A split verdict can mean the fork is real, or that both lanes lack what the repo holds

*Errand, on a two-lane referral that split and was then beaten by a grep.*

A technical fork went out of family. **The lanes split cleanly**, which is normally the signal that the
fork is genuine:

- One chose **B** — put the daemon's state-directory root in the greeting — with an argument that
  correctly killed option A: *a plist tells you about a job, not about the process that answered the
  door*, so a daemon run with no LaunchAgent yields `None` and is waved through, leaving the defect
  intact for exactly the case a test harness creates.
- The other chose **neither**, proposing a per-incarnation id required to match across both carriages —
  the invariant itself rather than the state-directory proxy.

**Then the repo answered both.** The per-incarnation id the second lane wanted to *add* **already
existed**: a per-boot audience tag, minted once at `bind()`, random, and `| 1` so it can **never be
zero — because zero is the value a forgotten field would have.** Already on both carriages, already
carrying its own cannot-say sentinel.

**So the fork was between two changes, and the answer was a field already in the wire.** The defect
turned out to be one line and an *overwrite* rather than a missing mechanism: the upgrade **adopts** the
door's value instead of comparing it.

**The rule: inlining the evidence is what makes an out-of-family lane usable, and it is also what caps
what the lane can find.** A lane reasoning from a packet cannot know what the tree already contains, so
a split verdict has two readings — the fork is real, or **both lanes are missing something the
repository would have told them in one grep.** Check the second before accepting the first. The lanes
narrowed it to *what property do we need*; only the repo could say *you already have it*.

**And one design detail worth stealing**: a sentinel chosen so that an **uninitialised** field is
distinguishable from a real one. `| 1` costs nothing and makes "nobody set this" a different value from
every legitimate answer — the constructive form of *absence must not read as a value*.

**A hazard found by the same measurement, recorded rather than rewritten at 04:00**: that codebase does
**no canonicalization** — `grep -c canonicalize` returns 0 — so a plist string and a client's resolved
directory are two renderings of one directory. A client resolving through a symlink (`/var` →
`/private/var`, the standard macOS case) compares **unequal while being the same directory**, and is
falsely refused on a healthy machine. Fail-safe, and it silently disables the feature it guards.

