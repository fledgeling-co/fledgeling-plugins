#!/usr/bin/env python3
"""audit_sheet.py — render an icon commission's contact sheet, then prove it is real.

Two subcommands, and the second is the point.

    python3 audit_sheet.py render <dir> [--take id=file[:kind]] ...
    python3 audit_sheet.py check  <dir>

`render` produces the retina sources the sheet displays. `check` is the
mechanical half: it reads audit.html, resolves every <img src> against the
directory, and fails when one is missing. A contact sheet whose images 404 is
the exact artifact that ships unseen, because writing the file tells you nothing
about whether its paths resolve — and "the skill says to create an audit.html"
has twice not been enough on its own.

Kinds: svg (default for .svg), png (default for raster), svg-letterbox for
artwork that is not square, raster-mask to squircle-mask a full-bleed raster
first. With no --take arguments, render discovers icon*.svg and icon*.png in the
directory and infers the kind from the extension.

Sizes are retina pairs: 256/128/96/64/32 sources shown at 128/64/48/32/16 css
px, plus a 1024 hero. The 48 row exists because a Finder list and a marketplace
tile use it, and an icon that survives 128 and 16 can still fail between them.

Requires rsvg-convert for SVG sources and Pillow for raster work; both are
reported as a named skip rather than a crash when absent.
"""
from __future__ import annotations

import argparse
import html.parser
import pathlib
import re
import shutil
import subprocess
import sys
import urllib.parse

SIZES = (1024, 256, 128, 96, 64, 32)
DISPLAY = {256: 128, 128: 64, 96: 48, 64: 32, 32: 16}
SQUIRCLE_CANDIDATES = ("squircle-path.txt", "../assets/squircle-path.txt")


def die(msg: str, code: int = 1):
    print(f"FAIL  {msg}", file=sys.stderr)
    raise SystemExit(code)


def have(binary: str) -> bool:
    return shutil.which(binary) is not None


def load_pil():
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        return None
    from PIL import Image
    return Image


def squircle_path(base: pathlib.Path) -> str | None:
    here = pathlib.Path(__file__).resolve().parent
    for cand in (*(base / c for c in SQUIRCLE_CANDIDATES),
                 here.parent / "assets" / "squircle-path.txt"):
        if cand.exists():
            return cand.read_text().strip()
    return None


# ---------------------------------------------------------------- render

def alpha_mask(size: int, path_d: str, out: pathlib.Path, Image):
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" '
           f'viewBox="0 0 1024 1024"><path d="{path_d}" fill="#fff"/></svg>')
    tmp_svg, tmp_png = out / "_mask.svg", out / "_mask.png"
    tmp_svg.write_text(svg)
    subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size),
                    str(tmp_svg), "-o", str(tmp_png)], check=True)
    mask = Image.open(tmp_png).convert("RGBA").split()[3]
    tmp_svg.unlink(missing_ok=True)
    tmp_png.unlink(missing_ok=True)
    return mask


def render(base: pathlib.Path, takes: dict[str, tuple[str, str]]):
    out = base / "audit-renders"
    out.mkdir(exist_ok=True)
    Image = load_pil()
    d = squircle_path(base)
    made, skipped = 0, []

    for take, (src, kind) in sorted(takes.items()):
        p = base / src
        if not p.exists():
            skipped.append(f"{take}: {src} not found")
            continue
        if kind.startswith("svg") and not have("rsvg-convert"):
            skipped.append(f"{take}: needs rsvg-convert")
            continue
        if kind != "svg" and Image is None:
            skipped.append(f"{take}: needs Pillow")
            continue

        for s in SIZES:
            dst = out / f"{take}-{s}.png"
            if kind == "svg":
                subprocess.run(["rsvg-convert", "-w", str(s), "-h", str(s),
                                str(p), "-o", str(dst)], check=True)
            elif kind == "svg-letterbox":
                tmp = out / f"_{take}.png"
                subprocess.run(["rsvg-convert", "-w", str(s), str(p), "-o", str(tmp)], check=True)
                im = Image.open(tmp).convert("RGBA")
                canvas = Image.new("RGBA", (s, s), (0, 0, 0, 0))
                canvas.alpha_composite(im, (0, max(0, (s - im.height) // 2)))
                if d:
                    canvas.putalpha(alpha_mask(s, d, out, Image))
                canvas.save(dst)
                tmp.unlink(missing_ok=True)
            elif kind == "raster-mask":
                im = Image.open(p).convert("RGBA").resize((s, s), Image.LANCZOS)
                if d:
                    im.putalpha(alpha_mask(s, d, out, Image))
                else:
                    skipped.append(f"{take}: no squircle-path.txt, shipped unmasked")
                im.save(dst)
            else:
                Image.open(p).convert("RGBA").resize((s, s), Image.LANCZOS).save(dst)
            made += 1
        print(f"  rendered {take}: {', '.join(str(s) for s in SIZES)}")

    print(f"\n{made} renders into {out}")
    for s in skipped:
        print(f"SKIP  {s}")
    print("\nRetina pairing for the sheet: " +
          ", ".join(f"{src}px source shown at {css}px" for src, css in DISPLAY.items()))
    return 0 if made else 1


def discover(base: pathlib.Path) -> dict[str, tuple[str, str]]:
    takes = {}
    for p in sorted(base.glob("icon*.svg")) + sorted(base.glob("icon*.png")):
        if p.parent.name == "audit-renders":
            continue
        stem = re.sub(r"^icon[-_]?", "", p.stem) or "master"
        stem = re.sub(r"[^a-zA-Z0-9]+", "-", stem).strip("-") or "master"
        if re.fullmatch(r"\d+", stem):          # icon-256.png etc — an export, not a take
            continue
        takes[stem] = (p.name, "svg" if p.suffix == ".svg" else "png")
    return takes


# ---------------------------------------------------------------- check

class ImgSrc(html.parser.HTMLParser):
    def __init__(self):
        super().__init__()
        self.srcs: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag == "img":
            for k, v in attrs:
                if k == "src" and v:
                    self.srcs.append(v)


def check(base: pathlib.Path) -> int:
    problems: list[str] = []
    notes: list[str] = []

    sheet = base / "audit.html"
    if not sheet.exists():
        problems.append("audit.html is not on disk — the commission is not finished")
    else:
        text = sheet.read_text(errors="replace")
        parser = ImgSrc()
        parser.feed(text)
        if not parser.srcs:
            problems.append("audit.html references no images at all")
        missing = []
        for src in parser.srcs:
            if src.startswith(("http://", "https://", "data:")):
                continue
            target = (base / urllib.parse.unquote(src.split("?")[0])).resolve()
            if not target.exists():
                missing.append(src)
        if missing:
            problems.append(f"{len(missing)} image(s) in audit.html do not resolve: "
                            + ", ".join(sorted(set(missing))[:8]))
        else:
            notes.append(f"audit.html: {len(parser.srcs)} image references, all resolve")

        left = sorted(set(re.findall(r"\{\{[A-Z_0-9]+\}\}", text)))
        if left:
            problems.append(f"unfilled template placeholders: {', '.join(left)}")

        rows = len(re.findall(r"<tr[ >]", text))
        if rows < 3:
            notes.append(f"only {rows} table rows — a sheet that hides its losing takes is not an audit")

    masters = [p for p in base.glob("icon*.svg")] + [p for p in base.glob("*.svg")
                                                     if p.name.startswith("icon")]
    if not masters:
        problems.append("no SVG master (icon*.svg) in the directory")

    renders = base / "audit-renders"
    if not renders.exists() or not any(renders.glob("*.png")):
        problems.append("audit-renders/ is empty — run `render` first")
    else:
        by_take: dict[str, set[int]] = {}
        for p in renders.glob("*-*.png"):
            m = re.fullmatch(r"(.+)-(\d+)", p.stem)
            if m:
                by_take.setdefault(m.group(1), set()).add(int(m.group(2)))
        if len(by_take) < 2:
            notes.append(f"only {len(by_take)} take rendered — three engines is the floor, "
                         "and a missing engine is a named deviation, not a default")
        for take, sizes in sorted(by_take.items()):
            gaps = sorted(set(DISPLAY) - sizes)
            if gaps:
                problems.append(f"take '{take}' missing retina sources: "
                                + ", ".join(str(g) for g in gaps))
        if 96 not in {s for sizes in by_take.values() for s in sizes}:
            notes.append("no 96px source: the 48px display row is the Finder-list and "
                         "marketplace-tile size, and nothing else covers it")

    for n in notes:
        print(f"NOTE  {n}")
    for p in problems:
        print(f"FAIL  {p}")
    if problems:
        print(f"\n{len(problems)} problem(s). The icon is not delivered until these clear.")
        return 1
    print("\nOK — audit sheet present, populated, and every image resolves.")
    print("Now open it in a browser and read it. This script proves the files exist;")
    print("only looking proves the icons are any good.")
    return 0


# ---------------------------------------------------------------- cli

def main():
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)

    r = sub.add_parser("render", help="render every take at the sheet's retina sources")
    r.add_argument("dir", type=pathlib.Path)
    r.add_argument("--take", action="append", default=[],
                   metavar="id=file[:kind]",
                   help="kind is svg | png | svg-letterbox | raster-mask")

    c = sub.add_parser("check", help="prove the sheet exists, is filled, and its images resolve")
    c.add_argument("dir", type=pathlib.Path)

    a = ap.parse_args()
    base = a.dir.expanduser().resolve()
    if not base.is_dir():
        die(f"{base} is not a directory")

    if a.cmd == "check":
        raise SystemExit(check(base))

    takes: dict[str, tuple[str, str]] = {}
    for spec in a.take:
        if "=" not in spec:
            die(f"--take needs id=file[:kind], got {spec!r}")
        tid, rest = spec.split("=", 1)
        if ":" in rest:
            src, kind = rest.rsplit(":", 1)
        else:
            src, kind = rest, ("svg" if rest.endswith(".svg") else "png")
        takes[tid] = (src, kind)
    if not takes:
        takes = discover(base)
        if not takes:
            die("no icon*.svg / icon*.png found and no --take given")
        print(f"discovered {len(takes)} take(s): {', '.join(sorted(takes))}\n")
    raise SystemExit(render(base, takes))


if __name__ == "__main__":
    main()
