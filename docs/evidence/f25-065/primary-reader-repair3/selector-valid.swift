import Foundation
final class Example: NSObject {
    private func seed() {}
    @objc func read(_ value: Any) {}
    func measure() {
        seed()
        let selector = #selector(read(_:))
        _ = selector
    }
}
