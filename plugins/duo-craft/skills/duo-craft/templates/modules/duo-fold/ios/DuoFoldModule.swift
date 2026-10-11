import ExpoModulesCore
import UIKit

/// Where a folding iPhone's fold is and how far its hinge is open, for layout in JavaScript.
///
/// React Native has no fold API, so this reads UIKit's reserved regions (iOS 27.1) from a
/// transparent view laid over the key window. Division regions are queried with
/// `.includeInactive`, so a device with a fold reports it even while it lies flat (the region
/// is then inactive and has no width); that is what lets the app hold one two-pane layout
/// instead of rearranging each time the hinge moves. On any other device, and below iOS 27.1,
/// the state is "no fold, no hinge".
public final class DuoFoldModule: Module {
  private let lock = NSLock()
  private var state: [String: Any] = DuoFoldModule.noFold
  private var observer: FoldObserverView?
  private var attachAttempts = 0

  static let noFold: [String: Any] = [
    "hasFold": false,
    "divisions": [[String: Any]](),
    "hinge": "none",
    "hingeAngle": NSNull(),
  ]

  public func definition() -> ModuleDefinition {
    Name("DuoFold")

    Events("onChange")

    Function("getState") { () -> [String: Any] in
      self.lock.lock()
      defer { self.lock.unlock() }
      return self.state
    }

    OnCreate {
      DispatchQueue.main.async { self.attach() }
    }

    OnDestroy {
      DispatchQueue.main.async {
        self.observer?.removeFromSuperview()
        self.observer = nil
      }
    }
  }

  /// The window does not exist yet when the module is created at bridge start-up, so retry
  /// until it does. Twenty tries a quarter of a second apart covers a slow cold launch.
  @MainActor
  private func attach() {
    guard observer == nil else { return }
    guard let window = Self.keyWindow() else {
      attachAttempts += 1
      if attachAttempts < 20 {
        DispatchQueue.main.asyncAfter(deadline: .now() + 0.25) { self.attach() }
      }
      return
    }
    let view = FoldObserverView(frame: window.bounds)
    view.onChange = { [weak self] next in self?.publish(next) }
    window.addSubview(view)
    observer = view
    view.refresh()
  }

  private func publish(_ next: [String: Any]) {
    lock.lock()
    let changed = !NSDictionary(dictionary: state).isEqual(to: next)
    if changed { state = next }
    lock.unlock()
    if changed { sendEvent("onChange", next) }
  }

  @MainActor
  private static func keyWindow() -> UIWindow? {
    let scenes = UIApplication.shared.connectedScenes.compactMap { $0 as? UIWindowScene }
    for scene in scenes {
      if let key = scene.windows.first(where: { $0.isKeyWindow }) { return key }
    }
    return scenes.first?.windows.first
  }
}

/// A transparent, non-interactive view covering the window. It re-reads the reserved regions
/// whenever it is laid out (the window resized: opened, closed, rotated, Split View) and
/// whenever the hinge reports a change (folded without resizing).
final class FoldObserverView: UIView {
  var onChange: (([String: Any]) -> Void)?
  private var hingeStatus = "none"
  private var hingeAngle: CGFloat?

  override init(frame: CGRect) {
    super.init(frame: frame)
    isUserInteractionEnabled = false
    backgroundColor = .clear
    autoresizingMask = [.flexibleWidth, .flexibleHeight]
    accessibilityElementsHidden = true
    if #available(iOS 27.1, *) {
      addInteraction(UIHingeInteraction { [weak self] _, update in
        guard let self else { return }
        if let hinge = update.hinge {
          self.hingeAngle = hinge.angle
          switch hinge.status {
          case .closed: self.hingeStatus = "closed"
          case .partiallyOpen: self.hingeStatus = "partiallyOpen"
          case .fullyOpen: self.hingeStatus = "fullyOpen"
          default: self.hingeStatus = "unknown"
          }
        } else {
          self.hingeStatus = "none"
          self.hingeAngle = nil
        }
        self.refresh()
      })
    }
  }

  required init?(coder: NSCoder) { fatalError("init(coder:) is not used") }

  override func layoutSubviews() {
    super.layoutSubviews()
    refresh()
  }

  override func traitCollectionDidChange(_ previous: UITraitCollection?) {
    super.traitCollectionDidChange(previous)
    setNeedsLayout()
  }

  func refresh() {
    var divisions: [[String: Any]] = []
    if #available(iOS 27.1, *) {
      divisions = reservedRegions(kind: .division, options: .includeInactive).map { region in
        let f = region.frame
        return [
          "x": Double(f.origin.x),
          "y": Double(f.origin.y),
          "width": Double(f.size.width),
          "height": Double(f.size.height),
          "active": region.isActive,
        ]
      }
    }
    onChange?([
      "hasFold": !divisions.isEmpty || hingeStatus != "none",
      "divisions": divisions,
      "hinge": hingeStatus,
      "hingeAngle": hingeAngle.map { Double($0) as Any } ?? NSNull(),
    ])
  }
}
