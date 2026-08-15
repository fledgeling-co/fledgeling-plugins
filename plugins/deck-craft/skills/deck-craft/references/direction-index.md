# Visual direction index — 34 style systems

Direction *evidence*, not a menu. These are complete looks (palette + type + accent + layout
signature); the 200 entries in `template-catalogue.md` are compositions. Different axis — pick a
direction here, then compose with templates there.

**Read progressively.** This table is the whole index; it is enough to shortlist. Only after the
user picks a direction do you read that one system's full `design.md` at
`~/Dev/frontend-slides/bold-template-pack/templates/<slug>/design.md`. Never bulk-read them, and
never read `template.html` unless the chosen `design.md` is missing an implementation detail.
For title-slide previews, `preview.md` per shortlisted candidate is the lightweight card.

Shortlist on **formality** and **scheme** first — they eliminate most of the table — then mood.

| slug | look | mood | formality | density | scheme |
|---|---|---|---|---|---|
| `8-bit-orbit` | Pixel-art neon arcade aesthetic on a deep navy void | retro-tech/playful/cyberpunk | low | medium | dark |
| `biennale-yellow` | Solar yellow on warm parchment with deep indigo serif and atmospheric sun-glow gradients | editorial/atmospheric/warm | high | medium | light |
| `block-frame` | Neobrutalist deck with pastel-neon color blocks and chunky black borders | bold/playful/graphic | medium-low | high | light |
| `blue-professional` | Cream paper background with electric cobalt blue accents; clean modern professional | professional/modern/calm | medium-high | medium | light |
| `bold-poster` | Editorial poster aesthetic with massive Shrikhand display and a single fire-engine red accent | bold/editorial/loud | medium | low | light |
| `broadside` | Dark editorial canvas with a single fire orange accent and bilingual Latin/Chinese type stack | editorial/dramatic/loud | medium-high | medium | dark |
| `capsule` | Modular pill-shaped cards on warm bone with a full pastel-pop palette | playful/modern/warm | medium-low | medium | light |
| `cartesian` | Quiet warm-neutral palette with classical Playfair serifs; tasteful and unhurried | quiet/considered/elegant | high | low | light |
| `cobalt-grid` | Electric cobalt serifs on a graph-paper canvas, anchored by stair-stepped pixel-glitch decorations and slim hairline rules | editorial/design-research/studious | high | medium | light |
| `coral` | Cream and coral on near-black, set in oversized Bebas Neue | bold/warm/modern | medium | medium | mixed |
| `creative-mode` | Cream paper canvas with confident multi-color (green, pink, orange, yellow) accents and Archivo Black display | creative/confident/playful | medium | medium-high | light |
| `daisy-days` | Cheerful pastel deck with hand-drawn daisies, stars, and rainbows. Friendly, soft, and warm | cheerful/playful/warm | low | medium | light |
| `editorial-forest` | Forest green, dusty pink, and warm cream meet Source Serif 4 in a quiet, intentional quarterly-review deck | editorial/quiet/considered | medium | medium | mixed |
| `editorial-tri-tone` | Three-color editorial system: dusty pink, mustard cream, and deep burgundy, set in Bricolage + Instrument Serif | editorial/warm/intentional | medium-high | medium | mixed |
| `emerald-editorial` | A magazine-cover business deck: emerald + navy + paper, double-rule masthead ornaments, and a bold Bodoni-style display serif | editorial/considered/confident | medium-high | medium | mixed |
| `grove` | Forest-green canvas with cream type, classical Playfair serifs, and a single rust accent | organic/considered/warm | medium-high | medium | mixed |
| `long-table` | Warm cream and rust-red supper-club aesthetic with bold uppercase grotesk headlines, Fraunces serifs, and pill-shaped outlined buttons | warm/intimate/modern | medium | medium | light |
| `mat` | Dark sage canvas with bone paper and burnt-orange accent; mid-century modern with wood undertones | warm-modern/considered/tactile | medium | medium | mixed |
| `monochrome` | Ivory ledger paper with all-black type; Lora serif headlines, Jost body, no color at all | restrained/literary/archival | high | high | light |
| `neo-grid-bold` | Editorial neo-brutalism with a single neon yellow accent on off-white paper | confident/punchy/editorial | medium | high | light |
| `peoples-platform` | Activist poster energy: blue, orange, red on cream, with Alfa Slab + Caveat Brush | activist/loud/graphic | medium-low | medium-high | light |
| `pin-and-paper` | Yellow paper with safety-pin illustrations, ink-blue handwritten Caveat, paper-grain texture | crafted/handmade/warm | medium | medium | light |
| `pink-script` | Black canvas, hot pink accent, pearl-cream paper, Instrument Serif headlines: late-night editorial luxury | nocturnal/moody/intentional | medium-high | low | dark |
| `playful` | Sun-warm peach background with Syne display: a friendly indie launch deck | warm/approachable/indie | low | medium | light |
| `raw-grid` | Neo-brutalist deck with thick borders, offset shadows, and a pink/sage/ink palette | raw/punchy/energetic | medium-low | high | light |
| `retro-windows` | Windows 95 chrome: gray title bars, MS Sans Serif, pixel typography, full nostalgia | nostalgic/retro/geeky | low | medium | light |
| `retro-zine` | Beige paper with green accent and Bebas Neue + Caveat: a riso-printed zine in HTML form | crafted/lo-fi/underground | medium-low | medium | light |
| `sakura-chroma` | Vintage Japanese cassette-package aesthetic: cream paper, diagonal rainbow ribbons, condensed bold type, JIS-style spec checkboxes | retro/playful/kawaii-tech | low | medium | light |
| `scatterbrain` | Post-it inspired: pastel sticky notes, Caveat handwriting, Shrikhand and Zilla Slab type stack | playful/creative/warm | low | high | light |
| `signal` | Deep navy canvas with bone paper and a single muted-gold accent; institutional with quiet weight | institutional/trustworthy/considered | high | high | mixed |
| `soft-editorial` | Cormorant Garamond serif on warm paper with sage, blush, and lemon accents | literary/elegant/quiet | high | low | light |
| `stencil-tablet` | Bone paper with stencil-cut headlines and a six-color earth palette: archaeology meets brand | archival/earthy/tactile | medium-high | medium | light |
| `studio` | Black canvas with electric-yellow type; high-voltage design studio aesthetic | electric/bold/graphic | medium | medium | dark |
| `vellum` | Deep navy canvas with warm-yellow Cormorant serifs and a single dusty teal accent. A quiet, scholarly aesthetic | scholarly/literary/considered | high | low | dark |

## Choosing

- **Board, regulatory, healthcare, investor:** high formality, calm scheme. The restrained option
  should be genuinely restrained; the bolder one authoritative rather than decorative.
- **Editorial, campaign, launch, internal culture:** lower formality earns its keep. Pick one strong
  system and commit to it rather than blending two.
- **Never mix two systems in one deck.** Each is a complete grammar; half of one against half of
  another reads as a deck that changed its mind.

Two further libraries on this machine, same progressive rule:

- `~/Dev/open-design/design-templates/html-ppt-*/` — 30+ named systems with a baked `example.html`
  each, plus `kami-deck`, `simple-deck`, `replit-deck`, `open-design-landing-deck`. Skim 2–3 that
  match the brief's formality.
- `~/Dev/open-design/design-systems/<slug>/` — 150+ portable brand systems (`DESIGN.md` +
  `tokens.css`). When the brief names or evokes a brand, read that system and treat it as binding.

When a real `DESIGN.md` or token file exists for the actual company, it outranks everything here.
These are for the greenfield case. See `visual-craft.md` §1.
