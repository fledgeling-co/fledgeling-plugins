# Kilnhand — macOS app icon, delivery note

Commission run with the `create-mac-icon` skill. **Ships: `kilnhand-A1-wheelhead.svg`** (11/12, zero failures on checks 1–4). Full contact sheet with real renders, measured evidence and the losing takes: **`audit.html`**.

## Brief as taken

Kilnhand — a pottery-studio booking app. Personality: **warm, tactile, unhurried**. No brand colour constraint, no existing mark, no raster reference supplied. Nothing was open enough to be worth a question, so the calls below were made and are recorded rather than asked.

## Deviation: one engine, not three

`media-gen-pro` was unavailable in this environment, so the skill's stated fallback applied: **Engine A widened to three genuinely different hand-authored takes**, and **Engine B (Arrow vector) and Engine C (corpus-referenced raster) did not run**. These are named deviations, not silent omissions. What that costs, stated plainly:

- No independently-generated vector take, so no outside shape ideas were available to salvage into the master.
- No diffusion raster, so **no material target**. The fidelity loop (`fidelity.py score` / `gate`) requires a raster reference and therefore **did not run** — there is no `runs/` directory because there was no measurable loop, not because one was skipped. The master's material ceiling is untested rather than proven, which is exactly the gap the skill exists to close.
- What *was* run from the loop's toolkit: the static **`structure` gate** on all three masters (all PASS — 4 named layer groups each, well inside the 400-path / 200 KB envelope, no `<image>` or `<script>`).

The three takes are differentiated at the level the anti-sameness rules ask for, not by palette swap: three different ground registers (porcelain / dark charcoal / saturated tile), three different light models (soft top / emissive interior / soft top with frost), three different silhouettes.

## Direction and device

**Chosen:** Direction 2 *Tahoe Gel-Glass*, sub-register (a) — porcelain cushion tile carrying a coloured object — hybridised with Direction 1's **Tahoe-softening clause** (the 3D miniature survives the era change in matte-satin/clay with a real contact shadow). The answer key's tell #7 sanctions exactly this pairing, and it is what makes a pot look like clay rather than candy.
**Runner-up:** Direction 4 *Dark-Field Emissive* — built as take A2 rather than left as an assertion.

**Subject-mined device:** device-bank #4, inverted — not the hand, but **the trace of the hand**. The vessel's wall carries the rising throwing ridges a potter's fingers leave, with a wet-rim highlight at the lip. Signature move: **the fingerprint spiral**. It names the app (Kiln*hand*) and it is the "tactile" adjective made literal.
**Secondary device (A1 only):** device-bank #20, data-as-glyph — the wheel head carries 24 bat-pin ticks with exactly one glazed warm: **the session mark**, the booked slot. This is the only element carrying the *booking* half of the product; see liabilities.

**Calibration checks the reference demands:** no blue or indigo anywhere — the corpus's template default is explicitly avoided, and "warm" positively justifies the terracotta/amber family. The glyph is a thrown pot, not a category glyph (no calendar, no clock, no checkmark). Drawing a calendar *and* a pot was rejected as failure-mode #5, metaphor pile-up.

## Shared spec (step 0)

- **Canvas** 1024 full-bleed. No baked corner radius, no baked drop shadow. Only the rim-light/vignette layer is clipped to the system squircle (`squircle-path.txt`), because an edge treatment has to know where the edge is; the artwork under it stays full-bleed.
- **Palette** ≤2 hue families per take. Terracotta ramp `#E9A87C → #C9714A → #8E4527`; porcelain `#FFFDFB → #EDE6DE`; one bounded glaze accent `#F5B95F`. A2: emissive amber `#FFD79A → #F08A34` on warm charcoal `#2E2823 → #141110`. A3: terracotta gel tile `#E8946A → #B85331` under white frost at 72–94% opacity.
- **Light** one soft top light; rim highlights and soft AO carry depth; zero hard speculars. A2's second light is an emissive interior under a shell — the one sanctioned exception.
- **Layer plan** `bg` / `mid` / `fg` / `highlight` as named `<g>`s in every master, mapping 1:1 onto Icon Composer layers.

## The takes

| Take | Register | Rubric | Role |
|---|---|---|---|
| A1 · Wheelhead | porcelain cushion + matte-clay vessel on a wheel head | **11/12** | **ships** |
| A2 · Kiln Glow | dark charcoal + emissive kiln chamber, pot firing | 11/12 | runner-up (nocturnal brand) |
| A3 · Frostware | saturated terracotta gel tile + white frosted vessel | 10/12 | alternate (most orthodox current-era) |

Deductions, in short: A1 loses #11 because the session mark is sub-legible below 128px; A2 loses #9 because nothing in it is translucent, so it misses the era's defining tell; A3 loses #10 (a near-white glyph is hostage to ground *value* at the light end of the tint range) and #11 (its own device was cut — see below). Per-take reasoning, measured contrast, silhouette tests and tint variants are in `audit.html`.

## One branch, recorded

A3 was originally "Thumbprint": a vertical thumb-pull hollow drawn up the front wall. It was authored and rejected **twice** — at 1024 it read as an applied stripe rather than an indentation, and at 32px it was noise. Per the fidelity loop's *two consecutive rejections = stop or branch* rule it was branched rather than ground on, and A3 now carries A1's ridge device re-materialised in frost. The cost is honest and scored: A3 has no device of its own, which is why it lost #11.

## Deliverables

```
kilnhand-A1-wheelhead.svg      the shipping master (full-bleed, 4 named layers)
kilnhand-A2-kilnglow.svg       alternate
kilnhand-A3-frostware.svg      alternate
build_icon.py                  emits all three; geometry + material as named
                               constants, so a later fidelity round is a
                               parameter edit rather than path surgery
make_renders.py                audit renders, silhouette test, tint variants,
                               measured figure-ground contrast
squircle-path.txt              the system mask path (copied from the skill)
audit.html                     the contact sheet — renders, scores, losers,
                               measured evidence, recommendation + liabilities
audit-renders/                 1024 / 256 / 64 / 32 masked renders, -sil, -tint
preview/                       squircle-masked and tint SVGs (audit only,
                               never shipped)
```

## Known liabilities

1. **"Booking" does not read at small sizes.** The session mark is invisible below ~128px. If booking must read in the Dock, enlarge and warm the tick, or move the session mark into the vessel's rim as a notch so it lives in the silhouette.
2. **16px ambiguity.** The dark elliptical opening dominates at 16px; the icon can momentarily read as a mug. Lightening the interior gradient's far wall would separate "thrown pot" from "drink".
3. **No authored translucency in the shipping take.** Legal under the softened-3D-miniature clause, but A1 does not carry the era's most reliable tell. A3 is the take that does — if "unmistakably macOS 26" outranks "warm and tactile", ship A3 and fix its #10 liability instead.
4. **Untested material ceiling.** No Engine C raster means no fidelity loop, so nothing here has been measured against a diffusion render's volumetric shading. If media-gen-pro becomes available, the highest-value next step is one raster take in the porcelain register (reference images `apple-23.png` Safari + `apple-28.png` Photos + `apple-06.png` Home) and a bounded loop against it.
5. **Cross-renderer variance.** librsvg and WebKit (`qlmanage`) agree structurally, but WebKit renders the cushion vignette wider and the wet-rim highlight thinner. Re-check those two values if the icon is ever composited in a browser context.

## Not appended to `material-recipes.md` — and why

Two reusable findings came out of this run, but neither was confirmed by a measured fidelity iteration, and that file's contract is that entries are wins the loop confirmed. Recording them here instead, as candidates for a future run to confirm:

- **A blurred wide stroke needs a generous filter region.** A `feGaussianBlur` on a stroke wider than the path's bounding box gets clipped by the default filter region and renders as a hard-edged rectangle — a "material" defect that is really a plumbing defect. `x="-120%" y="-120%" width="340%" height="340%"` fixed three separate artifacts here.
- **A surface groove will not read as an indentation on a flat-shaded body.** Two rounds of paired flank shading still read as an applied stripe. Indentation appears to need either the silhouette (a notch in the rim) or a full per-face gradient separation, which is consistent with the existing "per-face gradient separation is the cheapest volumetric move" entry.
