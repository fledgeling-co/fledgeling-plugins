# TypeScript Cross-Cutting Checklist

Always loaded for any `.ts` / `.tsx` diff. These rules cover defensive typing patterns the compiler
alone cannot enforce.

Each item gives the rule, the severity, and the fix pattern. The typecheck gate the repo actually
runs — whatever its `typecheck` script invokes, which the Phase 1 profile records — already catches
a large class of these, so a finding it would have caught is noise. Flag what the compiler cannot
see.

Two applications of these rules are worth stating up front because they decide whole categories
below. **Trust-boundary input is parsed, never cast**, and parsed strictly: an unexpected key
rejected beats an unexpected key silently dropped and then re-added by a later refactor. And **a
cross-package wire type wants an exhaustive key enumeration**, not a structural check — a
`Record<keyof ApiX, true>` literal per type forces the compiler to fail when a field is added or
removed on one side only. Where the repo has such a guard, a diff editing a wire type without its
enumeration entry is a §2 exhaustiveness failure wearing different clothes; where it has none, the
boundary is a `no-oracle` row.

---

## 1. Type strictness

### 1.1 New `any` (explicit or implicit) — `MEDIUM`

`any` disables all type checking on the value. Replace with `unknown` and narrow with a type guard or Zod, or with the actual concrete type.

Bad:
```ts
function parse(input: any) { return input.foo.bar }
```

Good:
```ts
function parse(input: unknown): string {
  if (typeof input === 'object' && input !== null && 'foo' in input) {
    const foo = (input as { foo: unknown }).foo
    if (typeof foo === 'object' && foo !== null && 'bar' in foo) {
      return String((foo as { bar: unknown }).bar)
    }
  }
  throw new Error('invalid input')
}
```

Or, when validating external input, use Zod:

```ts
const Schema = z.object({ foo: z.object({ bar: z.string() }) })
function parse(input: unknown): string {
  return Schema.parse(input).foo.bar
}
```

### 1.2 `as` cast that bypasses narrowing — `MEDIUM`

`x as User` claims `x` is a `User` without proof. The compiler trusts you. Acceptable in two cases:
- Disambiguating union members the compiler can't narrow on its own (and you've checked the discriminant).
- Casting library output where the library's types are wrong but you've verified the runtime shape.

Always a smell when applied to user input or `JSON.parse(...)`.

### 1.3 `as unknown as T` (double cast) — `HIGH`

This pattern actively defeats two layers of safety. It almost always indicates either: (a) a type error that should be fixed at the source, or (b) two libraries with incompatible types where a real adapter is needed.

### 1.4 Non-null assertion `!` on a value that might genuinely be null — `MEDIUM`

`array.find(p => p.id === id)!.name` crashes when nothing matches. Acceptable when proven by surrounding code (e.g., immediately after a `length > 0` check on a non-empty literal). Otherwise, narrow explicitly.

### 1.5 `@ts-ignore` / `@ts-expect-error` without a comment — `MEDIUM`

If you're suppressing a type error, document why. A bare `@ts-ignore` is almost always a bug-in-waiting. Prefer `// @ts-expect-error <reason>` (the reason text follows on the same comment line, no colon — TypeScript treats it as free-form prose) so the suppression is removed automatically when the underlying type error goes away.

---

## 2. Discriminated union exhaustiveness

### 2.1 `switch` over a union without exhaustiveness check — `HIGH` if the diff just extended the union

When a discriminated union is `switch`ed on, the `default` branch must assign the unhandled state to `never`, so the compiler errors when a new variant is added.

Bad:
```ts
type State = { kind: 'loading' } | { kind: 'ready'; data: string } | { kind: 'error'; err: Error }

function render(s: State) {
  switch (s.kind) {
    case 'loading': return '...'
    case 'ready': return s.data
    // missing 'error' — silent runtime omission
  }
}
```

Good:
```ts
function render(s: State) {
  switch (s.kind) {
    case 'loading': return '...'
    case 'ready': return s.data
    case 'error': return s.err.message
    default:
      const _exhaustive: never = s
      return _exhaustive
  }
}
```

If the diff adds a new variant to a discriminated union, **grep every usage** of the discriminant. Each `switch`/`if-chain` over it must be updated. This is the highest-value exhaustiveness flag — flag a `HIGH` finding for each unupdated site.

### 2.2 `if/else if` chain over discriminant without exhaustiveness — `MEDIUM`

Same problem as `switch`, but TypeScript can't enforce exhaustiveness here unless you `assertNever(s)` in a final `else`. Recommend converting to `switch`.

---

## 3. Module boundary types

### 3.1 Public function / method without explicit return type — `MEDIUM`

Exported functions and class methods on exported classes should declare return types. Inferred return types at module boundaries change silently when the body changes, which then propagates type changes to callers without any visible signal in the diff. This is especially dangerous for API route handlers and Server Actions.

```ts
// Bad — return type changes when implementation changes
export async function getUser(id: string) { ... }

// Good
export async function getUser(id: string): Promise<User | null> { ... }
```

### 3.2 Re-exported type from a module that imports it — `LOW`

Pure re-exports cause module resolution issues in monorepos with multiple module systems. Prefer `export type { Foo } from './foo'` over `import { Foo } from './foo'; export { Foo }`.

### 3.3 Returning an entity / DB row directly from a public boundary — `HIGH` (data leak risk)

Tied closely to the security-checklist. If the diff returns the result of a `findFirst()` / `findUnique()` from an API handler or Server Action, sensitive fields (`passwordHash`, `apiKey`, internal flags) are sent to the client. Pick the fields explicitly.

---

## 4. Promise / async hygiene

### 4.1 Floating promise — `HIGH`

```ts
async function ship() { ... }
ship()   // unhandled rejection becomes an unhandledRejection event
```

Either `await` it, `.catch(handler)` it, attach `.then(noop, errHandler)`, or explicitly mark `void ship()` to signal intentional fire-and-forget. All four are accepted by `@typescript-eslint/no-floating-promises`. Don't false-flag legitimate fire-and-forget patterns in event-emitter / queue-consumer code.

### 4.2 `forEach` with an async callback — `HIGH`

```ts
items.forEach(async item => { await save(item) })
```

`forEach` ignores the returned promises. Use `for...of` with `await` for sequential, or `await Promise.all(items.map(save))` for concurrent.

### 4.3 Mixing `then` and `await` in the same function — `LOW`

Style inconsistency. Pick one.

### 4.4 Missing `await` before `expect` in tests — `HIGH`

```ts
expect(api.getUser(id)).toEqual({ name: 'x' })   // expects a Promise to equal an object
```

Should be `await expect(api.getUser(id)).resolves.toEqual({ name: 'x' })`.

### 4.5 Promise constructor anti-pattern — `MEDIUM`

```ts
return new Promise((resolve, reject) => {
  someAsyncFn().then(resolve, reject)
})
```

Already a promise — just `return someAsyncFn()`.

---

## 5. Error handling

### 5.1 `catch (e)` that loses the error — `HIGH`

```ts
try { ... } catch { return null }
```

Swallowing the error completely is acceptable only when the caller has no actionable response. Otherwise, log it or rethrow.

### 5.2 `catch (e: any)` — see §1.1; specifically use `unknown`

```ts
try { ... } catch (e: unknown) {
  if (e instanceof ZodError) { ... }
  if (e instanceof Error) { logger.error(e.message) }
  throw e
}
```

### 5.3 Rethrowing `new Error(originalError.message)` — `MEDIUM`

Loses the stack trace. Use `throw new Error('context', { cause: originalError })` (Node 16.9+).

---

## 6. Generics and overloads

### 6.1 Wide `extends` constraint — `LOW`

```ts
function id<T>(x: T): T   // fine
function id<T extends object>(x: T): T   // wider than needed
function id<T extends Record<string, unknown>>(x: T): T   // tighter, prefer
```

### 6.2 Function overloads where a union return type would suffice — `LOW`

Overloads are easy to get wrong. Keep them where each overload maps one input type to one narrowed return type. Where two or more overloads share a return type, or a call site has to cast the result, a single signature with a union return is the smaller surface.

---

## 7. Compile-time guarantees

### 7.1 Disabled compiler flag in the diff — `HIGH`

If the diff modifies `tsconfig.json` to disable `strict` / `strictNullChecks` / `noImplicitAny` / `strictFunctionTypes` / `noUncheckedIndexedAccess`, flag it. Recommend opting *in* to more strictness, not out.

### 7.2 `// eslint-disable-next-line` without a reason — `LOW`

If the rule is genuinely wrong here, document why.

---

## 8. Common runtime traps the type system misses

### 8.1 `Array.prototype.includes` on a literal union — `LOW`

```ts
type Color = 'red' | 'green' | 'blue'
const allowed: Color[] = ['red', 'green']
allowed.includes(input)   // TS error if input: string and the array is non-readonly
```

Fix: `(allowed as readonly string[]).includes(input)` and then narrow, or use a type predicate function.

Note: TypeScript 5.x widened the `readonly Array<T>.includes(...)` signature to accept `unknown`, so the false-positive frequency for this rule has dropped substantially. Only flag when the array is explicitly typed as a non-readonly literal-union array AND the call site genuinely fails type-check.

### 8.2 `Object.keys` returning `string[]` not `(keyof T)[]` — `LOW`

By design — runtime objects can have extra keys. Don't add `as Array<keyof T>` casts unless you've proven it's safe.

### 8.3 Optional chaining masking a logic bug — `MEDIUM`

```ts
const name = user?.profile?.name ?? 'anonymous'
```

If `user` should always exist at this code path, `?.` hides the contract violation. Assert / throw instead.

### 8.4 `JSON.parse` typed as the result type — `HIGH`

```ts
const config: Config = JSON.parse(rawString)   // pure assertion, runtime can be anything
```

Always validate parsed JSON with a schema before assigning a non-`unknown` type.

---

## 9. React + TypeScript specifics

### 9.1 `React.FC` with generic props — `LOW`

`React.FC<Props>` makes `children` implicit (deprecated in modern types), and complicates generics. Prefer plain function declarations:

```ts
function MyComponent<T>({ items }: { items: T[] }): JSX.Element { ... }
```

### 9.2 Event handler typed too widely — `LOW`

`onClick: (e: any) => void` should be `onClick: React.MouseEventHandler<HTMLButtonElement>`.

### 9.3 `useState` typed without accounting for the unset state — `HIGH`

```ts
const [user, setUser] = useState<User>()
```

Modern `@types/react` correctly infers this as `User | undefined`, so the *type* isn't lying. The bug is downstream: code that reads `user.foo` without first narrowing crashes on the first render where `user` is still `undefined`. Either use `useState<User | null>(null)` (forces explicit null-checking at use sites) or commit to `useState<User | undefined>(undefined)` and narrow with `if (!user) return null` before any property access.

---

## Sources

- TypeScript handbook — [Narrowing](https://www.typescriptlang.org/docs/handbook/2/narrowing.html), [Discriminated unions](https://www.typescriptlang.org/docs/handbook/2/narrowing.html#discriminated-unions)
- TypeScript ESLint rules — `no-floating-promises`, `no-misused-promises`, `switch-exhaustiveness-check`, `no-explicit-any`, `no-unsafe-assignment`, `prefer-nullish-coalescing`
