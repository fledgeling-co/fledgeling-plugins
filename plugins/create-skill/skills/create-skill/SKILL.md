---
name: create-skill
description: End-to-end pipeline for building a brand-new skill from scratch, when there is no predecessor to improve. Starts with a broad clarifying interview so the desired outcome is actually pinned down (recommendations offered, notes allowed per answer, multi-choice where it fits, and nothing asked that is already answered elsewhere), runs paid+free deep research on the domain (Dossier panel, read in full, citations verified), builds the skill through skill-creator with every structural choice traced to evidence, proves it with structural evals against a no-skill baseline and a blind multi-family judge panel, iterates on the findings, then ships the full brand treatment — user-chosen name and icon concept, mac-design-studio icon with its audit sheet, composed banner, Luke-voice README and EVALS, a root-README entry — and commits and pushes. Use whenever the user wants a new skill built, says "create a skill for X", "turn this workflow into a skill", "I want a skill that does Y", or hands over a process they keep repeating by hand. Not for improving a skill that already exists (use improve-skill).
---

# create-skill

Build a skill that does not exist yet, properly: understand what the user
actually wants before writing anything, ground the design in evidence
rather than instinct, prove it works against the honest baseline of not
having it, and ship it like a product.

The sibling of `improve-skill`. That one starts from an artifact and its
failures; this one starts from an intention, which is harder, because an
unstated intention is the most common reason a new skill misses. So this
pipeline front-loads the interview and treats a vague answer as a defect
to fix rather than a constraint to work around.

## Phase 0 — Discovery (the phase that decides everything)

A new skill has no predecessor to argue with, so the brief is the only
specification. Get it right before anything else runs. Full protocol:
`references/discovery.md`.

The short version:

- **Answer what you can from what you already have.** The conversation,
  the repo, sibling skills, an earlier subagent's findings, a failed
  workflow's output. A question whose answer is already on disk wastes
  the user's attention and makes the rest look less considered.
- **Then ask, with recommendations.** Use AskUserQuestion, multi-choice
  where the options are genuinely discrete, each option carrying what it
  means and what it costs. Lead with the one you would pick and say why.
  Users answer a recommendation faster than an open question, and a
  recommendation they reject is itself information.
- **Cover the axes a skill actually turns on**: what triggers it, what it
  produces, who reads the output, what "done" looks like, what it must
  never do, whether outputs are objectively checkable, and what existing
  tools or skills it should route to rather than reimplement.
- **Leave room for notes.** Every question invites free text alongside
  the choice; the notes are where the real constraint usually appears.

Do not start the research panel until the interview has landed. Research
scoped by a guess buys a survey of the wrong field.

## Phase 1 — Research (starts as soon as the brief is fixed)

Kick off the Dossier panel on the skill's *domain* — the techniques,
failure modes and measured results in the field the skill operates in.
Protocol, budget rules and the read-in-full requirement:
`references/research.md`. It runs 5-60 minutes; the eval scaffold and the
prior-art survey proceed while it does.

While it runs, survey the prior art the skill will sit beside: existing
skills in this marketplace and the user's others, so the new one routes
to them rather than duplicating them, and so its name and shape fit the
family.

## Phase 2 — Build it through skill-creator

When the research lands (all reports read in full, citations verified),
invoke **skill-creator** and follow its process: capture intent, write
SKILL.md, keep it under ~300 lines with depth pushed to references,
bundle scripts for anything deterministic and repeated, and write test
cases before claiming it works.

What this pipeline adds on top of skill-creator's defaults:

- **Every structural choice traces to something** — a research finding, a
  measured failure mode, or an explicit answer from the interview. A rule
  nobody can source is a rule nobody should follow.
- An `evidence.md` reference carrying the citations, and the research
  corpus exported into `docs/deep-research/` so the claims stay auditable
  from inside the repo.
- Scripts for whatever the skill would otherwise re-derive per run.

## Phase 3 — Prove it

There is no predecessor, so the baseline is **the same prompts with no
skill at all**. That comparison is the honest one: it answers "does this
skill earn its place in the context window". Full protocol:
`references/evals-and-judging.md`.

- **Structural assertions**, not 1-10 scores — checkable properties of
  the output, graded by an independent subagent with quoted evidence.
- **A blind panel** of heterogeneous judge families on anonymised A/B
  pairs, where neither side is identified and judges never see the skill.
- **Iterate**: every confirmed defect becomes a rule the same day, and
  the lost case is re-judged blind to verify the flip.

If the skill does not beat the no-skill baseline, say so plainly and fix
it or drop it. A skill that changes nothing is worse than no skill: it
costs context and implies a guarantee it does not keep.

## Phase 4 — Name and concepts (user checkpoint)

Present via AskUserQuestion, before any icon or banner generation:

1. **Name options** — 3-4 candidates with one-line rationales and a
   recommendation, mined from the marketplace's existing naming threads.
2. **Icon concept options** — 2-3 subject-mined directions described in
   words (register, device, signature move).

Do not proceed to Phase 5 until both are answered.

## Phase 5 — Brand treatment

Full protocol: `references/brand-and-docs.md` — the marketplace
aesthetic, the hardened three-engine icon pipeline with `audit.html`, the
composed banner, the Luke-voice README and EVALS written for a
non-technical reader, and the root-README row.

## Phase 6 — Ship

Commit at checkpoints (brief agreed; skill built; evals graded; panel
judged; brand landed), push when pushing is in scope, update the
portfolio manifest, and report exact costs where APIs were metered.

## Own evals

`evals/evals.json` carries foundational **process** evals: that the
discovery interview happens before research, that skill-creator is
actually invoked, that the no-skill baseline is run rather than assumed,
that the blind panel and voice lint run, and that both user checkpoints
are asked before generation.

## Prompting the agents this pipeline spawns

Every runner here is Opus, so each brief is an Opus prompt.
`references/opus-5-prompting.md` carries the patterns and the three Anthropic
documents to read in full first: XML-structured briefs with the task last, no
verification scaffolding (Opus 5 self-verifies, and instructing it again causes
over-verification), explicit delegation caps and scope statements, vision work
given crop-and-sample tools, calibrated deliverable length, calm trigger
language, and the environment traps that make `claude -p` fail in ways no code
review catches.

## Operating rules

- **A vague brief is a defect, not a constraint.** If an answer leaves
  the skill's trigger, output or success condition undetermined, ask
  again rather than guessing and building the wrong thing well.
- **Never report a panel member before the panel settles.**
- **Subagents never run git operations**; the orchestrating session owns
  every commit. Parallel agents get non-overlapping directories and
  distinct localhost ports.
- **Route, don't reimplement.** If an existing skill already does part of
  the job, the new skill calls it and says so.
- **The comparison must be honest enough to lose.** If the no-skill
  baseline matches the skill on an eval, that goes in the table, and
  either the skill earns that case or the eval was measuring nothing.
