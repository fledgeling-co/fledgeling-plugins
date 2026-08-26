# Graphic Concepting Reference (Diolog lead-designer approach)

Every article ships with an accompanying graphic concept: a single image lifts LinkedIn comment rate ~2x over text-only. This reference captures Diolog's lead designer's actual thinking so the concept feels on-brand and personable, not stock. Output a concept the user can hand to a designer or an image model; do not render the image yourself.

## The ideation flow (the important bit)

The designer's signature move, in their own words: start from something **personal or directly relatable to the content** (something obvious, on-theme), then push to **something more abstract** related to that, then **bring it back to the theme**. The result is related to the content but *not the most obvious* version; the theme is legible, but it feels personable rather than literal.

Run that for every concept:
1. **Obvious anchor**: the literal thing the topic is about.
2. **Abstract step**: a metaphor or adjacent idea one hop away from the anchor.
3. **Bring it home**: tie the abstract image back so the topic is still unmistakable at a glance.

Worked example (topic: AI coding agents you can finally trust with bigger changes):
- Obvious anchor: a code editor / a diff.
- Abstract step: handing over the wheel; a steering wheel, a co-pilot's hands.
- Brought home: a hand easing off a steering wheel while a calm autopilot line continues, rendered in the Diolog palette with a faint code-grid texture in the background. Reads as "trust, but supervise" without being a screenshot of code.

## Composition conventions

- **Layered depth:** lighter pastel background, a darker pastel mid-ground, and a foreground in the high-contrast brand colours.
- **Shadows do the work:** foreground elements carry shadows (large soft radius for a subtle lift; small tight radius for a sharp, graphic feel). Foreground can read as "flat 3D" (dimensional via shadow only, not rendered realism).
- **Texture:** a subtle grain on the background (and sometimes mid-ground) layers adds warmth. Keep the foreground clean.
- **Background accents:** scatter small highlight shapes: overlapping rounded squares of varied size and colour, and an abstract 4-point sparkle/star whose points connect with curved (not straight) edges.
- **Social/LinkedIn lean:** favour shades of blue and grey, and LinkedIn/social graphics may include text (a short title or the post's key phrase).

## Audience awareness

Read the topic's audience and tone first. For investors, simple legible signals work ("graph up = good"), but treat that as one example, not a default; let the content's actual tone (humorous / light / informative) drive the treatment. Match the graphic's mood to the article's mood.

## Diolog colour palette (hex)

Background / light: `#fff8f2`, `#ffffff`, `#e5e5e9`
Blues (lead for social): `#67b0ff`, `#027aff`, `#014cb1`, `#01214d`
Purples: `#8c00ff`, `#ceb6f5`
Warm accents: `#ffb379`, `#ff6795`, `#d93785`

Default LinkedIn/social treatment: pastel-blue/grey background, mid-ground in a deeper blue (`#014cb1` / `#01214d`), foreground accents in `#027aff` / `#67b0ff` with a warm pop (`#ffb379` or `#ff6795`) used sparingly.

## Output shape for the concept

Provide, after the article:
1. **Concept (one or two sentences):** the brought-home image and why it fits the stance; show the obvious→abstract→home logic in a phrase so the user can see the thinking.
2. **Image-model prompt:** a ready-to-paste prompt describing subject, the layered/pastel/shadow/grain composition, the specific Diolog hex colours to use, mood, and "no logos, no literal screenshots, abstract and metaphorical". Include "16:9 for a blog header" or "square (1:1) or 1.91:1 for a LinkedIn feed image" as appropriate to the chosen format.
3. **Alt text:** one plain sentence describing the image for accessibility (LinkedIn supports alt text and it aids reach).
