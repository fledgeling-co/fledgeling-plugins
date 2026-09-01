private var stored = 0

private func seed() {
    stored = 1
}

private func seed(_ body: () -> Void) {
    stored = 1
    body()
}

private func configure() {}

private func read() -> Int {
    stored
}

func testStoredClosureIsNotInvoked() {
    seed()
    let observation = { read() }
    _ = observation
}

func testImmediatelyInvokedClosure() {
    seed()
    let observation = { read() }
    _ = observation()
}

func testHelperTrailingClosureRemainsValid() {
    seed { configure() }
    _ = read()
}

func testLiteralFalseBranchDoesNotInvokeReader() {
    seed()
    if false { _ = read() }
}
