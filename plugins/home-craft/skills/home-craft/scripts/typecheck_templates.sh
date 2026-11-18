#!/usr/bin/env bash
# Type-checks the bundled Swift templates against the installed iOS SDK, at two deployment
# targets, under Swift 6 language mode. Exit 0 only when every pass is clean.
#   scripts/typecheck_templates.sh            # templates bundled with this skill
#   scripts/typecheck_templates.sh <app-dir> <widget-dir>
set -u
here="$(cd "$(dirname "$0")/.." && pwd)"
app_dir="${1:-$here/templates/App}"
widget_dir="${2:-$here/templates/Widget}"

if ! sdk="$(xcrun --sdk iphoneos --show-sdk-path 2>/dev/null)"; then
  echo "typecheck: no iOS SDK found (xcrun --sdk iphoneos failed); install Xcode 27 or later" >&2
  exit 2
fi
echo "typecheck: SDK $(xcrun --sdk iphoneos --show-sdk-version)"

status=0
for target in arm64-apple-ios26.0 arm64-apple-ios27.0; do
  for dir in "$app_dir" "$widget_dir"; do
    files=("$dir"/*.swift)
    if [ ! -e "${files[0]}" ]; then
      echo "typecheck: no .swift files in $dir" >&2
      status=1
      continue
    fi
    if output="$(xcrun swiftc -typecheck -sdk "$sdk" -target "$target" -swift-version 6 \
        -parse-as-library "${files[@]}" 2>&1)"; then
      if printf '%s' "$output" | grep -q 'warning:'; then
        printf '%s\n' "$output"
        echo "typecheck: WARN $(basename "$dir") @ $target"
        status=1
      else
        echo "typecheck: PASS $(basename "$dir") @ $target"
      fi
    else
      printf '%s\n' "$output"
      echo "typecheck: FAIL $(basename "$dir") @ $target"
      status=1
    fi
  done
done
exit $status
