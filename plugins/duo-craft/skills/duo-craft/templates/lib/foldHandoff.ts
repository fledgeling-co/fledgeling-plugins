/**
 * Keeping what is on screen when an iPhone Duo opens (pattern 2, the opening half).
 *
 * Closed, a row pushes its detail full screen. Opened, that detail belongs in the right pane beside
 * the list it came from: `FoldHandoff` pops the pushed screen and hands its id here, and the tab's
 * `DetailPaneLayout` (given `handoffTab`) takes it as the selection. Closing again pushes it back,
 * which `DetailPaneLayout` already does, so the detail survives the fold both ways.
 *
 * Only a first-level detail of the tab underneath moves. A detail pushed from another tab stays
 * pushed, because the list beside it would not be the list it came from, and so does a screen
 * pushed on top of a detail, because the pane would drop what led to it.
 *
 * Built in Egress's iPhone app and seen on the Duo simulator on 28 November 2026: Settings ›
 * Connection opened while closed came back as the right pane beside the Settings list on unfolding.
 */

export type Handoff = { tab: string; id: string };

/**
 * The app's pushed detail routes, by expo-router route name, with the tab each is a first-level
 * detail of. `param` names the route parameter holding the id (default `id`); `toId` maps it to the
 * id the tab's pane uses when the two differ.
 */
export type HandoffRoutes = Record<string, { tab: string; param?: string; toId?: (value: string) => string | null }>;

let pending: Handoff | null = null;
const listeners = new Set<() => void>();

export function handOff(h: Handoff) {
  pending = h;
  for (const l of listeners) l();
}

/** The id waiting for `tab`'s pane, taken once. */
export function takeHandoff(tab: string): string | null {
  if (pending?.tab !== tab) return null;
  const id = pending.id;
  pending = null;
  return id;
}

export function subscribeHandoff(l: () => void): () => void {
  listeners.add(l);
  return () => {
    listeners.delete(l);
  };
}

type Params = Record<string, string | string[] | undefined> | undefined;
const one = (p: Params, k: string) => {
  const v = p?.[k];
  return Array.isArray(v) ? v[0] : v;
};

/** The tab a pushed route is a first-level detail of, and the id its pane shows; null otherwise. */
export function handoffFor(routes: HandoffRoutes, route: string, params: Params): Handoff | null {
  const entry = routes[route];
  if (!entry) return null;
  const value = one(params, entry.param ?? 'id');
  if (!value) return null;
  const id = entry.toId ? entry.toId(value) : value;
  return id ? { tab: entry.tab, id } : null;
}

/** A navigator's state as `useRootNavigationState` gives it, reduced to what the handoff reads. */
export type RootState = {
  routes: { name: string; params?: Params; state?: RootState & { index?: number } }[];
  index?: number;
};

/**
 * The stack that holds the tabs. expo-router wraps the root layout's navigator in its own slot
 * (`__root`), so the tabs are one level down rather than at the top of the root state. Egress's
 * first build looked only at the top, passed every hand-written test, and on the device opened
 * with the detail still pushed.
 */
function stackWithTabs(state: RootState | undefined, tabsRoute: string): RootState | undefined {
  let s = state;
  for (let depth = 0; s && depth < 4; depth++) {
    if (s.routes.some(r => r.name === tabsRoute)) return s;
    s = s.routes.length === 1 ? s.routes[0].state : undefined;
  }
  return undefined;
}

/**
 * What to hand off from the root state as it stands: one detail pushed directly over the tabs,
 * belonging to the tab under it. `initialTab` names the tab shown before the tab navigator has any
 * state of its own (the first tab, until someone switches).
 */
export function handoffFromState(
  routes: HandoffRoutes,
  state: RootState | undefined,
  { tabsRoute = '(tabs)', initialTab }: { tabsRoute?: string; initialTab?: string } = {},
): Handoff | null {
  const stack = stackWithTabs(state, tabsRoute);
  if (!stack) return null;
  const at = stack.routes.findIndex(r => r.name === tabsRoute);
  if (at !== stack.routes.length - 2) return null;
  const tabs = stack.routes[at].state;
  const under = tabs ? tabs.routes[tabs.index ?? 0]?.name : initialTab;
  if (!under) return null;
  const top = stack.routes[at + 1];
  const h = handoffFor(routes, top.name, top.params);
  return h && h.tab === under ? h : null;
}
