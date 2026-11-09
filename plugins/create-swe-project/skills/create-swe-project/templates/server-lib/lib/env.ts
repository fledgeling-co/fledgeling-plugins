import 'server-only';

// One typed module for env access (CP §6.8). Secrets and security-sensitive
// values fail closed: a missing variable throws rather than falling back.

export type AppEnv = 'production' | 'preview' | 'development';

/**
 * The runtime environment, resolved on the server, never in client code (BP §24:
 * Next sets NODE_ENV=production for staging builds too). Each permissive
 * behaviour needs a positive signal: `production` only from VERCEL_ENV or
 * APP_ENV, `development` only from `next dev` or APP_ENV. Anything else is
 * `preview`, the restrictive middle, so a deploy with no signal neither
 * enables dev login nor emails real customers.
 */
export function appEnv(): AppEnv {
  const explicit = process.env.APP_ENV;
  if (explicit === 'production' || explicit === 'preview' || explicit === 'development') return explicit;
  if (process.env.VERCEL_ENV === 'production') return 'production';
  if (process.env.VERCEL_ENV) return 'preview';
  return process.env.NODE_ENV === 'development' ? 'development' : 'preview';
}

export function requireEnv(name: string): string {
  const value = process.env[name];
  if (!value) throw new Error(`${name} is not set`);
  return value;
}

/** A signing secret: required, and long enough to carry real entropy. */
export function requireSecret(name: string): string {
  const value = requireEnv(name);
  if (value.length < 32) {
    throw new Error(`${name} must be at least 32 characters (generate one with: openssl rand -base64 32)`);
  }
  return value;
}

/** `||`, not `??`: a key copied from .env.example is present but empty (CP §6.8). */
export function optionalEnv(name: string, fallback: string): string {
  return process.env[name] || fallback;
}
