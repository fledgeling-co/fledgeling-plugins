import SwiftUI
import UIKit

// iPhone Duo fold reading for a SwiftUI app: the same reservedRegions and UIHingeInteraction reads as
// the React Native module in modules/duo-fold, exposed as an environment value. Needs the iOS 27.1
// SDK; build with Xcode 27.1, because the 27.0 SDK has neither API and both ship Swift 6.4, so no
// compiler check can gate them.
//
// At the root of the scene:
//
//     @State private var fold = FoldState()
//     var body: some Scene {
//         WindowGroup {
//             RootView()
//                 .background(FoldReader(state: $fold))
//                 .environment(\.fold, fold)
//         }
//     }

/// Where a folding iPhone's fold is and how far its hinge is open. "No fold" everywhere else.
struct FoldState: Equatable {
    enum Hinge: Equatable { case none, closed, partiallyOpen, fullyOpen, unknown }
    /// Division regions in window coordinates. Read with `.includeInactive`, so the fold is reported
    /// while the device lies flat, as a region with no thickness.
    var divisions: [CGRect] = []
    var hinge: Hinge = .none

    var hasFold: Bool { !divisions.isEmpty || hinge != .none }
    var fold: CGRect? { divisions.first }
    /// A fold running top to bottom: the open display in landscape.
    var vertical: Bool {
        guard let f = fold else { return false }
        return f.height > f.width || (f.width == 0 && f.height > 0)
    }
    /// Half folded, so the two halves read as separate surfaces.
    var folded: Bool { hinge == .partiallyOpen }
    /// Book: a vertical fold, half folded. List and detail divide at the fold.
    var book: Bool { hasFold && vertical && folded }
    /// Tabletop: a horizontal fold, half folded. Content on the raised half, controls on the flat half.
    var tabletop: Bool { hasFold && !vertical && folded && fold != nil }
}

private struct FoldKey: EnvironmentKey { static let defaultValue = FoldState() }
extension EnvironmentValues {
    var fold: FoldState {
        get { self[FoldKey.self] }
        set { self[FoldKey.self] = newValue }
    }
}

/// A transparent view that reports the fold whenever the window resizes or the hinge moves.
struct FoldReader: UIViewRepresentable {
    @Binding var state: FoldState

    func makeUIView(context: Context) -> FoldObserverView {
        let view = FoldObserverView()
        view.onChange = { next in if next != state { state = next } }
        return view
    }

    func updateUIView(_ uiView: FoldObserverView, context: Context) {
        uiView.onChange = { next in if next != state { state = next } }
    }
}

final class FoldObserverView: UIView {
    var onChange: ((FoldState) -> Void)?
    private var hinge: FoldState.Hinge = .none

    override init(frame: CGRect) {
        super.init(frame: frame)
        isUserInteractionEnabled = false
        backgroundColor = .clear
        accessibilityElementsHidden = true
        if #available(iOS 27.1, *) {
            addInteraction(UIHingeInteraction { [weak self] _, update in
                guard let self else { return }
                if let h = update.hinge {
                    switch h.status {
                    case .closed: self.hinge = .closed
                    case .partiallyOpen: self.hinge = .partiallyOpen
                    case .fullyOpen: self.hinge = .fullyOpen
                    default: self.hinge = .unknown
                    }
                } else {
                    self.hinge = .none
                }
                self.refresh()
            })
        }
    }

    required init?(coder: NSCoder) { fatalError("init(coder:) is not used") }

    override func didMoveToWindow() { super.didMoveToWindow(); refresh() }
    override func layoutSubviews() { super.layoutSubviews(); refresh() }

    func refresh() {
        var divisions: [CGRect] = []
        if #available(iOS 27.1, *), let window {
            divisions = window.reservedRegions(kind: .division, options: .includeInactive).map(\.frame)
        }
        let next = FoldState(divisions: divisions, hinge: hinge)
        DispatchQueue.main.async { self.onChange?(next) }
    }
}

/// Layout tiers, from the space the window has rather than the device model.
enum Tier { case compact, expanded, book }

func tier(width: CGFloat, fold: FoldState) -> Tier {
    if fold.book { return .book }
    // A folding phone keeps list and detail together from 900pt, where the open display starts;
    // without a fold (iPad in portrait, Split View at half width) two columns fit from 700pt.
    return width >= (fold.hasFold ? 900 : 700) ? .expanded : .compact
}

/// How wide the list runs on the flat open display. `.narrow` is the fixed 320pt column 21 shipping
/// apps measured on a device use for plain rows. `.fold` runs it to the fold (about 476pt) for rows
/// that carry meters, figures or several values each, which the owner found cramped at 320pt.
enum ListWidth { case narrow, fold }

/// The list column beside a detail: `listWidth` while the open display lies flat, and up to the
/// fold once it folds like a book.
func listColumnWidth(_ fold: FoldState, _ listWidth: ListWidth = .narrow) -> CGFloat {
    if fold.book, let f = fold.fold { return max(280, f.minX) }
    if listWidth == .fold, fold.vertical, let f = fold.fold { return max(320, f.midX) }
    return 320
}
