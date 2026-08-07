import { NextResponse, type NextRequest } from 'next/server';
import { z } from 'zod';
import { consumeSignInCode, mintSession } from '@/lib/auth-server';
import { findOrCreateUser } from '@/lib/users';
import { sendWelcomeEmail } from '@/lib/email';

export const runtime = 'nodejs';

const bodySchema = z
  .object({ email: z.string().trim().toLowerCase().email(), code: z.string().regex(/^\d{6}$/) })
  .strict();

export async function POST(req: NextRequest): Promise<NextResponse> {
  const parsed = bodySchema.safeParse(await req.json());
  if (!parsed.success) return NextResponse.json({ error: 'Invalid body' }, { status: 400 });
  const { email, code } = parsed.data;
  if (!(await consumeSignInCode(email, code))) {
    return NextResponse.json({ error: 'Invalid or expired code' }, { status: 401 });
  }
  const user = await findOrCreateUser(email);
  await mintSession({ userId: user.id, email: user.email });
  if (user.created) await sendWelcomeEmail(user.email).catch(() => undefined);
  return NextResponse.json({ ok: true });
}
