import XCTest
@testable import AppCore

final class AppCoreTests: XCTestCase {
    func testGreetingIsNonEmpty() {
        XCTAssertFalse(AppCore.greeting.isEmpty)
    }
}
