# cadence

> Source: `~/Dev/dossier/cadence/index.html`. Published research page, captured 20 August 2026 for the `code-review` and `atlas-publish` skills. Live at https://dossier.fledgeling.app/cadence where published.

      
      [![](data:image/svg+xml;base64,<stripped>)
        **Margin**](https://margin.fledgeling.app/)
    
    

      
Artifact-checked
        Every load-bearing number here was read from the vendor page, the API or the shipping file — not from the research that commissioned it.

    
  

  

    Permit to work · macOS maintenance
    Compiled 15 August 2026
    Theme: auto
  

  
# The gap was never the automation

  
Unattended deletion already runs on macOS — on a ten-minute
  timer, in a rule engine two decades old, and in a product the market leader withdrew
  five weeks ago. The position nobody occupies is narrower and stranger than that.

  

    
**The finding.** What is unbuilt is not a program that acts while you
    are away. It is one whose *permission widens as the interval lengthens* — a job
    running every fifteen minutes allowed less than the same job running weekly, because
    the cost of a wrong deletion does not fall just because you checked more often.

    
**The open question.** Whether the set of things people will let
    software delete unattended is large enough to build a business on. Nothing here
    settles it, and the one company that tried has stopped.

  

  
    Read this as
    Read this as
    
    **Primer**from scratch
    
    **Brief**what it means
    
    **Technical**how we know
  

  Interlock 01 · the permit

  
## A program that waits longer should be trusted with more

  
## Permission should widen with the interval, and nowhere doesInference

  
## Cadence-coupled permission has no shipping precedentInference

  

    
Lots of programs already tidy your Mac while you are not watching. What none of
    them do is trust themselves more when they have waited longer.[1](#r1)[2](#r2)

    
Here is why that matters. If a program checks every fifteen minutes and gets one
    thing wrong, it has thrown away something you needed and you find out much later. If
    it only wakes once a week, it can afford to stop and ask you first. So the safe rule
    is not "check often" or "check rarely" — it is that the more often it runs, the less
    it should be allowed to touch on its own.

  

  

    
Unattended action is not the gap. It already ships: a ten-minute launch agent that
    kills processes without asking,[2](#r2)
    a rule engine that has acted on files for about twenty years,[3](#r3)
    and until July, a product that cleaned enrolled Macs on a schedule and forced the job
    through if the user skipped it.[1](#r1)

    
What none of the three does is vary its permission by cadence. Each has one
    permitted action set and one timer. The unoccupied position is the coupling: a fifteen
    minute job allowed only what it can prove is regenerable, a weekly one allowed to
    propose deleting a git worktree — because the cost of being wrong is unchanged by how
    recently you last looked.

  

  

    
Scheduled unattended deletion on macOS has at least three shipping precedents:
    cc-reaper's 600-second LaunchAgent,[2](#r2)
    Hazel's rule engine,[3](#r3)
    and CleanMyMac Business's 7/14/30-day Smart Scan automation until
    2026-07-14.[1](#r1)
    None couples the permitted action set to the schedule period.

    
The coupling is what is unoccupied, and the argument for it is a cost asymmetry
    rather than a convenience one: deletion risk is a property of the target's
    reproducibility, and it does not decay with observation frequency. A high-frequency
    tier therefore has to be *narrower*, not merely faster.

    
**Limit.** This is assembled from three examples, not an exhaustive
    survey. The absence of a fourth is weaker evidence than the presence of these three.

  

  
    
The permit widens with the interval — and the ceiling never moves

    

      
        The permit envelope across five cadences
        A band representing what may be deleted without asking. It is
        narrowest at the fifteen-minute cadence and widest at seven days. A flat ceiling
        line above it marks the class of things never deleted unattended at any cadence:
        live connections, other people's repositories, and anything the user has
        protected. This is a diagram of a design rule, not measured data.

        
        
        NEVER, AT ANY CADENCE — LIVE CONNECTIONS · OTHER PEOPLE'S REPOS · PROTECTED PATHS

        
        

        
        

        
        
          
          
          
          
          15 min
          1 hour
          12 hours
          1 day
          7 days
        
        INTERVAL BETWEEN RUNS →

        
        
          dead processes
          build output
          tool-vouched caches
          dead simulators
          worktrees
        

        
        
          The longer it waits, the more it may do
        
        
          acts on its own
          ↓ HEIGHT = WHAT IT MAY REMOVE WITHOUT ASKING
        
        
          7d PROPOSES, WAITS FOR A HUMAN
        
      
    
    **This is a diagram of a design rule, not measured data.**
    The vertical axis is ordinal — a widening class of permitted targets — and carries no
    quantity. The ceiling is the point: widening the permit never raises it.
  

  Interlock 02 · the withdrawn permit

  
## The one company that sold this stopped selling it

  
## The proof that it works was cancelled in July

  
## The cited evidence terminated four weeks before it was cited

  

    
One big company sold a version of this to businesses. It cleaned the Macs at a
    company on a timer, and if someone kept putting it off, it went ahead anyway. They
    stopped selling it in July, and did not say why.[1](#r1)

    
The research done for this page pointed at that product to prove the idea works.
    The page it pointed at now says the product was cancelled.[4](#r4)

  

  

    
CleanMyMac Business was the single commercial product shipping scheduled unattended
    macOS cleaning: Smart Scan automation on 7, 14 or 30-day intervals, with forced
    execution if a user skipped it. MacPaw withdrew it effective 14 July
    2026.[1](#r1)

    
A commissioned research backend rated that product its strongest evidence for the
    central question, at "Medium to High Confidence", and cited its documentation more than
    a dozen times as proof the model was commercially viable. Dereferencing that URL
    returns the discontinuation notice.[4](#r4)

    
**What this does not establish.** MacPaw gave no reason beyond focusing
    on other products. Nothing here shows the automation failed, or that it caused the exit.
    What it does mean is that the product can no longer be cited as evidence that scheduled
    unattended cleaning sells.

  

  

    
CleanMyMac Business Smart Scan automation: admin-configured tasks with a start
    datetime, repeat interval of 7, 14 or 30 days, a forced-execution day and time on skip,
    and a configurable reminder count. Cleaned system log files, broken login items, user
    cache files and language files across enrolled devices. Schedule parameters were
    immutable after creation. Discontinued effective
    2026-07-14, announced 2026-07-29.[1](#r1)

    
The failure mode this exposes is general: a live-resolving URL is not a live claim.
    Citation verification proves dereferenceability, not that the content still supports
    the proposition attached to it. The panel's citation resolved perfectly.[4](#r4)

    
**Limit.** Causation is unestablished. A B2B withdrawal is equally
    consistent with go-to-market economics, support cost, or portfolio strategy. Both the
    "demand failed" and "distribution failed" readings survive this evidence intact.

  

  

    

      Artifact · vendor notice
      macpaw.com · 29 July 2026
    
    

      
“We've made the difficult decision to discontinue CleanMyMac Business, effective
      July 14, 2026.”

    
    
Read directly from the URL the research cited as its evidence
    that the model works.[1](#r1)

  

  Interlock 03 · it already runs

  
## Someone already built this, and almost nobody found it

  
## A ten-minute timer already reaps processes, and waits an hour before it does

  
## Sustained-window confirmation is shipping, at fifteen stars

  

    
One project already does this every ten minutes. It watches for programs that have
    lost the thing that started them and are now stuck burning the machine's
    power.[2](#r2)

    
The clever part is the waiting. It will not act on one look, because one look cannot
    tell a program that is working hard from a program that is broken — both look identical.
    So it waits for an hour of bad behaviour first.

    
At least six people built this same tool without knowing about each other. Almost
    nobody found any of them.[5](#r5)

  

  

    
cc-reaper runs a launch agent every ten minutes, finds processes whose parent has
    died, and kills them — unattended, no prompt. It requires 80 percent average CPU
    sustained for at least an hour before it treats one as a runaway, which is a sustained
    test rather than a snapshot.[2](#r2)

    
It also scopes the kill by identity, never by name: group cleanup targets only groups
    whose *leader* is a session it owns, and it "never matches by group membership".
    A separate team hit the same wall and built a registry proving a process belongs to
    their own config path before killing it.[6](#r6)
    Two teams, no contact, same rule.

    
Six independent implementations of this idea exist. None has more than fifteen
    stars.[5](#r5)
    The idea is not rare. Finding it is.

  

  

    
cc-reaper: LaunchAgent at 600s detecting PPID=1 orphans; runaway trigger requires
    `CC_RUNAWAY_CPU` ≥ 80 *and* `CC_RUNAWAY_MIN` ≥ 60 minutes
    elapsed. Companion janitors at hourly (disk) and Sunday 04:00 (weekly clean). It rejects
    TTY filtering on measured grounds — in SSH, Docker and tmux every process reports
    `TTY=?`. Ancestor guard walks `$$` → PID 1 and never kills a
    forebear.[2](#r2)

    
Its protection list carries a deliberate override: Chrome, Spotlight and shared MCP
    servers are protected, but "a process pinned at high CPU for hours is broken, regardless
    of category". Cloudflare's MCP server is named as explicitly not protected because it
    orphans and pins CPU.[2](#r2)

    
Convergent design worth noting: ownership proof by config path (Empryo) and by
    process-group leader identity (cc-reaper), both rejecting pattern matching, which cannot
    distinguish your runaway from another session's healthy
    worker.[6](#r6)

    
**Limits.** cc-reaper is at 15 stars — established as existing and
    well-designed, not as adopted. The six-implementation count comes from a single query
    shape on one day and is a floor, not a census.[5](#r5)

  

  Interlock 04 · what it costs to leave one running

  
## A forgotten helper program ate a hundred gigabytes

  
## This stopped being tidiness and became stability

  
## Orphaned agent processes, measured at the upper tail

  

    
When these helper programs are forgotten, they do not just sit there quietly. One of
    them kept growing until it had taken about a hundred gigabytes — enough to fill a
    laptop.[7](#r7)
    On another machine, forgotten helpers crashed the computer
    outright.[8](#r8)

  

  

    
This is no longer a housekeeping problem. An orphaned tool server reached roughly
    100 GB on an M4 Max.[7](#r7)
    On 16 GB machines, orphaned language-server and shell instances grew about 1.25 GB each
    per 35 minutes and produced kernel panics with 50 GB of swap
    swell.[8](#r8)
    One team's telemetry found a single machine holding 127 orphaned
    processes.[6](#r6)

    
That is the honest case for acting rather than advising. A tool that notices this and
    then writes you a recommendation has not solved it.

  

  

    
Three primary reports: `oraios/serena` #1367, ~100 GB RSS from an orphaned
    MCP server on an M4 Max;[7](#r7)
    `anomalyco/opencode` #12687, ~1.25 GB per instance per 35 minutes from
    unbounded output concatenation (O(n²)), causing kernel panics and ~50 GB swap swell at
    16 GB unified memory;[8](#r8)
    Empryo telemetry, 127 orphaned processes holding 725 MB on one
    host.[6](#r6)

    
**Limit, and it is a real one.** These are issue-tracker reports and a
    changelog. Severe cases are what get filed, so all three are upper-tail by selection.
    Nothing here establishes a typical figure, and none should be read as one.

  

  

    

      One orphan
      ~100 GB
      
An MCP server that outlived its parent, on an M4 Max.[7](#r7)

    
    

      One session's leak
      ~50 GB
      
Swap swell alongside kernel panics on a 16 GB machine.[8](#r8)

    
    

      One machine
      127
      
Orphaned processes found by telemetry on a single host.[6](#r6)

    
  

  Interlock 05 · the market that was described

  
## The research described a crowd that was not there

  
## Two backends built a market picture on repositories nobody uses

  
## Adoption claims anchored at n = 0, 0, 9, 11 and 15 stars

  

    
To describe what people really use, the research picked projects that almost nobody
    has starred. Two of them had none at all — not one person had marked them as
    interesting.[9](#r9)[10](#r10)

    
Meanwhile the one tool here that a lot of people genuinely do use, it described at
    the wrong price, the wrong size, and under the wrong
    licence.[12](#r12)[13](#r13)

    
All of that was free to check. It took seconds.

  

  

    
Both paid backends built their picture of the free market on repositories with 0, 0,
    9, 11 and 15 stars. One with *zero* was cited about twenty times by one backend as
    its free-market evidence base, and named by the other as evidence of "actual adoption of
    AI in this space".[10](#r10)
    A nine-star repository was called "the strongest direct
    competitor".[9](#r9)

    
The same panel got Mole wrong three ways: $19, not $9; 63,562 stars, not 59,100 or
    28,500; GPL-3.0, not MIT.[12](#r12)[13](#r13)
    The price was on the vendor's own front page. The backend sourced a Medium post
    instead.[11](#r11)

    
A vendor page, one API call and one URL fetch corrected every load-bearing number.
    The research cost about $29.70. The corrections cost nothing.

  

  

    
Star count is a weak proxy for use. It is the metric here because it is the proxy
    those reports leaned on implicitly, and no backend queried the API that returns
    it.[9](#r9)[10](#r10)

    
`tw93/Mole`: vendor-stated $19 one-time for 2 Macs against a reported
    $9.00;[12](#r12)
    63,562 stars and GPL-3.0 against reported 59,100 / 28,500 and
    MIT.[13](#r13)
    Four of four load-bearing corrections resolved against first-party artifacts at zero
    marginal cost.

    
The reading that survives: the panel's value was in *disagreeing* enough to
    show where to look, not in the figures it returned. Three backends produced three
    incompatible answers on the central question, and that disagreement is the only reason
    anyone went and read the artifact.

    
**Limit.** Prices change. The $9 figure may have been correct at some
    earlier date; it was not correct on the day it was reported.

  

  
    
The tools the research described, against the tool people use

    

      
        GitHub stars of the repositories cited as the free market
        Bar chart with a zero baseline. Six repositories cited in the
        research as evidence of the free market range from zero to fifteen stars. Mole, the
        one widely adopted tool in the category, has 63,562 stars — roughly four thousand
        times the top of this axis, and shown as an annotation rather than a bar because it
        cannot be drawn to the same scale.

        
        
          
          
          0
          5
          10
          15
          GITHUB STARS · ZERO BASELINE · READ 2026-08-15
        

        
        
          
          
          
          
          
          
          
        

        
        
          cc-reaper
          skills-plugin
          devclean
          claude-code-janitor
          mcp-cleanup
          process-guardian
          clean-my-mac
        

        
        
          15
          11
          9
          1
          0
          0
          0
        

        
        
          
          Mole
          63,562
          OFF THIS AXIS BY
          A FACTOR OF ~4,200
        
        
          Mole
          63,562
          FAR TOO BIG TO DRAW HERE
        

        
        
          
          
          CITED ~20× AS THE FREE-MARKET EVIDENCE BASE
        
      
    
    Zero baseline, linear scale, one axis. Mole is annotated rather than drawn
    because a bar four thousand times the length of the others would compress every real
    difference on this chart to nothing — which is itself the finding.
  

  Interlock 06 · the bound

  
## People mind about the folder, not about the program

  
## What bounds this is which directory gets touchedInference

  
## The tolerated envelope tracks reproducibility, not sophisticationInference

  

    
People mind much less about a program deleting something the computer can rebuild by
    itself than about it touching a folder where they keep things. When one cleaning program
    started removing files from the Downloads folder, the complaint was not that it was
    badly built — it was that lots of people keep things
    there.[14](#r14)

    
Most tools in this area have decided the safest thing is to tell you what to do and
    never do it themselves.[17](#r17)
    Whether the safe part is big enough for anyone to make a living from, nobody here can
    tell you. The people who looked at this do not agree, and the one company that tried has
    stopped.

  

  

    
Tolerance tracks the target, not the tool. Caches and build output are forgiven
    because the machine can rebuild them; Downloads and Documents are not. The CCleaner
    moderator's objection was precisely that — not that the feature was broken, but that
    "many people use Downloads as long-term
    storage".[14](#r14)

    
The surrounding sentiment is harder than that. A senior Apple Support contributor
    advises never installing this class of software at
    all.[15](#r15)
    Sensei sells *against* automation in its own marketing
    testimonial.[16](#r16)
    And the prevailing engineering posture is refusal: one plugin documents its process
    skills as "pure diagnostic", stating they "never kill processes on their own" and
    "merely suggest kill commands".[17](#r17)

    
**This is the question the page does not close.** Whether the forgiven
    set is commercially large enough is genuinely unresolved, and the CleanMyMac Business
    withdrawal is consistent with either answer.[1](#r1)

  

  

    
The tolerated envelope is defined by the reproducibility of the target, not by the
    sophistication of the gate in front of it. A perfect verification gate on
    `~/Downloads` is still outside the envelope; a crude one on
    `DerivedData` is inside it.[14](#r14)

    
The stronger version of the objection is not about risk at all. Howard Oakley argues
    macOS already empties the caches in question and asks why a second application should
    need to exist — which, if right, makes part of this category redundant rather than
    dangerous.[18](#r18)

    
**Unresolved, and stated as unresolved.** This corpus cannot settle
    whether the envelope supports a business. The single commercial datapoint terminated
    without a stated cause and is consistent with both the demand-failure and the
    go-to-market readings. Nothing in the research, and nothing found on this machine,
    breaks that tie.

  

  

    

      Artifact · vendor marketing
      cindori.com
    
    

      
“gives me full control unlike other apps that automatically delete system files”

    
    
A testimonial a paid Mac utility chose to put on its own product
    page. The thing being sold against is the thing this page is
    about.[16](#r16)

  

  Interlock 07 · where the capability actually goes

  
## The store version has had its useful parts removed

  
## Apple's rules, not engineering, decide what a cleaner may do

  
## The binding constraint is the distribution channel

  

    
The version of these apps you get from Apple's store has had its most useful parts
    taken out — not because they were dangerous, but because the store's rules do not allow
    them. The company that makes the best-known one publishes the list
    itself.[19](#r19)

  

  

    
The App Store build of the category leader cannot clean system logs or caches, touch
    Xcode simulators, manage launch agents, or monitor for malware in real time. MacPaw
    publishes that list on its own support site and is explicit that the exclusions do not
    mean the features are harmful.[19](#r19)

    
Underneath that, the paid and free tools have converged on the same targets. Pricing
    runs from $9.99 once for five Macs[20](#r20)
    to $65.99 a year,[21](#r21)
    with Sensei at $29/yr or $59 once[22](#r22)
    and Mole at $19 once.[12](#r12)
    The real lever on perpetual buyers is not a feature gate at all: a one-time licence
    excludes major-version upgrades.[23](#r23)

  

  

    
Per MacPaw's own knowledge base, updated 2024-10-16, sandboxing plus review guidelines
    remove system log and cache cleaning, Xcode simulators, language files, iOS device
    backups, launch-agent enable/disable, menu-bar hardware temperatures and real-time
    malware monitoring from the App Store
    build.[19](#r19)
    A tool intending unattended launchd operation is therefore off that channel by
    construction.

    
Price band: $9.99 one-time for 5 Macs (DaisyDisk)[20](#r20)
    to $65.99/yr (CleanMyMac Plus).[21](#r21)
    Conversion mechanism is major-version exclusion on perpetual licences, stated in the
    vendor's own docs.[23](#r23)

    
**Limit, and it is unresolved.** Direct-store pricing could not be read:
    macpaw.com sits behind a challenge that returned HTTP 403 to a fetch and an unresolvable
    JavaScript challenge to a browser engine. Aggregators report $119.95 direct against the
    App Store's $89.99 one-time.[21](#r21)
    That roughly $30 gap between channels is not reconciled here, and multi-Mac direct
    pricing is unverified.

  

  
## Sources

  
Twenty-three sources. Where a
  row says *first-party read*, it was fetched from this machine on 15 August 2026 and
  the environment is recorded in the methods note below.

  

    1. [CleanMyMac Business Has Been Discontinued](https://macpaw.com/support/cleanmymac-business/knowledgebase/smart-scan-automation)
      MacPaw · vendor notice · 29 Jul 2026 · first-party read · establishes the withdrawal effective 14 July 2026, at the URL the research cited as evidence the model works

    1. [cc-reaper](https://github.com/theQuert/cc-reaper)
      theQuert · source repository · read 15 Aug 2026 · establishes the 10-minute LaunchAgent, the ≥80% / ≥60 min sustained runaway test, and PGID-leader scoping

    1. [Hazel](https://www.noodlesoft.com/)
      Noodlesoft · vendor page · establishes roughly two decades of rule-based macOS automation that acts on files unattended

    1. [Dossier run dr_e90bf27c97d1efa0](https://macpaw.com/support/cleanmymac-business/knowledgebase/smart-scan-automation)
      Perplexity sonar-deep-research · commissioned research · 15 Aug 2026 · the claim that CleanMyMac Business proves scheduled unattended cleaning commercially viable

    1. [GitHub repository search — orphan process reapers](https://github.com/search?q=claude+orphan+process+cleanup+mcp&type=repositories)
      GitHub · first-party API read · 15 Aug 2026 · six independent implementations, none above 15 stars

    1. [Empryo changelog](https://empryo.com/changelog)
      Empryo · release notes · 2026 · 127 orphaned processes on one host; the fix proves a process belongs to the agent's own config path before killing

    1. [serena issue #1367](https://github.com/oraios/serena/issues/1367)
      oraios/serena · issue tracker · Apr 2026 · an orphaned MCP server survived its parent and reached roughly 100 GB on an M4 Max

    1. [opencode issue #12687](https://github.com/anomalyco/opencode/issues/12687)
      anomalyco/opencode · issue tracker · Feb 2026 · ~1.25 GB per instance per 35 minutes, kernel panics and ~50 GB swap swell at 16 GB

    1. [ImL1s/devclean](https://github.com/ImL1s/devclean)
      GitHub · first-party API read · 15 Aug 2026 · 9 stars, last push 14 Mar 2026 — called "the strongest direct competitor" by one run

    1. [shihabshahrier/clean-my-mac](https://github.com/shihabshahrier/clean-my-mac)
      GitHub · first-party API read · 15 Aug 2026 · 0 stars, 0 forks — cited roughly twenty times as one run's free-market evidence base

    1. [Dossier run dr_2b955b389a9918f9](https://github.com/tw93/mole)
      Gemini deep-research-max-preview · commissioned research · 15 Aug 2026 · the $9.00 price claim, sourced to a Medium post, and the no-prior-art conclusion

    1. [mole.fit — store line](https://mole.fit)
      Mole (tw93) · vendor page · read 15 Aug 2026 · "$19 one-time license for 2 Macs. No subscription." CLI free and GPL-3.0

    1. [GitHub API — repos/tw93/Mole](https://api.github.com/repos/tw93/Mole)
      GitHub · first-party API read · 15 Aug 2026 · 63,562 stars, 2,237 forks, GPL-3.0

    1. [CCleaner deleted my data please help](https://community.ccleaner.com/t/ccleaner-deleted-my-data-please-help/78301)
      CCleaner Community · user report with moderator reply · 2023–24 · a moderator confirms newer versions selectively remove files from Downloads, irreversibly if overwriting is on

    1. [Oops, Installed and ran Clean My Mac](https://discussions.apple.com/thread/255139763)
      Apple Support Communities · user forum · 20 Sep 2023 · a Level 10 contributor: "Never install any app that claims to 'tune up', 'speed up' or 'clean up' your Mac"

    1. [Sensei — product page](https://cindori.com/sensei)
      Cindori · vendor marketing · read 15 Aug 2026 · a testimonial selling control against automatic deletion, on the vendor's own page

    1. [lifedever/skills-plugin](https://github.com/lifedever/skills-plugin)
      lifedever · source repository · read 15 Aug 2026 · process skills documented as "pure diagnostic"; they "never kill processes on their own"

    1. [Last Week on My Mac: Can we make cleaning up our Macs simpler?](https://eclecticlight.co/2025/01/26/last-week-on-my-mac-can-we-make-cleaning-up-our-macs-simpler/)
      Howard Oakley, The Eclectic Light Company · domain expert · 26 Jan 2025 · macOS controls and empties its own caches; questions why a second app should be needed

    1. [Missing features in the App Store version of CleanMyMac X](https://macpaw.com/support/cleanmymac-x/knowledgebase/missing-features)
      MacPaw · vendor support doc · updated 16 Oct 2024 · first-party read · the vendor's own enumeration of what App Store review removes

    1. [DaisyDisk](https://daisydiskapp.com/)
      DaisyDisk · vendor pricing page · read 15 Aug 2026 · $9.99 one-time, up to 5 personal Macs, explicitly not a subscription

    1. [CleanMyMac on the App Store](https://apps.apple.com/us/app/cleanmymac/id1339170533)
      Apple / MacPaw Way Ltd · store listing · read 15 Aug 2026 · yearly $34.99–$39.99, Plus $65.99/yr, CleanMyMac X one-time $89.99

    1. [Buy Sensei](https://cindori.com/store/sensei)
      Cindori · vendor pricing page · read 15 Aug 2026 · $29 billed annually or $59 one-time, each up to 3 Macs

    1. [CleanMyMac purchase options](https://macpaw.com/support/cleanmymac/knowledgebase/purchase-options)
      MacPaw · vendor support doc · read 15 Aug 2026 · "a one-time purchase includes only updates and fixes for your current major version"

  

  

    
## How this page was made, and what it could not establish

    

      
A research panel ran, and then every
      number it produced that mattered was checked against the thing itself. The checks
      changed the answer, so the method is part of the finding rather than a footnote to it.

    
    
      Panel
      **Gemini** deep-research-max-preview ($7.00, 91 sources) and
      **Perplexity** sonar-deep-research ($4.00, 19 sources), commissioned for
      this question. Four earlier runs on the adjacent question: xAI Grok-4.5 ($2.50), and
      three more at $3.00, $2.00 and $1.20. **About $29.70 in total.**

      Free lane
      Requested and **not delivered by the panel**. The research tool
      reported every local CLI "not on PATH" although `claude`, `codex`
      and `cursor-agent` are all present, so it seated three paid backends and
      zero free. The free half was run by hand instead — and it is the half that caught
      every error on this page.

      Read
      All six reports exported and read end to end, not the merged distillation. Where
      backends disagreed, the disagreement is carried onto the page rather than resolved.

      Verified
      Four load-bearing claims were settled against artifacts, not reports: one vendor
      store line, one GitHub API call, one URL dereference, one repository README. All four
      contradicted at least one backend. Environment: macOS 15 (Darwin 25.6.0), Apple
      silicon, 15 August 2026; `gh` CLI against the GitHub REST API; Obscura
      2026-08 for pages behind a fetch block.

      Corrected
      Mole's price ($9 → **$19**), its stars (59,100 and 28,500 →
      **63,562**), its licence (MIT → **GPL-3.0**), and the status
      of CleanMyMac Business (cited as live → **discontinued 14 July 2026**).

      Could not establish
      MacPaw's **direct-store pricing** — the page returned HTTP 403 to a
      fetch and an unresolvable JavaScript challenge to a browser engine, leaving a roughly
      $30 gap between the aggregator-reported $119.95 and the App Store's $89.99 unreconciled.
      **Why CleanMyMac Business was withdrawn** — no reason was published beyond
      product focus. **Whether the tolerable envelope supports a business** — the
      page's open question, which this corpus does not settle in either direction.
      **Revenue or install figures** for any private vendor here.

      Not measured
      Adoption. Star counts appear on this page because they are the proxy the research
      leaned on implicitly; they are a weak measure of use and are not presented as anything
      more. No download, install or active-user figure on this page is independently audited.

      Motion
      Reduced-motion first, and the static page is the safe state. An earlier build
      faded sections in from `opacity: 0` under an IntersectionObserver; measured
      on the review engine the observer existed, never fired, and **every section
      rendered blank**. A reveal that hides content until script runs fails open, so
      it was replaced with a transform-only CSS scroll timeline — the worst case if it
      strands or never runs is a 16px offset, never hidden text.
      **No scrubbed or pinned GSAP episode ships here**: the argument is a
      sequence of discrete corrections, and scrubbing between them would dramatise a
      transition that carries no evidence. Recorded rather than dropped silently.

      Typography
      System stack only. The publisher chrome nominates three webfonts and they are
      deliberately **not loaded**, so it falls back to system faces — the page
      makes zero font requests and stays self-contained.

      Accountable
      Written by Luke Rhodes with Claude Opus 5. The research was machine-generated and
      the corrections were made by hand against primary sources. Errors are mine.
    
  

  

    

      [![](data:image/svg+xml;base64,<stripped>)](https://github.com/fledgeling-co/dossier-research-mcp)
      [![](data:image/svg+xml;base64,<stripped>)](https://margin.fledgeling.app/)
    
    

      
## The research was wrong four times. Checking cost nothing.

      
This page was built with Dossier, which runs a panel of research backends and then makes you read all of it. The panel earned its money by disagreeing — three backends, three incompatible answers, which is the only reason anyone went and looked at the artifact. Margin is where the arguing gets written down.

    
    
      PanelGemini deep-research-max and Perplexity sonar-deep-research, plus four earlier runs
      Spendabout $29.70 across six runs; the corrections cost nothing
      Readall six reports end to end, not the merged distillation
      Correctedprice, star count, licence and one discontinued product
      Unresolvedwhether the tolerable envelope is commercially large enough
