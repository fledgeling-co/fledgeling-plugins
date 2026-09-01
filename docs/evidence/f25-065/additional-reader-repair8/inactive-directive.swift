private var readCount = 0

private func seed() {}

private func read() -> Int {
    readCount += 1
    return readCount
}

func testInactiveDirective() {
    seed()
    #if false
    _ = read()
    #endif
}

func testMissingModuleDirective() {
    seed()
    #if canImport(DefinitelyMissingF25065Module)
    _ = read()
    #endif
}

testInactiveDirective()
testMissingModuleDirective()
assert(readCount == 0)

