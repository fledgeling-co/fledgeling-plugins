#!/usr/bin/env python3
"""review_sheet.py — self-contained side-by-side human review sheet for an icon round.

Generates review.html: the candidate and baseline takes BLINDED as Take 1 /
Take 2 (seeded random order) beside the raster reference, at 1024-view and a
pixelated small-size strip. Feedback is multi-choice first (radio groups +
defect checkboxes); free text is optional.

By default it also starts a mini web server: open the printed URL, click,
Submit — the server writes review-feedback.json into the round directory
itself and then exits. No downloads to shepherd out of ~/Downloads.

Usage:
  python3 review_sheet.py --candidate icon.svg --baseline prev/icon.svg \
      --reference C2.png --outdir runs/r05 --label "round 5: material" \
      [--port 8490] [--no-serve]

Run it in the background from a loop (it exits after one submission, or when
killed); --no-serve just writes the sheet, whose Submit falls back to a
browser download if no server answers.
"""
import argparse
import base64
import hashlib
import http.server
import io
import json
import pathlib
import subprocess
import tempfile

from PIL import Image

SIZES = (1024, 128, 32, 16)


def render(path: pathlib.Path, size: int) -> Image.Image:
    if path.suffix.lower() == ".svg":
        with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as t:
            tmp = pathlib.Path(t.name)
        subprocess.run(["rsvg-convert", "-w", str(size), "-h", str(size),
                        str(path), "-o", str(tmp)], check=True)
        im = Image.open(tmp).convert("RGBA")
        tmp.unlink(missing_ok=True)
        return im
    return Image.open(path).convert("RGBA").resize((size, size), Image.LANCZOS)


def b64(im: Image.Image) -> str:
    buf = io.BytesIO()
    im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()


def cell(path: pathlib.Path) -> dict:
    big = b64(render(path, 512))
    small = {s: b64(render(path, s).resize((s * (6 if s <= 32 else 1),) * 2, Image.NEAREST))
             for s in (128, 32, 16)}
    return {"big": big, "s128": small[128], "s32": small[32], "s16": small[16]}


QUESTIONS = [
    ("overall", "Overall: which take is closer to the reference?",
     ["Take 1", "Take 2", "Tie"]),
    ("material", "Material (shading, lighting, depth): which reads richer, closer to the reference?",
     ["Take 1", "Take 2", "Tie"]),
    ("silhouette", "Silhouette and composition: which matches the reference better?",
     ["Take 1", "Take 2", "Tie"]),
    ("smallsize", "Small sizes (32/16): which stays more legible?",
     ["Take 1", "Take 2", "Tie"]),
    ("action", "What should the loop do next?",
     ["Ship the winner", "Keep iterating", "Revert and branch"]),
]
DEFECTS = ["Flat material", "Wrong lighting direction", "Silhouette drift",
           "Small-size smear", "Colour off", "Reads as a different object"]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--candidate", required=True)
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--reference", required=True)
    ap.add_argument("--outdir", required=True)
    ap.add_argument("--label", default="")
    ap.add_argument("--port", type=int, default=8490)
    ap.add_argument("--no-serve", action="store_true")
    args = ap.parse_args()
    out = pathlib.Path(args.outdir)
    out.mkdir(parents=True, exist_ok=True)

    seed = int(hashlib.sha256((args.label + args.candidate).encode()).hexdigest(), 16)
    cand_first = seed % 2 == 0
    takes = [("Take 1", pathlib.Path(args.candidate if cand_first else args.baseline)),
             ("Take 2", pathlib.Path(args.baseline if cand_first else args.candidate))]
    unblind = {"Take 1": "candidate" if cand_first else "baseline",
               "Take 2": "baseline" if cand_first else "candidate"}

    cols = [("Reference", cell(pathlib.Path(args.reference)))]
    cols += [(name, cell(p)) for name, p in takes]

    def qhtml(qid, text, opts):
        radios = "".join(
            f'<label><input type="radio" name="{qid}" value="{o}"> {o}</label>' for o in opts)
        return f'<div class="q"><p>{text}</p>{radios}</div>'

    defect_boxes = "".join(
        f'<label><input type="checkbox" name="defect" value="{d}"> {d}</label>' for d in DEFECTS)

    col_html = ""
    for name, c in cols:
        col_html += f'''<div class="col"><h2>{name}</h2>
<img class="hero" src="{c["big"]}" width="360" height="360" alt="{name} at 512px">
<div class="strip">
<figure><img src="{c["s128"]}" width="128" height="128" alt=""><figcaption>128</figcaption></figure>
<figure><img class="px" src="{c["s32"]}" width="96" height="96" alt=""><figcaption>32 &times;6</figcaption></figure>
<figure><img class="px" src="{c["s16"]}" width="96" height="96" alt=""><figcaption>16 &times;6</figcaption></figure>
</div></div>'''

    html = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Icon review — {args.label}</title>
<style>
body{{margin:0;padding:32px;background:#0b1418;color:#d7e3e7;font:15px/1.5 -apple-system,BlinkMacSystemFont,sans-serif}}
h1{{font-size:20px;margin:0 0 4px}} .sub{{color:#7fa0aa;margin-bottom:24px}}
.cols{{display:flex;gap:28px;flex-wrap:wrap}}
.col h2{{font-size:14px;color:#7fa0aa;text-transform:uppercase;letter-spacing:.06em}}
img{{background:#08252e;border-radius:10px;display:block}} img.px{{image-rendering:pixelated;border:1px solid #1c2d33}}
.strip{{display:flex;gap:12px;margin-top:10px}} figure{{margin:0;text-align:center}}
figcaption{{color:#7fa0aa;font-size:11px;margin-top:4px}}
.q{{margin:18px 0;padding:14px 16px;background:#0e1c22;border:1px solid #1c2d33;border-radius:10px;max-width:840px}}
.q p{{margin:0 0 8px;font-weight:600}} .q label{{margin-right:18px;color:#a9bec5}}
textarea{{width:100%;max-width:840px;min-height:70px;background:#08161b;color:#d7e3e7;border:1px solid #1c2d33;border-radius:8px;padding:10px;font:inherit}}
button{{margin-top:16px;padding:10px 22px;background:#C4622D;color:#fff;border:0;border-radius:8px;font:600 15px/-apple-system;cursor:pointer}}
.done{{color:#ffd98f;margin-left:12px}}
</style></head><body>
<h1>Icon review — {args.label}</h1>
<div class="sub">Two takes, blinded and randomly ordered, beside the raster reference. Click your answers; typing is optional. Export writes review-feedback.json.</div>
<div class="cols">{col_html}</div>
{"".join(qhtml(*q) for q in QUESTIONS)}
<div class="q"><p>Defects you can see in the closer take (tick any):</p>{defect_boxes}</div>
<div class="q"><p>Anything else (optional):</p><textarea id="notes" placeholder="Optional"></textarea></div>
<button onclick="submitFeedback()">Submit feedback</button><span id="ok" class="done"></span>
<script>
const META = {json.dumps({"label": args.label, "unblind": unblind,
                          "candidate": args.candidate, "baseline": args.baseline,
                          "reference": args.reference})};
function collect(){{
  const ans = {{}};
  for (const q of {json.dumps([q[0] for q in QUESTIONS])}) {{
    const el = document.querySelector(`input[name="${{q}}"]:checked`);
    ans[q] = el ? el.value : null;
  }}
  ans.defects = [...document.querySelectorAll('input[name="defect"]:checked')].map(e=>e.value);
  ans.notes = document.getElementById('notes').value || "";
  return {{...META, answers: ans, exported: new Date().toISOString()}};
}}
async function submitFeedback(){{
  const payload = collect();
  try {{
    const r = await fetch('/submit', {{method:'POST', headers:{{'Content-Type':'application/json'}},
                                      body: JSON.stringify(payload)}});
    if (!r.ok) throw new Error(r.status);
    document.getElementById('ok').textContent = 'saved to review-feedback.json on disk';
  }} catch (e) {{
    const a = document.createElement('a');
    a.href = URL.createObjectURL(new Blob([JSON.stringify(payload,null,2)],{{type:'application/json'}}));
    a.download = 'review-feedback.json'; a.click();
    document.getElementById('ok').textContent = 'no server running - downloaded instead; move it into the round directory';
  }}
}}
</script></body></html>'''

    (out / "review.html").write_text(html)
    (out / "review-map.json").write_text(json.dumps(unblind, indent=2))
    print(f"wrote {out}/review.html and review-map.json")
    if args.no_serve:
        return

    class Handler(http.server.BaseHTTPRequestHandler):
        done = False

        def log_message(self, *a):
            pass

        def do_GET(self):
            body = html.encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def do_POST(self):
            n = int(self.headers.get("Content-Length", 0))
            payload = self.rfile.read(n)
            try:
                json.loads(payload)  # refuse to write a corrupt submission
            except json.JSONDecodeError:
                self.send_response(400)
                self.end_headers()
                return
            (out / "review-feedback.json").write_bytes(payload)
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"ok")
            Handler.done = True

    srv = http.server.HTTPServer(("127.0.0.1", args.port), Handler)
    print(f"review server: http://127.0.0.1:{args.port}/  (submits write {out}/review-feedback.json; exits after one submission)")
    while not Handler.done:
        srv.handle_request()
    print(f"feedback received -> {out}/review-feedback.json")


if __name__ == "__main__":
    main()
