import { beforeEach, describe, expect, it, vi } from 'vitest';
import { FakeRedis } from '@/test/fake-redis';

const state = vi.hoisted(() => ({ redis: undefined as unknown, sent: [] as string[] }));

vi.mock('@/lib/redis', () => ({ redis: async () => state.redis }));
vi.mock('@/lib/email', () => ({ sendSignInCodeEmail: async (to: string) => void state.sent.push(to) }));
vi.mock('next/server', async (importOriginal) => ({
  ...(await importOriginal<typeof import('next/server')>()),
  after: (task: () => unknown) => void task(),
}));

const { POST } = await import('./route');

function request(body: string, origin = 'http://app.test'): Parameters<typeof POST>[0] {
  return new Request('http://app.test/api/auth/request-code', {
    method: 'POST',
    headers: { origin, 'content-type': 'application/json', 'x-real-ip': '203.0.113.7' },
    body,
  }) as Parameters<typeof POST>[0];
}

beforeEach(() => {
  vi.stubEnv('NEXT_PUBLIC_APP_URL', 'http://app.test');
  vi.stubEnv('JWT_SECRET', 'test-secret-that-is-at-least-thirty-two-chars');
  state.redis = new FakeRedis();
  state.sent = [];
});

describe('POST /api/auth/request-code', () => {
  it('refuses a cross-site origin before reading anything', async () => {
    const res = await POST(request('{"email":"a@b.co"}', 'https://evil.example'));
    expect(res.status).toBe(403);
    expect(state.sent).toEqual([]);
  });

  it('answers malformed JSON with 400', async () => {
    expect((await POST(request('{nope'))).status).toBe(400);
  });

  it('gives every address the identical response', async () => {
    const a = await POST(request('{"email":"known@b.co"}'));
    const b = await POST(request('{"email":"never-seen@b.co"}'));
    expect([a.status, b.status]).toEqual([200, 200]);
    expect(await a.json()).toEqual(await b.json());
  });

  it('stops sending after three requests per email while still answering 200', async () => {
    const statuses = [];
    for (let i = 0; i < 4; i += 1) statuses.push((await POST(request('{"email":"a@b.co"}'))).status);
    expect(statuses).toEqual([200, 200, 200, 200]);
    expect(state.sent).toEqual(['a@b.co', 'a@b.co', 'a@b.co']);
  });
});
