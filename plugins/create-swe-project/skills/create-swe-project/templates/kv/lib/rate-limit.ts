import 'server-only';
import { redis } from './redis';

/**
 * Fixed-window counter. INCR and EXPIRE NX run in one MULTI, so a crash between
 * them can't strand a key with no TTL and lock someone out for good (CP §6.11).
 * Returns true while the caller is within `limit` for this window.
 */
export async function rateLimit(bucket: string, id: string, limit: number, windowSeconds: number): Promise<boolean> {
  const key = `rl:${bucket}:${id}`;
  const client = await redis();
  const [count] = await client.multi().incr(key).expire(key, windowSeconds, 'NX').exec();
  return Number(count) <= limit;
}

/**
 * The caller's IP, for limits on unauthenticated routes. Outside Vercel's edge
 * x-forwarded-for is attacker-controlled (CP §6.4), so treat this as defence in
 * depth, never the only guard on a path that costs money. Key authenticated
 * routes by user id instead (CP §6.11).
 */
export function clientIp(req: Request): string {
  return req.headers.get('x-real-ip') ?? req.headers.get('x-forwarded-for')?.split(',')[0]?.trim() ?? 'unknown';
}
