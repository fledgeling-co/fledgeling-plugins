import { NextResponse, type NextRequest } from 'next/server';
import { z } from 'zod';
import { requestAdminCode } from '@/lib/auth-admin';

export const runtime = 'nodejs';

const bodySchema = z.object({ email: z.string().trim().toLowerCase().email() }).strict();

export async function POST(req: NextRequest): Promise<NextResponse> {
  const parsed = bodySchema.safeParse(await req.json());
  if (!parsed.success) return NextResponse.json({ error: 'Invalid body' }, { status: 400 });
  await requestAdminCode(parsed.data.email);
  return NextResponse.json({ ok: true }); // identical response for non-admins
}
