#!/usr/bin/env python3
"""
run_review.py — capture and probe a surface across the viewport matrix.

Produces the evidence base for stages 1-4 of the review: renders, tiles,
per-viewport probe output, console logs, and (optionally) staged interaction
states and mid-flight animation frames.

This script does not judge anything. It gathers facts so the review reasons over
evidence rather than recollection.

Requires Playwright:
    pip install playwright && playwright install chromium

Usage:
    python run_review.py --url http://localhost:3000 --out ./review-work
    python run_review.py --url ... --states --motion --tile
    python run_review.py --url ... --viewports 375,1280

Output layout:
    <out>/
      manifest.json                 index of everything captured
      probes/<w>x<h>.json           probe results per viewport
      console/<w>x<h>.json          console messages + page errors
      shots/<w>x<h>-full.png        full-page capture
      shots/<w>x<h>-fold.png        above-the-fold only
      tiles/<w>x<h>-tile-NN.png     viewport-sized tiles of the full page
      states/<name>.png             staged interaction states
      motion/<name>-tNNN.png        mid-flight animation frames
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright, Error as PWError
except ImportError:
    sys.exit(
        "Playwright is not installed.\n"
        "  pip install playwright && playwright install chromium\n"
        "If no browser automation is available at all, say so in the review "
        "summary and run the static checks only — never imply a page was seen."
    )

HERE = Path(__file__).resolve().parent
PROBES_JS = HERE / "probes.js"

# The review matrix. 375 is the true stress test; breakpoint transitions break
# more often than breakpoints, hence the in-between widths.
DEFAULT_VIEWPORTS = [
    (375, 812),    # mobile
    (600, 900),    # in-between
    (768, 1024),   # tablet
    (1024, 900),   # in-between
    (1280, 900),   # desktop
    (1920, 1080),  # wide
]

# DPR by purpose: 1 answers "what does a user see", 2 answers "is this defective".
DPR_OVERVIEW = 1
DPR_DETAIL = 2


def wait_settled(page, extra_ms: int) -> None:
    """Network idle plus an explicit wait for async renderers.

    Charts and canvas need 2-4s after networkidle. A screenshot of a
    half-rendered chart generates a false finding, which costs more than the
    wait does.
    """
    try:
        page.wait_for_load_state("networkidle", timeout=15000)
    except PWError:
        pass  # some pages never go idle (polling, websockets) — carry on
    try:
        page.evaluate("document.fonts && document.fonts.ready")
    except PWError:
        pass
    page.wait_for_timeout(extra_ms)


def capture_viewport(browser, url, width, height, out: Path, settle_ms: int,
                     tile: bool, dpr: int):
    ctx = browser.new_context(
        viewport={"width": width, "height": height},
        device_scale_factor=dpr,
    )
    page = ctx.new_page()

    console: list[dict] = []
    page.on("console", lambda m: console.append({"type": m.type, "text": m.text[:500]}))
    page.on("pageerror", lambda e: console.append({"type": "pageerror", "text": str(e)[:500]}))
    failed: list[dict] = []
    page.on("requestfailed", lambda r: failed.append(
        {"url": r.url[:200], "failure": (r.failure or "")[:200]}))

    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    wait_settled(page, settle_ms)

    tag = f"{width}x{height}"
    (out / "shots").mkdir(parents=True, exist_ok=True)
    (out / "probes").mkdir(parents=True, exist_ok=True)
    (out / "console").mkdir(parents=True, exist_ok=True)

    page.screenshot(path=str(out / "shots" / f"{tag}-fold.png"))
    page.screenshot(path=str(out / "shots" / f"{tag}-full.png"), full_page=True)

    page.add_script_tag(content=PROBES_JS.read_text())
    probes = page.evaluate("() => window.__designReviewProbes.runAll()")
    (out / "probes" / f"{tag}.json").write_text(json.dumps(probes, indent=2))

    (out / "console" / f"{tag}.json").write_text(json.dumps(
        {"messages": console, "failedRequests": failed}, indent=2))

    tiles: list[str] = []
    if tile:
        # Never feed a monolithic full-page scroll to a vision model: extreme
        # aspect ratios hit image-token compression limits. Tile instead.
        (out / "tiles").mkdir(parents=True, exist_ok=True)
        total = page.evaluate("document.documentElement.scrollHeight")
        offset, idx = 0, 0
        while offset < total and idx < 30:
            page.evaluate(f"window.scrollTo(0, {offset})")
            page.wait_for_timeout(220)
            p = out / "tiles" / f"{tag}-tile-{idx:02d}.png"
            page.screenshot(path=str(p))
            tiles.append(p.name)
            offset += height
            idx += 1
        page.evaluate("window.scrollTo(0, 0)")

    errors = [m for m in console if m["type"] in ("error", "pageerror")]
    result = {
        "viewport": tag,
        "dpr": dpr,
        "shots": {"fold": f"{tag}-fold.png", "full": f"{tag}-full.png"},
        "tiles": tiles,
        "consoleErrorCount": len(errors),
        "failedRequestCount": len(failed),
        "pageOverflowsHorizontally": probes["overflow"]["pageOverflowsHorizontally"],
        "escapingElementCount": len(probes["overflow"]["escaping"]),
        "contrastFailureCount": len([c for c in probes["contrast"] if "ratio" in c]),
        "layoutFindingCount": _layout_finding_count(probes.get("layout")),
        "componentTypeCount": (probes.get("layout") or {}).get("inventory", {}).get("distinctTypes"),
        "targetsBelowAA": len([t for t in probes["targets"] if t["belowAA"]]),
        "heavyCropImages": len([i for i in probes["images"] if i["heavyCrop"]]),
    }
    ctx.close()
    return result


def capture_states(browser, url, out: Path, settle_ms: int, selectors: list[str]):
    """Stage interaction states deliberately.

    Hover contaminates a selected-state capture unless the pointer is moved away
    first, so each state is captured in isolation.
    """
    ctx = browser.new_context(viewport={"width": 1280, "height": 900},
                              device_scale_factor=DPR_DETAIL)
    page = ctx.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    wait_settled(page, settle_ms)
    (out / "states").mkdir(parents=True, exist_ok=True)

    captured = []
    if not selectors:
        selectors = ["button", "a[href]", "input", "[role='button']"]

    for sel in selectors:
        try:
            el = page.query_selector(sel)
            if not el:
                continue
            safe = sel.replace("[", "_").replace("]", "_").replace("'", "").replace(" ", "")[:30]

            el.scroll_into_view_if_needed()
            page.mouse.move(0, 0)
            page.wait_for_timeout(150)
            p = out / "states" / f"{safe}-rest.png"
            el.screenshot(path=str(p))
            captured.append(p.name)

            el.hover()
            page.wait_for_timeout(400)  # let the transition finish
            p = out / "states" / f"{safe}-hover.png"
            el.screenshot(path=str(p))
            captured.append(p.name)

            page.keyboard.press("Tab")
            page.wait_for_timeout(200)
            p = out / "states" / f"{safe}-focus-page.png"
            page.screenshot(path=str(p))
            captured.append(p.name)
        except PWError:
            continue

    # Reduced motion and print are two at-rest checks that catch content which
    # only exists because an animation ran.
    for media, name in ((("reduce",), "reduced-motion"), (None, "print")):
        try:
            if name == "print":
                page.emulate_media(media="print")
            else:
                page.emulate_media(reduced_motion="reduce")
            page.reload(wait_until="domcontentloaded")
            wait_settled(page, settle_ms)
            p = out / "states" / f"page-{name}.png"
            page.screenshot(path=str(p), full_page=True)
            captured.append(p.name)
        except PWError:
            continue
        finally:
            page.emulate_media(media="screen", reduced_motion="no-preference")

    ctx.close()
    return captured


def capture_motion(browser, url, out: Path, settle_ms: int, selector: str,
                   trigger_class: str, frames: int, interval_ms: int):
    """Mid-flight frames.

    Every static check reads the DOM at rest, where an entrance has finished and
    a transient overlay is invisible. A whole class of defect lives in neither
    state, so restart the animation deterministically and capture through it.
    """
    ctx = browser.new_context(viewport={"width": 1280, "height": 900},
                              device_scale_factor=DPR_DETAIL)
    page = ctx.new_page()
    page.goto(url, wait_until="domcontentloaded", timeout=30000)
    wait_settled(page, settle_ms)
    (out / "motion").mkdir(parents=True, exist_ok=True)

    page.evaluate(
        """([sel, cls]) => {
            const el = document.querySelector(sel);
            if (!el) return false;
            el.classList.remove(cls);
            void el.offsetWidth;      // force reflow — this restarts the animation
            el.classList.add(cls);
            return true;
        }""",
        [selector, trigger_class],
    )

    captured = []
    for i in range(frames):
        p = out / "motion" / f"frame-t{i * interval_ms:03d}.png"
        page.screenshot(path=str(p))
        captured.append(p.name)
        page.wait_for_timeout(interval_ms)

    ctx.close()
    return captured


def _layout_finding_count(L):
    """Layout-integrity findings, summed. A probe nobody reads is the failure
    this whole section exists to correct, so it surfaces in the run summary."""
    if not L:
        return 0
    return (len(L["shapeMismatch"]) + len(L["columnDrift"]) +
            len(L["columnHeaderAlignment"]) + len(L["touchingHeadings"]) +
            len(L["textOverlap"]) + len(L["deadSpace"]) +
            len(L["affordance"]["unactionableRows"]) +
            len(L["affordance"]["pointerCursorNotFocusable"]) +
            len(L["tokenOverload"]) + (1 if L["rails"]["exceedsThreshold"] else 0))


def main():
    ap = argparse.ArgumentParser(description="Capture and probe a surface for design review.")
    ap.add_argument("--url", required=True, help="Served URL. Never file:// — module scripts and fonts silently fail.")
    ap.add_argument("--out", default="./review-work")
    ap.add_argument("--viewports", help="Comma-separated widths, e.g. 375,1280. Default: full matrix.")
    ap.add_argument("--settle-ms", type=int, default=2500, help="Extra wait after networkidle for async renderers.")
    ap.add_argument("--dpr", type=int, default=DPR_OVERVIEW, help="1 for 'what a user sees', 2-3 for defect inspection.")
    ap.add_argument("--tile", action="store_true", help="Tile long pages into viewport chunks.")
    ap.add_argument("--states", action="store_true", help="Capture staged interaction states.")
    ap.add_argument("--state-selectors", help="Comma-separated selectors to stage.")
    ap.add_argument("--motion", action="store_true", help="Capture mid-flight animation frames.")
    ap.add_argument("--motion-selector", default="body")
    ap.add_argument("--motion-class", default="seen")
    ap.add_argument("--motion-frames", type=int, default=6)
    ap.add_argument("--motion-interval", type=int, default=200)
    args = ap.parse_args()

    if args.url.startswith("file://"):
        print("WARNING: file:// breaks module scripts, fetches and some fonts. "
              "Serve over HTTP instead (python3 -m http.server).", file=sys.stderr)

    out = Path(args.out).resolve()
    out.mkdir(parents=True, exist_ok=True)

    if args.viewports:
        widths = [int(w.strip()) for w in args.viewports.split(",")]
        sizes = [(w, dict(DEFAULT_VIEWPORTS).get(w, 900)) for w in widths]
    else:
        sizes = DEFAULT_VIEWPORTS

    manifest = {"url": args.url, "viewports": [], "states": [], "motion": []}

    with sync_playwright() as pw:
        browser = pw.chromium.launch()
        for w, h in sizes:
            print(f"  capturing {w}x{h} ...", file=sys.stderr)
            manifest["viewports"].append(
                capture_viewport(browser, args.url, w, h, out, args.settle_ms, args.tile, args.dpr))

        if args.states:
            print("  staging interaction states ...", file=sys.stderr)
            sels = [s.strip() for s in args.state_selectors.split(",")] if args.state_selectors else []
            manifest["states"] = capture_states(browser, args.url, out, args.settle_ms, sels)

        if args.motion:
            print("  capturing mid-flight frames ...", file=sys.stderr)
            manifest["motion"] = capture_motion(
                browser, args.url, out, args.settle_ms,
                args.motion_selector, args.motion_class,
                args.motion_frames, args.motion_interval)

        browser.close()

    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))

    print(f"\nCaptured to {out}")
    print("\nPer viewport:")
    for v in manifest["viewports"]:
        flags = []
        if v["pageOverflowsHorizontally"]:
            flags.append("H-OVERFLOW")
        if v["consoleErrorCount"]:
            flags.append(f"{v['consoleErrorCount']} console errors")
        if v["contrastFailureCount"]:
            flags.append(f"{v['contrastFailureCount']} contrast fails")
        if v["targetsBelowAA"]:
            flags.append(f"{v['targetsBelowAA']} targets <24px")
        if v["heavyCropImages"]:
            flags.append(f"{v['heavyCropImages']} heavy-crop images")
        if v.get("layoutFindingCount"):
            flags.append(f"{v['layoutFindingCount']} layout findings")
        print(f"  {v['viewport']:>10}  {' · '.join(flags) if flags else 'no gate flags'}")

    types = [v.get("componentTypeCount") for v in manifest["viewports"]
             if v.get("componentTypeCount") is not None]
    if types:
        print(f"\n{max(types)} distinct component types found. That is the denominator")
        print("for the report's Coverage block — crop and open them in priority order")
        print("(layout-flagged, interactive, >=3 instances, task path).")

    print("\nCaptures are evidence only once opened. Read the crops before "
          "reporting anything about them. A clean gate run is not a verdict on "
          "the design; it says no known computable defect is present.")


if __name__ == "__main__":
    main()
