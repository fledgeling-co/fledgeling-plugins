import { NextResponse, type NextRequest } from 'next/server';
import { z } from 'zod';
import { isAllowedOrigin, jsonError, readJson } from '@/lib/http';
import { clientIp, rateLimit } from '@/lib/rate-limit';
import { joinWaitlist, newViewerToken, statusForViewer } from '@/lib/waitlist';

export const runtime = 'nodejs';

const VIEWER_COOKIE = 'waitlist_viewer';
const VIEWER_MAX_AGE_S = 60 * 60 * 24 * 365;

const joinSchema = z.strictObject({
  email: z.string().trim().toLowerCase().max(254).email(),
  ref: z.string().max(24).optional(),
});

// Public sign-up: origin → IP limit → capped, validated body (CP §6.1). The
// response is identical for a new address and a known one, and so is the cookie:
// a fresh opaque token either way, which only a real insert stores. A browser
// that already holds a working token keeps it, so its owner keeps their status.
// The IP limit also bounds how fast one person can inflate a referral count.
export async function POST(req: NextRequest): Promise<Response> {
  if (!isAllowedOrigin(req)) return jsonError('Forbidden', 403);
  if (!(await rateLimit('waitlist-ip', clientIp(req), 10, 3600))) return jsonError('Too many requests', 429);
  const body = await readJson(req, joinSchema, 1024);
  if (!body.ok) return body.response;

  const held = req.cookies.get(VIEWER_COOKIE)?.value;
  const keepHeld = held ? (await statusForViewer(held)) !== null : false;
  const token = newViewerToken();
  await joinWaitlist(body.data.email, token, body.data.ref);

  const res = NextResponse.json({ ok: true });
  if (!keepHeld) {
    res.cookies.set(VIEWER_COOKIE, token, {
      httpOnly: true,
      secure: process.env.NODE_ENV === 'production',
      sameSite: 'lax',
      path: '/',
      maxAge: VIEWER_MAX_AGE_S,
    });
  }
  return res;
}

// This browser's own entry, if it created one. There is no lookup by code or
// email, so a share link reveals nothing about its owner.
export async function GET(req: NextRequest): Promise<Response> {
  const token = req.cookies.get(VIEWER_COOKIE)?.value;
  const status = token ? await statusForViewer(token) : null;
  if (!status) return jsonError('Not found', 404);
  return NextResponse.json(status);
}
