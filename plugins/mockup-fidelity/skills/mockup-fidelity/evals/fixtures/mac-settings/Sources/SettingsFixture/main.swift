// A Settings pane that is deliberately wrong, in eight specific ways.
//
// It exists to give mockup-fidelity's eval 9 a target that is a RUNNING MAC APP
// rather than an HTML file, because that eval is about what a second measurement
// engine can and cannot answer, and no HTML fixture can pose that question.
//
// The defects are split by which tier of the proctor lane can see them:
//
//   N1  absent            "Reset to Defaults" is in the mock and not built
//   N2  content           "Notifications" shipped as "Alerts"
//   N3  geometry          card top padding 16 -> 28
//   N4  hit size          the "Check" control is 44x20, under the 24pt floor
//   N5  unexposedControl  a 96x28 Manage button drawn by an NSView with no AX node
//   A1  radius            corner radius 8 -> 2          (needs the reflector)
//   A2  colour            accent #2f6df6 -> #3b6fd0     (needs the reflector)
//   A3  shadow            card shadow removed           (needs the reflector)
//
// N1-N5 are catchable from the accessibility tree, geometry and the tri-observer
// check, so they are catchable at BOTH tiers. A1-A3 are layer properties: at Tier
// A they are measurements, and at Tier B the only honest answer is inconclusive.
//
// A2 is the trap the eval is really built around. The colour difference is plainly
// visible in a screenshot, so a run at Tier B can "find" it by eyedropping the
// capture — and reporting it is a FALSE PASS in ANSWER-KEY.md, not a catch. An
// eyedropped colour is not a declared value, and a fixture whose only failure mode
// is missing something cannot test the failure mode of claiming too much.
//
// AppKit rather than SwiftUI, on purpose: ProctorReflector's own documentation says
// SwiftUI subtrees are walked as ordinary NSViews and there is no supported way to
// read resolved SwiftUI modifier values from outside the framework. A SwiftUI
// fixture would make Tier A and Tier B nearly indistinguishable, which is the one
// thing this fixture must not do.

import AppKit

// MARK: - The eight divergences, in one table

enum Divergence {
    static let cardCornerRadius: CGFloat = 2      // A1 · mock: 8
    static let accent = NSColor(srgbRed: 0x3b / 255.0, green: 0x6f / 255.0,
                                blue: 0xd0 / 255.0, alpha: 1)   // A2 · mock: #2f6df6
    static let cardShadow = false                 // A3 · mock: 0 1px 3px rgba(16,26,44,.16)
    static let cardPaddingTop: CGFloat = 28       // N3 · mock: 16
    static let updatesButtonHeight: CGFloat = 20  // N4 · mock: 28
    static let notificationsTitle = "Alerts"      // N2 · mock: "Notifications"
    static let buildResetButton = false           // N1 · mock has one
}

let ink = NSColor(srgbRed: 0x10 / 255.0, green: 0x1a / 255.0, blue: 0x2c / 255.0, alpha: 1)
let muted = NSColor(srgbRed: 0x6b / 255.0, green: 0x74 / 255.0, blue: 0x88 / 255.0, alpha: 1)
let line = NSColor(srgbRed: 0xd9 / 255.0, green: 0xde / 255.0, blue: 0xe8 / 255.0, alpha: 1)
let paneBG = NSColor(srgbRed: 0xf4 / 255.0, green: 0xf6 / 255.0, blue: 0xfa / 255.0, alpha: 1)

// MARK: - N5 · a control with pixels and no accessibility node

/// Draws a button. Exposes nothing.
///
/// A plain `NSView` is not an accessibility element, so this renders a
/// control-shaped, control-sized, labelled region that the accessibility tree has
/// no node for. Neither a tree walk nor a screenshot review finds that on its own —
/// the tree sees no control and the pixels look correct — which is what
/// `proctor_assert`'s `agree` kind exists to catch, reported as `unexposedControl`.
///
/// Sized 96x28 deliberately. A first cut drew it as a 38x22 switch and `agree`
/// returned seven findings with no `unexposedControl` among them: a region that
/// small appears to sit under the detector's threshold, so the planted defect was
/// invisible to the instrument meant to catch it. A planted defect the tool cannot
/// see tests nothing. The measurement is recorded in ANSWER-KEY.md rather than
/// quietly fixed, because it is a capability fact about `agree`, not about this app.
final class GhostControl: NSView {
    override var isFlipped: Bool { true }
    override func draw(_ dirtyRect: NSRect) {
        let body = NSBezierPath(roundedRect: bounds.insetBy(dx: 0.5, dy: 0.5),
                                xRadius: 6, yRadius: 6)
        Divergence.accent.setFill()
        body.fill()
        let title: NSString = "Manage"
        let attrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.systemFont(ofSize: 13, weight: .medium),
            .foregroundColor: NSColor.white,
        ]
        let size = title.size(withAttributes: attrs)
        title.draw(at: NSPoint(x: bounds.midX - size.width / 2,
                               y: bounds.midY - size.height / 2), withAttributes: attrs)
    }
    // Deliberately absent: isAccessibilityElement = true, setAccessibilityRole(.button),
    // setAccessibilityLabel("Manage"). Restoring those three lines is what fixing N5 means.
}

// MARK: - Card

final class Card: NSView {
    override var isFlipped: Bool { true }
    init(padTop: CGFloat = Divergence.cardPaddingTop) {
        super.init(frame: .zero)
        wantsLayer = true
        layer?.backgroundColor = NSColor.white.cgColor
        layer?.cornerRadius = Divergence.cardCornerRadius        // A1
        layer?.borderWidth = 1
        layer?.borderColor = line.cgColor
        if Divergence.cardShadow {                               // A3
            layer?.shadowOpacity = 0.16
            layer?.shadowOffset = CGSize(width: 0, height: 1)
            layer?.shadowRadius = 3
            layer?.shadowColor = ink.cgColor
        }
        self.padTop = padTop
    }
    required init?(coder: NSCoder) { fatalError() }
    var padTop: CGFloat = Divergence.cardPaddingTop
}

// MARK: - Builders

func label(_ text: String, size: CGFloat, weight: NSFont.Weight, colour: NSColor) -> NSTextField {
    let f = NSTextField(labelWithString: text)
    f.font = .systemFont(ofSize: size, weight: weight)
    f.textColor = colour
    return f
}

/// The same drawing as `GhostControl`, with the accessibility node PRESENT.
///
/// N4 and N5 are deliberately a matched pair: identical custom views, differing
/// only in whether they expose themselves. That isolates the variable — a run
/// that catches one and not the other is telling you about the observer, not
/// about the app.
///
/// It is a custom view rather than an `NSButton` because an `NSButton` would not
/// paint at this size. Constrained to 20pt with a `.rounded` bezel it reported
/// h=22 in the accessibility tree and drew nothing at all; `isBordered = false`
/// drew nothing either. `agree` flagged exactly that as a `ghostNode` — a control
/// the tree has and the pixels do not — which was correct and was an unplanted
/// defect. A fixture whose key says "hit size" while shipping an invisible button
/// is lying about what it tests, so the control is drawn by hand and the AppKit
/// behaviour is recorded in ANSWER-KEY.md instead.
final class TinyControl: NSView {
    private let title: String
    init(title: String, frame: NSRect) {
        self.title = title
        super.init(frame: frame)
        setAccessibilityElement(true)
        setAccessibilityRole(.button)
        setAccessibilityLabel(title)
    }
    required init?(coder: NSCoder) { fatalError() }
    override var isFlipped: Bool { true }
    override func draw(_ dirtyRect: NSRect) {
        let body = NSBezierPath(roundedRect: bounds.insetBy(dx: 0.5, dy: 0.5),
                                xRadius: 4, yRadius: 4)
        NSColor.white.setFill()
        body.fill()
        line.setStroke()
        body.lineWidth = 1
        body.stroke()
        let t: NSString = title as NSString
        let attrs: [NSAttributedString.Key: Any] = [
            .font: NSFont.systemFont(ofSize: 11, weight: .regular),
            .foregroundColor: ink,
        ]
        let size = t.size(withAttributes: attrs)
        t.draw(at: NSPoint(x: bounds.midX - size.width / 2,
                           y: bounds.midY - size.height / 2), withAttributes: attrs)
    }
}

func plainButton(_ title: String, height: CGFloat, primary: Bool = false) -> NSButton {
    let b = NSButton(title: title, target: nil, action: nil)
    b.bezelStyle = .rounded
    b.setButtonType(.momentaryPushIn)
    b.font = .systemFont(ofSize: 13)
    b.setAccessibilityLabel(title)
    b.wantsLayer = true
    b.layer?.cornerRadius = 6
    if primary {
        b.contentTintColor = .white
        b.layer?.backgroundColor = Divergence.accent.cgColor
    }
    b.translatesAutoresizingMaskIntoConstraints = false
    b.heightAnchor.constraint(equalToConstant: height).isActive = true
    return b
}

// MARK: - The pane

final class SettingsViewController: NSViewController {
    override func loadView() {
        let root = NSView(frame: NSRect(x: 0, y: 0, width: 560, height: 420))
        root.wantsLayer = true
        root.layer?.backgroundColor = paneBG.cgColor
        root.setAccessibilityIdentifier("settings.pane")

        let stack = NSStackView()
        stack.orientation = .vertical
        stack.alignment = .leading
        stack.spacing = 14
        stack.translatesAutoresizingMaskIntoConstraints = false
        root.addSubview(stack)
        NSLayoutConstraint.activate([
            stack.topAnchor.constraint(equalTo: root.topAnchor, constant: 24),
            stack.leadingAnchor.constraint(equalTo: root.leadingAnchor, constant: 24),
            stack.trailingAnchor.constraint(equalTo: root.trailingAnchor, constant: -24),
        ])

        let title = label("Settings", size: 22, weight: .semibold, colour: ink)
        title.setAccessibilityIdentifier("settings.title")
        stack.addArrangedSubview(title)

        // Card 1 — notifications, shipped under the wrong name, with a ghost toggle
        let toggle = GhostControl(frame: NSRect(x: 0, y: 0, width: 96, height: 28))
        toggle.translatesAutoresizingMaskIntoConstraints = false
        toggle.widthAnchor.constraint(equalToConstant: 96).isActive = true
        toggle.heightAnchor.constraint(equalToConstant: 28).isActive = true
        stack.addArrangedSubview(rowCard(
            id: "settings.card.notifications",
            heading: Divergence.notificationsTitle,                        // N2
            body: "Alert me when a run finishes or a gate fails.",
            trailing: toggle, width: 512))

        // Card 2 — updates, with a button under the hit-size floor
        stack.addArrangedSubview(rowCard(
            id: "settings.card.updates",
            heading: "Automatic updates",
            body: "Check daily and install in the background.",
            trailing: {
                let c = TinyControl(title: "Check",
                                    frame: NSRect(x: 0, y: 0, width: 44,
                                                  height: Divergence.updatesButtonHeight))  // N4
                c.translatesAutoresizingMaskIntoConstraints = false
                c.widthAnchor.constraint(equalToConstant: 44).isActive = true
                c.heightAnchor.constraint(
                    equalToConstant: Divergence.updatesButtonHeight).isActive = true
                return c
            }(),
            width: 512))

        // Card 3 — plain
        stack.addArrangedSubview(rowCard(
            id: "settings.card.location",
            heading: "Evidence location",
            body: "Captures and ledgers are written beside the project.",
            trailing: nil, width: 512))

        // Footer — "Reset to Defaults" is in the mock and is not built (N1)
        let footer = NSStackView()
        footer.orientation = .horizontal
        footer.spacing = 10
        footer.translatesAutoresizingMaskIntoConstraints = false
        if Divergence.buildResetButton {
            footer.addArrangedSubview(plainButton("Reset to Defaults", height: 28))
        }
        footer.addArrangedSubview(plainButton("Done", height: 28, primary: true))
        stack.addArrangedSubview(footer)
        footer.widthAnchor.constraint(equalToConstant: 512).isActive = true

        view = root
    }

    private func rowCard(id: String, heading: String, body: String,
                         trailing: NSView?, width: CGFloat) -> NSView {
        let card = Card()
        card.setAccessibilityIdentifier(id)
        card.translatesAutoresizingMaskIntoConstraints = false
        card.widthAnchor.constraint(equalToConstant: width).isActive = true

        let h = label(heading, size: 15, weight: .semibold, colour: ink)
        let p = label(body, size: 13, weight: .regular, colour: muted)
        let text = NSStackView(views: [h, p])
        text.orientation = .vertical
        text.alignment = .leading
        text.spacing = 4

        let row = NSStackView()
        row.orientation = .horizontal
        row.alignment = .centerY
        row.spacing = 12
        row.addArrangedSubview(text)
        if let trailing {
            let spacer = NSView()
            spacer.translatesAutoresizingMaskIntoConstraints = false
            spacer.setContentHuggingPriority(.init(1), for: .horizontal)
            row.addArrangedSubview(spacer)
            row.addArrangedSubview(trailing)
        }
        row.translatesAutoresizingMaskIntoConstraints = false
        card.addSubview(row)
        NSLayoutConstraint.activate([
            row.topAnchor.constraint(equalTo: card.topAnchor,
                                     constant: Divergence.cardPaddingTop),   // N3
            row.leadingAnchor.constraint(equalTo: card.leadingAnchor, constant: 18),
            row.trailingAnchor.constraint(equalTo: card.trailingAnchor, constant: -18),
            row.bottomAnchor.constraint(equalTo: card.bottomAnchor, constant: -16),
        ])
        return card
    }
}

final class AppDelegate: NSObject, NSApplicationDelegate {
    var window: NSWindow!
    func applicationDidFinishLaunching(_ note: Notification) {
        // Tier A is opt-in and needs ProctorReflector added by local path — see
        // README.md. Without it `proctor_inspect` answers `reflectorUnavailable`,
        // which is the fixture's default and the tier the eval leans on.
        #if PROCTOR_REFLECTOR
        ProctorReflector.start()
        #endif

        window = NSWindow(
            contentRect: NSRect(x: 0, y: 0, width: 560, height: 420),
            styleMask: [.titled, .closable, .miniaturizable],
            backing: .buffered, defer: false)
        window.title = "Settings Fixture"
        window.contentViewController = SettingsViewController()
        window.center()
        window.makeKeyAndOrderFront(nil)
        NSApp.activate(ignoringOtherApps: true)
    }
    func applicationShouldTerminateAfterLastWindowClosed(_ s: NSApplication) -> Bool { true }
}

let app = NSApplication.shared
let delegate = AppDelegate()
app.delegate = delegate
app.setActivationPolicy(.regular)
app.run()
