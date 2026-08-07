import { NextResponse, type NextRequest } from 'next/server';
import { z } from 'zod';
import { randomInt } from 'node:crypto';
import { rateLimitCodeRequest, storeSignInCode } from '@/lib/auth-server';
import { sendSignInCodeEmail } from '@/lib/email';

export const runtime = 'nodejs';

const bodySchema = z.object({ email: z.string().trim().toLowerCase().email() }).strict();

// BP §9: rate-limit 3/email/hour; return success even when the account doesn't
// exist (no existence leak, OWASP A07).
export async function POST(req: NextRequest): Promise<NextResponse> {
  const parsed = bodySchema.safeParse(await req.json());
  if (!parsed.success) return NextResponse.json({ error: 'Invalid body' }, { status: 400 });
  const { email } = parsed.data;
  if (await rateLimitCodeRequest(email)) {
    const code = String(randomInt(100000, 1000000));
    await storeSignInCode(email, code);
    await sendSignInCodeEmail(email, code);
  }
  return NextResponse.json({ ok: true });
}
