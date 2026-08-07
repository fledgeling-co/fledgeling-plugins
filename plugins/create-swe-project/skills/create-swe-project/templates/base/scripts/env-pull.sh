#!/usr/bin/env bash
# Fill .env.local values from 1Password. Reads OP_ACCOUNT + OP_VAULT from the
# env file itself, then resolves every `KEY=op://...` reference with `op read`.
# Secrets flow op → file directly; they never pass through an agent's context.
# Graduate keys to op:// references over time, e.g.:
#   JWT_SECRET=op://<vault>/<project> JWT_SECRET/credential
set -euo pipefail
ENV_FILE="${1:-apps/web/.env.local}"
[ -f "$ENV_FILE" ] || { echo "no $ENV_FILE — copy the .env.example first" >&2; exit 1; }
command -v op >/dev/null || { echo "1Password CLI (op) not installed: brew install 1password-cli" >&2; exit 1; }

account="$(grep -E '^OP_ACCOUNT=' "$ENV_FILE" | cut -d= -f2- || true)"
vault="$(grep -E '^OP_VAULT=' "$ENV_FILE" | cut -d= -f2- || true)"
[ -n "$account" ] || { echo "OP_ACCOUNT is empty in $ENV_FILE" >&2; exit 1; }

tmp="$(mktemp)"
while IFS= read -r line; do
  key="${line%%=*}"; val="${line#*=}"
  if [[ "$val" == op://* ]]; then
    resolved="$(op read --account "$account" "$val")"
    printf '%s=%s\n' "$key" "$resolved" >> "$tmp"
  else
    printf '%s\n' "$line" >> "$tmp"
  fi
done < "$ENV_FILE"
mv "$tmp" "$ENV_FILE"
echo "resolved op:// references in $ENV_FILE (account: $account, vault: ${vault:-n/a})"
