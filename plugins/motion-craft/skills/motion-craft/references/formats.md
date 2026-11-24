# Formats: what each kind of film needs

Pick the row from the request, then read its section. Each section adds to `direction.md`, `story-and-rhythm.md` and `craft.md`; it never replaces them.

| Request | Section | Default canvas and length |
|---|---|---|
| Launch, feature, promo, ad | §1 | 1920×1080 at 60 fps, 15-45 s |
| Explainer, tutorial, walkthrough | §2 | 1920×1080 at 30 fps, 30-90 s, narrated |
| Data story from a CSV, dashboard or report | §3 | 1920×1080 at 30 fps, 15-45 s |
| Logo sting, title card, kinetic line | §4 | 1920×1080 at 30 fps, 3-10 s |
| Lower third, callout, caption overlay | §5 | 1920×1080 at 30 fps, 4-10 s, transparent |
| Vertical social clip, reel, short | §6 | 1080×1920 at 60 fps, 15-45 s |
| Product demo of a real app or site | §7 | 1920×1080 at 60 fps, 15-60 s |
| 3D object, simulation, particles, fly-through | §8 | 1080×1350 or 1920×1080 at 60 fps, 15-30 s |
| Remake another film's rhythm on a new subject | `reference-films.md` | match the reference |

60 fps is the default for launch, vertical and demo films, which are led by interface motion and a moving camera: 20 of the 21 product films motionflare.ai made from websites render at 60. 30 fps stays the default for narrated explainers, data stories, stings and overlays, and for any film long enough that render time matters.

## 1. Launch and promo

The beat table in `story-and-rhythm.md` §2 is the default shape; hybrid is the default route. The film is made of the product: real interface captures rebuilt to move, real outputs, real numbers (`direction.md` §2). Every selling point that matters gets its own shot; a price or a key number gets a card of its own rather than tiny type at the end (Cft-TBQv_Y4's comparison). End on the mark, carried in and held 3 s, with the ask as text (`saas-films.md` §10). Music and hits by default. A 15-30 s launch film made from a website works as one continuous take of feature chapters on the brand's moving signature ground, a headline and a product panel swapping every 3-5 s (`looks.md` §1). A launch film about a software product also follows `saas-films.md`: most measured product launches are 45-90 s music-led feature films paced by change inside the shot, not by a cut every 2-3 s.

## 2. Explainer

Narration leads (`sound.md` §1). Measured narrated product explainers run 90-232 s at about 167 spoken words a minute, cut 3-9 times a minute, and restart attention with a 1-5-word chapter card every product area (`saas-films.md` §1, §3). One concrete example is worked through from start to finish; a question the viewer would ask opens each section. Pick the visual grammar by what is being explained: a mechanism or derivation as a diagram that builds and transforms (the 3Blue1Brown family: one canvas, objects morphing rather than cutting); a process as an object travelling through stations; a history as one timeline the camera travels along; numbers as a data story (§3). Long holds are correct while the viewer reads or the picture moves on its own; the camera makes no visible move then, beyond a slow 3-5 % push (`craft.md` §5). Subtitles for vertical, 4:5 and square deliveries; none by default on 16:9.

## 3. Data story

- The data is the source of truth: read the file, compute the figures yourself, and put the computation in `materials.md` so every number on screen can be traced.
- Every headline figure of the data reaches the screen (the total, the peak, the change, and any second metric the data carries) unless the user narrowed the story; a striking chart of one series that leaves the rest of the data unsaid is the measured failure here.
- One number earned per scene. A count-up eases out and lands on the exact value (`craft.md` §1, "a value that lands"), then holds 0.5 s plus 0.3 s a word for its label.
- A chart builds in the order of the argument: axes and baseline first, then the series in the order the story needs, then the one annotation that carries the point, in the accent colour.
- Chart honesty is not optional: a bar chart's baseline is zero; a truncated axis or a dual axis is labelled on screen; the units and the date range are visible while the chart is.
- A dashboard becomes a film by choosing its one story (Anthropic's launch film turned a bike-share dashboard into "the docks on the hill are empty by 8:15"), not by animating every tile.
- The key number made physical (a city of docks, a stack of cash, buildings sized by population) is the hero moment; the 3D route in §8 applies.

## 4. Logo sting, title, kinetic line

Under 10 s, one idea; a 2-second idea stretched to 8 feels slow however it is animated (HyperFrames motion-graphics guide). The logo is the real file. Three beats: an entrance with a deliberate build (assembled from parts of itself, drawn on, revealed through a mask), the completion with its one sound, then a clean hold of at least 1.5 s with nothing moving. The first and last frames are deliberate: the last is a poster that can hold indefinitely.

## 5. Overlay

A lower third, callout, caption group or bug meant to sit on footage. Render with an alpha channel: transparent WebM (VP9 `yuva420p`) or ProRes 4444 MOV, never an MP4. The page background is transparent, the first and last frames are fully clear, and the element holds long enough to read (0.5 s + 0.3 s a word). Name where it sits and check it over a real frame of the footage before handover. Transparency only makes sense when part of the frame is meant to be empty; a full-frame design ships as MP4. No sound, and no signature or watermark.

## 6. Vertical social

1080×1920 at 30 fps. Frame 0 is the thumbnail and the feed autoplays muted, so the first line reads without sound and lands inside 2 s. Keep key content inside the centre 1080×1420 band: the top 10 % and the bottom 20 % carry platform UI, and the right edge carries buttons. Captions on by default; one line at a time, at least 5 % of frame height. A talking head with graphics: the person stays at full brightness and is never covered by a card; cards appear beside or behind them (a matte cut-out lets type sit between the plate and the person).

## 7. Product demo

Use Benji Taylor's Stageshow method: a staged, simplified copy of the real screen made only for the film, with real words only where the story is (3-7 real strings) and quiet filler bars elsewhere, a cursor that moves in shallow arcs timed by distance with visible presses, one action told in 3-5 beats over 10-16 s, and a loop whose last frame matches its first. Caruso's product loops are a measured instance (getcaruso.com, 2026-11-24): about 1 s between steps, a cursor that ticks one checkbox at a time, a status pill above the card narrating in present tense, status chips that turn green as each check passes, and a button that turns green with a check when pressed (`saas-films.md` §3). When the demo shows a real or full-size interface, push 1.5-3x onto the control in use so its text reaches 2.6 % of the frame's short side, and show the whole window only to orient (`saas-films.md` §5). design-craft:design-craft's `references/product-demo.md` carries the full procedure for a demo embedded in a page; here the same demo is one shot inside a film, and the film's rhythm, sound and review apply to it.

## 8. 3D, simulation and particles

When the idea is hundreds of moving things with their own rules, a machine the camera flies through, or a number made into a physical object, build that scene as a canvas or three.js layer inside the composition (claude-motion `web-sims`):

- Simulate anything stateful once at load and store it; the per-frame function only reads that state at time t, so any frame renders on demand and seeking backwards works.
- Seed every random number. Load three.js and fonts from local files, never a CDN, so a render does not depend on the network.
- One hero object beats a crowd; if parts hide the subject, move or fade them.
- Bloom and emissive layers stay under about 1.0 and rise only for the one hero moment, or they eat detail.
- Big glossy surfaces at roughness ≥ 0.45 and `envMapIntensity` around 0.5 avoid white streaks.
- One key light; light from everywhere looks flat (cDb-wPq0Iyk tip 11).
- A camera that flies through the object is worth more than ten orbits.
- Chapters with a one-line caption and labels carrying real numbers make a simulation read as an explanation rather than eye candy.

When the session has a Blender MCP and the film needs a real 3D product (photoreal materials, an exploded view), route that scene to Blender, render it to an image sequence, and composite the sequence into the film as footage; say which scenes came from Blender.
