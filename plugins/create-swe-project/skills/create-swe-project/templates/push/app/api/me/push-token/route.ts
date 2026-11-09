import { NextResponse, type NextRequest } from 'next/server';
import { z } from 'zod';
import { getSession } from '@/lib/auth-server';
import { db } from '@/lib/db';
import { jsonError, readJson } from '@/lib/http';
import { UserModel } from '@/lib/models';
import { rateLimit } from '@/lib/rate-limit';

export const runtime = 'nodejs';

const bodySchema = z.strictObject({ token: z.string().min(16).max(400) });

// The native client registers its APNs device token here; the sender prunes a
// token when APNs reports it Unregistered. Auth first, then the body (CP §6.1),
// with the limit keyed by user (CP §6.11).
export async function POST(req: NextRequest): Promise<Response> {
  const session = await getSession();
  if (!session) return jsonError('Unauthorized', 401);
  if (!(await rateLimit('push-token', session.userId, 20, 3600))) return jsonError('Too many requests', 429);
  const body = await readJson(req, bodySchema, 1024);
  if (!body.ok) return body.response;
  await db();
  await UserModel.updateOne({ _id: session.userId }, { $addToSet: { pushTokens: body.data.token } });
  return NextResponse.json({ ok: true });
}
