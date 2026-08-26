# Icon commission — create-luke-content (fledgeling-plugins)

<context>

## What you are making

A macOS-style app icon for a Claude Code plugin called `create-luke-content`,
which ships in the `fledgeling-plugins` marketplace at
`/Users/lukerhodes/Dev/fledgeling-plugins`. The plugin directory is
`plugins/create-luke-content/`; its assets belong in
`plugins/create-luke-content/assets/`.

## The subject, so the glyph can be mined from it rather than from the category

The skill ghostwrites in one real person's voice. Two layers make it work, and
they are stacked:

- **The voice layer on top.** An evidence-anchored profile of how Luke Rhodes
  actually writes, every rule traced to a quoted sample of his real prose.
- **The craft layer underneath.** The structural discipline that decides whether
  a piece is any good as a piece: message hierarchy, what a claim has to be
  backed by, what an announcement or a landing page or an email is shaped like.

The rebuild this icon is for exists because the second layer was missing under
the marketing route. Voice-correct prose sat on nothing, and it read wrong. So
the icon's argument is: **there are two planes, and the one you can see is
resting on the one you cannot.**

## The concept the user chose

**"Voice over craft."** A translucent sheet carrying prose, lying on a ruled
measuring plane, with the rule showing through the sheet from underneath.

The user picked this over two alternatives, so it is settled: do not redesign
the concept. What is open is the execution, and that is the whole job.
Two things the concept has to earn:

- The lower plane must read as a **measure** (a rule, a scale, a grid with real
  graduations), not as decorative texture and not as a second sheet of prose.
  It is craft, and craft is measured.
- The upper sheet must read as **prose**, and the corpus's most reliable signal
  for that is a left-aligned ragged-right stack whose last line runs short.
  Note that the sibling plugin `armada-sync` already owns stacked prose capsule
  lines on porcelain as its whole glyph, so this must not resolve into that
  icon. The differentiators available to you: this one is two planes rather than
  one, the hero relationship is *through* rather than *on*, and armada-sync's
  accent is a seal band lying across a line where yours belongs to the lower
  plane.

Luke's single most distinctive mechanical habit is that he uses a **semicolon**
where most writers reach for an em dash, and the package hard-fails on em
dashes. If a punctuation mark can be worked in as a small true detail on the
upper sheet, it is the most Luke-specific thing available; treat it as an option
to test, not a requirement, and drop it if it costs the silhouette.

## The marketplace's house style — this is the repo's, not the icon skill's

- **Outside shape is non-negotiable.** Full-bleed 1024 on the set's exact
  superellipse. The path every sibling ships is at
  `plugins/create-mac-icon/assets/squircle-path.txt`. A rounded-rect
  approximation visibly breaks the shelf. Any raster take that ships gets masked
  with that same path.
- **Ground register: porcelain / daylight.** The dark deep-sea register belongs
  to the sibling `trawl` alone; treat it as taken.
- **One warm accent**, vermilion / ember / amber, kin to Fledgeling's `#C4622D`,
  reserved for the focal or semantic element. Never spent on decoration. Here
  the semantically right home for it is the lower plane, because the lower plane
  is the thing this rebuild added.
- **Material over flatness.** Rich soft-3D Tahoe gel-glass: volumetric gel,
  authored translucency and overlap, one soft top light, real contact shadows.
  The user has repeatedly chosen the richer raster material over a flatter
  vector, so push the painterly volumetric end and rebuild whatever wins into
  the layered master. Authored overlap is this concept's core craft tell: the
  rule is visible *because* the sheet above it is genuinely translucent, and
  that is the one thing a flat pre-masked raster cannot fake.
- **16px survival is a hard audit check.**

## Sibling glyph devices already spoken for — do not land on any of these

`armada-sync` prose lines with a seal band · `braindump` sediment cylinder with
glowing seams · `clarify` the drawn card · `code-review` the through-cut ·
`create-mac-icon` the cast · `create-skill` the casting flask pour ·
`create-swe-project` hull on a slipway · `dossier-report` the folded sheet
revealing a chart · `geminify` the second leaf · `improve-skill` plane iron and
shaving · `mac-doctor` capacity ring · `mockup-fidelity` the scribed overlay ·
`report` the creased sheet · `ship-armada` plot table · `ship-fleet` berth grid ·
`discipline` the set stop.

`mockup-fidelity`'s scribed overlay is your nearest neighbour, since it also
involves two registered planes. Read its `assets/icon-notes.md` before you
settle the composition and say in your notes how yours differs.

## Process

`create-mac-icon` is installed and it owns this procedure. Read its SKILL.md at
`/Users/lukerhodes/Dev/fledgeling-plugins/plugins/create-mac-icon/skills/create-mac-icon/SKILL.md`
and follow it: the direction catalogue, the device bank, the ground-truth
corpus, the three-engine floor, the `audit.html` template, the material-recipes
library, and the fidelity loop with its scoring harness. It carries lessons a
hand-rolled pass would start over on, and its recipe library should gain
whatever new construction this commission invents.

The score in that loop is a proxy for a human judgment. Make the icon right and
let the number follow; tuning constants against the score produces a high number
and a worse icon.

## Scope

In scope: the icon, its takes, its audit sheet, its layered master and build
script, the exported sizes, and `assets/icon-notes.md` in the house format the
siblings use.

Out of scope: the banner, the READMEs, the SKILL.md, the marketplace
registration, and anything in `plugins/create-luke-content/skills/`. Another
track owns those and is editing them concurrently. Write only inside
`plugins/create-luke-content/assets/`.

Deliver what was asked at the scope intended, make routine judgment calls
yourself, and if the brief looks mistaken say so in a sentence and carry on.

## Constraints

- **Run no git commands.** Not `add`, not `commit`, not `checkout`, not `stash`.
  The orchestrating session owns every commit and is working in the same tree.
- **Spawn no subagents.** This is a single track.
- Use `media-gen-pro` for raster engine takes as the icon skill directs.

</context>

<task>

Produce the icon.

Expected on disk when you are done, all under
`plugins/create-luke-content/assets/`:

- the layered SVG master and the build script that emits it,
- at least three engine takes spanning hand-authored SVG, Arrow vector, and
  raster,
- `audit.html` scoring every take including the ones that lost, with the
  recommendation block naming known liabilities,
- the fidelity run directory,
- `icon.png` at 1024, `icon-256.png`, `icon-128.png`,
- `icon-notes.md` stating the direction by name with its runner-up and the
  reason, the subject-mined glyph with its device-bank numbers, the signature
  move, the risk taken, and how it differs from `mockup-fidelity`.

Then run the sheet's own gate and leave it passing:

```
python3 plugins/create-mac-icon/skills/create-mac-icon/scripts/audit_sheet.py check plugins/create-luke-content/assets
```

Report back in about 250 words: the direction and runner-up, the glyph and its
signature move, what each engine take scored and why the winner won, the gate's
exit code, and any liability you are handing over.

</task>
