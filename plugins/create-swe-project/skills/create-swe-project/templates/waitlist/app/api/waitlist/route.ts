import { NextResponse, type NextRequest } from 'next/server';
import { z } from 'zod';
import { joinWaitlist, waitlistStatus } from '@/lib/waitlist';

export const runtime = 'nodejs';

const joinSchema = z
  .object({ email: z.string().trim().toLowerCase().email(), ref: z.string().max(24).optional() })
  .strict();

export async function POST(req: NextRequest): Promise<NextResponse> {
  const parsed = joinSchema.safeParse(await req.json());
  if (!parsed.success) return NextResponse.json({ error: 'Invalid body' }, { status: 400 });
  const result = await joinWaitlist(parsed.data.email, parsed.data.ref);
  return NextResponse.json(result);
}

export async function GET(req: NextRequest): Promise<NextResponse> {
  const code = req.nextUrl.searchParams.get('code');
  if (!code) return NextResponse.json({ error: 'Missing code' }, { status: 400 });
  const result = await waitlistStatus(code);
  if (!result) return NextResponse.json({ error: 'Not found' }, { status: 404 });
  return NextResponse.json(result);
}
