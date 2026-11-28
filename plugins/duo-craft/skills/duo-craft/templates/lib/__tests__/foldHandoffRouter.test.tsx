import React from 'react';

import { Text } from 'react-native';

import { act } from '@testing-library/react-native';
import { Stack, Tabs, router, useRootNavigationState } from 'expo-router';
import { renderRouter } from 'expo-router/testing-library';

import { handoffFromState, type RootState } from '../foldHandoff';

/**
 * The handoff read against expo-router's own navigation state rather than one written by hand: in
 * Egress, a check that passed every hand-written test never matched on a device, because the real
 * root state wraps the app's stack in expo-router's `__root` slot.
 */
let seen: RootState | undefined;
const settle = () =>
  act(async () => {
    await Promise.resolve();
    if (jest.isMockFunction(setTimeout)) jest.runOnlyPendingTimers();
  });
function Root() {
  seen = useRootNavigationState() as unknown as RootState;
  return <Stack />;
}

const ROUTES = { 'settings/[part]': { tab: 'settings', param: 'part' } };
// Tabs at the root, a stack inside each tab, details pushed on the root stack, as in the starter.
const routes = {
  _layout: Root,
  '(tabs)/_layout': () => <Tabs />,
  '(tabs)/home/_layout': () => <Stack />,
  '(tabs)/home/index': () => <Text>Home</Text>,
  '(tabs)/settings/_layout': () => <Stack />,
  '(tabs)/settings/index': () => <Text>Settings list</Text>,
  'settings/[part]': () => <Text>A setting</Text>,
  'log/[id]': () => <Text>A log</Text>,
};

describe('the handoff against the router', () => {
  it('finds a Settings page pushed from Settings under the root slot', async () => {
    renderRouter(routes, { initialUrl: '/settings' });
    await settle();
    await act(async () => router.push('/settings/connection'));
    await settle();
    expect(seen?.routes[0]?.name).toBe('__root');
    expect(handoffFromState(ROUTES, seen)).toEqual({ tab: 'settings', id: 'connection' });
  });

  it('leaves a Settings page pushed from another tab where it is', async () => {
    renderRouter(routes, { initialUrl: '/home' });
    await settle();
    await act(async () => router.push('/settings/connection'));
    await settle();
    expect(JSON.stringify(seen)).toContain('settings/[part]');
    expect(handoffFromState(ROUTES, seen)).toBeNull();
  });

  it('leaves a screen pushed on top of a detail where it is', async () => {
    renderRouter(routes, { initialUrl: '/settings' });
    await settle();
    await act(async () => router.push('/settings/about'));
    await settle();
    expect(handoffFromState(ROUTES, seen)).toEqual({ tab: 'settings', id: 'about' });
    await act(async () => router.push('/log/x'));
    await settle();
    expect(handoffFromState(ROUTES, seen)).toBeNull();
  });
});
