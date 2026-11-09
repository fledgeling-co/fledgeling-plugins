// The real `server-only` throws outside a React Server Components bundle, which
// would block every unit test of a server module (BP §15). Vitest aliases it here.
export {};
