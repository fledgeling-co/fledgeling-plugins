# MailTwin — profile

- **Source:** macapp.supply (meta.json + cover.png marketing composite; icon.png) · **Surfaces digested:** 1 (marketing OG cover, containing an illustrated app mock) · **Last updated:** 2026-07-19
- **One-sentence identity:** The current "AI-lavender-gradient" landing aesthetic applied to an Apple Mail plug-in — Superhuman's warmth pushed pinker, its whole personality in a violet serif-italic on the word "voice."
- **Cluster:** unassigned (not native macOS evidence — marketing/consumer-web)
- **Lineage:** web-electron (low confidence) — but this is a *marketing illustration*, not a shipping app screenshot; classify the illustration's design language only, never as native evidence
- **Era (chrome):** custom (marketing illustration; no real macOS chrome present)

> **Provenance warning — read before reusing any value here.** These images contain **no actual shipping macOS UI**. `cover.png` is a 1200×630 marketing OG composite; the "app window" on its right is explicitly stamped **ILLUSTRATED WORKFLOW** — a stylised mock, not a screenshot. MailTwin is described as living *inside* Apple Mail ("Keep Apple Mail. Choose the AI provider."), so it plausibly has **no standalone AppKit window at all**. Everything below is `source: mock` / brand evidence, feeds **zero** macOS canon, and should be re-digested if a real native surface ever appears.

## Tokens

All values `(estimated)(inferred)` from a single downscaled marketing render (~@1x). Brand/marketing tokens, not native control tokens.

| Token | Value | Provenance | Notes |
|---|---|---|---|
| brand/gradient | pink `#E86A9C` → violet `#9A62C8` → blue `#5B7BE0`, diagonal L→R | (estimated)(inferred) | the connective tissue: CTA pills, panel button, and app icon all share this warm-magenta→cool-blue sweep |
| bg/backdrop | pastel mesh: magenta bloom (L) → near-white (centre) → lavender (R) | (estimated)(inferred) | HSL saturation low, lightness high — desaturated marketing ground |
| type/headline | heavy geometric sans, ~700–800 wt, cap-height ~50–56px, lh ~1.05, tracking near 0 | (estimated)(inferred) | rounded terminals; Poppins/Gilroy-class, not SF Pro |
| type/accent-display | modern serif **italic**, violet `#8B5FBF`, matched to headline size | (estimated)(inferred) | set only on "your voice" — the one type-contrast move |
| type/wordmark | ~22px bold black | (estimated)(inferred) | "MailTwin" |
| type/eyebrow | ~12–13px tracked uppercase, grey `#8A8A90`, in an outlined capsule pill (~34px tall) | (estimated)(inferred) | "● AI FOR APPLE MAIL", violet dot |
| type/subhead | ~18–19px regular, grey `#6B6B72` | (estimated)(inferred) | ~5:1 on white |
| type/body-panel | ~15–16px regular, grey `#5C5C63`, lh ~1.5 | (estimated)(inferred) | reply card copy — web body size, NOT 13pt native |
| cta/pill | gradient capsule, ~44–52px tall, radius = h/2, white bold ~15px label | (estimated)(inferred) | trial pill + "Insert reply into Mail" both use it |
| panel/window | white card, radius ~18–20px, soft diffuse shadow | (estimated)(inferred) | illustrated, floating on the mesh |
| panel/chrome-dots | 3 grey dots ~10px, ~18px pitch | (estimated)(inferred) | **faked traffic lights** — grey, no colour, no real window |
| panel/field | white, 1px lavender border (<3:1), radius ~12px, ~56px tall | (estimated)(inferred) | keyword input "delay · apologize · propose Friday" |
| panel/chip | pill (radius ~15px, ~30px tall); tinted-blue `#E8F0FE`/blue-text and grey `#EDEDEF`/dark-text variants | (estimated)(inferred) | "Reply in my style" / "Warm" — not native selection grammar |
| panel/reply-card | grey `#F2F2F4`, radius ~14px, ~20px padding | (estimated)(inferred) | bold "Hi Sarah," + body |
| icon/squircle | Big-Sur superellipse, full-bleed brand gradient, white envelope glyph + 2 four-point sparkles | (estimated)(inferred) | flat single-plane light model — no Liquid-Glass depth/specular layers |

## Layout skeletons

**Marketing cover (1200×630 OG composite).** Two-column split. **Left column** (x≈64–600): wordmark row (icon squircle + "MailTwin") top-left → eyebrow capsule → 3-line headline → one-line subhead → gradient trial pill. Consistent shared left edge; vertical rhythm reads on an 8px family. **Right column** (x≈650–1200, cropped bleed): a single floating white "app" card, corner ~18–20px, containing top-to-bottom: grey-dot chrome strip → grey header chip ("Work inbox · Renewal timing", blue dot) → keyword field → chip row (2 pills) → grey reply card → full-width gradient primary button → "ILLUSTRATED WORKFLOW" micro-label bottom-right. The card demonstrates a 3-step value story (keywords → tone chips → generated reply → insert), i.e. demonstrate-don't-describe.

## Signature moves
- **[GOLDEN-NUGGET] The violet serif-italic on "your voice."** A single two-word swap from heavy geometric sans to a violet modern-serif italic carries the entire brand promise (your words, your tone). Von Restorff in one type decision — the one thing on the poster you remember.
- **The icon is a deliberate *twin* of Apple Mail's envelope.** Same envelope silhouette and flap-V as the system Mail icon, recolored off the blue onto the pink→violet brand gradient, with two AI sparkles top-right. Name-driven mimicry (MailTwin = a twin of Mail) that also does Jakob's-Law work: "this belongs to your Mail."
- **One gradient as connective tissue.** The same magenta→blue sweep unifies icon, trial pill, and panel CTA — cheap, effective brand cohesion across three surfaces.
- **"ILLUSTRATED WORKFLOW" candor.** An unusually honest disclaimer that the product shot is illustrative, not a screenshot. Rare and creditable; also a tell that no shippable native surface was available to photograph.

## Defects
- **Faked chrome → native-authenticity miss.** Three grey dots imitate a macOS traffic-light cluster, but they're grey/colourless and wrap a card that is not a real window. Sets a native expectation a Mail plug-in doesn't fulfil. Canon: either show the real Apple Mail window it augments, or don't imply a standalone Mac window.
- **Gradient-as-accent (non-native if transplanted).** The "accent" is a decorative pink→violet→blue gradient, not a single bound system hue. Fine for a marketing poster; a defect the moment it enters native UI, where selection/focus/primary must bind to one system accent.
- **Focal Collision (mild).** Two saturated gradient CTAs share one viewport (trial pill + "Insert reply into Mail"). Region-separated so it mostly survives, but the eye must choose.
- **Contrast Dilution (minor).** The "ILLUSTRATED WORKFLOW" label (~2:1) and the field's lavender border (<3:1) fall below the 3:1 non-text floor — decorative, but flagged.

## Rubric history
| Surface | Score | Failures |
|---|---|---|
| Marketing cover (composite; illustrated app mock) | 11/14 | #8 two gradient CTAs in one viewport (mild); #9 "ILLUSTRATED WORKFLOW" label & panel border near/below floor; #10 lavender field border <3:1; #14 no focus state assessable (n/a, static marketing) |
| Native-tells audit (panel treated as if it were the app) | 2/10 | #1 not native (web-consumer illustration); #3 chips aren't native selection grammar; #5 web density (15–16px body, 50px+ controls); #6 gradient accent not a bound system hue; #8 radii not concentric; #9/#10 faked grey traffic-light dots. Audit is largely moot — this is a marketing illustration, not a native surface. |
