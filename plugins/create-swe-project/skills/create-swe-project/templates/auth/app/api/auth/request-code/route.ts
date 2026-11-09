import { NextResponse, after, type NextRequest } from 'next/server';
import { randomInt } from 'node:crypto';
import { z } from 'zod';
import { allowCodeRequest, storeSignInCode } from '@/lib/auth-server';
import { sendSignInCodeEmail } from '@/lib/email';
import { isAllowedOrigin, jsonError, readJson } from '@/lib/http';
import { logger } from '@/lib/logger';
import { clientIp, rateLimit } from '@/lib/rate-limit';

export const runtime = 'nodejs';

const bodySchema = z.strictObject({ email: z.string().trim().toLowerCase().max(254).email() });

// Public auth entry point (CP §6.1): origin → IP limit → capped, validated body
// → handler, all before any read or write. Every address gets the same work and
// the same response, and the email goes out after the response, so neither
// latency nor a provider failure reveals whether an account exists.
export async function POST(req: NextRequest): Promise<Response> {
  if (!isAllowedOrigin(req)) return jsonError('Forbidden', 403);
  if (!(await rateLimit('signin-ip', clientIp(req), 30, 3600))) return jsonError('Too many requests', 429);
  const body = await readJson(req, bodySchema, 1024);
  if (!body.ok) return body.response;
  const { email } = body.data;
  if (await allowCodeRequest(email)) {
    const code = String(randomInt(100000, 1000000));
    await storeSignInCode(email, code);
    after(() => sendSignInCodeEmail(email, code).catch((err: unknown) => logger.error({ err }, 'sign-in code email failed')));
  }
  return NextResponse.json({ ok: true });
}
