import { handOff, handoffFor, handoffFromState, takeHandoff, type HandoffRoutes } from '../foldHandoff';

const ROUTES: HandoffRoutes = {
  'item/[id]': { tab: 'items' },
  'settings/[part]': { tab: 'settings', param: 'part' },
  'pull/[id]': { tab: 'repositories', toId: v => `pull~${decodeURIComponent(v)}` },
};
const tabs = (name: string) => ({ name: '(tabs)', state: { index: 0, routes: [{ name }] } });

describe('the opening half of keeping what is on screen', () => {
  it("names each first-level detail's tab and pane id", () => {
    expect(handoffFor(ROUTES, 'item/[id]', { id: 'a' })).toEqual({ tab: 'items', id: 'a' });
    expect(handoffFor(ROUTES, 'settings/[part]', { part: 'connection' })).toEqual({ tab: 'settings', id: 'connection' });
    expect(handoffFor(ROUTES, 'pull/[id]', { id: encodeURIComponent('web~42') })).toEqual({ tab: 'repositories', id: 'pull~web~42' });
  });

  it('leaves routes it was not given, and a route with no id, pushed', () => {
    expect(handoffFor(ROUTES, 'log/[id]', { id: 'x' })).toBeNull();
    expect(handoffFor(ROUTES, 'item/[id]', {})).toBeNull();
  });

  it('hands off only one detail pushed over the tab it came from', () => {
    expect(handoffFromState(ROUTES, { routes: [tabs('settings'), { name: 'settings/[part]', params: { part: 'pairing' } }] })).toEqual({ tab: 'settings', id: 'pairing' });
    // Pushed from another tab: the list beside it would not be the one it came from.
    expect(handoffFromState(ROUTES, { routes: [tabs('activity'), { name: 'settings/[part]', params: { part: 'connection' } }] })).toBeNull();
    // Two screens deep: something is pushed on top of the detail.
    expect(handoffFromState(ROUTES, { routes: [tabs('items'), { name: 'item/[id]', params: { id: 'a' } }, { name: 'log/[id]', params: { id: '1' } }] })).toBeNull();
    expect(handoffFromState(ROUTES, { routes: [tabs('items')] })).toBeNull();
    expect(handoffFromState(ROUTES, undefined)).toBeNull();
  });

  it("finds the tabs under expo-router's root slot, and uses the initial tab before the tabs have state", () => {
    const pushed = { routes: [{ name: '(tabs)' }, { name: 'item/[id]', params: { id: 'b' } }] };
    expect(handoffFromState(ROUTES, { routes: [{ name: '__root', state: pushed }] }, { initialTab: 'items' })).toEqual({ tab: 'items', id: 'b' });
    expect(handoffFromState(ROUTES, { routes: [{ name: '__root', state: pushed }] })).toBeNull();
  });

  it('is taken once, by its own tab', () => {
    handOff({ tab: 'settings', id: 'about' });
    expect(takeHandoff('items')).toBeNull();
    expect(takeHandoff('settings')).toBe('about');
    expect(takeHandoff('settings')).toBeNull();
  });
});
