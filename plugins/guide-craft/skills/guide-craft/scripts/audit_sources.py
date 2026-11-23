#!/usr/bin/env python3
"""Audit guide source resolution, independent publisher counts, and telemetry sample validity.

Expected JSON shape:
{
  "sources": [
    {"id": "r1", "url": "https://...", "publisher": "activision", "kind": "official"}
  ],
  "publisher_aliases": {"codmunity.gg": "stat-cluster-1", "mw4intel.app": "stat-cluster-1"},
  "recommendations": [
    {
      "id": "ar-pick",
      "core": true,
      "confidence": "high",
      "sources": ["r1", "r2"],
      "telemetry": {"wins": 120, "games": 220, "bracket": "Emerald+", "patch": "16.17"}
    }
  ]
}

Checks:
1. Every recommendation source id resolves in sources.
2. Independent publisher count collapses domain/channel duplicates and cloned stat-site aliases,
   and excludes automated research runs (kind == "automated_research").
3. Core recommendations fail when confidence == "low" (triggers Round-2 deep research)
   or when independent publishers < min_publishers (default 2) unless marked single_source_ok.
4. Telemetry rows compute 95% Wilson score lower bound and fail if missing bracket/patch or n < min_games (default 50).

Exit 0 when clean, exit 1 on any hard failure.
"""

from __future__ import annotations

import argparse
import json
import math
import pathlib
import sys
import tempfile
from urllib.parse import urlparse
from typing import Any, Dict, List, Set, Tuple


def wilson_lower_bound(wins: int, games: int, z: float = 1.959963984540054) -> float:
    if games <= 0:
        return 0.0
    p = wins / games
    denom = 1.0 + (z * z) / games
    center = p + (z * z) / (2.0 * games)
    margin = z * math.sqrt((p * (1.0 - p) + (z * z) / (4.0 * games)) / games)
    return max(0.0, (center - margin) / denom)


def canonical_publisher(src: Dict[str, Any], aliases: Dict[str, str]) -> str | None:
    if src.get("kind") == "automated_research":
        return None
    pub = (src.get("publisher") or "").strip().lower()
    if not pub:
        host = urlparse(src.get("url", "")).netloc.lower()
        pub = host[4:] if host.startswith("www.") else host
    if not pub:
        return None
    return aliases.get(pub, pub)


def audit_payload(data: Dict[str, Any], min_publishers: int = 2, min_games: int = 50) -> Tuple[List[str], List[str]]:
    sources = {s["id"]: s for s in data.get("sources", []) if isinstance(s, dict) and s.get("id")}
    aliases = {k.lower(): v.lower() for k, v in (data.get("publisher_aliases") or {}).items()}
    recs = data.get("recommendations") or []
    errors: List[str] = []
    warnings: List[str] = []
    cited: Set[str] = set()

    if not sources:
        errors.append("sources list is empty")
    if not recs:
        errors.append("recommendations list is empty")

    for rec in recs:
        rid = rec.get("id", "<unnamed>")
        rec_sources = rec.get("sources") or []
        if not rec_sources:
            errors.append(f"{rid}: no sources cited")
            continue
        pubs: Set[str] = set()
        for sid in rec_sources:
            if sid not in sources:
                errors.append(f"{rid}: unresolved source id {sid}")
            else:
                cited.add(sid)
                pub = canonical_publisher(sources[sid], aliases)
                if pub:
                    pubs.add(pub)

        conf = (rec.get("confidence") or "").strip().lower()
        is_core = bool(rec.get("core", True))
        if is_core and conf == "low":
            errors.append(f"{rid}: core pick is low confidence (run Round-2 research before shipping)")
        if is_core and len(pubs) < min_publishers and not rec.get("single_source_ok"):
            errors.append(
                f"{rid}: only {len(pubs)} independent publisher(s) after deduplication ({sorted(pubs)}); need >= {min_publishers}"
            )

        tel = rec.get("telemetry")
        if isinstance(tel, dict):
            games = int(tel.get("games", 0))
            wins = int(tel.get("wins", 0))
            if not tel.get("bracket"):
                errors.append(f"{rid}: telemetry missing rank/mode bracket")
            if not tel.get("patch"):
                errors.append(f"{rid}: telemetry missing patch or hotfix version")
            if games < min_games:
                errors.append(f"{rid}: telemetry sample n={games} below minimum floor {min_games}")
            elif wins > games or wins < 0:
                errors.append(f"{rid}: invalid telemetry wins={wins} for games={games}")
            else:
                lb = wilson_lower_bound(wins, games)
                warnings.append(f"{rid}: raw WR={wins/games:.1%}, 95% Wilson lower bound={lb:.1%} (n={games})")

    uncited = sorted(set(sources) - cited)
    if uncited:
        warnings.append(f"{len(uncited)} uncited source(s): {', '.join(uncited[:10])}")
    return errors, warnings


def self_test() -> int:
    good = {
        "sources": [
            {"id": "r1", "url": "https://www.callofduty.com/patchnotes", "publisher": "activision", "kind": "official"},
            {"id": "r2", "url": "https://youtube.com/watch?v=abc", "publisher": "thexclusiveace", "kind": "measured"},
            {"id": "r3", "url": "https://u.gg/lol/champions/ahri", "publisher": "u.gg", "kind": "official_telemetry"},
        ],
        "publisher_aliases": {"codmunity.gg": "stat-model-1", "mw4intel.app": "stat-model-1"},
        "recommendations": [
            {
                "id": "ar-pick",
                "core": True,
                "confidence": "high",
                "sources": ["r1", "r2"],
            },
            {
                "id": "mid-pick",
                "core": True,
                "confidence": "high",
                "sources": ["r1", "r3"],
                "telemetry": {"wins": 115, "games": 200, "bracket": "Emerald+", "patch": "16.17"},
            },
        ],
    }
    errs, warns = audit_payload(good)
    assert not errs, f"expected clean good fixture, got {errs}"
    assert any("Wilson lower bound" in w for w in warns), f"expected Wilson readout, got {warns}"

    bad = {
        "sources": [
            {"id": "r1", "url": "https://codmunity.gg/ttk/mw4", "publisher": "codmunity.gg"},
            {"id": "r2", "url": "https://mw4intel.app/ttk", "publisher": "mw4intel.app"},
            {"id": "r3", "url": "https://local/run", "publisher": "dossier", "kind": "automated_research"},
        ],
        "publisher_aliases": {"codmunity.gg": "stat-model-1", "mw4intel.app": "stat-model-1"},
        "recommendations": [
            {
                "id": "echo-chamber-pick",
                "core": True,
                "confidence": "low",
                "sources": ["r1", "r2", "r3", "r99"],
                "telemetry": {"wins": 12, "games": 20},
            }
        ],
    }
    errs_bad, _ = audit_payload(bad)
    expected = ["unresolved source id r99", "low confidence", "only 1 independent publisher", "missing rank/mode bracket", "missing patch", "below minimum floor"]
    for token in expected:
        assert any(token in e for e in errs_bad), f"expected {token!r} in {errs_bad}"

    print(f"audit_sources.py --self-test: PASS (good fixture 0 errors; bad fixture {len(errs_bad)}/6 defect classes caught)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Audit source resolution, publisher deduplication, and telemetry floors.")
    ap.add_argument("json_path", nargs="?", help="Path to audit JSON file")
    ap.add_argument("--min-publishers", type=int, default=2)
    ap.add_argument("--min-games", type=int, default=50)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if not args.json_path:
        ap.error("provide a json_path or --self-test")

    data = json.loads(pathlib.Path(args.json_path).read_text(encoding="utf-8"))
    errors, warnings = audit_payload(data, min_publishers=args.min_publishers, min_games=args.min_games)
    for w in warnings:
        print(f"INFO {w}")
    if errors:
        for e in errors:
            print(f"FAIL {e}")
        print(f"audit_sources: {len(errors)} error(s)")
        return 1
    print(f"audit_sources: ok ({len(data.get('recommendations', []))} recommendations, 0 errors)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
