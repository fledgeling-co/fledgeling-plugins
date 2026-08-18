#!/usr/bin/env python3
"""banner_sheet.py — score a banner commission, then prove the score is about this banner.

The sibling of create-mac-icon's `audit_sheet.py`, and it exists because the two
halves of this marketplace's brand were gated very unequally. An icon gets a
direction catalogue, three engines, a 12-point rubric, a contact sheet at six
sizes, a fidelity loop and a blind panel. A banner got five mechanical
assertions from `render_banner.py` and nobody looking at the result.

That asymmetry let three banners ship wrong, all of them passing every assertion
made of them, because none of those assertions is about whether the banner is
any good or whether it agrees with its siblings:

  resume-session      1600x520, which is the layout size at deviceScaleFactor 1,
                      so it is half resolution and soft on every retina display.
  create-test-suite   3200x840 from a 1600x420 layout, against the family's 520.
  whats-left          3200x840, same cause.

And a fourth defect that no size check would ever have found: create-test-suite
and whats-left set their wordmarks in `Iowan Old Style` and `Avenir Next`, which
are local macOS system faces with no web font linked. Those two banners are not
reproducible. Re-render them on a machine without those fonts, or in CI, and the
wordmark silently becomes Georgia or a generic sans. The banner still renders,
still passes, and is a different banner.

Two subcommands, and as with the icon sheet the second is the point.

    python3 banner_sheet.py sheet  <plugin-assets-dir>
    python3 banner_sheet.py check  <plugin-assets-dir>
    python3 banner_sheet.py family <repo-root>

`sheet` renders the banner at the sizes a person actually meets it (full, README
width, catalogue-card width, thumbnail) plus a 1:1 crop of the left third where
the icon and wordmark sit, and writes `banner-audit.html` from those renders.
`check` is the mechanical half. `family` builds one sheet of every banner in the
repo stacked at README width, which is the only view in which wordmark and
register drift across the set is visible at all.

Rendering needs no browser: banner.png already exists, and every display size is
a downscale of it. That is deliberate. The icon pipeline learned that driving a
headless engine is where silent failures live, and a resize cannot fail silently.
"""

from __future__ import annotations

import argparse
import hashlib
import html.parser
import json
import pathlib
import re
import sys

BANNER_W = 3200
BANNER_H = 1040

# The sizes a banner is actually seen at, as CSS pixels of displayed width.
#   1600  the layout's own logical width, so 1:1 with how it was composed
#    900  a GitHub README's content column, which is where most people meet it
#    400  the catalogue card on skills.fledgeling.app
#    200  a thumbnail, where only the icon and the wordmark's shape survive
DISPLAY_WIDTHS = (1600, 900, 400, 200)

RUBRIC_TOTAL = 12
RUBRIC_BAR = 10

# A banner and the icon it displays, produced by the same build, land within
# seconds of each other. A stale banner is days behind. Anything inside this
# window is treated as the same build rather than as drift.
SAME_BUILD_SECONDS = 600

RUBRIC = [
    (1, "Exactly 3200x1040, from a 1600x520 layout at deviceScaleFactor 2", True),
    (2, "The plugin's real icon asset, referenced rather than redrawn", True),
    (3, "The wordmark is set in a linked web font, not a local system face", True),
    (4, "Ground register agrees with the icon it sits beside", False),
    (5, "One warm accent, carried from the icon's own accent constant", False),
    (6, "Composition derived from the icon's build script, not eyeballed from a sibling", False),
    (7, "One essence line, no em dash", True),
    (8, "Nothing overflows the frame", False),
    (9, "Wordmark and essence line both legible at 900px", False),
    (10, "Wordmark legible at 400px", False),
    (11, "No element illegibly overlapping another", False),
    (12, "banner-src retained, so the banner stays editable", True),
]


def load_pil():
    try:
        from PIL import Image
    except ImportError:
        return None
    return Image


def sha256_of(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def png_size(path: pathlib.Path) -> tuple[int, int] | None:
    """Width and height out of the IHDR chunk, so a size check needs no PIL."""
    if not path.exists():
        return None
    with path.open("rb") as fh:
        head = fh.read(24)
    if len(head) < 24 or head[1:4] != b"PNG":
        return None
    return int.from_bytes(head[16:20], "big"), int.from_bytes(head[20:24], "big")


class SrcRefs(html.parser.HTMLParser):
    """Every <img src> and every stylesheet href in a banner source."""

    def __init__(self):
        super().__init__()
        self.imgs: list[str] = []
        self.links: list[str] = []

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "img" and a.get("src"):
            self.imgs.append(a["src"])
        if tag == "link" and a.get("href"):
            self.links.append(a["href"])


def find_src(base: pathlib.Path) -> pathlib.Path | None:
    for name in ("banner-src.html", "banner-src.svg"):
        if (base / name).exists():
            return base / name
    return None


# A face is reproducible when it arrives with the document. Anything else is the
# rendering machine's furniture, and two banners in this repo are already
# unreproducible because of it.
LOCAL_ONLY_FACES = re.compile(
    r"\b(Iowan Old Style|Palatino|Avenir|Segoe UI|Helvetica Neue|Lucida|Baskerville|Optima|Futura|Gill Sans)\b",
    re.I,
)


def font_evidence(src: pathlib.Path) -> tuple[list[str], list[str]]:
    """(web faces the source actually loads, local-only faces it names)."""
    text = src.read_text(encoding="utf-8", errors="replace")
    web = sorted({
        f.replace("+", " ")
        for m in re.finditer(r"fonts\.googleapis\.com[^\"']*", text)
        for f in re.findall(r"family=([^&:\"']+)", m.group(0))
    })
    if re.search(r"@font-face", text) and re.search(r"url\(\s*['\"]?data:", text):
        web.append("(inlined @font-face)")
    local = sorted(set(LOCAL_ONLY_FACES.findall(text)))
    return web, local


def visible_text(src: pathlib.Path) -> str:
    """Rough strip of markup, enough to count em dashes in copy rather than code."""
    text = src.read_text(encoding="utf-8", errors="replace")
    text = re.sub(r"<(script|style)\b.*?</\1>", " ", text, flags=re.S | re.I)
    return re.sub(r"<[^>]+>", " ", text)


PLACEHOLDER_REC = (
    "<strong>Recommendation.</strong> No verdict written yet. Put it in "
    "<code>banner-verdict.md</code> beside this file: does this banner ship, and "
    "what are its known liabilities? That file is a sidecar precisely so that "
    "re-rendering this sheet cannot destroy it. The rows above marked as needing "
    "an eye are the reason this is a sheet rather than a script's exit code."
)


def recommendation_html(base: pathlib.Path) -> str:
    """The human verdict, read from its sidecar so a re-render never clobbers it."""
    verdict = base / "banner-verdict.md"
    if not verdict.exists():
        return PLACEHOLDER_REC
    text = verdict.read_text(encoding="utf-8").strip()
    if not text:
        return PLACEHOLDER_REC
    paras = [p.strip().replace("\n", " ") for p in re.split(r"\n\s*\n", text) if p.strip()]
    body = "".join(f"<p>{p}</p>" for p in paras)
    return f"<strong>Recommendation.</strong>{body}"


# ------------------------------------------------------------------ sheet

def render_displays(base: pathlib.Path, Image) -> dict[str, str]:
    """Downscale banner.png to each display width, plus a 1:1 left-third crop."""
    out_dir = base / "banner-renders"
    out_dir.mkdir(exist_ok=True)
    banner = base / "banner.png"
    im = Image.open(banner).convert("RGBA")

    written = {}
    for w in DISPLAY_WIDTHS:
        h = round(im.height * w / im.width)
        path = out_dir / f"display-{w}.png"
        im.resize((w, h), Image.LANCZOS).save(path)
        written[f"display-{w}"] = path.name

    # The left third at 1:1 against the composed layout: icon plus wordmark, the
    # two things that have to survive. Cropped from the 2x master then halved, so
    # it is the same pixels a 1600px-wide viewer sees.
    crop = im.crop((0, 0, im.width // 3, im.height))
    crop = crop.resize((crop.width // 2, crop.height // 2), Image.LANCZOS)
    crop_path = out_dir / "crop-lockup.png"
    crop.save(crop_path)
    written["crop-lockup"] = crop_path.name

    icon = base / "icon.png"
    manifest = {
        "banner": banner.name,
        "banner_mtime": banner.stat().st_mtime,
        "icon_sha": sha256_of(icon) if icon.exists() else None,
        "source_size": [im.width, im.height],
        "displays": written,
    }
    (out_dir / "banner-manifest.json").write_text(json.dumps(manifest, indent=2) + "\n")
    return written


SHEET_CSS = """
:root{--ink:#17191c;--muted:#5e676f;--rule:#d7dde2;--ground:#f5f7f8;--surface:#fff;--bad:#c4622d;--ok:#3e6b54}
*{box-sizing:border-box}
body{margin:0;background:var(--ground);color:var(--ink);
  font:15px/1.6 "IBM Plex Sans",ui-sans-serif,system-ui,sans-serif}
.wrap{max-width:1240px;margin:0 auto;padding:48px 24px 96px}
h1{font-size:30px;letter-spacing:-.02em;margin:0 0 6px}
h2{font-size:19px;letter-spacing:-.01em;margin:44px 0 4px}
p.note{color:var(--muted);margin:0 0 22px;max-width:70ch}
.shot{background:var(--surface);border:1px solid var(--rule);border-radius:3px;
  padding:14px;margin:0 0 18px;overflow-x:auto}
.shot img{display:block;max-width:100%;height:auto}
.shot figcaption{color:var(--muted);font:12px/1.5 "IBM Plex Mono",ui-monospace,monospace;
  margin-top:10px}
table{border-collapse:collapse;width:100%;background:var(--surface);
  border:1px solid var(--rule);border-radius:3px;font-size:14px}
th,td{text-align:left;padding:9px 12px;border-bottom:1px solid var(--rule);vertical-align:top}
thead th{background:#eef1f3;font:600 11px/1.4 "IBM Plex Mono",ui-monospace,monospace;
  text-transform:uppercase;letter-spacing:.06em;color:var(--muted)}
tbody tr:last-child td{border-bottom:0}
td.n{text-align:center;font-family:"IBM Plex Mono",ui-monospace,monospace;width:64px}
.pass{color:var(--ok);font-weight:600}
.fail{color:var(--bad);font-weight:600}
.score{font:700 34px/1 "IBM Plex Sans",sans-serif;letter-spacing:-.02em}
.rec{background:var(--surface);border:1px solid var(--rule);border-left:3px solid var(--bad);
  border-radius:3px;padding:18px 20px;margin-top:14px}
"""


def build_sheet(base: pathlib.Path, plugin: str, written: dict[str, str],
                mech: list[tuple[int, str, bool | None, str]]) -> pathlib.Path:
    rows = []
    for num, label, non_negotiable in RUBRIC:
        hit = next((m for m in mech if m[0] == num), None)
        if hit is None:
            verdict, evidence = "&mdash;", "judged by eye on the renders above; fill this in"
            cls = ""
        else:
            _, _, ok, evidence = hit
            verdict = "pass" if ok else "FAIL"
            cls = "pass" if ok else "fail"
        rows.append(
            f'<tr><td class="n">{num}</td><td>{label}'
            f'{" <strong>(non-negotiable)</strong>" if non_negotiable else ""}</td>'
            f'<td class="{cls}">{verdict}</td><td>{evidence}</td></tr>'
        )

    shots = []
    for w in DISPLAY_WIDTHS:
        key = f"display-{w}"
        if key in written:
            shots.append(
                f'<figure class="shot"><img src="banner-renders/{written[key]}" '
                f'alt="{plugin} banner at {w}px" width="{w}" />'
                f'<figcaption>{w}px displayed width'
                f'{" &middot; a GitHub README content column" if w == 900 else ""}'
                f'{" &middot; the catalogue card" if w == 400 else ""}'
                f'{" &middot; thumbnail" if w == 200 else ""}</figcaption></figure>'
            )
    if "crop-lockup" in written:
        shots.append(
            f'<figure class="shot"><img src="banner-renders/{written["crop-lockup"]}" '
            f'alt="{plugin} icon and wordmark at 1:1" />'
            f'<figcaption>the icon and wordmark lockup at 1:1 against the composed layout'
            f'</figcaption></figure>'
        )

    scored = [m for m in mech if m[2] is not None]
    won = sum(1 for m in scored if m[2])
    unjudged = RUBRIC_TOTAL - len(scored)

    recommendation = recommendation_html(base)
    doc = f"""<!doctype html>
<meta charset="utf-8">
<title>{plugin} banner audit</title>
<style>{SHEET_CSS}</style>
<div class="wrap">
<h1>{plugin} &middot; banner audit</h1>
<p class="note">Every size a person actually meets this banner at, then the
12-point rubric. Delivery bar is {RUBRIC_BAR} of {RUBRIC_TOTAL} with checks 1, 2, 3, 7
and 12 non-negotiable. {won} of {len(scored)} mechanical checks pass and
{unjudged} still need a human verdict, which is what the renders above are for.</p>

<h2>The renders</h2>
{"".join(shots)}

<h2>Rubric</h2>
<table><thead><tr><th>#</th><th>Check</th><th>Verdict</th><th>Evidence</th></tr></thead>
<tbody>{"".join(rows)}</tbody></table>

<p class="score">{won} / {RUBRIC_TOTAL}</p>

<div class="rec">
{recommendation}
</div>
</div>
"""
    out = base / "banner-audit.html"
    out.write_text(doc, encoding="utf-8")
    return out


# ------------------------------------------------------------------ check

def mechanical(base: pathlib.Path) -> list[tuple[int, str, bool | None, str]]:
    """The rubric rows a script can decide. Returns (num, label, ok, evidence)."""
    results = []
    labels = {n: l for n, l, _ in RUBRIC}

    size = png_size(base / "banner.png")
    if size is None:
        results.append((1, labels[1], False, "assets/banner.png is absent"))
    else:
        ok = size == (BANNER_W, BANNER_H)
        why = f"{size[0]}x{size[1]}"
        if not ok and size == (BANNER_W // 2, BANNER_H // 2):
            why += ", which is the layout size at deviceScaleFactor 1, so it is half resolution"
        results.append((1, labels[1], ok, why))

    src = find_src(base)
    if src is None:
        results.append((12, labels[12], False, "no banner-src.html or banner-src.svg"))
        return results
    results.append((12, labels[12], True, src.name))

    if src.suffix == ".html":
        refs = SrcRefs()
        refs.feed(src.read_text(encoding="utf-8", errors="replace"))
        icons = [s for s in refs.imgs if not s.startswith("data:")]
        inlined = [s for s in refs.imgs if s.startswith("data:")]
        if icons:
            missing = [s for s in icons if not (base / s).exists()]
            results.append((2, labels[2], not missing,
                            "referenced " + ", ".join(icons) if not missing
                            else "does not resolve: " + ", ".join(missing)))
        elif inlined:
            results.append((2, labels[2], True,
                            f"{len(inlined)} artwork reference inlined as a data URI, which is "
                            "how a file:// render loads it at all"))
        else:
            results.append((2, labels[2], False,
                            "no <img> in the source, so the icon is drawn rather than referenced"))
    else:
        has_image = re.search(r"<image\b", src.read_text(encoding="utf-8", errors="replace"))
        results.append((2, labels[2], bool(has_image),
                        "SVG source embeds an <image>" if has_image
                        else "SVG source has no <image>, so the icon is redrawn rather than referenced"))

    web, local = font_evidence(src)
    if web and not local:
        results.append((3, labels[3], True, "loads " + ", ".join(web)))
    elif web and local:
        results.append((3, labels[3], True,
                        "loads " + ", ".join(web) + "; also names local faces ("
                        + ", ".join(local) + "), acceptable only as fallbacks"))
    else:
        results.append((3, labels[3], False,
                        "no web font is loaded. It sets " + (", ".join(local) or "an undeclared face")
                        + ", which is the rendering machine's furniture: re-render this anywhere "
                        "without those faces and the wordmark silently becomes something else"))

    dashes = visible_text(src).count("—")
    results.append((7, labels[7], dashes == 0,
                    "no em dash in the copy" if dashes == 0
                    else f"{dashes} em dash(es) in the visible copy"))

    # A banner shows the icon it was rendered against, and an icon rebuild
    # silently invalidates it. Nothing caught this before: be-my-witness's icon
    # moved from a periwinkle-violet ground to warm porcelain, and its banner
    # kept displaying the purple one at a correct 3200x1040 with a properly
    # linked font, so every other check passed.
    #
    # Two ways of deciding it, because the cheap one alone is wrong. An exact
    # answer needs the icon's hash as it was when the banner was rendered, which
    # `sheet` now records; where that exists it is definitive. Where it does not,
    # fall back to mtimes with a generous margin, because a banner and an icon
    # produced by the same build land within seconds of each other and a strict
    # comparison then fails on sub-second write order. clarify tripped exactly
    # that: same minute, same build, flagged as stale.
    banner, icon = base / "banner.png", base / "icon.png"
    if banner.exists() and icon.exists():
        recorded = None
        manifest = base / "banner-renders" / "banner-manifest.json"
        if manifest.exists():
            try:
                recorded = json.loads(manifest.read_text()).get("icon_sha")
            except Exception:
                recorded = None
        if recorded:
            if recorded != sha256_of(icon):
                results.append((4, labels[4], False,
                                "the icon has changed since this banner was rendered, so the "
                                "banner displays a previous version of it. Re-render it."))
        elif icon.stat().st_mtime - banner.stat().st_mtime > SAME_BUILD_SECONDS:
            age = (icon.stat().st_mtime - banner.stat().st_mtime) / 86400
            results.append((4, labels[4], False,
                            f"icon.png is {age:.1f} days newer than banner.png, so the banner "
                            "very likely displays a previous version of the icon. Re-render it, "
                            "which also records the icon's hash so this stops being a guess."))
    return results


def cmd_check(base: pathlib.Path) -> int:
    mech = mechanical(base)
    problems = [(n, e) for n, _, ok, e in mech if ok is False]
    for num, label, ok, evidence in mech:
        state = "ok  " if ok else "FAIL"
        print(f"{state}  {num:>2}. {label}\n        {evidence}")

    sheet = base / "banner-audit.html"
    if not sheet.exists():
        problems.append((0, "no banner-audit.html; run `sheet` first"))
        print("FAIL   0. banner-audit.html is absent, so no take was ever scored")
    else:
        text = sheet.read_text(encoding="utf-8", errors="replace")

        # The check the icon sheet earns its keep on: resolve every image the
        # sheet displays. A contact sheet whose sources 404 renders as an empty
        # page, and writing the file tells you nothing about whether its paths
        # resolve. Verified against a real case: this sheet renders blank under
        # a file:// load because the browser here refuses file:// subresources,
        # which looks identical to a 404 and is not one. So resolve on disk and
        # say so, rather than trusting a render.
        refs = SrcRefs()
        refs.feed(text)
        unresolved = [s for s in refs.imgs
                      if not s.startswith(("data:", "http:", "https:"))
                      and not (base / s).exists()]
        if unresolved:
            problems.append((0, "sheet images do not resolve: " + ", ".join(unresolved)))
            print(f"FAIL   0. {len(unresolved)} image(s) in banner-audit.html do not resolve: "
                  + ", ".join(unresolved))
        else:
            local = [s for s in refs.imgs if not s.startswith(("data:", "http:", "https:"))]
            print(f"ok     0. all {len(local)} sheet image(s) resolve on disk")

        if not re.search(rf"\d+\s*/\s*{RUBRIC_TOTAL}", text):
            problems.append((0, f"no N / {RUBRIC_TOTAL} score in banner-audit.html"))
            print(f"FAIL   0. banner-audit.html carries no N / {RUBRIC_TOTAL} score")
        # Test the sidecar itself rather than sniffing the rendered HTML. Sniffing
        # meant a sheet generated before the sidecar existed carried older
        # placeholder prose, matched nothing, and passed unsigned.
        verdict = base / "banner-verdict.md"
        if not verdict.exists() or not verdict.read_text(encoding="utf-8").strip():
            problems.append((0, "no banner-verdict.md, so nobody has signed this banner off"))
            print("FAIL   0. no banner-verdict.md beside the sheet, so nobody has signed this "
                  "banner off. Write the verdict there: does it ship, and what are its known "
                  "liabilities?")
        banner = base / "banner.png"
        if banner.exists() and sheet.stat().st_mtime < banner.stat().st_mtime:
            problems.append((0, "banner-audit.html is older than the banner it describes"))
            print("FAIL   0. banner-audit.html is older than banner.png, so its verdicts "
                  "are about a previous banner")

    if problems:
        print(f"\n{len(problems)} problem(s). This banner is not signed off.")
        return 1
    print("\nOK — sized, reproducible, sourced and scored. Now open the sheet and look at it.")
    return 0


# ------------------------------------------------------------------ family

def cmd_family(repo: pathlib.Path) -> int:
    """One sheet of every banner at README width, where drift across the set shows."""
    Image = load_pil()
    if Image is None:
        print("family needs Pillow", file=sys.stderr)
        return 2

    rows = []
    for plugin_dir in sorted((repo / "plugins").iterdir()):
        banner = plugin_dir / "assets" / "banner.png"
        if not banner.exists():
            continue
        size = png_size(banner)
        src = find_src(plugin_dir / "assets")
        web, local = font_evidence(src) if src else ([], [])
        flag = ""
        if size != (BANNER_W, BANNER_H):
            flag += f'<span class="fail">{size[0]}x{size[1]}</span> '
        if not web:
            flag += '<span class="fail">no web font</span> '
        rows.append(
            f'<figure class="shot"><img src="../plugins/{plugin_dir.name}/assets/banner.png" '
            f'alt="{plugin_dir.name} banner" width="900" />'
            f'<figcaption><strong>{plugin_dir.name}</strong> &middot; '
            f'{", ".join(web) or "no linked face"} {flag}</figcaption></figure>'
        )

    out = repo / "site" / "banner-family.html"
    out.write_text(f"""<!doctype html>
<meta charset="utf-8"><title>Banner family</title><style>{SHEET_CSS}</style>
<div class="wrap">
<h1>Every banner in the set, at README width</h1>
<p class="note">The only view in which drift across the family is visible.
Watch the wordmark face and the ground register down the column: a banner that
looks considered alone can still be the one that does not belong. Anything
flagged in vermilion is a mechanical failure rather than a matter of taste.</p>
{"".join(rows)}
</div>
""", encoding="utf-8")
    print(f"{len(rows)} banners -> {out}")
    return 0


# ------------------------------------------------------------------ cli

def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("sheet", help="render the display sizes and write banner-audit.html")
    s.add_argument("dir")
    c = sub.add_parser("check", help="prove the banner is sized, reproducible, sourced and scored")
    c.add_argument("dir")
    f = sub.add_parser("family", help="one contact sheet of every banner in the repo")
    f.add_argument("repo")
    args = ap.parse_args()

    if args.cmd == "family":
        return cmd_family(pathlib.Path(args.repo).resolve())

    base = pathlib.Path(args.dir).resolve()
    if not base.is_dir():
        print(f"not a directory: {base}", file=sys.stderr)
        return 2

    if args.cmd == "check":
        return cmd_check(base)

    Image = load_pil()
    if Image is None:
        print("sheet needs Pillow", file=sys.stderr)
        return 2
    if not (base / "banner.png").exists():
        print(f"no banner.png in {base}", file=sys.stderr)
        return 2

    plugin = base.parent.name
    written = render_displays(base, Image)
    mech = mechanical(base)
    sheet = build_sheet(base, plugin, written, mech)
    print(f"{len(written)} renders + {sheet.name}")
    print("\nNow open it and look at it. Five rows are scored; the rest need your eye, "
          "and the recommendation block is deliberately a placeholder until you write it.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
