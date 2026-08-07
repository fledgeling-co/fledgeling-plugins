#!/usr/bin/env bash
# slipway doctor: what this machine can actually do, as JSON. Run before an
# interview so module recommendations match reality (no macos module without
# xcodegen, no op seeding without the CLI). Read-only; no network calls.
set -euo pipefail
have() { command -v "$1" >/dev/null 2>&1; }
ver() { "$@" 2>/dev/null | head -1 | tr -d '"' || echo ""; }
json_kv() { printf '"%s": {"present": %s, "version": "%s"}' "$1" "$2" "$3"; }
entries=""
add() { entries="$entries${entries:+, }$1"; }
add "$(json_kv node   "$(have node && echo true || echo false)"   "$(ver node --version)")"
add "$(json_kv pnpm   "$(have pnpm && echo true || echo false)"   "$(ver pnpm --version)")"
add "$(json_kv git    "$(have git && echo true || echo false)"    "$(ver git --version)")"
add "$(json_kv cargo  "$(have cargo && echo true || echo false)"  "$(ver cargo --version)")"
add "$(json_kv xcodegen "$(have xcodegen && echo true || echo false)" "$(ver xcodegen --version)")"
add "$(json_kv xcodebuild "$(have xcodebuild && echo true || echo false)" "$(ver xcodebuild -version)")"
add "$(json_kv docker "$(have docker && echo true || echo false)" "$(ver docker --version)")"
add "$(json_kv caddy  "$(have caddy && echo true || echo false)"  "$(ver caddy version)")"
add "$(json_kv op     "$(have op && echo true || echo false)"     "$(ver op --version)")"
add "$(json_kv gh     "$(have gh && echo true || echo false)"     "$(gh --version 2>/dev/null | head -1)")"
add "$(json_kv maestro "$(have maestro && echo true || echo false)" "")"
add "$(json_kv fastlane "$(have fastlane && echo true || echo false)" "$(ver fastlane --version | tail -1)")"
add "$(json_kv vercel "$(have vercel && echo true || echo false)" "$(ver vercel --version)")"
printf '{%s, "machine_caddy_confd": %s}\n' "$entries" \
  "$([ -d /opt/homebrew/etc/caddy/conf.d ] && echo true || echo false)"
