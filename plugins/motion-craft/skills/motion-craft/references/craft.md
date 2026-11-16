# Motion craft: the numbers

Defaults measured from shipped films. A reference the user gave, or a moment that does otherwise on purpose and says so in `SPEC.md`, wins for its own beat. Sources: HyperFrames `motion.md` (measured frame by frame from its launch films), claude-motion `motion-design` (every number from one shipped piece), huashu-art-motion's camera rules, and the twelve tips of cDb-wPq0Iyk.

## 1. Eases by role

| Role | Curve | Notes |
|---|---|---|
| Arrival, reveal | `expo.out`, `power4.out`, or `cubic-bezier(0.16, 1, 0.3, 1)` | lands on a long tail; landing takes longer than leaving |
| Move between two states, camera, colour flood | `power2.inOut` or `cubic-bezier(0.65, 0, 0.35, 1)` | eases both ways |
| Exit, zoom through | `power3.in` or `cubic-bezier(0.6, 0, 0.9, 0.35)` | accelerates away; one smooth motion, never slide, stop, then leave |
| A value that lands | `cubic-bezier(0.55, 0, 0.2, 1.12)` | a slight overshoot on a slider or a bar reaching its level |
| Continuous motion | linear | only rotation, progress, drift, grain, a ticking hand |

The same `power2.out` at 0.5 s on everything is the flat default that makes a film feel generated. Entrances that are too snappy read as glitches; slowing the whole film by about a second often fixes it.

## 2. Springs

Name springs by damping ratio: 1.0 never bounces, 0.7-0.85 reads premium, 0.4-0.6 playful, under 0.3 a cartoon. Position and size may bounce; opacity and colour never do. Use springs for things that feel physical (UI panels, objects, badges) and bezier tweens for type and camera. One elastic accent per film at most, for the hero moment. Write springs in closed form as a function of time so any frame renders on its own.

## 3. Timing

- **Exits** are 40-50 % shorter than their entrances (claude-motion: exits 0.35-0.55 s against entrances 0.7-1.25 s).
- **Overlap**: the next element starts when the previous is 30-50 % done. Fully sequential looks robotic; all at once looks cheap.
- **Stagger**: letters one frame apart, words 60-120 ms, list items 40-80 ms (chips and cards up to 0.2-0.25 s).
- **Typing**: about 35 ms a character; an idle caret blinks at about 2.4 Hz.
- **Holds**: a line the viewer must read holds 0.5 s plus 0.3 s a word after it settles; the film's last line holds at least 2 s; a one- or two-word chapter line may hold 0.4 s. The commonest user note on generated films is "you barely read that before it goes" (hbPvZvpu9KU).
- **Pause before the payoff**: hold 0.3-0.75 s before it; the payoff plays at normal speed.
- **Rhythm inside shots**: montages cut every 0.13-0.8 s; a demo holds one framing for 7-10 s while the UI acts; shots average 1.8-3 s with motion inside them.
- **Beat grid**: frames per beat = fps × 60 / BPM. Compute each beat from its index and round it; never add a rounded beat repeatedly (at 128 BPM and 30 fps that drifts 2 frames in 32 beats). Cut on the beat; change the layout on the bar.

## 4. Type

- **Size**: titles 4-9 % of frame height, one or two lines; quiet lines 2.5-4 % against hero words that fill 60-90 % of the width. Text meant to be read is never under 2.6 % of the short side (28 px on a 1080 canvas). Too many words means cutting words, never shrinking type.
- **Phone test**: the key line still reads when the frame is shown 360 px wide.
- **Entrances, varied within one film** rather than a fade and slide-up for each:
  - per word: blur 6 px → 0 and opacity 0 → 1 in 0.13 s, words 67 ms apart, no translate;
  - per word: grey to ink, 70-100 ms apart, no position change;
  - per word sliding up out of a mask one after another, no bounce (cDb-wPq0Iyk calls this the current premium style);
  - the whole line blurring in, 8 px → 0 in 0.13-0.2 s;
  - per letter for a name, 0.1 s apart, opacity 0.3 → 1 with a slight blur;
  - one word of a sentence rolling through options like a slot machine, about 0.1 s a roll.
- **A landed title is dead still.** The motion moves on to the next element, the camera or the world behind it. Exit with a 0.13-0.25 s blur-out and fade, word by word, or with the scene's own move.
- One highlighted word in the accent colour, carrying the point.
- Real typefaces from the brand or from `assets/fonts/`, declared with `@font-face`; a fallback system font in a hold is a craft failure the eye catches at once.

## 5. Composition and the camera

- **One focal point per frame.** If two things compete, one of them waits.
- **The hero fills at least 40 % of the frame's height or width.** A small object in the middle of an empty frame is never a shot: push in, crop, or give it a world.
- **The whole canvas works.** No region larger than about a quarter of the frame stays empty or unchanged for the whole film. In a vertical clip the stage is the full 1080×1420 safe band; a chart in the top half over a flat colour block for fifteen seconds wastes half the screen, and blind judges marked it down (`evidence.md` §6).
- **Keep the eye's landing point steady across cuts.** cDb-wPq0Iyk: keep "whatever is happening" where the eye already is so it never has to hunt. That is about the focal point carrying across a cut, not about centring every layout; centring everything is on the banned list.
- **Safe area**: content inside the 90 % action-safe box, captions and key text inside 80 % title-safe; for vertical clips leave the bottom 20 % and right 12 % clear of platform UI.
- **Camera is punctuation** (huashu-art-motion): hold still when the picture moves on its own or the viewer is reading; use a slow push to lead the eye to the next detail, a lateral move to travel between things, a pull-out to show the whole and close a section; save fast pushes, slams and whips for accents (a reveal, a key number, a turn) you could count on one hand. After pushing in, come back out or cut to another scale; never three pushes in a row. A 102-second explainer that pushed in about 48 times was described by its author as "too many zoom-ins, too fast, not smooth at all".
- **One hero move per shot.** Secondary moves travel 50-70 % as far, start 100-200 ms after it, and everything else holds still.
- **Something always moves**, but meaningful motion: the product's UI working, footage playing, a character acting, a world turning, a background stage orbiting 3-5° a second. Breathing, floating or pulsing loops standing in for motion on titles and UI read as generated.
- **Depth on a 2D stage**: a shallow depth of field (background blur behind the subject) reads as a real camera (cDb-wPq0Iyk tip 7). In 3D, one key light source; light from everywhere looks flat and fake (tip 11).

## 6. Transitions with a cause

Use 3-5 kinds of transition in a film, each caused by something on screen. Hard cuts belong inside a scene (punch-ins); at most a third of the seams between beats are hard cuts, and worlds never cross-dissolve into each other. Before a seam, ask "how does this shape become that shape?" and answer it in the continuity chain.

| Transition | How it is built |
|---|---|
| Zoom through a button | camera tracks to the button with blur (0.6 s), then the button scales from about 8 % to 250 % of the frame in 0.35 s on a strong ease-in; its fill becomes the next frame |
| Object becomes the world | a pill or card grows past the frame in 0.65 s ease-in-out, its radius shrinking; what was around it blurs about 15 px and fades in 0.3 s; the new content fades in while it still grows |
| Morph | one container widens into the next (icon card → prompt box, about 110 → 880 px in 0.2 s `power3.out`) with a horizontal blur 12 → 0 |
| Carry across | the result shrinks 1 → 0.6 with blur peaking at 6 px mid-move and lands inside the next screen as it builds around it |
| Colour flood | the hero object stays while the ground changes colour in about 0.4 s `power2.inOut` |
| Whip | a horizontal or vertical smear of 0.13-0.3 s; the arriving element lands blurred and sharpens in about 0.13 s |
| Iris from the click | a `clip-path: circle()` opens from the clicked point onto the next world in 0.15 s |
| Dip cut | the outgoing frame darkens about 40 % for 3 frames before a hard cut, so the cut reads as meant |
| Blur swap on one stage | out: opacity → 0 with about 8 px blur in 0.13-0.2 s; in: blur → 0 in 0.13 s; the ground never cuts |
| Match cut | one shape holds while everything around it changes: a circle becomes a lens, a wheel, a logo |
| Ground flip | a hard cut that inverts the ground (white interface to a black claim card, and back) to mark a change of world; four flips in 81 s in Harvey's "Introducing Memory" (`saas-films.md` §7) |
| Zoom travel inside one recording | the camera pushes from one panel of a captured screen to another with a blur that peaks mid-move and sharpens on arrival, so a long take changes focus without a cut |
| Outline fill | a drawn outline of the next device or panel appears over the current shot and fills with its screen, handing the eye from one surface to the next |

Cut at the fastest frame of a move, with matching direction and speed on both sides; mirror the eases across the seam (`power3.in` out, `power3.out` in). A click into a new screen is a match cut on the click's rebound: the new screen comes in slightly large and settles.

**Motion blur** on fast moves: 6-12 px on text-sized elements and 15-20 px full-frame at the move's fastest frame, horizontal-only on a horizontal move. Either render it (average sub-frames per output frame) or draw it as a directional CSS `filter: blur()` keyed to the element's velocity.

## 7. Continuity

- Prefer persistent objects over cuts. An element that travels through scenes and changes role (the prompt bar that becomes the card that becomes the phone) is what makes a film feel designed rather than assembled.
- Keep one home stage to return to, one carrier the eye follows, and the palette and type constant across worlds.
- Derive motion trails and squash from velocity (the value now minus the value one frame ago) rather than faking them.
- Drive glow and emphasis from state, never from time: light should explain the story.
- One hero moment per film. Build to it; do not spend it early.

## 8. Tells of a generated film

Check every render against this list as well as the BANNED line in `SPEC.md`:

- everything fading in at once, or everything on the same duration and curve;
- linear easing on anything that starts or stops;
- text moving while it is read, or titles drifting after they land;
- every scene entering the same way, or the same move beat after beat;
- side-by-side panels and floating cards standing in for a scene;
- a slow creeping scale on a title, or a slow push late in a scene;
- bounce on UI; click rings;
- a page-flip deck: fixed header, page numbers, points fading in one by one, the same camera move each shot, ending on a centred quote card (huashu-art-motion's first failure mode);
- an abstract idea drawn only as words and icons, with no concrete object doing something;
- a dead ground: one flat colour or starfield behind a small moving patch for the whole film;
- real material available but drawn in code instead;
- a film about the logo instead of the product: the mark performs an idea while the product's work, output and evidence never appear;
- a must-carry fact missing, or on screen too small or too briefly to read;
- a camera move that crops the labels at the frame edge partway through (an axis label cut to "RS"), so check the range of every pan, not just its ends;
- a transition frame where the incoming element blurs or scales behind content that is still on screen, so the two collide mid-seam;
- a wide shot of the whole interface that the voice depends on, with its text under 2.6 % of the short side (the commonest fault in 48 shipped product films, `saas-films.md` §5);
- the voice making a claim with no picture of it on screen.
