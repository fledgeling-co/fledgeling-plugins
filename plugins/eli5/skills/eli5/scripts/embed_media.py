#!/usr/bin/env python3
"""
embed_media.py -- resize, re-encode and inline an image as a data: URI.

    python3 embed_media.py hero.png --max-width 1200 --format webp --alt "brass lock and key"

Writes an <img> tag to stdout and the encoded size to stderr. A 1024x1024 PNG straight from
an image model runs ~1.5 MB, which becomes ~2 MB of base64 in the artifact; at 1200px wide
in WebP the same picture is usually under 200 KB. The artifact runtime caps a rendered page
at 16 MB, and data: URIs count toward it.

Generated imagery earns its place by carrying the analogy's source domain. Caption it with
what it depicts and that it was generated -- a reader who mistakes an illustration for a
photograph of the real system has been misled by the artifact.

Needs Pillow. WebP support is checked at runtime rather than assumed.
"""

import argparse
import base64
import io
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    raise SystemExit("embed_media.py needs Pillow: python3 -m pip install pillow")

MIME = {"webp": "image/webp", "jpeg": "image/jpeg", "png": "image/png"}


def encode(path: Path, max_width: int, fmt: str, quality: int) -> bytes:
    img = Image.open(path)
    if img.width > max_width:
        height = round(img.height * max_width / img.width)
        img = img.resize((max_width, height), Image.LANCZOS)

    if fmt == "jpeg" and img.mode in ("RGBA", "P", "LA"):
        img = img.convert("RGB")

    buf = io.BytesIO()
    if fmt == "png":
        img.save(buf, format="PNG", optimize=True)
    else:
        img.save(buf, format=fmt.upper(), quality=quality, method=6 if fmt == "webp" else 0)
    return buf.getvalue()


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("path", type=Path)
    ap.add_argument("--max-width", type=int, default=1200)
    ap.add_argument("--format", choices=sorted(MIME), default="webp")
    ap.add_argument("--quality", type=int, default=82)
    ap.add_argument("--alt", default="", help="alt text; describe what the image shows")
    ap.add_argument("--class", dest="css_class", default="", help="class attribute for the tag")
    args = ap.parse_args()

    if not args.path.is_file():
        raise SystemExit(f"no such file: {args.path}")

    if args.format == "webp" and "WEBP" not in Image.registered_extensions().values():
        try:
            Image.new("RGB", (1, 1)).save(io.BytesIO(), format="WEBP")
        except Exception:
            raise SystemExit("this Pillow has no WebP encoder; rerun with --format jpeg")

    raw = encode(args.path, args.max_width, args.format, args.quality)
    b64 = base64.b64encode(raw).decode()

    cls = f' class="{args.css_class}"' if args.css_class else ""
    print(f'<img{cls} alt="{args.alt}" src="data:{MIME[args.format]};base64,{b64}">')

    original = args.path.stat().st_size
    print(
        f"{args.path.name}: {original:,} B -> {len(raw):,} B {args.format} "
        f"-> {len(b64):,} B base64 in the page",
        file=sys.stderr,
    )
    if len(b64) > 3_000_000:
        print("  over 3 MB encoded; lower --max-width or --quality", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
