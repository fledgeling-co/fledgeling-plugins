private var stored = 0

private func seed() {
    stored = 1
}

private func seed(_ body: () -> Void) {
    stored = 1
    body()
}

private func configure() {}
private func read() -> Int { stored }
private func read(λ value: Int) -> Int { value }
private func read(`repeat` value: String) -> String { value }
private func read(_ first: Int, _ second: Int) -> Int { first + second }

func testDirectReader() {
    seed()
    _ = read()
}

func testHelperTrailingThenDirectReader() {
    seed { configure() }
    _ = read()
}

func testUnicodeAndBacktickReferences() {
    seed()
    let unicode: (Int) -> Int = read(λ:)
    let escaped: (String) -> String = read(`repeat`:)
    let wildcard: (Int, Int) -> Int = read(_:_:)
    _ = (unicode, escaped, wildcard)
}

func testDeliberatelyConservativeNestedReaders() {
    seed()
    do { _ = read() }
    _ = { read() }()
}

