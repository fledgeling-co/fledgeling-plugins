import { NextResponse, after, type NextRequest } from 'next/server';
import { z } from 'zod';
import { consumeSignInCode, mintSession } from '@/lib/auth-server';
import { sendWelcomeEmail } from '@/lib/email';
import { isAllowedOrigin, jsonError, readJson } from '@/lib/http';
import { logger } from '@/lib/logger';
import { clientIp, rateLimit } from '@/lib/rate-limit';
import { findOrCreateUser } from '@/lib/users';

export const runtime = 'nodejs';

const bodySchema = z.strictObject({
  email: z.string().trim().toLowerCase().max(254).email(),
  code: z.string().regex(/^\d{6}$/),
});

// The session is minted only after the code proves the caller controls the
// mailbox, for a new account and an existing one alike (CP §6.1).
export async function POST(req: NextRequest): Promise<Response> {
  if (!isAllowedOrigin(req)) return jsonError('Forbidden', 403);
  if (!(await rateLimit('verify-ip', clientIp(req), 60, 3600))) return jsonError('Too many requests', 429);
  const body = await readJson(req, bodySchema, 1024);
  if (!body.ok) return body.response;
  const { email, code } = body.data;
  if (!(await consumeSignInCode(email, code))) return jsonError('Invalid or expired code', 401);
  const user = await findOrCreateUser(email);
  await mintSession({ userId: user.id, email: user.email });
  if (user.created) {
    after(() => sendWelcomeEmail(user.email).catch((err: unknown) => logger.error({ err }, 'welcome email failed')));
  }
  return NextResponse.json({ ok: true });
}
