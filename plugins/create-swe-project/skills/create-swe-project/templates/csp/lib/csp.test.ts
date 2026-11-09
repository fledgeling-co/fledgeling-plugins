import { describe, expect, it } from 'vitest';
import { buildCsp } from './csp';

describe('buildCsp', () => {
  it('nonces scripts and never allows inline script', () => {
    const csp = buildCsp('abc', { dev: false, https: true });
    const script = csp.split('; ').find((d) => d.startsWith('script-src')) ?? '';
    expect(script).toBe("script-src 'self' 'nonce-abc' 'strict-dynamic'");
    expect(csp).toContain('upgrade-insecure-requests');
    expect(csp).toContain("frame-ancestors 'none'");
  });

  it('adds unsafe-eval only in development and upgrades only over https', () => {
    const csp = buildCsp('abc', { dev: true, https: false });
    expect(csp).toContain("'unsafe-eval'");
    expect(csp).not.toContain('upgrade-insecure-requests');
  });
});
