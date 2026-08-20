# Icon commission — code-review

<context>
You are producing the app icon for `code-review`, a new plugin in the
`fledgeling-plugins` marketplace. Everything you need is on disk; this brief
tells you where to look and what the house style is, because the house style
lives in the repo rather than in the icon skill.

## The skill this icon is for

`code-review` reviews a diff, a PR or a branch range and reports findings. It is
the general successor to two narrower skills. Three things make it itself:

- **It runs many independent finder angles that are forbidden from suppressing
  each other.** Two angles that flag the same line for different reasons both
  survive; deduplication happens later, on evidence.
- **It has three verdicts, not two.** CONFIRMED, PLAUSIBLE, REFUTED, and only
  REFUTED drops. The middle state existing at all is the point: realistic but
  unproven survives instead of going out with the noise.
- **It prints what it could not check.** A coverage ledger with a not-checked
  column, so a skipped check never reads as a clean one.

The third is the strongest signature available and no sibling says it: the
review that reports its own blind spot.

## The chosen concept (settled on renders — build this, do not re-open it)

**The Open Column.** A graphite gel slab, the ledger, its face carrying four
faint engraved rows. A tall rectangular column is cut clean through it, off to
the right, so the porcelain the slab stands on shows through the opening. The
cut wall is chamfered and poured in vermilion, brightest on the faces turned
into the key light. Light that got through the opening lands on the porcelain
past the slab's foot.

The signature move is **the through-cut**: an absence that was machined rather
than one that merely happened. The rows run up to it and stop, which is the
coverage ledger's not-checked column made physical.

Two things the concept has to survive, both of which killed an earlier version:

- **A notch is not a hole.** Every graphite margin around the chamfer has to
  clear 100px at 1024, or the opening reads at 16px as a bite taken out of the
  slab's right edge rather than as an interior void, and the meaning inverts.
- **A thin accent dies before a fat one at equal area.** Divide the opening's
  smallest dimension by 64 and it has to come out over 1.5px. At 168px wide it
  is 2.6px and it reads.

## The marketplace house style — non-negotiable

- **Outside shape**: full-bleed 1024 on the set's exact superellipse. The path
  is at `plugins/create-mac-icon/assets/squircle-path.txt`. A rounded-rect
  approximation visibly breaks the shelf. Any raster take that ships gets masked
  with that same path.
- **Ground**: porcelain / daylight, `#FBF7F0` to `#DED4C2`. The dark deep-sea
  register belongs to `trawl` alone — treat it as taken.
- **One warm accent** in the vermilion / ember / amber family, kin to
  Fledgeling's `#C4622D`, reserved for the focal or semantic element. Here that
  is the cut wall and the light it throws, and nothing else.
- **Material over flatness**: rich, soft-3D Tahoe gel-glass — volumetric gel,
  authored translucency and overlap, one soft top light, real contact shadows.
  The user has repeatedly chosen the richer material over a flatter vector, so
  push the painterly volumetric end.
- **Subject-mined literal glyph** with a stated signature move. No category
  clip-art, no glyph-on-blue-ramp.
- **16px survival** is a hard audit check.

## Sibling glyphs — do not duplicate any of these

Read the full set at `plugins/*/assets/icon-256.png` before committing; there
are forty-one. The ones that bear on this concept:

- `atlas-publish` — a graphite script letterform stopped against a vermilion
  slab. This plugin's sibling, and the one whose banner device is closest.
- `design-review` — frosted UI cards under a vermilion crosshair. Inspection
  optics are taken.
- `be-my-witness` — an eyepiece on a measuring grid. Judgement optics are taken.
- `test-campaign` — a grid of nine tiles, one vermilion and one left blank. The
  closest semantic neighbour: it already owns "an empty cell in a grid", so the
  absence here has to be a hole in a solid, not a missing tile.
- `armada-sync`, `report`, `stocktake`, `warrant` — between them they own every
  stack of horizontal bars in the marketplace, so rows can be texture here but
  never the subject.
- `mockup-fidelity`, `tui-craft`, `agent-voice` — a dark rounded mass carrying
  one small warm mark, three times. The nearest structural neighbours at 16px.

A hole cut through a solid body is unclaimed. Nothing in the set has one.
</context>

<task>
Read `plugins/create-mac-icon/skills/create-mac-icon/SKILL.md` and follow its
process. It carries the direction catalogue, the ground-truth corpus, the
three-engine floor, the `audit.html` template, the material-recipes library and
the fidelity loop with its scoring harness. Follow it rather than hand-rolling
an icon pass.

Build the concept above.

Deliver into `plugins/code-review/assets/`:
- the layered SVG master and its build script
- `icon.png` at 1024, plus `icon-256.png` and `icon-128.png`
- `audit.html` scoring every take, including the ones that lost
- the fidelity run directory
- `banner.png` at 3200x1040 with its `banner-src.html` and signed verdict
- `icon-notes.md`, recording which concept shipped and what the losing one was
  better at

Both gates have to exit 0: `audit_sheet.py check <dir>` and
`banner_sheet.py check <dir>`.

Scope: this icon and its banner. Do not touch the skill files, the README,
`plugin.json`, the marketplace manifest, or anything outside
`plugins/code-review/assets/`.

Run no git commands at all — no add, commit, branch, or checkout. A pre-push
hook in this repo drafts and sends marketing email to real subscribers.

Deliver what was asked at the scope intended, and make routine judgment calls
yourself. If some part of this brief looks wrong, say so in a sentence and carry
on rather than quietly changing it.

Report back in under 200 words: which take shipped, its 16px verdict, and
anything you had to depart from.
</task>
