# Icon: ScreenLex

- **Era:** **Custom flat web mark** (transparent-background, multi-object flat illustration — **not** any native macOS icon era; no squircle field, no top-down baked lighting, no Liquid Glass layers). Borrows flat-transition-style free silhouettes but ignores the macOS full-bleed system entirely. · **Rubric:** 6/12 (6 failures — incl. non-negotiables #1/#2/#4 — 4 soft passes) · **Digested:** 2026-07-19
- **Source:** macapp.supply. `icon.png` is actually a **128×128 ICO with a transparent background** (favicon-grade web render, not the 1024 master). Text/edges are already degraded at native size; all hex sampled from a 4× upscale, so `(estimated)`. The composition is fully legible here (unlike glyph-only cutouts) because the whole scene ships in the file.

| Dimension | Reading |
|---|---|
| Background | **Transparent — no field.** No squircle base tile, no ramp, no scene backdrop. Objects float directly on alpha. This is the single most non-native choice: a macOS icon is a full-bleed square the system masks; this is a cut-out web mark (estimated) |
| Glyph | **Multi-object scene** (3+ anchors): (1) four **scanner/viewfinder corner brackets** in charcoal `#303030`, thick rounded strokes, one per canvas corner — the "capture frame" affordance; (2) a centred **mini window card**, faint vertical gradient `#DFF4FF` (top) → `#A9BBC6` (muted blue-grey mid), rounded corners, carrying three **traffic-light dots** (red `#FF736A`, amber `#FEBC2E`, green `#16C02E`) and three lines of **real legible text** ("AI drives / efficie[ncy] / Human…") fading top→bottom from charcoal `#242627` to faded blue `#B4CEDD`; (3) an **oversized macOS pointer** — black `#303030` fill, white `#FFFFFF` outline — overlapping the card's lower-right and the green dot. No single dominant anchor; the frame and the cursor both compete (estimated) |
| Overlay device | **Cursor-over-frame** — the pointer is laid across the window card and one bracket as the compositing device that fuses "screen" + "action." Not a diagonal tool in the TextEdit/Preview sense; a literal UI cursor |
| Light model | **Flat — no directional lighting.** No cast shadows, no specular, no bevel. The only tonal cue is the card's faint top-lighter gradient. Consistent by absence of lighting rather than by a committed light source (estimated) |
| Layer stack | scanner corner brackets (back) → window card (gradient fill) → traffic-light dots + fading text lines → oversized cursor arrow (front) |
| Palette economy | **Exceeds ≤2 hue families.** Neutral charcoal (brackets + cursor) + blue (card) + a saturated **traffic-light triad** (red/amber/green). The triad reads as borrowed macOS chrome rather than free accent, so it's forgivable as one semantic unit — but no accent is *reserved* for a single focal element; red/amber/green all sit at full saturation. Brand blue coheres with the cover (estimated) |

## Signature devices
- **Scanner viewfinder corner brackets** — the four-corner capture frame (à la iOS screenshot / `dot.viewfinder`) is the icon's clearest device and its most native-feeling gesture: it says "screen capture" in one shape. `[GOLDEN-NUGGET]`
- **Traffic-light window showing *real* captured text** — the card isn't an abstract "window" glyph; it renders actual words with a top→bottom **opacity fade**, which doubles as the app's privacy/redaction cue (content dissolving = "focuses on privacy"). Subject-mining taken literally: screenshot + OCR/text ("Lex") + redaction, all three in one card.
- **Oversized cursor as the fuse** — a big macOS pointer overlapping the frame binds "screen" to "action/capture." It's also the second-highest-contrast object, which is why it fights the brackets for the eye.

## Failures
- **#1 mask discipline** — transparent background, no squircle field; corner brackets sit ~10px from the canvas edge (at 128) where a true-scale system squircle mask would clip them. Artwork is not designed for the mask at all.
- **#2 grid adherence** — no safe-zone margin (art runs to the content bbox edge, x10–119 / y10–120); the cursor pulls visual weight hard to the bottom-right, breaking the otherwise-symmetric frame's optical centre.
- **#4 16px squint test** — three text lines + three dots + a white-outlined cursor smear to mush at menu-bar/Spotlight size; text is already borderline at 128. Only the vague "framed thing with a cursor" survives; all detail is lost.
- **#7 figure-ground** — with no background field, contrast rides on the wallpaper: the pale blue card and faded lower text lines (`#B4CEDD` on `#C4E9FF` card is near-zero contrast *by design*) drop well below 3:1 on light desktops; only the charcoal brackets/cursor hold.
- **#10 variant robustness** — not a layered/appearance-aware construction. The reading depends on charcoal-on-light; a macOS 26 Dark/Clear/Tinted render would swallow the charcoal frame and cursor and there are no Icon Composer variants to fall back on.
- **#12 no-text check** — legible words are baked into the card ("AI drives / efficie… / Human…"). Even read charitably as "captured text," the rubric treats words in an icon as a defect, and here they're a load-bearing element that vanishes at any real Dock size.

## Soft passes (borderline — scored pass, flagged for synthesis)
- **#3 silhouette test** — filled solid black it becomes frame-brackets + card block + cursor (dots and text vanish). The *concept* "cursor over a framed window = screen capture" is nameable, but there's no single clean anchor — it's a cluster, not a mark.
- **#5 single light model** — passes only because the icon is wholly flat; there's no lighting to be inconsistent. Trivially coherent, but it also means zero native depth model.
- **#6 palette economy** — passes as "charcoal + blue + traffic-light triad," the triad being a recognised convention rather than three free accents; strictly it exceeds ≤2 hue families and reserves no accent for a focal detail.
- **#9 era coherence** — internally consistent flat vocabulary (flat brackets, flat card, flat cursor), so it doesn't *mix* eras — but it commits to no macOS era language at all.

## Rhymes with
- *(hint only)* Flat **web/SaaS + browser-extension utility marks** — multi-object explanatory glyphs built from a viewfinder/frame + a mini-window + a cursor, floated on transparency. The "diagrammatic productivity utility" family, **not** the Big-Sur single-object-on-gradient family (agentpeek, 1password) nor the diagonal-tool (TextEdit/Preview) family. Its nearest corpus cousins are other transparent-background non-native marks that lag or skip the macOS icon system. Confirm against future digests before clustering.

## Provenance / caveats
- All hex `(estimated)` from a 128px ICO upscaled 4×; `(inferred)` — single icon, single source. No 1024 master, no dark/tinted variant shown.
- **Mask observation:** transparent background + art to the corners means either the app genuinely ships a non-full-bleed (non-native) icon, or macapp.supply saved a favicon/web render instead of the tile. Either way, nothing here is designed for the macOS squircle.
- **Brand-coherence with `cover.png`:** strong and deliberate. The cover reuses the *exact* icon scene (brackets + traffic-light card + cursor) beside a **serif wordmark "ScreenLex"**, floated over a **Big-Sur-blue gradient** (`~#4AA3F0`→`#9CD0FA` sky) that matches a stock macOS wallpaper. The icon's blue card is that same brand blue pulled into the mark; the cover also demos the actual product (a screenshot-annotation toolbar over a redacted-text panel), confirming the subject: **screenshot capture + OCR/translate + smart redaction**. The icon communicates its subject honestly — arguably *too* honestly, cramming capture + text + cursor + chrome into one 128px square.
- **Era-lag note for synthesis:** another shipping third-party utility that skips the current macOS icon language — but where agentpeek/1password ship *flat Big-Sur* marks, ScreenLex ships a *transparent web-illustration* mark with no field at all, a step further from native. Evidence for a "non-native transparent web-mark" sub-family distinct from the Big-Sur-lag group.
