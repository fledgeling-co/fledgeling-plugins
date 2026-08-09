#!/usr/bin/env python3
"""Anonymise the 16 eval outputs for independent grading.

Each response is graded ALONE against its case's structural assertions, with no
indication of which arm produced it and without its counterpart in view. That is
blind enough for checkable assertions ("does it state a character count") and
avoids the incoherence that stripping skill names would cause: the skill arm
legitimately cites its own scripts, so redaction would mangle the text rather
than conceal it.

Ordering is deterministic (sorted by sha256 of the filename) so the mapping is
reproducible without storing a seed.
"""
import hashlib
import json
import shutil
from pathlib import Path

OUT = Path("/tmp/gh-evals/out")
ANON = Path("/tmp/gh-evals/anon")
CASES = ["G01", "G02", "G03", "G05", "L01", "L02", "L03", "L05"]

files = [OUT / f"{arm}-{c}.md" for c in CASES for arm in ("base", "skill")]
missing = [f.name for f in files if not f.exists()]
if missing:
    raise SystemExit(f"not ready, missing: {missing}")

ANON.mkdir(exist_ok=True)
order = sorted(files, key=lambda p: hashlib.sha256(p.name.encode()).hexdigest())
mapping = {}
for i, src in enumerate(order, 1):
    rid = f"r{i:02d}"
    shutil.copy(src, ANON / f"{rid}.md")
    arm, case = src.stem.split("-")
    mapping[rid] = {"arm": arm, "case": case, "bytes": src.stat().st_size}

Path("/tmp/gh-evals/mapping.json").write_text(json.dumps(mapping, indent=2))
print(f"{len(order)} responses anonymised into {ANON}")
for rid, m in mapping.items():
    print(f"  {rid}  case={m['case']}  ({m['bytes']}B)")
