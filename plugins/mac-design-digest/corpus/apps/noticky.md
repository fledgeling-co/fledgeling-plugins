# Noticky — profile

- **Source:** macapp.supply (cover composite only — no raw app screenshots supplied) · **Surfaces digested:** floating note panels ×4 (one shot, marketing render) · **Last updated:** 2026-07-19
- **One-sentence identity:** macOS Stickies grown up into *structured* paper cards — checklists, bullet lists and a masked-secret field on saturated pastel panels, with every control drawn as monochrome ink so each note keeps reading as paper, not a form. Reference peers: Apple Stickies (ancestor), Antinote, Notion's colored callouts.
- **Cluster:** unassigned (candidate: "friendly-paper / playful-utility" — sole member so far)
- **Lineage:** native (med) — SF Pro system type, frameless Stickies-style NSPanel-class windows, compact 13pt-class body, real macOS menu bar + Dock in the scene. Confidence capped at *med* because the only evidence is a **marketing composite render**, not a raw screenshot: window shadows, chrome and the "screen" are art-directed, so no measurement is clean and no live chrome (traffic-light states, focus rings, vibrancy) can be inspected.
- **Era (chrome):** custom — the app custom-draws opaque colored *paper* note surfaces; correctly keeps content opaque (no glass-in-content). No toolbar/sidebar/glass is shown, so Liquid-Glass vs Big-Sur era is **not determinable** from this evidence. Surrounding desktop (wallpaper, Dock, menu bar) reads current macOS.

## Tokens

All app-surface tokens are `(estimated)` at best and `(assumed)` where noted: the source is a nominal-scale marketing render, not a pixel-accurate capture. Treat every value as directional, not authoritative.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| note/paper-yellow | `#FDE375` | (estimated)(inferred) | Q2 Roadmap panel; the saturated hero hue |
| note/paper-pink | `#F5B2CD` | (estimated)(inferred) | Design ideas panel |
| note/paper-green | `#B9E17B` | (estimated)(inferred) | Daily goals panel |
| note/paper-blue | `#8EBDFC` | (estimated)(inferred) | API Key panel |
| note/ink-primary | black, ~#0F0D05 | (estimated)(confirmed) | title + body both near-black on every paper; hierarchy is weight-only, no color de-emphasis of body |
| type/title | ~15px SF Pro **Bold**, black | (estimated)(confirmed) | "Q2 Roadmap", "Daily goals", "API Key" — one bold title per note |
| type/body | ~13px SF Pro Regular, black | (estimated)(confirmed) | checklist / bullet item text |
| control/checkbox | rounded square, ~1.5px **black stroke**, empty-off / **black check**-on; radius ~4px | (estimated)(confirmed) | NOT the native accent-filled checkbox — drawn as ink on paper (see Signature) |
| control/bullet | small filled round bullet, ink | (estimated)(inferred) | Design-ideas list |
| control/secret-field | rounded-rect ~capsule, translucent darker fill over paper, value + trailing lock glyph | (estimated)(inferred) | masks "sk_live_51H8x…"; radius ~10px |
| control/overflow | "···" three-dot menu, gray, top-right corner of every note | (estimated)(confirmed) | the note's only visible chrome affordance |
| control/truncation | "···" bottom-left of a note = "more content below" | (estimated)(recurring within app) | appears on Q2, Design ideas, Daily goals |
| warn/link | black label + solid **red underline** ("Do not share") | (estimated)(inferred) | custom warning affordance, not a blue hyperlink |
| radius/note | ~10–12px | (estimated)(inferred) | panel corner |
| space/pad | ~16px note inner padding; ~8px item gap; ~26–28px checklist row | (estimated)(inferred) | reads on an 8/4 grid; no magic numbers visible |
| elevation/note | single soft diffuse drop shadow; no border | (estimated)(confirmed) | the paper edge + shadow is the entire "frame" |
| chrome/frame | **frameless** — no title bar, no traffic lights | (estimated)(confirmed) | floating panel like Stickies |

### Brand evidence (left marketing panel — NOT app tokens; recorded separately, never merged into app canon)

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/bg | `#F8F9F9` warm near-white | (measured) | left panel ground |
| brand/headline | black `#000000`, heavy/black weight, tight, large display | (measured) | "Sticky notes. Always on top." |
| brand/accent | `#F7D155` gold-yellow | (measured) | "Hidden when you share." accent line — slightly more gold than the note yellow |
| brand/subtitle | `#AAAAAA` gray | (measured) | supporting copy |
| brand/feature-icons | 4× monochrome thin-stroke line icons, consistent stroke | (estimated) | screen-share / recording / screenshot / fullscreen states |
| brand/store-badge | black "Download on the Mac App Store" | (measured) | |

## Layout skeletons

**Floating note panel (one component, 4 instances tiled/overlapping on the desktop):**
- Narrow portrait card, ~180–190px render width, frameless, soft drop shadow, ~10–12px corners.
- Top-right corner: "···" overflow menu (per-note actions). No title bar / traffic lights.
- Content stack, ~16px padding, left-aligned:
  1. **Title row** — one bold ~15px black title (optionally with a trailing emoji, e.g. "Design ideas 💡").
  2. **Body block** — a *typed* content list, one of: (a) checklist = leading ink checkbox + label, ~26–28px rows; (b) bullet list = ink round bullet + label; (c) field block = "API Key" label above a masked capsule field with lock glyph, then a red-underlined "Do not share" warning.
  3. **Truncation** — "···" bottom-left when content overflows.
- Each note is a single-color paper surface; the color is the note's identity, chosen per note (yellow/pink/green/blue observed).

## Signature moves

- **[GOLDEN-NUGGET] Monochrome ink controls on colored paper.** Checkboxes are drawn as thin black-outlined squares with a black check — not the native accent-blue filled checkbox, and not a colored fill. Bullets, the truncation dots and the overflow menu are all ink too. This is systematic across every note and is the single choice that makes the surface read as *paper you write on* rather than a settings form. Native correction if this were an app-chrome list: selection/toggles should bind to the system accent — but on a deliberately-skeuomorphic note surface this monochrome house style is a defensible signature, not a defect.
- **[GOLDEN-NUGGET] The note is a structured micro-record, not a text blob.** Stickies hold free text; Noticky notes hold *typed blocks* — checklist, bullet list, and a masked-secret/lock field with a warning link. "Sticky notes with schema" is the product's whole differentiation expressed visually.
- **Color IS the note's identity.** Four saturated pastels (one saturated yellow hero + three lighter hues) let a wall of notes be located pre-attentively by color alone — Von Restorff isolation used as a filing system.
- **Chrome reduced to two "···".** One top-right (menu) and one bottom-left (more-below). The paper edge + shadow does all other framing work — minimal, but the two identical glyphs carry different meanings, a small discoverability risk.

## Defects

- **Target Starvation (soft):** the "···" menu dot-cluster and the ~16–18px ink checkboxes read below the 24px WCAG hit floor as drawn. Likely padded to a larger invisible hit region (common and fine), but unverifiable from a render — flag, don't condemn.
- **Warning contrast (minor):** the red underline under "Do not share" sits on the blue paper; red-on-blue is a marginal non-text contrast pairing and the underline can read as a spellcheck squiggle. Pairs with a label so meaning survives.
- **Not a rendering defect but worth flagging for the synthesis pass:** an *editable note* that stores a live-looking API secret and only masks it on display is mild security theater — the app's own "Do not share" copy concedes it. Product concern, not a visual one.
- **Contrast Dilution — absent (good):** black ink on light paper is high-contrast everywhere; the app does not fall into the everything-mid-gray trap.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| floating note panels (composite render) | 12/14 | #11 target starvation (small "···"/checkbox glyphs, ~16–18px, sub-24px as drawn); #14 focus appearance unevaluable (static marketing render — no focus state visible). #7 de-emphasis passes on weight only (body ink is not lightened — paper convention). |

**Native-tells audit: 8/10.** Passing: #1 lineage reads native (med conf, composite), #2 content correctly opaque / no glass abuse, #5 13pt-class compact density, #7 one action per note, #8 concentric-ish radii (checkbox < field < note). N/A: #4 no sidebar, #9 no toolbar. Deviation: #3 selection/toggle grammar — custom monochrome checkbox instead of accent-fill (logged as signature). Caveat: #10 frameless-by-design and #6 accent — the app deliberately uses no system accent (note color is the identity), so accent-binding is n/a rather than wrong.
