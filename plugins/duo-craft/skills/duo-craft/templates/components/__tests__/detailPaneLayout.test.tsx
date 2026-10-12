import React from 'react';

import { Pressable, Text } from 'react-native';

import { act, fireEvent, render, screen } from '@testing-library/react-native';

import { DetailPaneLayout, useDetailPane } from '../DetailPaneLayout';

// The library's own mock, so the test does not depend on the app's jest setup.
jest.mock('react-native-safe-area-context', () => require('react-native-safe-area-context/jest/mock').default);

const mockPush = jest.fn();
jest.mock('expo-router', () => ({ useRouter: () => ({ push: mockPush }) }));

let mockPane: { leftWidth: number; rightX: number } | null = null;
let mockHasFold = true;
jest.mock('~/lib/fold', () => ({
  useTwoPane: () => mockPane,
  useFold: () => ({ hasFold: mockHasFold }),
  // The 900pt rule itself is covered in fold.test.ts; this stands in for it.
  twoPaneForWidth: (w: number) => (w >= 900 ? { leftWidth: 324, rightX: 324 } : null),
}));

function List() {
  const pane = useDetailPane();
  return (
    <Pressable accessibilityRole="button" onPress={() => pane?.open('co-2')}>
      <Text>Open second</Text>
    </Pressable>
  );
}

const tree = () => (
  <DetailPaneLayout
    hrefFor={id => `/company/${id}`}
    defaultId="co-1"
    renderDetail={id => <Text>{`Detail ${id}`}</Text>}
  >
    <List />
  </DetailPaneLayout>
);

beforeEach(() => {
  mockPush.mockReset();
  mockPane = null;
  mockHasFold = true;
});

const layoutAt = (width: number) =>
  fireEvent(screen.root, 'layout', { nativeEvent: { layout: { x: 0, y: 0, width, height: 800 } } });

describe('DetailPaneLayout', () => {
  it('pushes the detail screen with one pane, as before', () => {
    render(tree());
    expect(screen.queryByText(/Detail/)).toBeNull();
    fireEvent.press(screen.getByRole('button', { name: 'Open second' }));
    expect(mockPush).toHaveBeenCalledWith('/company/co-2');
  });

  it('shows the default beside the list when split, and swaps it on open', () => {
    mockPane = { leftWidth: 462, rightX: 489 };
    render(tree());
    expect(screen.getByText('Detail co-1')).toBeTruthy();
    fireEvent.press(screen.getByRole('button', { name: 'Open second' }));
    expect(screen.getByText('Detail co-2')).toBeTruthy();
    expect(mockPush).not.toHaveBeenCalled();
  });

  it('keeps a chosen detail open as a full screen when the split closes', () => {
    mockPane = { leftWidth: 462, rightX: 489 };
    const view = render(tree());
    fireEvent.press(screen.getByRole('button', { name: 'Open second' }));
    mockPane = null;
    act(() => view.rerender(tree()));
    expect(mockPush).toHaveBeenCalledWith('/company/co-2');
  });

  it('does not push the default when the split closes', () => {
    mockPane = { leftWidth: 462, rightX: 489 };
    const view = render(tree());
    mockPane = null;
    act(() => view.rerender(tree()));
    expect(mockPush).not.toHaveBeenCalled();
  });

  it('splits a wide pane without a fold, from the width of the pane itself', () => {
    mockHasFold = false;
    render(tree());
    expect(screen.queryByText(/Detail/)).toBeNull();
    act(() => layoutAt(1180));
    expect(screen.getByText('Detail co-1')).toBeTruthy();
    act(() => layoutAt(820));
    expect(screen.queryByText(/Detail/)).toBeNull();
  });
});
