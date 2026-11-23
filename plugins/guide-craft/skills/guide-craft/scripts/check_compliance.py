#!/usr/bin/env python3
"""Pre-flight App Store (Apple Guidelines 4.1(c), 5.2.1, 5.2.2) and publisher IP compliance gate.

Validates a companion app release manifest JSON:
{
  "publisher": "riot|blizzard|bungie|ea|capcom|ggg|valve|epic|activision|other",
  "app_name": "Draftline: Tactics & Builds",
  "subtitle": "Season 14 comps & decks",
  "display_name": "Draftline",
  "trademarks": ["League of Legends", "VALORANT", "TFT", "Riot"],
  "disclaimer": "...",
  "has_written_license": false,
  "has_production_api_key": true,
  "monetization": {"subscriptions": false, "free_tier": true, "web_banner_ads": false, "overlay_ads": false, "voice_ads": false, "paid_download": false},
  "uses_client_memory_read": false,
  "uses_official_art_in_store_shots": false,
  "embeds_api_key_in_binary": false
}

Exit 0 when compliant, exit 1 on any policy violation.
"""

from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys
from typing import Any, Dict, List

PUBLISHER_RULES: Dict[str, Dict[str, Any]] = {
    "riot": {
        "required_disclaimer_substr": "Legal Jibber Jabber",
        "forbids_store_without_key_or_license": True,
        "allows_subscriptions_with_free_tier": True,
        "forbids_overlay_ads": True,
        "forbids_memory_read": True,
        "forbids_embedded_key": True,
    },
    "blizzard": {
        "forbids_all_monetization": True,
        "forbids_paid_download": True,
        "forbids_subscriptions": True,
        "forbids_embedded_key": True,
    },
    "bungie": {
        "forbids_any_revenue_without_license": True,
    },
    "ea": {
        "required_disclaimer_substr": "not endorsed by or affiliated with EA",
        "forbids_subscriptions": True,
        "forbids_paid_download": True,
        "allows_web_banner_ads": True,
    },
    "capcom": {
        "forbidden_disclaimer_substr": "©CAPCOM",
        "forbids_subscriptions": True,
        "forbids_paid_download": True,
        "forbids_commercial_entity": True,
    },
    "ggg": {
        "required_disclaimer_substr": "Grinding Gear Games",
        "forbids_subscriptions": True,
        "forbids_paid_download": True,
        "forbids_embedded_key": True,
        "forbids_memory_read": True,
    },
    "valve": {
        "forbids_subscriptions": True,
        "forbids_paid_download": True,
    },
    "epic": {
        "required_disclaimer_substr": "not official and is not endorsed by Epic",
        "forbids_subscriptions": True,
        "forbids_paid_download": True,
    },
    "activision": {
        "forbids_subscriptions": True,
        "forbids_paid_download": True,
    },
    "other": {},
}


def check_manifest(m: Dict[str, Any]) -> Tuple[List[str], List[str]]:
    errors: List[str] = []
    warnings: List[str] = []

    pub = (m.get("publisher") or "other").strip().lower()
    if pub not in PUBLISHER_RULES:
        errors.append(f"unknown publisher '{pub}'; choose one of {sorted(PUBLISHER_RULES)}")
        return errors, warnings
    rules = PUBLISHER_RULES[pub]

    name = (m.get("app_name") or "").strip()
    subtitle = (m.get("subtitle") or "").strip()
    display_name = (m.get("display_name") or "").strip()
    disclaimer = (m.get("disclaimer") or "").strip()
    licensed = bool(m.get("has_written_license", False))
    prod_key = bool(m.get("has_production_api_key", False))
    mon = m.get("monetization") or {}

    if not name:
        errors.append("app_name is empty")
    elif len(name) > 30:
        errors.append(f"app_name '{name}' is {len(name)} chars (Apple App Store limit is 30)")
    if len(subtitle) > 30:
        errors.append(f"subtitle '{subtitle}' is {len(subtitle)} chars (Apple App Store limit is 30)")
    if display_name and len(display_name) > 15:
        warnings.append(f"display_name '{display_name}' ({len(display_name)} chars) may truncate under iOS home-screen icon")

    if not licensed:
        for tm in m.get("trademarks") or []:
            t = str(tm).strip()
            if not t:
                continue
            if re.search(rf"\b{re.escape(t)}\b", name, re.IGNORECASE):
                errors.append(
                    f"Apple 4.1(c) / 5.2.1 risk: trademark '{t}' appears inside app_name '{name}' without written license"
                )
        if m.get("uses_official_art_in_store_shots"):
            errors.append("Apple 5.2.1 risk: uses_official_art_in_store_shots=true without written license")

    non_endorse_ok = any(
        phrase in disclaimer.lower()
        for phrase in ("unofficial", "not affiliated", "not endorsed", "does not endorse", "isn't affiliated")
    )
    if not disclaimer or not non_endorse_ok:
        errors.append("disclaimer must explicitly state unofficial / non-affiliated / not endorsed status")

    if mon.get("voice_ads"):
        errors.append("Apple Guidelines prohibit ads inside Siri/voice/Shortcut responses")
    if m.get("embeds_api_key_in_binary"):
        errors.append("embeds_api_key_in_binary=true: proxy publisher API keys through backend, never ship inside iOS binary")
    if m.get("uses_client_memory_read"):
        errors.append("uses_client_memory_read=true: client memory reads violate Riot (Oct 2026 lockdown) / GGG / anti-cheat policies")

    if not licensed:
        req_sub = rules.get("required_disclaimer_substr")
        if req_sub and req_sub.lower() not in disclaimer.lower():
            errors.append(f"{pub} policy requires disclaimer containing '{req_sub}'")
        forb_sub = rules.get("forbidden_disclaimer_substr")
        if forb_sub and forb_sub.lower() in disclaimer.lower():
            errors.append(f"{pub} policy explicitly forbids '{forb_sub}' in fan disclaimers")
        if rules.get("forbids_store_without_key_or_license") and not prod_key:
            errors.append(f"{pub} forbids App Store/Google Play distribution without written license or approved Production API key")
        if rules.get("forbids_overlay_ads") and mon.get("overlay_ads"):
            errors.append(f"{pub} forbids ads in overlays or loading screens")
        if rules.get("forbids_subscriptions") and mon.get("subscriptions"):
            errors.append(f"{pub} forbids paid subscriptions / paywalls without written license")
        if rules.get("forbids_paid_download") and mon.get("paid_download"):
            errors.append(f"{pub} forbids paid app downloads without written license")
        if rules.get("allows_subscriptions_with_free_tier") and mon.get("subscriptions") and not mon.get("free_tier"):
            errors.append(f"{pub} requires a free player tier alongside any paid subscription")
        if rules.get("forbids_any_revenue_without_license") and any(
            mon.get(k) for k in ("subscriptions", "paid_download", "web_banner_ads", "overlay_ads")
        ):
            errors.append(f"{pub} treats any API-driven revenue (including ads) as commercial requiring prior written permission")
        if rules.get("forbids_all_monetization") and any(
            mon.get(k) for k in ("subscriptions", "paid_download", "web_banner_ads", "overlay_ads")
        ):
            errors.append(f"{pub} API Terms forbid paid tiers and API-driven ad monetization")
        if rules.get("forbids_commercial_entity") and m.get("submitted_by_corporation"):
            warnings.append(f"{pub} Fan Content Guidelines (Nov 2025) restrict fan works to individuals or unincorporated groups")

    return errors, warnings


def self_test() -> int:
    good_riot = {
        "publisher": "riot",
        "app_name": "Draftline: Builds & Matchups",
        "subtitle": "Season 16 runes & counters",
        "display_name": "Draftline",
        "trademarks": ["League of Legends", "Riot", "VALORANT"],
        "disclaimer": "Draftline was created under Riot Games' 'Legal Jibber Jabber' policy using assets owned by Riot Games. Riot Games does not endorse or sponsor this project.",
        "has_written_license": False,
        "has_production_api_key": True,
        "monetization": {"subscriptions": True, "free_tier": True, "web_banner_ads": False, "overlay_ads": False, "voice_ads": False, "paid_download": False},
        "uses_client_memory_read": False,
        "uses_official_art_in_store_shots": False,
        "embeds_api_key_in_binary": False,
    }
    errs, _ = check_manifest(good_riot)
    assert not errs, f"expected compliant Riot manifest to pass, got {errs}"

    bad_capcom = {
        "publisher": "capcom",
        "app_name": "Street Fighter 6 Ultimate Frame Data Companion",
        "subtitle": "All SF6 hitboxes, framedata & season 3 counters",
        "display_name": "SF6 Companion",
        "trademarks": ["Street Fighter", "Capcom"],
        "disclaimer": "Unofficial fan guide. ©CAPCOM.",
        "has_written_license": False,
        "monetization": {"subscriptions": True, "voice_ads": True},
        "uses_client_memory_read": True,
        "uses_official_art_in_store_shots": True,
        "embeds_api_key_in_binary": True,
    }
    errs_bad, _ = check_manifest(bad_capcom)
    expected = [
        "limit is 30",
        "Apple 4.1(c)",
        "uses_official_art_in_store_shots",
        "©CAPCOM",
        "paid subscriptions",
        "voice/Shortcut",
        "embeds_api_key_in_binary",
        "uses_client_memory_read",
    ]
    for token in expected:
        assert any(token in e for e in errs_bad), f"missing expected compliance failure {token!r} in {errs_bad}"

    bad_bungie = {
        "publisher": "bungie",
        "app_name": "Vaultsmith: Roll Appraiser",
        "subtitle": "Perks & builds",
        "trademarks": ["Destiny", "Bungie"],
        "disclaimer": "Unofficial community companion, not affiliated with Bungie.",
        "has_written_license": False,
        "monetization": {"web_banner_ads": True},
    }
    errs_bungie, _ = check_manifest(bad_bungie)
    assert any("any API-driven revenue" in e for e in errs_bungie), f"expected Bungie ad refusal, got {errs_bungie}"

    print(f"check_compliance.py --self-test: PASS (good Riot fixture ok; bad Capcom {len(errs_bad)}/8 violations + Bungie ad violation caught)")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="Check Apple 4.1(c)/5.2 and publisher IP/monetization compliance.")
    ap.add_argument("manifest_json", nargs="?", help="Path to app release manifest JSON")
    ap.add_argument("--self-test", action="store_true")
    args = ap.parse_args()

    if args.self_test:
        return self_test()
    if not args.manifest_json:
        ap.error("provide manifest_json or --self-test")

    manifest = json.loads(pathlib.Path(args.manifest_json).read_text(encoding="utf-8"))
    errors, warnings = check_manifest(manifest)
    for w in warnings:
        print(f"WARN {w}")
    if errors:
        for e in errors:
            print(f"FAIL {e}")
        print(f"check_compliance: {len(errors)} violation(s)")
        return 1
    print(f"check_compliance: ok ({manifest.get('publisher', 'other')}, 0 violations)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
