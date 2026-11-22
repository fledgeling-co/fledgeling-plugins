# A generated video hero

When the person wants motion in the hero and a shader is more than the page needs, a short
generated clip works: muted, `playsinline`, no controls of its own, played once and held on its
last frame, or looped with a pause button. Most of this procedure was paid for once in a real
session, where each unsettled question below cost a regeneration. The rest comes from the
research in `docs/deep-research/`. Sources are in `evidence.md` under "Video".

## Settle four things before anything is generated

Write them into `plan.hero.settled`; `plan_check.py` fails until all four are there.

1. **Whether it replaces the current hero or builds on it.** The first stills in the source
   session reused the existing scene; the person had meant a replacement.
2. **Where it sits and which edge things enter and leave by.** A figure that walks on should cross
   the window's own edge. Mirroring a clip to fit the layout mirrors the exit too, and an exit that
   ran toward the text meant two clips made again.
3. **What the page shows when the clip ends.** A clip that ends on an empty frame leaves a hole in
   the hero and gives nothing to show under reduced motion. End on a frame that can stay.
4. **The beats and their pauses, with a length for each**, adding up to the runtime. Pauses are
   beats: one that is not in the prompt will not be in the clip.

Then settle `plan.hero.playback`: `once` (the default, which holds on the resting frame) or
`loop` (which needs a visible pause control on the page).

## Generate

- **Stills first, and wait for the person's OK** before any video call. Video is billed by the
  second: quote the model's price with `spend.py quote` and say it before the first clip, then the
  running total after each.
- **Read the video tool's parameters before planning a sequence.** The `media-gen-pro` server's
  `generate_video` takes `sourceImage` (the first frame), `lastFrame`, `referenceImages` (a
  character sheet), `inputVideo` (continue from a clip), `resolution`, `durationSeconds`, `audio`
  and `style` (the model). A sequence that joins needs a last-frame input, a resolution and
  `audio: false`. A tool that sends only a prompt and a first frame cannot make clips that join.
- **Image-to-video keeps a subject consistent only from a frame it is given.** To show things
  settling into an arrangement, generate the settled arrangement, animate it coming apart, and
  reverse the clip (`clip_tools.py reverse`). Reverse only motion that reads the same backwards:
  drifting, settling, assembling. Footsteps, falling water and smoke give it away.
- **One continuous clip beats two joined ones.** A full model carried four actions with named
  pauses in one eight-second clip. Split only where the sequence exceeds the model's longest clip.
- **A cheaper model can redraw the subject.** In the source session the lite model simplified a
  face and enlarged a head in its first clip, and every later clip inherited it; the full model
  held the approved design for five clips.
- **Use a 16:9 source.** A 3:1 source produced no file.
- **A router or gateway can time out while the job carries on.** Wait several minutes for the
  file before retrying, or the clip is billed twice.
- **Model ids turn over.** Google shut down the Gemini API's Veo 3.1 preview ids on 22 October
  2026. Pick by the controls you need (first frame, last frame, resolution, silence) and read the
  server's current list, not a model name remembered from earlier.

## Join, loop and fit

- **Join only where one clip's last frame is the next clip's first frame**, given to the model as
  its last-frame and first-frame inputs, and put each join on a pose the subject holds still for
  the final second or two. A model still in motion snaps onto its last frame, and the next clip
  starts from rest; the person saw that as a skipped frame in the middle of a gesture.
- **Find a skip by measuring.** `clip_tools.py joins clip.mp4` compares each frame with the one
  before it and flags a jump more than 2.5 times its neighbours. The skip in the source session
  was one difference three times its neighbours. A crossfade across the join
  (`clip_tools.py xfade a.mp4 b.mp4 out.mp4 --seconds 0.4`, which normalises frame rate, size and
  pixel format first, as FFmpeg's xfade requires) can patch footage already made; it can also
  ghost over motion that does not match, so run `joins` on the result and look at it.
- **A loop.** For a discrete subject or camera move, condition the first and last frames on the
  same image, then `clip_tools.py loop` drops the final frame if it repeats the first. For a
  continuous texture (water, cloud, smoke, particles), first-equals-last conditioning tends to rush
  the motion back in the final second; generate one way and crossfade tail to head instead.
  `clip_tools.py seam` measures the wraparound. Identical endpoints can still loop badly, so watch
  the loop.
- **Fit the length in the script.** In the source session, speeding a clip up and cutting inside
  a clip both showed as skips and were undone. Shorten by rewriting the beats and generating
  again. (Two research members called a retime within 10 to 15% safe; the measured failure wins
  here until a run shows otherwise. See the conflict in `evidence.md`.)

## Watch it

A contact sheet of sampled frames confirms the right actions happened and the design held. It
cannot show pace, a skip, a missing pause, a single-frame flash or a brief morph; Google's own
video understanding samples at one frame a second by default and says so. Run
`clip_tools.py joins`, `seam` and `flashes` on the final encode, then play it at speed on a local
copy of the page. Say in the report whether anyone watched it at speed.

## A stylised character of a real person

Bolder than an abstract image, and the person decides. Say once who will see it.

- **Make a character sheet first** from the photographs they supply: three full-body views on a
  plain background. Get it approved, then pass it as `referenceImages` for every later still and
  clip. Compare each still with the sheet for proportions before showing it.
- **A video model may refuse a stylised still as a real person.** Report the refusal and the
  choices. Trying another model works around a filter, so it is the person's decision.
- **Ask what the picture might be taken to mean.** A grid of objects sorted by size read to one
  person as "a banner for autism", which was not the association wanted on a profile page.

## Blend into the page

Put the subject on a plain backdrop close to the page colour, then
`clip_tools.py grade clip.mp4 out.mp4 --bg "#F4F1EA"` lifts the darkest backdrop to the page's
background, clamps at it and reports the matching share (88% in the source session; the rest was
the subject and its shadow). With an edge fade that stays clear of the text, the video has no
visible frame.

## Encode and serve

`clip_tools.py variants clip.mp4 site/media/ [--av1]` writes a desktop H.264 MP4 (CRF 23, the
x264 default), a phone MP4 at up to 720 px wide, a VP9 WebM, optionally an AV1 file, the first
frame as the poster and the last frame as the resting still, all without audio and with
faststart. CRF is a quality setting, not a size: read the megabytes it prints. It warns past the
provisional budgets (1 MB phone, 3 MB desktop), which one research member proposed as
conservative experimental limits rather than measured ones; shorten or simplify the clip before
raising them, and judge by the page's LCP on the target devices.

```html
<div class="hero-media" style="aspect-ratio: 16 / 9">
  <video autoplay muted playsinline preload="auto" poster="media/hero-poster.jpg"
         aria-hidden="true" data-hero-video>
    <source src="media/hero-phone.mp4" type="video/mp4" media="(max-width: 767px)">
    <source src="media/hero-av1.mp4" type='video/mp4; codecs="av01.0.05M.08"'>
    <source src="media/hero.webm" type="video/webm">
    <source src="media/hero.mp4" type="video/mp4">
  </video>
  <button type="button" class="hero-pause" aria-pressed="false">Pause</button>
</div>
<link rel="preload" as="image" href="media/hero-poster.jpg" fetchpriority="high">
```

```js
const v = document.querySelector("[data-hero-video]");
const btn = document.querySelector(".hero-pause");
const reduce = matchMedia("(prefers-reduced-motion: reduce)");
function settle() { v.pause(); btn.textContent = "Play"; btn.setAttribute("aria-pressed", "true"); }
if (reduce.matches) settle();                       // resting on the poster; nothing plays
else v.play().catch(settle);                        // a refused play() leaves the poster
reduce.addEventListener("change", (e) => e.matches && settle());
btn.addEventListener("click", () => (v.paused ? (v.play(), btn.textContent = "Pause",
  btn.setAttribute("aria-pressed", "false")) : settle()));
```

For a `loop` clip, add the `loop` attribute and keep the button labelled Pause and Play. For a
`once` clip, swap the poster for the resting still on `ended` and relabel the button "Replay". To keep a reduced-motion visitor from downloading the clip at all, put the
sources in `data-src` attributes and assign them only when `reduce.matches` is false.

- **The poster is the likely LCP element.** A video counts for LCP at the earlier of its poster
  or first frame, so preload the poster with `fetchpriority="high"` and never lazy-load the hero.
  Lazy-load video below the fold.
- **Reserve the box.** Give the container an `aspect-ratio` that matches the clip and keep poster
  and video in the same box, so nothing shifts when the video arrives. `width` and `height`
  attributes are fine only when they match the clip and CSS sets `height: auto`; a pair that
  fought the CSS ratio produced a tall zoomed crop on a phone.
- **Sources are chosen once, in order.** Put the phone file first with its `media` query and keep
  the H.264 file last with no `media`, as the file every browser plays. This is a viewport choice,
  not adaptive streaming; check `currentSrc` in the capture.
- **AV1 on Safari needs a hardware decoder** (M3 Macs and A17 Pro iPhones onwards), which is why
  H.264 stays as the fallback.
- **Autoplay is an attempt.** Chrome allows muted autoplay, Safari needs `muted` and `playsinline`
  and pauses off-screen video, iOS Low Power Mode refuses it, and Firefox users can block muted
  video too. Handle a rejected `play()` by leaving the poster, and treat the still hero as a
  complete experience.
- **Under reduced motion,** do not start the video: leave the resting frame showing and do not
  assign the sources, since CSS hiding does not stop the download. Offer a replay control once a
  `once` clip has ended.
- **Range requests.** Safari has refused video from servers that ignore `Range`, including
  `python3 -m http.server`. Run `deploy_check.py media <video URL>` on the deployed host and expect
  206 with a matching `Content-Range`.
