"""Crop evidence snippets out of a source PDF, with highlighter marks baked into the pixels.

    python3 crop_snippets.py --pdf source/resume.pdf --spec snippets.json --out review/img/

Every finding on a review page cites the document it came from. A snippet that is a real
crop of the person's own PDF, with the words in question highlighted, lets the reader
qualify the finding without opening the file. Marks are composited into the PNG rather
than positioned with CSS, so they survive being copied into any page or message.

Needs Pillow and poppler's `pdftotext` and `pdftoppm`.

`snippets.json`:

    {"page_images": {"1": "review/img/resume-1.png", "2": "review/img/resume-2.png"},
     "thumbs": {"1": "r-page1-thumb"},
     "snippets": [
       {"name": "r-header", "page": 1,
        "box": [34, 58, 572, 300],
        "from_phrase": "PROFESSIONAL EXPERIENCE", "from_edge": "top", "from_offset": -8,
        "highlight": ["more than 20 years", "jane@example.com"]}
     ]}

`box` is [x0, y0, x1, y1] in PDF points. Any of the four may instead be resolved from text:
`from_phrase` with `from_edge` ("top" or "bottom") and `from_offset` replaces y1, and
`to_phrase` / `to_edge` / `to_offset` replaces y0. Phrase lookup is whole-token and
case-insensitive, so a phrase that appears twice needs `occurrence`.

Render the page images first:
    pdftoppm -r 150 -png source/resume.pdf review/img/resume
"""
import re, subprocess, html, json, os, sys, argparse
from PIL import Image, ImageDraw

SCALE = 150 / 72  # pdftoppm -r 150 against PDF points
norm = lambda t: html.unescape(t).strip(".,;:()").lower()

def page_words(pdf):
    out = subprocess.run(["pdftotext", "-bbox", pdf, "-"],
                         capture_output=True, text=True).stdout
    return [[(float(x0), float(y0), float(x1), float(y1), t)
             for x0, y0, x1, y1, t in re.findall(
                 r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">(.*?)</word>',
                 page)]
            for page in out.split("<page ")[1:]]

def hits(words, phrase):
    """Every occurrence of `phrase`, as a list of per-line bounding boxes."""
    toks = [norm(t) for t in phrase.split()]
    found = []
    for i in range(len(words) - len(toks) + 1):
        if all(norm(words[i + j][4]) == toks[j] for j in range(len(toks))):
            seg = words[i:i + len(toks)]
            lines = {}
            for w in seg:
                lines.setdefault(round(w[1]), []).append(w)
            found.append([(min(w[0] for w in l), min(w[1] for w in l),
                           max(w[2] for w in l), max(w[3] for w in l))
                          for l in lines.values()])
    return found

def locate(words, phrase, occurrence=0):
    h = hits(words, phrase)
    if not h:
        sys.exit(f"phrase not found in this page: {phrase!r}")
    return h[occurrence][0]

def crop(image, words, box, out_path, highlight=(), pad=10, colour=(255, 205, 0, 105)):
    x0, y0, x1, y1 = box
    im = Image.open(image).convert("RGBA")
    W, H = im.size
    overlay = Image.new("RGBA", im.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)
    marks = 0
    for phrase in highlight:
        for occurrence in hits(words, phrase):
            inside = [(a, b, c, d) for (a, b, c, d) in occurrence
                      if a >= x0 - 2 and c <= x1 + 2 and b >= y0 - 2 and d <= y1 + 2]
            for (a, b, c, d) in inside:
                draw.rounded_rectangle((a * SCALE - 3, b * SCALE - 2,
                                        c * SCALE + 3, d * SCALE + 2),
                                       radius=4, fill=colour)
                marks += 1
            # A phrase that wraps past the box edge loses its outside lines' marks silently,
            # and the crop still passes the no-marks check. Say so.
            if inside and len(inside) < len(occurrence):
                print(f"WARN {os.path.basename(out_path)}: {phrase!r} is marked on "
                      f"{len(inside)} of its {len(occurrence)} lines; widen the box or anchor "
                      f"its edge on the phrase", file=sys.stderr)
    im = Image.alpha_composite(im, overlay).convert("RGB")
    crop_box = (max(0, int(x0 * SCALE - pad)), max(0, int(y0 * SCALE - pad)),
                min(W, int(x1 * SCALE + pad)), min(H, int(y1 * SCALE + pad)))
    im.crop(crop_box).quantize(160, method=Image.Quantize.MEDIANCUT,
                               dither=Image.Dither.NONE).save(out_path, optimize=True)
    size = f"{crop_box[2]-crop_box[0]}x{crop_box[3]-crop_box[1]}"
    print(f"{out_path}  {size}  marks={marks}")
    return marks

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf", required=True)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()
    spec = json.load(open(args.spec))
    pages = page_words(args.pdf)
    os.makedirs(args.out, exist_ok=True)
    unmarked = []
    for s in spec["snippets"]:
        page = int(s["page"])
        words = pages[page - 1]
        image = spec["page_images"][str(page)]
        box = list(s.get("box", [0, 0, 0, 0]))
        if "from_phrase" in s:
            loc = locate(words, s["from_phrase"], s.get("occurrence", 0))
            box[3] = loc[1 if s.get("from_edge", "top") == "top" else 3] + s.get("from_offset", 0)
        if "to_phrase" in s:
            loc = locate(words, s["to_phrase"], s.get("to_occurrence", 0))
            box[1] = loc[1 if s.get("to_edge", "top") == "top" else 3] + s.get("to_offset", 0)
        marks = crop(image, words, box, os.path.join(args.out, s["name"] + ".png"),
                     highlight=s.get("highlight", []), pad=s.get("pad", 10))
        if s.get("highlight") and marks == 0:
            unmarked.append(s["name"])
    for page, stem in (spec.get("thumbs") or {}).items():
        im = Image.open(spec["page_images"][str(page)]).convert("RGB")
        im.thumbnail((560, 760))
        im.quantize(128, dither=Image.Dither.NONE).save(
            os.path.join(args.out, stem + ".png"), optimize=True)
        print(f"{stem}.png  thumbnail")
    if unmarked:
        print("FAIL no highlight landed in: " + ", ".join(unmarked), file=sys.stderr)
        print("The phrase is outside the crop box or spelled differently in the PDF.",
              file=sys.stderr)
        sys.exit(1)
