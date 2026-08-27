#!/usr/bin/env python3
"""
new_explainer.py -- write a starting file with the mechanical scaffolding already wired.

    python3 new_explainer.py out.html --with gsap
    python3 new_explainer.py out.html --with gsap,scrolltrigger --title "The ring that stopped mattering"
    python3 new_explainer.py out.html --with three --canvas

It emits ONLY what the gate enforces and what is identical in every artifact by necessity:
theme tokens, a reduced-motion path, the four data-* markers, pointer capture, an animation
frame that cancels itself, and any vendor blocks you asked for, fetched and checksummed by
vendor_lib.py.

It deliberately emits NO page shape -- no headings beyond the title you pass, no sections, no
layout, no copy. A skill that ships a page template produces pages that look alike, which is
the failure `references/forms.md` exists to fix. Phase 3 picks the shape; this only removes
the typing that is the same every time.

The output FAILS the gate as written: no defined terms, no visual scenes, no wired controls,
no anchored title. That is intended. It is a starting point, not a draft.
"""

import argparse
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
KNOWN = ("gsap", "scrolltrigger", "three")


def vendor_block(kind: str) -> str:
    out = subprocess.run(
        [sys.executable, str(HERE / "vendor_lib.py"), kind],
        capture_output=True, text=True,
    )
    if out.returncode != 0:
        raise SystemExit(out.stderr.strip() or f"vendor_lib.py failed for {kind}")
    sys.stderr.write(out.stderr)
    return out.stdout.rstrip()


HEAD = """<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{title}</title>
<style>
/* Phase 3 sets these. A dominant colour with one accent beats five equal hues, and a flat
   white ground is the strongest single "generated" tell -- replace both deliberately. */
:root{{
  --bg:#f5f3ee; --panel:#fffdf8; --fg:#17150f; --muted:#5b564a; --line:#d5cec0;
  --accent:#0f6d75; --warn:#c2531f; --ok:#2f6d3f;
  --sans:ui-sans-serif,system-ui,-apple-system,"Segoe UI",Roboto,sans-serif;
  --mono:ui-monospace,SFMono-Regular,Menlo,monospace;
}}
@media (prefers-color-scheme: dark){{
  :root{{ --bg:#0e1013; --panel:#161a1f; --fg:#eceae3; --muted:#9aa0a6; --line:#2b3138;
          --accent:#4fd0d8; --warn:#ff8a4c; --ok:#68c98a; }}
}}
*{{box-sizing:border-box}}
body{{margin:0;background:var(--bg);color:var(--fg);font-family:var(--sans);font-size:17px;line-height:1.5}}
.wrap{{max-width:940px;margin:0 auto;padding:40px 22px 90px}}
p{{margin:0 0 14px;max-width:64ch}}
svg{{display:block;width:100%;height:auto}}
canvas{{display:block;width:100%;touch-action:none}}
dfn{{font-style:normal;border-bottom:1px dashed var(--accent)}}
button,input{{font:inherit}}
button:focus-visible,input:focus-visible{{outline:2px solid var(--accent);outline-offset:2px}}
.scrub{{touch-action:none;user-select:none;cursor:ew-resize}}
[hidden]{{display:none}}
@media (prefers-reduced-motion: reduce){{*{{animation:none!important;transition:none!important}}}}
</style>
</head>
<body>
<div class="wrap">

<!-- FORM: <one of the eight in references/forms.md, or your own> because <why, from the invariant>. -->
<!-- surface: <delete this line once the page uses canvas, three.js, gsap, a clip or an image> -->

<h1>{title}</h1>

<section data-pass="1">
  <!-- The turn the mechanism makes, one live variable, the boundary in reach.
       Under 120 words of prose. Define every topic-specific word with <dfn> at first use;
       definitions cost nothing against the budget. -->
  <p data-predict><!-- ask for a guess before the reveal --></p>
  <p data-boundary><!-- where the analogy stops being true, in the topic's own words --></p>
</section>

<section data-pass="2">
  <!-- The steps, reader-paced, state changes signalled. -->
</section>

<section data-pass="3">
  <!-- What production systems do, the edge cases, and what this account still leaves out. -->
</section>

</div>
"""

APP = """
<script>
// One source of truth. Compute, then render; never write state from inside render().
const state = {{ step: 0 }};
function set(patch) {{ Object.assign(state, patch); render(); }}
function render() {{ /* read state, write DOM */ }}

// Drags survive touch only with both of these.
function draggable(el, valueFrom) {{
  let on = false;
  el.addEventListener('pointerdown', e => {{ el.setPointerCapture(e.pointerId); on = true; }});
  el.addEventListener('pointermove', e => {{ if (on) set(valueFrom(e)); }});
  el.addEventListener('pointerup',   e => {{ on = false; el.releasePointerCapture(e.pointerId); }});
}}

// Own the handle and stop at equilibrium; an unbounded loop leaks CPU.
let raf = null;
function tick() {{
  if (!advance()) {{ cancelAnimationFrame(raf); raf = null; return; }}
  render();
  raf = requestAnimationFrame(tick);
}}
function advance() {{ return false; }}
function play()  {{ if (!raf) raf = requestAnimationFrame(tick); }}
function pause() {{ if (raf) {{ cancelAnimationFrame(raf); raf = null; }} }}

const still = matchMedia('(prefers-reduced-motion: reduce)').matches;
{motion}
render();
</script>
</body>
</html>
"""

GSAP_NOTE = """
// Signalling is not optional: an unmarked state change costs g = 0.46-0.53. Build the
// timeline paused, play it on the reader's action, and land its end state under reduced motion.
// const tl = gsap.timeline({ paused: true }).to('#thing', { x: 120, duration: 0.4 });
// if (still) tl.progress(1).pause();
"""

ST_NOTE = """
// gsap.registerPlugin(ScrollTrigger);
// ScrollTrigger.create({ trigger:'#stage', start:'top top', end:'+=2400',
//                        pin:true, scrub:true, animation: tl });
"""

THREE_NOTE = """
// THREE is on window from the vendor block above. Render on change, never on an idle loop,
// and keep a 2D inset in sync -- that is what makes 3D legible rather than impressive.
// const renderer = new THREE.WebGLRenderer({ canvas: document.getElementById('stage'), antialias: true });
"""


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("out", type=Path)
    ap.add_argument("--title", default="Untitled explainer",
                    help="name the subject; a title anchored by nothing fails the gate")
    ap.add_argument("--with", dest="libs", default="",
                    help=f"comma-separated: {', '.join(KNOWN)}")
    ap.add_argument("--canvas", action="store_true", help="declare a <canvas> with an aria-label slot")
    args = ap.parse_args()

    libs = [x.strip().lower() for x in args.libs.split(",") if x.strip()]
    bad = [x for x in libs if x not in KNOWN]
    if bad:
        raise SystemExit(f"unknown library {bad}; choose from {', '.join(KNOWN)}")

    body = HEAD.format(title=args.title)
    if args.canvas:
        body = body.replace(
            '<section data-pass="2">',
            '<canvas id="stage" aria-label="<what the viewport shows and what state it is in>"></canvas>\n\n'
            '<section data-pass="2">')

    blocks = "\n".join(vendor_block(k) for k in libs)
    motion = ""
    if "gsap" in libs:
        motion += GSAP_NOTE
    if "scrolltrigger" in libs:
        motion += ST_NOTE
    if "three" in libs:
        motion += THREE_NOTE

    args.out.write_text(body + blocks + APP.format(motion=motion or "\n"))
    size = args.out.stat().st_size
    print(f"{args.out}: {size:,} bytes"
          + (f", vendoring {', '.join(libs)}" if libs else ", no libraries"), file=sys.stderr)
    print("It fails the gate as written -- no terms, no scenes, no wired controls. "
          "That is the starting point, not a draft.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
