# vacuous

> Source: `~/Dev/dossier/vacuous/index.html`. Published research page, captured 20 August 2026 for the `code-review` and `atlas-publish` skills. Live at https://dossier.fledgeling.app/vacuous where published.


      Primer
      Brief
      Technical
    
  

  

    

      Testing·
      20 August 2026·
      Luke Rhodes
    
    
# The suite passed a guarantee it never ran.

    
A team wrote 230 tests for a program, checked that 220 of them could actually catch a mistake, and every one of them passed. Then somebody read the program and found it never talks to the internet at all. The tests weren't lying. They were checking a promise about something the program doesn't do.

    
A campaign closed 230 cases, armed 220 of 220 passing ones, cleared every gate, and recorded a network policy as observed. The product has no HTTP client in its dependency tree. The condition has a name, a measured base rate since 2001, and a detector that costs about as much as running the suite.

    
Arming an assertion mutates the system and finds what a suite fails to cover. Vacuity needs the specification mutated instead, and it's the direction that catches G(communication → outbound_443) holding because the antecedent never fires. One campaign ran the first direction 220 times and the second never.

    

      4 research backends · 151 sources · 47 domains
      Evidence as at 20 Aug 2026
    

    

      

        One cell per case · 230 cases from one campaign
        220 passing, 220 armed, 0 at a rung that asks for an effect outside the process
      
      

      

        **Marked · assertion ran and was watched to fail (220)
        **Not measurable on this host (10)
      
      

        
        And the branch that was never a case. It has no cell in the grid above,
          which is the entire problem: nothing counted it, so nothing reported it missing.
      
    
  

  

    

      
## The short version

      
## What this found

      
## Finding

      

        
A test can pass for a boring reason: the thing it was checking never happened. If you promise "when the car moves, the seatbelt light comes on", and the car never moves, you've kept the promise perfectly and learned nothing.

        
People who verify computer chips have known this since about 2001, and they gave it a name. They also measured how often it happens, and it turned out to matter every single time it did.

        
The odd part is that ordinary software testing never picked the idea up, and most of the tools you'd reach for to catch it can't see it. One of them can't see it on purpose.

      
      

        
A guarantee can hold because the capability it constrains never runs. Everything reads green, every number is true, and the suite has learned nothing about the thing it was written for.

        
Hardware verification named this, measured it and shipped a remedy two decades ago. Software testing mostly didn't, and the parts of the modern toolkit you'd expect to catch it are blind for structural reasons rather than accidental ones.

        
The cheap half of the fix is a grep. On the campaign that missed it, that grep found a live defect in about ten minutes.

      
      

        
Ball and Kupferman define two directions of mutation. Mutating the system finds coverage gaps; mutating the specification finds guarantees never exercised at all.[1](#S1) A campaign arming every assertion is running one direction of a two-direction technique.

        
Mutation testing mutates code that exists, so a boundary nothing reaches yields no mutants. Line coverage counts execution, and a rule generator's lines all execute. And the test-isolation stack asserts the *absence* of I/O by design, so it cannot separate "correctly outbound-only" from "never communicates".[4](#S4)

        
The remedy transfers intact from SVA: pair every implication with a cover on its antecedent.[3](#S3) In a requirement inventory that becomes an effect class plus a provider in production source.

      
    

    

      The load-bearing numbers
      

        - **230**cases closed, 220 of 220 passing ones armed, every gate clear.[L1](#L1)

        - **0**of those cases stood at a rung that asks for an effect outside the process, because no such rung existed.[L1](#L1)

        - **20%**of formulas trivially valid in production hardware verification, and trivial validity *always* pointed at a real problem.[2](#S2)

        - **26/32**tests that change state and never read the observable again. One grep, 164 test functions.[L3](#L3)

        - **3**verbs found reporting success while changing nothing, in the campaign that had already passed them.[L4](#L4)

      

      

        What would change this
        
If somebody measured how often this happens in normal software, instead of in computer chips. Nobody has.

        
A measurement of the base rate in software requirement inventories. The 20% figure comes from hardware model checking, and whether it transfers is untested.

        
A software-domain replication of the Beer et al. base rate. The mechanism transfers by construction; the rate is borrowed and marked as borrowed.[2](#S2)

      
    
  

  
  

    
01The pass
    
  

      
## Every number in it was true

      

        
The program is a build machine. You give it a job, it runs the job somewhere sealed off from the rest of your network, and it reports back. So the promises are all about the sealed-off part: what gets in, what gets out, which door things use.

        
The tests said all of that worked. And they'd been checked in the strongest way a test can be checked: somebody deliberately broke the program, watched each test go red, then put it back. 220 of them, one at a time.

        
Then a person on a different project read the code and noticed the program never opens a connection to anything. The sealed-off part isn't sealed off; it just doesn't exist yet. The bit that writes the firewall rules writes them and never runs them.

      
      

        
The product is a self-hosted CI runner built around network isolation, so a lot of what it promises is about a boundary: what crosses it, in which direction, on which port. Of its 33 requirements, 17 name an effect that happens outside the process.[L3](#L3)

        
The campaign closed 230 cases and armed 220 of 220 passing ones, which is the strongest evidence a suite can offer that its assertions bite. Revert the behaviour an assertion guards, watch it go red, restore it. Two hundred and twenty times.[L1](#L1)

        
Somebody working on a neighbouring project then read the source. No HTTP client anywhere in the dependency tree. No line of production code that spawns a subprocess. The isolation engines generate their rules and execute none of them; the daemon only ever binds loopback.[L2](#L2)

      
      

        
The campaign: 230 cases, 220 pass, 10 n/a with structural reasons, 0 fail, 0 inconclusive, 0 open. Armed 220/220. Eight lanes, four of them proved on glass with an artifact and an attachment witness.[L1](#L1)

        
The source, read at commit 8441437: zero Command::new in production code and eight in test harnesses; no HTTP client crate in Cargo.lock; no mDNS anywhere in product src; 127.0.0.1:9876 as the daemon's only default bind.[L2](#L2)

        
The requirement read "runner communication is outbound pull only over HTTPS/WSS on TCP 443", and it was recorded as observed. It is true. Nothing communicates.

        
Formally that's G(communication → outbound_443) with an antecedent that never fires. The suite proved the implication and never once evaluated its right-hand side.

      
    

  
  

    
02The name
    
  

      
## It's half of a technique, and the campaign shipped the other half

      

        
There's a trick for checking whether your tests are any good: break the program on purpose and see if a test notices. If nothing goes red, the test wasn't watching.

        
That trick has a twin, and the twin is the one nobody uses. Instead of breaking the *program*, you make the *promise* harder. If you promised "the car goes at most 60" and you change it to "the car goes at most 0" and everything still passes, the car isn't moving.

        
Two researchers wrote both halves down together in 2008. Most testing only ever picked up the first one.

      
      

        
Arming is mutation applied to the system. Break the behaviour, watch the case go red, restore. It's the right instrument and it answers a real question: does this assertion bite?

        
Ball and Kupferman defined it alongside its opposite. Mutate the system and you find what the suite doesn't cover; mutate the specification and you find what the suite never exercised at all.[1](#S1) They're two directions of one technique, written down in the same paper.

        
A campaign that arms every assertion is running one direction, 220 times, and the other direction never. It's not that the evidence was weak. It's that it was evidence about a different question.

      
      

        
The definition, verbatim: "If the system satisfies the mutated *specification* … the specification is satisfied in some vacuous way. If the mutated *system* satisfies the specification … some elements of the system are not covered."[1](#S1)

        
The detector is written down too, and it costs about what running the suite costs. For a deterministic specification: "whenever a branch of S is taken, we mark it, and T passes S vacuously in P if we are done testing T and some branch is still not marked". NLOGSPACE-complete.[1](#S1)

        
The catch for a software campaign is that a prose requirement has no branch structure to mark. Which is the actual work: giving a requirement enough shape that an unmarked branch is a thing a script can see. Inference

      
    

  
  

    
03The rate
    
  

      
## One in five, and it always meant something

      

        
Engineers who check computer chips ran into this constantly, so they counted it. About one promise in five was passing for a boring reason.

        
The part that should make you sit up isn't the one in five. It's what they found underneath: every single time a promise passed for a boring reason, something was genuinely wrong. Not usually. Not mostly.

      
      

        
IBM Haifa measured this across years of production hardware verification, and published the number in 2001: about 20% of formulas came back trivially valid on first runs.[2](#S2)

        
The stronger half of the finding is the qualifier they attached to it. Trivial validity *always* pointed at a real problem, in the design or the specification or the environment.[2](#S2) It's a signal with, on their evidence, no false positives.

        
I'm conscious that's a hardware number and this is a software problem. The mechanism transfers by construction; the rate is borrowed, and it's worth saying so plainly rather than quoting 20% at a codebase and hoping.

      
      

        
Beer, Ben-David, Eisner and Rodeh, *FMSD* 18(2), p. 141: "typically 20% of formulas are found to be trivially valid, and that trivial validity **always** points to a real problem in either the design or its specification or environment."[2](#S2)

        
Scope: ACTL formulas, hardware model checking, one organisation's production practice through the late 1990s. No software-domain replication exists that these four research runs surfaced.

        
A detector with no measured false positives is worth building even if you never learn its true positive rate in your domain.Inference

      
    

  
  

    
04The blind spot
    
  

      
## Every instrument you'd reach for, and one that's blind by design

      

        
You'd think a good testing toolkit would catch this. It doesn't, and the reasons are worth knowing because none of them is carelessness.

        
One tool works by breaking your code in small ways to see if tests notice. It can only break code that's there, and the problem here is code that isn't.

        
Another counts which lines of your program the tests ran. The lines all ran. They just don't do anything to the outside world.

        
And the third one is the awkward one. There's a whole family of tools whose job is to stop tests touching the network, so they run fast and don't depend on the internet. They're good tools. But if your entire test setup is built to prove nothing touches the network, it can't tell you the difference between a program that's carefully polite about the network and one that has never heard of it.

      
      

        
Three instruments, three different reasons for missing it.

        
Mutation testing mutates the code that exists. If nothing production-reachable opens a socket, spawns a process or writes a filter rule, the mutation denominator holds only the internal model, and a clean run means the denominator was empty rather than the code correct.

        
Coverage counts lines the suite executed. A rule generator's lines all execute, thoroughly, and produce strings.

        
The third is the uncomfortable one, because it's blind on purpose. pytest --disable-socket, WebMock.disable_net_connect! and nock.disableNetConnect() all assert the absence of I/O.[4](#S4) They're correct for their job. A suite that treats them as the whole picture cannot separate "correctly outbound-only" from "never communicates", because both look identical from inside.

      
      

        
The language toolchain has a fourth gap in this family. Rust's dead_code lint "detects unused, unexported items", so a pub fn in a library crate that nothing calls anywhere in the workspace produces no warning at all; the compiler works crate by crate and a pub item may be another crate's API.[9](#S9) Answering it needs cargo-workspace-unused-pub or an equivalent SCIP index.[10](#S10)

        
Worth separating two axes here that get conflated. cargo-machete and cargo-shear find unused *dependencies*, which is the "no HTTP client" half. Only the workspace-wide tools find unused *public functions*, which is the "rule generators nobody calls" half.

      

      

        

          Can it see a guarantee held up by a capability that never runs?
          | Instrument | Sees it | Why not |

          
            | Assertion arming / mutation testing |  | Mutates code that exists. A boundary nothing reaches has no mutants to catch.This is the instrument the campaign ran 220 times. |

            | Line and branch coverage |  | Counts execution. A rule generator executes fully and emits a string. |

            | Network isolation harnesses |  | Asserts the absence of I/O by design, so absence reads as compliance.[4](#S4) |

            | Rust dead_code |  | Detects unused *unexported* items only.[9](#S9) |

            | Workspace unused-pub analysis |  | Answers "does anything call this, anywhere" across the workspace.[10](#S10) |

            | SVA vacuity reporting |  | Standardised for two decades in hardware, and unavailable in this form to a software suite.[3](#S3) |

            | Effect census over the requirement inventory |  | Names the effect, then looks for the thing in production source that could perform it. |

          
        

      
      
An empty cell is an instrument that returns clean on this condition. It is not a defect in the instrument.

    

  
  

    
05The cheap half
    
  

      
## Two of the checks are greps, and one of them found a live bug

      

        
The fix isn't clever. For each promise, write down what it makes the program do out in the world: start something, open a connection, write a file. Then go and find the piece of the program that could actually do that. If there isn't one, the promise isn't verified and you knew before writing a single test.

        
There's a second check that's even cheaper. Look through the tests for ones that tell the program to change something and then never look again to see whether it changed. Those tests can only be checking that the program said "done".

        
Running that second check on the campaign took a few minutes and turned up three commands that report success and do nothing at all.

      
      

        
The remedy from hardware transfers almost unchanged. In SVA, an implication that succeeds because its antecedent never matched is reported as a vacuous success, and the standard practice is to pair every implication with a cover on its antecedent.[3](#S3)

        
In a requirement inventory that becomes two fields. An **effect class** naming what the requirement makes the product do outside its own memory, and a **provider**: the thing in production source that could perform it. A requirement claiming an effect with no provider is unverified before you write a test.

        
The second check is a scan of the test tree for a call that changes state with no read after it. That shape is how a verb gets to report success while doing nothing, because the only thing the test reads is the verb's own return value.

        
On the campaign above, that scan read 164 test functions, found 32 that call a state-changing verb, and found 26 of them never reading the observable again. Five of the 26 sat in a file named for the effect it wasn't measuring.[L3](#L3)

      
      

        
Both passes are name-based and deliberately generous. The census over-flags: a false positive costs one "effect": "none" and a false negative costs the campaign its central claim. The blind scan under-flags: a read called for an unrelated reason still counts, so 26 is a floor rather than an estimate.

        
The denominator moves with the declared mutator vocabulary, which is why it gets printed rather than summarised.

      

      

        Measured 20 Aug 2026 · vacuity-check.py, blind pass over crates/
        
```
unclassed:  examined=33  findings=17
uncensused: examined=0   findings=0
blind:      examined=164 mutating=32 re-read-after=6 blind=26
```

      
      

        Measured 20 Aug 2026 · every mutating RPC verb, against the observable it claims to change
        
```
set_max_concurrency  CHANGED    2 -> 5
cancel_job           CHANGED    job 52119 gone, 2 -> 1
clear_queue          CHANGED    2 -> 0
stop_runner          UNCHANGED  reported ok=true, runner still present=true
stop_all_runners     UNCHANGED  reported 2 stopped, 2 -> 2
restart_runtime      UNORACLED  returns ok=true; nothing specified for a check to read
mutating RPC verbs: examined=7 changed=4 unchanged=2 unoracled=1
```

      
      
stop_runner returns true twice for the same runner and never removes it. stop_all_runners reports the count it didn't change. restart_runtime returns "Hypervisor and container daemons restarted successfully" having restarted nothing.[L4](#L4) The case covering that last one stood at the outcome rung, and the outcome it asserted was the arrival of a sentence.

      
restart_runtime is recorded unoracled rather than failing, which is a different condition with the opposite remedy. Nothing was ever specified that a check could read, so there's no authority to appeal to; an inconclusive wants a better instrument and an unoracled wants an oracle built.[L4](#L4)

      
stop_runner says it stopped the runner. Ask again and the runner's still there, and it says it stopped it again. That's the whole bug, and 230 tests walked past it.

    

  
  

    
06The agents
    
  

      
## The suites are getting more simulated, and that's measured

      

        
One more thing worth knowing, though it's a weaker piece of evidence than the rest of this page. When AI coding assistants write tests, they reach for fakes more often than people do. Somebody counted it across a million-odd changes to real projects.

        
A fake stands in for the real thing. That's often fine. It also means the test never touches the real thing, which is exactly the gap this page is about.

      
      

        
Hora and Robbes mined 1.2M commits from 2025 across 2,168 repositories, isolating 48,563 agent-authored ones. Agent commits added mocks to tests at 36% against 26% for non-agent commits, and modified test files at 23% against 13%.[7](#S7)

        
I'd be careful with what that does and doesn't show. It measures mocking rate, not whether the resulting suites are hollow, and those are different questions. The panel that surfaced it flagged the consequence as insufficiently evidenced even while agreeing the rate is real, and that split is worth preserving rather than smoothing over.

        
Separately, METR recorded o3 reward-hacking on 30% of RE-Bench runs, which included modifying tests to raise a score.[8](#S8) That's the mechanism by which a hollow pass gets *reported* rather than found.

      
      

        
Both figures are observational and neither establishes causation toward vacuity. What they establish is that the population of suites is drifting toward simulation at a measurable rate, which raises the prior on a class of defect that no instrument in the table above detects.Inference

        
Related and worth naming for anyone building a gate rather than a document: instruction-following degrades across long interactions. Laban et al. measured a 39% average drop from single-turn to multi-turn across 15 models and 200,000+ simulated conversations, decomposing into −15% aptitude and +112% unreliability.[11](#S11) It's why the remedy shipped here is an exit code and not a paragraph.

      
    

  
  

    
07Not settled
    
  

      
## Where the floor sits, nobody agreed

      
There's one thing the research didn't settle, and it stays unsettled here. If you want proof that a program really did something out in the world, how strong does the proof have to be? The two answers pull in opposite directions and both have a point.

      
The four research runs split on where the evidence floor sits for an effect outside the process, and the split is the finding rather than a problem to resolve. Both readings are defensible and choosing between them is a judgement about who runs the suite.

      
The disagreement is recorded in the shipped reference rather than resolved in it. A gate that encodes the strict reading on a laptop is a gate nobody can pass; a gate that encodes the permissive reading on a CI box is a gate that certifies less than it claims.[1](#S1)

      

        

          The strict reading
          
### Kernel or nothing

          
Nothing below a kernel-observed causal effect may be recorded as observed. A production entry point, a sabotage that flips the result, removal of the test action failing, and a machine-verifiable artifact. Anything softer is a model of the effect wearing the effect's name.

        
        

          The portable reading
          
### A real floor without root

          
A machine without root still has a genuine floor: a real loopback listener logging its accepts, or a real spawned process writing a sentinel file. Setting the bar at dtrace on every host means the rung goes unused, and an unused rung catches nothing.

        
      
      
I lean portable, for the reason the second box gives; a gate that opens red on a developer machine gets switched off inside a week, and a switched-off gate is worth nothing. But I'd rather record that as a lean than launder it into a consensus the evidence doesn't support.

    

  
  

    
08Methods
    
  

      
## How this was made, and what it can't tell you

      
Four research backends ran the same brief concurrently: OpenAI, Gemini, Perplexity and a local Claude lane. 151 sources across 47 independent registrable domains, with 3% overlap between members. A fifth lane (Antigravity) refused to start and is counted as a failure rather than dropped.

      
Every member's report was exported and read end to end before anything here was written, and citations on the load-bearing member were checked: 44 dereferenced, 0 fabricated, 0 dead. One did not resolve (systemverilog.us/attempt.pdf, for the SVA LRM section number) and its claim is carried here only on the independently resolving Doulos tutorial.[3](#S3)

      
The local measurements are primary evidence about one repository on one machine, not general findings. They were taken on macOS 25.6.0 against commit 8441437 on 20 August 2026, and the commands that produced them are printed above rather than described.

      
**What this can't tell you.** How often vacuity occurs in software requirement inventories; the 20% is a hardware number. Whether agent-written suites are hollower than human ones, as opposed to more mocked. Whether the effect census finds things in codebases that do perform external I/O, since the only inventory it has been run against is the one that doesn't.

      
Design reference: Mobbin section trawl, 2 queries, 12 results opened. Took the empty-cell convention for absence, the label-and-content grid for the registry, and the above-the-fold density. Left the gradient card mosaic and the dark instrument ground, the second because three pages in this portfolio already use it.

    

  

    
09Registry
    

      
## The frozen registry

      
Cited from this list and nowhere else. Sources marked L are local artefacts read on this machine, not published documents.

    
  

  
S1 · Peer-reviewedBall & Kupferman, *Vacuity in Testing*, TAP 2008.[doi.org/10.1007/978-3-540-79124-9_2](https://doi.org/10.1007/978-3-540-79124-9_2)
  
S2 · Peer-reviewedBeer, Ben-David, Eisner & Rodeh, *Efficient Detection of Vacuity in Temporal Model Checking*, Formal Methods in System Design 18(2), 2001, p. 141.[link.springer.com/article/10.1023/A:1008779610539](https://link.springer.com/article/10.1023/A:1008779610539)
  
S3 · ReferenceDoulos, SystemVerilog Assertions tutorial.[doulos.com · systemverilog-assertions-tutorial](https://www.doulos.com/knowhow/systemverilog/systemverilog-tutorials/systemverilog-assertions-tutorial/)
  
S4 · Repositoriespytest-socket, WebMock and nock, read for their stated behaviour on blocked connections.[github.com/miketheman/pytest-socket](https://github.com/miketheman/pytest-socket) · [bblimke/webmock](https://github.com/bblimke/webmock) · [nock/nock](https://github.com/nock/nock)
  
S7 · Repository miningHora & Robbes, arXiv:2602.00409, MSR 2026 (accepted). 1.2M commits, 2,168 repositories.[arxiv.org/abs/2602.00409](https://arxiv.org/abs/2602.00409)
  
S8 · EvaluationMETR, *Recent frontier models are reward hacking*, 5 June 2025.[metr.org/blog/2025-06-05-recent-reward-hacking](https://metr.org/blog/2025-06-05-recent-reward-hacking/)
  
S9 · Vendor docsrustc, the dead_code lint: "detects unused, unexported items".[doc.rust-lang.org · warn-by-default lints](https://doc.rust-lang.org/rustc/lints/listing/warn-by-default.html)
  
S10 · Repositorycargo-workspace-unused-pub, workspace-wide unused pub detection via a SCIP index.[github.com/cpg314/cargo-workspace-unused-pub](https://github.com/cpg314/cargo-workspace-unused-pub)
  
S11 · Peer-reviewedLaban, Hayashi, Zhou & Neville, arXiv:2505.06120, ICLR 2026.[arxiv.org/abs/2505.06120](https://arxiv.org/abs/2505.06120)
  
L1 · Local artefactCampaign registry for the product under discussion, read 20 Aug 2026 via campaign.py check. 33 requirements, 33 surfaces, 230 cases, armed 220/220.
  
L2 · Local artefactSource tree at commit 8441437, read 20 Aug 2026: Cargo.lock and crates/**/src.
  
L3 · Local measurementvacuity-check.py --tests crates, 20 Aug 2026. Output printed above verbatim.
  
L4 · Local measurementmutating_verb_effect_sweep.rs, 20 Aug 2026. Output printed above verbatim.

  

    Vacuous · 20 August 2026 · Luke Rhodes
    Evidence as at 20 Aug 2026 · 151 sources · 47 domains
