// An in-memory stand-in for the node-redis client, covering exactly the
// commands lib/ uses, so auth and rate-limit tests stay hermetic (BP §15).
// Each command reads and writes synchronously before resolving, so it is atomic
// the way a real Redis command is; eval() implements the one script in use,
// compare-and-delete.
type Entry = { value: string; expiresAt: number | null };

export class FakeRedis {
  private store = new Map<string, Entry>();

  private live(key: string): Entry | undefined {
    const entry = this.store.get(key);
    if (entry && entry.expiresAt !== null && entry.expiresAt <= Date.now()) {
      this.store.delete(key);
      return undefined;
    }
    return entry;
  }

  async get(key: string): Promise<string | null> {
    return this.live(key)?.value ?? null;
  }

  async set(key: string, value: string, opts?: { EX?: number }): Promise<'OK'> {
    this.store.set(key, { value, expiresAt: opts?.EX ? Date.now() + opts.EX * 1000 : null });
    return 'OK';
  }

  async del(...keys: string[]): Promise<number> {
    let removed = 0;
    for (const key of keys) if (this.store.delete(key)) removed += 1;
    return removed;
  }

  async incr(key: string): Promise<number> {
    const entry = this.live(key);
    const next = Number(entry?.value ?? '0') + 1;
    this.store.set(key, { value: String(next), expiresAt: entry?.expiresAt ?? null });
    return next;
  }

  async expire(key: string, seconds: number, mode?: 'NX'): Promise<number> {
    const entry = this.live(key);
    if (!entry || (mode === 'NX' && entry.expiresAt !== null)) return 0;
    entry.expiresAt = Date.now() + seconds * 1000;
    return 1;
  }

  async getDel(key: string): Promise<string | null> {
    const value = this.live(key)?.value ?? null;
    this.store.delete(key);
    return value;
  }

  async eval(_script: string, opts: { keys: string[]; arguments: string[] }): Promise<number> {
    const [key] = opts.keys;
    const [expected] = opts.arguments;
    if (key === undefined || this.live(key)?.value !== expected) return 0;
    this.store.delete(key);
    return 1;
  }

  multi(): FakeMulti {
    return new FakeMulti(this);
  }
}

class FakeMulti {
  private ops: Array<() => Promise<unknown>> = [];
  constructor(private readonly client: FakeRedis) {}
  incr(key: string): this { this.ops.push(() => this.client.incr(key)); return this; }
  expire(key: string, seconds: number, mode?: 'NX'): this { this.ops.push(() => this.client.expire(key, seconds, mode)); return this; }
  set(key: string, value: string, opts?: { EX?: number }): this { this.ops.push(() => this.client.set(key, value, opts)); return this; }
  del(key: string): this { this.ops.push(() => this.client.del(key)); return this; }
  async exec(): Promise<unknown[]> {
    const out: unknown[] = [];
    for (const op of this.ops) out.push(await op());
    return out;
  }
}
