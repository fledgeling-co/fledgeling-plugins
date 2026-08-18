#!/usr/bin/env python3
"""Render a banner-src.html to an exact-size PNG, and prove it rendered.

Why this is a script rather than a paragraph of instructions: the banner step is
the one brand artifact with no mechanical check anywhere, and it is the one that
has actually been skipped. tui-craft shipped with a full icon set, an audit
sheet, a README and a root-README row, and no banner, and nothing anywhere
noticed -- not the catalogue build, not a review, not the registration checklist
in the repo's own CLAUDE.md, which does not contain the word.

Three things it asserts, each because trusting them has a silent failure mode:

  1. The viewport override took effect.       A CDP method returning without an
     error proves only that it was accepted. So this reads window.innerWidth back
     and refuses to continue if it is not what was asked for.

  2. The intended font actually loaded.       A web font that fails to arrive
     falls back to a system face, and the render looks deliberate: right layout,
     right colours, wrong letterforms. `document.fonts.check()` settles it, and
     the fallback width is measured as a control so a font that is merely
     *installed* locally cannot pass for one that was fetched.

  3. The PNG is exactly the size the family ships.  3200x1040 by default, from a
     1600x520 layout at deviceScaleFactor 2.

Usage
-----
    render_banner.py plugins/<name>/assets/banner-src.html
    render_banner.py <src> --font "Martian Mono" --weight 700
    render_banner.py <src> --width 1600 --height 520 --scale 2 --port 9377
"""

from __future__ import annotations

import argparse
import asyncio
import base64
import json
import os
import re
import shutil
import signal
import socket
import subprocess
import sys
import time
from pathlib import Path

try:
    import websockets
except ImportError:
    print("This needs the `websockets` package to speak CDP: pip install websockets",
          file=sys.stderr)
    raise SystemExit(2)


def free_port(preferred: int) -> int:
    """A port no sibling agent is using.

    Banners get rendered by parallel agents in this pipeline, and two of them on
    one port is a race that shows up as a blank or half-painted capture rather
    than as an error.
    """
    for p in [preferred] + list(range(preferred + 1, preferred + 40)):
        with socket.socket() as s:
            try:
                s.bind(("127.0.0.1", p))
                return p
            except OSError:
                continue
    raise SystemExit("no free port near %d" % preferred)


class Obscura:
    def __init__(self, port: int):
        self.port = port
        self.proc: subprocess.Popen | None = None

    def __enter__(self):
        if not shutil.which("obscura"):
            raise SystemExit("obscura is not on PATH. Every browser task in this "
                             "environment goes through it.")
        self.proc = subprocess.Popen(
            ["obscura", "serve", "--port", str(self.port), "--allow-private-network"],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
            start_new_session=True)
        deadline = time.time() + 25
        while time.time() < deadline:
            try:
                import urllib.request
                with urllib.request.urlopen(
                        f"http://127.0.0.1:{self.port}/json/version", timeout=1) as r:
                    json.load(r)
                return self
            except Exception:
                time.sleep(0.3)
        raise SystemExit(f"obscura serve did not come up on {self.port}")

    def __exit__(self, *exc):
        if self.proc and self.proc.poll() is None:
            os.killpg(os.getpgid(self.proc.pid), signal.SIGTERM)
            try:
                self.proc.wait(timeout=8)
            except subprocess.TimeoutExpired:
                os.killpg(os.getpgid(self.proc.pid), signal.SIGKILL)

    def browser_ws(self) -> str:
        """The BROWSER endpoint, then create and attach a page from it.

        Obscura's `serve` advertises a page target at `/json/list`, and
        connecting straight to that socket is the obvious move and the wrong one:
        every page, runtime and emulation call then fails with
        `{"code": -32601, "message": "No page for session"}`, which reads like a
        missing method and is actually a missing session. The working sequence is
        the flattened-session one -- connect to the browser, `Target.createTarget`,
        `Target.attachToTarget` with `flatten: true`, and pass the returned
        `sessionId` on every subsequent command. Measured here 2026-08-17: with
        the session attached, `Emulation.setDeviceMetricsOverride` takes effect
        and `window.innerWidth` reads back the requested 1600.
        """
        import urllib.request
        deadline = time.time() + 15
        while time.time() < deadline:
            try:
                with urllib.request.urlopen(
                        f"http://127.0.0.1:{self.port}/json/version", timeout=3) as r:
                    v = json.load(r)
                if v.get("webSocketDebuggerUrl"):
                    return v["webSocketDebuggerUrl"]
            except Exception:
                pass
            time.sleep(0.4)
        raise SystemExit(f"obscura advertised no browser socket on {self.port}")


class CDP:
    def __init__(self, ws):
        self.ws, self.n, self.session = ws, 0, None

    async def call(self, method: str, params: dict | None = None,
                   browser_level: bool = False):
        self.n += 1
        mid = self.n
        msg = {"id": mid, "method": method, "params": params or {}}
        if self.session and not browser_level:
            msg["sessionId"] = self.session
        await self.ws.send(json.dumps(msg))
        while True:
            got = json.loads(await self.ws.recv())
            if got.get("id") == mid:
                if "error" in got:
                    raise RuntimeError(f"{method}: {got['error']}")
                return got.get("result", {})

    async def attach(self) -> str:
        t = await self.call("Target.createTarget", {"url": "about:blank"},
                            browser_level=True)
        a = await self.call("Target.attachToTarget",
                            {"targetId": t["targetId"], "flatten": True},
                            browser_level=True)
        self.session = a["sessionId"]
        return self.session

    async def evaluate(self, expr: str, await_promise: bool = False):
        r = await self.call("Runtime.evaluate", {
            "expression": expr, "returnByValue": True,
            "awaitPromise": await_promise})
        if r.get("exceptionDetails"):
            raise RuntimeError(f"evaluate: {r['exceptionDetails']}")
        return r.get("result", {}).get("value")


async def render(src: Path, out: Path, width: int, height: int, scale: int,
                 font: str | None, weight: int, port: int, settle: float) -> dict:
    with Obscura(port) as ob:
        async with websockets.connect(ob.browser_ws(),
                                      max_size=64 * 1024 * 1024) as ws:
            cdp = CDP(ws)
            await cdp.attach()
            await cdp.call("Page.enable")
            await cdp.call("Runtime.enable")

            await cdp.call("Emulation.setDeviceMetricsOverride", {
                "width": width, "height": height,
                "deviceScaleFactor": scale, "mobile": False})

            await cdp.call("Page.navigate", {"url": src.resolve().as_uri()})
            await asyncio.sleep(settle)
            try:
                await cdp.evaluate("document.fonts.ready.then(()=>true)", True)
            except Exception:
                pass
            await asyncio.sleep(0.4)

            # ASSERTION 1 -- the override is real, not merely accepted.
            iw = await cdp.evaluate("window.innerWidth")
            ih = await cdp.evaluate("window.innerHeight")
            if iw != width:
                raise SystemExit(
                    f"viewport override was accepted and did not take effect: "
                    f"asked for {width}px, page reports {iw}px. Rendering now "
                    f"would produce a correct-looking banner at the wrong size.")

            report = {"innerWidth": iw, "innerHeight": ih}

            # ASSERTION 2 -- the intended font arrived, with a control.
            if font:
                ok = await cdp.evaluate(
                    f'document.fonts.check(\'{weight} 80px "{font}"\')')
                probe = await cdp.evaluate(f"""(() => {{
                  const mk = f => {{
                    const s = document.createElement('span');
                    s.textContent = 'HHHHHHHHHH';
                    s.style.cssText =
                      'position:absolute;visibility:hidden;display:inline-block;'
                      + 'font:{weight} 80px ' + f;
                    document.body.appendChild(s);
                    const w = s.getBoundingClientRect().width;
                    s.remove(); return w;
                  }};
                  return JSON.stringify({{
                    target: mk('"{font}", monospace'),
                    fallback: mk('monospace'),
                  }});
                }})()""")
                p = json.loads(probe)
                ratio = (p["target"] / p["fallback"]) if p["fallback"] else 0
                report["font"] = {"name": font, "fontsCheck": bool(ok),
                                  "advanceRatioVsFallback": round(ratio, 4), **p}
                # The MEASURED advance decides, not `document.fonts.check()`.
                # Measured on this engine 2026-08-17: check() returned False for
                # a font it was demonstrably rendering with -- the same probe
                # gave 560px against a 481px monospace fallback, a 1.164 ratio
                # that reproduced exactly in a standalone test. So the API
                # under-reports and the observable is right, which is the whole
                # reason this asserts an observable at all. check() is kept in
                # the report as advisory and the disagreement is stated.
                if abs(p["target"] - p["fallback"]) < 1.0:
                    raise SystemExit(
                        f'the banner asks for "{font}" and it did not load: its '
                        f'advance ({p["target"]}px) matches the monospace '
                        f'fallback ({p["fallback"]}px), so the render would look '
                        f'deliberate and carry the wrong letterforms. Not written.')
                if not ok:
                    print(f'note: document.fonts.check() says "{font}" is not '
                          f'available, but its advance differs from the fallback '
                          f'by a factor of {ratio:.3f}, so it is being used. '
                          f'check() under-reports on this engine.', file=sys.stderr)

            # ASSERTION 2b -- every image actually decoded.
            # A banner whose icon failed to load renders as a correct layout with
            # a hole in it and reports no error at all. That shipped once.
            imgs = await cdp.evaluate("""JSON.stringify(
              Array.from(document.images).map(i => ({
                src: (i.currentSrc || i.src || '').slice(0, 60),
                complete: i.complete, w: i.naturalWidth })))""")
            broken = [i for i in json.loads(imgs or "[]")
                      if not i["complete"] or not i["w"]]
            report["images"] = {"total": len(json.loads(imgs or "[]")),
                                "broken": broken}
            if broken:
                raise SystemExit(
                    f"{len(broken)} image(s) did not load, so the banner has a "
                    f"hole where artwork should be: {broken}. Obscura does not "
                    f"fetch file:// subresources from a file:// page -- inline "
                    f"the artwork as a data URI.")

            # ASSERTION 2c -- no *text* runs past the frame.
            #
            # This deliberately ignores elements with no text of their own. The
            # assertion exists so nothing readable is cropped, and a decorative
            # element bleeding off the edge under `overflow: hidden` is a
            # composition choice the family already uses: better-loop's seal row
            # sits at `right: -60px` on purpose, so the state reads as continuing
            # past the window. Flagging it refused a banner whose PNG was correct
            # and whose only overflowing nodes were six empty divs and spans.
            #
            # A text node's own text is what matters, not its descendants', or a
            # wrapper inherits the blame for a child that fits.
            over = await cdp.evaluate(f"""(() => {{
              const ownText = (el) => Array.from(el.childNodes)
                .filter(n => n.nodeType === 3)
                .map(n => n.textContent)
                .join('')
                .trim();
              const bad = [];
              for (const el of document.querySelectorAll('body *')) {{
                const r = el.getBoundingClientRect();
                const t = ownText(el);
                if (r.width && r.right > {width} + 0.5 && t)
                  bad.push({{ tag: el.tagName.toLowerCase(),
                              cls: el.className || '',
                              right: Math.round(r.right),
                              text: t.slice(0, 40) }});
              }}
              return JSON.stringify(bad.slice(0, 6));
            }})()""")
            spill = json.loads(over or "[]")
            report["overflow"] = spill
            if spill:
                raise SystemExit(
                    f"text runs past the {width}px frame and would be cropped "
                    f"in the shipped PNG: {spill}")

            derived = await cdp.evaluate(
                "window.__banner ? JSON.stringify(window.__banner) : null")
            if derived:
                report["derived"] = json.loads(derived)

            shot = await cdp.call("Page.captureScreenshot",
                                  {"format": "png", "captureBeyondViewport": False})
            data = base64.b64decode(shot["data"])
            out.write_bytes(data)

    # ASSERTION 3 -- the file on disk is the size the family ships.
    want = (width * scale, height * scale)
    try:
        from PIL import Image
        got = Image.open(out).size
    except ImportError:
        got = None
    if got and got != want:
        raise SystemExit(f"rendered {got[0]}x{got[1]}, expected {want[0]}x{want[1]}")
    report["png"] = {"path": str(out), "size": list(got) if got else "unverified",
                     "bytes": out.stat().st_size}
    return report


# CSS this engine accepts and never paints. Each was measured on 2026-08-19
# against a deterministic fixture: a hard black shadow at a 30px offset on white
# read (255,255,255) where `filter: drop-shadow` specified it and (0,0,0) where
# the identical `box-shadow` did, and an `inset` band specified black read as the
# element's own grey. Nothing errors, `banner_sheet.py check` passes, and the
# banner simply has no contact shadow or no rim light.
#
# This is the same class as the five assertions above and it was the largest one:
# 28 of the family's banner sources declared a drop-shadow that has never painted
# once, and 7 declared inset shadows, 13 in total. `clip-path: ellipse()` is inert
# too and no banner uses it; it is listed so the next author does not discover it
# the slow way. Refusing here is deliberate, and it refuses at re-render time
# rather than in any gate: a banner already shipped stays shipped, and the defect
# gets fixed by whoever next opens that source.
INERT_CSS = (
    (re.compile(r"filter\s*:[^;{}]*\bdrop-shadow\s*\(", re.I),
     "filter: drop-shadow()",
     "put a box-shadow on a backing box behind the element, or draw the shadow "
     "in inline SVG with feDropShadow, which does render"),
    (re.compile(r"box-shadow\s*:[^;{}]*\binset\b", re.I),
     "inset box-shadow",
     "draw the rim or seat as its own absolutely positioned element, or as an "
     "inline SVG stroke"),
    (re.compile(r"clip-path\s*:[^;{}]*\bellipse\s*\(", re.I),
     "clip-path: ellipse()",
     "clip-path: polygon() renders, and so does an SVG <clipPath>"),
)


def assert_effects_paint(src_text: str) -> None:
    """Refuse a source whose declared effects this engine will silently drop."""
    body = re.sub(r"<!--.*?-->", "", src_text, flags=re.S)
    body = re.sub(r"/\*.*?\*/", "", body, flags=re.S)
    found = []
    for rx, name, fix in INERT_CSS:
        n = len(rx.findall(body))
        if n:
            found.append(f"  {n}x {name}\n      instead: {fix}")
    if found:
        raise SystemExit(
            "render_banner: the source declares effects this engine accepts and "
            "never paints, so the banner would render without them and pass every "
            "check:\n" + "\n".join(found) +
            "\n  (measured 2026-08-19 against a fixture; comments are ignored, so "
            "documenting the trap in a comment is fine)")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("src", help="path to banner-src.html")
    ap.add_argument("-o", "--out", help="default: banner.png beside the source")
    ap.add_argument("--width", type=int, default=1600)
    ap.add_argument("--height", type=int, default=520)
    ap.add_argument("--scale", type=int, default=2)
    ap.add_argument("--font", help="assert this family actually loaded")
    ap.add_argument("--weight", type=int, default=700)
    ap.add_argument("--port", type=int, default=9377)
    ap.add_argument("--settle", type=float, default=3.0)
    args = ap.parse_args()

    src = Path(args.src)
    if not src.exists():
        raise SystemExit(f"no such file: {src}")
    assert_effects_paint(src.read_text(errors="replace"))
    out = Path(args.out) if args.out else src.with_name("banner.png")

    report = asyncio.run(render(src, out, args.width, args.height, args.scale,
                                args.font, args.weight, free_port(args.port),
                                args.settle))
    print(json.dumps(report, indent=1))
    print("\nNow open it and look at it. Every assertion above is about whether "
          "the render happened, not about whether it is any good.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
