#!/usr/bin/env python3
"""Generate assets/timeline.js from timeline.json so scenes and the sound cue sheet share one clock.

    python3 timeline_js.py <project>/timeline.json <project>/assets/timeline.js

timeline.json holds film-absolute seconds: a top-level "duration" plus named beats, usually
grouped by scene. The output defines window.TL with the same data, frozen so a scene cannot
change it at render time. Exits 1 with a reason when the JSON is unreadable or has no duration.
"""

import json
import sys


def main(argv):
    if len(argv) != 3:
        sys.exit("usage: timeline_js.py <timeline.json> <out.js>")
    src, dst = argv[1], argv[2]
    try:
        with open(src, encoding="utf-8") as f:
            data = json.load(f)
    except (OSError, json.JSONDecodeError) as exc:
        sys.exit(f"timeline_js: cannot read {src}: {exc}")
    duration = data.get("duration") if isinstance(data, dict) else None
    if not isinstance(duration, (int, float)) or duration <= 0:
        sys.exit("timeline_js: timeline.json needs a positive top-level \"duration\" in seconds")
    body = json.dumps(data, indent=2, ensure_ascii=False)
    js = (
        "// Generated from timeline.json by motion-craft's timeline_js.py. Edit the JSON, not this file.\n"
        "(function (tl) {\n"
        "  function freeze(o) { Object.values(o).forEach(function (v) { if (v && typeof v === 'object') freeze(v); }); return Object.freeze(o); }\n"
        "  window.TL = freeze(tl);\n"
        f"}})({body});\n"
    )
    with open(dst, "w", encoding="utf-8") as f:
        f.write(js)
    print(f"wrote {dst}: duration {duration}s, {len(data) - 1} top-level groups")


if __name__ == "__main__":
    main(sys.argv)
