# Make an Animation: Timeline Pieces, Motion Stories, and Video Export

Produce cinematic, timeline-based motion — product walkthrough videos, animated explainers, launch teasers, kinetic-type pieces, animated logos — as a self-contained HTML artifact with a scrubber, exportable to a real `.mp4`. Use this when the deliverable *is* motion. For motion *inside* a UI (transitions, micro-interactions, scroll effects), use `motion-design.md`.

**An animation is a story with a clock, not a page with movement.** The difference between agency motion work and AI motion slop is direction: shots, pacing, and a reason for every camera move.

## Phase 1: Direct before you animate

Before building anything, write the story: the arc, the key tension, what the viewer should feel at each beat, and the single takeaway. Run it by the user as a **shot list** — one line per scene with duration, content, and camera behavior:

```
0.0–2.5s  Cold open: headline sets the problem, dark bg, type mask-reveals
2.5–6.0s  Product UI establishing shot, slow push-in toward the inbox
6.0–9.5s  Zoom to the compose box; cursor enters, types, sends
9.5–12s   Result: metric counts up, hold 1.5s for reading, end card
```

Direction rules (apply to every scene):

- **Ground scenes in a context.** Elements shouldn't float in a void — put UI inside a browser/device frame, type on a textured or toned background, product shots in an environment. Establishing shot first, then move in close for the action.
- **The static-frame rule.** Except for deliberate dramatic holds, *something* is always in motion — the camera, an element, or a transition. A truly static frame reads as a bug. Images especially: slow zoom or pan (Ken Burns), text building in, or rapid cuts.
- **Reading time is part of the edit.** Text and data need seconds to sink in — a rule of thumb is 0.3s per word plus a beat. Don't cut away from a line the viewer hasn't finished.
- **Cursor walkthroughs:** zoom in and follow the pointer with a damped viewport (the camera eases toward the cursor like Screen Studio, never locks rigidly). Anchor the cursor to real element positions — measure them, don't guess coordinates.
- **Apply the film cut vocabulary:** hard cuts for energy, crossfades for time passing, push-ins for focus, pull-outs for reveals. Pick 2–3 moves and repeat them; a different move every scene reads amateur.
- Disney fundamentals carry straight over: **anticipation** (small counter-move before the main move), **follow-through** (elements settle, don't stop dead), **exaggeration** (10% past realistic reads intentional on screen).

## Phase 2: Build on a timeline engine

Build the piece as one self-contained HTML file around a deterministic clock — every visual is a pure function of time `t`, so the scrubber, reduced-motion end-state, and video export all come free. Implement this engine inline (adapt freely):

```html
<div id="stage-wrap"><div id="stage"><!-- scenes --></div>
  <div id="bar"><button id="play">⏯</button><input id="scrub" type="range" min="0" max="12000" value="0" step="16"><span id="clock"></span></div>
</div>
<script>
const DURATION = 12000, W = 1920, H = 1080;
const stage = document.getElementById('stage');
let t = +localStorage.getItem('anim-t') || 0, playing = false, raf, last;

// Letterbox the fixed-size stage into any viewport (controls stay outside the scale)
function fit() { const s = Math.min(innerWidth / W, (innerHeight - 56) / H);
  stage.style.transform = `scale(${s})`; }
addEventListener('resize', fit); fit();

const clamp01 = v => Math.max(0, Math.min(1, v));
const ease = { out: p => 1 - Math.pow(1 - p, 3), inOut: p => p < .5 ? 4*p*p*p : 1 - Math.pow(-2*p + 2, 3) / 2, lin: p => p };
// Progress of a window [a,b] at time t, eased
const win = (a, b, fn = ease.out) => fn(clamp01((t - a) / (b - a)));
const lerp = (from, to, p) => from + (to - from) * p;

function render() {  // EVERYTHING derives from t — no setTimeout, no CSS animations
  const s1 = win(0, 600);          // e.g. headline reveal
  headline.style.opacity = s1;
  headline.style.transform = `translateY(${lerp(24, 0, s1)}px)`;
  const push = win(2500, 6000, ease.inOut);   // camera push-in
  scene2.style.transform = `scale(${lerp(1, 1.4, push)}) translate(${lerp(0, -120, push)}px, ${lerp(0, -60, push)}px)`;
  document.getElementById('clock').textContent = (t/1000).toFixed(1) + 's';
  scrub.value = t; localStorage.setItem('anim-t', t);
  stage.dataset.screenLabel = `t=${(t/1000).toFixed(1)}s`;  // comments can cite timestamps
}
function tick(now) { if (!playing) return; t = Math.min(DURATION, t + (now - last)); last = now;
  render(); t < DURATION ? raf = requestAnimationFrame(tick) : playing = false; }
play.onclick = () => { playing = !playing; if (playing) { if (t >= DURATION) t = 0; last = performance.now(); raf = requestAnimationFrame(tick); } };
scrub.oninput = e => { playing = false; t = +e.target.value; render(); };
addEventListener('keydown', e => { if (e.key === ' ') { e.preventDefault(); play.onclick(); }
  if (e.key === 'ArrowRight') { t = Math.min(DURATION, t + 250); render(); }
  if (e.key === 'ArrowLeft') { t = Math.max(0, t - 250); render(); }
  if (e.key === '0') { t = 0; render(); } });

// Export bridge — REQUIRED for video export and verifier stepping (Phase 4)
window.__animStage = { duration: DURATION / 1000, setTime: s => { playing = false; t = s * 1000; render(); }, setPlaying: p => { playing = p; } };
if (new URLSearchParams(location.search).has('capture')) document.getElementById('bar').style.display = 'none';
render();
</script>
```

Conventions on top of the engine: group each scene in a positioned container gated by its time window (`display: none` outside it); define scene times as named constants at the top (the edit lives in one place); model motion as `win(start, end, easing)` calls so retiming a scene is a two-number change. Under `prefers-reduced-motion`, render the final frame (`t = DURATION`) with the scrubber still usable — the timeline is content; autoplay is the courtesy you drop.

**Alternative engine: a paused GSAP master timeline** (`gsap-motion.md` Phase 6) — labels, nested scene timelines, and real eases for free; the export bridge becomes `setTime: s => master.time(s, true)` and everything else here (scrubber, export, verifier stepping) works unchanged. Choose it when the piece is choreography-heavy (many overlapping tweens, SplitText, SVG morphs); keep the hand-rolled `t`-engine when the piece is camera-and-scenes simple. Either way, every visual must derive from the clock — no `setTimeout` side-channels, or exported frames desync.

## Phase 3: Score the pacing

Scrub through at 0.25× increments and check: every beat lands ≥300ms after the previous motion settles; nothing important happens during a camera move (viewers can't read mid-pan); total duration is honest (product teasers 15–30s, walkthroughs 30–90s; past 2 minutes it's a video series, not an animation); the last frame is a designed end card that can hold indefinitely. Then step `window.__animStage.setTime()` through the shot list's boundary times, screenshot each, and open every frame — mis-timed scenes show up as empty or overlapping frames, and only in a frame you actually looked at.

## Phase 4: Export to video (when the user wants a file)

The artifact is already the renderer — every frame is a deterministic function of `t`, so export = seek + screenshot + encode. **This is also the reason the engine on this machine can export a timeline piece at all:** Obscura executes no CSS animation and no GSAP timeline (measured 13 Aug 2026), so a piece driven by anything other than the `__animStage.setTime()` bridge cannot be captured here, frame one included. The bridge is not a convenience — it is the export path.

Requires `ffmpeg` on PATH plus **Obscura** (`obscura --version`); Playwright, Puppeteer and `chrome-headless-shell` are removed from this machine, so tell the user what is missing rather than reaching for one or degrading silently. Serve the piece over HTTP first, then drive `obscura serve` over CDP: for each frame, `Runtime.evaluate` the seek, then `Page.captureScreenshot`, and pipe the PNGs into ffmpeg.

```bash
python3 -m http.server 4311 &                  # serve the directory
obscura serve --port 9222 --allow-private-network &   # localhost needs the flag
# then, per frame f:  Runtime.evaluate  window.__animStage.setTime(f/fps)
#                     Page.captureScreenshot  -> stdin of:
ffmpeg -y -f image2pipe -framerate 30 -i - -vf scale=1920:1080 \
       -c:v libx264 -pix_fmt yuv420p -crf 18 out.mp4
```

Set the capture viewport with `Emulation.setDeviceMetricsOverride` (1920×1080, `deviceScaleFactor: 2`) — that domain **does** work here, unlike `setEmulatedMedia`. Two things to check before trusting a long export: **web fonts do not load in this engine**, so the exported video carries the fallback face and that must be stated in the handover; and **if most exported frames are identical the bridge is not seeking** (wrong global name, or the page animates outside the `t` model).

Quality levers: **fps** 30 default, 60 for fast motion, 24 for a filmic feel. **crf** 18 ≈ visually lossless, 23 smaller, >28 artifacts. `deviceScaleFactor: 2` supersamples so text stays crisp after encoding. Every frame is a real screenshot, so a 60s piece at 30fps is 1,800 screenshots — **export a sub-range while iterating**, full range only at the end. This exports seekable timelines only — never try to screen-record arbitrary HTML this way.

## Phase 5: Deliver

Hand over the HTML artifact (the interactive master — scrubber, keyboard controls, persistent playhead), the shot list as the change-request interface ("tighten scene 3" is a two-number edit), and the `.mp4` if exported (note fps/crf so re-exports match). Suggest the natural variants: a 15s cutdown, a square/vertical crop for social (re-fit the stage constants, don't rebuild), or lifting a scene's motion into the product UI via `motion-design.md`.
