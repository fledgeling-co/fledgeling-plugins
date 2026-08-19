# Icon corpus aggregate

_134 icon observations aggregated from `observations/*-icon.json`._  
Icons carry no framework-lineage field, so **nativeCount = 0** and no rule here is promoted to macOS canon. Hue families are **derived** (HSV bucketing of observer hex). Style families are **candidate/recurring** keyword groupings of observer text, not canon (canon needs >=3 independent NATIVE-lineage apps).

## Era distribution

| era | n | share |
|---|---|---|
| big-sur | 61 | 46% |
| custom | 38 | 28% |
| liquid-glass | 16 | 12% |
| skeuomorphic-quote | 13 | 10% |
| flat-transition | 6 | 4% |

## Rubric score distribution

min 4 / median 11 / mean 10.32 / max 12 (n=134)

| score | n | bar |
|---|---|---|
| 4 | 1 | .............................. |
| 6 | 1 | .............................. |
| 7 | 1 | .............................. |
| 8 | 8 | ##............................ |
| 9 | 14 | ###........................... |
| 10 | 38 | #########..................... |
| 11 | 56 | #############................. |
| 12 | 15 | ###........................... |

## Failure frequency by rubric check

225 failure lines across 119/134 icons; 15 icons ship clean (no failures).

| check | failures | members |
|---|---|---|
| #10 | 102 | agentpeek, alcove, atlas, audio-notes-formerly-email-me, autoshelf, ayron-time-tracker, bartender-6, bauhaus-clock, canary-mail, claude-notch-usage-companion, cleanmymac, cleanshot-x (+90) |
| #4 | 27 | bauhaus-clock, code-meter, codex, compressor, creos, dropadoo, dynamiclake, finbar, folder-hub, foldervitrine, hilium, hipixel (+15) |
| #3 | 26 | agentpeek, alcove, bartender-6, cleanshot-x, cooldock, corner-time, creavit-studio, drivemosaic, droppy, dynamiclake, fantastical, finbar (+14) |
| #1 | 19 | autoshelf, bartender-6, claude-notch-usage-companion, compressor, creos, grape, hipixel, klack, notion-calendar, nox, pokey, raycast (+7) |
| #7 | 16 | bartender-6, bauhaus-clock, dynamiclake, fantastical, finbar, folder-hub, foldervitrine, hejour, hilium, macrest, minarah, purge (+4) |
| #6 | 9 | backdrop, compressor, dia, drivemosaic, fantastical, forma, nox, soulver, subscription-day |
| #12 | 8 | code-meter, corner-time, leafy-vocabulary-builder-for-mac, maestri, pixelcasso, raycast, screenlex, zipic |
| #9 | 6 | canary-mail, liqoria, macusb, open-timer, raycast, slapmac |
| #5 | 5 | macrest, macusb, raycast, screen-charm, tokens-4-breakfast |
| #2 | 4 | claude-notch-usage-companion, leafy-vocabulary-builder-for-mac, raycast, screenlex |
| #11 | 3 | mailtwin, supaste, zonedial |

### Soft-pass (near-miss) frequency by check

| check | soft passes |
|---|---|
| #4 | 85 |
| #2 | 76 |
| #3 | 60 |
| #1 | 47 |
| #9 | 36 |
| #5 | 33 |
| #10 | 32 |
| #8 | 31 |
| #7 | 29 |
| #11 | 20 |
| #6 | 19 |
| #12 | 11 |

## Palette

### Background field type

| type | n |
|---|---|
| ramp | 63 |
| flat | 49 |
| scene | 10 |
| glass-layers | 10 |
| none/transparent | 2 |

Accent recorded as none/monochromatic: **66/134**.

### Dominant hue families (derived, HSV bucketing of hex)

| hue family | background | glyph | accent | all |
|---|---|---|---|---|
| white/near-white | 66 | 113 | 1 | 180 |
| blue | 61 | 93 | 15 | 169 |
| grey/silver | 34 | 71 | 0 | 105 |
| indigo/violet | 34 | 59 | 9 | 102 |
| black/near-black | 49 | 36 | 0 | 85 |
| orange | 17 | 45 | 9 | 71 |
| red | 15 | 38 | 15 | 68 |
| yellow | 11 | 39 | 10 | 60 |
| cyan/teal | 5 | 23 | 5 | 33 |
| magenta/purple | 5 | 17 | 4 | 26 |
| green | 4 | 15 | 5 | 24 |
| chartreuse/lime | 6 | 13 | 1 | 20 |
| pink/rose | 2 | 12 | 2 | 16 |

## Composition

### Marginals

**background_type**: ramp 63, flat 49, scene 10, glass-layers 10, none/transparent 2

**glyph_type**: object 50, abstract 49, mascot 12, monogram 12, scene 11

**overlay_device**: none 83, other 30, frame 11, diagonal-tool 5, badge 5

### background_type x glyph_type

| background | glyph | n |
|---|---|---|
| ramp | abstract | 25 |
| ramp | object | 21 |
| flat | abstract | 19 |
| flat | object | 15 |
| scene | object | 8 |
| flat | mascot | 6 |
| flat | monogram | 6 |
| ramp | scene | 6 |
| ramp | monogram | 6 |
| ramp | mascot | 5 |
| glass-layers | abstract | 4 |
| glass-layers | object | 4 |
| flat | scene | 3 |
| none/transparent | object | 2 |
| scene | abstract | 1 |
| glass-layers | scene | 1 |
| glass-layers | mascot | 1 |
| scene | scene | 1 |

### Top background x glyph x overlay combinations

| background \| glyph \| overlay | n |
|---|---|
| ramp | abstract | none | 19 |
| flat | abstract | none | 13 |
| flat | object | none | 11 |
| ramp | object | none | 9 |
| flat | mascot | none | 6 |
| ramp | monogram | none | 6 |
| scene | object | other | 5 |
| flat | monogram | none | 4 |
| ramp | object | diagonal-tool | 4 |
| ramp | object | other | 4 |
| ramp | abstract | other | 4 |
| scene | object | none | 3 |
| flat | object | other | 3 |
| glass-layers | abstract | none | 3 |
| flat | abstract | other | 3 |
| flat | abstract | frame | 3 |
| ramp | mascot | none | 3 |
| none/transparent | object | none | 2 |
| ramp | scene | none | 2 |
| glass-layers | object | other | 2 |

## Light model distribution

| model | n |
|---|---|
| top-down soft + specular/glass | 48 |
| flat/null | 41 |
| emissive/self-lit | 23 |
| specular/glass (no explicit top-down) | 19 |
| other/unclassified | 2 |
| top-down soft | 1 |

## Device-motif keyword frequency

| motif | n |
|---|---|
| glass/refraction material | 44 |
| subject-mined literal object | 35 |
| concentric/radial motif | 30 |
| device/hardware portrait | 30 |
| monogram/letterform fusion | 26 |
| diagonal-tool overlay | 25 |
| mascot/face personification | 25 |
| emissive glow focal | 23 |
| double-read/pun glyph | 21 |
| negative-space cut | 16 |

## Adjective frequency

| adjective | n |
|---|---|
| monochrome | 19 |
| literal | 16 |
| luminous | 13 |
| austere | 12 |
| glossy | 10 |
| tactile | 9 |
| nocturnal | 7 |
| friendly | 6 |
| buoyant | 4 |
| kinetic | 4 |
| stark | 4 |
| geometric | 4 |
| utilitarian | 4 |
| glassy | 3 |
| flat | 3 |
| atmospheric | 3 |
| anonymous | 3 |
| reductive | 3 |
| cheerful | 3 |
| restrained | 3 |
| nostalgic | 3 |
| warm | 3 |
| playful | 3 |
| diagrammatic | 3 |
| characterful | 3 |
| monochromatic | 2 |
| emblematic | 2 |
| iridescent | 2 |
| spare | 2 |
| retro-arcade | 2 |
| glossy-candy | 2 |
| electric-blue | 2 |
| glossy-skeuomorphic | 2 |
| dimensional | 2 |
| assertive | 2 |
| brand-abstract | 2 |
| high-contrast | 2 |
| minimal | 2 |
| faceted | 2 |
| monochrome-green | 2 |
| optimistic | 2 |
| prismatic | 2 |
| matte | 2 |
| frosted-glass | 2 |
| metallic | 2 |
| template-default | 2 |
| brash | 2 |
| serene | 2 |
| electric | 2 |
| instrumental | 2 |
| minimalist | 2 |
| engraved | 2 |
| emissive | 2 |
| crystalline | 2 |
| monochrome-violet | 2 |
| confident | 2 |
| concentric | 1 |
| electric-cool | 1 |
| matte-silver | 1 |
| mascot-personable | 1 |
| subject-literal | 1 |
| ascendant | 1 |
| recessed | 1 |
| moody-violet | 1 |
| sunlit-amber | 1 |
| origami-tactile | 1 |
| send-kinetic | 1 |
| unshaded | 1 |
| athletic | 1 |
| loud | 1 |
| formal | 1 |
| functionalist | 1 |
| hairline-monochrome | 1 |
| hygienic | 1 |
| warm-terracotta | 1 |
| notation-witty | 1 |
| aqua-glossy | 1 |
| monochrome-blue | 1 |
| brand-forward | 1 |
| impish | 1 |
| monochrome-clay | 1 |
| magenta-committed | 1 |
| literal-appliance | 1 |
| warm-monochrome | 1 |
| literal-gauge | 1 |
| mac-literate | 1 |
| vaporous | 1 |
| electric-indigo | 1 |
| appetizing | 1 |
| tactile-translucent | 1 |
| metaphor-oblique | 1 |
| abstract | 1 |
| enigmatic | 1 |
| polished-chrome | 1 |
| off-platform-luxe | 1 |
| puffy-dimensional | 1 |
| timer-literal | 1 |
| cartographic | 1 |
| muted-polychrome | 1 |
| matte-orderly | 1 |
| muted | 1 |
| device-literal | 1 |
| backlit-glassy | 1 |
| brooding | 1 |
| engineered | 1 |
| nocturnal-glow | 1 |
| device-mimetic | 1 |
| soft-focus | 1 |
| domestic | 1 |
| interlaced | 1 |
| pearlescent | 1 |
| punny | 1 |
| aquatic | 1 |
| hardware-literal | 1 |
| warm-amber | 1 |
| underlit | 1 |
| frosted | 1 |
| airy | 1 |
| delicate | 1 |
| jewel-saturated | 1 |
| connective | 1 |
| architectural | 1 |
| monolithic | 1 |
| frosted-neutral | 1 |
| soft-embossed | 1 |
| molten | 1 |
| obsidian-lit | 1 |
| primary-triad-playful | 1 |
| dot-matrix-mechanical | 1 |
| markdown-literal | 1 |
| earnest | 1 |
| energetic | 1 |
| thermal | 1 |
| grainy | 1 |
| sunny | 1 |
| flat-confident | 1 |
| aqua-monochrome | 1 |
| radial-energetic | 1 |
| template-gradient | 1 |
| demonstrative | 1 |
| glossy-retro | 1 |
| owlish | 1 |
| hand-inked | 1 |
| signature-bold | 1 |
| warm-editorial | 1 |
| photoreal-skeuomorphic | 1 |
| monochrome-restrained | 1 |
| hand-lettered | 1 |
| acid-green | 1 |
| chunky | 1 |
| tender | 1 |
| monochrome-metallic | 1 |
| retro-skeuomorphic | 1 |
| rounded-friendly | 1 |
| chromatic | 1 |
| high-key rose | 1 |
| soft-pastel | 1 |
| gentle-domestic | 1 |
| keyline-flat | 1 |
| cinematic | 1 |
| elemental | 1 |
| convivial | 1 |
| layered | 1 |
| vivid | 1 |
| derivative | 1 |
| devotional | 1 |
| soft-3d-clay | 1 |
| literal-architectural | 1 |
| warm-earthy | 1 |
| hand-drawn-naturalistic | 1 |
| utilitarian-flat | 1 |
| editorial | 1 |
| wayfinding | 1 |
| single-hue | 1 |
| idiosyncratic | 1 |
| committed-dark | 1 |
| graphic | 1 |
| bookish | 1 |
| blocky | 1 |
| spectral | 1 |
| self-referential | 1 |
| sunlit | 1 |
| ornate | 1 |
| blueprinted | 1 |
| over-packed | 1 |
| fluid | 1 |
| flat-graphic | 1 |
| painterly | 1 |
| witty | 1 |
| gallery-dark | 1 |
| cartoon-sticker | 1 |
| plush | 1 |
| monochromatic-violet | 1 |
| chunky-monogram | 1 |
| sky-blue | 1 |
| dark-neon | 1 |
| glow-rimmed | 1 |
| wordmark-burdened | 1 |
| premium-utilitarian | 1 |
| translucent-graphite | 1 |
| backlit | 1 |
| abstract-austere | 1 |
| glossy-chrome | 1 |
| stark-monochrome | 1 |
| legacy-templated | 1 |
| dark-premium | 1 |
| woven-geometric | 1 |
| singular | 1 |
| cluttered | 1 |
| instrument-like | 1 |
| punny-literal | 1 |
| amber-warm | 1 |
| irreverent | 1 |
| cartoonish | 1 |
| graphic-bold | 1 |
| flat-brand | 1 |
| translucent | 1 |
| dashboard-literal | 1 |
| punchy | 1 |
| brand-generic | 1 |
| sculptural | 1 |
| throwback | 1 |
| notch-forward | 1 |
| warm-orange | 1 |
| precise | 1 |
| cool-luminous | 1 |
| bold | 1 |
| naturalist | 1 |
| frosted-violet | 1 |
| paired | 1 |
| stealth-monochrome | 1 |
| understated | 1 |
| vivid-azure | 1 |
| flat-wireframe | 1 |
| brisk | 1 |
| cyber-industrial | 1 |
| machined | 1 |
| monumental | 1 |
| glossy-teal | 1 |
| moody | 1 |
| conventional | 1 |
| template-premium | 1 |
| warm-luminous | 1 |
| pun-forward | 1 |
| candy-glossy | 1 |
| contrast-shy | 1 |
| mechanical | 1 |
| didactic | 1 |

## Candidate icon style families (>=2 members, keyword-signature grouping)

_Overlap is expected and recorded — icons can belong to several families. These are (candidate/recurring), promotable only with lineage evidence the icon layer lacks._

| family | n | members |
|---|---|---|
| skeuomorphic / photoreal literal-object | 40 | bartender-6, canary-mail, cleanmymac, cleanshot-x, code-meter, codeshot, compressor, cooldock, creos, deskminder, drivemosaic, droppy, fantastical, fello-ai, forma, framer, glaze, glyph, grape, hipixel, keeby, klack, letterboxx, liqoria, looq-preview-files-for-mac, open-timer, orbs, pieoneer, radial, revone, runey, subscription-day, supaste, sweeper, tono, unfold, viaduct, waterlemon, zipic, zush |
| Liquid-Glass frosted-glass-glyph/object | 31 | ajar, audio-notes-formerly-email-me, autoshelf, codex, compressor, creavit-studio, cursor, dropzone, finbar, foldervitrine, forma, gatheros, glaze, heatscope-ai-ux-attention-heatmaps, hoolo, mole, mux, notion, onlook, prostir-zvuku, purge, revone, room-service, runey, sero, sketch, slapmac, slashit-app, spacepeek, supaste, textsniper |
| mascot / character / creature | 21 | agentpeek, bartender-6, claude-notch-usage-companion, cleanshot-x, code-meter, finbar, glance, keeby, leafy-vocabulary-builder-for-mac, macusb, maestri, mole, mymind, pokey, sessionwatcher, shake-it-on, slapmac, tono, tuple, waterlemon, zush |
| Big-Sur diagonal-tool / cleaner-maintenance | 18 | 1password, agentpeek, cachesweep, cleanmymac, cleanshot-x, code-meter, creavit-studio, dropadoo, leafy-vocabulary-builder-for-mac, mac-4-breakfast, notion, orbs, screenlex, superlist, sweeper, tuple, uninstally, zipic |
| device-portrait / notch / framed-screen utility | 17 | agentpeek, alcove, claude-notch-usage-companion, codeshot, cooldock, corner-time, droppy, dynamiclake, folder-hub, gatheros, healthynotch, maestri, mjsfx, open-screen-shot, purge, tellie, vocal-notes |
| 3D-render / claymorphism (Blender/Spline) | 16 | compressor, creos, fello-ai, glaze, keeby, letterboxx, minarah, mymind, presentify, revone, room-service, shake-it-on, subscription-day, viaduct, waterlemon, zipic |
| Big-Sur single-object-on-gradient-squircle utility | 13 | audio-notes-formerly-email-me, autoshelf, glyph, mac-4-breakfast, macrest, minarah, onlook, pokey, resurf, screenlex, soulver, walltune, waterlemon |
| flat-monochrome-logomark (Vercel/Linear register) | 12 | atlas, ayron-time-tracker, compresto, coreviz-studio, cursor, hoolo, leafy-vocabulary-builder-for-mac, notion, notion-calendar, satu, slashit-app, voiceos |
| dark-field emissive-object (glow-on-black) | 10 | backdrop, dropzone, lookaway, noticky, onlook, prostir-zvuku, screen-studio, sero, usage, viaduct |
| single-glyph-on-single-hue gradient (monochromatic tint) | 9 | ajar, cachesweep, mailtwin, pokey, purge, revone, supaste, tuple, unfumble |
| AI violet->blue gradient glass-blob dev/agent | 7 | cachesweep, codex, cursor, inkline-text-editor, lookaway, mac-4-breakfast, maestri |
| flat two-tone / geometric-glyph indie utility | 6 | bauhaus-clock, caesura, mole, super-shortcuts, tokens-4-breakfast, zonedial |
| data-viz / ring-chart emblem | 6 | code-meter, drivemosaic, nox, sessionwatcher, spacepeek, subscription-day |
| spectrum-gradient organic brand-blob (Arc/Raycast/Siri-orb) | 5 | backdrop, dia, heatscope-ai-ux-attention-heatmaps, inkline-text-editor, prostir-zvuku |
| charcoal-squircle single-white-glyph (dark mono-minimal utility) | 5 | cooldock, radial, supaste, toplify, wallspace |
| scene / diorama / app-UI-as-icon | 5 | fantastical, finbar, macwall, open-screen-shot, pixelcasso |
| monogram editorial / serif-initial | 2 | hora-calendar, mural |

Icons assigned to >=1 family: **126/134**. Unassigned (idiosyncratic / thin signal): craft, hejour, hilium, obsidian, orchard, picmal, raycast, screen-charm.

## Device map (slug -> devices)

- **1password**: numeral-as-keyhole double reading (the brand '1' IS the keyhole slot); concentric vault-dial / combination-lock motif (rotational symmetry instead of a diagonal tool overlay); electric-blue-on-silver focal economy (whole saturation budget in the one focal ring)
- **agentpeek**: notch-as-mascot (the MacBook notch silhouette personified); negative-space googly eyes (pupils + pinpoint sparkles + eyebrow arcs); baked soft-shadow lift on an otherwise perfectly flat glyph
- **ajar**: wedge-as-lid-ajar (laptop side profile, lid at an angle — the literal subject); double-read glyph (same wedge = upward arrow/mountain = light rises with the lid); curved-belly base with specular keel (convex bottom + refraction rim, not a flat triangle base); monochromatic single-hue tint system (glyph is a lighter value of the field, no second hue)
- **alcove**: framed recessed glow ('alcove') — beveled near-black bezel wrapping a luminous inner panel; literal read of the app name and the Dynamic-Island/notch nook; inverted glow ramp — light rises from the bottom edge, opposite Big-Sur sky logic; wallpaper-echo palette — violet->pink field mirrors the Monterey-style desktop the app overlays
- **atlas**: six-point asterisk / spark mark (spark-of-inspiration + footnote-asterisk = reference-library metaphor); logo-on-near-black treatment (wordless brand glyph used verbatim as app icon); negative-space radial burst (arms separated by hard black wedges)
- **audio-notes-formerly-email-me**: origami send-plane (folded-paper airplane as the send metaphor); object-at-an-angle (nose up-right, motion vector); sunburst backdrop (lower-left light burst, not a top-down sky ramp); baked contact shadow (grounds the plane; era-tell fighting Liquid Glass)
- **autoshelf**: file-dropping-onto-shelf narrative (subject-literal: the app files your files); shelf-curve doubling as a friendly smile under the document; dog-eared document as the universal file/paper signifier; flat tint-as-highlight (lighter coral flags the fold without invoking a light model)
- **ayron-time-tracker**: rising-'A' double-read (letter A that also reads as an ascending diagonal / mountain-peak = 'time/productivity climbs'); acid-lime + black athletic/performance palette (hi-vis register, committed brand direction confirmed by cover site); angular italic-slanted geometric letterform, all straight cuts and hard terminals with forward lean
- **backdrop**: iridescent glass droplet (oil-slick/holographic refraction as whole identity); self-lit bloom on near-black (no top-down light); aurora vertical ramp (cool tip -> warm bulb); name-as-glyph pun: Backdrop -> a drop
- **bartender-6**: tuxedo-as-mascot: the menu-bar butler / maitre d' concept rendered as literal formalwear (subject communicates function); photoreal material contrast: glossy satin lapel sheen against matte cotton shirt; cross-stitched black buttons as focal detail with micro-shadows; lone desaturated-navy pen as the single accent in an otherwise achromatic field (accent-as-jewelry); vertical mirror symmetry about the shirt placket
- **bauhaus-clock**: Braun/Max-Bill functionalist clock face (committed product-design quotation); open-ring center hub with white core dot; hairline hands and hairline tick ring (austerity as brand); full-bleed white ground with no drawn squircle — relies on the system mask
- **cachesweep**: sparkle cluster (`sparkles` SF Symbol) size-cascaded small->medium->large along the ramp diagonal, so glyph motion echoes the light-to-dark sweep; monochrome-blue + single white mark, zero accent
- **caesura**: caesura-mark-as-glyph — the // musical/poetic pause-and-breath notation IS the app name, function, and typographic origin; slanted-not-vertical bars — leans the literary/musical caesura over the media-pause button, choosing the editorial register; rounded (capsule) stroke caps — soft exhale-like terminals rhyming with the breath/breaks content; flat two-tone economy — cream ground + one terracotta, no gradient, no second hue, no separate accent
- **canary-mail**: crescent-C-plus-twin-darts logomark (Canary bird / send motif, doubles as a C monogram); aqua-gel baked gloss with specular sweep; monochrome blue-on-white tile
- **claude-notch-usage-companion**: pixel-art mascot (Space Invaders crab-alien family); brand-colour subject-mining — creature body rendered in Claude clay to name its subject without a logo; knockout-pixel eyes as the whole face; monochrome-clay-on-black arcade framing
- **cleanmymac**: the subject IS the object (draws the Mac the app cleans, not an abstract freshness glyph); diagonal chrome maintenance tool crossing the plane (Apple TextEdit/Preview tool-at-an-angle grammar); candy-gloss magenta screen (skeuomorphic wet-glass quote inside a Big Sur composition; the MacPaw house saturation); embossed tone-on-tone C brand monogram in the stand
- **cleanshot-x**: capture-as-peel: the screenshot rendered as a physical blue sheet peeled off the screen, revealing the desktop beneath — the app's verb animated in a static mark; confetti-desktop reveal: 5 saturated dots as abstract stand-ins for a colourful Mac desktop, giving the peel something worth revealing; diagonal cyan->blue sheet ramp (sky-logic rotated to track the peel direction, not gravity); curl-underside gloss: pale #CBE6F5 back-face sheen selling the lifted material, the strongest value contrast in the mark (8.38:1 vs base)
- **code-meter**: redline quota gauge (arc ramps yellow->orange->red toward full, the fuel/tachometer redline; colour semantics ARE the product); glossy skeuomorphic dial (raised bezel, baked specular rim, environment reflections, recessed vignetted face); endpoint pip (single bright light dot marking current value at arc end); baked 'CODE METER' wordmark set into the dial face
- **codeshot**: camera-lens-as-window dual metaphor (a snapshot of a code window); macOS traffic-light triad as the sole brand accent moment; titlebar seam bisecting the body into chrome + camera; glossy skeuomorphic candy-sphere window buttons; tone-on-tone charcoal modelling of the subject
- **codex**: terminal prompt >_ knocked out of a glass cloud (cloud-compute agent + CLI, whole concept in one move); crown specular as a warm pink-lavender bloom on a cool blue-violet glass body (hue-shift sells the glass); white-field ground instead of a saturated background (inverts the usual filled-squircle convention); rounded stroke terminals on the >_ (soft friendly CLI matching the pillowy cloud)
- **compressor**: freshness-pouch metaphor (food-storage bag = compress-but-keep-quality, subject-mined); translucency window (fruit read through the front bag wall via subsurface transparency); pink zip-clip as the single saturated anchor; photoreal soft-3D product render on transparent alpha (web/App-Store authoring, no squircle)
- **compresto**: concave four-pointed 'pinch-star' — compression rendered as inward squeeze to a narrow hollow waist (subject-mined, not stock); logo-first achromatic treatment — off-white #F2F2F2 over warm-neutral near-black #171717, behaves like a brand monogram not a native utility icon; hollow negative-space waist — the dark field reads through the middle, defining the pinch by absence
- **cooldock**: dock-as-pill: one wide glossy capsule low on a dark tile abstracts the product's floating dock/widget bar; committed monochrome minimalism: near-black field + single high-key white shape, zero hue, no tool overlay; Big Sur baked gloss: charcoal ramp + top-edge specular rim + top-lit capsule micro-shadow
- **coreviz-studio**: concentric rounded-hexagon 'nut/aperture' ring (super-elliptical vertices, points to the sides); negative-space hex bore as the only focal detail; max-contrast monochrome two-tone (no gradient, no accent, ~19:1)
- **corner-time**: self-referential product depiction (the icon IS the app's on-screen output); full-bleed field (art bleeds to mask edge; whole squircle = a screen); corner-anchored clock (numerals in the top-right corner, echoing the app name)
- **craft**: quartered pinwheel mark (four rounded quarter-petals around a plus-gutter of negative space); two-bright / two-dark quadrant split (top row glows, bottom row grounds); saturated glass segments floating on a frosted field rather than an opaque gradient squircle; abstract brand mark with no subject metaphor (recognition-led, Notion/Linear register)
- **creavit-studio**: bisecting white seam splitting the dark panel and running past its ends into the field; twin charcoal side capsule rails (grips/device-buttons) in the margins; monochrome charcoal+white mark on a single saturated brand field
- **creos**: polished-chrome 3D emblem (photoreal reflective metal); mirror-floor reflection under the glyph; pure-black void field maximising chrome pop; tri-stable checkmark / C-monogram / chevron form with lightning-spike terminal
- **cursor**: dual-read cube-cursor — the bright inverted triangle reads simultaneously as the cube's near vertical edge/front facet AND as a downward-pointing cursor/pointer blade; one geometric move carries both '3D agent/environment' and 'cursor'; tonal ramp as self-lighting with zero hue — a monochrome facet ramp (#43->#55->#D9->#FFF) does all the 3D work, the opposite pole from the LLM-era violet->blue glass blob; vanishing back-faces — darkest facets (#43413D) sit ~1.5:1 against the #13120B tile so the cube's far edges melt into the ground and it reads open/floating, letting the bright blade dominate
- **deskminder**: off-axis gauge needle (Big Sur tool-at-an-angle, mined from the countdown subject); broken-ring gauge (open countdown arc, gap at top); monochrome tonal figure-ground (glyph is a lighter tint of the background hue, no accent); puffy 3D extrusion (ring + needle as rounded plastic tubes with baked bevel/AO)
- **dia**: sunset/aurora spectrum ramp poured into a brand shape (blue->red vertical temperature travel = the memorable move); scalloped-bottom gumdrop mark (abstract non-object logomark, dome top + concave wave base); glass-on-white pedestal (translucent coloured layer tinting its ground, lavender contact-halo not grey shadow)
- **drivemosaic**: the product as its own portrait (icon is a stylized render of the app's core treemap view); muted-rainbow treemap used as a semantic category legend, desaturated vs the cover's saturated version; per-cell top-down gradient giving soft embossed depth without glass/gloss/bevel; dark grout field with even ~8px gutters reading as a tiled mosaic wall
- **dropadoo**: envelope-as-canvas (subject becomes the background field, not a centred glyph); letter/card emerging from the envelope top carrying abstracted text lines; paperclip laid diagonally across the fold (Big Sur tool-at-an-angle) doubling as the literal attachment metaphor; single desaturated accent (#BDD894 pistachio) reserved for the focal attachment; ties to cover-art green
- **droppy**: notch-as-subject (literal MacBook notch cut into the top of the screen); front-on device portrait (screen-in-frame, not glyph-on-gradient); backlit glass screen (rim-light + hourglass specular making a flat field read as an emissive display)
- **dropzone**: emissive drop-target core — a crimson->peach glowing bullseye recessed in a dark bowl; literal 'zone' you drop onto and a brand-continuity callback to classic Dropzone's red drop-target mark, re-skinned in Liquid Glass; the single warm accent in a cool tile; stacked translucent glass rings/slots — frosted open hoops with specular top rims hovering above the pad, refracting the violet field; reads as drop-slots / a shelf the files fall through; metallic silver plinth tray — a Liquid-Glass base with a bright top-edge rim grounding the assembly as a physical 'device on a desk', not a floating glyph; subject-literal drop stack — glass slots (top) over glowing zone (bottom) animates the app's verb in a static mark
- **dynamiclake**: Dynamic-Island notch cutout; iPhone screen-in-bezel frame quote; bottom-up screen glow gradient
- **fantastical**: red header band over white page (wall-calendar skeuomorphic quote, the 16px anchor); scattered soft-focus multicolor event tiles (multicolor-as-subject, not a single glyph); ghosted gridlines ~2% darker than white (texture not structure)
- **fello-ai**: interwoven quaternary knot (four rings laced over-under, 4-fold rosette; on-subject metaphor for a multi-model aggregator); pearl/chrome tube material with baked roundness + crossing occlusion; monochrome-on-charcoal restraint (zero chromatic accent)
- **finbar**: Finbar double-pun: shark 'fin' + menu-rows/search-pill 'bar' — name rendered as image; waterline doubles as a selected-list-row band (one shape, two readings); the app's own search panel used as the icon's background field; rim-lit translucent glass fin with refraction-style inner gradient
- **folder-hub**: notch-as-subject (the MacBook hardware notch is the icon's anchor); the squircle IS the screen (rounded top corners + notch quote a MacBook display's top edge); drawer panel pill sliding from the notch; long single-hue amber->black vertical ramp, unusually dark for the era
- **foldervitrine**: glass vitrine (frosted squircle as a display case you look into); folder-that-previews-its-media (photo card poking out = the app's Quick Look function); single warm jewel (orange sun) in an all-cool frost; double-plane folder with content card z-sandwiched between back and flap
- **forma**: connector-wire flourish (glossy grey tube looping left coil + lower-right hook, stitching the cards like mind-map links); jewel cards on black (three translucent saturated glass tiles on a near-black stage); system-color card palette (card hues sit on Apple's system Red/Orange/Blue chips); baked floor reflection + glass translucency weave (wire visible through the blue card)
- **framer**: chrome/brushed-metal material quote (skeuomorphic metal over Big Sur front-facing grammar); monochrome brand discipline (zero hue; contrast and metal do all the work); logomark-as-glyph (the Framer F used directly, no tool overlay or added metaphor)
- **gatheros**: prismatic glass dispersion (chromatic aberration across a frosted letterform); dark full-bleed field with diagonal top-left light (inverts Big Sur light-sky ramp); bold rounded monogram with counter + side-notch (same mark as the app wordmark: logo-as-icon)
- **glance**: block-cursor eyes (vertical rounded rects that read as both eyes and code-editor block cursors); smiley-mascot brand; ghost grid (whisper notebook/table lines that vanish at small sizes); soft-plastic emboss halos; achromatic / color-free palette
- **glaze**: brand mark as molten glass marble (quatrefoil logo rendered as a volumetric fluid blob); warm/cool thermal split (emissive amber core vs refractive indigo rim inside one object); caustic sparkle dust (suspended star particles selling a live fluid sim); obsidian gallery field (near-black vignette as a lighting rig, dark-mode-native)
- **glyph**: dot-matrix / LED-display plate (skeuomorphic grille texture inset into a flat Big Sur icon); markdown asterisk as literal subject (* = emphasis syntax; three of them nod at ***bold-italic***); primary color triad reading as syntax-highlight tokens on a dark editor pane; glyphs-on-an-inset-screen framing, weight settled low like a nameplate
- **grape**: raw Apple Color Emoji grapes glyph (U+1F347) used as-is; literal name pun (app 'Grape' -> the grapes emoji); glossy skeuomorphic 3D shaded spheres; single leaf + curved stem crown
- **healthynotch**: 8-bit / pixel-art HP heart with the classic two-pixel specular sparkle (health + score fused for a gamified work-wellness app); nested 'screen' tile: dark navy inner tile framed inside a bright blue squircle plate; inverted inner glow: dark-top -> lit-bottom, opposite of Big-Sur sky logic, reading as screen bloom
- **heatscope-ai-ux-attention-heatmaps**: negative-space lightning bolt carved by the black/gradient boundary (speed x heat subject-mining); thermal attention-heatmap ramp: cool green -> hot red as literal subject; grain-over-mesh-gradient face (web-first / AI-startup idiom); full-bleed diagonal figure-ground split with no discrete framed glyph
- **hejour**: squircle-in-squircle: inner white card echoes the system mask superellipse; knockout glyph: checkmark is negative space (field bleeding through the card), same colour as the field; mono-hue-plus-white economy: one committed brand colour, zero gradient, zero depth
- **hilium**: wireless-wave concentric rings; radial aperture/spinner burst; inward cursor arrow (point-to-control)
- **hipixel**: literal before/after upscaling split; diagonal comparison-slider divider in shouting yellow; pixelation->painting fidelity gradient; Van Gogh Starry Night as the demo subject; glossy white photo-frame bezel
- **hoolo**: owl-from-negative-space (subject carried entirely by white cut-outs on black); 'oVo' monogram double-read (the doubled 'oo' of Hoolo with a central wedge); white-logo-on-black-tile (web/mobile-first idiom)
- **hora-calendar**: signature-scale hand-inked brush-script monogram breaking across all layers; flattened calendar-page quote (coral header + ruled agenda lines + grey date numeral); coral ground-glow brand-warmth halo; short soft ink drop-shadow
- **inkline-text-editor**: caret + ink-stroke pairing (calm vertical white caret beside a kinetic tilted glowing slash — a literal 'Ink + line' rebus that states the subject); emissive gradient stroke that lights its own field (glyph is a light source, not a painted shape); aurora ribbons + sparkle dust at the base (refraction-under-glass scene grounding); nocturnal glass field (near-black indigo ground inverting the Big-Sur white-field default)
- **keeby**: keycap-as-icon (the app's whole subject is one literal keycap); embossed smiley on the crown (tool becomes a friendly character); candy-gloss injection-moulded ABS plastic (blown-white specular + hard rim); visible keycap skirt selling real 3D depth (not a flat rounded square)
- **klack**: literal 3D matte-black mechanical keycap shot from a 3/4 downward camera (subject-mined: a keystroke-sound app rendered as the physical key); diegetic monogram — 'K' molded into the top face, catching the same light as the plastic, not typeset over the icon; free object silhouette on transparent that deliberately refuses the squircle; warm-neutral discipline — ivory legend #FFFBF3 not pure white, tying to the cream brand ground
- **leafy-vocabulary-builder-for-mac**: word-as-leaf wordmark (letterforms + diagonal midrib resolve into a leaf); diagonal leaf-vein stroke crossing the letters (occupies the diagonal-tool position); highlighter acid-green on pure black; full-bleed lettering with zero safe zone
- **letterboxx**: object-as-squircle: physical inbox tray container; airmail chevron border (red/blue nostalgia motif); fanned document stack implying accumulation/volume; claymorphic glossy-plastic soft-body 3D render
- **liqoria**: play button embedded in a glossy glass bubble/orb (Aqua-glass-button quotation); zero-chroma monochrome grayscale palette
- **lookaway**: closed-eyes rest-face (two upturned arcs = peaceful/sleeping eyes; literal 'look away and rest'); emissive gradient orb (self-luminous pink->peach pebble on black, no outline); warm specular rim (single bronze/gold top-edge light-catch); dark-field figure-ground (glow-on-black, not Big-Sur light-field)
- **looq-preview-files-for-mac**: monochrome chrome rainbow (spectrum motif stripped of colour, cast in polished metal); per-band tubular specular (white crest -> grey belly per arc); tenebrous silver-on-black high-contrast plate
- **mac-4-breakfast**: menu-bar device row (frosted capsule of 5 colour-coded dots under the hero object); literal charging metaphor (green fill + white lightning-bolt knockout); complementary field-vs-object contrast (violet-blue field, green object)
- **macrest**: crescent-moon + gear-badge subject pairing (sleep + control); monochrome high-key rose (whole icon one hue); bottom-lit inverted background ramp
- **macusb**: diagonal object staging (drive runs lower-left to upper-right, the 'tool at an angle' tradition); uniform dark keyline outline around the whole object (flat sticker / clip-art treatment); fully monochrome grayscale palette, no brand color
- **macwall**: rising red-sun disc as sole backlight accent; ukiyo-e / Hokusai-Fuji red-sun-behind-snow-peak quotation; cotton cloud-bank base hiding the peak/ground seam; near-invisible cool white->ice-blue field ramp
- **maestri**: terminal prompt reimagined as a winking face (> eye + smile arc + | cursor eye); three receding stacked translucent window cards ('many agents, one canvas'); graph-paper canvas ground behind the stack; literal macOS window-chrome quotation (real traffic lights + wordmark inside the icon)
- **mailtwin**: twin 4-point AI sparkles (white + violet); pink->violet diagonal brand ramp (coherent with the cover); white line-art envelope with purple stroke flap; lighter horizontal top-sheen band
- **minarah**: literal-subject depiction (icon IS a minaret — subject-mined for a prayer-times app); 3D clay/plastic Blender-style render; crescent finial as sole warm gold accent; grounded bottom-bleed composition
- **mjsfx**: oscilloscope screen — dark inset panel framed by a lighter bezel (framed-window motif applied literally to waveform editing); single-cycle sine wave with rounded stroke caps, near-full-bleed; zero-axis baseline hairline (the scope centerline); monochrome-cyan-on-near-black instrument palette; accent saturation reserved entirely for the glyph
- **mole**: negative-space anatomy — eye, claws, and haunch cut back to the field through one espresso mass (subtractive detail, single ink); digging-claw forepaw as subject-mining — the one detail that disambiguates mole from generic rodent and doubles as the product metaphor (digs through your disk); two-tone flat brand-mark (logo-as-icon) — wordmark glyph on a field, deliberately no icon dimensionality; circular-badge presentation carried brand-wide (cover logo, toolbar lozenge), inverted to white-on-dark on the cool cover
- **mural**: engraved museum-monogram serif (high-contrast Didone italic capital M with calligraphic swash left-leg); maximal-contrast achromatic field (#000 on #FFF, 21:1, no colour/gradient/material); confident scale — glyph fills ~78% of plate width, dead optical centre (510,510)
- **mux**: diverging path / fork junction (curved left branch + vertical stem-to-T-foot + diagonal up-right arrow from one junction); mismatched terminals as meaning: one outward arrowhead (switch/redirect) vs plain rounded T/foot caps (stay) — semantics carried by cap shape, not colour or badge; glass-rod extrusion with rounded line caps and top specular; left branch passes cleanly under the diagonal arrow; monochrome menu-bar template derivative (same glyph, single tint) confirmed in cover
- **mymind**: flocked/velvet matte 3D-rendered creature; single-hue orange object floating on pure white; hunched thinking-figure pose (mind-at-rest literalism)
- **noticky**: glowing note on a black stage (emissive, product-thesis: always-on-top/visible-in-the-dark); peeled top-left corner + ~11deg tilt = instant 'sticky note' read; engraved ruled lines suggesting text with zero letters; dark-field inversion of a conventionally-bright subject
- **notion**: the N-block: serif capital N on the front face of an isometric notebook-block (object-monogram hybrid = 'a block of notes'); monochrome-only identity, zero hue families, no accent in the mark; isometric/axonometric projection instead of front-facing (breaks Big Sur front-plane convention); keyline-as-depth-system: one chunky black outline does all structural work, no shading or bevel; recessed rounded-rect white label plate framing the glyph
- **notion-calendar**: stacked-cards depth without a shadow (offset + white keyline as the page gap); monochrome brand-mark-as-icon (zero saturation budget); Apple-Calendar '31' date-page quotation; maximal achromatic contrast, no accent
- **nox**: monitor-as-canvas (quotes Apple legacy Displays / System Preferences icon); diagonal spectrum bands as literal tint-preset wallpaper (subject-mining); crescent moon = the name 'Nox' (night) made visible, the sole saturated glyph
- **obsidian**: object-as-logo faceted gemstone (the obsidian crystal); low-poly gem rendered as flat linear-gradient faces (cut reads from gradient-direction seams, not texture); near-white specular catch on the upper-left facet; monochrome-violet ramp as the entire chromatic budget on a neutral-dark field
- **onlook**: emissive doorway — the subject is a hole of light, not a lit object (inverts glyph-on-field); warm bloom into dark — glow bleeds into the charcoal walls so figure and ground dissolve; lit threshold floor — orange light-spill receding in one-point perspective, the only depth cue; drenched-dark atmosphere — near-black field, single warm luminous focal, no decoration
- **open-screen-shot**: OS-in-a-box: depicts a macOS window + traffic lights + dock strip rather than an abstract mark (self-referential — a capture tool drawing the desktop it captures); corner crop-bracket frame quoting the screen-capture selection marquee (subject-mined); descending dots resolving into a down-arrow — 'long/scrolling screenshot' motion frozen in a static glyph; dual-hue sunrise ramp: blue top -> warm-orange bottom, breaking Big Sur single-hue convention
- **open-timer**: chronograph-in-a-squircle (watch case echoes the icon squircle); emissive teal timer-ring; blueprint-grid technical field; winding crown breaking the right margin; 'F' monogram on the dial
- **orbs**: glossy monochrome orb (Aqua/chrome-sphere quotation inside a Big Sur squircle); concentric-ring composition that literally diagrams the radial launcher subject; zero-hue silver-on-black hardware/pro-tool register
- **orchard**: Passbook/Wallet skeuomorph quotation (leather + barcode loyalty card); 'your apps in a wallet' — real macOS app icons tucked as pocket cards; debossed tonal Apple logo as ecosystem/authenticity stamp; centre fold-spine dividing your-Apple-apps (left) from Apple+Orchard mark (right) — the 'bridge'
- **picmal**: marbled flow field (full-bleed fluid S-curve ribbons, no glyph); single-hue tonal ramp (#1B5BFF->#CBDEFF->#F2F6FF); baked saturated-blue keyline on the squircle; full-bleed no-margin field-as-mark
- **pieoneer**: aperture-as-pie-slices double read (glyph carries the Pieoneer pun + radial pie-menu launcher metaphor); glossy skeuomorphic metal-on-black quote on a modern squircle; all-neutral monochrome identity in a colourful Dock
- **pixelcasso**: pixel-dissolve pun (classical portrait quantizing into mosaic blocks = Pixel + Picasso); full-bleed art reproduction as the icon, no glyph/chrome/tool overlay; gallery-black ground making the pale portrait glow
- **pokey**: pointer-cursor glove made flesh (Mickey-style white four-fingered hand = the app's subject); heavy comic black keyline (sticker/cartoon register); diagonal reach anchored to the bottom-right corner (kinetic gesture, not centred object); striped wrist-cuff detail
- **presentify**: presentation easel/whiteboard-on-tripod front-facing object (Keynote lectern lineage); soft-plastic claymorphic Big-Sur 3D render; monochrome-tonal single-hue composition (object = white tint of the field's violet); sky-logic vertical background ramp
- **prostir-zvuku**: emissive waveform/aurora bloom on void black; film-grain / dithered gradient (analog airbrush, volumetric backlit-smoke feel); total monochrome restraint (zero hue in a blue-branded app); figure defined by luminance, not by silhouette
- **purge**: frosted-glass letterform (translucent monogram treated as a glass slab, baked not layered); counter tick inside the P bowl (cursor-like vertical accent); arched notch cut into the base of the stem; sky-ramp brand blue (single-hue light-top->dark-bottom field)
- **radial**: segmented spinner ring (8 capsule dashes = 8 pie-menu wedges; reads as both loader and radial menu); rotational luminance fade (round-the-ring bright->dim implies motion in a static image); capsule-dash emboss (top-lit highlight + inner micro-shadow, restrained skeuomorphic pillow)
- **raycast**: neon glow rim (red light from bottom edge, bleeding up the sides); baked grey bevel frame fighting the system mask; corner-crammed pointer glyph with diagonal motion streaks; baked lowercase wordmark
- **resurf**: monogram-as-knockout (R carved out of the gem to the substrate tone); isometric gem / rounded-hexagon crystal substrate; dark-field inversion of an otherwise airy white brand; fully achromatic palette, no accent hue
- **revone**: inflated/clay 3D bars with rounded extruded tops; lavender 3D ribbon growth-arrow rising to upper-right; monochromatic indigo field with near-white subject (tonal restraint)
- **room-service**: backlit glass washer — 3D-extruded translucent ring at a slight perspective tilt; razor top-rim specular carrying the silhouette; hole = ground (aperture is exact background colour, ring reads as a portal); monochrome-on-violet-black — chroma-free graphite glass
- **runey**: running-R monogram (open bowl, striding leg — subject-echo of the name, reused as in-app sidebar logo); baked gloss dome (pre-rendered specular sheen, iOS-6-era); beveled chrome letterform (white top face, dark under-edge); pre-masked squircle envelope with baked edge rim (defect-device)
- **satu**: diagonal negative-space slice cleaving the mark (reads as a glass glint); monochrome austerity — white + charcoal, zero accent (mnmls studio signature); capsule-terminal geometry — all stroke ends fully rounded, one radius language; subtle left-lit charcoal gradient within the glyph
- **screen-charm**: woven translucent triangle knot (three overlapping rounded bars; Affinity-suite construction); two-tone cornflower->indigo ribbon gradient standing in for lighting; alpha-overlap vertices as pseudo-glass depth; self-colored mark floated on near-black indigo (premium dark-icon idiom)
- **screen-studio**: luminous record-ring on a void (self-illuminated violet torus, subject-mined record 'O'/lens aperture); monochrome-purple discipline (ground+glow+glyph all one hue at different values); emissive-over-lit (glyph emits its own light rather than reflecting a top-down source)
- **screenlex**: scanner viewfinder corner brackets (four-corner capture frame); traffic-light mini-window showing real captured text; top-down text opacity fade (privacy/redaction cue); oversized macOS cursor as the fuse binding screen to action
- **sero**: emissive aperture — glyph as its own light source, blooming into the black; conic electric-blue -> lavender iridescent sweep on the ring (Liquid-Glass specular tint on flat art); radial center vignette giving the flat ring lens/void depth; baked Big-Sur squircle + soft drop shadow + faint top rim (raster-baked container hygiene)
- **sessionwatcher**: ascending-bars-as-subject (the analytics chart the app draws IS the icon); monochrome-metal restraint (silver-on-charcoal, zero colour, reads pro/menu-bar-native); baked contact shadows + top-lit bars (Big-Sur depth move)
- **shake-it-on**: shake-pun made literal — a mouse jiggler drawn as maracas; the macOS arrow cursor pulled into the scene as a physical prop being shaken awake; rubber-duck engraving stamped on each maraca bulb (brand easter egg); flat-vector motion arcs conveying shake in a static frame; 3D clay-render object on a gradient squircle (base Big Sur idiom)
- **sketch**: amber faceted low-poly gem (the 'jewel') as the entire identity; gem-on-white — object on a minimal near-white ground, no colored background field (flat-transition tell); value-stepped facet shading (illustrated depth, gradients not glass); front-facing symmetrical cut-diamond silhouette
- **slapmac**: the comic slap (disembodied hand + radial impact starburst + motion-ticks); anthropomorphised laptop with a face; monochrome-green drench (one hue carries the whole surface)
- **slashit-app**: leading-slash monogram — cobalt '/' before the S, punning the app name (Slashit) and the text-expander trigger syntax (/); single cobalt accent on near-black ink — exactly one saturated element; high-contrast display 'S' with sheared terminals (wordmark-flavoured, not geometric)
- **soulver**: notepad page-fold header (torn/folded top sheet revealing paper beneath); multicolor 2x2 keypad as the glyph (rainbow = the multi-domain brand signal); domain-glyph storytelling: $ currency / % percent / clock time / = math spells the feature set; concentric mask-echo corner: bottom-right key's outer radius enlarged to nest in the squircle
- **spacepeek**: ring-as-lens: disk-usage donut chart doubles as the magnifier lens (the icon's whole idea in one shape); diagonal glass tool overlay (magnifier handle breaks the front plane to the corner — Preview/loupe lineage); in-product artifact quotation: ring palette directly quotes the app's own multicolour donut chart (icon shows the exact object you'll use); ghosted translucent folder (background ramp reads through it — Liquid-Glass flourish on a Big-Sur base)
- **subscription-day**: renewal-arrow fused with chart-arc (the largest donut segment ends in an arrowhead); radar/spider stat hub (spokes + 3D sphere) miniaturising the app's in-product chart; category-colour donut ring encoding subscription categories; sparkle-stars insight/analyze flourish; nocturnal charcoal ground with radial vignette
- **supaste**: single glossy capsule as the sole glyph (reductive to one element); sky-logic electric-blue ramp with an empty lower-two-thirds field; baked specular gloss on the pill (old iOS/Big-Sur gesture, not Liquid Glass); top-anchored bar readable as a clipboard-clip / top-of-list
- **super-shortcuts**: lightning-bolt-as-automation (category-default speed metaphor, Apple Shortcuts lineage); two-colour flat field (#1F9D6F + #FFFFFF, reads at 16px); baked rounded-rect favicon mask transplanted onto a Mac icon
- **superlist**: monochrome sculptural relief (figure and ground are one material); folded-paper logomark (the S as a curled list page); full-bleed field with no background/glyph split; tonal-only figure-ground carried entirely by baked self-shadow
- **sweeper**: trash-can quote (macOS Trash silhouette as container); overflowing mouth (contents spill above rim, front wall occludes their base); monochrome vessel / polychrome contents (gray bin frames discarded colourful apps + photos)
- **tellie**: the notch as protagonist (black pill pinned to the field's top edge, literalizing 'gives every Mac a notch'); live-caption transcript (centre-aligned white word-pills flanked by dim beige tracks = current word bright, upcoming words quiet); raised silver bevel frame (framed-tile motif enclosing the field); baked squircle + self-baked drop shadow in a ~10% transparent margin (pre-Tahoe delivery)
- **textsniper**: serif-T capture reticle (four serif capital Ts = T-for-Text, stems meeting as an X crosshair, crossbars as selection corner brackets); floating saturated glass lens on a pale frosted squircle slab (Liquid-Glass object-on-glass depth); cool cyan->violet diagonal ramp that doubles as the light model
- **tokens-4-breakfast**: token-in-the-coffee pun: a coin/chip that is both 'tokens for breakfast' and 'token = currency' (the app tracks AI spend) — the icon's cleverest detail is also its exact subject; coin rendered as a short cylinder (top face + side wall) so it reads as a chip, not a marshmallow/pill; single-accent flat graphic (one amber-orange does cup+saucer+handle) on a dark field that doubles as menu-bar context; orange rim as a negative-space fence around a coffee well that is nearly the background tone
- **tono**: robin bust portrait cropped to the lower/right mask edges (creature as identity, not a function glyph); sculpted matte plumage — cool-grey sheen ramp gives volume under top light with no gloss; catchlit white eye-ring as the lone specular and the small-size identification anchor; flat warm-ivory ground instead of a gradient ramp; two-tone bill (yellow upper -> deeper orange lower)
- **toplify**: burst-with-rising-arrow fusion glyph (lower rays replaced by an up-chevron = 'climbing to the top'); metallic vertical gradient on the glyph (top-down light on brushed silver); near-black background ramp instead of flat black
- **tuple**: paired translucent panes (the name made literal: tuple = pair = two shared screens); additive-translucency overlap (panes brighten where they cross, proving glass over opaque planes); single-hue violet sky-ramp (one hue, light-top->dark-bottom, no second accent)
- **unfold**: spacebar-key glyph = the app's trigger gesture (Quick Look is invoked by the spacebar, so the icon depicts the keystroke, not a preview/file/eye metaphor) — the strongest subject-mine; stealth monochrome: a black key on a near-black field, separated only by a top-lit bevel; presence built from value + light, not colour; debossed key rendered as a ⊔ well carved into a filled squircle (not a free 3D object) — the minimalist inverse of the klack/keeby photoreal-keycap family that drops the squircle for transparent; a single #FFFFFF specular top-line as the sole material cue on an otherwise matte, textureless field
- **unfumble**: sparkle-on-globe (globe=language/international, sparkle=automatic/magic) — the one identity move, but stock-symbol pairing; hue-drifting diagonal ramp (cools azure->indigo, not just value-darkens); brand-colour coherence: icon azure is the brand accent echoed in the cover tagline
- **uninstally**: diagonal broom as the Big Sur tool-at-an-angle crossing the squircle (TextEdit/Preview lineage); sparkle trail scaling large->small off the brush (the sparkle-clean motif); monochrome white glyph on a single-hue saturated violet field, no competing accent
- **usage**: etched PCB circuit-board faceplate texture; emissive turbine/aperture dial as an activity gauge (glow = load); machined bezel with functional faceplate hardware (screw, heatsink slots, vent dots, ports); violet-on-graphite emissive focal (accent-as-light-source, not accent-as-fill)
- **viaduct**: literal-monument glyph (app named Viaduct drawn as a viaduct/aqueduct arch); teal-glass extrusion with beveled top faces and a bright specular catch; dark-field spotlight (single luminous object on a near-black shelf); modeled inner-arch recess reading as a passage/tunnel
- **vocal-notes**: welded capsule waveform — EQ bars fused into one continuous ribbon via rounded negative-space notches, not discrete sticks; two isolated bookend dots flanking the ribbon (quiet start/end-of-recording markers); vertically-offset inner nubs (high-left, low-right) giving a subtle oscillation instead of a static mirror; single flat brand-azure fill, no glyph gradient
- **voiceos**: letterforms-as-primitives monogram (V = downward solid triangle, O = solid disc); matched vertical fade tying both marks into one lockup; strict monochrome on near-white, ~18:1 contrast, zero accent
- **wallspace**: AI-shine four-pointed sparkle (custom concave arms, category signifier not subject glyph); diagonal charcoal gradient (corner light, not canonical vertical sky-ramp); achromatic monochrome palette (charcoal + white, zero hue); total icon<->brand coherence (icon doubles as wordmark logo on the cover)
- **walltune**: unrolling wallpaper (rolled cream sheet peeling back to reveal a vibrant gradient field — subject-mined literalism); roll-mouth (magenta ring + dark inner hole selling the cylinder read and a focal pink pop); vibrant gradient as content, neutral-dark field as stage (UI de-emphasis logic on an icon); icon/brand palette coherence (wordmark is a mini of this icon; same ramp washes the cover)
- **waterlemon**: pun-glyph: watermelon-slice silhouette rendered in lemon-yellow (name made visual); dogfooded material: the glossy AI-3D candy render is exactly what the app produces (cover gallery = same style); object floated on flat white plate with only a contact shadow, no Big Sur sky-ramp
- **zipic**: feature-as-machine skeuomorphism (compression level as a physical LEVEL 0-10 dial/gauge); photos physically dispensing from a slot as a stacked ream; LED status light; matte soft-3D rendered-object register (Blender/C4D studio look)
- **zonedial**: round-terminal monoline clock at a stylised ~10:10-ish angle (faint — restyled system clock symbol)
- **zush**: 3D character mascot as the entire icon (glossy Pixar-render robot, not a flat glyph); glossy emerald eyes as the sole saturated focal accent, dark-rim->bright-centre iris ramp with dual speculars; radial glow vignette background (spotlight-on-mascot, not sky ramp); paneled-head construction seams as the robot cue; cool-neutral white body with purple-grey tinted shadows tying figure to the field
