# Looks: six media written as numbers

Read this when the subject has no strong look of its own, when a storyline needs a material, or when a first render reads as plain. A look holds together when it is the rules of one medium (`direction.md` §5), so each entry gives its parts with numbers, where it was measured, and how it fails. The subject's own material and signature device (`direction.md` §2) come first; a look from this file dresses them and never replaces them. Borrow the medium, never another brand's trade dress (`reference-films.md` §3).

Sources are in `evidence.md` §9.

## 1. Brand motif ground

Measured from 21 films that motionflare.ai made from product websites (2026-11-24): 15 s vertical or 30 s landscape, 20 of the 21 at 60 fps, all 21 with sound, a median of 2 hard cuts a film.

- The brand's own signature graphic, animated full-bleed behind everything: Stripe's gradient ribbon, Raycast's diagonal red light bars, Cal.com's grid of keycap tiles, Midjourney's wall of `/imagine` prompts that resolves into its wordmark.
- The headline sits flush left in 2-3 lines at about 6-9 % of frame height, with the product panel or a device beside it at 45-60 % of the frame width. The layout persists while its content swaps, one feature every 3-5 s, inside one continuous take.
- Each chapter may tint the ground (Notion gives four features mint, blue, peach and pink), or the film flips once to the brand's second colour (Stripe to navy, Cal.com to purple).
- Real figures from the site land as a row of three (Stripe: "135+", "$1.9T", "99.999%") or as one large number over a logo marquee (Notion: "98% of the Forbes Cloud 100").
- The end card is the mark, one line, the product's own primary and secondary buttons and the URL beneath them, held about 3 s.
- It fails where the product panel is shown whole: its interface text was under the 2.6 % floor in most of these films. Zoom per `saas-films.md` §5.

## 2. Fine-art backdrop

Measured from getcaruso.com (2026-11-24): two homepage films and 15 animated interface loops on its investor-relations and private-equity pages.

- A painting or photograph of architecture or landscape (a colonnade, a flight of steps, a coast) fills the frame behind white interface cards with a soft lift shadow. The art is the world; the interface sits in it.
- A serif display face for headlines, a neutral sans in the interface, one muted accent (lavender) on primary buttons and on one key word per line.
- Status chips carry the only other colour: green for passed or verified, amber for flagged.
- Simplified cards: real words only where the story is, grey skeleton bars everywhere else (`formats.md` §7).
- Motion is calm: one action at a time, a cursor at reading speed, about 1 s between steps.
- It fails by standing still: the two homepage films hold one frame for 7.0 s and 4.5 s and are still for 74-78 % of their runtime. During every hold, push the camera 3-5 % or drift the backdrop in slow parallax.

## 3. Product glass

From the prompts behind two films on prompt-motion.com (an image-model launch and the gallery's most-liked launch film, 2026).

- Controls (a prompt bar, a slider panel, a caption pill) are liquid glass over real imagery: the scene behind blurred about 14 px for the body, a 12 px band along the edge showing that scene magnified about 1.06x, then a top sheen, a bright rim and a soft lift shadow. For chromatic edges, displace the cloned scene with an SVG `feDisplacementMap` at three slightly different scales.
- Glass disappears on a plain white ground, so put a slow pastel aura in the brand colours, or a blurred wash of the photograph, behind it.
- White ground, one typeface, black ink, real photographs; the one emphasised word types in a gradient of the brand colours.
- The camera drifts from 1.0 to 1.04 across each scene, and the next scene starts at the zoom where the last one ended.
- It fails as a text selection when a highlight box sits behind a word, and as a pop when a fade is shorter than 0.3 s.

## 4. Interface in space

From motlab's `gl3d.js` panels (staryone/motlab, 2026).

- Screens and cards are flat panels in a perspective scene: a field of view of 34-38° with the camera about 1,600 units away, so one unit is about one pixel at 1080p. Panel pictures are drawn at twice their size so they hold up close.
- Shallow depth of field keeps the panel in focus sharp and the rest soft; fog fades far panels into the ground colour; an optional glossy floor reflects the panels faintly; a diagonal sheen band slides across glass panels.
- One camera for the whole film, moving one way, with its distance eased in log space so a push feels even from far to near.
- One soft light, a gentle glow behind the hero, and one light sweep across the final mark.
- It fails when a text panel swaps draw order with the card behind it as the camera moves (give text a depth bias), and when a screenshot blurs at close range (redraw anything the camera nears as vector).

## 5. Graphite stage

From motion-educator's house look (zeative/motion-educator, 2026) and its 13 sample films.

- A dark graphite ground that is never empty: one slow field of flowing light behind everything, a key light with a soft streak, fine film grain that changes every frame, highlights blooming into their surroundings.
- Glass panels lit from above (a bright top edge, an accent-tinted bottom edge, a long soft shadow); a sheen passes once across a headline after it lands.
- One accent taken from the subject (sky blue for the sky, amber for electricity), and the stage light changes colour act by act to tell the story. Glow belongs only to things that are light in the story: a beam, a screen, a sun.
- Two or three depths: a blurred far layer, the subject, a near detail.
- It fails as the banned dark void (`direction.md` §5) the moment the light field stops moving or the subject stops filling the frame.

## 6. Monochrome editorial

From Caruso's 112 s agent film and Harvey's films (`saas-films.md` §12).

- A near-white ground, black type, and a serif chapter word typed with a caret before each section ("Compliance", "Finance").
- One product surface (a chat composer, a card) large in the frame, with everything else removed.
- The agent's work shows as a checklist ticking line by line, ending on "Done." with a green check.
- Colour appears only as status (green done, amber flagged) and as the brand accent on one word.
- It fails as a slideshow when nothing moves between steps; pair every hold with a push or the next row arriving.

## Checking a look

After the first render, compare one still per scene with the look's reference frame on six measures: ground colour, ink colour, palette, lightness, colourfulness, and how much of the frame is line and grain (motion-educator's `lookmatch` measures these six). Name each drift in REVIEW.md and fix it before polishing anything else.
