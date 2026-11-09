import 'server-only';
import { NextResponse } from 'next/server';
import type { z } from 'zod';
import { appEnv } from './env';

// The shared front of every state-changing route (CP §6.1, BP §10): origin check
// → rate limit → size-capped, Zod-validated body → handler. Malformed input is
// a 4xx, never a 500 (CP §4 A10).

export function jsonError(message: string, status: number): Response {
  return NextResponse.json({ error: message }, { status });
}

/**
 * True when the request's Origin is this app's configured origin, compared as
 * scheme + host + port. A literal `Origin === Host` compare always fails, since
 * Origin carries the scheme. Webhooks and native clients send no Origin and
 * authenticate with a signature or token instead.
 */
export function isAllowedOrigin(req: Request): boolean {
  const header = req.headers.get('origin');
  if (!header) return false;
  let origin: URL;
  try {
    origin = new URL(header);
  } catch {
    return false;
  }
  const configured = process.env.NEXT_PUBLIC_APP_URL;
  if (configured && URL.canParse(configured) && new URL(configured).origin === origin.origin) return true;
  // Local dev reaches the app through Caddy and directly on its port.
  const local = origin.hostname === 'localhost' || origin.hostname === '127.0.0.1' || origin.hostname.endsWith('.localhost');
  return appEnv() === 'development' && local;
}

export type Parsed<T> = { ok: true; data: T } | { ok: false; response: Response };

/** Read a JSON body under a byte cap and parse it with `schema`. */
export async function readJson<S extends z.ZodType>(
  req: Request,
  schema: S,
  maxBytes = 16_384,
): Promise<Parsed<z.infer<S>>> {
  const declared = Number(req.headers.get('content-length') ?? '0');
  if (declared > maxBytes) return { ok: false, response: jsonError('Payload too large', 413) };
  const text = await req.text();
  if (Buffer.byteLength(text) > maxBytes) return { ok: false, response: jsonError('Payload too large', 413) };
  let body: unknown;
  try {
    body = JSON.parse(text);
  } catch {
    return { ok: false, response: jsonError('Malformed JSON', 400) };
  }
  const parsed = schema.safeParse(body);
  if (!parsed.success) {
    const issues = parsed.error.issues.map((i) => ({ path: i.path.join('.'), message: i.message }));
    return { ok: false, response: NextResponse.json({ error: 'Invalid body', issues }, { status: 400 }) };
  }
  return { ok: true, data: parsed.data };
}
