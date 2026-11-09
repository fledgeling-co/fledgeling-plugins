import { NextResponse, type NextRequest } from 'next/server';
import { z } from 'zod';
import { verifyAdminCode } from '@/lib/auth-admin';
import { isAllowedOrigin, jsonError, readJson } from '@/lib/http';
import { clientIp, rateLimit } from '@/lib/rate-limit';

export const runtime = 'nodejs';

const bodySchema = z.strictObject({
  email: z.string().trim().toLowerCase().max(254).email(),
  code: z.string().regex(/^\d{6}$/),
});

export async function POST(req: NextRequest): Promise<Response> {
  if (!isAllowedOrigin(req)) return jsonError('Forbidden', 403);
  if (!(await rateLimit('admin-verify-ip', clientIp(req), 30, 3600))) return jsonError('Too many requests', 429);
  const body = await readJson(req, bodySchema, 1024);
  if (!body.ok) return body.response;
  if (!(await verifyAdminCode(body.data.email, body.data.code))) return jsonError('Invalid or expired code', 401);
  return NextResponse.json({ ok: true });
}
