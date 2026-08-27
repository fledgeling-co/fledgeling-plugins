#!/usr/bin/env python3
"""
vendor_lib.py -- inline a JavaScript library into a single-file explainer.

    python3 vendor_lib.py gsap   /path/to/gsap.min.js          > block.html
    python3 vendor_lib.py three  /path/to/three.module.min.js  > block.html
    python3 vendor_lib.py plugin /path/to/ScrollTrigger.min.js --name gsap-scrolltrigger

Every block carries a `data-vendor` attribute. lint_explainer.py excludes those blocks from
the containment, animation-frame and word-count scans, because Three.js ships three fetch()
calls in its loaders that would otherwise fail no-network-calls on every 3D artifact.

Classic scripts (GSAP and its plugins) inline unchanged; they assign globals.

Three.js ships ES modules only, and only a SINGLE-FILE build inlines. A split build
(three.module.min.js re-exporting ./three.core.min.js) fails two ways in Chromium from
file://, both silently as far as the reader is concerned:

    inlined directly   Access to script at 'file:///.../three.core.min.js' blocked by CORS
    via importmap      Failed to resolve module specifier "./three.core.min.js"

so this script refuses a split build rather than emitting one that half-works. For a single
file build it rewrites the trailing `export{A as B, ...}` into `const THREE = {B: A, ...}`,
which puts the library and the artifact code in one module scope with no importmap.
"""

import argparse
import hashlib
import os
import re
import sys
import urllib.request
from pathlib import Path

# Pinned, checksummed, fetched once into a cache outside the repo. Verified byte-identical
# to the copies these versions ship in node_modules.
LIBS = {
    "gsap": (
        "https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/gsap.min.js",
        "96c01b81f44a3290e2b4532f55e2c9534b2adc43273a19f3756b2cb41f0fd0b6", 72435),
    "scrolltrigger": (
        "https://cdn.jsdelivr.net/npm/gsap@3.13.0/dist/ScrollTrigger.min.js",
        "308219390e5e3b84cda0c481e70caa9820883ae10bda44e6e9a149a81aac4b3f", 44157),
    "three": (
        "https://cdn.jsdelivr.net/npm/three@0.169.0/build/three.module.min.js",
        "f7cee3c7533449a1505cc12cb5128b89e3d4fd3d7ea62b05f9f5464a217472ee", 687458),
}

CACHE = Path(os.environ.get("ELI5_VENDOR_CACHE",
                            Path.home() / ".cache" / "eli5-vendor"))


def cached(kind: str) -> Path:
    """Fetch once, verify, reuse. Nothing is redistributed in this repo and nothing is
    fetched at page-render time -- this runs at build time, and the artifact stays inline."""
    url, sha, size = LIBS[kind]
    dest = CACHE / f"{kind}-{sha[:12]}.js"
    if dest.is_file():
        return dest
    CACHE.mkdir(parents=True, exist_ok=True)
    print(f"fetching {kind} from {url}", file=sys.stderr)
    with urllib.request.urlopen(url, timeout=90) as r:
        blob = r.read()
    got = hashlib.sha256(blob).hexdigest()
    if got != sha:
        raise SystemExit(
            f"checksum mismatch for {kind}\n  expected {sha}\n  got      {got}\n"
            f"Refusing to inline a file that is not the pinned version.")
    dest.write_bytes(blob)
    print(f"cached {len(blob):,} bytes at {dest}", file=sys.stderr)
    return dest

CLASSIC = {"gsap", "plugin", "classic"}


def emit_classic(source: str, name: str) -> str:
    return f'<script data-vendor="{name}">\n{source}\n</script>'


def rewrite_three(source: str) -> str:
    """Turn the trailing ESM export list into a THREE namespace object."""
    head = source[:2000]
    if re.search(r"(?:^|[;\n])\s*import[\s{*]", head):
        raise SystemExit(
            "refusing: this is a SPLIT three build -- it imports a sibling module, which "
            "cannot resolve from file:// or from a data: URL.\n"
            "Use a single-file build (three r169's build/three.module.min.js is one), or "
            "concatenate three.core.min.js ahead of it and strip the import line first."
        )

    m = re.search(r"export\s*\{([^}]*)\}\s*;?\s*$", source)
    if not m:
        raise SystemExit(
            "refusing: no trailing `export{...}` found, so the public names cannot be "
            "recovered. Check this is three.module.min.js rather than a bundle."
        )

    pairs = []
    for part in m.group(1).split(","):
        part = part.strip()
        if not part:
            continue
        if " as " in part:
            internal, public = part.split(" as ", 1)
            pairs.append(f"{public.strip()}:{internal.strip()}")
        else:
            pairs.append(f"{part}:{part}")

    return source[: m.start()] + "const THREE={" + ",".join(pairs) + "};"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("kind", choices=sorted(CLASSIC | {"three", "scrolltrigger"}))
    ap.add_argument("path", type=Path, nargs="?",
                    help="a local .js file; omit it to fetch and cache the pinned version")
    ap.add_argument("--name", help="value for data-vendor (defaults to kind)")
    args = ap.parse_args()

    if args.path is None:
        if args.kind not in LIBS:
            raise SystemExit(f"no pinned version for '{args.kind}'; give a local path")
        args.path = cached(args.kind)
    if not args.path.is_file():
        raise SystemExit(f"no such file: {args.path}")

    source = args.path.read_text(encoding="utf-8")
    # The GSAP licence permits free commercial use and forbids removing its notices, so the
    # header comment travels with the code into the artifact. Never strip it.
    if args.kind in ("gsap", "scrolltrigger", "plugin") and "@license" not in source[:600]:
        raise SystemExit("refusing: the licence header is missing from this GSAP file")
    name = args.name or args.kind

    if args.kind in CLASSIC or args.kind == "scrolltrigger":
        block = emit_classic(source, name)
    else:
        # The library gets its own block and publishes THREE on window, so artifact code
        # lives in a separate <script> the gate can still read. Author code inside a
        # data-vendor block would be excluded from the pointer, animation-frame and
        # network scans along with the library.
        block = (
            f'<script type="module" data-vendor="{name}">\n'
            f"{rewrite_three(source)}\n"
            f"window.THREE = THREE;\n"
            f"</script>"
        )

    print(block)
    print(
        f"{args.path.name}: {len(source):,} bytes inlined as data-vendor=\"{name}\"",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
