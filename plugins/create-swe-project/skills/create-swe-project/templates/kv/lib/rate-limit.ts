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
 * The caller's IP, for limits on unauthenticated routes, taken only from a
 * header the deployment's own proxy writes (CP §6.4). On Vercel that is
 * x-real-ip, which the platform sets. Elsewhere it is the RIGHT-most
 * X-Forwarded-For entry, the one the nearest proxy (Caddy, a load balancer)
 * appended; every entry to its left came from the client and can be forged.
 * With neither, all callers share one bucket, which fails closed. Key
 * authenticated routes by user id instead (CP §6.11).
 */
export function clientIp(req: Request): string {
  if (process.env.VERCEL) {
    const real = req.headers.get('x-real-ip')?.trim();
    if (real) return real;
  }
  const appended = req.headers.get('x-forwarded-for')?.split(',').pop()?.trim();
  return appended || 'unknown';
}
