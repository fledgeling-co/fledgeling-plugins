#!/usr/bin/env python3
"""Gate a live voice briefing against character/token caps and zero-drop entity retention.

Prevents two measured MW4 failures:
1. Exceeding GPT-Live's 16,384-token session.instructions cap (checked via strict char cap
   and conservative 3.6 chars/token estimate).
2. Silently dropping a meta pick, map, hardware card, or key setting when compressing the guide.

Exit 0 when within budget and 100% of required entities appear (case-insensitive); exit 1 otherwise.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import sys
import tempfile
from typing import List, Tuple

CHARS_PER_TOKEN = 3.6
HARD_TOKEN_CAP = 16384


def check_briefing(
    briefing_text: str,
    required_entities: List[str],
    max_chars: int = 50000,
    max_tokens: int = 14000,
) -> Tuple[int, int, List[str]]:
    chars = len(briefing_text)
    est_tokens = int(chars / CHARS_PER_TOKEN) + 1
    errors: List[str] = []

    if chars == 0:
        errors.append("briefing text is empty")
    if chars > max_chars:
        errors.append(f"briefing length {chars:,} chars exceeds cap {max_chars:,}")
    if est_tokens > min(max_tokens, HARD_TOKEN_CAP):
        errors.append(f"estimated tokens {est_tokens:,} exceeds cap {min(max_tokens, HARD_TOKEN_CAP):,}")
    if not required_entities:
        errors.append("required_entities list is empty (zero denominator is not a pass)")

    lower_text = briefing_text.lower()
    missing = [e for e in required_entities if e.strip() and e.strip().lower() not in lower_text]
    if missing:
        errors.append(f"dropped {len(missing)} of {len(required_entities)} entities: {', '.join(missing[:12])}")
    return chars, est_tokens, errors


def self_test() -> int:
    entities = ["Patriot XMR", "VEL 46", "RTX 5090", "Shipment", "Frame Generation"]
    good_text = "Season 1 briefing: Patriot XMR leads ARs, VEL 46 leads SMGs. RTX 5090 runs 4K. Shipment map. Turn Frame Generation off."
    c, t, errs = check_briefing(good_text, entities)
    assert not errs and c > 0 and t < 14000, f"expected good briefing pass, got {errs}"

    too_long = ("word " * 12000) + good_text
    _, _, errs_len = check_briefing(too_long, entities, max_chars=50000, max_tokens=14000)
    assert any("exceeds cap" in e for e in errs_len), f"expected length cap failure, got {errs_len}"

    dropped = "Season 1 briefing: Patriot XMR leads ARs. RTX 5090 runs 4K."
    _, _, errs_drop = check_briefing(dropped, entities)
    assert any("dropped 3 of 5 entities" in e for e in errs_drop), f"expected 3 dropped entities, got {errs_drop}"

    _, _, errs_zero = check_briefing(good_text, [])
    assert any("zero denominator" in e for e in errs_zero), f"expected zero-denominator error, got {errs_zero}"

    print("check_briefing.py --self-test: PASS (good fixture ok; overflow, entity-drop, and zero-denominator fixtures caught)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Validate voice briefing size cap and entity retention.")
    ap.add_argument("--briefing", help="Path to generated briefing text file")
    ap.add_argument("--entities", help="Path to JSON array of required entity strings")
    ap.add_argument("--max-chars", type=int, default=50000)
    ap.add_argument("--max-tokens", type=int, default=14000)
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if not args.briefing or not args.entities:
        ap.error("provide --briefing and --entities, or --self-test")

    text = pathlib.Path(args.briefing).read_text(encoding="utf-8")
    entities = json.loads(pathlib.Path(args.entities).read_text(encoding="utf-8"))
    if not isinstance(entities, list):
        print("FAIL --entities must be a JSON array of strings")
        return 1
    chars, tokens, errors = check_briefing(text, [str(x) for x in entities], args.max_chars, args.max_tokens)
    if errors:
        for e in errors:
            print(f"FAIL {e}")
        return 1
    print(f"check_briefing: ok ({chars:,} chars, ~{tokens:,} tokens, {len(entities)}/{len(entities)} entities retained)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
