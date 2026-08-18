#!/usr/bin/env python3
"""audit_sheet.py — render an icon commission's contact sheet, then prove it is real.

Two subcommands, and the second is the point.

    python3 audit_sheet.py render <dir> [--take id=file[:kind]] ...
    python3 audit_sheet.py check  <dir>

`render` produces the retina sources the sheet displays, and records what it
did in `audit-renders/render-manifest.json` — each take's id, its source file,
the kind it was rendered as, and the source's mtime. `check` is the mechanical
half: it reads audit.html, resolves every <img src> against the directory, and
fails when one is missing. A contact sheet whose images 404 is the exact
artifact that ships unseen, because writing the file tells you nothing about
whether its paths resolve — and "the skill says to create an audit.html" has
twice not been enough on its own.

The manifest exists because three of `check`'s holes were unclosable without
it. It could prove a render existed but not that it was **current**, and the
fidelity loop guarantees the master changes after the sheet is first written,
so a sheet showing the pre-loop icon beside a post-loop master passed cleanly.
It could not tell a raster take rendered as `png` from one rendered as
`raster-mask`, so a full-bleed raster shipped square-cornered on the sheet
unnoticed. And it had no per-take source to compare anything against.

Kinds: svg (default for .svg), png (default for raster), svg-letterbox for
artwork that is not square, raster-mask to squircle-mask a full-bleed raster
first. With no --take arguments, render discovers icon*.svg and icon*.png in the
directory and infers the kind from the extension.

Sizes are retina pairs: 256/128/96/64/32 sources shown at 128/64/48/32/16 css
px, plus a 1024 hero. The 48 row exists because a Finder list and a marketplace
tile use it, and an icon that survives 128 and 16 can still fail between them.

Severity convention: `FAIL` and `NOTE` both go to **stderr**, so a caller
redirecting stdout cannot lose either. Exit 0 means every FAIL cleared; it does
not mean there was nothing to read, and a NOTE on a clean exit is still worth
reading.

Requires rsvg-convert for SVG sources and Pillow for raster work; both are
reported as a named skip rather than a crash when absent.
"""
from __future__ import annotations

import argparse
import html.parser
import json
import pathlib
import re
import shutil
import subprocess
import sys
import time
import urllib.parse

SIZES = (1024, 256, 128, 96, 64, 32)
DISPLAY = {256: 128, 128: 64, 96: 48, 64: 32, 32: 16}
HERO = 1024                      # rendered for every take and displayed as the hero
RUBRIC_BAR = 10                  # of 12; checks 1-4 non-negotiable (icon-directions.md)
TAKE_FLOOR = 3                   # A + B + C; the pipeline's stated minimum set
STALE_GRACE_S = 2                # filesystem mtime slack, not a tolerance for staleness
SQUIRCLE_CANDIDATES = ("squircle-path.txt", "../assets/squircle-path.txt")
MANIFEST = "render-manifest.json"


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
    recorded: dict[str, dict] = {}

    for take, (src, kind) in sorted(takes.items()):
        p = base / src
        if not p.exists():
            skipped.append(f"{take}: {src} not found")
            continue
        if kind.startswith("svg") and not have("rsvg-convert"):
            skipped.append(f"{take}: needs rsvg-convert (brew install librsvg)")
            continue
        if kind != "svg" and Image is None:
            skipped.append(f"{take}: needs Pillow (pip install Pillow)")
            continue
        # A raster kind pointed at an SVG used to surface as a bare
        # PIL.UnidentifiedImageError several frames deep. It is the commonest
        # --take typo there is, and the fix is a one-word edit, so it deserves a
        # sentence rather than a traceback.
        if kind in ("png", "raster-mask") and p.suffix.lower() == ".svg":
            skipped.append(f"{take}: kind '{kind}' expects a raster file but {src} is an SVG "
                           f"— use ':svg', or ':svg-letterbox' if the artwork is not square")
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
        recorded[take] = {"source": src, "kind": kind,
                          "source_mtime": p.stat().st_mtime,
                          "rendered_at": time.time()}
        print(f"  rendered {take}: {', '.join(str(s) for s in SIZES)}")

    # What was rendered, from what, as what. `check` needs all three: it cannot
    # otherwise tell a current render from a stale one, nor a raster masked to
    # the squircle from one shipped full-bleed square.
    (out / MANIFEST).write_text(json.dumps(
        {"takes": recorded, "sizes": list(SIZES), "display": {str(k): v for k, v in DISPLAY.items()}},
        indent=2))

    print(f"\n{made} renders into {out}")
    for s in skipped:
        print(f"SKIP  {s}", file=sys.stderr)
    print("\nRetina pairing for the sheet: " +
          ", ".join(f"{src}px source shown at {css}px" for src, css in DISPLAY.items()) +
          f", plus the {HERO}px hero.")
    return 0 if made else 1


def discover(base: pathlib.Path) -> dict[str, tuple[str, str]]:
    """Infer the takes from the directory, so `render` works with no arguments.

    Two rules here exist because the naive version produced a manifest `check`
    then rejected, which makes bare `render` look like a way to make a sheet
    worse. Both were found by running it across twenty-three commissions at once
    and watching nine of them regress.

    First, a full-bleed raster and its squircle-masked twin are the same take,
    and the masked one is the take that ships. Discovering both registered the
    unmasked file under its own id, and `check` correctly failed it for opaque
    corners. So an unmasked raster is skipped when a `-masked` sibling exists.

    Second, a raster with no masked twin still has opaque corners, and the kind
    that fixes that is `raster-mask` rather than `png`. Inferring the kind from
    the file extension alone is what put a square-cornered tile on the sheet in
    the first place, so the corners decide it, not the suffix.
    """
    Image = load_pil()
    candidates = []
    for p in sorted(base.glob("icon*.svg")) + sorted(base.glob("icon*.png")):
        if p.parent.name == "audit-renders":
            continue
        stem = re.sub(r"^icon[-_]?", "", p.stem) or "master"
        stem = re.sub(r"[^a-zA-Z0-9]+", "-", stem).strip("-") or "master"
        if re.fullmatch(r"\d+", stem):          # icon-256.png etc, an export rather than a take
            continue
        candidates.append((stem, p))

    masked_stems = {s[: -len("-masked")] for s, _ in candidates if s.endswith("-masked")}

    takes = {}
    for stem, p in candidates:
        if p.suffix == ".svg":
            takes[stem] = (p.name, "svg")
            continue
        if stem in masked_stems:
            continue                            # its masked twin is the take
        kind = "raster-mask" if corners_opaque(p, Image) else "png"
        takes[stem] = (p.name, kind)
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


def corners_opaque(png: pathlib.Path, Image) -> bool | None:
    """True when all four extreme corner pixels are opaque.

    A squircle-masked take has transparent corners by construction. A full-bleed
    raster passed as `png` instead of `raster-mask` does not, and it lands on the
    sheet as a square-cornered tile beside masked siblings — which is a
    silhouette break, the one defect the sheet's own rule says reads as an error
    at every size. Nothing could see it before, because only `render` knew the
    kind and only `check` looked at the output.
    """
    if Image is None:
        return None
    try:
        im = Image.open(png).convert("RGBA")
    except Exception:
        return None
    w, h = im.size
    pts = ((0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1))
    return all(im.getpixel(p)[3] > 16 for p in pts)


def run_structure(master: pathlib.Path) -> tuple[str, list[str]]:
    """Run the sibling structure gate on a master. Returns (state, lines).

    eval 1 asserts "the shipped master passes fidelity.py structure", and until
    now nothing in the commission path ran it — only the fidelity loop did. So a
    commission that shipped without looping shipped without the <image>-embed
    check, the complexity envelope or the layer-plan check, with the invariant
    asserted in the eval and enforced nowhere.
    """
    fid = pathlib.Path(__file__).resolve().parent / "fidelity.py"
    if not fid.exists():
        return "skip", [f"fidelity.py not beside audit_sheet.py ({fid})"]
    try:
        r = subprocess.run([sys.executable, str(fid), "structure", "--candidate", str(master)],
                           capture_output=True, text=True, timeout=60)
    except Exception as e:
        return "skip", [f"could not run structure: {e}"]
    lines = [ln.strip() for ln in (r.stderr or "").splitlines()
             if ln.strip().startswith(("-", "?"))]
    return ("pass" if r.returncode == 0 else "fail"), lines


def check(base: pathlib.Path) -> int:
    problems: list[str] = []
    notes: list[str] = []
    Image = load_pil()

    # ---- the takes, their sources, and what they were rendered as
    renders = base / "audit-renders"
    manifest = renders / MANIFEST
    recorded: dict[str, dict] = {}
    if renders.exists() and manifest.exists():
        try:
            recorded = (json.loads(manifest.read_text()) or {}).get("takes") or {}
        except Exception as e:
            problems.append(f"{MANIFEST} is unreadable ({e}) — re-run `render`")

    masters = sorted(set(base.glob("icon*.svg")))
    if not masters:
        problems.append("no SVG master (icon*.svg) in the directory. The glob is the "
                        "naming contract: a master named for its content still has to be "
                        "called icon*.svg here, because the marketplace family requires "
                        "icon.png / icon-256.png beside it")

    # The newest thing the sheet is supposed to be describing. Build scripts count:
    # a regenerated master is the whole point of the build-script discipline.
    sources = list(masters) + sorted(base.glob("build_icon*.py")) + sorted(base.glob("*.svg"))
    for t in recorded.values():
        p = base / t.get("source", "")
        if p.exists():
            sources.append(p)
    newest_src = max((p.stat().st_mtime for p in set(sources) if p.exists()), default=None)

    # ---- the sheet itself
    sheet = base / "audit.html"
    if not sheet.exists():
        problems.append("audit.html is not on disk — the commission is not finished")
    else:
        text = sheet.read_text(errors="replace")
        parser = ImgSrc()
        parser.feed(text)
        if not parser.srcs:
            problems.append("audit.html references no images at all")
        local, missing = [], []
        for src in parser.srcs:
            if src.startswith(("http://", "https://", "data:")):
                continue
            local.append(src)
            if not (base / urllib.parse.unquote(src.split("?")[0])).resolve().exists():
                missing.append(src)
        if missing:
            problems.append(f"{len(missing)} image(s) in audit.html do not resolve: "
                            + ", ".join(sorted(set(missing))[:8]))
        elif parser.srcs and not local:
            # "all resolve" was printed for a sheet that resolved nothing locally,
            # because remote and data: srcs are skipped and only zero <img> failed.
            problems.append(f"every one of the {len(parser.srcs)} image references is "
                            f"remote or a data: URI — the sheet displays no render from "
                            f"audit-renders/, so it is not auditing this commission")
        elif local:
            notes.append(f"audit.html: {len(local)} local image reference(s), all resolve")

        # Widened from \{\{[A-Z_0-9]+\}\}, which caught 6 of the template's
        # placeholder forms and missed every prose-carrying one — the recommendation
        # block, each take's verdict, and {{LIABILITIES — never leave this empty…}}
        # whose own text says not to. A sheet whose recommendation read literally
        # "{{WHY_IT_SHIPS — …}}" exited 0.
        #
        # Scanned over the body with HTML comments removed, because the template
        # DOCUMENTS the convention using placeholder-shaped strings ("fill every
        # {{PLACEHOLDER}}"). Under the old regex, keeping the template's own
        # instructions in the sheet failed the gate on its own documentation — so
        # the instructions had to be deleted to pass, which is why the shipped
        # sheet carries none of them. A comment is not shown to a reviewer, so it
        # cannot be an unfilled field.
        body = re.sub(r"<!--.*?-->", "", text, flags=re.S)
        left = sorted(set(re.findall(r"\{\{[^{}]{1,200}\}\}", body)))
        # Names are shown untruncated up to a generous cap: the panel that judged
        # these messages singled out "truncated leftover strings" as the thing that
        # stopped an agent locating the field, and a placeholder's whole point is
        # that it is searchable text.
        if left:
            shown = [p if len(p) <= 120 else p[:117] + "…" for p in left[:8]]
            problems.append(f"{len(left)} unfilled placeholder(s) — the sheet ships "
                            f"showing them: " + ", ".join(shown))

        # Three engines are a floor, and this is the only place that can prove it.
        # Two things were wrong with counting <tr>: it was a note rather than a
        # problem, so a one-take sheet exited 0; and it counted the header row, so
        # `rows < 3` actually permitted TWO takes while claiming to require three.
        #
        # Count the take cells where the current template's class is present, and
        # fall back to rows-minus-header where it is not. The fallback is not
        # politeness: keying only on `class="take"` failed a sheet that ships in
        # this marketplace and predates that class, reporting 0 takes for a sheet
        # carrying four. A check that fires on every historical artifact is a
        # defect in the check.
        #
        # The floor is three TAKES, not three engines: where media-gen-pro is
        # unavailable the skill widens Engine A to two or three genuinely different
        # hand-authored takes, and that still clears this. What it will not clear is
        # a single take written up as though a set had been judged.
        rows = len(re.findall(r"<tr[ >]", body))
        tagged = len(re.findall(r"<td[^>]*class=\"[^\"]*\btake\b[^\"]*\"", body, re.I))
        takes = tagged or max(rows - 1, 0)
        if takes < TAKE_FLOOR:
            problems.append(f"audit.html carries {takes} take(s); the floor is {TAKE_FLOOR}. "
                            f"A contact sheet exists to show what lost and why, so a sheet "
                            f"with one row is a verdict with no comparison behind it. Run "
                            f"the missing engines, or — where media-gen-pro is unavailable "
                            f"— widen Engine A to three genuinely different hand-authored "
                            f"takes and say in the sheet that the engines were unavailable.")

        # The bar was never checked. `check` proved the sheet was populated, never
        # that it passed: the delivery bar is >=10/12 with checks 1-4 non-negotiable.
        #
        # Read out of the score CELLS, not the page. Scanning the whole body found
        # the rubric footer's own sentence — "delivery bar >=10/12" — and read 10
        # as a take's score, so a sheet whose every take scored 8 passed the bar on
        # the strength of the text describing the bar.
        cells = re.findall(r"<td[^>]*class=\"[^\"]*\bscore\b[^\"]*\"[^>]*>(.*?)</td>",
                           body, re.I | re.S)
        scores = [int(m) for c in cells
                  for m in re.findall(r"(\d{1,2})\s*(?:/|&#47;)\s*12\b", c)]
        if not scores:
            problems.append("no rubric score of the form 'N / 12' anywhere in audit.html — "
                            "the 12-point rubric is the shipping authority and the sheet "
                            "has to carry each take's score")
        elif max(scores) < RUBRIC_BAR:
            problems.append(f"best take scores {max(scores)}/12, below the {RUBRIC_BAR}/12 "
                            f"delivery bar — this sheet records a commission that has not "
                            f"met the bar yet, not a delivery")
        if not re.search(r"Recommendation:\s*ship", body, re.I):
            problems.append("no recommendation block naming the shipping take — the sheet "
                            "has to say which take ships and what its known liabilities are")

        if not re.search(rf"-{HERO}\.png", body):
            problems.append(f"the {HERO}px hero is rendered for every take and displayed "
                            f"nowhere in audit.html, while the sheet's own subtitle claims "
                            f"it. Show it or stop claiming it")

        if newest_src is not None and sheet.stat().st_mtime < newest_src - STALE_GRACE_S:
            problems.append("audit.html is older than the master it describes: its verdicts "
                            "and scores are about a previous icon. The fidelity loop changes "
                            "the master after the sheet is first written, which is exactly "
                            "when this happens — re-render and rewrite the sheet")

    # ---- the renders
    if not renders.exists() or not any(renders.glob("*.png")):
        problems.append("audit-renders/ is empty — run `render` first")
    else:
        if not manifest.exists():
            problems.append(f"audit-renders/{MANIFEST} is absent, so nothing can prove these "
                            f"renders came from the current master or what kind each take was "
                            f"rendered as — re-run `render`")
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
            if HERO not in sizes:
                problems.append(f"take '{take}' has no {HERO}px hero render")
        if 96 not in {s for sizes in by_take.values() for s in sizes}:
            notes.append("no 96px source: the 48px display row is the Finder-list and "
                         "marketplace-tile size, and nothing else covers it")

        # Stale renders. `check` proved files existed; nothing compared them to the
        # master. A sheet showing the pre-loop icon beside a post-loop master passed
        # cleanly, and the loop guarantees the master moves after the sheet is written.
        for take, meta in sorted(recorded.items()):
            src = base / meta.get("source", "")
            if not src.exists():
                problems.append(f"take '{take}' was rendered from {meta.get('source')!r}, "
                                f"which is no longer on disk")
                continue
            src_m = src.stat().st_mtime
            stale = [p.name for s in sorted(SIZES)
                     if (p := renders / f"{take}-{s}.png").exists()
                     and p.stat().st_mtime < src_m - STALE_GRACE_S]
            if stale:
                problems.append(f"take '{take}': {len(stale)} render(s) predate their source "
                                f"{meta.get('source')} — the sheet is showing an older icon "
                                f"than the one being delivered ({', '.join(stale[:4])})")

            if meta.get("kind") == "png":
                opaque = corners_opaque(renders / f"{take}-{max(SIZES)}.png", Image)
                if opaque is None and Image is None:
                    notes.append(f"SKIP  mask check on '{take}': needs Pillow")
                elif opaque:
                    problems.append(f"take '{take}' was rendered as kind 'png' and its "
                                    f"corners are opaque, so it ships full-bleed square "
                                    f"beside squircle-masked siblings. A raster take is "
                                    f"audited on its masked version: re-render it with "
                                    f"--take {take}=<file>:raster-mask")

    # ---- the master's own structure, which the commission path never checked
    #
    # Masters only. `masters` globs icon*.svg, which also catches the losing
    # engine takes the house convention names icon-engineB-arrow-<hash>.svg, and
    # those are not required to carry a layer plan — an Arrow take that lacks one
    # is a take that lost, and the sheet's job is to record that it lost, not to
    # pretend it shipped. Measured before this narrowing: proctor failed here
    # twice and whats-left once, on icons that shipped, so the gate could not be
    # run on any commission in the marketplace including this skill's own.
    ENGINE_TAKE = re.compile(r"^icon-engine[A-Z]", re.I)
    for master in masters:
        if ENGINE_TAKE.match(master.name):
            continue
        state, lines = run_structure(master)
        if state == "fail":
            detail = " | ".join(lines) if lines else "see `fidelity.py structure` output"
            problems.append(f"{master.name} fails `fidelity.py structure`: {detail}")
        elif state == "skip":
            notes.append(f"SKIP  structure gate on {master.name}: {lines[0] if lines else 'unavailable'}")
        else:
            for w in lines:
                if w.startswith("?"):
                    notes.append(f"{master.name} structure advisory: {w.lstrip('? ').strip()}")

    for n in notes:
        print(f"NOTE  {n}", file=sys.stderr)
    for p in problems:
        print(f"FAIL  {p}", file=sys.stderr)
    if problems:
        print(f"\n{len(problems)} problem(s). The icon is not delivered until these clear.",
              file=sys.stderr)
        return 1
    print("\nOK — sheet present, filled, current, past the rubric bar, and every image resolves.")
    print("Now open it in a browser and read it. This script proves the files exist and")
    print("match the master; only looking proves the icons are any good.")
    if notes:
        print(f"({len(notes)} NOTE line(s) on stderr — a clean exit does not mean there was "
              f"nothing to read.)")
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
