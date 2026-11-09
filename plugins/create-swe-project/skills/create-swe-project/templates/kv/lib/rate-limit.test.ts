import { afterEach, describe, expect, it, vi } from 'vitest';
import { clientIp } from './rate-limit';

afterEach(() => vi.unstubAllEnvs());

const req = (headers: Record<string, string>) => new Request('http://app.test/', { headers });

describe('clientIp', () => {
  it('ignores client-written entries and takes the one the proxy appended', () => {
    vi.stubEnv('VERCEL', '');
    expect(clientIp(req({ 'x-forwarded-for': '1.1.1.1, 2.2.2.2, 203.0.113.7' }))).toBe('203.0.113.7');
    expect(clientIp(req({ 'x-forwarded-for': '203.0.113.7', 'x-real-ip': '9.9.9.9' }))).toBe('203.0.113.7');
  });

  it('trusts x-real-ip only on Vercel, which sets it', () => {
    vi.stubEnv('VERCEL', '1');
    expect(clientIp(req({ 'x-real-ip': '198.51.100.4', 'x-forwarded-for': '1.1.1.1' }))).toBe('198.51.100.4');
  });

  it('puts callers with no proxy header in one shared bucket', () => {
    vi.stubEnv('VERCEL', '');
    expect(clientIp(req({}))).toBe('unknown');
  });
});
