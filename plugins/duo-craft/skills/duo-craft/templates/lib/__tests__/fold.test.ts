import { FLAT_LIST_WIDTH, FOLD_GAP, LIST_MAX_WIDTH, LIST_MIN_WIDTH, foldColumnLeftWidth, foldGeometry, twoPaneFor, twoPaneForWidth } from '../fold';
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
  it('keeps a fixed 320pt list on the open inner display lying flat', () => {
    expect(FLAT_LIST_WIDTH).toBe(320);
    expect(twoPaneFor(foldGeometry(flat), 951, 669)).toEqual({ leftWidth: 320, rightX: 320 });
  });

  it('divides at the fold, with its gap, once the device folds like a book', () => {
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

describe('twoPaneForWidth (no fold)', () => {
  it('splits iPad landscape beside its sidebar at about 35/65', () => {
    // 1180pt window less the 260pt sidebar.
    expect(twoPaneForWidth(920)).toEqual({ leftWidth: 331, rightX: 331 });
  });

  it('keeps one pane on iPad portrait and in a Split View half', () => {
    expect(twoPaneForWidth(820)).toBeNull();
    expect(twoPaneForWidth(507)).toBeNull();
  });

  it('holds the list between its bounds on very wide windows', () => {
    expect(twoPaneForWidth(1600)?.leftWidth).toBe(LIST_MAX_WIDTH);
    expect(twoPaneForWidth(900)!.leftWidth).toBeGreaterThanOrEqual(LIST_MIN_WIDTH);
  });
});

describe('foldColumnLeftWidth', () => {
  it('meets at the fold for a row across the open display', () => {
    // A row padded 20pt from the left edge and ending at the side bar (867pt).
    expect(foldColumnLeftWidth(foldGeometry(flat), 20, 827)).toBe(442);
    expect(foldColumnLeftWidth(foldGeometry(book), 20, 827)).toBe(440);
  });

  it('shares the row by flex inside a detail pane beside the 320pt list', () => {
    // The detail pane runs 320-867pt; padded, its row starts at 340pt, 135pt short of the fold.
    expect(foldColumnLeftWidth(foldGeometry(flat), 340, 507)).toBeNull();
  });

  it('shares the row by flex without a fold or across a tabletop fold', () => {
    expect(foldColumnLeftWidth(foldGeometry(NO_FOLD), 20, 827)).toBeNull();
    expect(foldColumnLeftWidth(foldGeometry(tabletop), 20, 627)).toBeNull();
  });
});
