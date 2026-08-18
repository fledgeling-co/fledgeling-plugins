#!/usr/bin/env python3
"""Build the audit_sheet.py fixture suite: one directory per measured hole.

Each fixture is a commission directory that the ORIGINAL `check` exits 0 on and
the improved `check` must exit 1 on — except F8, the clean control, which both
must pass. Fixtures are built from a real render so nothing here is a mock.
"""
import json, os, pathlib, re, shutil, subprocess, sys, time

HERE = pathlib.Path(__file__).resolve().parent
ROOT = pathlib.Path(os.environ.get("FIXTURE_DIR", HERE / "_built"))
SKILL = HERE.parent.parent / "skills" / "create-mac-icon"
TEMPLATE = SKILL / "assets" / "icon-audit-template.html"
NEW = SKILL / "scripts" / "audit_sheet.py"

# A minimal but genuinely layered master: two named groups, a real gradient,
# no <image>. Passes `structure`.
MASTER = """<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
  <defs>
    <linearGradient id="ground" x1="0" y1="0" x2="0" y2="1">
      <stop offset="0" stop-color="{c1}"/><stop offset="1" stop-color="{c2}"/>
    </linearGradient>
    <clipPath id="mask"><path d="M512 24C199 24 24 199 24 512s175 488 488 488 488-175 488-488S825 24 512 24Z"/></clipPath>
  </defs>
  <g id="bg" clip-path="url(#mask)"><rect width="1024" height="1024" fill="url(#ground)"/></g>
  <g id="fg" clip-path="url(#mask)">
    <rect x="300" y="360" width="424" height="300" rx="48" fill="#fff" opacity="0.88"/>
    <rect x="356" y="430" width="312" height="26" rx="13" fill="{c2}" opacity="0.55"/>
    <rect x="356" y="500" width="228" height="26" rx="13" fill="{c2}" opacity="0.45"/>
  </g>
  <g id="highlight" clip-path="url(#mask)">
    <rect x="24" y="24" width="976" height="8" rx="4" fill="#fff" opacity="0.35"/>
  </g>
</svg>
"""

# A full-bleed raster take, square corners, no mask: the Engine C output shape.
FULLBLEED = """<svg xmlns="http://www.w3.org/2000/svg" width="1024" height="1024" viewBox="0 0 1024 1024">
  <g id="bg"><rect width="1024" height="1024" fill="#c8552a"/></g>
  <g id="fg"><circle cx="512" cy="512" r="260" fill="#ffe9c9"/></g>
</svg>
"""


def sheet(rows, rec_filled=True, score=11, hero=True, remote=False, keep_comments=False):
    """Render audit.html from the real template, filling placeholders."""
    t = TEMPLATE.read_text()
    body = t.split("<!-- ROW BLOCK", 1)[0]
    rowblock = t.split("<!-- ROW BLOCK", 1)[1].split("<!-- /ROW BLOCK -->", 1)[0]
    rowblock = rowblock.split("-->", 1)[1]
    tail = t.split("<!-- /ROW BLOCK -->", 1)[1]

    out = [body.replace("{{APP_NAME}}", "Ledgerline").replace("{{DIRECTION_NAME}}", "Porcelain Instrument")]
    for i, (tid, fname, n) in enumerate(rows):
        r = rowblock
        r = r.replace("{{ship|fail|}}", "ship" if i == 0 else "fail")
        r = r.replace("{{TAKE_ID}}", tid).replace("{{FILENAME}}", fname).replace("{{take}}", tid)
        r = r.replace('{{ENGINE_AND_ROLE — e.g. "hand-authored layered SVG — SHIPS" / "Arrow vector take" / "GPT-Image raster, corpus-referenced"}}',
                      "hand-authored layered SVG — SHIPS" if i == 0 else "raster take")
        r = r.replace("{{N}}", str(n if i == 0 else max(6, n - 3)))
        r = r.replace("{{WHY: what passes, which rubric checks failed and the mechanism, what was salvaged into the master. Losing takes state the reason they lost.}}",
                      "Ground cushion reads at 48px; frosted plate holds figure-ground 4.2:1." if i == 0
                      else "Lost on #10: flat pre-masked raster, identity dies under Tinted.")
        if not hero:
            r = re.sub(r'<figure><img src="audit-renders/[^"]*-1024\.png"[^>]*>.*?</figure>', "", r, flags=re.S)
        if remote:
            r = re.sub(r'src="audit-renders/[^"]*"', 'src="https://example.invalid/x.png"', r)
        out.append(r)
    tail = tail.replace("{{TAKE_ID}}", rows[0][0]).replace("{{FILENAME}}", rows[0][1])
    if rec_filled:
        tail = tail.replace("{{WHY_IT_SHIPS — Icon-Composer readiness, non-negotiable checks 1–4 on real renders, material provenance.}}",
                            "Checks 1-4 pass on real renders; material sampled from apple-23 and apple-28.")
        tail = tail.replace("{{LIABILITIES — never leave this empty; an audit with no known liabilities hasn't looked hard enough.}}",
                            "The highlight bar clips at 16px; the plate's lower edge wants 1px more separation.")
    out.append(tail)
    s = "".join(out)
    if not keep_comments:
        import re as _re
        s = _re.sub(r"<!--.*?-->", "", s, flags=_re.S)
    return s


def base_commission(d: pathlib.Path, takes, master_text=None):
    d.mkdir(parents=True, exist_ok=True)
    (d / "icon.svg").write_text(master_text or MASTER.format(c1="#fafafb", c2="#2f6f7f"))
    (d / "build_icon.py").write_text("# generator: geometry and material as named constants\n")
    if len(takes) > 1:
        # Engine C's real output shape: a full-bleed 1024 PNG, square corners.
        tmp = d / "_c.svg"
        tmp.write_text(FULLBLEED)
        subprocess.run(["rsvg-convert", "-w", "1024", "-h", "1024",
                        str(tmp), "-o", str(d / "icon-c.png")], check=True)
        tmp.unlink()
    return d


def do_render(d: pathlib.Path, extra_args=()):
    r = subprocess.run([sys.executable, str(NEW), "render", str(d), *extra_args],
                       capture_output=True, text=True)
    if r.returncode != 0:
        print(f"  render failed for {d.name}: {r.stderr[-400:]}")
    return r


ROWS2 = [("master", "icon.svg", 11), ("c", "icon-c.png", 11)]

if ROOT.exists():
    shutil.rmtree(ROOT)

built = {}

# F8 — clean control. Both versions must pass.
d = base_commission(ROOT / "F8-clean", ROWS2)
do_render(d, ("--take", "master=icon.svg:svg", "--take", "c=icon-c.png:raster-mask"))
(d / "audit.html").write_text(sheet(ROWS2))
built["F8-clean"] = "control: a correct commission. Both versions must exit 0."

# F1 — prose placeholder left unfilled in the recommendation + liabilities.
d = base_commission(ROOT / "F1-prose-placeholder", ROWS2)
do_render(d, ("--take", "master=icon.svg:svg", "--take", "c=icon-c.png:raster-mask"))
(d / "audit.html").write_text(sheet(ROWS2, rec_filled=False))
built["F1-prose-placeholder"] = "recommendation reads literally {{WHY_IT_SHIPS — ...}} and {{LIABILITIES — ...}}"

# F2 — stale renders: master rewritten after the sheet was rendered.
d = base_commission(ROOT / "F2-stale-render", ROWS2)
do_render(d, ("--take", "master=icon.svg:svg", "--take", "c=icon-c.png:raster-mask"))
(d / "audit.html").write_text(sheet(ROWS2))
time.sleep(1.2)
# the loop moves the master: a real parameter change, teal -> warmer ground
(d / "icon.svg").write_text(MASTER.format(c1="#fbf7f2", c2="#b8562c"))
now = time.time()
import os
os.utime(d / "icon.svg", (now + 5, now + 5))
built["F2-stale-render"] = "the fidelity loop changed the master after the sheet was rendered"

# F3 — every image reference remote: the sheet audits nothing local.
d = base_commission(ROOT / "F3-all-remote-src", ROWS2)
do_render(d, ("--take", "master=icon.svg:svg", "--take", "c=icon-c.png:raster-mask"))
(d / "audit.html").write_text(sheet(ROWS2, remote=True))
built["F3-all-remote-src"] = "all <img src> are https:, so nothing local is displayed"

# F4 — best take below the 10/12 delivery bar.
d = base_commission(ROOT / "F4-below-rubric-bar", ROWS2)
do_render(d, ("--take", "master=icon.svg:svg", "--take", "c=icon-c.png:raster-mask"))
(d / "audit.html").write_text(sheet([("master", "icon.svg", 8), ("c", "icon-c.png", 8)]))
built["F4-below-rubric-bar"] = "best take scores 8/12, under the >=10 bar"

# F5 — 1024 hero rendered, displayed nowhere.
d = base_commission(ROOT / "F5-hero-not-shown", ROWS2)
do_render(d, ("--take", "master=icon.svg:svg", "--take", "c=icon-c.png:raster-mask"))
(d / "audit.html").write_text(sheet(ROWS2, hero=False))
built["F5-hero-not-shown"] = "1024 rendered for every take, shown in no <img>"

# F6 — raster take passed as `png`, so it ships unmasked and square.
d = base_commission(ROOT / "F6-unmasked-raster", ROWS2)
do_render(d, ("--take", "master=icon.svg:svg", "--take", "c=icon-c.png:png"))
(d / "audit.html").write_text(sheet(ROWS2))
built["F6-unmasked-raster"] = "Engine C take rendered kind=png: square corners beside squircle siblings"

# F7 — master embeds a raster: the metric-gaming exploit, structure never run.
bad = MASTER.format(c1="#fafafb", c2="#2f6f7f").replace(
    '<g id="highlight"',
    '<image href="data:image/png;base64,iVBORw0KGgo=" x="0" y="0" width="1024" height="1024"/>\n  <g id="highlight"')
d = base_commission(ROOT / "F7-master-embeds-raster", ROWS2, master_text=bad)
do_render(d, ("--take", "master=icon.svg:svg", "--take", "c=icon-c.png:raster-mask"))
(d / "audit.html").write_text(sheet(ROWS2))
built["F7-master-embeds-raster"] = "master contains <image>: raster embedding, the metric-gaming exploit"

# F9 — instructions retained. The template documents its own convention with
# placeholder-shaped strings, so the old regex failed a correct sheet on its docs.
d = base_commission(ROOT / "F9-keeps-instructions", ROWS2)
do_render(d, ("--take", "master=icon.svg:svg", "--take", "c=icon-c.png:raster-mask"))
(d / "audit.html").write_text(sheet(ROWS2, keep_comments=True))
built["F9-keeps-instructions"] = "correct sheet that keeps the template comment: old false-positives on its own docs"

(ROOT / "MANIFEST.json").write_text(json.dumps(built, indent=2))
print(f"\nbuilt {len(built)} fixtures in {ROOT}")
for k, v in built.items():
    print(f"  {k}: {v}")
