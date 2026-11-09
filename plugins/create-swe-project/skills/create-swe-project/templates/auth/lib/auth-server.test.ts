import { beforeEach, describe, expect, it, vi } from 'vitest';
import { FakeRedis } from '@/test/fake-redis';

const state = vi.hoisted(() => ({ redis: undefined as unknown, jar: new Map<string, string>() }));

vi.mock('@/lib/redis', () => ({ redis: async () => state.redis }));
vi.mock('next/headers', () => ({
  cookies: async () => ({
    get: (name: string) => (state.jar.has(name) ? { name, value: state.jar.get(name) } : undefined),
    set: (name: string, value: string) => void state.jar.set(name, value),
    delete: (name: string | { name: string }) => void state.jar.delete(typeof name === 'string' ? name : name.name),
  }),
}));

const auth = await import('./auth-server');

beforeEach(() => {
  vi.stubEnv('JWT_SECRET', 'test-secret-that-is-at-least-thirty-two-chars');
  state.redis = new FakeRedis();
  state.jar.clear();
});

describe('sign-in codes', () => {
  it('a code works exactly once', async () => {
    await auth.storeSignInCode('a@b.co', '123456');
    expect(await auth.consumeSignInCode('a@b.co', '123456')).toBe(true);
    expect(await auth.consumeSignInCode('a@b.co', '123456')).toBe(false);
  });

  it('two concurrent verifies of one code succeed once between them', async () => {
    await auth.storeSignInCode('a@b.co', '123456');
    const results = await Promise.all([auth.consumeSignInCode('a@b.co', '123456'), auth.consumeSignInCode('a@b.co', '123456')]);
    expect(results.filter(Boolean)).toHaveLength(1);
  });

  it('purges the code after five wrong guesses, so the right code then fails', async () => {
    await auth.storeSignInCode('a@b.co', '123456');
    for (let i = 0; i < 5; i += 1) expect(await auth.consumeSignInCode('a@b.co', '000000')).toBe(false);
    expect(await auth.consumeSignInCode('a@b.co', '123456')).toBe(false);
  });

  it('allows three code requests per email per hour', async () => {
    const allowed = [];
    for (let i = 0; i < 4; i += 1) allowed.push(await auth.allowCodeRequest('a@b.co'));
    expect(allowed).toEqual([true, true, true, false]);
  });
});

describe('sessions', () => {
  it('reads back the session it minted, and rejects a tampered token', async () => {
    await auth.mintSession({ userId: 'u1', email: 'a@b.co' });
    expect(await auth.getSession()).toEqual({ userId: 'u1', email: 'a@b.co' });
    const [name, token] = [...state.jar.entries()].find(([n]) => n.endsWith('session')) ?? [];
    state.jar.set(String(name), `${token}x`);
    expect(await auth.getSession()).toBeNull();
  });

  it('a refresh token rotates once; replaying the old one fails', async () => {
    await auth.mintSession({ userId: 'u1', email: 'a@b.co' });
    const refreshName = [...state.jar.keys()].find((n) => n.endsWith('refresh')) ?? '';
    const original = state.jar.get(refreshName) ?? '';
    expect(await auth.rotateRefresh()).toEqual({ userId: 'u1', email: 'a@b.co' });
    state.jar.set(refreshName, original);
    expect(await auth.rotateRefresh()).toBeNull();
  });

  it('refuses a JWT secret too short to carry entropy', async () => {
    vi.stubEnv('JWT_SECRET', 'short');
    await expect(auth.mintSession({ userId: 'u1', email: 'a@b.co' })).rejects.toThrow(/at least 32/);
  });
});
