import { NextResponse, type NextRequest } from 'next/server';
import { z } from 'zod';
import { verifyAdminCode } from '@/lib/auth-admin';

export const runtime = 'nodejs';

const bodySchema = z
  .object({ email: z.string().trim().toLowerCase().email(), code: z.string().regex(/^\d{6}$/) })
  .strict();

export async function POST(req: NextRequest): Promise<NextResponse> {
  const parsed = bodySchema.safeParse(await req.json());
  if (!parsed.success) return NextResponse.json({ error: 'Invalid body' }, { status: 400 });
  const ok = await verifyAdminCode(parsed.data.email, parsed.data.code);
  if (!ok) return NextResponse.json({ error: 'Invalid or expired code' }, { status: 401 });
  return NextResponse.json({ ok: true });
}
