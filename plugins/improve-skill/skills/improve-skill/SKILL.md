---
name: improve-skill
description: End-to-end skill-improvement pipeline — take an existing skill (a repo, a SKILL.md, references) plus the user's feedback about it, run paid+free deep research on how to improve it (Dossier MCP panel), combine everything into a plan, build the improved skill as a new plugin in this marketplace, prove it with comparative evals and a blind multi-family AI judge panel (CLIs and APIs, keys via 1Password), iterate on the findings, then ship the full brand treatment — Luke-voice README and EVALS with a succinct-then-deep comparison to the original, a name the user chose from options, a mac-design-studio icon with its audit sheet, composed banners, a root-README entry — and commit and push. Use whenever the user wants to improve, upgrade, rebuild, modernise or "make a better version of" an existing skill, asks to research how a skill could be better, or hands over a skill plus complaints about it. Not for building a brand-new skill from scratch with no predecessor (use skill-creator directly).
---

# improve-skill

Take a skill that exists, learn everything about why it is the way it is,
research what the world has learned since it was written, rebuild it
better, and *prove* the rebuild — with evals the original is scored on
too, and blind judges who don't know which output came from which
version. Then ship it like a product: named by the user, iconed through
the full design pipeline, documented for a non-technical reader, pushed.

The pipeline is long. Its honesty rules are what make it worth running:
research is read in full and citation-verified, judges never see the
skill or know which take is which, losing takes stay on the audit sheet,
and a finding becomes a rule in the skill the same day it's confirmed.

## Phase 0 — Intake

Gather three things before anything runs:

1. **The source.** The skill's repo/directory, its SKILL.md, references,
   evals, benchmarks, README. Read all of it. If the source repo is
   third-party (origin not owned by the user), it is **read-only
   evidence** — the improved skill is born in this marketplace, and the
   original gets a genuine, named shoutout in the README, never silent
   appropriation.
2. **The feedback.** What the user has seen go wrong, plus whatever the
   source's own eval history records (a benchmark loss is the most
   valuable input you'll get — it names the exact failure to engineer
   away).
3. **A working name.** The final name comes later, from the user; use
   the source's name with a suffix until then.

## Phase 1 — Research (starts first, runs in background)

Kick off the Dossier deep-research panel immediately — it runs 5–60
minutes and everything else can proceed while it does. Protocol,
budget rules, and the read-in-full requirement: `references/research.md`.

While it runs: if the source skill's own methodology can be turned on
itself (an ideation skill can ideate about itself, a review skill can
review itself), run that meta-pass — it produces improvement candidates
research alone won't.

## Phase 2 — Plan and build

When the research lands (all reports read in full, citations verified),
merge three streams — research findings, the user's feedback, the
meta-pass — into a plan where **every structural change traces to a
measured result or a documented failure**. Then build the improved skill
as a new plugin here: SKILL.md under ~300 lines with depth pushed to
references, an `evidence.md` reference carrying the citations, legacy
trigger aliases if the name will change, and the research corpus
exported into `docs/deep-research/` so the claims stay auditable.

## Phase 3 — Prove it

Evals first, judges second, iteration third. Full protocol:
`references/evals-and-judging.md`. The shape:

- **Structural assertions**, not 1–10 scores — the judge-bias literature
  is clear that scores collapse; artifacts (did the run produce X) are
  checkable. Old skill and new skill run the same prompts; an
  independent grader marks every assertion with quoted evidence.
- **A blind panel** of heterogeneous judge families (CLIs you're signed
  into, APIs with keys from 1Password) scoring anonymised A/B pairs.
- **Iterate**: every confirmed finding becomes a rule in the skill, and
  the lost case is re-judged blind to verify the flip. A unanimous flip
  after a fix is the strongest evidence this pipeline produces.

## Phase 4 — Name and concepts (user checkpoint)

Present via AskUserQuestion, before any icon or banner generation:

1. **Name options** — 3–4 candidates with one-line rationales and a
   recommendation. Mine the marketplace's existing naming threads; a
   name that sits beside its siblings beats a clever orphan.
2. **Icon concept options** — 2–3 subject-mined directions described in
   words (register, device, signature move), so the user chooses the
   concept, not just the rendering.

Do not proceed to Phase 5 until both are answered.

## Phase 5 — Brand treatment

Full protocol: `references/brand-and-docs.md`. In brief:

- **Icon**: an Opus agent running mac-design-studio's hardened icon
  pipeline — three engines are a floor, `audit.html` from the template
  is a required deliverable, losing takes stay scored on the sheet — and
  briefed with the **marketplace aesthetic** in
  `references/brand-and-docs.md`: the set's exact superellipse outside
  shape, porcelain register (dark is trawl's alone), one vermilion/ember
  accent on the focal element, rich volumetric gel material over flat
  vector, a subject-mined glyph with a stated signature move.
- **Banner**: composed HTML (design-craft + ux-craft), the *real* icon
  beside a set wordmark, rendered at 2× retina. Never a generated image
  standing in for typography.
- **README + EVALS.md**: create-luke-content marketing persona, voice
  lint clean (the em-dash ban covers alt text and repo descriptions),
  written for a non-technical reader, with the comparison to the
  original stated succinctly up top and in depth in EVALS.md. Mermaid
  only where a diagram genuinely clarifies; media-gen-pro for imagery
  the design needs, never for diagrams.
- **Root README**: add the skill's row — icon, description, link.

## Phase 6 — Ship

Commit at sensible checkpoints throughout (skill built; evals graded;
panel judged; brand landed), push when the user has said pushing is in
scope, and update the portfolio manifest if this marketplace is tracked
in one. Report exact costs where APIs were metered — the panel's token
usage is part of the deliverable.

## Own evals

`evals/evals.json` carries foundational **process** evals: they assert the
pipeline's skills and tools are actually invoked (Dossier panel, full-read
+ citation verification, blind panel, create-luke-content + lint,
mac-design-studio + audit.html, root-README update, commit/push) and that
the two user checkpoints are asked before generation. Output quality is
proven by the evals this pipeline builds for each improved skill, not here.

## Prompting the agents this pipeline spawns

Every runner here is Opus, so each brief is an Opus prompt and its shape decides
what comes back. `references/opus-5-prompting.md` carries the patterns and the
three Anthropic documents to read in full first: XML-structured briefs with the
task last, no verification scaffolding (Opus 5 self-verifies, and instructing it
again causes over-verification), explicit delegation caps and scope statements,
vision work given crop-and-sample tools rather than told to double-check,
calibrated deliverable length, calm trigger language, and the environment traps
that make `claude -p` fail in ways no code review catches.

## Operating rules (learned the hard way)

- **Never report a panel member's findings before the panel settles** —
  an early single-sourced read becomes "corroborated" in the retelling.
- **Rate-limited judge CLIs are reported and substituted, not retried
  into the ground.** Same model via a different harness is an honest
  substitute; say which harness ran.
- **Max-effort API judges burn output budget on reasoning** — if a
  verdict comes back empty, re-run the truncated calls with 4× the
  output budget rather than shrinking the ask.
- **Subagents never run git operations**; the orchestrating session
  owns every commit. Parallel agents get non-overlapping directories
  and distinct localhost ports.
- **Vacuous assertions are findings about the evals.** A conditional
  assertion that can't fail on the current outputs gets an adversarial
  eval written to make it bite.
- **The comparison must be honest enough to lose.** If the original
  wins an eval, that goes in the table, and the fix-and-reflip is the
  story — a scorecard that only shows wins convinces nobody.
