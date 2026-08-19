# Icon: Zush

- **Era:** Big Sur unified (3D-render mascot sub-style) · **Rubric:** 11/12 · **Digested:** 2026-07-19
- **Source:** macapp.supply (`icon.png`, 500×500 @72dpi — a downscaled web render, not the 1024 master; small-size behaviour below is inferred by downscaling, not measured from a vector) · **Category:** Utility (AI File Renamer & Organizer)

| Dimension | Reading |
|---|---|
| Background | Radial glow ramp, indigo/blue-violet: centre `#5E4FFA` → corners `#3F30ED` (estimated). Brighter behind the head, vignetted darker at the corners — a spotlight-on-mascot field, not a top→bottom sky ramp. |
| Glyph | Mascot — a 3D-rendered white robot (head + nub side-ears + partial torso), front-facing. Body `#FDFEFE` highlight with cool purple-grey shadow modelling (`#D8D1E8` → `#AFA8C5`). Optically anchored by the head in the upper-centre; torso bleeds off the bottom edge. |
| Overlay device | None (no diagonal tool, badge, or frame). |
| Light model | Single top / upper-left key. Dual white specular highlights per eye sit upper-left; soft baked ambient occlusion in the eye sockets and under the chin; short soft contact shadow beneath the torso. Consistent across all elements. |
| Layer stack | (back→front) radial indigo glow · white robot body/head with panel seams · recessed eye sockets (AO) · green iris radial gradient · dual specular highlights · recessed dark mouth. |
| Palette economy | 2 hue families + neutral: indigo background, white (neutral) body, and one reserved saturated accent — emerald eyes `#014421` → `#04EC77`. Accent lands only on the focal element (eyes). Textbook economy. |

## Signature devices
- **3D character mascot as the entire icon** — a glossy Pixar-render robot, not a flat glyph. The icon *is* the character; this is the whole identity move (toy/character family).
- **Glossy emerald eyes as the sole focal accent** — green iris with a dark-rim→bright-centre radial ramp and two white speculars each. The only saturated colour in the frame; it carries recognition and matches the app's green wordmark (see brand coherence).
- **Radial glow vignette background** — brighter behind the head, darker at the corners, spotlighting the mascot rather than the light-top/dark-bottom sky ramp of most Big Sur backgrounds.
- **Paneled-head construction seams** — faint lines dividing the head into segments, the "robot" cue that keeps the silhouette from reading as a generic blob.
- **Cool-neutral white body** — shadows tinted purple-grey (not neutral grey), tying the white figure back to the indigo field.

## Brand coherence (cover glance)
- Cover palette confirms the icon is on-brand: the "AI File Renamer & Organizer" heading is the same indigo/violet as the background; the "Zush" wordmark is the same emerald as the eyes. Icon ↔ brand palette are tightly linked.
- Subject communication is partial: the mascot signals "friendly AI assistant," not "file renaming/organizing." The icon sells the AI-buddy metaphor, not the actual job. Legitimate for an AI utility, but note the gap for synthesis — this is an AI-mascot icon, not a subject-literal one.

## Failures
- **#10 Variant robustness (FAIL)** — a fixed raster with the contrast baked into the dark indigo background. The white body depends entirely on that dark field; strip or invert it (Liquid Glass clear/tinted/mono renders) and the mascot flattens into an unreadable white-on-light blob. No light/dark/clear/tinted adaptation. On macOS 26 this is also a HIG deviation: baked speculars, gloss, ambient occlusion, and a drop shadow are exactly the effects Apple says to leave to the system on a layered Liquid Glass icon.

## Soft passes (counted as passes, flagged for synthesis)
- **#2 Grid** — figure is bottom-weighted with the torso cut off at the edge; the head anchor sits slightly above optical centre. Reads fine but isn't textbook centring.
- **#3 Silhouette** — filled solid black it's a rounded head + two nub ears + shoulders: nameable as "a little robot/mascot," but it leans on the ears for robot-ness and on the (colourless-in-this-test) eyes for identity. Borderline, not generic-fail.
- **#4 16px squint** — survives: white figure + two green eye-dots on indigo still reads as "little robot with green eyes." Fine facial paneling, mouth, and eye speculars smear away at that size, so the read is the gestalt, not the detail.

## Rhymes with
- The **3D-mascot-on-radial-gradient AI-app idiom** — glossy Pixar-render character (friendly bot/assistant) centred on a saturated glow field. Style family: playful/toy 3D character. Rhymes with the wave of AI-assistant icons that use a rounded character + one saturated accent as the whole brand, rather than a flat glyph + tool overlay. (Hint only — synthesis owns cluster assignment.)
