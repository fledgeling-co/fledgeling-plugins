#!/usr/bin/env python3
"""
run_review.py — capture and probe a surface across the viewport matrix.

Produces the evidence base for stages 1-4 of the review: renders, tiles,
per-viewport probe output, console logs, and (optionally) staged interaction
states.

This script does not judge anything. It gathers facts so the review reasons over
evidence rather than recollection.

Requires Obscura on PATH and nothing else:
    download the aarch64-macos release from
    https://github.com/h4ckf0r0day/obscura and put it in ~/.local/bin

The CDP client below is stdlib-only, so there is no pip install and no virtualenv
to keep in step with the Node path — both scripts drive the same `obscura serve`.

Usage:
    python run_review.py --url http://localhost:3000 --out ./review-work
    python run_review.py --url ... --states --tile
    python run_review.py --url ... --viewports 375,1280

Output layout:
    <out>/
      manifest.json                 index of everything captured
      probes/<w>x<h>.json           probe results per viewport
      console/<w>x<h>.json          console messages + failed requests
      shots/<w>x<h>-full.png        full-page capture
      shots/<w>x<h>-fold.png        above-the-fold only
      tiles/<w>x<h>-tile-NN.png     viewport-sized tiles of the full page
      states/<name>.png             staged interaction states
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import random
import shutil
import socket
import struct
import subprocess
import sys
import time
import urllib.request
from pathlib import Path
from urllib.parse import urlparse

if shutil.which("obscura") is None:
    sys.exit(
        "Obscura is not on PATH.\n"
        "  download the aarch64-macos release from\n"
        "  https://github.com/h4ckf0r0day/obscura and put it in ~/.local/bin\n"
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


class CDPError(RuntimeError):
    pass


# ---------------------------------------------------------------------------
# Obscura driver.
#
# `obscura serve` speaks Chrome-compatible CDP over a WebSocket. Python has no
# WebSocket in the standard library, and the alternative — driving `obscura
# fetch` per capture — cannot set a viewport at all, which would delete the
# viewport matrix this whole script exists for. So the framing is done here:
# ~70 lines of RFC 6455, no dependency to install.
# ---------------------------------------------------------------------------


class _WebSocket:
    """Just enough RFC 6455 to carry CDP: masked text out, fragmented text in."""

    def __init__(self, url: str, timeout: float = 30.0):
        u = urlparse(url)
        self.sock = socket.create_connection((u.hostname, u.port or 80), timeout=timeout)
        self.sock.settimeout(timeout)
        key = base64.b64encode(os.urandom(16)).decode()
        path = u.path + (("?" + u.query) if u.query else "")
        req = (
            f"GET {path} HTTP/1.1\r\n"
            f"Host: {u.hostname}:{u.port}\r\n"
            "Upgrade: websocket\r\nConnection: Upgrade\r\n"
            f"Sec-WebSocket-Key: {key}\r\nSec-WebSocket-Version: 13\r\n\r\n"
        )
        self.sock.sendall(req.encode())
        self._buf = b""
        while b"\r\n\r\n" not in self._buf:
            chunk = self.sock.recv(4096)
            if not chunk:
                raise CDPError("websocket handshake closed early")
            self._buf += chunk
        head, self._buf = self._buf.split(b"\r\n\r\n", 1)
        if b"101" not in head.split(b"\r\n")[0]:
            raise CDPError("websocket handshake refused: " + head.split(b"\r\n")[0].decode())

    def _recv_exact(self, n: int) -> bytes:
        while len(self._buf) < n:
            chunk = self.sock.recv(65536)
            if not chunk:
                raise CDPError("websocket closed")
            self._buf += chunk
        out, self._buf = self._buf[:n], self._buf[n:]
        return out

    def send(self, text: str) -> None:
        payload = text.encode()
        n = len(payload)
        header = bytearray([0x81])          # FIN + text
        if n < 126:
            header.append(0x80 | n)
        elif n < (1 << 16):
            header.append(0x80 | 126)
            header += struct.pack(">H", n)
        else:
            header.append(0x80 | 127)
            header += struct.pack(">Q", n)
        mask = os.urandom(4)
        header += mask
        masked = bytes(b ^ mask[i % 4] for i, b in enumerate(payload))
        self.sock.sendall(bytes(header) + masked)

    def recv(self) -> str | None:
        """Next complete text message, or None when the peer closed."""
        parts: list[bytes] = []
        while True:
            b0, b1 = self._recv_exact(2)
            fin, opcode = b0 & 0x80, b0 & 0x0F
            length = b1 & 0x7F
            if length == 126:
                length = struct.unpack(">H", self._recv_exact(2))[0]
            elif length == 127:
                length = struct.unpack(">Q", self._recv_exact(8))[0]
            data = self._recv_exact(length) if length else b""
            if opcode == 0x8:               # close
                return None
            if opcode == 0x9:               # ping — keep the session alive
                self.sock.sendall(b"\x8a\x80" + os.urandom(4))
                continue
            if opcode in (0x1, 0x0):
                parts.append(data)
                if fin:
                    return b"".join(parts).decode("utf-8", "replace")
            # binary and pong frames carry nothing CDP needs

    def close(self) -> None:
        try:
            self.sock.sendall(b"\x88\x80" + os.urandom(4))
        except OSError:
            pass
        try:
            self.sock.close()
        except OSError:
            pass


class CDP:
    """A CDP connection. Replies are matched by id; events are collected."""

    def __init__(self, port: int):
        self.port = port
        raw = urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=10).read()
        self.ws = _WebSocket(json.loads(raw)["webSocketDebuggerUrl"])
        self._id = 0
        self.events: list[dict] = []

    def reconnect(self) -> None:
        """Drop a desynced socket and open a fresh one.

        After a read timeout the reply is still in flight, so the next command's
        recv() picks up the PREVIOUS reply and from then on every result is
        attributed to the wrong caller. That is worse than the timeout, because
        the numbers stay plausible. Ids restart from zero on the new socket.
        """
        try:
            self.ws.close()
        except Exception:
            pass
        raw = urllib.request.urlopen(
            f"http://127.0.0.1:{self.port}/json/version", timeout=10).read()
        self.ws = _WebSocket(json.loads(raw)["webSocketDebuggerUrl"])
        self._id = 0

    def send(self, method: str, params: dict | None = None, session_id: str | None = None) -> dict:
        self._id += 1
        msg = {"id": self._id, "method": method, "params": params or {}}
        if session_id:
            msg["sessionId"] = session_id
        self.ws.send(json.dumps(msg))
        while True:
            raw = self.ws.recv()
            if raw is None:
                raise CDPError(f"connection closed waiting for {method}")
            frame = json.loads(raw)
            if frame.get("id") == self._id:
                return frame
            if "method" in frame:
                self.events.append(frame)

    def drain(self, seconds: float) -> None:
        """Read pending events for a while. CDP is push-based; without this the
        network bookkeeping only advances when a command happens to be sent."""
        deadline = time.time() + seconds
        self.ws.sock.settimeout(0.2)
        try:
            while time.time() < deadline:
                try:
                    raw = self.ws.recv()
                except (socket.timeout, TimeoutError):
                    continue
                except OSError:
                    return
                if raw is None:
                    return
                frame = json.loads(raw)
                if "method" in frame:
                    self.events.append(frame)
        finally:
            self.ws.sock.settimeout(30.0)

    def close(self) -> None:
        self.ws.close()


def start_obscura(port: int) -> subprocess.Popen:
    """Start `obscura serve`. --allow-private-network is not optional: a dev
    server on 127.0.0.1 is blocked by default and the capture fails as an SSRF
    block, which reads like a broken page rather than a blocked fetch."""
    proc = subprocess.Popen(
        ["obscura", "--allow-private-network", "serve", "--port", str(port), "--quiet"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
    )
    deadline = time.time() + 15
    while time.time() < deadline:
        try:
            urllib.request.urlopen(f"http://127.0.0.1:{port}/json/version", timeout=1).read()
            return proc
        except Exception:
            time.sleep(0.2)
    proc.kill()
    raise CDPError(f"obscura serve did not come up on port {port}")


# Obscura emits neither Runtime.consoleAPICalled nor Log.entryAdded, so the
# console gate is served by a page-side hook installed before navigation. It
# records what the page's own scripts log plus uncaught errors and rejections.
# It cannot see browser-emitted subresource failures ("Failed to load resource
# … 404") — those come from the network list instead, which is why both are
# written out and why a console count alone is never a finding.
CONSOLE_HOOK = """
(() => {
  if (window.__drConsole) return;
  window.__drConsole = [];
  const push = (type, text) => { try { window.__drConsole.push({ type, text: String(text).slice(0, 500) }); } catch (e) {} };
  const fmt = v => {
    if (typeof v === 'string') return v;
    if (v instanceof Error) return v.stack || v.message;
    try { return JSON.stringify(v); } catch (e) { return String(v); }
  };
  for (const k of ['log', 'info', 'warn', 'error', 'debug']) {
    const orig = console[k];
    console[k] = (...a) => { push(k, a.map(fmt).join(' ')); if (orig) orig.apply(console, a); };
  }
  addEventListener('error', e => push('pageerror', e.message || e.error));
  addEventListener('unhandledrejection', e => push('pageerror', e.reason));
})();"""

REVEAL_JS = """(async () => {
  const step = Math.max(200, Math.round(window.innerHeight * 0.8));
  const end = document.documentElement.scrollHeight;
  for (let y = 0; y < end; y += step) {
    window.scrollTo(0, y);
    await new Promise(r => setTimeout(r, 90));
  }
  window.scrollTo(0, 0);
  await new Promise(r => setTimeout(r, 400));
})()"""

SETTLE_JS = """(async () => {
  const deadline = Date.now() + %d;
  const running = () => (document.getAnimations ? document.getAnimations() : [])
    .filter(a => a.playState === 'running');
  while (Date.now() < deadline && running().length) {
    await new Promise(r => setTimeout(r, 100));
  }
  return running().length;
})()"""


class Page:
    """One Obscura target plus the bookkeeping the review needs from it."""

    def __init__(self, cdp: CDP, width: int, height: int, dpr: int):
        self.cdp = cdp
        self.width, self.height, self.dpr = width, height, dpr
        self.url: str | None = None
        target = cdp.send("Target.createTarget", {"url": "about:blank"})
        self.target_id = target["result"]["targetId"]
        attached = cdp.send("Target.attachToTarget",
                            {"targetId": self.target_id, "flatten": True})
        self.session_id = attached["result"]["sessionId"]
        for domain in ("Page", "Runtime", "Network", "DOM"):
            cdp.send(f"{domain}.enable", {}, self.session_id)
        cdp.send("Page.addScriptToEvaluateOnNewDocument",
                 {"source": CONSOLE_HOOK}, self.session_id)
        self._event_mark = len(cdp.events)
        self.set_viewport(width, height, dpr)

    def set_viewport(self, width: int, height: int, dpr: int) -> None:
        self.cdp.send("Emulation.setDeviceMetricsOverride",
                      {"width": width, "height": height, "deviceScaleFactor": dpr,
                       "mobile": width <= 480}, self.session_id)

    def recover(self) -> bool:
        """Rebuild this page after a desynced socket. Returns True on success.

        Re-attaching to the SAME target is not available on this engine.
        Measured 15 Aug 2026: on a fresh socket Obscura's `Target.getTargets`
        returns an empty list and `Target.attachToTarget` answers "Target not
        found", because the Target domain is scoped to the connection that
        created it — while `/json/list` still cheerfully lists the page. The
        HTTP listing is not evidence that a target is reachable.

        So recovery is a new target and a fresh navigation, and it is not free:
        scroll position, settle state and anything the page accumulated are
        gone, so probes taken afterwards were taken on a re-loaded document.
        `run_probes()` records which ones those were.
        """
        if not self.url:
            return False
        # The renderer is usually still finishing the call that overran and
        # cannot service a createTarget until it is done, so an immediate single
        # attempt fails on exactly the case worth recovering.
        last: Exception | None = None
        for delay in (0, 2, 4, 8):
            if delay:
                time.sleep(delay)
            try:
                self.cdp.reconnect()
                target = self.cdp.send("Target.createTarget", {"url": "about:blank"})
                self.target_id = target["result"]["targetId"]
                attached = self.cdp.send("Target.attachToTarget",
                                         {"targetId": self.target_id, "flatten": True})
                self.session_id = attached["result"]["sessionId"]
                for domain in ("Page", "Runtime", "Network", "DOM"):
                    self.cdp.send(f"{domain}.enable", {}, self.session_id)
                self.cdp.send("Page.addScriptToEvaluateOnNewDocument",
                              {"source": CONSOLE_HOOK}, self.session_id)
                self._event_mark = len(self.cdp.events)
                self.set_viewport(self.width, self.height, self.dpr)
                self.goto(self.url)
                return True
            except Exception as e:                    # busy renderer, refused socket
                last = e
        print(f"  ! page recovery failed after retries: {last}", file=sys.stderr)
        return False

    def goto(self, url: str, timeout_ms: int = 30000) -> None:
        self.url = url
        r = self.cdp.send("Page.navigate", {"url": url}, self.session_id)
        if "error" in r:
            raise CDPError(f"navigate failed: {r['error']}")
        deadline = time.time() + timeout_ms / 1000
        while time.time() < deadline:
            if self.evaluate("document.readyState") in ("complete", "interactive"):
                return
            time.sleep(0.15)

    def evaluate(self, expression: str, await_promise: bool = False):
        r = self.cdp.send("Runtime.evaluate",
                          {"expression": expression, "returnByValue": True,
                           "awaitPromise": await_promise}, self.session_id)
        if "error" in r or r.get("result", {}).get("exceptionDetails"):
            return None
        return r.get("result", {}).get("result", {}).get("value")

    def console_messages(self) -> list[dict]:
        raw = self.evaluate("JSON.stringify(window.__drConsole || [])")
        try:
            return json.loads(raw or "[]")
        except (TypeError, ValueError):
            return []

    def failed_requests(self) -> list[dict]:
        """Failed subresources. Obscura reports an HTTP error as an ordinary
        response with a 4xx/5xx status rather than as Network.loadingFailed, so
        both shapes are read."""
        out = []
        for frame in self.cdp.events[self._event_mark:]:
            if frame.get("method") == "Network.loadingFailed":
                out.append({"url": "(unknown)",
                            "failure": str(frame.get("params", {}).get("errorText", ""))[:200]})
            elif frame.get("method") == "Network.responseReceived":
                resp = frame.get("params", {}).get("response", {})
                if resp.get("status", 0) >= 400:
                    out.append({"url": str(resp.get("url", ""))[:200],
                                "failure": f"HTTP {resp['status']}"})
        return out

    def screenshot(self, path: Path, full_page: bool = False, clip: dict | None = None) -> bool:
        params: dict = {"format": "png"}
        if clip:
            params["clip"] = {**clip, "scale": 1}
            params["captureBeyondViewport"] = True
        elif full_page:
            metrics = self.cdp.send("Page.getLayoutMetrics", {}, self.session_id)
            size = (metrics.get("result", {}).get("contentSize")
                    or metrics.get("result", {}).get("cssContentSize"))
            if size:
                params["clip"] = {"x": 0, "y": 0, "width": size["width"],
                                  "height": size["height"], "scale": 1}
                params["captureBeyondViewport"] = True
        r = self.cdp.send("Page.captureScreenshot", params, self.session_id)
        data = r.get("result", {}).get("data")
        if not data:
            return False
        path.write_bytes(base64.b64decode(data))
        return True

    def box_of(self, selector: str) -> dict | None:
        raw = self.evaluate(
            "(() => { const e = document.querySelector(%s);"
            " if (!e) return null; const r = e.getBoundingClientRect();"
            " return JSON.stringify({x: r.left, y: r.top, width: r.width, height: r.height}); })()"
            % json.dumps(selector))
        return json.loads(raw) if raw else None

    def mouse_move(self, x: float, y: float) -> None:
        self.cdp.send("Input.dispatchMouseEvent",
                      {"type": "mouseMoved", "x": x, "y": y}, self.session_id)

    def press_key(self, key: str, code: str, key_code: int) -> None:
        for kind in ("keyDown", "keyUp"):
            self.cdp.send("Input.dispatchKeyEvent",
                          {"type": kind, "key": key, "code": code,
                           "windowsVirtualKeyCode": key_code}, self.session_id)

    def close(self) -> None:
        self.cdp.send("Target.closeTarget", {"targetId": self.target_id})


def wait_settled(page: Page, extra_ms: int) -> None:
    """Let the network go quiet, then wait explicitly for async renderers.

    Charts and canvas need 2-4s after the last response. A screenshot of a
    half-rendered chart generates a false finding, which costs more than the
    wait does.
    """
    page.cdp.drain(1.5)
    page.evaluate("document.fonts && document.fonts.ready", await_promise=True)
    time.sleep(extra_ms / 1000)


def reveal_pass(page: Page) -> None:
    """Scroll the whole document, then return to the top, before probing.

    Two defect classes hide behind a page that was never scrolled, and both have
    been misreported as real findings: a scroll-reveal system leaves every band
    below the fold at opacity 0, so a load-time capture reads as a blank page;
    and `loading="lazy"` images have naturalWidth 0 until they enter the
    viewport, so an image probe reports five of eight as broken.
    """
    page.evaluate(REVEAL_JS, await_promise=True)


def prove_settled(page: Page, timeout_ms: int = 5000) -> int:
    """Drain running animations, then RETURN how many were still running.

    Draining is not the point; the returned count is. A gate that samples during
    an entrance animation reports precise, confident, wrong numbers — on a real
    run a 400ms-after-scroll axe pass read a `#E85A2A` accent as `#6a2d18` and
    reported a surface getting worse after a fix that provably removed its
    failures. Any count above zero invalidates the colour numbers in that row.

    Obscura does not execute CSS animations or transitions, so under it this
    returns 0 whatever the page declares. A zero here is the absence of a signal
    rather than proof of settling, which is what the run summary says.
    """
    v = page.evaluate(SETTLE_JS % timeout_ms, await_promise=True)
    # Obscura returns JSON numbers as floats, so this is a number check, not an
    # int check — `isinstance(v, int)` reads a perfectly good 0.0 as a failure.
    return int(v) if isinstance(v, (int, float)) else -1


# The probe roster, run one at a time. runAll() remains probes.js's contract
# and the analysis scripts read the same shape — but a probe that throws or
# overruns the CDP socket now costs its own key instead of the whole review.
# Measured before this existed: probeTextOverlap took 26.8s on a 12-slide deck,
# the 30s socket timed out mid-frame, and the run died on its THIRD viewport with
# a TimeoutError traceback — no probes written, two captures orphaned, and
# nothing in the output naming the probe responsible.
PROBE_ROSTER = [
    # Capability first, because every probe after it may consult the result, and
    # a reviewer reading any zero below needs to know which channels answered.
    ("capability", "initRun"),
    ("settled", "probeAnimationSettled"),
    ("stranded", "probeStrandedElements"),
    ("contrast", "probeContrast"),
    ("overflow", "probeOverflow"),
    ("images", "probeImages"),
    ("targets", "probeTargets"),
    ("semantics", "probeSemantics"),
    ("focus", "probeFocusStyles"),
    ("layout", "probeLayoutIntegrity"),
    ("tokens", "probeUnconsumedTokens"),
    ("styles", "dumpStyles"),
]


def run_probes(page: Page, tag: str) -> dict:
    """runAll(), one probe per round trip, with failures named rather than lost."""
    probes: dict = {
        "url": page.evaluate("location.href"),
        "viewport": json.loads(page.evaluate(
            "JSON.stringify({width:innerWidth,height:innerHeight,dpr:devicePixelRatio})") or "{}"),
        "prefersReducedMotionSupported": page.evaluate(
            "matchMedia('(prefers-reduced-motion: reduce)').media !== 'not all'"),
    }
    failed: list[str] = []
    for key, fn in PROBE_ROSTER:
        started = time.time()
        try:
            raw = page.evaluate(f"JSON.stringify(window.__designReviewProbes.{fn}())")
            probes[key] = json.loads(raw) if raw else None
            if probes[key] is None:
                failed.append(f"{fn}: returned nothing")
        except Exception as e:                        # socket timeout, closed, decode
            probes[key] = None
            failed.append(f"{fn}: {type(e).__name__} after {time.time() - started:.0f}s")
            if not page.recover():
                probes["probeErrors"] = failed + [
                    "page recovery failed — remaining probes NOT RUN (this is not clean)"]
                return probes
            try:
                page.evaluate(PROBES_JS.read_text())
                reveal_pass(page)
                prove_settled(page)
            except Exception as e2:
                probes["probeErrors"] = failed + [
                    f"re-injection failed ({type(e2).__name__}) — remaining probes NOT RUN"]
                return probes
            # Everything measured from here came off a re-loaded document.
            probes.setdefault("reloadedAfter", []).append(fn)
    if failed:
        # NOT the same as a probe that ran and found nothing. Both the analysis
        # scripts and the reviewer need to tell "checked, clean" from "never ran".
        probes["probeErrors"] = failed
        print(f"  ! {tag}: {len(failed)} probe(s) did not run — recorded as null, "
              f"NOT as clean: {'; '.join(failed)}", file=sys.stderr)
    return probes


def capture_viewport(cdp: CDP, url, width, height, out: Path, settle_ms: int,
                     tile: bool, dpr: int):
    page = Page(cdp, width, height, dpr)

    page.goto(url)
    wait_settled(page, settle_ms)
    reveal_pass(page)
    still_running = prove_settled(page)

    tag = f"{width}x{height}"

    (out / "shots").mkdir(parents=True, exist_ok=True)
    (out / "probes").mkdir(parents=True, exist_ok=True)
    (out / "console").mkdir(parents=True, exist_ok=True)

    page.screenshot(out / "shots" / f"{tag}-fold.png")
    page.screenshot(out / "shots" / f"{tag}-full.png", full_page=True)

    page.evaluate(PROBES_JS.read_text())
    probes = run_probes(page, tag)
    (out / "probes" / f"{tag}.json").write_text(json.dumps(probes, indent=2))

    console = page.console_messages()
    failed = page.failed_requests()
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
            time.sleep(0.22)
            p = out / "tiles" / f"{tag}-tile-{idx:02d}.png"
            page.screenshot(p)
            tiles.append(p.name)
            offset += height
            idx += 1
        page.evaluate("window.scrollTo(0, 0)")

    errors = [m for m in console if m["type"] in ("error", "pageerror")]
    tokens = probes.get("tokens") or {}
    contrast = probes.get("contrast")
    settled = probes.get("settled") or {}
    overflow = probes.get("overflow") or {}
    semantics = probes.get("semantics") or {}
    capability = probes.get("capability") or {}

    # Every read below goes through a guard, because `run_probes()` writes None
    # on a probe failure precisely so a failure is not read as clean — and then
    # six keys here indexed it anyway. Measured 18 Aug 2026: the sharper version
    # of that bug was `probes["layout"]["rails"]["exceedsThreshold"]`, which
    # raised KeyError on the FIRST viewport of this skill's own eval fixture,
    # because probeSharedRails' early return omitted the key. One capture width,
    # two orphaned screenshots, a traceback instead of a review.
    #
    # A count that could not be taken is None here, never 0. `null` in the
    # manifest is the difference between "no failures" and "never measured", and
    # both the analysis scripts and the reviewer read this file.
    def count(seq, pred=None):
        if seq is None:
            return None
        try:
            return len([x for x in seq if pred(x)]) if pred else len(seq)
        except (TypeError, KeyError):
            return None

    result = {
        "viewport": tag,
        "dpr": dpr,
        "shots": {"fold": f"{tag}-fold.png", "full": f"{tag}-full.png"},
        "tiles": tiles,
        # Settling proof on an engine that runs animations. Obscura does not, so
        # a zero here means "no signal" — see prove_settled.
        "animationsRunningAtMeasure": still_running,
        "elementsBelowFullOpacity": settled.get("partiallyTransparentElements"),
        # The engine's stranded-entrance artifact, reported rather than mixed into
        # the geometry probes it would otherwise pollute.
        "strandedElementCount": (probes.get("stranded") or {}).get("count"),
        "consoleErrorCount": len(errors),
        "failedRequestCount": len(failed),
        "pageOverflowsHorizontally": overflow.get("pageOverflowsHorizontally"),
        "escapingElementCount": count(overflow.get("escaping")),
        # Four numbers, not one. The ACT Rules Format (W3C) names the states a
        # result may take — passed, failed, cantTell, untested, inapplicable —
        # and `cantTell` is the one a boolean gate destroys. axe-core does the
        # same thing under the name `incomplete`, and returns it for exactly this
        # case: "The background color could not be determined due to a
        # background image." An unresolved backdrop is not a pass and not a
        # failure, and on a 285-homepage scan, counting incompletes as failures
        # moved the reported failure rate to 97.9% — the size of the population a
        # pass/fail gate silently absorbs.
        "contrastFailureCount": (contrast or {}).get("failureCount") if isinstance(contrast, dict) else None,
        "contrastPassCount": (contrast or {}).get("passCount") if isinstance(contrast, dict) else None,
        "contrastCantTellCount": (contrast or {}).get("unresolvedCount") if isinstance(contrast, dict) else None,
        "contrastExamined": (contrast or {}).get("examined") if isinstance(contrast, dict) else None,
        "contrastGradientJudged": (contrast or {}).get("gradientJudgedCount") if isinstance(contrast, dict) else None,
        "contrastAssumedBackdrop": (contrast or {}).get("assumedBackdropCount") if isinstance(contrast, dict) else None,
        "layoutFindingCount": _layout_finding_count(probes.get("layout")),
        "layoutRootCauseCount": _layout_root_cause_count(probes.get("layout")),
        "componentTypeCount": ((probes.get("layout") or {}).get("inventory") or {}).get("distinctTypes"),
        "targetsBelowAA": count(probes.get("targets"), lambda t: t.get("belowAA")),
        "heavyCropImages": count(probes.get("images"), lambda i: i.get("heavyCrop")),
        # WCAG 2.4.2 Page Titled is Level A and is the cheapest gate in the set.
        "missingTitle": (not (semantics.get("title") or "").strip()) if probes.get("semantics") is not None else None,
        "unconsumedTokenCount": count((tokens.get("unconsumed") or None), lambda t: "token" in t),
        # The headline honesty number. How many measurement channels this engine
        # would not answer on this page, so no zero above can be mistaken for a
        # measurement that was taken.
        "unreadableChannelCount": capability.get("unreadableCount"),
        "unreadableChannels": capability.get("unreadable"),
        "probesNotRun": probes.get("probeErrors"),
    }
    page.close()
    return result


def capture_states(cdp: CDP, url, out: Path, settle_ms: int, selectors: list[str]):
    """Stage interaction states deliberately.

    Hover contaminates a selected-state capture unless the pointer is moved away
    first, so each state is captured in isolation.
    """
    page = Page(cdp, 1280, 900, DPR_DETAIL)
    page.goto(url)
    wait_settled(page, settle_ms)
    (out / "states").mkdir(parents=True, exist_ok=True)

    captured: list[str] = []
    if not selectors:
        selectors = ["button", "a[href]", "input", "[role='button']"]

    for sel in selectors:
        box = page.box_of(sel)
        if not box or box["width"] <= 0 or box["height"] <= 0:
            continue
        safe = sel.replace("[", "_").replace("]", "_").replace("'", "").replace(" ", "")[:30]

        page.evaluate("document.querySelector(%s).scrollIntoView({block: 'center'})"
                      % json.dumps(sel))
        time.sleep(0.15)
        rest = page.box_of(sel)
        if not rest:
            continue
        clip = {"x": rest["x"], "y": rest["y"], "width": rest["width"], "height": rest["height"]}

        page.mouse_move(0, 0)
        time.sleep(0.15)
        p = out / "states" / f"{safe}-rest.png"
        page.screenshot(p, clip=clip)
        captured.append(p.name)

        page.mouse_move(rest["x"] + rest["width"] / 2, rest["y"] + rest["height"] / 2)
        time.sleep(0.4)  # let the transition finish
        p = out / "states" / f"{safe}-hover.png"
        page.screenshot(p, clip=clip)
        captured.append(p.name)

        page.press_key("Tab", "Tab", 9)
        time.sleep(0.2)
        p = out / "states" / f"{safe}-focus-page.png"
        page.screenshot(p)
        captured.append(p.name)

    # Reduced motion and print are two at-rest checks that catch content which
    # only exists because an animation ran. Obscura accepts
    # Emulation.setEmulatedMedia and then ignores it — matchMedia and the cascade
    # do not change — so capturing here would write the ordinary rendering under
    # a name claiming otherwise. Record the gap instead: a review showing a
    # screen-media screenshot named `page-print.png` is worse than one saying the
    # check did not run.
    skipped = [
        "page-reduced-motion.png (Obscura cannot emulate prefers-reduced-motion)",
        "page-print.png (Obscura cannot emulate print media)",
    ]

    page.close()
    return captured, skipped


def _layout_finding_count(L):
    """Layout-integrity findings, summed. A probe nobody reads is the failure
    this whole section exists to correct, so it surfaces in the run summary.

    `dividerProximity` was that failure, in this function: `probes.js` ran it,
    `layout-integrity.md` documented it, and no consumer anywhere added it up —
    so a surface whose only layout defect was a divider gutter printed
    `layoutFindingCount: 0` on the first line a reviewer reads. Corroborating
    evidence that it was never wired: its three fixtures were the only orphans in
    the eval set.

    Every read is `.get()` with a default now. A probe that did not run
    contributes nothing rather than raising, and `probesNotRun` in the summary is
    where its absence is recorded.
    """
    if not L:
        return None
    n = (len(L.get("shapeMismatch") or []) + len(L.get("columnDrift") or []) +
         len(L.get("columnHeaderAlignment") or []) + len(L.get("touchingHeadings") or []) +
         len(L.get("textOverlap") or []) + len(L.get("deadSpace") or []) +
         len((L.get("columnVoids") or {}).get("voids") or []) +
         len((L.get("implicitTracks") or {}).get("spilledRows") or []) +
         len((L.get("implicitTracks") or {}).get("emptyCells") or []) +
         len((L.get("dividerProximity") or {}).get("violations") or []) +
         len((L.get("dividerProximity") or {}).get("clipped") or []) +
         len((L.get("affordance") or {}).get("unactionableRows") or []) +
         len((L.get("affordance") or {}).get("pointerCursorNotFocusable") or []) +
         len(L.get("tokenOverload") or []))
    if (L.get("rails") or {}).get("exceedsThreshold"):
        n += 1
    return n


def _layout_root_cause_count(L):
    """The same findings, clustered by mechanism and by the component they sit in.

    A raw geometry count inflates badly, and the size of the inflation is
    published: ReDeCheck (Walsh, Kapfhammer & McMinn, ISSTA 2017) reported **147
    small-range findings on one page that collapsed to a single underlying
    failure**, and needed 4.2 viewport inspections per real failure across 26
    live pages. This skill measured the same shape independently on one
    14-screen surface: 2 real, 35 false.

    So the summary carries both numbers. The raw count says how much geometry
    fired; this one estimates how many distinct things are actually wrong, which
    is the number a reviewer should act on. Clustering is by
    `{mechanism, nearest component ancestor}` — deliberately coarse, because the
    failure being prevented is a hundred rows for one bug, not a slightly wrong
    cluster boundary.
    """
    if not L:
        return None

    def component_of(selector):
        """The nearest ancestor in the selector path that looks like a component.

        A repeated defect names a different `:nth-of-type` every time while the
        component class stays put, so truncating at the last class-bearing
        segment is what makes fourteen rows of one bug into one row.
        """
        if not selector:
            return "?"
        segments = [s.strip() for s in str(selector).split(">") if s.strip()]
        for seg in reversed(segments):
            if "." in seg:
                # Drop the positional suffix; keep the classes.
                return seg.split(":")[0]
        return segments[-1].split(":")[0] if segments else "?"

    keys = set()

    def add(mechanism, rows, *fields):
        for row in rows or []:
            if not isinstance(row, dict):
                keys.add((mechanism, "?"))
                continue
            sel = next((row.get(f) for f in fields if row.get(f)), None)
            keys.add((mechanism, component_of(sel)))

    add("shape-mismatch", L.get("shapeMismatch"), "selector", "group", "el")
    add("column-drift", L.get("columnDrift"), "selector", "group", "el")
    add("header-alignment", L.get("columnHeaderAlignment"), "selector", "el", "header")
    add("touching-headings", L.get("touchingHeadings"), "selector", "el", "second")
    add("text-overlap", L.get("textOverlap"), "a", "selector", "el")
    add("dead-space", L.get("deadSpace"), "selector", "el", "section")
    add("column-void", (L.get("columnVoids") or {}).get("voids"), "selector", "el", "section")
    add("implicit-track", (L.get("implicitTracks") or {}).get("spilledRows"), "selector", "grid", "el")
    add("empty-cell", (L.get("implicitTracks") or {}).get("emptyCells"), "selector", "el")
    add("divider-gutter", (L.get("dividerProximity") or {}).get("violations"), "el", "selector")
    add("divider-clipped", (L.get("dividerProximity") or {}).get("clipped"), "el", "selector")
    add("unactionable-row", (L.get("affordance") or {}).get("unactionableRows"), "selector", "el")
    add("pointer-not-focusable", (L.get("affordance") or {}).get("pointerCursorNotFocusable"), "selector", "el")
    add("token-overload", L.get("tokenOverload"), "token", "selector")
    if (L.get("rails") or {}).get("exceedsThreshold"):
        keys.add(("rail-disagreement", "page"))
    return len(keys)


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
    ap.add_argument("--settle-ms", type=int, default=2500, help="Extra wait after the network quietens, for async renderers.")
    ap.add_argument("--dpr", type=int, default=DPR_OVERVIEW, help="1 for 'what a user sees', 2-3 for defect inspection.")
    ap.add_argument("--tile", action="store_true", help="Tile long pages into viewport chunks.")
    ap.add_argument("--states", action="store_true", help="Capture staged interaction states.")
    ap.add_argument("--state-selectors", help="Comma-separated selectors to stage.")
    ap.add_argument("--motion", action="store_true", help="Unavailable: Obscura does not execute CSS animations.")
    ap.add_argument("--force", action="store_true",
                    help="Overwrite a workdir that already holds a run. Discards its before-captures.")
    ap.add_argument("--cdp-port", type=int, help="Attach to an `obscura serve` already running on this port "
                                                 "instead of starting one.")
    ap.add_argument("--worklist", help="Workdir holding worklist.md. Marks this surface's "
                                       "gates and render cells done once capture succeeds.")
    ap.add_argument("--surface", help="This surface's name in the worklist (default: --url).")
    args = ap.parse_args()

    if args.motion:
        sys.exit(
            "ERROR: --motion is unavailable under Obscura. It does not execute CSS\n"
            "animations or transitions — a declared `animation: fade 3s` never advances\n"
            "and document.getAnimations() reports none — so the frames would be N copies\n"
            "of one still. Report the motion pass as not performed rather than reading a\n"
            "mid-flight defect off identical frames."
        )

    if args.url.startswith("file://"):
        print("WARNING: file:// breaks module scripts, fetches and some fonts. "
              "Serve over HTTP instead (python3 -m http.server).", file=sys.stderr)

    out = Path(args.out).resolve()
    # A second run over the same workdir used to overwrite probes/, shots/ and
    # manifest.json in place, which destroys the before-evidence that a fix has
    # to be scored against. `capture-protocol.md` requires capturing the before
    # BEFORE editing; nothing enforced it.
    existing = out.exists() and any(out.glob("probes/*.json"))
    if existing and not args.force:
        sys.exit(
            f"ERROR: {out} already holds a completed run.\n"
            "Overwriting it destroys the before-captures a fix has to be scored\n"
            "against, and a fix you cannot see in new evidence is unresolved.\n"
            "Either write the second run somewhere else (--out <dir>-after), or\n"
            "pass --force if you genuinely mean to discard the first one."
        )
    out.mkdir(parents=True, exist_ok=True)

    if args.viewports:
        widths = [int(w.strip()) for w in args.viewports.split(",")]
        sizes = [(w, dict(DEFAULT_VIEWPORTS).get(w, 900)) for w in widths]
    else:
        sizes = DEFAULT_VIEWPORTS

    manifest = {"url": args.url, "viewports": [], "states": [], "statesSkipped": [], "motion": []}

    port = args.cdp_port or random.randint(9200, 9499)
    server = None if args.cdp_port else start_obscura(port)
    cdp = CDP(port)

    try:
        for w, h in sizes:
            print(f"  capturing {w}x{h} ...", file=sys.stderr)
            manifest["viewports"].append(
                capture_viewport(cdp, args.url, w, h, out, args.settle_ms, args.tile, args.dpr))

        if args.states:
            print("  staging interaction states ...", file=sys.stderr)
            sels = [s.strip() for s in args.state_selectors.split(",")] if args.state_selectors else []
            manifest["states"], manifest["statesSkipped"] = capture_states(
                cdp, args.url, out, args.settle_ms, sels)
    finally:
        cdp.close()
        if server:
            server.kill()

    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))

    print(f"\nCaptured to {out}")
    print("\nPer viewport:")
    for v in manifest["viewports"]:
        flags = []
        if v.get("animationsRunningAtMeasure"):
            flags.append(f"NOT SETTLED ({v['animationsRunningAtMeasure']} animations running)")
        if v.get("pageOverflowsHorizontally"):
            flags.append("H-OVERFLOW")
        if v.get("missingTitle"):
            flags.append("NO <title> (WCAG 2.4.2, Level A)")
        if v.get("consoleErrorCount"):
            flags.append(f"{v['consoleErrorCount']} console errors")
        # Three numbers on one line, because two of them used to be invisible.
        # `cantTell` is W3C ACT's name for a target the rule applied to and could
        # not resolve. Printing it beside the failures is what stops an
        # unresolvable backdrop being read either as a pass or as a Blocker.
        ct = v.get("contrastCantTellCount")
        flags.append(
            f"contrast {v.get('contrastFailureCount')} fail"
            f" / {v.get('contrastPassCount')} pass"
            f" / {ct} cantTell"
            f" of {v.get('contrastExamined')} examined"
            + (f" ({v['contrastGradientJudged']} judged against gradient stops)"
               if v.get("contrastGradientJudged") else ""))
        if v.get("targetsBelowAA"):
            flags.append(f"{v['targetsBelowAA']} targets <24px")
        if v.get("heavyCropImages"):
            flags.append(f"{v['heavyCropImages']} heavy-crop images")
        if v.get("layoutFindingCount"):
            # Raw beside clustered. ReDeCheck measured 147 geometry findings on one
            # page that were one bug; the clustered number is the one to act on.
            flags.append(f"{v['layoutFindingCount']} layout findings"
                         f" ({v.get('layoutRootCauseCount')} root causes)")
        if v.get("unconsumedTokenCount"):
            flags.append(f"{v['unconsumedTokenCount']} declared-but-unread tokens")
        if v.get("strandedElementCount"):
            flags.append(f"{v['strandedElementCount']} engine-stranded elements (excluded from geometry)")
        if v.get("probesNotRun"):
            flags.append(f"!! {len(v['probesNotRun'])} probe(s) DID NOT RUN — not clean")
        print(f"  {v['viewport']:>10}  {' · '.join(str(f) for f in flags)}")

    if manifest["statesSkipped"]:
        print("\nNot captured:")
        for s in manifest["statesSkipped"]:
            print(f"  {s}")

    # The unmeasurable population, printed once rather than per row. This is the
    # generalisation of the rule the skill previously applied to one layer only:
    # a check whose pass and cannot-run look identical must report which it is.
    caps = [v.get("unreadableChannels") for v in manifest["viewports"]
            if v.get("unreadableChannels")]
    if caps:
        merged = sorted(set(c for lst in caps for c in lst))
        print(f"\n{len(merged)} measurement channel(s) this engine would not answer:")
        print(f"  {', '.join(merged)}")
        print("Every one is a check whose clean result would be indistinguishable from")
        print("a real one. Where a fallback exists the value is tagged `declared` in")
        print("probes/*.json `styles`; where none exists the value is null, never 0.")
        print("Carry this list into the report's 'Not checked' line — it is not")
        print("something to rediscover per review.")

    print("\nObscura does not run CSS animations or transitions, so")
    print("animationsRunningAtMeasure is 0 on every row whatever the page declares.")
    print("That zero is the absence of a signal, not proof the surface had settled —")
    print("any finding that turns on entrance timing needs a different engine.")

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
