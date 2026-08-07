import 'server-only';
import Redis from 'ioredis';

// Fail closed in prod: a missing REDIS_URL throws on first call rather than
// silently degrading (BP §5). Only reach for Redis for concrete cross-request
// state: rate limits, one-time codes with TTL, webhook idempotency keys.
const globalForRedis = globalThis as unknown as { _redis?: Redis };

export function redis(): Redis {
  const url = process.env.REDIS_URL;
  if (!url) throw new Error('REDIS_URL is not set');
  globalForRedis._redis ??= new Redis(url, { maxRetriesPerRequest: 2 });
  return globalForRedis._redis;
}
