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
import re
import sys
from pathlib import Path

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
    ap.add_argument("kind", choices=sorted(CLASSIC | {"three"}))
    ap.add_argument("path", type=Path)
    ap.add_argument("--name", help="value for data-vendor (defaults to kind)")
    args = ap.parse_args()

    if not args.path.is_file():
        raise SystemExit(f"no such file: {args.path}")

    source = args.path.read_text(encoding="utf-8")
    name = args.name or args.kind

    if args.kind in CLASSIC:
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
