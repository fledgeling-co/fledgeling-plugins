import { FOLD_GAP, foldGeometry, twoPaneFor } from '../fold';
import { layoutFor, sizeClassFor } from '../layout';
import { NO_FOLD, type FoldState } from '../../modules/duo-fold';

// iPhone Duo inner display: 951 × 669 pt landscape, the fold at 475.5 pt.
const flat: FoldState = {
  hasFold: true,
  divisions: [{ x: 475.5, y: 0, width: 0, height: 669, active: false }],
  hinge: 'fullyOpen',
  hingeAngle: Math.PI,
};
const book: FoldState = {
  hasFold: true,
  divisions: [{ x: 460, y: 0, width: 31, height: 669, active: true }],
  hinge: 'partiallyOpen',
  hingeAngle: 2.2,
};
const tabletop: FoldState = {
  hasFold: true,
  divisions: [{ x: 0, y: 462, width: 669, height: 27, active: true }],
  hinge: 'partiallyOpen',
  hingeAngle: 1.9,
};

describe('fold geometry', () => {
  it('reports no fold on every other device', () => {
    const g = foldGeometry(NO_FOLD);
    expect(g).toEqual({ hasFold: false, posture: 'none', verticalFoldX: null, horizontalFoldY: null, gap: 0 });
    expect(twoPaneFor(g, 1194, 834)).toBeNull();
  });

  it('places a flat fold at its inactive region and keeps the minimum gap', () => {
    const g = foldGeometry(flat);
    expect(g.posture).toBe('flat');
    expect(g.verticalFoldX).toBe(475.5);
    expect(g.gap).toBe(FOLD_GAP);
  });

  it('reads a top-to-bottom active fold as a book and widens the gap to the region', () => {
    const g = foldGeometry(book);
    expect(g.posture).toBe('book');
    expect(g.verticalFoldX).toBe(475.5);
    expect(g.gap).toBe(31);
  });

  it('reads an across fold as tabletop', () => {
    const g = foldGeometry(tabletop);
    expect(g.posture).toBe('tabletop');
    expect(g.horizontalFoldY).toBe(475.5);
    expect(g.verticalFoldX).toBeNull();
  });
});

describe('two panes', () => {
  it('splits the open inner display at the fold, flat or folded, with the same divider', () => {
    expect(twoPaneFor(foldGeometry(flat), 951, 669)).toEqual({ leftWidth: 462, rightX: 489 });
    expect(twoPaneFor(foldGeometry(book), 951, 669)).toEqual({ leftWidth: 460, rightX: 491 });
  });

  it('stays one pane in portrait, Split View and the outer display', () => {
    expect(twoPaneFor(foldGeometry(flat), 669, 951)).toBeNull();
    expect(twoPaneFor(foldGeometry(flat), 475, 669)).toBeNull();
    expect(twoPaneFor(foldGeometry(flat), 466, 678)).toBeNull();
  });
});

describe('fold-aware layout tiers', () => {
  it('treats the inner display in portrait as regular only on a device with a fold', () => {
    expect(sizeClassFor(669, true)).toBe('regular');
    expect(sizeClassFor(669)).toBe('compact');
    expect(layoutFor(669, true).isWide).toBe(true);
  });

  it('leaves the outer display and the closed phone compact', () => {
    expect(sizeClassFor(382, true)).toBe('compact');
    expect(sizeClassFor(475, true)).toBe('compact');
  });
});
