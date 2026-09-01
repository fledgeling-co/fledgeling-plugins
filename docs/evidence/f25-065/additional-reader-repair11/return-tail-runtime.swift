private var stores = 0
private var reads = 0

private func store() { stores += 1 }
private func read() { reads += 1 }
private func seed() -> Int {
    store()
    return 7
}

private func testMeasure() -> Int {
    return seed()
    read()
    return 0
}

precondition(testMeasure() == 7)
precondition(stores == 1 && reads == 0)
print("stores=\(stores) reads=\(reads)")
