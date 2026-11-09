import { afterEach, describe, expect, it, vi } from 'vitest';
import { z } from 'zod';
import { isAllowedOrigin, readJson } from './http';

afterEach(() => vi.unstubAllEnvs());

function post(body: string, headers: Record<string, string> = {}): Request {
  return new Request('http://app.test/api/x', { method: 'POST', body, headers });
}

describe('isAllowedOrigin', () => {
  it('accepts only the configured scheme, host and port', () => {
    vi.stubEnv('NEXT_PUBLIC_APP_URL', 'https://app.example.com');
    const req = (origin?: string) => post('{}', origin ? { origin } : {});
    expect(isAllowedOrigin(req('https://app.example.com'))).toBe(true);
    expect(isAllowedOrigin(req('http://app.example.com'))).toBe(false);
    expect(isAllowedOrigin(req('https://app.example.com:8443'))).toBe(false);
    expect(isAllowedOrigin(req('https://evil.example.com'))).toBe(false);
    expect(isAllowedOrigin(req('app.example.com'))).toBe(false);
    expect(isAllowedOrigin(req())).toBe(false);
  });

  it('allows a localhost origin in development only', () => {
    vi.stubEnv('NEXT_PUBLIC_APP_URL', 'http://app.localhost');
    const req = post('{}', { origin: 'http://localhost:3000' });
    vi.stubEnv('APP_ENV', 'preview');
    expect(isAllowedOrigin(req)).toBe(false);
    vi.stubEnv('APP_ENV', 'development');
    expect(isAllowedOrigin(req)).toBe(true);
  });
});

describe('readJson', () => {
  const schema = z.object({ name: z.string().max(10) });

  it('returns the parsed body', async () => {
    const r = await readJson(post('{"name":"ok"}'), schema);
    expect(r).toEqual({ ok: true, data: { name: 'ok' } });
  });

  it('answers malformed JSON with 400, not a crash', async () => {
    const r = await readJson(post('{not json'), schema);
    expect(r.ok ? 200 : r.response.status).toBe(400);
  });

  it('answers a schema violation with 400 and the field path', async () => {
    const r = await readJson(post('{"name":"far too long a name"}'), schema);
    if (r.ok) throw new Error('expected a rejection');
    expect(r.response.status).toBe(400);
    expect(await r.response.json()).toMatchObject({ issues: [{ path: 'name' }] });
  });

  it('answers an oversized body with 413 before parsing it', async () => {
    const r = await readJson(post(JSON.stringify({ name: 'x'.repeat(100) })), schema, 32);
    expect(r.ok ? 200 : r.response.status).toBe(413);
  });

  it('stops reading a chunked body with no Content-Length once it passes the cap', async () => {
    let pulled = 0;
    const stream = new ReadableStream<Uint8Array>({
      pull(controller) {
        pulled += 1;
        if (pulled > 1000) controller.close();
        else controller.enqueue(new Uint8Array(64).fill(32));
      },
    });
    const req = new Request('http://app.test/api/x', { method: 'POST', body: stream, duplex: 'half' } as RequestInit);
    const r = await readJson(req, schema, 256);
    expect(r.ok ? 200 : r.response.status).toBe(413);
    expect(pulled).toBeLessThan(20);
  });

  it('answers a malformed Content-Length with 400', async () => {
    const r = await readJson(post('{"name":"ok"}', { 'content-length': '-5' }), schema);
    expect(r.ok ? 200 : r.response.status).toBe(400);
  });
});
