import "server-only";

/**
 * Model wiring for the search lane.
 *
 * Model IDs live in one object so a swap is one line. The `provider/model`
 * string form routes through Vercel AI Gateway, which is the only path this
 * lane uses — there is no direct-provider fallback, because a credential for
 * one provider cannot serve a model from another and a silent wrong-provider
 * call is worse than an honest 503.
 */

export const MODELS = {
  /** Search ranking: small, fast, and cheap enough to sit on a public URL. */
  search: "openai/gpt-5.6-luna",
} as const;

/** Reasoning effort per call. Ranking sixteen items against one query is a
 *  shallow task; more thinking buys nothing and costs latency on every query. */
export const EFFORT = {
  search: "low",
} as const;

export function hasCredentials(): boolean {
  return Boolean(process.env.AI_GATEWAY_API_KEY || process.env.VERCEL_OIDC_TOKEN);
}

/**
 * The gateway takes the `provider/model` string directly. Returning it unchanged
 * keeps the model id the single thing that changes when the model changes.
 */
export function resolveModel(id: string): string {
  return id;
}
