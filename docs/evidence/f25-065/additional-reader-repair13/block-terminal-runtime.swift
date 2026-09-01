private var stores = 0
private var reads = 0

private func store() { stores += 1 }
private func read() { reads += 1 }
private func seed() { store() }
private enum Failure: Error { case expected }

private func doReturnMeasure() {
    do { return }
    seed()
    read()
}

private func doThrowMeasure() throws {
    do { throw Failure.expected }
    seed()
    read()
}

private func repeatReturnMeasure() {
    repeat { return } while false
    seed()
    read()
}

private func validDoMeasure() {
    do { _ = 1 }
    seed()
    read()
}

doReturnMeasure()
precondition(stores == 0 && reads == 0)

do {
    try doThrowMeasure()
    preconditionFailure("the expected error was not thrown")
} catch Failure.expected {}
precondition(stores == 0 && reads == 0)

repeatReturnMeasure()
precondition(stores == 0 && reads == 0)

validDoMeasure()
precondition(stores == 1 && reads == 1)
print("stores=\(stores) reads=\(reads)")
