# Icon commission — atlas-publish

<context>
You are producing the app icon for `atlas-publish`, a new plugin in the
`fledgeling-plugins` marketplace. Everything you need is on disk; this brief
tells you where to look and what the house style is, because the house style
lives in the repo rather than in the icon skill.

## The skill this icon is for

`atlas-publish` is the only brand-specific plugin in this marketplace. It
carries two skills for **Atlas** (shipping brand "Bella"), an iOS beauty-review
app plus four Next.js services:

- `atlas-publish` — the release conductor. Takes the open PRs to a shipped
  release, classifying over-the-air JS-only updates against full App Store
  builds from the native fingerprint.
- `code-review` — the review pass that used to ship beside it, now a standalone plugin.

**The defining constraint is that draft is the terminal state.** The skill
archives, uploads and registers a bundle, then stops. Making a release live for
users is always an explicit human action it will not take. That refusal, not
the release machinery, is what the icon has to say.

## The brand mark exists, and it is the reason this icon is not generic

`/Users/lukerhodes/Dev/atlas-app/apps/atlas-app/assets/images/atlas-icon.png` —
1024x1024, a black script wordmark reading "Atlas", no alpha. Look at it before
deciding anything. It is genuinely distinctive and no sibling icon in this
marketplace ships a letterform of any kind.

That source directory is read-only. Trace from it; never write to it.

## The chosen concept (settled on renders — build this, do not re-open it)

**The stroke that stops at the gate.** The mark's capital A, lifted verbatim and
cut at the exact point where the letterform hands over to the `t`, re-poured as
a soft-extruded graphite gel monoline on warm porcelain. Where the next stroke
would begin, a vermilion gate slab stands instead, and the script's exit stroke
butts flush against its flat left face. The porcelain beyond the gate is bare.

The signature move is **the cut at the handover**: the word is drawn as far as
it can be drawn without a person, and stopped by something deliberate rather
than by running out.

Two things the concept must survive, both of which killed earlier versions:

- The **whole word** is a wordmark, which trips the catalogue's own no-text rule
  and is a horizontal smear at 16px. A single letterform is the sanctioned form
  (device #15, diegetic monogram; device #19, re-materialised brand mark).
- A **pill-shaped** accent reads as a text caret sitting after a letter. The
  gate needs a flat left face for the stroke to press against.

## The marketplace house style — non-negotiable

- **Outside shape**: full-bleed 1024 on the set's exact superellipse. The path
  is at `plugins/create-mac-icon/assets/squircle-path.txt`. A rounded-rect
  approximation visibly breaks the shelf. Any raster take that ships gets masked
  with that same path.
- **Ground**: porcelain / daylight. The dark deep-sea register belongs to
  `trawl` alone — treat it as taken.
- **One warm accent** in the vermilion / ember / amber family, kin to
  Fledgeling's `#C4622D`, reserved for the focal or semantic element. Here that
  is the gate and nothing else. Never spent on decoration.
- **Material over flatness**: rich, soft-3D Tahoe gel-glass — volumetric gel,
  authored translucency and overlap, one soft top light, real contact shadows.
  The user has repeatedly chosen the richer material over a flatter vector, so
  push the painterly volumetric end.
- **Subject-mined literal glyph** with a stated signature move. No category
  clip-art, no glyph-on-blue-ramp.
- **16px survival** is a hard audit check.

## Sibling glyphs — do not duplicate any of these

Read the full set at `plugins/*/assets/icon-256.png` before committing; the
ones that bear on this concept are:

- `agent-voice` — a dark card with two vermilion quote strokes
- `tui-craft` — a dark terminal panel with a vermilion cursor
- `mac-design-digest` — a dark card with a vermilion wax seal
- `should-compact` — two dark blocks with a vermilion seam
- `better-loop` — a track with a vermilion block held on it
- `whats-left` — an arch with a vermilion keystone held above it
- `ship-feature`, `ship-fleet`, `shipyard`, `create-swe-project` — between them
  they own every ramp, slipway, cradle and hull in the marketplace

That last row is why "a sealed bundle held at the lip of a stage" is a harder
concept than it sounds. A letterform is unclaimed; a dark slab is not.

</context>

<task>
Read `plugins/create-mac-icon/skills/create-mac-icon/SKILL.md` and follow its
process. It carries the direction catalogue, the ground-truth corpus, the
three-engine floor, the `audit.html` template, the material-recipes library and
the fidelity loop with its scoring harness. Follow it rather than hand-rolling
an icon pass.

Build the concept above.

Deliver into `plugins/atlas-publish/assets/`:
- the layered SVG master and its build script
- the derived glyph path, plus the script that reproduces it from the brand mark
- `icon.png` at 1024, plus `icon-256.png` and `icon-128.png`
- `audit.html` scoring every take, including the ones that lost
- the fidelity run directory
- `icon-notes.md`, recording which concept shipped and what the losing one was
  better at

Scope: this icon and its banner. Do not touch the skill files, the README,
`plugin.json`, the marketplace manifest, or anything outside
`plugins/atlas-publish/assets/`.

Run no git commands at all — no add, commit, branch, or checkout. A pre-push
hook in this repo drafts and sends marketing email to real subscribers.

Deliver what was asked at the scope intended, and make routine judgment calls
yourself. If some part of this brief looks wrong, say so in a sentence and carry
on rather than quietly changing it.

Report back in under 200 words: which take shipped, its 16px verdict, and
anything you had to depart from.
</task>
