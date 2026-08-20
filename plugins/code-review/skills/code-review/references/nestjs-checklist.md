# NestJS Review Checklist

This checklist covers the load-bearing areas of NestJS that AI reviewers most reliably get wrong (or fail to catch) in real PRs: DI hygiene, module boundaries, decorator placement, scope, validation, exception handling, lifecycle, and testing seams.

Each item lists: the rule, what to grep for, the severity to assign, and the recommended fix-pattern. Skip items that don't apply to the diff, and record a skipped section as `not-applicable` with its structural reason rather than dropping it silently (`coverage.md`).

**Load this file only when the Phase 1 repo profile shows `@nestjs/*` in a touched package's dependencies.** Its rules pattern-match on shapes that recur outside NestJS — a DI container, a decorator-registered handler, a global validation pipe — so applied to a repo without it, they produce findings whose fixes cannot be applied. Those are refuted at Gate 1 as a class, which is wasted budget rather than a safety net. The same rule runs in the other direction: where the profile *does* show NestJS, this file loads whatever the path patterns look like, because a `.service.ts` naming convention is not what makes a file a NestJS provider.

§10 below covers TypeORM and Prisma hazards. Read it against the ORM the profile says is installed, and treat the other as `not-applicable`.

---

## Contents

- [1. Dependency Injection (DI) hygiene](#1-dependency-injection-di-hygiene)
- [2. Module boundaries](#2-module-boundaries)
- [3. `forwardRef` and circular dependencies](#3-forwardref-and-circular-dependencies)
- [4. Scope (REQUEST / TRANSIENT)](#4-scope-request-transient)
- [5. Validation pipes + DTOs](#5-validation-pipes-dtos)
- [6. Global vs scoped enhancers](#6-global-vs-scoped-enhancers)
- [7. Exception filters](#7-exception-filters)
- [8. Lifecycle and async cleanup](#8-lifecycle-and-async-cleanup)
- [9. Testing boundaries](#9-testing-boundaries)
- [10. ORM hazards (TypeORM / Prisma)](#10-orm-hazards-typeorm-prisma)
- [11. RxJS misuse (interceptors and gateways)](#11-rxjs-misuse-interceptors-and-gateways)
- [12. Security (defer to `security-checklist.md`)](#12-security-defer-to-security-checklistmd)
- [13. Decorator ordering and stacking](#13-decorator-ordering-and-stacking)
- [Sources](#sources)

## 1. Dependency Injection (DI) hygiene

### 1.1 Provider missing `@Injectable()` — `HIGH` (compile-time DI failure)

Every class that NestJS instantiates as a provider must be decorated with `@Injectable()`. Without it, the container cannot resolve the provider's own dependencies.

Bad:
```ts
export class UsersService {
  constructor(private readonly users: UsersRepository) {}
}
```

Good:
```ts
@Injectable()
export class UsersService {
  constructor(private readonly users: UsersRepository) {}
}
```

### 1.2 Manual instantiation of a DI-managed class — `MEDIUM`

If a service is calling `new SomeService(...)` for a class registered as a provider, the IoC container is being bypassed and singletons / scopes break. Exception: DTOs, entities, and value objects are fine to `new`.

### 1.3 `@Inject('TOKEN')` for a token that may not be registered — `HIGH`

If the diff adds `@Inject('CONFIG')` and the token isn't provided in the importing module's providers (or in a globally-visible module), the app will fail to bootstrap. Two distinct cases — handle them differently:

- **Truly optional dependency** (the service has a defined value or code path for the `undefined` case): mark `@Optional()` and handle the `undefined` injection.
- **Mandatory but conditionally registered** (the token must always exist; the registration is just split across modules): do **not** add `@Optional()` — that hides the real bootstrap bug. Fix by guaranteeing the token is registered (move it to a globally-visible / shared module, or import the providing module wherever it's needed).

### 1.4 Property-based `@Inject(...)` instead of constructor injection — `MEDIUM`

Per the NestJS docs: *"If your class doesn't extend another class, it's generally better to use constructor-based injection. The constructor clearly specifies which dependencies are required."* Property injection is reserved for sub-classes that would otherwise need to thread deps through `super()`.

### 1.5 Heavy use of `ModuleRef` / `app.get()` outside `bootstrap()` — `MEDIUM`

Manual resolution defeats DI. Acceptable in `main.ts` for one-time setup, in factories, or for resolving request-scoped providers in tests. Inside services it's a smell.

---

## 2. Module boundaries

### 2.1 Provider used outside its declaring module without being exported — `HIGH` (compile failure)

NestJS modules encapsulate their providers by default. If `ModuleA` declares `ServiceA` and `ModuleB` imports `ModuleA`, `ModuleB` can only inject `ServiceA` if `ModuleA` lists it in `exports`.

### 2.2 Same provider re-declared in multiple modules — `HIGH`

If `UsersService` is in the `providers` array of two modules, NestJS creates two separate singletons. State diverges between the two instances. Fix: declare in one module, export it, import that module wherever needed.

### 2.3 `@Global()` overuse — `MEDIUM`

Per the docs: *"Making everything global is not recommended as a design practice. The global modules approach is available to reduce the amount of necessary boilerplate. The imports array is generally the preferred way to make the module's API available to consumers."* If the diff adds `@Global()` to a feature module (not infra: not Config/Logger/Db), flag it.

### 2.4 Importing barrel files for module/provider classes — `HIGH` (causes cycles)

Per the NestJS circular-dependency docs: *"Barrel files should be omitted when it comes to module/provider classes."* Barrel imports of providers cause the resolution order to invert silently and produce undefined dependencies.

### 2.5 "God Module" anti-pattern — `MEDIUM`

`AppModule` registers dozens of providers / services / controllers that should live in feature modules. If the diff dumps a new feature into `AppModule` instead of creating its own module, flag it.

---

## 3. `forwardRef` and circular dependencies

### 3.1 New `forwardRef()` usage — `MEDIUM`

`forwardRef` exists, and NestJS supports it, but it is widely treated as a code smell indicating a module-boundary violation. Per the Tessl developer-kit guidance: *"Avoid `forwardRef()` by default, as it signals poor module design. When two modules depend on each other, extract shared logic into a third module instead."*

When you flag this, suggest one of:

- Extract the shared logic into a third common module that both depend on.
- Switch one direction of the dependency to event-driven (`EventEmitter2`).
- Resolve one side at *call time* via `ModuleRef.get(SomeService)` (or `.get(SomeService, { strict: false })` to look outside the current module) — this breaks the constructor-time cycle by deferring resolution until the method is invoked.

### 3.2 `forwardRef` combined with `Scope.REQUEST` — `HIGH`

Per the docs: *"Having circular dependencies depend on providers with `Scope.REQUEST` can lead to undefined dependencies."* If the diff has both, the order of instantiation is undefined and the request-scoped provider may be undefined when the other side reads it.

---

## 4. Scope (REQUEST / TRANSIENT)

### 4.1 New `Scope.REQUEST` provider deep in the dep graph — `HIGH`

Per the docs: *"The REQUEST scope bubbles up the injection chain. A controller that depends on a request-scoped provider will, itself, be request-scoped."* A single low-level service marked `Scope.REQUEST` makes everything that transitively depends on it request-scoped, dramatically slowing the app and breaking lifecycle hooks for the affected subtree.

If the diff adds `Scope.REQUEST` (or injects `REQUEST` / `INQUIRER`), trace the dep graph upward. If multiple controllers / services are affected, flag as HIGH and recommend either a **durable provider** (with `ContextIdStrategy`) or restructuring so the per-request data is passed as an argument rather than injected.

### 4.2 `Scope.REQUEST` on a Gateway or scheduled job — `CRITICAL`

WebSocket Gateways and `@Cron` / scheduled jobs cannot be instantiated multiple times. Per the docs: *"Each gateway encapsulates a real socket and cannot be instantiated multiple times."* Request-scoping them fails at runtime.

Passport strategies are a softer case — they *can* be request-scoped in custom-strategy patterns, but it's brittle and almost never necessary. Flag as `HIGH` rather than `CRITICAL` and recommend pulling the per-request data out via `@Req()` instead of injecting REQUEST.

### 4.3 Lifecycle hooks on a request-scoped provider — `HIGH`

`onModuleInit`, `onApplicationBootstrap`, `onModuleDestroy`, etc. **do not fire** for request-scoped classes. If the diff adds `implements OnModuleInit` to a `Scope.REQUEST` provider, the hook will silently never run.

---

## 5. Validation pipes + DTOs

### 5.1 Missing global `ValidationPipe` — `HIGH`

If `main.ts` does not register `app.useGlobalPipes(new ValidationPipe(...))` (or the equivalent `APP_PIPE` provider), DTO decorators are not enforced. Recommend the strict default:

```ts
app.useGlobalPipes(new ValidationPipe({
  whitelist: true,
  forbidNonWhitelisted: true,
  transform: true,
}))
```

### 5.2 `@Body()` typed as `any` or as an interface — `HIGH`

`ValidationPipe` only validates **class-based** DTOs. Interfaces are erased at runtime; `any` opts out entirely. `import type { Dto }` also erases.

### 5.3 Array body without `ParseArrayPipe` — `HIGH`

```ts
@Post('bulk') createBulk(@Body() dtos: CreateUserDto[]) { ... }
```
Plain `CreateUserDto[]` body is **not validated**. Use:

```ts
@Body(new ParseArrayPipe({ items: CreateUserDto })) dtos: CreateUserDto[]
```

Or wrap in a class:
```ts
class BulkCreate { @ValidateNested({ each: true }) @Type(() => CreateUserDto) items: CreateUserDto[] }
```

### 5.4 Mapped types from the wrong package — `MEDIUM`

`PartialType` / `PickType` / `OmitType` come in three flavors: `@nestjs/mapped-types`, `@nestjs/swagger`, `@nestjs/graphql`. Using the wrong one (e.g., `@nestjs/mapped-types` with a Swagger decorator-driven DTO) silently strips Swagger metadata.

### 5.5 Missing `@IsString()` etc. on DTO fields — `MEDIUM`

A class-based DTO with bare `field: string` declarations and no `class-validator` decorators is not actually validated. `ValidationPipe` will accept anything. Each field needs at least one decorator.

### 5.6 Generic / parameterized DTOs — `MEDIUM`

Per the docs: *"Since TypeScript does not store metadata about generics or interfaces, when you use them in your DTOs, ValidationPipe may not be able to properly validate incoming data."* Flag generic DTOs.

---

## 6. Global vs scoped enhancers

### 6.1 Global pipe / guard / filter / interceptor that needs DI but registered with `useGlobalX()` — `HIGH`

`app.useGlobalPipes(new ValidationPipe())` cannot inject providers, because it's instantiated outside any module context. Use the DI-capable token instead:

```ts
// providers in a module
{ provide: APP_PIPE, useClass: ValidationPipe }
{ provide: APP_FILTER, useClass: HttpExceptionFilter }
{ provide: APP_GUARD, useClass: AuthGuard }
{ provide: APP_INTERCEPTOR, useClass: LoggingInterceptor }
```

Caveats when using these tokens:

- The enhancer must be registered as `useClass` or `useFactory`. `useValue` (a pre-built instance) won't get its dependencies injected, defeating the whole point of switching to the `APP_*` token.
- Any module-scoped provider the enhancer depends on must be visible from the module that registers the `APP_*` provider — either declared in the same module, or exported from an imported module, or globally available (`@Global()` or `forRoot()` global modules).

### 6.2 Catch-anything filter declared after specific filters — `HIGH`

Per the docs: *"When combining an exception filter that catches everything with a filter that is bound to a specific type, the 'Catch anything' filter should be declared first."* If the diff registers them in the wrong order, the specific filter never fires.

### 6.3 `useGlobalFilters` / `useGlobalPipes` in a hybrid app — `HIGH`

Enhancers registered via `app.useGlobalX()` on the HTTP app instance do **not** automatically apply to connected microservice or gateway transports in a hybrid app. If the project mixes HTTP + microservice/gateway transports, register the enhancer through an `APP_FILTER` / `APP_PIPE` / `APP_GUARD` / `APP_INTERCEPTOR` provider instead — those propagate across all transports because they go through DI.

Don't flag a hybrid app that uses `APP_*` providers correctly; only flag the case where `useGlobalX()` is the *only* registration and the project has microservice/gateway transports attached.

---

## 7. Exception filters

### 7.1 Generic `HttpException` instead of a specific subclass — `LOW`

Prefer `BadRequestException`, `UnauthorizedException`, `NotFoundException`, `ForbiddenException`, `ConflictException`, `UnprocessableEntityException`, `InternalServerErrorException` over hand-rolled `new HttpException('msg', 500)`.

### 7.2 Custom exception not extending `HttpException` thrown from an HTTP path — `HIGH`

If a controller path throws a plain `Error` or a custom non-HttpException, the response defaults to 500 and the message is hidden. Custom exceptions should extend `HttpException`.

### 7.3 Lost cause / context — `MEDIUM`

```ts
catch (err) { throw new BadRequestException('msg') }   // err is lost
```
Better:
```ts
catch (err) { throw new BadRequestException('msg', { cause: err, description: 'detail' }) }
```

### 7.4 `IntrinsicException` not logged — `MEDIUM`

NestJS does not log `HttpException`, `WsException`, `RpcException` by default. If observability matters and the app has no `AllExceptionsFilter` to log them, flag it.

### 7.5 Filter instantiated with `new` at the controller level — `MEDIUM`

`@UseFilters(new MyFilter())` duplicates the instance per controller and prevents NestJS from reusing the singleton. Use `@UseFilters(MyFilter)` (class form).

### 7.6 Catch-all filter not platform-agnostic — `HIGH` if app is hybrid

A `@Catch()` decorator with no arguments creates a catch-all filter. If the app uses HTTP + microservice/gateway transports, the filter must switch on `host.getType()` (or use `host.switchToHttp()` / `switchToRpc()` / `switchToWs()`) before reading request/response objects. Otherwise the filter crashes the moment a non-HTTP transport raises an exception. Use `HttpAdapterHost` (`abstractHttpAdapter.reply(...)`) for the HTTP path so the filter doesn't hard-code Express/Fastify response APIs.

---

## 8. Lifecycle and async cleanup

### 8.1 Long-running background work without `enableShutdownHooks()` — `HIGH`

Per the docs: *"Shutdown hooks are disabled by default."* Without `app.enableShutdownHooks()` in `main.ts`, `onModuleDestroy` / `onApplicationShutdown` never fire on SIGTERM/SIGINT. `setInterval`s, queue consumers, and websocket sessions leak.

### 8.2 Service holds intervals/timers/subscriptions without disposal — `HIGH`

Service has `setInterval` / `setTimeout` / RxJS subscription / EventEmitter listener but no corresponding cleanup in `onModuleDestroy`.

```ts
implements OnModuleDestroy
async onModuleDestroy() {
  clearInterval(this.timer)
  this.subscription?.unsubscribe()
}
```

### 8.3 `onModuleInit` doing heavy work that should be in `onApplicationBootstrap` — `LOW`

`onModuleInit` runs per module before all modules are initialized. `onApplicationBootstrap` runs once after the entire app is initialized. DB warm-up / cache prefill belongs in the latter.

### 8.4 Lifecycle hook on a request-scoped class — see §4.3

---

## 9. Testing boundaries

### 9.1 `Test.createTestingModule(...).compile()` not awaited — `HIGH`

`compile()` is async. Forgotten `await` causes the test to use an uninitialized module.

### 9.2 `moduleRef.get(RequestScoped)` returns the wrong instance — `HIGH`

`get()` returns static instances; for request-scoped or transient providers, use `moduleRef.resolve(Token, contextId)` with a created `contextId`.

### 9.3 Globally registered guard / pipe / filter cannot be overridden in tests — `HIGH`

```ts
// in production module:
{ provide: APP_GUARD, useClass: JwtAuthGuard }   // cannot .overrideProvider() this
```

Fix pattern (production module change):
```ts
providers: [
  { provide: APP_GUARD, useExisting: JwtAuthGuard },
  JwtAuthGuard,
]
// then in tests:
.overrideProvider(JwtAuthGuard).useClass(MockAuthGuard)
```

### 9.4 No `await app.close()` in `afterAll` for E2E tests — `MEDIUM`

Leaks connections, causes flake on CI.

### 9.5 Manually mocking via `jest.mock(...)` instead of `.overrideProvider(...)` — `MEDIUM`

Bypasses the DI container, defeats the value of `@nestjs/testing`. Use the override APIs.

### 9.6 Missing repository mock token — `HIGH`

If the diff tests a service that injects a TypeORM repository, the test module must provide it via the canonical token:

```ts
{
  provide: getRepositoryToken(User),
  useValue: { create: jest.fn(), save: jest.fn(), find: jest.fn() }
}
```

A bare `useValue: {}` for `UsersRepository` will silently fail to inject.

### 9.7 Missing `.spec.ts` for a non-trivial new service — `MEDIUM`

Don't flag for a 5-line getter. Do flag for a new business-logic service with branching logic.

---

## 10. ORM hazards (TypeORM / Prisma)

### 10.1 N+1 query in a loop — `HIGH`

```ts
for (const user of users) {
  user.posts = await this.postsRepo.find({ where: { authorId: user.id } })  // N+1
}
```

Fix: use `relations: ['posts']` (TypeORM) or `include: { posts: true }` (Prisma) on the initial query.

### 10.2 Sensitive columns returned by default queries — `HIGH`

Sensitive columns (`passwordHash`, `apiKey`, `mfaSecret`, `refreshToken`, etc.) should be excluded from default queries so a careless `find()` followed by a whole-entity controller return doesn't leak them.

- **TypeORM:** mark the column with `{ select: false }` on `@Column(...)`.
- **Prisma:** use `omit:` at query time (`prisma.user.findUnique({ where: { id }, omit: { passwordHash: true } })`), define a reusable `select:` projection per query type, or use `Prisma.UserOmit<...>` types as the boundary type.

Don't apply the TypeORM-specific fix to a Prisma project (or vice versa) — the rule is "sensitive columns should not leave the data layer in default queries," and the *mechanism* is ORM-specific.

### 10.3 Multi-statement mutation outside a transaction — `HIGH`

If the diff has two or more `.save()` / `.update()` / `.delete()` calls that should be atomic, wrap in `dataSource.transaction(...)` (TypeORM) or `prisma.$transaction([...])` (Prisma).

### 10.4 Raw SQL with template-literal interpolation — `CRITICAL` (SQL injection)

Building a raw SQL string with `${userId}` interpolation is injection. Always use parameter binding (`queryRunner.query('SELECT * FROM users WHERE id = $1', [userId])` for TypeORM; `prisma.$queryRaw\`...\`` tagged template for Prisma).

This rule overlaps with `security-checklist.md` A03.1 — the security checklist is the canonical owner; this entry exists so a NestJS-only review still catches it. Don't double-flag.

### 10.5 Missing index on a foreign key the diff adds queries against — `MEDIUM`

If the diff adds `findBy({ userId })` queries on a column without `@Index`, performance degrades at scale.

---

## 11. RxJS misuse (interceptors and gateways)

### 11.1 Subscription not cleaned up — `HIGH`

Subscriptions inside services should be disposed in `onModuleDestroy`.

### 11.2 `tap` for side effects swallowed errors — `MEDIUM`

`tap(...)` runs side effects but does not swallow errors; however, sequencing side effects with `tap` and then `catchError` returning `EMPTY` swallows the error silently. Flag when you see this pattern combined.

### 11.3 Mixing Promises and Observables in interceptor return — `MEDIUM`

Returning `Observable<Promise<T>>` from `intercept()` doesn't await the inner promise. Use `from(promise)` or `mergeMap(() => from(promise))`.

---

## 12. Security (defer to `security-checklist.md`)

The security checklist owns: JWT secret hygiene, JWT `expiresIn`, JWT algorithm pinning, password hashing (argon2id / bcrypt cost), deny-by-default auth, cookie attributes, CSRF on Route Handlers, and the OWASP-aligned items. Do not duplicate findings here — when reviewing a NestJS project that touches auth/secrets, load `security-checklist.md` and let it own those rules. This section exists only as a routing pointer.

---

## 13. Decorator ordering and stacking

### 13.1 `@UseGuards(...)` and `@UseInterceptors(...)` stacking order — `MEDIUM`

When stacking on the same controller or method, NestJS executes guards before interceptors, and within each kind, executes them in the order listed. If two interceptors must run in a specific order (e.g., a transaction-wrapping interceptor that must wrap a logging interceptor), the listed order matters. Flag if the diff reorders existing decorators in a way that changes execution order without a corresponding test update.

### 13.2 Param decorator order vs. validation pipe binding — `MEDIUM`

Mixing `@Body()`, `@Query()`, `@Param()` in one method signature with a method-scoped pipe (`@UsePipes(...)`) applies the pipe to every parameter. Use parameter-scoped pipes (`@Body(new ValidationPipe(...))`) when only one parameter should be validated, and confirm the order doesn't accidentally expose an unvalidated parameter.

### 13.3 `@Public()` placed at the method level when the class has `@UseGuards()` — `HIGH`

If a controller class has `@UseGuards(JwtAuthGuard)` and a method has `@Public()`, the resolver order matters: `Reflector.getAllAndOverride(IS_PUBLIC_KEY, [handler, controller])` returns true and the route becomes public — sometimes intentional, sometimes a security regression. If the diff adds `@Public()` to a method on a guarded controller, confirm with the developer this was intended and that the method does not access `request.user` (which won't be set).

### 13.4 Missing `@Injectable()` on a class used by `@Inject()` — see §1.1

---

## Sources

- NestJS — [Providers](https://docs.nestjs.com/providers), [Modules](https://docs.nestjs.com/modules), [Pipes](https://docs.nestjs.com/pipes), [Exception filters](https://docs.nestjs.com/exception-filters)
- NestJS — [Validation](https://docs.nestjs.com/techniques/validation), [Authentication](https://docs.nestjs.com/security/authentication), [Testing](https://docs.nestjs.com/fundamentals/testing)
- NestJS — [Circular dependencies](https://docs.nestjs.com/fundamentals/circular-dependency), [Injection scopes](https://docs.nestjs.com/fundamentals/injection-scopes), [Lifecycle events](https://docs.nestjs.com/fundamentals/lifecycle-events)
- GitHub — [`awesome-copilot/instructions/nestjs.instructions.md`](https://github.com/github/awesome-copilot/blob/main/instructions/nestjs.instructions.md)
- PatrickJS — [typescript-nestjs-best-practices cursor rules](https://github.com/PatrickJS/awesome-cursorrules/blob/main/rules/typescript-nestjs-best-practices-cursorrules-promp/.cursorrules)
- Tessl developer-kit — [arch-module-boundaries](https://tessl.io/registry/giuseppe-trisciuoglio/developer-kit/files/plugins/developer-kit-typescript/skills/nestjs-best-practices/references/arch-module-boundaries.md)
