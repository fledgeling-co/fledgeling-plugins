import { NextResponse, after, type NextRequest } from 'next/server';
import { z } from 'zod';
import { requestAdminCode } from '@/lib/auth-admin';
import { isAllowedOrigin, jsonError, readJson } from '@/lib/http';
import { clientIp, rateLimit } from '@/lib/rate-limit';

export const runtime = 'nodejs';

const bodySchema = z.strictObject({ email: z.string().trim().toLowerCase().max(254).email() });

// Partitioned per IP, never one global bucket, so nobody can lock every admin
// out by failing from anywhere (CP §6.1).
export async function POST(req: NextRequest): Promise<Response> {
  if (!isAllowedOrigin(req)) return jsonError('Forbidden', 403);
  if (!(await rateLimit('admin-code-ip', clientIp(req), 10, 3600))) return jsonError('Too many requests', 429);
  const body = await readJson(req, bodySchema, 1024);
  if (!body.ok) return body.response;
  const send = await requestAdminCode(body.data.email);
  if (send) after(send);
  return NextResponse.json({ ok: true }); // identical for admins and everyone else
}
