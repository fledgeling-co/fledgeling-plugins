import React from 'react';

import { render } from '@testing-library/react-native';

import { takeHandoff } from '~/lib/foldHandoff';

import { FoldHandoff } from '../FoldHandoff';

const mockBack = jest.fn();
let mockState: unknown;
jest.mock('expo-router', () => ({
  useRouter: () => ({ back: mockBack, canGoBack: () => true }),
  useRootNavigationState: () => mockState,
}));
let mockPane: { leftWidth: number; rightX: number } | null = null;
jest.mock('~/lib/fold', () => ({ SPLIT_MIN_WIDTH: 900, useFold: () => ({ hasFold: true }), useTwoPane: () => mockPane }));

const ROUTES = { 'item/[id]': { tab: 'items' } };
const itemPushed = { routes: [{ name: '(tabs)', state: { index: 0, routes: [{ name: 'items' }] } }, { name: 'item/[id]', params: { id: 'a' } }] };

beforeEach(() => {
  mockBack.mockReset();
  mockPane = null;
  takeHandoff('items');
});

describe('FoldHandoff', () => {
  it('pops a pushed item into the Items pane beside its list when the Duo opens', () => {
    mockState = itemPushed;
    const view = render(<FoldHandoff routes={ROUTES} />);
    expect(mockBack).not.toHaveBeenCalled();
    mockPane = { leftWidth: 320, rightX: 320 };
    view.rerender(<FoldHandoff routes={ROUTES} />);
    expect(mockBack).toHaveBeenCalledTimes(1);
    expect(takeHandoff('items')).toBe('a');
  });

  it('does nothing when the app starts open, or while it stays open', () => {
    mockState = itemPushed;
    mockPane = { leftWidth: 320, rightX: 320 };
    const view = render(<FoldHandoff routes={ROUTES} />);
    view.rerender(<FoldHandoff routes={ROUTES} />);
    expect(mockBack).not.toHaveBeenCalled();
  });

  it('leaves a route it was not given pushed', () => {
    mockState = { routes: [itemPushed.routes[0], { name: 'log/[id]', params: { id: 'x' } }] };
    const view = render(<FoldHandoff routes={ROUTES} />);
    mockPane = { leftWidth: 320, rightX: 320 };
    view.rerender(<FoldHandoff routes={ROUTES} />);
    expect(mockBack).not.toHaveBeenCalled();
  });
});
