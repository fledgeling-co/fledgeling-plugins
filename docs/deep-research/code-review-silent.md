# silent

> Source: `~/Dev/dossier/silent/index.html`. Published research page, captured 20 August 2026 for the `code-review` and `atlas-publish` skills. Live at https://dossier.fledgeling.app/silent where published.

      
      [![](data:image/svg+xml;base64,<stripped>)
        **Margin**](https://margin.fledgeling.app/)
    
    

      
Perishable
        Cua ships 130+ commits a week. Every gap named here was measured on one day and may already be closed.

    
  

  

    Proctor against Cua · 15 August 2026
    
# It said *ok*. Nothing happened.

    

      
Cua Driver is an open-source tool that lets an AI agent operate a Mac. Its own documentation lists five situations where it reports a successful action and the machine did nothing at all. Those five cases are not a scandal. They are a specification, and they decide what a Mac testing tool should be building.

    
    

      
**The verdict.** Hand the hands over. Everything that clicks, types and targets a window is now a worse copy of something MIT-licensed shipping 130 commits a week.[15](#r15) Keep the instrument. What survives is not a better driver, it is the thing that tells you when the driver is lying.

    
  

  

    

      Cua's own limits page
      
## Five ways to succeed at nothing

      
Every pair below is documented by Cua, about Cua: what the caller was told, set against what the machine actually did.

    

    

      Driver said
      Machine did
      

        
ok
        
ok
        
ok
        
ok
        
ok
        
no commit
        
no-op
        
wrong place
        
menu bar only
        
black frame
      
    

    

      
Minimised window
A Return keypress into a minimised window "returns success, but the field doesn't commit". [3](#r3)

    
    

**1**  of 5 cases where the report and the machine disagree
  

  

    The decision
    
## Give away the hands, keep the verdict

    

      

        Hand over
        
### Actuation

        

          - Background clicking and typing through the accessibility layer

          - Window and element targeting

          - The drawn agent cursor

          - Permission checks and the installer

          - Browser handoff, where Cua went further and drives the real window

        

      
      

        Keep building
        
### Measurement

        

          - Determinism scoring: run a flow five times, report where the runs first diverged[1](#r1)

          - Selectors that survive a replay, built on the identifier Apple ships for testing

          - Accessibility auditing on an app you did not write[12](#r12)

          - Visual fidelity against a design[26](#r26)

          - In-process reading of resolved colour and type, for apps you own[13](#r13)

        

      
      

        Where you win
        
### Disagreement

        

          - Compare the tree against the geometry against the pixels, and report the gap

          - Label every capture with whether the frame can be trusted[9](#r9)

          - Catch the five silent failures above, which nothing currently catches[3](#r3)

          - Score the app under test, where the benchmarks score the agent[7](#r7)

        

      
    
  

  

    The objection that changed the plan
    
A tool that checks three witnesses needs at least one it can trust.

    

      
The first draft of this report said Proctor should be rebuilt entirely on top of Cua, consuming its accessibility tree and its screenshots. An adversarial review took that apart using the report's own evidence.

      
Cua returns the tree and a screenshot together, and says plainly why: the tree lies on some surfaces.[2](#r2) Off-Space SwiftUI windows come back holding only a menu bar.[3](#r3) And nothing in Cua's documented surface labels a screenshot with whether the frame is complete,[5](#r5) while Apple defines six frame states and expects a consumer to check before trusting one.[9](#r9)

      
**So both channels are suspect, and a cross-check with two unreliable witnesses is not a cross-check.** The conclusion moved: Cua for actuation, Proctor for observation. Keep the capture path, because frame status has to be known where the frame is taken, not inferred afterwards from an image somebody else handed you.

      
Cua's screen-lock defect is the same shape and is still open. A user reproduced a capture returning zero pixels alongside 746 accessibility elements, every one of them a menu bar item. The maintainers' own framing is that the agent "has no way to know any of it happened".[20](#r20)

    
  

  

    Checked against the market
    
## What nobody packages

    
The competitive question is narrower than it first looked. Appium and Squish both drive native Mac apps without source access, and both are maintained.[24](#r24)[25](#r25) The gap is not automation. It is measurement.

    

    

      | Capability | Who has it | Verdict |

      
        | Background actuation on a Mac | Cua, Appium, Squish | Solved |

        | Durable semantic selector for replay | Appium and Squish; not Cua, whose element handle is per-snapshot[4](#r4) | Partial |

        | Repeat-run determinism scoring | Standard in web CI, absent on native macOS[28](#r28) | Nobody |

        | Frame trustworthiness on a capture | Apple documents the states; no driver surfaces them[9](#r9)[5](#r5) | Nobody |

        | Accessibility audit of a third-party app | Apple's own audit runs only on an app you build[12](#r12), and on macOS six of nine checks apply[11](#r11) | Nobody |

        | Visual fidelity for a native Mac app | Percy and Applitools are browser and mobile only[26](#r26); VisWiz will not capture for you[27](#r27) | Nobody |

        | Scoring the app under test | Cua-Bench scores the agent, deliberately[7](#r7) | Nobody |

      
    

    
  

  

    The risk that is not competition
    
## An empty shelf is not the same as a queue of buyers

    

      
Three projects looked like competitors and none survived a closer look. One has four stars and thirteen commits, all made on a single day.[21](#r21) Another's apparent outside interest turns out to be automation: a fix submitted by an account holding 17,888 public repositories, and an issue that is openly a directory advertisement.[22](#r22) The third is real and active but drives interfaces by what they look like rather than through accessibility, which makes it a different tool.[23](#r23)

      
The harder finding is on the other side of the shelf. Across Hacker News, GitHub and an archive sweep that returned 170 subreddit posts, **no first-hand account was found of anyone using a computer-use agent to test an application and reporting what happened.** This is the thinnest-sourced conclusion here, resting on three community sources out of forty-two, and it is stated at that strength rather than louder.

      
What the practitioner record does contain is agents failing. One person automating insurance-broker workflows described an agent asked to download twenty files: "It downloaded 3, hallucinated the rest, and reported success."[30](#r30) Benchmarks put proprietary agents above 30% on macOS overall and at 17 to 21% on ordinary file and productivity work, though that paper has had a later version withdrawn and the number should be re-checked before anyone leans on it.[29](#r29)

      
**An agent that finishes a fifth of ordinary tasks cannot be the thing that drives a repeatable test.** That does not remove the opportunity, it moves it. The value is in measuring how unreliable a run was, not in producing the run.

    
  

  

    If you build on it
    
## What depending on Cua actually means

    

      
The encouraging half is verifiable rather than claimed. One MIT licence covers the whole repository including the driver.[16](#r16) In ninety days, 652 pull requests were merged from people other than the two main committers, so this is open development rather than a company repository with a licence bolted on.[17](#r17) The repository carries 21,368 stars.[14](#r14)

      
The cautionary half is just as checkable. This is a 2025 Y Combinator company with a stated team of three.[18](#r18) Every named production user is the vendor's own claim, and none of the four companies has confirmed it anywhere.[19](#r19) The commercial product is sold infrastructure sitting on the free driver, which is a reason the driver probably stays free and also a reason its priorities follow the paying half.

      
One more thing follows from the commit rate rather than from the code: **every gap named on this page is perishable.** A verdict with no expiry date is the wrong artifact. Re-check before building, and again before shipping.

    
  

  

    Methods
    
## How this was made, and what it cannot tell you

    

      
Six search tasks ran across documentation, platform references, the practitioner record, company filings and a final pass aimed only at the contradictions the first five produced. The source registry was frozen before a word was drafted, and the drafting tool rejects a report that cites anything outside it. It rejected this one once.

      
Four adversarial lenses then attacked the finished report. They raised nine objections, five serious. Two changed the recommendation: the observation-versus-actuation split described above, and a correction to a claim that Cua has no durable selector at all. It does have one for pixel coordinates. The narrower and defensible claim is that it has no durable *semantic* selector, so a replay survives only by clicking the same absolute position, which is what a layout change breaks.[4](#r4)

      
**What this cannot tell you.** Every statement about what Cua does not do comes from Cua's own documentation, which is the weakest possible authority on a vendor's own absences. Nothing here was verified against the shipped binary, and nothing was built. Several Apple pages carry no publication date and one is from 2022, so they are treated as describing the shape of an API rather than proving its behaviour today. The claim that Cua's app-hosted daemon is a permissions mechanism rather than an introspection API is documented,[6](#r6) as is its verification contract of roughly forty evidence-bearing cells per test application.[8](#r8) Background capture without raising a window rests on an Apple session from 2022.[10](#r10)

      
        PanelFree lane. Six tasks run with the session's own web search. Nothing was charged.
        Corpus42 sources, 13 domains. 33 cited, every one dereferenced, none fabricated.
        ReviewFour lenses: claim validation, source diversity, recency, internal contradiction.
        HumanCommissioned, directed and reviewed by Luke Rhodes. Research and drafting were automated.
        As of15 August 2026, and not a day later.
      
    
  

  

    Sources
    
## The frozen registry

    

      1. Cua Driver MCP tool reference: element fields, verify_state, and replay. [cua.ai/docs/reference/cua-driver/mcp-tools.md](https://cua.ai/docs/reference/cua-driver/mcp-tools.md)

      1. Capture and delivery modalities: why the tree and the screenshot are returned together. [cua.ai/docs/concepts/capture-and-delivery-modalities.md](https://cua.ai/docs/concepts/capture-and-delivery-modalities.md)

      1. Cua Driver known limits, including the silent-failure cases. [cua.ai/docs/reference/cua-driver/limits.md](https://cua.ai/docs/reference/cua-driver/limits.md)

      1. Interface contracts, including the stale element token error. [cua.ai/docs/reference/cua-driver/contracts.md](https://cua.ai/docs/reference/cua-driver/contracts.md)

      1. MCP tool notes: the action-level effect field. [cua.ai/docs/reference/cua-driver/mcp-tool-notes.md](https://cua.ai/docs/reference/cua-driver/mcp-tool-notes.md)

      1. App-hosted daemon reference. [cua.ai/docs/reference/cua-driver/embedding.md](https://cua.ai/docs/reference/cua-driver/embedding.md)

      1. The Cua-Bench task lifecycle. [cua.ai/docs/concepts/cua-bench-task-lifecycle.md](https://cua.ai/docs/concepts/cua-bench-task-lifecycle.md)

      1. How Cua Driver is validated. [cua.ai/docs/concepts/how-cua-driver-is-validated.md](https://cua.ai/docs/concepts/how-cua-driver-is-validated.md)

      1. Apple, SCFrameStatus. [developer.apple.com/documentation/screencapturekit/scframestatus](https://developer.apple.com/documentation/screencapturekit/scframestatus)

      1. Apple WWDC22 session 10155, on single-window capture. [developer.apple.com/videos/play/wwdc2022/10155](https://developer.apple.com/videos/play/wwdc2022/10155)

      1. Apple, XCUIAccessibilityAuditType and its per-platform availability. [developer.apple.com/documentation/XCUIAutomation/XCUIAccessibilityAuditType](https://developer.apple.com/documentation/XCUIAutomation/XCUIAccessibilityAuditType)

      1. Apple, performAccessibilityAudit on XCUIApplication. [developer.apple.com/documentation/xctest/xcuiapplication/4191487-performaccessibilityaudit](https://developer.apple.com/documentation/xctest/xcuiapplication/4191487-performaccessibilityaudit)

      1. Apple's accessibility model: semantic properties, no visual ones. [developer.apple.com/library/archive/.../OSXAXmodel.html](https://developer.apple.com/library/archive/documentation/Accessibility/Conceptual/AccessibilityMacOSX/OSXAXmodel.html)

      1. GitHub API, trycua/cua repository statistics. [api.github.com/repos/trycua/cua](https://api.github.com/repos/trycua/cua)

      1. GitHub API, trycua/cua commit activity. [api.github.com/repos/trycua/cua/stats/commit_activity](https://api.github.com/repos/trycua/cua/stats/commit_activity)

      1. The repository's MIT licence. [raw.githubusercontent.com/trycua/cua/main/LICENSE.md](https://raw.githubusercontent.com/trycua/cua/main/LICENSE.md)

      1. GitHub API search: merged pull requests excluding the two core committers. [api.github.com search, merged PRs](https://api.github.com/search/issues?q=repo:trycua/cua+is:pr+is:merged+-author:f-trycua+-author:r33drichards)

      1. Y Combinator company page for Cua. [ycombinator.com/companies/cua](https://ycombinator.com/companies/cua)

      1. Cua's own site, including its named production users. [cua.ai](https://cua.ai/)

      1. Cua issue 1745: driving while the desktop is locked. [github.com/trycua/cua/issues/1745](https://github.com/trycua/cua/issues/1745)

      1. mac-use, an MCP server marketing itself for macOS QA. [github.com/entpnomad/mac-use](https://github.com/entpnomad/mac-use)

      1. mac-use-mcp issue 32, and the accounts appearing on it. [github.com/antbotlab/mac-use-mcp/issues/32](https://github.com/antbotlab/mac-use-mcp/issues/32)

      1. OculiX, the SikuliX successor. [github.com/oculix-org/Oculix](https://github.com/oculix-org/Oculix)

      1. Appium's Mac2 driver. [appium.github.io/appium-mac2-driver](https://appium.github.io/appium-mac2-driver/latest)

      1. Squish for Mac. [qt.io/quality-assurance/squish](https://qt.io/quality-assurance/squish/platform-automated-mac-gui-testing)

      1. Visual regression tooling coverage. [percy.io/blog/visual-regression-testing-tools](https://percy.io/blog/visual-regression-testing-tools)

      1. VisWiz, bring-your-own-capture visual diffing. [viswiz.io](https://viswiz.io/)

      1. Google on flaky tests and repeat runs. [testing.googleblog.com, May 2016](https://testing.googleblog.com/2016/05/flaky-tests-at-google-and-how-we.html)

      1. macOSWorld: computer-use agent success rates on macOS. [arxiv.org/abs/2506.04135](https://arxiv.org/abs/2506.04135)

      1. A practitioner on desktop agents fabricating success. [news.ycombinator.com/item?id=46796280](https://news.ycombinator.com/item?id=46796280)

    

  

  

    

      [![](data:image/svg+xml;base64,<stripped>)](https://github.com/fledgeling-co/dossier-research-mcp)
      [![](data:image/svg+xml;base64,<stripped>)](https://margin.fledgeling.app/)
    
    

      
## Research that argues with itself before it argues with you

      
This page came out of Dossier, a research MCP that runs a panel of backends, freezes a source registry before a word is drafted, and refuses a draft that cites anything outside it. Four adversarial lenses then attack the finished report. Five of the nine objections they raised were serious, and two of them changed the recommendation you are about to read.

    
    
      Cost$0. The free lane, run with the session's own web search.
      Corpus42 sources, 13 domains, six search tasks.
      Citations33 cited, all dereferenced, none fabricated.
      ReviewedFour adversarial lenses, nine objections, two changed the conclusion.
