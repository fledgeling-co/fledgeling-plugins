import 'server-only';
import { createClient } from 'redis';
import { requireEnv } from './env';
import { logger } from './logger';

// node-redis, not ioredis: ioredis's own README points new projects here (BP §5).
// Reach for Redis only for concrete cross-request state: rate limits, one-time
// codes with a TTL, webhook idempotency keys.
function connect() {
  const client = createClient({ url: requireEnv('REDIS_URL') });
  client.on('error', (err: unknown) => logger.error({ err }, 'redis client error'));
  return client.connect();
}

export type Redis = Awaited<ReturnType<typeof connect>>;

const globalForRedis = globalThis as unknown as { _redis?: Promise<Redis> };

/**
 * Fails closed: a missing REDIS_URL throws on every deployed environment,
 * previews included (BP §5, CP §6.8). The connect promise is cached and cleared
 * on rejection, like db().
 */
export function redis(): Promise<Redis> {
  let pending = globalForRedis._redis;
  if (!pending) {
    pending = connect().catch((err: unknown) => {
      globalForRedis._redis = undefined;
      throw new Error('Redis connection failed', { cause: err });
    });
    globalForRedis._redis = pending;
  }
  return pending;
}
