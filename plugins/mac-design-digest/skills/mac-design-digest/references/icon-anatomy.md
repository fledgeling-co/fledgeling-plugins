# macOS App Icon Anatomy & Evaluation

Reference for digesting app icons (e.g., from macapp.supply/icons). Covers canvas geometry, the era model, composition conventions, and the digest fields.

**Without this file, an icon digest classifies nothing and compares nothing** — it reports colours and a shape, and every icon reads as sui generis. The era model in §2 is what makes two icons commensurable: era first, then everything else is read relative to that era's grammar, so a "flat" icon in 2013 and a "flat" icon in 2026 stop being the same observation. §5's field list is what makes a digest joinable to the next one.

Written from Apple HIG app-icon guidance and observed mac indie-icon practice; where a user-supplied Apple UI kit or Icon Composer template contradicts this file, the kit wins. §4's rubric is owned by `create-mac-icon` and cited here rather than restated.

## 1. Canvas and grid

- **Master canvas:** 1024×1024px, delivered as a full-bleed square; **macOS applies the rounded-rectangle (squircle) mask and the system drop shadow itself**. Since macOS 26, custom-shaped icons and hand-drawn outside-the-mask protrusions are normalised away — design inside the mask.
- **Apple icon grid:** the HIG grid template overlays concentric circles and squares on the canvas. Key uses when analysing:
  - **Optical centring** — glyphs sit on grid circles, not geometric centre.
  - **Consistent visual weight** — a wide glyph uses the inner square; a round glyph uses the larger circle, so different shapes read as the same size in the Dock.
  - **Margin discipline** — primary artwork stays inside the safe zone; art bleeding to the mask edge is a deliberate, nameable choice (common for background fields, rare for glyphs).
- **Required render sizes:** 16, 32, 128, 256, 512 (+@2x). Detail must *degrade gracefully*: an icon that reads at 1024 but smears at 16 fails Dock/Spotlight/menu-bar duty.

## 2. The era model — load-bearing, and the only copy in the pair

Classify every digested icon into an era before anything else. It anchors the rest of the analysis, because it is what makes two icons commensurable: a "flat" icon in 2013 and a "flat" icon in 2026 are not the same observation until you know which language each is speaking. Eras are visual languages rather than dates; new indie icons often quote an older era deliberately, and that quotation is a signature move rather than a defect.

**This section is now the only home for the era model across this skill and `mac-craft`.** That skill cut its bundled icon corpus outright and cedes all icon work to `create-mac-icon`, so nothing else in the pair carries the era boundary. Keep it current; a stale era table quietly mis-files every icon digested after the next macOS release.

| Era | System window | Signature | Tell-tale evidence |
|---|---|---|---|
| **Classic skeuomorphic** | ≤ OS X Mavericks | Photoreal objects, free silhouettes, heavy textures | Non-squircle outline, literal materials (felt, leather, glass) |
| **Flat-transition** | Yosemite – Catalina | Flattened but still free-form silhouettes; circles, tilted rectangles | Mixed shapes in the Dock; simple gradients |
| **Big Sur unified** | Big Sur – Sequoia | Uniform squircle; front-facing; soft top-down lighting; baked micro-shadows; "tool at an angle" overlays | Squircle base + a diagonal tool/glyph breaking the front plane |
| **Liquid Glass** | macOS 26 (Tahoe) + | Layered glass: background + foreground layers composed in Icon Composer; specular highlights, refraction, translucency; system-generated light/dark/clear/tinted variants | Glass edge highlights, layer parallax feel, tinted-mode compatibility |

### Era-delta evidence — the highest-value icon input there is

**One app, two icons, either side of an era boundary.** Digest both and mark them as an era pair. This is the only evidence class that isolates what *the platform* changed while holding the app's own taste constant: same subject, same designer, same brand, different era grammar. Everything that differs is either the era or a deliberate redesign, and the app's continuity tells you which.

Record it as two digests plus one delta note in `icons/<app>.md`: what survived (the identity — silhouette, palette family, the signature device), what the era took (baked shadows, a pre-masked raster, a hard gloss sweep), and what the era gave (layer separation, authored translucency, variant robustness). **The delta is worth more than either digest alone**, and it is the one reading that can settle whether a corpus rule is an era convention or a timeless one — which is exactly the distinction canon promotion turns on.

An era pair still counts as **one app** toward the ≥3-independent-apps bar. Two icons of one subject are one root; the pair's value is qualitative, not arithmetic.

Two known gaps in `create-mac-icon`'s corpus, worth knowing when you cite it as a comparison set: its exemplar roster is headed "A-grade" but 14 of its 51 apps are graded B, so the heading overstates the set; and Slack and ChatGPT appear in it with no analysis block at all. Cite specific graded entries rather than the roster's heading.

## 3. Composition conventions (what to look for)

**Silhouette & figure-ground**
- One dominant glyph or object; instantly nameable ("a paper plane", "a terminal prompt"). Multi-object icons need a single clear anchor.
- Figure-ground: glyph-to-background contrast ≥3:1 as a floor; the best icons hold silhouette clarity even in grayscale.

**Lighting model**
- Canonical light source is **top-down** (Big Sur era) or **environmental glass** (Liquid Glass). One icon = one light model; mixed lighting is a defect.
- Baked shadows are subtle and short; long dramatic shadows read as web-graphic, not mac.

**Palette**
- Typically 1–2 hue families + a gradient ramp within each. Background ramps run light-at-top → darker-at-bottom (sky logic), usually within one hue.
- Saturated accent reserved for the glyph or its focal detail — same de-emphasis logic as UI.

**Depth & materials**
- Big Sur era: 2–3 stacked planes (background field, glyph, optional tool overlay), each with its own micro-shadow.
- Liquid Glass: explicit layer stack (background, 1–4 foreground glass layers); glass properties (specular, translucency) applied per layer in Icon Composer; test mentally against dark and tinted modes.

**Personality devices** (the indie signature space)
- The diagonal tool (pen, hammer, magnifier) crossing the squircle — Apple's own tradition (TextEdit, Preview).
- Mascots/characters, framed-window motifs, glyph-on-tilted-card, macOS-native materials quoted (brushed metal as nostalgia).
- Record these as `[GOLDEN-NUGGET]` observations — they're where icon taste lives.

**Typography in icons**
- Rare and risky; letters shrink badly. Single-letter monograms work only with strong shape logic. Words are almost always a defect.

## 4. Icon evaluation rubric — cited, not owned here

**`create-mac-icon` owns the 12-point rubric.** Its canonical text lives in that plugin's `references/icon-directions.md`, which carries the per-check corpus statistics and the generation bar. This file previously held a third copy, and the copy had silently lost the two statistics that make the rubric actionable — which is exactly how a restated rubric fails: it drifts, and nothing notices. **Where this index and that file differ, that file wins**, and a difference worth noticing is worth reporting.

Digestion needs the enumeration to produce an `n/12` score, so the checks are indexed here by name only:

1 mask discipline · 2 grid adherence · 3 silhouette test · 4 16px squint test · 5 single light model · 6 palette economy · 7 figure-ground contrast ≥3:1 · 8 depth coherence · 9 era coherence · 10 variant robustness under dark/clear/tinted · 11 personality device · 12 no-text check.

Two of those carry corpus statistics, and they are what turn a checklist into a priority order *(both attributed to `create-mac-icon`'s corpus of 532 shipping icons)*:

- **#3 silhouette — 26 icons fail here.** Non-negotiable.
- **#10 variant robustness — 76% fail, the highest-leverage fix.** They ship a flat pre-masked raster, so identity rides on a colour relationship that dies under Dark/Clear/Tinted.

Scoring rules for digestion: pass/fail with one line of evidence each. A borderline check is a **soft pass** — score it as a pass and flag it in prose, because the flag is what reaches synthesis. Checks 1–4 are what the system and the Dock do to an icon regardless of intent, so a failure there is structural rather than stylistic. The *generation* bar (≥10/12, no failures on 1–4) belongs to `create-mac-icon`; this skill scores what exists rather than gating what ships.

## 5. Icon digest fields

Capture per icon (template in corpus-templates.md):

- App, source, era classification, rubric scores
- **Palette:** background ramp (hex → hex), glyph colours, accent
- **Composition:** background field type (flat/ramp/scene), glyph type (abstract/object/mascot/monogram), overlay device (none/tool/badge)
- **Light model:** direction, shadow length/softness, specular presence
- **Layer stack:** enumerated planes, background → front
- **Signature devices:** the nameable moves
- **Cross-icon notes:** which digested icons it rhymes with (feeds icon style clusters)

## 6. What icon digestion feeds

- `icons/<app>.md` — the individual digest
- `ICONS.md` — synthesis: era distribution, recurring palettes, recurring devices, icon style clusters, and **canon rules for generating new mac icons** (same ≥3-independent-apps promotion bar as UI canon)
- Design mode: when asked to design an icon, load ICONS.md + the 2–3 nearest digests, choose era + light model + palette ramp *before* sketching composition, then audit against §4.
