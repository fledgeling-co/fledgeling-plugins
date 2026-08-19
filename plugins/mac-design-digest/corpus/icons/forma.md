# Icon: Forma

- **Era:** custom (glossy glass-quote — baked, dark-ground) · **Rubric:** 10/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply submission render (`icon.png`, 427×427 — a downscaled pre-masked web render, corners already rounded; treat all measurements as `(estimated)` and fine-detail claims as soft). App: "The best native whiteboard for Mac" (useforma.app).

The subject is legible and on-brand: three translucent, saturated **cards (nodes)** stitched together by a glossy grey **connector-wire**, i.e. a mind-map's nodes-and-links — the exact metaphor the cover shows (dark cards joined by black connector strokes on a dotted canvas). The icon communicates "whiteboard / connected cards," so subject-communication passes even where the rubric doesn't.

| Dimension | Reading |
|---|---|
| Background | Vertical near-black **ramp** `#000000` (top) → `#373737` (bottom); mid `#1D1D1D`. Bottom edge is a baked reflective "floor," so it reads as a dark glossy stage rather than a flat field. |
| Glyph | **Scene** of 3 translucent glass cards + 1 connector-wire (abstract, no single hero glyph). Blue-cyan card is the optical anchor, sitting just above centre; orange card lower-left, red-magenta card lower-right — a triangular node cluster. |
| Overlay device | **Connector-wire flourish** (closest to "other," not a diagonal tool): a glossy grey tube that coils into a pretzel/loop on the left, threads *behind* the blue card, and exits as a hook/comma-tail to the lower right — the "links" of the board rendered as the hero ornament. |
| Light model | Top-down / upper-left, **glossy** — plastic-specular highlight running the length of the grey tube, glossy top-lit vertical gradients on each card, and a baked floor reflection at the lower edge. One direction, but two material idioms (Web-2.0 plastic gloss on the tube + Liquid-Glass-style translucency on the cards). Highlights + shadow + reflection are **baked in**, not system-applied (contra HIG app-icon guidance). |
| Layer stack | back → front: dark ramp ground + baked floor reflection → grey connector-wire (glossy tube with its own drop shadow) → translucent color cards weaving z-order with the wire (blue card *over* wire on left, wire *over* cards elsewhere) → white concentric wave-arcs on the blue card + edge speculars. |
| Palette economy | **Fails** — 4 hue families: grey wire + blue→cyan card `#3AA9FF→#01E8FF` + gold→orange card `#FFC901→#FF8A01` + red→magenta card `#FF3546→#FF0DCB`. No hue is reserved as accent; every element is saturated. |

## Signature devices
- **[GOLDEN-NUGGET] Connector-wire flourish.** A single glossy grey tube loops into a left coil and a lower-right hook, stitching the three cards like mind-map links. The literal subject of a whiteboard app (the *connections*) is promoted to the hero ornament — a genuinely committed, nameable move, not a template glyph-on-gradient.
- **Jewel cards on black.** Three translucent glass tiles floating on a near-black stage; the black ground is what makes the saturation sing. This is the icon's whole personality and, simultaneously, the root of both its rubric failures.
- **System-color card palette.** The three hues sit almost exactly on Apple's system chips — red top `#FF3546` ≈ system Red `#FF383C`; orange and blue-cyan likewise. The "sticky notes" are drawn in the platform's own color language, which quietly reinforces the native-whiteboard claim.
- **Baked floor reflection + glass translucency weave.** The wire is visible *through* the blue card; the lower icon edge mirrors the cards. Skeuomorphic tells (baked reflection/specular) executed in a Liquid-Glass material vocabulary.

## Failures
- **#6 Palette economy — FAIL.** Four competing hue families (grey + three saturated rainbow ramps), no reserved accent. It's a rainbow, not the ≤2-family + accent economy.
- **#10 Variant robustness — FAIL.** The composition depends entirely on the fixed black ground + three color-coded hues. A dark/clear/tinted or mono render would flatten the three cards into indistinguishable blocks and erase the color-coding; nothing survives without the black stage. Not a valid layered Icon Composer icon — it's a baked raster scene.

### Soft passes (scored pass, flagged)
- **#1 Mask** — composition respects the squircle, but the delivered asset is a *pre-masked* web render (baked rounded corners over transparency), not the square unmasked layers HIG wants; can't verify true edge behavior.
- **#2 Grid** — optically balanced triangular node cluster (left coil balances right hook, top card balances bottom pair) but no strict grid-centred hero; anchor sits slightly high.
- **#3 Silhouette** — "cards joined by a wire" reads as nodes-and-links, but it's a multi-object scene with no single dominant anchor, and the left coil is ambiguous as pure shape.
- **#4 16px squint** — the three saturated cards survive as color blocks and keep a distinct Dock presence, **but** the thin mid-grey wire and the white wave-arcs smear away below ~32px — the "connection" half of the concept (the app's actual subject) is the first thing lost at menu-bar/Spotlight size.
- **#5 Single light** — consistent top/upper-left direction, but two material idioms (plastic-gloss tube vs. translucent-glass cards) sit slightly uneasily together.
- **#8 Depth** — z-order is deliberate (wire weaves behind/in-front) and the floor reflection is coherent, though the card translucency muddies figure-ground where the wire shows through.
- **#9 Era coherence** — internally consistent "glossy glass" language, but it straddles Web-2.0 plastic gloss and Liquid-Glass translucency rather than committing to one era cleanly.

### Clean passes
- **#7 Figure-ground** — saturated cards on near-black are well past 3:1; in grayscale the cards survive as distinct tonal blocks (color-coding lost, shapes hold). Grey wire on black is the weakest link but holds.
- **#11 Personality** — strongly present: the connector-wire flourish + jewel-cards-on-black is a committed direction, not a generic glyph-on-gradient.
- **#12 No-text** — free of words, UI screenshots, and photographic elements.

## Rhymes with
- (No prior icon digests in corpus yet — hints only.) Rhymes with glossy **dark-ground multicolor** icons where saturated glass/plastic shapes float on black; Web-2.0 gloss meets Liquid-Glass translucency. Style family: creative/board & node-graph tools that render their canvas objects (tiles, sticky notes, connectors) as the icon subject, using Apple system-color chips as the content palette. A candidate anchor for a future "jewel-on-black glass-quote" icon cluster if ≥2 more appear.

## Notes for synthesis
- **Resolution caveat:** 427×427 downscaled, pre-masked render — not the 1024 master. Fine-detail rubric calls (#3, #4, arcs, tube specular) are soft; palette hexes are `(estimated)` pixel samples, not the source ramps.
- **Era call is deliberate:** classified **custom**, not liquid-glass. It *quotes* Liquid Glass's translucent-pane material but bakes in specular, drop shadow, and floor reflection (exactly what HIG says to leave to the system) and depends on a fixed dark ground — so it fails the tinted/mono-variant test that real Liquid Glass passes. Not big-sur either (Big Sur is matte/soft top-down, not this high-gloss reflective look).
- **The two failures are one decision:** saturated jewel cards on black buys maximal personality (#11) at the cost of palette economy (#6) and variant robustness (#10). Worth flagging as a recurring trade-off pattern if it shows up again.
- **Palette coherence with the app (cover):** *loose*. The cover is a bright blue-sky ground with charcoal cards (light theme); the icon inverts to a black ground with rainbow cards. Only the blue-cyan card rhymes with the brand's blue; the orange/magenta are icon-only. The icon is its own jewel object rather than a palette match to the product UI.
