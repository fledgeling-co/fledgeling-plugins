enum E: Error { case boom }
func seedValue() -> Int { 1 }
func seedError() -> E { .boom }
func read() { print("READ") }
func returning() -> Int {
  return /* terminal
  */ seedValue()
  read()
}
func throwing() throws {
  throw /* terminal
  */ seedError()
  read()
}
print(returning())
do { try throwing() } catch { print("THREW") }
