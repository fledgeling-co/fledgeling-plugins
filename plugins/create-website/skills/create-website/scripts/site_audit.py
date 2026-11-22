#!/usr/bin/env python3
"""Audit a built website directory before it is shown or deployed.

    python3 site_audit.py site/                     # exit 0 clean, 1 on any error
    python3 site_audit.py site/ --deploy            # also fail on review tools left in the build
    python3 site_audit.py site/ --private private.txt   # fail on any listed string in visible text
    python3 site_audit.py site/ --json report.json

Static checks on the files, so they run before a browser is involved and fail on what a capture
would show as "looks fine":

- every local src, href, srcset, poster and CSS url() resolves to a file;
- every <img> has alt text (empty alt is allowed for decoration);
- a <video> that autoplays is muted and playsinline and has a poster; a looping one has a pause
  control on the page (WCAG 2.2.2, Level A, for motion past five seconds); width and height
  attributes are flagged for a look, because a pair that disagreed with the CSS aspect ratio gave a
  tall zoomed crop on a phone; a large file has a smaller phone source listed first;
- a <canvas> is either hidden from assistive technology as decoration or named, since an unnamed
  canvas is an empty box to a screen reader;
- a page with CSS animation, transitions on transform, GSAP, ScrollTrigger, Lenis or three.js
  handles prefers-reduced-motion somewhere it can take effect;
- a page that creates a WebGL context checks for it and has a non-WebGL path;
- with --deploy, no element or comment marked as a review tool (data-review-tool, class
  "review-tool", or <!-- review-tool -->) remains: a control that lets the person compare options
  is a review tool and never ships;
- with --private, none of the listed strings appears in the visible text of any page, read from the
  text a person sees and not from the page source, where a search once matched restricted figures
  inside font weights and pixel values.

ERROR fails the run. WARN is a prompt to read the line and decide.
"""
import argparse
import json
import os
import re
import sys
from html.parser import HTMLParser
from urllib.parse import unquote, urlparse

VIDEO_BYTES_WARN = 8 * 1024 * 1024
MOTION_JS = re.compile(r"\b(gsap|ScrollTrigger|Lenis|THREE\.|WebGLRenderer|requestAnimationFrame|animate\(\s*\[)", re.I)
MOTION_CSS = re.compile(r"(@keyframes|animation\s*:|animation-name\s*:|animation-timeline\s*:|view-timeline|scroll-timeline)", re.I)
REDUCED = re.compile(r"prefers-reduced-motion", re.I)
WEBGL = re.compile(r"(getContext\(\s*['\"](webgl2?|experimental-webgl)['\"]|WebGLRenderer|new\s+THREE\.WebGLRenderer)")
WEBGL_GUARD = re.compile(r"(WebGLRenderingContext|WebGL2RenderingContext|isWebGLAvailable|isWebGL2Available|webglcontextlost|catch\s*\(|data-fallback|\.fallback|if\s*\(\s*!\s*(gl|ctx|context|renderer)\b|(gl|ctx|context)\s*===?\s*null)", re.I)
REVIEW_COMMENT = re.compile(r"<!--\s*review-tool", re.I)
CSS_URL = re.compile(r"url\(\s*['\"]?([^'\")]+)['\"]?\s*\)")


class Page(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.refs, self.imgs, self.videos, self.review = [], [], [], []
        self.text, self.inline_js, self.inline_css = [], [], []
        self.canvases, self.buttons = [], []
        self._button = None
        self._skip = 0
        self._video = None
        self._in = None

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag in ("script", "style"):
            self._skip += 1
            self._in = tag
            if tag == "script" and a.get("src"):
                self.refs.append(("script src", a["src"]))
        for k in ("src", "href", "poster"):
            if k in a and a[k] and not (tag == "script" and k == "src"):
                if tag == "a" and k == "href":
                    continue
                self.refs.append((f"{tag} {k}", a[k]))
        if a.get("srcset"):
            for part in a["srcset"].split(","):
                url = part.strip().split(" ")[0]
                if url:
                    self.refs.append((f"{tag} srcset", url))
        if tag == "img":
            self.imgs.append(a)
        if tag == "canvas":
            self.canvases.append(a)
        if tag == "button":
            self._button = [a.get("aria-label") or "", a.get("title") or ""]
            self.buttons.append(self._button)
        if tag == "video":
            self._video = {"attrs": a, "sources": []}
            self.videos.append(self._video)
        if tag == "source" and self._video is not None:
            self._video["sources"].append(a)
        cls = (a.get("class") or "").split()
        if "data-review-tool" in a or "review-tool" in cls:
            self.review.append(f"<{tag} {' '.join(k for k in a)}>")

    def handle_endtag(self, tag):
        if tag in ("script", "style") and self._skip:
            self._skip -= 1
            self._in = None
        if tag == "video":
            self._video = None
        if tag == "button":
            self._button = None

    def handle_data(self, data):
        if self._button is not None:
            self._button.append(data)
        if self._skip:
            (self.inline_js if self._in == "script" else self.inline_css).append(data)
        elif data.strip():
            self.text.append(data.strip())

    def handle_comment(self, data):
        if data.strip().lower().startswith("review-tool"):
            self.review.append("<!-- review-tool -->")


def local_path(root, page_dir, ref):
    u = urlparse(ref)
    if u.scheme in ("http", "https", "data", "mailto", "tel", "javascript") or ref.startswith("//") or ref.startswith("#"):
        return None
    p = unquote(u.path)
    if not p:
        return None
    base = root if p.startswith("/") else page_dir
    full = os.path.normpath(os.path.join(base, p.lstrip("/")))
    if os.path.isdir(full):
        full = os.path.join(full, "index.html")
    return full


def audit(root, deploy=False, private=()):
    errors, warns = [], []
    files = []
    root = os.path.abspath(root)
    for d, dirs, fs in os.walk(root):
        # Skip hidden directories and dependencies under the site root, never the root's own path.
        dirs[:] = [x for x in dirs if not x.startswith(".") and x != "node_modules"]
        files += [os.path.join(d, f) for f in fs]
    js_text = "\n".join(open(f, encoding="utf-8", errors="replace").read() for f in files if f.endswith((".js", ".mjs")))
    css_text = "\n".join(open(f, encoding="utf-8", errors="replace").read() for f in files if f.endswith(".css"))
    for f in files:
        if f.endswith(".css"):
            for ref in CSS_URL.findall(open(f, encoding="utf-8", errors="replace").read()):
                p = local_path(root, os.path.dirname(f), ref)
                if p and not os.path.exists(p):
                    errors.append(f"{os.path.relpath(f, root)}: url({ref}) does not resolve")
    pages = [f for f in files if f.endswith(".html")]
    if not pages:
        errors.append("no .html files found")
    for f in pages:
        rel = os.path.relpath(f, root)
        raw = open(f, encoding="utf-8", errors="replace").read()
        pg = Page()
        pg.feed(raw)
        for kind, ref in pg.refs:
            p = local_path(root, os.path.dirname(f), ref)
            if p and not os.path.exists(p):
                errors.append(f"{rel}: {kind} '{ref}' does not resolve")
        for ref in CSS_URL.findall("\n".join(pg.inline_css)):
            p = local_path(root, os.path.dirname(f), ref)
            if p and not os.path.exists(p):
                errors.append(f"{rel}: inline url({ref}) does not resolve")
        for img in pg.imgs:
            if "alt" not in img:
                errors.append(f"{rel}: <img src='{img.get('src', '?')}'> has no alt attribute")
        for v in pg.videos:
            a = v["attrs"]
            name = a.get("src") or (v["sources"][0].get("src") if v["sources"] else "?")
            if "autoplay" in a:
                for need in ("muted", "playsinline"):
                    if need not in a:
                        errors.append(f"{rel}: autoplaying <video {name}> lacks {need}; browsers refuse to autoplay it")
            if not a.get("poster"):
                errors.append(f"{rel}: <video {name}> has no poster; reduced motion and a refused play() show nothing")
            if "width" in a or "height" in a:
                warns.append(f"{rel}: <video {name}> sets width/height; keep them only if they match the clip's aspect ratio "
                             "and CSS sets height:auto, since a pair that fought the CSS ratio cropped the phone view once")
            if "loading" in a and a.get("loading") == "lazy" and "autoplay" in a:
                warns.append(f"{rel}: autoplaying <video {name}> is lazy-loaded; a hero video's poster is the likely LCP and should load eagerly")
            labels = " ".join(" ".join(b) for b in pg.buttons).lower()
            if "loop" in a and "autoplay" in a and not re.search(r"\b(pause|stop|play)\b", labels):
                errors.append(f"{rel}: looping autoplay <video {name}> has no pause control; motion past five seconds needs one (WCAG 2.2.2, Level A)")
            sizes = []
            for s in v["sources"] or [{"src": a.get("src", "")}]:
                p = local_path(root, os.path.dirname(f), s.get("src", "") or "")
                if p and os.path.exists(p):
                    sizes.append(os.path.getsize(p))
            if sizes and max(sizes) > VIDEO_BYTES_WARN:
                warns.append(f"{rel}: <video {name}> is {max(sizes) / 1e6:.1f} MB; re-encode it or check the size budget")
            if sizes and max(sizes) > VIDEO_BYTES_WARN / 2 and not (v["sources"] and v["sources"][0].get("media")):
                warns.append(f"{rel}: <video {name}> has no smaller phone source first (a <source media=...>)")
        for c in pg.canvases:
            if c.get("aria-hidden") != "true" and not (c.get("aria-label") or c.get("aria-labelledby") or c.get("role")):
                warns.append(f"{rel}: <canvas id='{c.get('id', '?')}'> is neither aria-hidden decoration nor named; "
                             "name it and put its controls and information in HTML beside it")
        page_js = "\n".join(pg.inline_js)
        page_css = "\n".join(pg.inline_css)
        uses_motion = MOTION_JS.search(page_js) or MOTION_CSS.search(page_css)
        linked = any(k.startswith(("script src", "link href")) for k, _ in pg.refs)
        if linked:
            uses_motion = uses_motion or MOTION_JS.search(js_text) or MOTION_CSS.search(css_text)
        if uses_motion and not (REDUCED.search(page_js) or REDUCED.search(page_css) or REDUCED.search(js_text) or REDUCED.search(css_text)):
            errors.append(f"{rel}: animates but never reads prefers-reduced-motion")
        if WEBGL.search(page_js) or (linked and WEBGL.search(js_text)):
            if not (WEBGL_GUARD.search(page_js) or WEBGL_GUARD.search(js_text) or "data-fallback" in raw):
                errors.append(f"{rel}: creates a WebGL context with no availability check or fallback path")
        if deploy and (pg.review or REVIEW_COMMENT.search(raw)):
            errors.append(f"{rel}: review tool still in a deploy build: {', '.join(pg.review) or 'review-tool comment'}")
        visible = " ".join(pg.text)
        for s in private:
            if s and s in visible:
                errors.append(f"{rel}: private string '{s}' appears in the visible text")
        for m in re.finditer(r"<script[^>]+src=['\"](https?://[^'\"]+)['\"]", raw):
            if not re.search(r"@\d+\.\d+\.\d+|/\d+\.\d+\.\d+/", m.group(1)):
                warns.append(f"{rel}: external script without an exact version: {m.group(1)}")
    return {"pages": len(pages), "errors": errors, "warnings": warns}


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    ap.add_argument("root")
    ap.add_argument("--deploy", action="store_true")
    ap.add_argument("--private", help="file of strings that must not appear in visible text, one per line")
    ap.add_argument("--json")
    a = ap.parse_args()
    private = []
    if a.private:
        private = [ln.strip() for ln in open(a.private, encoding="utf-8") if ln.strip() and not ln.startswith("#")]
    r = audit(a.root, a.deploy, private)
    for e in r["errors"]:
        print("ERROR", e)
    for w in r["warnings"]:
        print("WARN ", w)
    print(f"RESULT: {r['pages']} page(s), {len(r['errors'])} error(s), {len(r['warnings'])} warning(s)")
    if a.json:
        json.dump(r, open(a.json, "w"), indent=2)
    return 1 if r["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
