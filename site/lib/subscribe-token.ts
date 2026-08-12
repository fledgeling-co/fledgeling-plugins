import "server-only";
import { createHmac, timingSafeEqual } from "node:crypto";

/**
 * Preference links.
 *
 * The link in every email has to identify one subscriber, be unguessable, and
 * work with no session — someone clicking unsubscribe from an email six months
 * later is not logged into anything.
 *
 * A signature over the id rather than a random token stored on the document:
 * nothing that grants access sits in the database, the links survive a restore,
 * and rotating the secret invalidates every outstanding link at once. The cost
 * is one env var, which is cheaper than a second index and a revocation story.
 */

function secret(): string {
  const value = process.env.SUBSCRIBE_TOKEN_SECRET;
  if (!value) throw new Error("SUBSCRIBE_TOKEN_SECRET is not set");
  return value;
}

export function hasTokenSecret(): boolean {
  return Boolean(process.env.SUBSCRIBE_TOKEN_SECRET);
}

function sign(id: string): string {
  return createHmac("sha256", secret()).update(id).digest("base64url");
}

/** `<id>.<signature>` — one path segment, safe in a URL, no encoding needed. */
export function mintToken(id: string): string {
  return `${id}.${sign(id)}`;
}

/** The id a token vouches for, or null. Never throws on malformed input. */
export function verifyToken(token: string): string | null {
  const dot = token.lastIndexOf(".");
  if (dot <= 0) return null;

  const id = token.slice(0, dot);
  const given = token.slice(dot + 1);

  let expected: string;
  try {
    expected = sign(id);
  } catch {
    return null; // no secret configured — nothing can be trusted, so nothing is
  }

  const a = Buffer.from(given);
  const b = Buffer.from(expected);
  // Length has to match before timingSafeEqual, which throws on a mismatch.
  // Comparing lengths first leaks only the length, which the format fixes anyway.
  if (a.length !== b.length) return null;
  return timingSafeEqual(a, b) ? id : null;
}

export function preferencesUrl(id: string, origin: string): string {
  return `${origin}/preferences/${mintToken(id)}`;
}
