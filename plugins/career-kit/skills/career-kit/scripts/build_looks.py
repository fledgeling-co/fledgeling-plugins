"""Build the same résumé in several looks and a page to compare them.

    python3 build_looks.py <copy.md> <out-dir> [--looks classic,calibri-teal,aptos-clean,arial-roles]
        [--name "Jane Doe"] [--font-dir "/Applications/Microsoft Word.app/Contents/Resources/DFonts"]
        [--pages 2] [--docx-python /tmp/dv/bin/python] [--title "Jane's résumé"]

For each look it writes `<id>.html`, `<id>.pdf` (headless Chrome, served over a local HTTP port
so @font-face files load), `<id>.docx` when `--docx-python` names an interpreter with
python-docx, and `big-<id>-<n>.png` page images; then `viewer.html`, which shows one look's pages
side by side or stacked, with the same-height description for every look, tabs, arrows and the
arrow keys. It prints each look's page count and embedded fonts, and marks a look whose PDF runs
past `--pages` instead of hiding it, because a look that costs a page is a trade the person
should see.

The words never change between looks: only what `looks.py` lets vary does. Check the Word file's
page count in Word itself; this script cannot.
"""
import argparse, functools, html, http.server, json, os, pathlib, shutil, socketserver
import subprocess, sys, tempfile, threading

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from looks import LOOKS, get_look  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("src"); ap.add_argument("out")
ap.add_argument("--looks", default="classic,calibri-teal,aptos-clean,arial-roles")
ap.add_argument("--name", default="")
ap.add_argument("--font-dir", default="/Applications/Microsoft Word.app/Contents/Resources/DFonts")
ap.add_argument("--pages", type=int, default=2)
ap.add_argument("--docx-python", default="")
ap.add_argument("--title", default="Résumé looks")
ap.add_argument("--chrome", default="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome")
a = ap.parse_args()

ids = [x.strip() for x in a.looks.split(",") if x.strip()]
for i in ids:
    get_look(i)  # refuses an unknown look or one outside the bounds, before any work
out = pathlib.Path(a.out); out.mkdir(parents=True, exist_ok=True)
root = pathlib.Path(tempfile.mkdtemp(prefix="looks-"))
fonts = pathlib.Path(a.font_dir)
if fonts.is_dir():
    (root / "_fonts").symlink_to(fonts)

class Quiet(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *args):
        pass


handler = functools.partial(Quiet, directory=str(root))
srv = socketserver.TCPServer(("127.0.0.1", 0), handler)
threading.Thread(target=srv.serve_forever, daemon=True).start()
base = f"http://127.0.0.1:{srv.server_address[1]}"


def sh(*cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


rows = []
try:
    for i in ids:
        look = LOOKS[i]
        page = root / f"{i}.html"
        args = [sys.executable, str(HERE / "build_resume.py"), a.src, str(page), "--look", i]
        if a.name:
            args += ["--name", a.name]
        if (root / "_fonts").exists():
            args += ["--font-dir", "/_fonts"]
        r = sh(*args)
        if r.returncode:
            sys.exit(f"{i}: build_resume.py failed\n{r.stderr}")
        shutil.copy(page, out / f"{i}.html")
        pdf = out / f"{i}.pdf"
        sh(a.chrome, "--headless=new", "--no-pdf-header-footer", "--virtual-time-budget=4000",
           f"--print-to-pdf={pdf}", f"{base}/{i}.html")
        info = sh("pdfinfo", str(pdf)).stdout
        pages = int(next((l.split()[-1] for l in info.splitlines() if l.startswith("Pages:")), "0"))
        faces = sorted({l.split()[0].split("+")[-1] for l in sh("pdffonts", str(pdf)).stdout.splitlines()[2:] if l.strip()})
        for old in out.glob(f"big-{i}-*.png"):
            old.unlink()
        sh("pdftoppm", "-r", "100", "-png", str(pdf), str(out / f"big-{i}"))
        for n in range(1, pages + 1):  # pdftoppm pads page numbers when there are 10 or more
            for cand in (out / f"big-{i}-{n:02d}.png", out / f"big-{i}-{n:03d}.png"):
                if cand.exists():
                    cand.rename(out / f"big-{i}-{n}.png")
        if a.docx_python:
            d = sh(a.docx_python, str(HERE / "make_docx.py"), a.src, str(out / f"{i}.docx"), "--look", i,
                   *(["--name", a.name] if a.name else []))
            if d.returncode:
                print(f"{i}: make_docx.py failed: {d.stderr.strip()}")
        expected_face = look["font"].replace(" ", "")
        fell_back = not any(f.startswith(expected_face) for f in faces)
        rows.append(dict(id=i, tab=look["label"], name=look["label"], what=look["what"], pages=pages,
                         over=pages > a.pages, faces=faces, fellBack=fell_back))
        flag = " OVER" if pages > a.pages else ""
        fb = "  (typeface fell back: pass --font-dir)" if fell_back else ""
        print(f"{i}: {pages} pages{flag}; fonts: {' '.join(faces)}{fb}")
finally:
    srv.shutdown()
    shutil.rmtree(root, ignore_errors=True)

VIEWER = (HERE.parent / "assets" / "looks-viewer.html").read_text()
page = (VIEWER.replace("__TITLE__", html.escape(a.title))
        .replace("__LOOKS__", json.dumps(rows, ensure_ascii=False))
        .replace("__PAGES__", str(a.pages)))
(out / "viewer.html").write_text(page)
print(f"wrote {out / 'viewer.html'}")
