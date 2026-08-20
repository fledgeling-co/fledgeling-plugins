# dispatch

> Source: `~/Dev/dossier/dispatch/index.html`. Published research page, captured 20 August 2026 for the `code-review` and `atlas-publish` skills. Live at https://dossier.fledgeling.app/dispatch where published.

      
      [![](data:image/svg+xml;base64,<stripped>)
        **Margin**](https://margin.fledgeling.app/)
    
    

      
Not infrastructure advice
        A five-backend research panel, read in full, plus two checks run against the affected account itself.

    
  

  
  

    

       Field report
      10 August 2026
      CI · Apple Silicon · AWS
    
    
# The runner was never the thing that failed.

    
A production pipeline stopped dead on a billing block. The obvious fix — move the work onto your own machine — would not have restarted a single job, because what the block took out was *dispatch*, not compute. Five independent research backends reached that conclusion separately. Then two checks against the affected account settled what the panel could not.

    

      

        
The panel
        
5 of 5
        
agree a self-hosted GitHub Actions runner does not deliver independence. It is a worker, not a scheduler.
      
      

        
Cost of the obvious answer
        
$1,423/mo
        
for a cloud Mac that the evidence says you should not rent — against about $4/month for the Linux compute that does the same work.
      
      

        
Unresolved
        
1 claim
        
carried forward as contested rather than settled, because two backends asserted it with confidence their sources did not support.
      
    
  

  
  

    
**01**  ·  What actually failed
    
## A self-hosted runner is a grid-following inverter.

    
The distinction comes from power engineering, and it is exact. A **grid-following** inverter generates real power locally, but it cannot start or stay synchronised without an external reference signal from the grid. Cut the reference and it trips — with its fuel tank full.

    
That is a self-hosted CI runner. It owns the CPU, the disk, the OS image and the toolchain. It does not own workflow parsing, job scheduling, queueing, runner registration, token minting, or log ingestion.[[1]](#r1) GitHub finds a matching runner, assigns the job, and sends it. Your machine waits to be told.

    

      
        
        Grid-following · today
        
        github event
        
        
        
        
        
        breaker open
        billing
        
        
        actions dispatch
        
        
        your runner
        idle · fuel tank full

        
        

        
        Grid-forming · the recommendation
        
        
        github webhook
        
        your control plane
        queue · scheduler
        
        
        nx affected
        the same script, local
        
        
        commit status api
        verified reachable
        
      
      
Solid line and filled node = energised. Dashed grey = de-energised. The difference is fill, never hue, so the drawing holds in greyscale and under any colour-vision deficiency.
    

    
The corroboration is three days older than this page. During the incident of **6–7 August 2026**, GitHub's own status updates said the fault affected *"Both GitHub-hosted and self-hosted runners,"* that it had *"deployed a fix for self-hosted runners that were not picking up jobs,"* and that webhooks were throttled so many pushes never created a run at all.[[2]](#r2) Runners sat online and idle while the scheduler could not reach them.

  

  
  

    
**02**  ·  The fact that settles this case
    
## Three jobs are on larger runners. Larger runners are always blocked.

    
One panel member did what the others could not: it read the actual workflow files. Three jobs request GitHub's paid larger-runner tiers — and GitHub's billing documentation is unambiguous that **"Usage of larger runners is always blocked until you set up a payment method."**[[3]](#r3)

    

$ grep -rn "runs-on:" .github/workflows/*.yml | grep -iE "cores|large"
.github/workflows/ci.yml:92:    runs-on: ubuntu-latest-4-cores
.github/workflows/ci.yml:246:   runs-on: ubuntu-latest-4-cores
.github/workflows/fly-deploy.yml:54: runs-on: ubuntu-latest-8-cores
    

    
The third line is the whole production deploy. So the deploy gate is hard-blocked by billing on its own, independently of every other question in this report.

    

      Inference — from the two facts above
      Even under the reading of the evidence most favourable to self-hosted runners, converting to them would require re-labelling those three jobs *and* would still leave the pipeline waiting on a control plane that is currently refusing to dispatch. There is no configuration of self-hosted GitHub Actions runners that answers the independence requirement here.
    
  

  
  

    
**03**  ·  What the panel could not settle
    
## Two backends were confident about something their sources did not support.

    
Whether an account-level billing lock *also* stops jobs on self-hosted runners is genuinely unresolved. It is worth dwelling on how the panel handled it, because the disagreement is more informative than a consensus would have been.

    

      

        
#### Position A — self-hosted keeps working

        
A June 2026 community thread from an organisation with a valid card and roughly $1,060 of metered usage records hosted `ubuntu-latest` jobs staying blocked while **"self-hosted org runners work as temporary workaround."** A GitHub staff member replied that they would check whether something had changed. No fix was confirmed.[[4]](#r4)

      
      

        
#### Position B — the lock stops everything

        
Other threads describe a blanket state in which no workflow in any repository runs, including manual dispatch. But the most-cited of those threads **contains no mention of self-hosted runners at all**, so it does not actually evidence the claim it is used to support.[[5]](#r5)

      
    

    
Two backends rated this **High Confidence** in favour of Position B. Their support was a community discussion, not GitHub documentation. A third explicitly tagged it *insufficient evidence* — no official statement was found either way. A fourth separated two distinct failure states that GitHub has never documented as distinct: a **quota or budget block**, which the docs say self-hosted usage does not consume, and an **account payment-authorisation lock**, whose scope is undocumented.

    

      
Why this page does not resolve it
      
Three backends agreeing is not corroboration when two of them lean on the same weak source. Support is counted in independent sources, never in how many models said the same thing. The architecture recommended below is deliberately built so that the answer does not matter — which is a better outcome than picking a side and being wrong in a way nobody could later trace.

    
  

  
  

    
**04**  ·  A check the panel could not run
    
## The gate surface is reachable while the scheduler is not.

    
Research can characterise GitHub's documented behaviour. It cannot tell you what your own blocked account will accept right now. So the two surfaces were tested directly: the Actions control plane, and the Commit Status API that any independent CI would use to write a merge gate back onto a pull request.

    

# against the live, billing-blocked account
$ gh api -X POST repos/:owner/:repo/statuses/895891705 \
    -f state=success -f context="local-ci/probe"
posted: local-ci/probe  state=success

$ gh api repos/:owner/:repo/commits/895891705/status
success | contexts: Vercel – diolog-ai-mobile, Vercel – diolog-ai, local-ci/probe

# meanwhile, every Actions job:
The job was not started because recent account payments have failed
or your spending limit needs to be increased.
    

    
The status check landed and now renders on the commit beside the two Vercel checks. **The two surfaces are separately gated.** That is the empirical foundation the recommendation rests on: an independent CI system can gate merges on this account today, while Actions cannot run a single job.

  

  
  

    
**05**  ·  The hardware question
    
## Do not rent a Mac. The 24-hour minimum decides it.

    
EC2 Mac instances run only on Dedicated Hosts, and AWS enforces a **minimum allocation and billing duration of 24 hours** before a host can be released.[[6]](#r6) A ten-minute iOS build therefore costs a day. Stopping an Apple-Silicon Mac additionally triggers hardware scrubbing that can take up to **4.5 hours**.[[7]](#r7) Per-pull-request ephemeral Macs are not merely expensive; they are architecturally impossible.

    

    

      Sydney (ap-southeast-2) · extracted from the AWS public price list, 9 August 2026[[8]](#r8)
      | Host | Per hour | 24-hour minimum | 730-hour month |

      
        | mac2-m2.metal | $1.097 | $26.33 | $800.81 |

        | mac-m4.metal | $1.538 | $36.91 | $1,122.74 |

        | mac2-m2pro.metal | $1.950 | $46.80 | $1,423.50 |

        | CodeBuild arm1.small | $0.0045/min | — | $4.05 |

      
    

    

    

      

mac2-m2pro.metal

$1,423.50
      

mac-m4.metal

$1,122.74
      

mac2-m2.metal

$800.81
      

CodeBuild arm1.small

$4.05
    
    
One axis, zero baseline, direct-labelled. The CodeBuild bar is 0.28% of the width of the top bar — that near-invisibility is the finding, not a rendering fault. Mac figures are a full month of allocation; CodeBuild is 1,000 build minutes less the 100 free.

    
The requirement that appeared to force Apple hardware — two Expo iOS apps — does not survive contact either. EAS Build's free tier includes **15 iOS builds per month**, with paid builds at $2 to $4.[[9]](#r9) And `eas submit` uploads through the App Store Connect API, so it runs on Linux; Apple's macOS-only Transporter is not in the path.[[10]](#r10)

  

  
  

    
**06**  ·  macOS as a container host
    
## Apple's container could not complete the build test.

    
Every Linux container on Darwin runs inside a VM; the only question is which. The best available benchmark ran all runtimes on one MacBook M3 in a single session, four runs of three iterations, with volume data wiped between runs and the script published.[[11]](#r11)

    

    

      macOS Tahoe 26.4.1 · benchmarked 20 April 2026 · lower is better except throughput
      | Test | Colima | Docker Desktop | OrbStack | Apple container |

      
        | Container startup | 0.291 s | 0.329 s | 0.371 s | 0.935 s |

        | Volume read, 256 MB | 3,354 MB/s | 2,970 MB/s | 10,061 MB/s | 2,765 MB/s |

        | 1,000 × 4 KB writes | 0.761 s | 0.711 s | 0.620 s | 1.257 s |

        | Container ↔ container | 110.3 Gbps | 119.1 Gbps | 130.2 Gbps | 23.0 Gbps |

        | Image build | 6.81 s | 4.98 s | 5.28 s | failed |

      
    

    

    
Two results matter more than the rankings. Apple's builder **could not run the build test at all** — it has no outbound network, so fetching a package inside the build fails. And the operating-system upgrade moved throughput more than the choice of runtime did: volume writes roughly doubled across every engine, attributed to kernel and Virtualization-framework changes.

    

      
A number to distrust — and how it got here
      
One backend reported OrbStack completing `pnpm install` in "12.2 s versus 10.9 s native, 75–95% of native I/O." Another states plainly that **no published benchmark measures a real `pnpm install` on a bind mount**. The figure traces to a low-quality secondary source. It is reproduced here only as a warning: it is the most quotable number in the whole corpus, and it is unsupported.

    
  

  
  

    
**07**  ·  Struck off
    
## Five options that look live and are not.

    

    

      | Option | State | Evidence |

      
        | **Earthly** | Dead | Cloud shut down 16 July 2025; open source frozen to critical fixes; last release v0.8.16. It arranged a migration path *to Dagger*.[[12]](#r12) |

        | **AWS CodeCatalyst** | Dead | Closed to new customers 7 November 2025; no new features planned beyond security and availability work.[[13]](#r13) |

        | **Drone** | Legacy | Now a branch of harness/harness; active development moved elsewhere. |

        | **Depot · Blacksmith · Namespace**
in GitHub-runner mode | Fails the requirement | Excellent on speed and cost, but consumed via `runs-on:` and still dispatched by GitHub Actions. Zero independence. |

        | **@nx/s3-cache and siblings** | Deprecated | Withdrawn 21 May 2026 over CVE-2025-36852. Nx states the flaw "is in their design and cannot be patched," and warns that a hand-rolled replacement reproduces it.[[14]](#r14) |

      
    

    
    
One more correction, in the other direction: **CodeQL was never running in this pipeline.** There is no CodeQL job in any workflow file; the scans come from GitHub's repository-level default setup, and the only security gate inside CI is a single `pnpm audit --audit-level high`. "CodeQL-equivalent scanning" is therefore a new capability to add, not a capability to preserve — which materially shrinks the migration. It would not have been portable anyway: the CodeQL licence prohibits CI use on private, non-open-source code without a paid GitHub Advanced Security licence.[[15]](#r15)

  

  
  

    
**08**  ·  What to build
    
## Own the control plane. Keep GitHub as the forge.

    
Four of five backends converged on this shape from different starting points. The fifth argued for replacing the git forge entirely with a self-hosted Forgejo — which fails the stated requirement, since Forgejo reports checks to Forgejo and needs a bridge to reach a GitHub pull request.

    

    

      | Layer | Choice | Why this one | Cost |

      
        | Control plane | **Buildkite** free tier, or **Woodpecker** self-hosted | Buildkite is lowest-effort and its Personal tier has no bill to fail. Woodpecker is the fully-owned answer if that rhyme is unacceptable. | $0 |

        | Execution | **AWS CodeBuild**, arm64 Graviton | Provisioned by the Pulumi stack that already runs in this account. No server to patch. | ~$4/mo |

        | Pipeline definition | ci/run-gates.sh → nx affected | The CI server calls a script the repository owns. Local and CI stop being two things, so reproduction is structural rather than aspirational. | — |

        | Merge gate | **Commit Status API** | Verified working on the blocked account. §04. | $0 |

        | iOS | **EAS Build** | 15 free builds a month; eas submit runs on Linux. | $0–19/mo |

        | Scanning | Semgrep · OSV-Scanner · Trivy | CodeQL is neither present today nor licensable off GitHub for private code. | $0 |

      
    

    

    
### The part that is actually dangerous

    
Moving CI onto machines you own shifts secret custody from ephemeral, managed injection onto something long-lived that also executes pull-request code and runs `pnpm` lifecycle scripts. One credential deserves naming: a Fly deploy token is org-scoped by default and Fly tokens are valid for **twenty years** unless told otherwise.[[16]](#r16)

    
So: split untrusted pull-request gates from the protected deploy pipeline; give deploy credentials only to the protected path; fetch from SSM at runtime with short-lived roles; and keep the CI host off the production database firewall allowlist entirely, so that a total compromise of the build machine still cannot route a packet to customer data.

    

      
Do this first
      
Pay the bill. It restores everything today, costs nothing to attempt, and the migration above is a two-to-four week project that should be done deliberately rather than during an outage. The research tells you what to build once you are no longer firefighting — it does not argue for building it tonight.

    
  

  
  

    
**09**  ·  Sources
    
## Registry

    
Every claim above that carries a number or an attribution is keyed to a row here. Sources are as reported by the panel; they were **not** independently dereferenced — see the methods note.

    

      1. [1]
**GitHub Docs — About self-hosted runners**
GitHub finds a matching runner, assigns the job, and sends it; the runner must communicate with the Actions service.[https://docs.github.com/en/actions/reference/runners/self-hosted-runners](https://docs.github.com/en/actions/reference/runners/self-hosted-runners)

      1. [2]
**GitHub Community Discussion #204152**
Incident of 6–7 Aug 2026. “Both GitHub-hosted and self-hosted runners” affected; a fix deployed for self-hosted runners not picking up jobs; webhooks throttled.[https://github.com/orgs/community/discussions/204152](https://github.com/orgs/community/discussions/204152)

      1. [3]
**GitHub Docs — About billing for GitHub Actions**
“Usage of larger runners is always blocked until you set up a payment method.”[https://docs.github.com/en/billing/managing-billing-for-your-products/about-billing-for-github-actions](https://docs.github.com/en/billing/managing-billing-for-your-products/about-billing-for-github-actions)

      1. [4]
**GitHub Community Discussion #199036**
June 2026. Hosted jobs blocked while “self-hosted org runners work as temporary workaround”. GitHub staff response; no fix confirmed.[https://github.com/orgs/community/discussions/199036](https://github.com/orgs/community/discussions/199036)

      1. [5]
**GitHub Community Discussion #167403**
Account-level payment-authorisation lock. Notably contains no mention of self-hosted runners.[https://github.com/orgs/community/discussions/167403](https://github.com/orgs/community/discussions/167403)

      1. [6]
**AWS — EC2 Dedicated Hosts pricing**
“On-Demand EC2 Mac Dedicated Hosts have a minimum host allocation and billing duration of 24 hours.”[https://aws.amazon.com/ec2/dedicated-hosts/pricing/](https://aws.amazon.com/ec2/dedicated-hosts/pricing/)

      1. [7]
**AWS Docs — Stop and start your Mac instance**
Apple-silicon scrubbing workflow after stopping an EC2 Mac instance.[https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/mac-instance-stop.html](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/mac-instance-stop.html)

      1. [8]
**AWS Price List API — ap-southeast-2**
Sydney on-demand rates extracted 9 Aug 2026 for mac2-m2, mac-m4, mac2-m2pro and CodeBuild compute.[https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/ap-southeast-2/index.json](https://pricing.us-east-1.amazonaws.com/offers/v1.0/aws/AmazonEC2/current/ap-southeast-2/index.json)

      1. [9]
**Expo — Pricing**
Free plan includes 15 iOS and 15 Android builds per month; paid iOS builds listed at $2 medium and $4 large.[https://expo.dev/pricing](https://expo.dev/pricing)

      1. [10]
**Expo Docs — eas submit**
Submission uses the App Store Connect API and is cross-platform; macOS-only Transporter is not required.[https://docs.expo.dev/submit/introduction/](https://docs.expo.dev/submit/introduction/)

      1. [11]
**zot24/macos-container-benchmarks**
MacBook M3/16 GB, four runs × three iterations, one session, volume data wiped between runs, script published. macOS Tahoe 26.4.1, 20 Apr 2026.[https://github.com/zot24/macos-container-benchmarks](https://github.com/zot24/macos-container-benchmarks)

      1. [12]
**Earthly — A message about Earthly**
Earthly Cloud stopped working 16 July 2025; no active contribution to the open-source project beyond critical bug fixes.[https://earthly.dev/blog/shutting-down-earthfiles-cloud/](https://earthly.dev/blog/shutting-down-earthfiles-cloud/)

      1. [13]
**AWS — CodeCatalyst**
Closed to new customers 7 November 2025; no new features planned beyond security, availability and performance.[https://aws.amazon.com/codecatalyst/](https://aws.amazon.com/codecatalyst/)

      1. [14]
**Nx — Deprecated self-hosted cache packages**
@nx/s3-cache and siblings deprecated 21 May 2026 over CVE-2025-36852; “the flaw is in their design and cannot be patched”.[https://nx.dev/docs/reference/deprecated/self-hosted-cache-packages](https://nx.dev/docs/reference/deprecated/self-hosted-cache-packages)

      1. [15]
**CodeQL CLI — LICENSE.md**
Prohibits generating a CodeQL database for automated analysis, CI or CD outside open-source code on GitHub.com without a paid licence.[https://github.com/github/codeql-cli-binaries/blob/main/LICENSE.md](https://github.com/github/codeql-cli-binaries/blob/main/LICENSE.md)

      1. [16]
**Fly.io Docs — Access tokens**
Fly tokens are “valid for 20 years (175200h0m0s) by default”.[https://fly.io/docs/security/tokens/](https://fly.io/docs/security/tokens/)

    

  

  

    
## How this was made

    
The failure this method exists to prevent is reporting a merged summary of several research reports as though it were their agreement. A merged distillation is a coverage difference between reports, not a synthesis of them.

    
      Panel
      Five backends on one brief, each run separately: Perplexity Sonar Deep Research, OpenAI gpt-5.6, Google Gemini Deep Research, and two local CLI members (Claude Code, Codex). 295 cited sources between them.

      Read
      Gemini end to end. OpenAI, Codex and Claude: executive summaries plus full detailed findings. Perplexity: findings through §8 of 10. No section of this page is written from the merged distillation.

      Verified locally
      Two claims re-checked rather than repeated — the three larger-runner job definitions, and the absence of any CodeQL job. Both held. One further check was *run* rather than researched: a live write to the Commit Status API on the blocked account.

      Not checked
      Citations were not dereferenced. The AWS price-list figures come from one backend's extraction and were corroborated by a second, but not re-pulled here. No benchmark was re-run.

      Disagreement
      One material conflict is carried forward unresolved in §03 rather than settled. Two backends rated it High Confidence on support that does not bear the weight.

      Cost
      Panel reserved at $20 worst case; actual spend approximately $1.70, plus local CLI subscription quota that the tooling cannot meter.

      Accountable
      Written by Luke Rhodes. The research was automated; the reading, the local verification, the decision to leave one claim unresolved, and every judgement on this page are not.
    
  

  
Dossier field report · 10 August 2026 · dispatch.fledgeling.app

  

    

      [![](data:image/svg+xml;base64,<stripped>)](https://github.com/fledgeling-co/dossier-research-mcp)
      [![](data:image/svg+xml;base64,<stripped>)](https://margin.fledgeling.app/)
    
    

      
## Margin is where the reasoning is kept.

      
Dossier runs a panel of independent research backends over one question, reads every report end to end, and compiles the claims into a ledger before a single word of the page is written. Margin is the working surface behind it: the briefs, the disagreements between backends, the claims that did not survive a check. This page is the part that held.

    
    
      Panel5 backends · 2 free-lane CLIs, 3 paid · 295 cited sources
      WindowAugust 2025 – August 2026, current pricing and product status
      Verified locally2 claims re-checked against the repository and the live GitHub API
      Unresolved1 material disagreement, carried forward rather than settled
