"""Probe harness: build a variant of icon.svg with constants overridden, without
touching build_icon.py. Reads the generator's source, rewrites the named
top-level constant assignments and the output path, and execs it in the assets
directory so its relative asset reads still work.

    python3 w6.py out.svg GRAIN_AMP_A=0 GRAIN_AMP_B=0
"""
import re
import sys
import pathlib

ASSETS = pathlib.Path(__file__).resolve().parents[3]
src = (ASSETS / 'build_icon.py').read_text()

out = sys.argv[1]
for kv in sys.argv[2:]:
    k, v = kv.split('=', 1)
    pat = re.compile(rf'^{re.escape(k)}( *)=[^\n]*$', re.M)
    if not pat.search(src):
        raise SystemExit(f'constant {k} not found at top level')
    src = pat.sub(lambda m: f'{k}{m.group(1)}= {v}', src, count=1)

src = src.replace('(ASSETS / "icon.svg").write_text(svg)',
                  f'(ASSETS / {out!r}).write_text(svg)')
g = {'__file__': str(ASSETS / 'build_icon.py'), '__name__': '__probe__'}
exec(compile(src, 'build_icon.py(probe)', 'exec'), g)
