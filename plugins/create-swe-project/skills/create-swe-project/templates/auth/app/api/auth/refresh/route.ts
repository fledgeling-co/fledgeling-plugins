import { NextResponse, type NextRequest } from 'next/server';
import { rotateRefresh } from '@/lib/auth-server';
import { isAllowedOrigin, jsonError } from '@/lib/http';

export const runtime = 'nodejs';

// 401 here means the session is over: the client signs out once. A network
// error or 5xx is transient and must not sign anyone out (BP §9.7).
export async function POST(req: NextRequest): Promise<Response> {
  if (!isAllowedOrigin(req)) return jsonError('Forbidden', 403);
  const session = await rotateRefresh();
  if (!session) return jsonError('Unauthorized', 401);
  return NextResponse.json({ ok: true });
}
