import "server-only";

/**
 * Best-effort rate limiting for the public search endpoint.
 *
 * Honest about what this is: an in-process sliding window. Serverless instances
 * do not share memory, so a caller spread across instances gets more than the
 * stated allowance. It blunts a burst from one client and bounds the spend of a
 * single warm instance; it is not the durable control.
 *
 * The durable control is the Vercel WAF rate-limit rule on /api/search, which is
 * configured in the dashboard and applies before a function is ever invoked.
 */

const PER_MINUTE = Number(process.env.SEARCH_RATE_PER_MINUTE ?? 8);
const DAILY_CEILING = Number(process.env.SEARCH_DAILY_CEILING ?? 2000);
const WINDOW_MS = 60_000;

const hits = new Map<string, number[]>();
let dayStamp = "";
let dayCount = 0;

export type Verdict = { ok: true } | { ok: false; reason: "per-ip" | "daily" };

export function check(key: string, now = Date.now()): Verdict {
  const today = new Date(now).toISOString().slice(0, 10);
  if (today !== dayStamp) {
    dayStamp = today;
    dayCount = 0;
  }

  if (dayCount >= DAILY_CEILING) return { ok: false, reason: "daily" };

  const recent = (hits.get(key) ?? []).filter((stamp) => now - stamp < WINDOW_MS);
  if (recent.length >= PER_MINUTE) {
    hits.set(key, recent);
    return { ok: false, reason: "per-ip" };
  }

  recent.push(now);
  hits.set(key, recent);
  dayCount += 1;

  // Keep the map from growing without bound on a long-lived instance.
  if (hits.size > 5_000) {
    for (const [entry, stamps] of hits) {
      if (stamps.every((stamp) => now - stamp >= WINDOW_MS)) hits.delete(entry);
    }
  }

  return { ok: true };
}

/** Identify the caller. Behind Vercel the leftmost x-forwarded-for is the client. */
export function callerKey(request: Request): string {
  return callerKeyFromHeaders(request.headers);
}

/**
 * The same derivation from a bare Headers.
 *
 * A Server Action has `headers()` rather than a Request, and both lanes need to
 * land on the same key or one caller counts twice under two identities.
 */
export function callerKeyFromHeaders(headers: Headers): string {
  const forwarded = headers.get("x-forwarded-for");
  const first = forwarded?.split(",")[0]?.trim();
  return first || headers.get("x-real-ip") || "unknown";
}
