import { afterEach, describe, expect, it, vi } from 'vitest';
import { logger, redact } from './logger';

afterEach(() => vi.restoreAllMocks());

describe('redact', () => {
  it('redacts sensitive keys at any depth', () => {
    const out = redact({ user: { id: 'u1', email: 'a@b.co', session: { refreshToken: 'r' } }, headers: { cookie: 'c' } });
    expect(out).toEqual({ user: { id: 'u1', email: '[redacted]', session: { refreshToken: '[redacted]' } }, headers: '[redacted]' });
  });

  it('keeps an error readable without leaking a nested secret in its cause', () => {
    const err = new Error('outer', { cause: { apiKey: 'k', status: 502 } });
    expect(redact({ err })).toEqual({ err: { name: 'Error', message: 'outer', cause: { apiKey: '[redacted]', status: 502 } } });
  });
});

describe('logger', () => {
  it('writes one JSON line with the secret removed', () => {
    const spy = vi.spyOn(console, 'error').mockImplementation(() => undefined);
    logger.error({ password: 'hunter2', route: '/api/x' }, 'failed');
    const line = JSON.parse(String(spy.mock.calls[0]?.[0])) as Record<string, unknown>;
    expect(line).toMatchObject({ level: 'error', msg: 'failed', route: '/api/x', password: '[redacted]' });
  });
});
