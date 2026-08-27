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

  eli5: {
    prompt: "why quaternions beat Euler angles",
    output: `One self-contained page, gated before it ships.

  Form       Solid — the invariant is orientation, so the
             page is a 3D rig you orbit, not a diagram

  Predict    "At ninety degrees of pitch, how many
             independent axes are left?"  → commit → run

  Boundary   a brass gimbal jams and you feel it; Euler
             angles keep returning three clean numbers
             while one has stopped meaning anything

  Plain      "a gimbal is a set of nested rings, each free
             to spin on its own axis" — every topic word
             defined where it first appears, or the build fails

  Gate       31 checks · exit 0 required

The three explainers built before this version opened with
identical headings under identical tabs. The gate now fails
on that, at three copied phrases or more.`,
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

  "better-goal": {
    prompt: "set a goal to ship the rest of the backlog",
    output: `arm.sh --dry-run   (writes nothing)

PREFLIGHT
  ✓ worklist grounded in the repo — 11 items with IDs
  ✗ 2 items have no gate command — added
  ✗ stop-hook block cap unset → 8 blocks, then the turn
    is reported as "completed". Raised.

DIFF
  hooks.Stop            +  guard.sh (command hook)
  BLOCK_CAP             -  unset    +  500

WRITES
  docs/goals/goal-backlog.md
  .claude/goals/backlog.json   gates decided by exit
                               code, not by transcript

ARMED
  guard     runs the gates at the end of every turn
  watcher   Monitor, for the turns that never end

Turn 4: tests failed identically for the third time.
Disarmed as stuck rather than re-sending it.`,
  },

  "better-loop": {
    prompt: "keep checking the deploy",
    output: `Mechanism picked BEFORE anything is written.

  change-gated watcher  ← chosen
  5-minute cron         rejected: 120 wakes to find 2
                        changes, each re-billing the
                        whole session prefix
  better-goal           rejected: no finish line here

  probe   vercel ls --json | jq -r '.[0].state'
  ✓ deterministic — ran twice, identical

ARMED   Monitor, persistent. No cron, so no 7-day expiry.

  18:04  baseline   BUILDING
  18:06  (quiet)
  18:12  CHANGE     BUILDING → ERROR      ← woke the session
  18:31  repeat     ERROR seen ×3, suppressed until 19:01

polls 47 · wakes 2 · budget 12/h`,
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
died there — already answered. One went to a lane.

  Writing the migration as one file. Everything here so
  far is single-file, and a single unit applies and rolls
  back together. Fable agreed and had nothing to add.

One survived, because the fact that decides it is missing.

  Does this migration carry a data backfill?

  › Schema-only
    Runs in seconds; one file applies and rolls back as a
    unit.

  › It backfills a large table
    Ships the structure first and fills after, so nothing
    holds a lock during the backfill.

Two options, nothing marked. A mark would mean the fork was
mine to take. The no-skill arm asked this in 57 words.`,
  },
  positioning: {
    prompt: "position our B2B reconciliation tool and tell us what to lead with",
    output: `docs/positioning/work/
  Product truth ................ 4 shipped · 2 designed
  Research panels .............. 2 dispatched · 7 members · $20.00
  Claims ....................... 160 · 38 independent domains
  Candidate positions .......... 6 generated via trawl → 3 shortlisted

DECISION INSTRUMENT
  Veto ......................... ML matching engine excluded (unbuilt)
  Consequences ................. natural units (conversion %, CAC, sales cycle)
  Dominance .................... Territory A dominates status quo
  Rank stability ............... A leads in 44.7% of 231 weight vectors

Recommendation: "Territory A — Audit-ready reconciliation" (promising hypothesis)
→ docs/positioning/positioning-report.html  (design-review: clean)`,
  },

  "launch-craft": {
    prompt: "build a launch site for this repo and update the PRD",
    output: `launch-craft pipeline · 4 phases

Phase 1: Gemini Synthesis via agy
  docs/features-to-triage/ ..... 8 briefs scanned
  PRD.md & OVERVIEW.md ......... updated with 100% requirement traceability

Phase 2: Positioning & Copywriting
  docs/positioning/ ............ 00-decision.md verified
  Copy drafted ................. /create-luke-content (marketing persona)
  Pricing architecture ......... $9.99 BYOK perpetual vs $4.99/mo hosted

Phase 3: Interactive Marketing Site
  design/marketing/index.html .. GSAP scroll timeline, Three.js 3D hero,
                                 interactive UI slices, 5-platform badges

Phase 4: Validation Gate
  validate_site.py ............. WCAG AA pass (4.5:1), 0 em dashes, responsive clean`,
  },

  "create-luke-content": {
    prompt: "draft release notes for the overnight question digest feature",
    output: `Diolog Release Notes: 3 September 2026

Version: 2026.09.03
Date: 3 September 2026
Affected users: All plans

Breaking changes: None.

Added:
- We have launched the Overnight Question Digest, a morning email that rounds up retail investor questions asked on your feed since the previous send. It groups questions across our 14 standard feed topics and lands in your inbox at 07:00 in your listing timezone (Monday to Friday). In our 6-week beta across 11 companies, median response times dropped from 31 hours to 9 hours.
- The digest puts the top 3 topics by question volume right at the top, followed by the rest in a plain list.
- Questions flagged price-sensitive stay out of the email body into a separate "Needs a human read" list without an AI summary.
- Configurable under Settings > Notifications > Digest.

What it does not do:
It is an alerting tool, not an auto-responder; every reply is still written and published by your team.

Known rough edges:
- Topic grouping misfiles roughly 1 in 12 questions in our beta sample.
- One email address per company workspace for now.
- The price-sensitive classifier is tuned to over-flag.`,
  },
};
