# Screen Charm — profile

- **Source:** macapp.supply (`sources/screen-charm/`) · **Surfaces digested:** cover.png (marketing OG card, dark) — **no app UI in any supplied asset** · **Last updated:** 2026-07-19
- **One-sentence identity:** A Screen-Studio-class screen recorder whose only supplied evidence is a Linear/Vercel-grade dark violet marketing card — brand-confident, but the actual macOS surface is unseen.
- **Cluster:** unassigned — **brand evidence only; contributes nothing to any macOS UI cluster** (no native surface digested).
- **Lineage:** **unknown (low confidence)** — no app body, chrome, or control is visible anywhere in the supplied assets. Marketing copy ("Built for macOS", "Mac only") is positioning, not design evidence, and is not used to infer lineage. Category peers (Screen Studio, CleanShot X) are typically native SwiftUI/AppKit, but that is a prior, not a reading of this app.
- **Era (chrome):** **not determinable** — no window chrome, traffic lights, toolbar, or material present to classify Liquid-Glass vs legacy.

> **Digest honesty note.** This is Workflow A (digest a UI screenshot), but the single asset is a **1200×630 marketing composite** — the standard Open Graph / social-share aspect. It carries a logo, a headline, a subhead, one CTA pill, and a footer on a dark gradient. There is **no app window inside the composite** (covers often frame a real window; this one does not). Everything below is therefore **web/brand evidence**, marked accordingly, and is walled off from macOS canon. If the app's real surfaces arrive later, re-digest — none of the platform-fidelity questions can be answered from this card.

## Tokens

All tokens below describe the **marketing card**, not the application. `platform: web/brand`. None feed macOS canon.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| bg/gradient-deep | `#090A1C` → `#262255` (radial, brightest center-top) | (measured)(inferred) | Near-black indigo corners lifting to a muted violet-navy bloom behind the logo |
| bg/base | `#141332` reads as the mid field | (measured)(inferred) | Faint 1px grid texture overlaid (blueprint/graph motif), very low contrast |
| accent/violet-primary | `#6F5EE8` (CTA fill) | (measured)(inferred) | The single brand accent; carries the CTA and the emphasised headline words |
| accent/violet-bright | `#8688FF`–`#A388FD` | (measured)(inferred) | Lighter violet on the payoff words "look stunning" |
| logo/gradient | `#6A5AF0` (blue-violet) → `~#424A9B`/purple, specular `#DCDCF8` | (measured)(inferred) | Abstract triangular/prism mark, top-lit; brand-only |
| text/headline | `#FFFFFF`, bold grotesque, cap-height ~48px (band 64px w/ descenders) | (measured)(inferred) | Display sans, ~590–700 weight; Inter/Söhne/General-Sans-class — face not positively ID'd |
| text/accent-word | `#8E7AEB`/`#8688FF` on same size/weight as headline | (measured)(inferred) | Two-tone headline: value-prop words flip to accent |
| text/subhead | `#A4A3B1`, ~20–22px, regular | (measured)(inferred) | Two centered lines; de-emphasised gray, 7.2:1 |
| text/wordmark | `#C6C5CB`, medium weight, ~22–24px | (measured)(inferred) | "Screen Charm" beside logo |
| text/footer | `#4E4D5D` (L) / `#424055` (R), ~13–14px | (measured)(inferred) | "screencharm.com" / "macOS · 4K · One-time purchase" — 1.9–2.4:1, sub-threshold |
| cta/pill | ~325×62px, fill `#6F5EE8`, radius = height/2 (capsule), white label 4.73:1 | (measured)(inferred) | "Try for free — Mac only"; fully-rounded pill, no border, soft violet glow beneath |
| layout/axis | single centered vertical axis; footer flush to L/R margins (~40px inset) | (measured)(inferred) | Classic OG-card centered stack |

## Layout skeletons

**cover.png — marketing OG card (dark), 1200×630 (web share aspect, not an app window):**
Centered vertical stack on a radial indigo→near-black gradient with a faint graph-paper grid texture. Top: logo mark + "Screen Charm" wordmark (row ~y112–138). Hero: two-line bold display headline "Screen recordings that **look stunning.**" (y185–324), where the last two words switch to the violet accent. Subhead: two centered gray lines "Zoom effects, cursor tracking, and beautiful backgrounds / Built for macOS" (y358–412). Action: one violet capsule CTA "Try for free — Mac only" (~y461–525). Footer band: dim left/right metadata at the bottom margin. **No toolbar, sidebar, content region, or control — nothing to name in macOS vocabulary.**

## Signature moves

- **[brand] Two-tone value-prop headline.** The accent (`#8688FF`) does double duty: brand hue *and* the semantic highlight on the exact words that carry the pitch ("look stunning"). It's the card's one memorable move — though it is also a common product-marketing device, not a proprietary invention.
- **[brand] Accent monogamy.** One violet, everywhere it matters (logo → emphasis words → CTA → the glow under the pill) and nowhere else. Restrained accent budget: ≤10% of pixels, single hue. This is the one genuinely disciplined choice on the card.

## Defects

*(Assessed as a web marketing graphic — knowledge-base taxonomy + design-craft genericness gate. No macOS anti-patterns can be assessed: no macOS UI is present.)*

- **Template-default aesthetic → dark neo-grotesque + single electric accent.** This is precisely the look `frontend-aesthetic-direction.md` flags as the model's *unprompted* reflex for dev-tool/product briefs (Linear/Vercel family). For a creative-utility screen recorder it reads competent but interchangeable — swap the wordmark and it could sell any of a dozen Mac indie tools. A subject-mined direction (recording/lens/cursor-trail motifs) would differentiate; none is present.
- **Contrast Dilution (footer).** Footer metadata at 1.9:1 (right) / 2.4:1 (left) against the near-black ground — below the 3:1 non-text and 4.5:1 text floors. Intentionally recessive brand chrome, but sub-threshold; low severity on a non-interactive card.
- **No app evidence supplied.** Not a design defect of the app, but the load-bearing gap: a screen-recorder store listing with no product screenshot leaves the buyer (and this corpus) unable to see the actual tool. Recorded as the primary knowledge gap.

## Rubric history

| Surface | Score | Failures |
|---|---|---|
| cover (marketing OG card) | 9/14 applicable · **native audit N/A** | #9 footer contrast (1.9–2.4:1); #1 grid unverifiable at this render; #6/#10/#12/#13/#14 N/A (no body copy / forms / inputs / focus states). Native-tells audit **not run — no macOS surface present.** |

**Do not average this into macOS UI or native-audit canon.** It scores a web graphic, not an app.
