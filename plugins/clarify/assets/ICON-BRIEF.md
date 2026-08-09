# Icon commission — clarify

<context>
You are producing the app icon for `clarify`, a new plugin in the
`fledgeling-plugins` marketplace. Everything you need is on disk; this brief
tells you where to look and what the house style is, because the house style
lives in the repo rather than in the icon skill.

## The skill this icon is for

`clarify` decides whether an AI coding agent should interrupt its user with a
question, and then composes that question so it takes one click to answer. Its
measured value is not that it makes the agent ask more or ask more safely — the
model already handles both. Its value is that the question costs less to answer:
in head-to-head runs the no-skill baseline produced a 57-word question with
46-word option descriptions where the skill produced a six-word question with
three distinct options.

The two things that make it distinctive:
- exactly one option carries a recommendation, and only when evidence earns it;
- the user can attach a written note to whichever option they choose, and that
  note overrides the label.

## The chosen concept (settled with the user — build this, do not re-open it)

**Option cards with a margin note.** Three stacked option cards. A vermilion
dot or mark on the recommended one. A small vermilion note written in the
margin beside the chosen card. The signature move is the margin note: it is the
part no sibling icon has, and it is the thing the skill is actually for.

## The marketplace house style — non-negotiable

- **Outside shape**: full-bleed 1024 on the set's exact superellipse. The path
  is at `plugins/create-mac-icon/assets/squircle-path.txt`. A rounded-rect
  approximation visibly breaks the shelf. Any raster take that ships gets masked
  with that same path.
- **Ground**: porcelain / daylight. The dark deep-sea register belongs to
  `trawl` alone — treat it as taken.
- **One warm accent** in the vermilion / ember / amber family, kin to
  Fledgeling's `#C4622D`, reserved for the focal or semantic element. Here that
  is the recommendation mark and the margin note. Never spent on decoration.
- **Material over flatness**: rich, soft-3D Tahoe gel-glass — volumetric gel,
  authored translucency and overlap, one soft top light, real contact shadows.
  The user has repeatedly chosen the richer material over a flatter vector, so
  push the painterly volumetric end.
- **Subject-mined literal glyph** with a stated signature move. No category
  clip-art, no glyph-on-blue-ramp.
- **16px survival** is a hard audit check.

## Sibling glyphs — do not duplicate any of these

- `trawl` — a trawl net, teal
- `design-review` — a UI surface with one column off its shared rail, vermilion
  registration mark on the break
- `armada-sync` — a manifest page, one entry stamped vermilion
- `compaction-quality` — a compressed graphite core banded with vermilion seams
- `improve-skill` — a plane blade mid-pass, trued behind, rough ahead
- `create-mac-icon` — a vermilion gel tile lifting out of its mould

Stacked cards are unclaimed. The margin note is unclaimed. Keep both legible.
</context>

<task>
Read `plugins/create-mac-icon/skills/create-mac-icon/SKILL.md` and follow its
process. It carries the direction catalogue, the ground-truth corpus, the
three-engine floor, the `audit.html` template, the material-recipes library and
the fidelity loop with its scoring harness. Follow it rather than hand-rolling
an icon pass.

Build the concept above.

Deliver into `plugins/clarify/assets/` in this worktree:
- the layered SVG master and its build script
- `icon.png` at 1024, plus `icon-256.png` and `icon-128.png`
- `audit.html` scoring every take, including the ones that lost
- the fidelity run directory
- any new construction appended to the skill's recipe library

Scope: this icon only. Do not touch the banner, the README, the skill files, or
anything outside `plugins/clarify/assets/`.

Run no git commands at all — no add, commit, branch, or checkout. The session
that briefed you owns every commit.

Do not spawn subagents; this is a single track of work.

Deliver what was asked at the scope intended, and make routine judgment calls
yourself. If some part of this brief looks wrong, say so in a sentence and carry
on rather than quietly changing it.

Report back in under 200 words: which take shipped, its 16px verdict, and
anything you had to depart from.
</task>
