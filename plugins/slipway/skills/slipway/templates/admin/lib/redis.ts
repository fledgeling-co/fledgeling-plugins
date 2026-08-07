import 'server-only';
import Redis from 'ioredis';

const globalForRedis = globalThis as unknown as { _redis?: Redis };

export function redis(): Redis {
  const url = process.env.REDIS_URL;
  if (!url) throw new Error('REDIS_URL is not set');
  globalForRedis._redis ??= new Redis(url, { maxRetriesPerRequest: 2 });
  return globalForRedis._redis;
}
