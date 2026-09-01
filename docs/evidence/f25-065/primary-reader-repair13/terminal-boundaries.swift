enum E: Error { case boom }
var stores = 0
var reads = 0
func seedInt() -> Int { stores += 1; return 1 }
func seedError() -> E { stores += 1; return .boom }
func seedVoid() { stores += 1 }
func read() { reads += 1 }
func sameReturn() -> Int { return seedInt(); read(); return 2 }
func newlineReturn() -> Int { return
  seedInt()
  read(); return 2 }
func commentReturn() -> Int { return /* terminal
  */ seedInt()
  read(); return 2 }
func sameThrow() throws { throw seedError(); read() }
func newlineThrow() throws { throw
  seedError()
  read() }
func commentThrow() throws { throw /* terminal
  */ seedError()
  read() }
func priorReturn() { return; seedVoid(); read() }
func afterNestedReturn() { if false { return }; seedVoid(); read() }
func doReturn() { do { return }; seedVoid(); read() }
func doThrow() throws { do { throw E.boom }; seedVoid(); read() }
func repeatReturn() { repeat { return } while false; seedVoid(); read() }
_ = sameReturn(); _ = newlineReturn(); _ = commentReturn()
do { try sameThrow() } catch {}
do { try newlineThrow() } catch {}
do { try commentThrow() } catch {}
priorReturn(); afterNestedReturn()
doReturn(); do { try doThrow() } catch {}; repeatReturn()
print("stores=\(stores) reads=\(reads)")
