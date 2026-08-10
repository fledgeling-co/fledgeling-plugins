/**
 * Illustrative examples.
 *
 * These are the one part of this site that is NOT extracted from the repository.
 * Each `prompt` is one of the skill's own quoted trigger phrases; each `output`
 * is a short, representative sketch written from that skill's README and
 * SKILL.md — grounded in what the skill documents itself as producing, but not
 * captured from a run.
 *
 * The detail page marks every one of them as illustrative. Do not remove that
 * marker, and do not add an entry whose claims are not traceable to the skill's
 * own documentation: a page that reads as authoritative makes an invented
 * example worse than no example.
 *
 * A skill with no entry here simply renders no example section, so a newly added
 * skill degrades quietly rather than showing something made up.
 */

export type Example = {
  prompt: string;
  output: string;
};

export const EXAMPLES: Record<string, Example> = {
  "ship-armada": {
    prompt: "what's happening across all my projects",
    output: `Read ARMADA.md · 34 projects · verified against git

  3 entries stale (fledgeling-app, margin, loupe)
  2 campaigns proposed, 0 running

CAMPAIGN  model-id-swap            status: proposed
  9 repos pin a superseded model id. Mechanical —
  worktree edit behind a code-review gate, no spec
  pipeline.

CAMPAIGN  skills-site              status: proposed
  1 repo, 1 feature → ship-feature.

Dispatch caps at 3 repos concurrently, 1 fleet per repo.
Nothing runs until you pick.`,
  },

  "armada-sync": {
    prompt: "update the armada manifest",
    output: `~/Dev/ARMADA.md — fledgeling-plugins

  status:   +  site/ added, deployed at skills.fledgeling.app
  features: +  searchable skill directory
  updated:  2026-08-04 → 2026-08-10
  changelog: + one line

Verified 6 paths, all resolve. Touched one entry.
Other 33 projects unchanged.`,
  },

  "create-swe-project": {
    prompt: "scaffold X",
    output: `scaffold.sh --plan   (writes nothing)

  codename   perch
  modules    web, tokens, data
  ports      web 3114, api 3115  (free on this machine)

  would write 122 files
    apps/web/            Next.js App Router, lib/ai.ts,
                         security headers, vercel.json
    packages/tokens/     drift gate
    docs/                CODING_PRACTICES, DEPLOYMENT,
                         NEW_PROJECT_BEST_PRACTICES
    .husky/pre-push      typecheck + build

Re-run without --plan to render it.`,
  },

  "design-review": {
    prompt: "looks AI-generated",
    output: `Coverage: 14 of 14 screens · 4 viewports · 3 tiers

HIGH   Pricing card contrast 2.9:1 on the muted label
       375 / 768 / 1280 / 1920
       fix: color: var(--color-muted) → var(--color-ink)

HIGH   Primary button has no :focus-visible ring
       fix: outline: 2px solid var(--accent);
            outline-offset: 2px

MED    17 distinct spacing values, 6 near-misses on the
       8px scale (14px, 18px, 22px…)

Not checked: real content at length, keyboard traps
inside the modal, anything behind auth.`,
  },

  "braindump": {
    prompt: "this summary is good",
    output: `score_retention.py  summary.md  transcript.jsonl

  user corrections      2 / 8    25.0%
  rejected approaches   0 / 6     0.0%
  standing constraints  3 / 7    42.9%
  file paths touched   11 / 12   91.7%

Exact string match. No model judgment anywhere in
this number.

Weakest: the four dead ends this session already ruled
out are absent, so the next one will try them again.`,
  },

  trawl: {
    prompt: "what are my options",
    output: `Trawl standard — 5 frames, 27 ideas → 19 after merge,
4 floored, 1 frame apoptosed. ★ BEATS baseline.

BASELINE (frozen)
  Add a Redis cache in front of the query.

★ Precompute on write            BEATS
  Removes the read path entirely rather than making it
  faster. First step: a materialised view + a trigger.

  Invert the ownership           TIES
  Read replica per tenant        TIES   ← non-obvious

TRAP  Cache with a short TTL — hides the slow query
      until traffic doubles, then fails at the worst time.`,
  },

  "create-mac-icon": {
    prompt: "make an icon for my app",
    output: `audit.html — 3 engines, 12-point rubric, losers included

  A  layered SVG (ships)     9.5 / 12
  B  Arrow vector            7.0 / 12
  C  raster, Apple-steered   8.5 / 12   ← fidelity target

Fidelity loop, A against C at 32 / 64 / 128 / 256 / 1024:

  r00  0.71   bevel too hard, ground reads flat
  r03  0.88   ground fixed, glyph still light at 32px
  r05  0.94   converged

Shipped: icon.svg + 1024 / 256 / 128 png, audit sheet
committed beside them.`,
  },

  "improve-skill": {
    prompt: "make a better version of",
    output: `Rebuild traced to evidence, then judged blind.

  Research     5 backends, reports committed
  Rules        14 changed, each mapped to a source
  Evals        v1 49.0%  →  v2 96.4%  (structural)
  Panel        4 families, anonymised, random order
               15-5 for the rebuild

  Claude liked it least (3-2), which is worth knowing
  given Claude wrote it.

Where it still loses is in EVALS.md, kept as a standing
counter-example rather than dropped.`,
  },

  "create-skill": {
    prompt: "create a skill for X",
    output: `Interview first — a vague answer is a defect to fix,
not a constraint to work around.

  ✓ trigger      what fires it, and what must not
  ✓ output       the artifact, named
  ✓ done         how you tell a run worked
  ✗ scope        "helps with releases" — too vague, asked again

Then: research → build → prove against the honest
baseline, which is the same prompts with NO skill at all.

  with skill    5 payloads, 5 pass
  no skill      6 payloads, 0 pass`,
  },

  "dossier-report": {
    prompt: "research X and make a page for it",
    output: `Panel: 5 backends. All 5 read end to end, not merged.

  Claims extracted        41
  Citations resolved      41 / 41
  Contradictions found     3  → own section on the page

  BUILD FAILED once: 2 citations returned 404.
  Re-run after replacing them.

Page designed from its own subject, so consecutive
dossiers do not converge on one look.`,
  },

  "mac-doctor": {
    prompt: "no space left on device",
    output: `Freed 73 GB · 93% → 89%

  52.2 GB  12 worktrees, four proofs each
  11.3 GB  CocoaPods cache
   4.2 GB  build output, 19 dirs with a live generator
   2.8 GB  pnpm + bun
   1.5 GB  Docker, brew

REFUSED (told you instead of guessing)
  ~/Dev/anvil        worktree has unpushed commits
  ~/Dev/loupe/dist   no generator found — cannot rebuild

The two short tiers are plain shell. 96 runs a day, zero
tokens.`,
  },

  discipline: {
    prompt: "why is this burning so many tokens",
    output: `A ~220-token block for the top of a session.

It targets three habits, not your prose:
  · re-printing plans and diffs already on your screen
  · opening a whole file to find one line
  · handing small jobs to sub-agents that each pay for
    a fresh context

Measured across 106 tasks on Claude Opus 5. The nearest
alternative compresses prose instead: a third off cost,
and 7.6 points off task score — because 78% of that
"saving" was the agent doing less work.

This one changes how much you write, never how much
you do.`,
  },

  "goal-harness": {
    prompt: "set a goal to ship the rest of the backlog",
    output: `arm.sh --dry-run   (writes nothing)

PREFLIGHT
  ✓ worklist grounded in the repo — 11 items with IDs
  ✓ brief 3,412 / 4,000 chars
  ✗ 2 items have no gate command — added
  ✓ 6 settings that end a run silently: 6 fixed

DIFF
  stopHookActive        -  false   +  true
  maxConsecutiveBlocks  -  8       +  unset

WRITES
  docs/goals/goal-backlog.md
  .claude/goal-guard.sh   decides by exit code, not by
                          reading the transcript

Ledger at docs/goals/ledger.md — answers "is it still
going" without interrupting the run.`,
  },

  "loop-harness": {
    prompt: "keep checking the deploy",
    output: `Mechanism picked BEFORE anything is written.

  event monitor   ← chosen: the deploy emits status
  polling         rejected: 30s of nothing, 120 times
  goal-harness    rejected: no finish line here

  ✓ .claude/loop.md  8,204 / 25,000 bytes
  ✗ /verify passed as plain text — a scheduled fire hands
    any skill you may not invoke to the run as prose,
    with no error. Rewritten as an explicit instruction.

ARMED
  wake signal   deploy webhook
  heartbeat     every 20 min, writes to the ledger
  renewal       reminder at day 6 of the 7-day expiry`,
  },

  report: {
    prompt: "write this up as a report",
    output: `Claim ledger built BEFORE the page is designed.

  MEASURED    the queue drops 12% of events
              — command output, in the transcript
  SINGLE      p99 latency 840ms
              — one sample, marked as one sample
  DERIVED     ~3.2 GB/day at current volume
              — computed from the two above

  UNSUPPORTED  "users found it faster"  → cut

Page is generated FROM the ledger, so a claim cannot be
cited afterwards. Reasoning renders visibly as reasoning.

Ships: one self-contained HTML file that paginates to a
real A4 PDF with the motion stripped out, plus a one-page
TLDR from the same ledger so the two cannot disagree.`,
  },

  clarify: {
    prompt: "ask me what you need",
    output: `Swept the conversation and the repo first. Two questions
died there — already answered. One survived the
divergence test.

  One migration file, or split into several?

  › One file (Recommended)
    Applies and rolls back as a single unit, so a failure
    halfway leaves nothing half-done.

  › Schema now, backfill after
    Structure ships quickly; the backfill runs separately
    without holding a lock on a large table.

  › One file per table
    Each re-runs on its own, at the cost of more files to
    order correctly.

Six words in the stem. The no-skill arm asked the same
thing in 57.`,
  },
};
