private var stores = 0
private var reads = 0

private func store() { stores += 1 }
private func read() { reads += 1 }

private func returnSeed() -> Int {
    store()
    return 7
}

private enum Failure: Error { case expected }

private func throwSeed() -> Failure {
    store()
    return .expected
}

private func returnedMeasure() -> Int {
    return
        returnSeed()
    read()
    return 0
}

private func thrownMeasure() throws {
    throw
        throwSeed()
    read()
}

precondition(returnedMeasure() == 7)
precondition(stores == 1 && reads == 0)

do {
    try thrownMeasure()
    preconditionFailure("the expected error was not thrown")
} catch Failure.expected {}

precondition(stores == 2 && reads == 0)
print("stores=\(stores) reads=\(reads)")
