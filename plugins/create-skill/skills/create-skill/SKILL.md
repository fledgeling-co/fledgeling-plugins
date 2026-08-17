---
name: create-skill
description: >-
  End-to-end pipeline for building a brand-new skill from scratch, when there is no predecessor to improve. Starts with a broad clarifying interview so the desired outcome is actually pinned down (recommendations offered, notes allowed per answer, multi-choice where it fits, and nothing asked that is already answered elsewhere), runs paid+free deep research on the domain (Dossier panel, read in full, citations verified), builds the skill through skill-creator with every structural choice traced to evidence, proves it with structural evals against a no-skill baseline and a blind multi-family judge panel, iterates on the findings, then ships the full brand treatment — user-chosen name and icon concept, mac-design-studio icon with its audit sheet, composed banner, Luke-voice README and EVALS, a root-README entry — and commits and pushes. Use whenever the user wants a new skill built, says "create a skill for X", "turn this workflow into a skill", "I want a skill that does Y", or hands over a process they keep repeating by hand. Not for improving a skill that already exists (use improve-skill).
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

**When the user forbids questions.** "Build it, don't ask me anything" is a
real instruction and it arrives often enough to need an answer, because
until it had one the whole of Phase 0 and Phase 4 simply did not run and
nothing recorded that they had been skipped. The substitution:

- Take every decision you can from the material, which is where most of
  the interview's answers were going to come from anyway.
- Put each genuinely open fork to the referral lanes instead of to the
  user — the four CLI lanes in `clarify`, out-of-family where it matters,
  with the candidate options in swapped order to control for
  first-position bias. Give them the actual evidence, not the question
  alone.
- **Record the substitution in the skill's own `EVALS.md`**: which
  checkpoints were not asked, who answered instead, and what they said.
  A skipped hard gate that leaves no trace reads afterwards as a gate
  that passed.

The lanes replace the interview's *decisions*. They cannot replace taste,
cost, scope or risk tolerance, so if a fork turns on one of those, say
plainly in the final report that it was decided without the user and name
the assumption.

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

**Check for a corpus before buying one.** A sibling skill's
`docs/deep-research/` may already cover this domain, and a panel bought
twice on one field returns the same field. Where an existing corpus
covers it, read that in full instead, cite it from the new skill's
`evidence.md`, and say in the run report that the panel was reused rather
than run. Where it covers the domain only partly, run a narrower panel on
the gap rather than the whole subject.

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

**If the evals cannot be run, the skill ships saying so.** Some sessions
cannot spawn the runners: subagents are off, the budget is not there, or
the user has asked for the skill and not for a benchmark. That is a
legitimate outcome and inventing numbers is not, so `EVALS.md` opens with
the fact that no run happened, lists what *was* verified mechanically
(self-tests, golden cases, gates demonstrated failing on a deliberately
bad fixture), and names the two or three tasks that would settle the
open question. An unevaluated skill with that section is honest. An
unevaluated skill whose EVALS.md merely omits the subject is not, and it
reads to every later reader as though the pipeline ran.

## Phase 4 — Name and concepts (user checkpoint)

Present via AskUserQuestion, before any icon or banner generation:

1. **Name options** — 3-4 candidates with one-line rationales and a
   recommendation, mined from the marketplace's existing naming threads.
2. **Icon concept options** — 2-3 subject-mined directions described in
   words (register, device, signature move).

Do not proceed to Phase 5 until both are answered, or until the
no-questions substitution in Phase 0 has supplied them and recorded that
it did.

**When the skill joins an existing plugin.** This pipeline assumes one new
skill in one new plugin, and that assumption is wrong often enough to
name: a skill that must share scripts with a sibling belongs in the
sibling's plugin, because a plugin is a distribution unit and two
separately installed plugins cannot import each other's code or resolve
each other's paths. When that is the shape:

- There is no new icon and no new banner. The plugin owns both, and the
  skills inside it share them. Say so rather than leaving the brand phase
  looking half-run.
- The plugin's `plugin.json` description, its marketplace entry, its
  README and the root-README row all have to grow to cover both skills,
  and the version bumps on the plugin.
- **The site indexes one SKILL.md per plugin** (`skills/<plugin-name>/SKILL.md`),
  so a second skill is invisible to the catalogue except through the
  plugin description and README. Put what a reader needs there.
- Each skill still gets its own SKILL.md, description and EVALS section,
  because the epistemic split between them is the reason they are two
  skills at all.

## Phase 5 — Brand treatment

Full protocol: `references/brand-and-docs.md` — the marketplace
aesthetic, the hardened three-engine icon pipeline with `audit.html`, the
composed banner, the Luke-voice README and EVALS written for a
non-technical reader, and the root-README row.

**Route the icon to `create-mac-icon` when it is installed** — that skill owns
the corpus catalogue, the three engines, the fidelity loop and the audit sheet,
and it grew out of the pipeline `brand-and-docs.md` describes. Gate the result
with its `scripts/audit_sheet.py check <assets-dir>` (exit 0 required), which
resolves every image the sheet references and fails on unfilled placeholders —
"the skill says to create an audit.html" has twice not been enough on its own.

**Render the banner with `scripts/render_banner.py`**, which asserts the things
that fail silently: that the viewport override took effect rather than merely
being accepted, that the web font actually loaded (measured against a fallback
control, because `document.fonts.check()` under-reports), that every image
decoded, that nothing overflows the frame, and that the PNG is exactly
3200x1040. A banner whose icon failed to load renders as a correct layout with
a hole in it and reports no error at all.

**Then open what you made.** Serve `audit.html` and read it; `Read` the banner
PNG and the icon renders. Writing a file proves nothing about how it looks, and
a contact sheet whose images 404 renders as an empty page that no script and no
summary will ever mention. Ask each one *"what is wrong with this?"*

**Then run the marketplace's own gate**, which is the only check that sees the
registration as a whole:

```bash
node site/scripts/build-catalogue.mjs   # must exit 0
```

It fails on a missing SKILL.md, a missing icon, a version that disagrees
between `plugin.json` and the marketplace manifest, and a missing banner. Read
the exit code, not the output: piping it through `grep` reports grep's status
and has already turned a failure into a pass once.

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
