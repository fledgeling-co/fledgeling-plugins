#!/usr/bin/env python3
"""Copy the model roster into every plugin that uses it, or check the copies are current.

    python3 scripts/sync_model_roster.py           # write the copies
    python3 scripts/sync_model_roster.py --check   # exit 1 if any copy differs from the source

The source is models/roster.json and models/roster.py. An installed plugin cannot read another
plugin's files or this repository's root, so each consumer carries its own copy in its skill's
scripts/ directory. The consumers are the keys of "consumers" in roster.json; add a plugin there
and run this script to give it the roster.
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "models"
FILES = ("roster.json", "roster.py")


def targets():
    roster = json.loads((SRC / "roster.json").read_text(encoding="utf-8"))
    for name, entry in roster["consumers"].items():
        if isinstance(entry, dict) and entry.get("path"):
            d = ROOT / entry["path"]
        else:
            d = ROOT / "plugins" / name / "skills" / name / "scripts"
        if not (ROOT / "plugins" / name).is_dir():
            sys.exit(f"sync_model_roster: {name} is a consumer in roster.json but plugins/{name} does not exist")
        existing = d / "roster.py"
        # flagship ships an unrelated scripts/roster.py; never overwrite a file that is not ours
        if existing.exists() and "Fledgeling's model roster" not in existing.read_text(encoding="utf-8"):
            sys.exit(f"sync_model_roster: {existing} exists and is not the model roster; refusing to overwrite it")
        yield name, d


def main():
    check = "--check" in sys.argv[1:]
    stale = []
    for name, d in targets():
        for f in FILES:
            src, dst = SRC / f, d / f
            same = dst.exists() and dst.read_bytes() == src.read_bytes()
            if check:
                if not same:
                    stale.append(str(dst.relative_to(ROOT)))
            elif not same:
                d.mkdir(parents=True, exist_ok=True)
                shutil.copy2(src, dst)
                print(f"wrote {dst.relative_to(ROOT)}")
    if check:
        for s in stale:
            print(f"STALE {s}")
        print(f"{len(stale)} stale copy(ies); run scripts/sync_model_roster.py" if stale else "roster copies are current")
        return 1 if stale else 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
