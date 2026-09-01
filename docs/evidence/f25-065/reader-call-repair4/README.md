# Rejected layered reader-guard attempt

This is retained failed author evidence, not a validation receipt. After primary FAIL `824e9aa0`,
the first repair added a statement-context predicate on top of the earlier identifier, qualification,
parenthesis and trailing-closure guards. The focused and portable suites stayed green, but the actual
source mutation run exited 1: three old guards could be removed without failing because the new
context rule already refused the same inputs. Those redundant faults receive no credit.

The implementation was not committed. The next repair removes the overlapping guards and binds the
contract to two independently live conditions: reader call syntax and a conservative invocation
context. `mutations.json` is the operative proof that this intermediate design was rejected rather
than reported as green.
