import { NextResponse, type NextRequest } from 'next/server';
import { z } from 'zod';
import { getSession } from '@/lib/auth-server';
import { db } from '@/lib/db';
import { UserModel } from '@/lib/models';

export const runtime = 'nodejs';

const bodySchema = z.object({ token: z.string().min(16).max(400) }).strict();

// The native client registers its APNs device token here; dead tokens are
// pruned by the sender when APNs reports them Unregistered.
export async function POST(req: NextRequest): Promise<NextResponse> {
  const session = await getSession();
  if (!session) return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
  const parsed = bodySchema.safeParse(await req.json());
  if (!parsed.success) return NextResponse.json({ error: 'Invalid body' }, { status: 400 });
  await db();
  await UserModel.updateOne({ _id: session.userId }, { $addToSet: { pushTokens: parsed.data.token } });
  return NextResponse.json({ ok: true });
}
