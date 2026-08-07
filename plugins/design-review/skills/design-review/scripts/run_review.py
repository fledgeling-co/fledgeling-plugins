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


REVEAL_JS = """async () => {
  const step = Math.max(200, Math.round(window.innerHeight * 0.8));
  const end = document.documentElement.scrollHeight;
  for (let y = 0; y < end; y += step) {
    window.scrollTo(0, y);
    await new Promise(r => setTimeout(r, 90));
  }
  window.scrollTo(0, 0);
  await new Promise(r => setTimeout(r, 400));
}"""

SETTLE_JS = """async (timeout) => {
  const deadline = Date.now() + timeout;
  const running = () => (document.getAnimations ? document.getAnimations() : [])
    .filter(a => a.playState === 'running');
  while (Date.now() < deadline && running().length) {
    await new Promise(r => setTimeout(r, 100));
  }
  return running().length;
}"""


def reveal_pass(page) -> None:
    """Scroll the whole document, then return to the top, before probing.

    Two defect classes hide behind a page that was never scrolled, and both have
    been misreported as real findings: a scroll-reveal system leaves every band
    below the fold at opacity 0, so a load-time capture reads as a blank page;
    and `loading="lazy"` images have naturalWidth 0 until they enter the
    viewport, so an image probe reports five of eight as broken.
    """
    try:
        page.evaluate(REVEAL_JS)
    except PWError:
        pass


def prove_settled(page, timeout_ms: int = 5000) -> int:
    """Drain running animations, then RETURN how many were still running.

    Draining is not the point; the returned count is. A gate that samples during
    an entrance animation reports precise, confident, wrong numbers — on a real
    run a 400ms-after-scroll axe pass read a `#E85A2A` accent as `#6a2d18` and
    reported a surface getting worse after a fix that provably removed its
    failures. Any count above zero invalidates the colour numbers in that row.
    """
    try:
        return page.evaluate(SETTLE_JS, timeout_ms)
    except PWError:
        return -1


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
    reveal_pass(page)
    still_running = prove_settled(page)

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
    tokens = probes.get("tokens") or {}
    result = {
        "viewport": tag,
        "dpr": dpr,
        "shots": {"fold": f"{tag}-fold.png", "full": f"{tag}-full.png"},
        "tiles": tiles,
        # Settling proof. Any non-zero value here invalidates every colour number
        # in this row — do not report them, re-measure.
        "animationsRunningAtMeasure": still_running,
        "elementsBelowFullOpacity": probes["settled"]["partiallyTransparentElements"],
        "consoleErrorCount": len(errors),
        "failedRequestCount": len(failed),
        "pageOverflowsHorizontally": probes["overflow"]["pageOverflowsHorizontally"],
        "escapingElementCount": len(probes["overflow"]["escaping"]),
        # Numerator AND denominator. `contrastFailureCount: 0` on its own cannot
        # be told apart from a probe that never ran.
        "contrastFailureCount": len([c for c in probes["contrast"] if "ratio" in c]),
        "contrastExamined": probes.get("contrastExamined"),
        "layoutFindingCount": _layout_finding_count(probes.get("layout")),
        "componentTypeCount": (probes.get("layout") or {}).get("inventory", {}).get("distinctTypes"),
        "targetsBelowAA": len([t for t in probes["targets"] if t["belowAA"]]),
        "heavyCropImages": len([i for i in probes["images"] if i["heavyCrop"]]),
        # WCAG 2.4.2 Page Titled is Level A and is the cheapest gate in the set.
        "missingTitle": not (probes["semantics"].get("title") or "").strip(),
        "unconsumedTokenCount": len([t for t in tokens.get("unconsumed", []) if "token" in t]),
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
            len((L.get("columnVoids") or {}).get("voids", [])) +
            len(L["affordance"]["unactionableRows"]) +
            len(L["affordance"]["pointerCursorNotFocusable"]) +
            len(L["tokenOverload"]) + (1 if L["rails"]["exceedsThreshold"] else 0))


def mark_worklist(workdir: Path, surface: str) -> None:
    """Mark this surface's gates and render cells done.

    Capture proves those two stages ran; it proves nothing about states,
    inventory, craft, flow or system, which stay open until their own work
    happens. Silently no-ops when no ledger exists — the ledger is the gate,
    this is only a convenience so it stays current without hand-editing.
    """
    ledger = workdir / "worklist.md"
    if not ledger.exists():
        print(f"\n(no ledger at {ledger}; skipping worklist update)", file=sys.stderr)
        return
    import subprocess
    script = HERE / "worklist.py"
    for stage in ("gates", "render"):
        subprocess.run(
            [sys.executable, str(script), "set", str(workdir),
             "--surface", surface, "--stage", stage, "--value", "done"],
            check=False, capture_output=True)
    print(f"\nWorklist: {surface} gates+render -> done. "
          f"states/inventory/craft/flow/system stay open until their work runs.")
    subprocess.run([sys.executable, str(script), "check", str(workdir)], check=False)


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
    ap.add_argument("--worklist", help="Workdir holding worklist.md. Marks this surface's "
                                       "gates and render cells done once capture succeeds.")
    ap.add_argument("--surface", help="This surface's name in the worklist (default: --url).")
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
        if v.get("animationsRunningAtMeasure"):
            flags.append(f"NOT SETTLED ({v['animationsRunningAtMeasure']} animations running)")
        if v["pageOverflowsHorizontally"]:
            flags.append("H-OVERFLOW")
        if v.get("missingTitle"):
            flags.append("NO <title> (WCAG 2.4.2, Level A)")
        if v["consoleErrorCount"]:
            flags.append(f"{v['consoleErrorCount']} console errors")
        flags.append(f"contrast {v['contrastFailureCount']}/{v.get('contrastExamined')} examined")
        if v["targetsBelowAA"]:
            flags.append(f"{v['targetsBelowAA']} targets <24px")
        if v["heavyCropImages"]:
            flags.append(f"{v['heavyCropImages']} heavy-crop images")
        if v.get("layoutFindingCount"):
            flags.append(f"{v['layoutFindingCount']} layout findings")
        if v.get("unconsumedTokenCount"):
            flags.append(f"{v['unconsumedTokenCount']} declared-but-unread tokens")
        print(f"  {v['viewport']:>10}  {' · '.join(flags)}")

    unsettled = [v for v in manifest["viewports"] if v.get("animationsRunningAtMeasure")]
    if unsettled:
        print("\nWARNING: at least one viewport was measured while animations were still")
        print("running. Colour and contrast numbers from those rows are not usable — a")
        print("mid-entrance sample reads a partially-composited colour as a real one.")
        print("Re-run with a longer --settle-ms before reporting any of them.")

    types = [v.get("componentTypeCount") for v in manifest["viewports"]
             if v.get("componentTypeCount") is not None]
    if types:
        print(f"\n{max(types)} distinct component types found. That is the denominator")
        print("for the report's Coverage block — crop and open them in priority order")
        print("(layout-flagged, interactive, >=3 instances, task path).")

    print("\nCaptures are evidence only once opened. Read the crops before "
          "reporting anything about them. A clean gate run is not a verdict on "
          "the design; it says no known computable defect is present.")

    if args.worklist:
        mark_worklist(Path(args.worklist).resolve(), args.surface or args.url)


if __name__ == "__main__":
    main()
