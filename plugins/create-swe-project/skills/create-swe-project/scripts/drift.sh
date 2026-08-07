#!/usr/bin/env bash
# slipway drift <project-dir>: compare files against .slipway/state.json hashes.
# "modified" files are user-owned changes an upgrade must never overwrite;
# "unchanged" files are safely replaceable; "missing" were deleted on purpose
# (respect that). The shadcn lesson: without this record, upgrades are blind.
set -euo pipefail
PROJECT="${1:?usage: drift.sh <project-dir>}"
python3 - "$PROJECT" <<'PY'
import hashlib, json, pathlib, sys
root = pathlib.Path(sys.argv[1])
state = json.loads((root / ".slipway" / "state.json").read_text())
modified, unchanged, missing = [], [], []
for rel, meta in state.items():
    p = root / rel
    if not p.exists():
        missing.append(rel)
    elif hashlib.sha256(p.read_bytes()).hexdigest() == meta["sha256"]:
        unchanged.append(rel)
    else:
        modified.append(rel)
print(json.dumps({"modified": modified, "missing": missing,
                  "unchanged_count": len(unchanged), "total": len(state)}, indent=1))
PY
