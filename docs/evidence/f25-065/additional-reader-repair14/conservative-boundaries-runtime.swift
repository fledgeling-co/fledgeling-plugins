private var stores = 0
private var reads = 0

private func store() { stores += 1 }
private func read() { reads += 1 }
private func seed() { store() }
private func seed(_ value: Int) { _ = value; store() }
private func wrapper(value: Int) -> Int { value }
private enum Failure: Error { case expected }

private func commentsAndLiterals() {
    let text = #"return throw"#
    /* return /* throw */ */
    // return throw
    seed()
    read()
    _ = text
}

private func escapedKeywordControl() {
    let `return` = 1
    _ = `return`
    seed()
    read()
}

private func balancedControl() {
    seed(wrapper(value: (1 + 2)))
    read()
}

private func doReturn() {
    do { return }
    seed()
    read()
}

private func doThrow() throws {
    do { throw Failure.expected }
    seed()
    read()
}

commentsAndLiterals()
precondition(stores == 1 && reads == 1)
escapedKeywordControl()
precondition(stores == 2 && reads == 2)
balancedControl()
precondition(stores == 3 && reads == 3)

doReturn()
precondition(stores == 3 && reads == 3)
do {
    try doThrow()
    preconditionFailure("the expected error was not thrown")
} catch Failure.expected {}
precondition(stores == 3 && reads == 3)
print("stores=\(stores) reads=\(reads)")
