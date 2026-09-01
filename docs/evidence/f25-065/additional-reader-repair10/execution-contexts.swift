private var stores = 0
private var reads = 0

private func store() { stores += 1 }
private func read() { reads += 1 }

private func seed(_ first: () -> Void, second: () -> Void) {
    store()
    second()
}

private func seed() { store() }

private func reset() {
    stores = 0
    reads = 0
}

reset()
seed { read() } second: {}
precondition(stores == 1 && reads == 0, "the reader-bearing first trailing closure was not invoked")

reset()
for _ in 0..<1 {
    seed()
    continue
    read()
}
precondition(stores == 1 && reads == 0, "continue makes the later reader unreachable")

reset()
for _ in 0..<1 {
    seed()
    break
    read()
}
precondition(stores == 1 && reads == 0, "break makes the later reader unreachable")

reset()
while false { seed() }
read()
precondition(stores == 0 && reads == 1, "the helper under while false never mutates")

reset()
if 0 == 1 { seed() }
read()
precondition(stores == 0 && reads == 1, "the helper under a false expression never mutates")

reset()
seed()
read()
precondition(stores == 1 && reads == 1, "valid direct mutation then read control")

reset()
seed({}) { read() }
precondition(stores == 1 && reads == 1, "valid invoked final closure control")

print("runtime boundaries passed")
