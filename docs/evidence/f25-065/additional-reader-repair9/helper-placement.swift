private var seedCount = 0
private var readCount = 0

private func reset() {
    seedCount = 0
    readCount = 0
}

private func seed() {
    seedCount += 1
}

private func seed(_ body: () -> Void) {
    seedCount += 1
    body()
}

private func read() -> Int {
    readCount += 1
    return readCount
}

func testNestedHelperCall() {
    let invoke = { seed() }
    _ = invoke
    _ = read()
}

func testInactiveHelperCall() {
    #if false
    seed()
    #endif
    _ = read()
}

func testDirectHelperAndReader() {
    seed()
    _ = read()
}

func testTrailingHelperAndNestedReader() {
    seed { _ = read() }
}

func testImmediatelyInvokedReader() {
    seed()
    _ = { read() }()
}

func testReturnBeforeReader() {
    seed()
    return;
    _ = read()
}

reset()
testNestedHelperCall()
assert(seedCount == 0 && readCount == 1)

reset()
testInactiveHelperCall()
assert(seedCount == 0 && readCount == 1)

reset()
testDirectHelperAndReader()
assert(seedCount == 1 && readCount == 1)

reset()
testTrailingHelperAndNestedReader()
assert(seedCount == 1 && readCount == 1)

reset()
testImmediatelyInvokedReader()
assert(seedCount == 1 && readCount == 1)

reset()
testReturnBeforeReader()
assert(seedCount == 1 && readCount == 0)
