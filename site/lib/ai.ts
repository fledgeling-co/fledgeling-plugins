import "server-only";
import { anthropic } from "@ai-sdk/anthropic";

/**
 * Model wiring for the search lane.
 *
 * Model IDs live in one object so a swap is one line. A `provider/model` string
 * routes through Vercel AI Gateway when a gateway credential is present; without
 * one it falls back to the direct Anthropic API, where the version separator is a
 * dash rather than a dot.
 */

export const MODELS = {
  /** Search ranking: small, fast, and cheap enough to sit on a public URL. */
  search: "anthropic/claude-haiku-4.5",
} as const;

/** Direct-API ids, which are dated and cannot be derived from the gateway id. */
const DIRECT_IDS: Record<string, string> = {
  "anthropic/claude-haiku-4.5": "claude-haiku-4-5-20251001",
};

export function hasCredentials(): boolean {
  return Boolean(
    process.env.AI_GATEWAY_API_KEY ||
      process.env.VERCEL_OIDC_TOKEN ||
      process.env.ANTHROPIC_API_KEY,
  );
}

export function resolveModel(id: string) {
  if (process.env.AI_GATEWAY_API_KEY || process.env.VERCEL_OIDC_TOKEN) return id;
  return anthropic(DIRECT_IDS[id] ?? id.replace(/^anthropic\//, "").replace(/\./g, "-"));
}
