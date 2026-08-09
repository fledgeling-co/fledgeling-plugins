# clarify icon notes

**Direction: "The Drawn Card".** Direction 2 *Tahoe Gel-Glass*, sub-register (a) — porcelain
cushion tile carrying one lit object — crossed with the device bank's #24 *UI-primitive-as-mark*,
#16 *the icon performs the verb* and #21 *authored overlap*. The subject is a skill that decides
whether to interrupt you with a question and then composes that question so it costs one click to
answer, so the icon shows the answered question: three option cards stacked as a list, the
recommended one **drawn out of the stack** into the light with a vermilion gel bead in its
selection well, and a vermilion note jotted in the margin its own displacement opened.

Runner-up: the same three cards as flat frosted panels in the register of `design-review`.
Rejected because that sibling already owns translucent UI panels with a vermilion registration
mark, and because a flat panel cannot show a card being *drawn out* of anything — the whole
argument here is physical displacement.

**Signature.** The drawn card and its margin. Every sibling that quotes an interface quotes it
flat; this one treats the option list as a physical stack and pulls one card clear of it, which
does three things at once: it names the recommendation without a label, it opens the margin, and
it puts the note somewhere that means something. The note is the part no sibling has, and it is
the thing the skill is actually for — the user attaches a written note to whichever option they
choose, and that note overrides the label.

**What the margin note is not, and why.** Four treatments were built and rendered before the
jotted lines won (contact sheet in `audit.html`): a proofreader's caret straddling the card's
right edge, a leader stroke crossing the boundary into the note, the grey label rule continuing
into vermilion past the card edge, and a bracket tying the note to the card. Every one of them
read as an **arrow**. That is the finding worth keeping: at icon scale a long stroke leaving a
shape is a pointer, whatever it is meant to be, and semantics do not survive the reading. The
note earns its association instead by sitting at the drawn card's own level in the space that
card opened, tilted off the horizontal — three parallel bars of equal weight read as a menu
glyph, and a hand does not write parallel.

**Palette.** Two families. Warm-neutral porcelain and clay carry the ground and the cards
(`#FFFEFB` → `#F5F0E5` → `#E2D8C2` cushion with a `#9C8D74` vignette; the drawn card `#FEFCF5` →
`#F1E9D8` over a `#BBAE95` → `#7A7059` wall; the two cards still in the stack `#A99D8A` →
`#8D8170` over `#7A6F5B` → `#4C4435`). One vermilion, kin to Fledgeling's `#C4622D`, is spent on
the recommendation bead (`#E36C40` → `#DA5B31` → `#D24B1E` → `#A82F0E`) and on the margin ink
(`#EC7F4C` → `#DD5A28`), and nowhere else. One soft top-left key: rim scatter on every top edge,
soft ambient occlusion, real contact shadows, zero hard speculars, no emissive interior — that
sanctioned second source is `trawl`'s.

**Deliberate avoidances.** The dark deep-sea register (`trawl`). The blue/indigo ramp the corpus
census records as the template default. And every sibling glyph: `armada-sync`'s stamped manifest
entry, `design-review`'s frosted proof panels, `compaction-quality`'s banded core,
`improve-skill`'s plane blade, `create-mac-icon`'s cast tile and mould, `trawl`'s net.

## Audit: 11 of 12, zero failures on the non-negotiable 1 to 4

Full contact sheet with every take scored and every loser kept: `audit.html`.

Full-bleed 1024 artwork with the marketplace superellipse as a *clip* — no baked corner radius,
no baked drop shadow. The focal group spans x 163–870 and y 238–803, so margins are 163 / 153 /
238 / 220 and the composition is optically centred. Checks 3 and 4 were verified on real renders
rather than imagined: a silhouette proof built by subtracting the ground layer and thresholding
still names "three stacked cards, the middle one marked, a note beside it", and the true 16px
render resolves as dark band / light band carrying a warm mark / dark band.

**The point is deducted at #7, figure-ground**, and the number is a range rather than a value.
The two shaded cards run **2.25:1** at their lit top-left corner to **3.60:1** at their shaded far
end against the tile ground, with their extrusion walls at 5.0–6.4:1; the bead clears the bar at
**3.04:1** against its own card; the margin note reaches **2.71:1** against the ground. But the
drawn card itself sits at **1.02:1** against the tile and reads as figure only through its own
shadow and its two darker neighbours. In a porcelain register a light object cannot clear 3:1
against a near-white field — Apple's own Contacts and Reminders do not either — so the honest
statement is that the mass clears the bar over most of its area and the accent clears it outright.

**#10 passes by construction:** four layers, `bg` / `mid` / `fg` / `highlight`, mapping 1:1 onto
Icon Composer, with identity carried by shape and value and colour as the last ten percent. The
drawn card, its bead and the margin note all live in `fg`.

### Known liabilities

1. **Figure-ground is a range, 1.02:1 to 3.60:1**, as above.
2. **The focal spans 69.1% of tile width**, over the 55–65% composition constant. Taken
   deliberately so the margin note stays legible beside the drawn card; the raster reference
   spans 75%.
3. **The margin note is the weaker of the two accent marks** at 2.71:1. Darkening it further
   makes ink on a page read as a second gel body, which is the wrong material claim.
4. **At 16px the two vermilion marks merge into one warm smear** on the middle band. The icon
   keeps its subject at menu-bar size and loses the "note in the margin" argument there.
5. **The shipped take scores lower against the raster reference than round 9 did** (1024
   composite 0.6202 → 0.5452). That is rounds 10–12 doing their job, not a regression — see below.
6. **LPIPS did not run** (no torch on this host), so every 1024 material number came from the
   weaker of the two available metric stacks and should be read as directional.

## Three engines

- **Engine A** is the shipping master, `icon.svg`, generated by `build_icon.py` so geometry and
  material are named constants and every fidelity round is a parameter edit rather than path
  surgery. 11/12.
- **Engine B**, `icon-engineB-arrow-954e4a.svg`, Arrow 1.1 from the spec-as-brief, lost at 4/12:
  a rounded-corner tile baked into the artwork on a 154.6 × 154.9 viewBox that is not square, so
  it can never be masked with the set's path; no named layer groups; flat CSS-class fills. It did
  get the structure right — three slabs, a bead on the middle one, three margin strokes — and its
  real contribution was as a negative control: the concept survives being drawn with no material
  at all, which is evidence that the material is doing separate work from the composition.
- **Engine C** produced two rasters through GPT Image 2 with four porcelain-register exemplars
  from `corpus/apple-2026/` as reference images (Reminders, News, Safari, Calculator). Both scored
  8–9/12 and both **won the material comparison**, as the pipeline expects. Neither can ship: a
  flat raster is failure mode #10 by definition, and both grounds are dead-flat white with no
  cushion, which the Tahoe grammar names as the previous era's tell. Both are kept,
  squircle-masked with the exact path, as `icon-engineC-*-masked.png`.

**C2 was chosen as the fidelity reference over C1** on two counts that its score does not carry:
C1's palette is colder and greyer, drifting out of the marketplace's warm-porcelain family, and
its margin note breaks into strokes of near-equal length, which reads closer to a menu glyph than
to handwriting.

## The fidelity loop

Thirteen rounds against `icon-engineC-4c230c-2-masked.png`, one edit class each, state in
`fidelity-runs/` with a `score.json` per round and a `rounds.json` ledger. The full table with
per-size composites is in `audit.html`.

| Phase | Rounds | 1024 | 16 | Gate |
|---|---|---|---|---|
| baseline | r00 | 0.6105 | 0.7866 | baseline |
| rebuild toward the reference | r01–r09 | 0.6202 | 0.8286 | ACCEPT (r06 vs r00, +0.1796 net) |
| divergence from the reference | r10–r12 | 0.5452 | 0.7157 | REJECT, shipped |

**The rebuild, r01–r09.** The raster's structural answer was the round that mattered: its cards
*overlap* into a stack where the first draft had three separated rows, which is both why the
raster read as cards and why the draft read as a settings list. Everything after that was
material — a vertical wall ramp, a measured occlusion line under every card, a lit top arris, the
bead's ramp resampled off the reference. r01–r05 all gated REJECT against intermediate states
that never became the accepted baseline; the verdict that settles the phase is r06 against r00,
which the gate ACCEPTs at +0.1796 net with every size improved.

**The divergence, r10–r12, and why it ships against the gate.** The reference is porcelain cards
on a porcelain ground. At 16px that has almost no value separation between glyph and field, and
downsampled beside `armada-sync` and `improve-skill` — whose glyphs are genuinely dark — the
master went to a pale blob with two vermilion specks. The accent survived, so it did not read as
broken; the subject did not survive, which is a hard failure of check #4. Converging further on
the reference makes it worse, because the reference has the same weakness and merely hides it
behind a flat white ground and heavy shadows.

So the value ramp moved, not the ground: the two options still in the stack are clay in shade, the
one drawn out of it is porcelain in the light. The ground stays porcelain, the register is
unchanged, and the deep-sea register stays `trawl`'s. Measured, the 16px contrast spread went
**0.229 → 0.362** against the reference's **0.326**, and the composite paid 0.075 at 1024 for it.
Gate informs; rubric decides.

**Four rounds were driven by measurement rather than by looking.**

- r02 came from perpendicular luminance profiles across the reference's card edges: under the
  drawn card the wall bottoms out near 0.63, then a hard dark line at **0.408**, then a 50px
  recovery. The master had no contact anywhere, so every boundary inside its stack was a value
  step of about 0.06 — which is exactly what dissolves at 32px.
- r05 came from profiling the reference's bead. It is not a glossy sphere: the body is nearly
  **flat** at L 0.47–0.49, the bright ring lives at the **rim** (0.65–0.71) and not at the centre,
  and it sits in a **recessed dark well** (L 0.54–0.56) rather than glowing on the surface. The
  master had a bright core and a warm bloom halo — the bloom had been carried over from Apple's
  Reminders, a different icon, on an assumption rather than a sample. Removing it fixed a mark
  that read as a stain.
- r07 caught a bug in the master rather than a mismatch: the wall's "vertical" gradient vector was
  x-dominated, so every point on the band projected past offset 1 and the whole 32px-long
  extrusion rendered as **one flat colour**. See the recipe below.
- r08 and r12 were both ratio work done by sampling: the bead deepened to the reference's own
  median L (which cleared rubric #7 as a side effect), and the shaded cards deepened until their
  faces cleared 3:1 against the tile.

**One construction bug worth recording separately.** The `highlight` layer breaks z-order by
existing: the back plane's rim lights are painted after the front card, so the lower card's lit
top edge drew a white hairline straight across the drawn card's wall. It is fixed with a
`backKey` mask that subtracts the drawn card's silhouette and paints its cast shadow in at partial
grey, so a rim light inside a cast shadow is dimmed rather than running at full strength — the
single light model contradicting itself is the same defect `create-mac-icon` recorded at its r03.

**Recipe added to `material-recipes.md` this session:** *a gradient's dominant axis is the one it
is measured along* — the flat-extrusion bug from r07.

## Files

| File | What it is |
|---|---|
| `build_icon.py` | Engine A generator. Edit the constants here, never `icon.svg`. |
| `icon.svg` | the shipping layered master, fidelity round 12 |
| `icon.png`, `icon-256.png`, `icon-128.png` | raster exports of the master |
| `icon-r00-baseline.svg` | the master before the loop, kept as the before |
| `icon-engineB-arrow-954e4a.svg` | Engine B take, 4/12 |
| `icon-engineC-9153f5.png`, `icon-engineC-4c230c-2.png` | Engine C rasters, as generated |
| `icon-engineC-*-masked.png` | the same two, masked with the set's exact superellipse |
| `measure.py` | reads the reference's numbers: card bands, edge profiles, accent ramp, shadow falloff |
| `render_audit.py` | renders every take at the sheet's 2x sources and masks the rasters |
| `rounds_ledger.py` | rolls the per-round scores up into `fidelity-runs/rounds.json` |
| `montage.py` | tiles renders side by side for a look |
| `audit.html`, `audit-renders/` | the contact sheet and its renders |
| `fidelity-runs/` | per-round candidates, scores, residuals, edge maps, `rounds.json` |
| `squircle-path.txt` | the set's superellipse, copied from `create-mac-icon/assets` |
