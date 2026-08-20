# The effect boundary — proving the product did something, not that it decided to

A campaign ran 230 cases over a zero-trust CI runner. Every case was accounted
for, 220 of them were mutation-armed and watched to fail, the strict ratchet sat
at 194, and the requirement *"runner communication is outbound pull only via
HTTPS/WSS on TCP 443"* was recorded `observed`.

The product had no HTTP client in its dependency tree. It spawned no process from
any line of production code. It emitted no mDNS. `tart`, `wsl.exe`, `pfctl` and
`nft` were never executed — the isolation engines were string generators that
nothing called, and the daemon bound `127.0.0.1`. The requirement passed because
**nothing communicated**, so the constraint on how communication must happen was
never tested by anything.

That is a named condition with a forty-year literature behind it, and the campaign
was missing exactly half of a known pair.

---

## 1. Two directions, and the campaign had one

Ball and Kupferman state both directions in one sentence: *"If the system
satisfies the mutated specification … the specification is satisfied in some
vacuous way. If the mutated system satisfies the specification … some elements of
the system are not covered"* (*Vacuity in Testing*, TAP 2008, pp. 4–17).

Arming — revert the behaviour an assertion guards, watch it go red, restore — is
the second direction. It mutates the **system**. Two hundred and twenty armed
cases is two hundred and twenty measurements of the same half, and no number of
them can detect that the specification was never exercised. The first direction
mutates the **specification**, and it is the one this campaign had never run.

The base rate says how much that costs. IBM Haifa measured that *"typically 20% of
formulas are found to be trivially valid, and that trivial validity **always**
points to a real problem in either the design or its specification or
environment"* (Beer, Ben-David, Eisner & Rodeh, *Formal Methods in System Design*
18(2), 2001, p. 141). A requirement inventory with no vacuity check should expect
hollow passes as the normal case, not the pathological one.

Hardware verification shipped this two decades ago. SystemVerilog gives vacuous
success a place in the language: an implication `A |-> B` succeeds vacuously when
the antecedent never matches, and the standard remedy is to pair every implication
assertion with a `cover property` on its antecedent (Doulos, *SystemVerilog
Assertions Tutorial*). Nothing equivalent has reached general-purpose test
frameworks; four independent research backends looked, and none found a mainstream
xUnit, acceptance or requirements tool that reports a vacuous pass.

---

## 2. The fifth evidence class

`project-comprehension.md` §2 records four evidence classes for a requirement.
This is the fifth, and it holds the gate:

- **Vacuous** — the guarantee holds only because the capability it constrains
  never runs. Formally, `G(communication → outbound_443)` is true in a system that
  never communicates. Carries the constrained capability and the reason it does not
  execute.

`vacuous` and `contradicted` are different findings with different remedies.
Contradicted means the document and the product disagree about something the
product does. Vacuous means the product does not do the thing at all, so there is
nothing for the constraint to be true or false about. Reading them as one status
sends a missing subsystem to the place that fixes a wrong one.

Two neighbouring statuses already exist and this one sits beside them.
`inconclusive` is an instrument problem and wants a better instrument. `unoracled`
is a specification problem and wants an oracle built. `vacuous` is a **product**
problem and wants the capability built — or the claim withdrawn.

---

## 3. The census, at requirement time, before a single test exists

The cheapest detector runs in phase 1 and costs one judgement call per
requirement. Every requirement classed `affordance` or `behaviour` whose text
names an effect outside the process gets an `effect` field from this closed list:

```
subprocess · outbound-socket · inbound-socket · packet-filter · multicast
filesystem-write · device · ipc · none
```

The mapping is the judgement. Everything after it is mechanical: for each declared
class, the production dependency graph and the call graph reachable from a shipped
entry point must contain a provider of it.

```bash
# outbound-socket: is there a client in the tree at all?
grep -c '^name = "reqwest"\|^name = "hyper"\|^name = "ureq"' Cargo.lock

# subprocess: census the sites, excluding tests
grep -rn "Command::new" --include="*.rs" crates/*/src/

# reachability: a pub fn nothing calls is not an implementation
cargo install cargo-workspace-unused-pub && cargo workspace-unused-pub
```

A requirement whose declared effect class has no provider in production source is
`vacuous` at phase 1, before any test is written — not `contradicted`, which is
what §2 above distinguishes: contradicted means the product does the thing and
does it differently from the document, and there is nothing here for the document
to disagree with. The campaign above would have found five of its six central
claims here, in the first hour, for the price of three greps.

**Rust's own dead-code lint cannot do this for you.** `dead_code` detects unused,
*unexported* items; it does not fire on a `pub` item in a library crate, because
the compiler works crate-by-crate and a `pub` item may be another crate's API.
Isolation drivers written as `pub fn` string generators produce zero warnings.
Workspace-wide detection needs `cargo-workspace-unused-pub` or `warnalyzer`;
rustc's own `-Ztreat-pub-as-pub-crate` is unstable.

---

## 4. Why the standard test toolkit cannot see this

The deployed isolation stack asserts the **absence** of I/O, never its presence.
`pytest --disable-socket` raises `SocketBlockedError` on any socket use;
`WebMock.disable_net_connect!` breaks the build on any external request;
`nock.disableNetConnect()` throws `NetConnectNotAllowedError`.

A suite built on those tools is structurally unable to tell *"correctly outbound
only"* from *"never communicates"*, because both produce zero blocked-socket
events. The oracle this needs does not exist off the shelf and has to be built.

Coding agents push a suite further in the same direction, measured: across 1.2M
2025 commits in 2,168 repositories, agent-authored commits added mocks to tests at
**36%** against **26%** for non-agent commits, and modified test files at **23%**
against **13%** (Hora & Robbes, *Are Coding Agents Generating Over-Mocked Tests?*,
arXiv:2602.00409, MSR 2026). How much of that converts into escaped defects is not
established — one backend on this panel flagged the consequence as
practitioner-report evidence rather than measurement, and that split is honest to
report rather than to resolve.

---

## 5. The oracle rung: `effect-witness`

A `raster-visual` pass owes a capture method and a frame status. An
`effect-witness` pass owes a **recorder, a class, and a non-zero count**, on the
same principle: a rung that claims something the other rungs cannot claim carries
the evidence obligation that makes the claim checkable.

Four parts make a witness causal rather than circumstantial:

1. the effect was driven from a **production entry point**, not by calling the
   generator directly from a test;
2. an **attempt** was recorded at the boundary — `execve`, `connect`, `sendto`,
   `bpf`, a netlink write, a file open;
3. **completion** was confirmed by something other than the code under test — the
   peer, the guest, the kernel, a process table, a sentinel file;
4. **sabotage flips it** — deny the effect and the scenario fails.

Part 4 is the one that is easy to skip and hardest to fake. Without it, a witness
proves an attempt happened near the test rather than because of it.

### Where the bar sits, and the panel does not agree

Two positions came back, and both are defensible:

- **The kernel bar.** An external-effect requirement may not be `observed` below a
  full four-part witness with independent completion and sabotage. Instruments:
  `strace -f -e trace=network`, an eBPF syscall census, `eslogger` on macOS,
  DTrace. This is the strong reading, and on a machine with the privilege for it,
  it is right.
- **The portable floor.** Most campaigns run on a developer machine with no root,
  no `bpf` and SIP enabled. The floor that still bites there is a **real** loopback
  listener that logs accepted connections, or a **real** spawned process that
  writes a sentinel file the test then reads. No kernel, no privilege, and it
  cannot pass when nothing runs.

Take the kernel bar where the lane supports it, record the portable floor as the
lane's ceiling where it does not, and say which was used. A lane that cannot
reach the kernel is a recorded structural limit, exactly as `--cannot-attach` is
for glass. What is not available is silence about which one was run.

### The rung is not always the cheapest detector

The instrument is the reflex and it is often the wrong first move. In the campaign
above, an in-process check with no instrument at all found a live defect the suite
had passed:

```
mutating RPC verbs: examined=7 changed=4 unchanged=2 unoracled=1
  stop_runner       UNCHANGED  reported ok=true, runner-mac-01 still present=true
  stop_all_runners  UNCHANGED  reported 2 stopped, 2 -> 2
  restart_runtime   UNORACLED  returns ok=true "…restarted successfully"
```

`stop_runner` returned `true` twice for the same runner and the runner never left
the fleet. The transport tests were careful, guarded against a constant return,
and asserted the reply's shape — `stop_all_runners_carries_the_count_the_daemon_reported`
compares the daemon's claim against a reading taken **before** the action, and
never reads again. One extra line would have caught it.

That generalises into a check needing no privilege and no new lane: **after the
last mutating call in a test body, does any reader appear?** Over the same suite:

```
test fns: examined=164 mutating=21 re-read-after=4 blind=17
```

Seventeen of twenty-one. Five of them in a file named `supervisor_effect_tests.rs`.
Run this before reaching for a tracer; it is a `grep` and it finds the same class
of hollow pass one level in.

---

## 6. The control: strengthen the specification and watch it break

This is the campaign's own arming rule turned on the half it was missing, and it
is the single most valuable line in this document.

Take a requirement that passes. Mutate its constraint to one that is **strictly
harder to satisfy**. Re-run. It must go red.

```
"outbound only on TCP 443"   →   "outbound only on TCP 1"
"at most two macOS guests"   →   "at most zero macOS guests"
"80 GB free before pre-warm" →   "80 TB free before pre-warm"
```

A strengthened constraint that still passes proves the check reads nothing, and
every verdict that check has ever issued is worthless. This is Ball and Kupferman's
definition executed literally: a suite passes a specification vacuously when the
specification can be replaced by a harder one that the suite still passes.

`vacuity-check.py --seed-strengthen` runs it. On the campaign above it would have
gone green on the first attempt, in under a second, in wave 1.

---

## 7. What this does not settle

- **Absence is weaker than presence.** "No provider in the production tree today"
  is a fact about this commit. It is not proof the capability never existed and
  not proof it cannot be added; say the narrow true thing.
- **A witness proves the effect, not its correctness.** A recorded `connect` to
  port 443 says a socket opened. Whether the payload was right is a different case
  at a different rung.
- **A count is not a distribution.** One non-zero effect count on one run is one
  draw. Where the effect is the product's central security claim, the case wants
  repeats and a stated failure mode, the same as any other flaky-sensitive lane.
- **Nothing here detects a capability nobody claimed.** The census reads the
  requirement inventory, so a product that quietly opens a socket no document
  mentions is sweep C's problem, not this one's.
