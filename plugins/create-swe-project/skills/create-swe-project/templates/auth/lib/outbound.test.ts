import { afterEach, describe, expect, it, vi } from 'vitest';
import { canReceiveOutbound } from './outbound';

afterEach(() => vi.unstubAllEnvs());

describe('canReceiveOutbound', () => {
  it('delivers to anyone in production', () => {
    vi.stubEnv('APP_ENV', 'production');
    expect(canReceiveOutbound('customer@example.com')).toBe(true);
  });

  it('delivers only to allowlisted domains elsewhere, matching the whole domain', () => {
    vi.stubEnv('APP_ENV', 'preview');
    vi.stubEnv('OUTBOUND_ALLOWED_DOMAINS', 'team.example');
    expect(canReceiveOutbound('me@team.example')).toBe(true);
    expect(canReceiveOutbound('me@TEAM.example')).toBe(true);
    expect(canReceiveOutbound('customer@example.com')).toBe(false);
    expect(canReceiveOutbound('me@evilteam.example')).toBe(false);
  });

  it('delivers to nobody outside production when the allowlist is empty', () => {
    vi.stubEnv('APP_ENV', 'development');
    vi.stubEnv('OUTBOUND_ALLOWED_DOMAINS', '');
    expect(canReceiveOutbound('me@team.example')).toBe(false);
  });
});
