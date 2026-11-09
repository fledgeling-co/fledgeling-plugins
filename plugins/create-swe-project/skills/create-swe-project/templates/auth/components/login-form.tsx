'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

type Stage = 'email' | 'code';

async function post(path: string, body?: unknown): Promise<boolean> {
  const res = await fetch(path, {
    method: 'POST',
    headers: body ? { 'content-type': 'application/json' } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  });
  return res.ok;
}

export function LoginForm({ devLogin }: { devLogin: boolean }): React.ReactElement {
  const router = useRouter();
  const [email, setEmail] = useState('');
  const [code, setCode] = useState('');
  const [stage, setStage] = useState<Stage>('email');
  const [pending, setPending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function attempt(action: () => Promise<boolean>, onSuccess: () => void, failure: string): Promise<void> {
    setPending(true);
    setError(null);
    try {
      if (await action()) onSuccess();
      else setError(failure);
    } catch {
      setError('Network error. Check your connection and try again.');
    } finally {
      setPending(false);
    }
  }

  return (
    <>
      {stage === 'email' ? (
        <form
          onSubmit={(e) => {
            e.preventDefault();
            void attempt(() => post('/api/auth/request-code', { email }), () => setStage('code'), 'Could not send a code. Try again.');
          }}
        >
          <label htmlFor="email">Email</label>
          <input id="email" type="email" autoComplete="email" required value={email} onChange={(e) => setEmail(e.target.value)} />
          <button type="submit" disabled={pending}>Email me a code</button>
        </form>
      ) : (
        <form
          onSubmit={(e) => {
            e.preventDefault();
            void attempt(() => post('/api/auth/verify', { email, code }), () => router.push('/'), 'That code is wrong or has expired.');
          }}
        >
          <label htmlFor="code">6-digit code sent to {email}</label>
          <input id="code" inputMode="numeric" autoComplete="one-time-code" pattern="\d{6}" required value={code} onChange={(e) => setCode(e.target.value)} />
          <button type="submit" disabled={pending}>Sign in</button>
        </form>
      )}
      {devLogin && (
        <button
          type="button"
          style={{ marginTop: 16 }}
          disabled={pending}
          onClick={() => void attempt(() => post('/api/auth/dev-login'), () => router.push('/'), 'Dev login failed.')}
        >
          Dev login
        </button>
      )}
      <p role="alert" aria-live="polite">{error}</p>
    </>
  );
}
