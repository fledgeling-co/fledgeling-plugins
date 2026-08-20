# egress

> Source: `https://dossier.fledgeling.app/egress`. Published research page, captured 20 August 2026 for the `atlas-publish` skill.

[![](data:image/svg+xml;base64,<stripped>)
        **Dossier**](https://github.com/fledgeling-co/dossier-research-mcp)
      
      [![](data:image/svg+xml;base64,<stripped>)
        **Margin**](https://margin.fledgeling.app/)
    
    

      
INFRASTRUCTURE AUDIT
        Compiled with Dossier and Margin from 112 independent panel sources.

    
  

  
  

    

      [EGRESS // CI AUDIT](#)

      
      
        Select Reading Register
        
          
          Primer
        
        
          
          Brief
        
        
          
          Technical
        
      

      
      
        ☼
        Theme
      
    
  

  

    
    

      

        ● RESEARCH DOSSIER · INFRASTRUCTURE & SECURITY
      
      
# Self-Hosted CI/CD: The Security Architecture & TCO Split

      
Local GitHub Actions runners save substantial capital on macOS mobile builds while carrying a steep break-even threshold on Linux. But without hardware-isolated microVMs and dedicated CI VLANs, private workflows become unmonitored backdoors for software supply chain intrusion.

      
      

        

          
958 – 2.1k
          
macOS Break-Even (Min/Mo)
          
Against GitHub's $0.062/min rate; pays for an M4 Mac mini in weeks.
        
        

          
5.9k – 18.4k
          
Linux Break-Even (Min/Mo)
          
Cloud Linux is $0.006/min; labor overhead dominates the ROI.
        
        

          
2 VMs Max
          
Apple EULA Ceiling
          
macOS SLA §2.B.iii caps concurrent guests per host, stopping vertical scaling.
        
        

          
< 125 ms
          
MicroVM Reset Floor
          
Firecracker/Tart per-job ephemeral boundary prevents supply chain persistence.
        
      
    

    
    

      
## 1. The Financial Break-Even Is Bifurcated by OS

      
The decision to self-host is fundamentally an economic question dictated by operating system pricing tiers and platform engineering labor. In January 2026, GitHub revised its hosted runner rates, reducing 2-core Linux to $0.006/min and standard macOS to $0.062/min while indefinitely postponing a proposed $0.002/min self-hosted orchestration tax [5](#r5).

      
    

      

        C1
        Inference
        HIGH CONFIDENCE
      
      

        
Building iPhone apps on a local Mac mini pays for itself in just a few weeks of heavy use because Apple cloud servers are expensive. But building regular Linux web apps on your own PC takes thousands of hours to save money because cloud Linux is already pennies per hour. [5](#r5)[12](#r12)[18](#r18)[19](#r19)

      
      

        
The financial case for self-hosting is heavily bifurcated by operating system. Local macOS runners break even at just ~1,000–2,200 monthly build minutes against GitHub's $0.062/min hosted rate, whereas local Linux runners require ~6,000–18,500 minutes to offset hardware, power, and routine maintenance against GitHub's $0.006/min rate. [5](#r5)[12](#r12)[18](#r18)[19](#r19)

      
      

        
Modeled on 36-month straight-line depreciation plus $0.173/kWh power and $75/mo platform engineering overhead: Local Mac mini ($1,799 CapEx, 35W) direct TCO is $59.39/mo ($134.39 burdened), yielding break-even at 958 direct / 2,168 burdened minutes at $0.062/min. Local Linux ($900 CapEx, 45W) direct TCO is $35.68/mo ($110.68 burdened), requiring 5,947 direct / 18,447 burdened minutes at $0.006/min. [5](#r5)[12](#r12)[18](#r18)[19](#r19)

        

          
**Verification:** Calculated from GitHub 2026 published baseline rates (Linux $0.006/min, macOS $0.062/min), hardware CapEx ($900 Linux PC, $1799 Mac mini M4 Pro setup), power consumption (45W Linux, 35W Mac at $0.173/kWh), and $75/mo labor allocation.
          
**Stated Limits:** Assumes consistent local runner utilization and does not account for burst queueing latency during parallel team PR rushes.
        
      
    
    

      
      

        

          
            | Platform / Workload | Hardware CapEx | Monthly Power (24/7) | Direct Monthly TCO | Burdened TCO (+1hr Labor) | Break-Even Minutes/Mo |

          
          
            | **Apple Silicon Mac mini M4 Pro** (iOS / Xcode) | $1,799 (36mo amortized) | 35W (~$4.42/mo) | **$59.39 / mo** | $134.39 / mo | 958 direct · 2,168 burdened |

            | **Linux x86 Mini PC** (Docker / Backend) | $900 (36mo amortized) | 45W (~$5.68/mo) | **$35.68 / mo** | $110.68 / mo | 5,947 direct · 18,447 burdened |

            | **Windows Server 2025 Host** (.NET / MSVC) | $1,400 (36mo amortized) | 70W (~$8.84/mo) | **$52.73 / mo** | $127.73 / mo | 5,273 direct · 12,773 burdened |

          
        

      

      

        **The Labor Threshold:** Direct hardware costs are negligible compared to platform engineering time. Allocating just one hour per month ($75) of maintenance labor triples the break-even threshold for Linux runners from ~6,000 to ~18,500 minutes [18](#r18)[19](#r19). For teams under 20,000 monthly Linux minutes, GitHub-hosted compute is financially optimal.
      
    

    
    

      
## 2. Private Repositories Do Not Eliminate Supply Chain Attacks

      
A widespread assumption in self-hosted CI deployments is that restricting runners to private repositories makes bare-metal execution safe. The evidence contradicts this: modern CI pipelines execute unvetted third-party scripts at build time [1](#r1)[3](#r3)[17](#r17)[20](#r20).

      
    

      

        C2
        Direct Evidence
        HIGH CONFIDENCE
      
      

        
Just because your code repository is private does not make it safe. When a build downloads code libraries from the internet, hidden setup scripts can run secretly on your computer, steal your passwords, and look around your home or office network. [1](#r1)[3](#r3)[17](#r17)[20](#r20)

      
      

        
Private repositories do not eliminate CI threat models. Routine package installation hooks (e.g. npm postinstall) and compromised developer credentials execute arbitrary shell commands within the runner's context, turning unisolated local machines into footholds for token theft and network reconnaissance. [1](#r1)[3](#r3)[17](#r17)[20](#r20)

      
      

        
npm and package manager lifecycle hooks (preinstall, postinstall, prepare) execute unconstrained shell commands during dependency resolution. GitHub warns that any identity with workflow dispatch or push privileges can execute arbitrary code on self-hosted runners, harvest environment variables, and weaponize the job identity before application-layer log scrubbing occurs. [1](#r1)[3](#r3)[17](#r17)[20](#r20)

        

          
**Verification:** GitHub Docs explicitly states private repo contributors who invoke workflows can compromise runners. npm docs verify lifecycle scripts run automatically. Praetorian red team demonstrated full-chain compromise via private workflows.
          
**Stated Limits:** Applies whenever workflows install unpinned dependencies, run third-party actions, or allow branch workflows without mandatory review.
        
      
    
    
      
    

      

        C10
        Direct Evidence
        HIGH CONFIDENCE
      
      

        
Real hackers have already found tricks to bypass GitHub's cleanup tools by setting special hidden settings, leaving background spy programs running on local computers even after the build finishes. [4](#r4)

      
      

        
Malware like Shai-Hulud has actively bypassed GitHub Actions process cleanup on persistent runners by setting RUNNER_TRACKING_ID=0 and RUNNER_ALLOW_RUNASROOT=1, establishing persistent backdoors that blend C2 traffic into GitHub Discussions. [4](#r4)

      
      

        
The Shai-Hulud attack vector demonstrates that GitHub's post-job process tree kill mechanism relies on tracking process group IDs via environment variables. Attackers decoupling background daemons with RUNNER_TRACKING_ID=0 and nohup survive job teardown on persistent runners, establishing reverse shells that communicate over GitHub Discussions API endpoints. [4](#r4)

        

          
**Verification:** Sysdig Threat Research documented the Shai-Hulud malware attack chain: setting RUNNER_TRACKING_ID=0 tricks the runner daemon into skipping orphaned background process termination, enabling long-lived C2 persistence.
          
**Stated Limits:** Only effective on persistent, non-ephemeral runner hosts; disposable microVMs destroy the background processes upon guest termination.
        
      
    
    

      

        **Active Threat Campaign:** Threat actors in campaigns such as *Shai-Hulud* explicitly weaponized the environment variables `RUNNER_TRACKING_ID=0` and `RUNNER_ALLOW_RUNASROOT=1`. This decoupled malicious processes from GitHub's process cleanup tree, establishing persistent backdoors that survived across distinct workflow runs on bare-metal runners [4](#r4).
      
    

    
    

      
## 3. The Isolation Hierarchy: Containers Are Not Security Boundaries

      
Continuous integration workloads execute arbitrary shell commands. Mounting the host Docker daemon or relying on shared-kernel containers creates an immediate path to host takeover [8](#r8)[15](#r15)[16](#r16).

      
    

      

        C3
        Direct Evidence
        HIGH CONFIDENCE
      
      

        
Putting your build inside standard Docker does not protect your main computer. If the build has access to Docker's control socket, it can easily break out and take full control of the entire physical machine as the administrator. [8](#r8)[15](#r15)[16](#r16)

      
      

        
Standard Docker is not an isolation boundary for untrusted CI code. Mounting /var/run/docker.sock allows build scripts to command the host Docker daemon, mount the root filesystem, and achieve root-level compromise of the host machine. [8](#r8)[15](#r15)[16](#r16)

      
      

        
Control of the Docker socket (/var/run/docker.sock) grants root-equivalent administrative authority on the host daemon. Containers share the host kernel; mounting the daemon enables workflows to launch privileged containers with host volume mounts (e.g., -v /:/host) and host namespaces, completely bypassing container boundaries. [8](#r8)[15](#r15)[16](#r16)

        

          
**Verification:** Docker Engine documentation explicitly states daemon control confers root-level capability to mount / and modify host files. Microsoft container security guidance confirms shared-kernel containers fail as hostile multi-tenant boundaries.
          
**Stated Limits:** Rootless Podman provides user namespace defense-in-depth, but still shares the underlying host Linux kernel.
        
      
    
    
      
    

      

        C4
        Direct Evidence
        HIGH CONFIDENCE
      
      

        
To keep your computer completely safe, every single build job must run inside its own tiny virtual computer that starts in a split second and is instantly destroyed and erased when the job finishes. [7](#r7)[9](#r9)[10](#r10)[16](#r16)

      
      

        
Hardware-virtualized microVMs (Firecracker on Linux, Tart on macOS) provide dedicated kernels and memory isolation. Combined with per-job destruction, they eliminate cross-job persistence and container breakout risks. [7](#r7)[9](#r9)[10](#r10)[16](#r16)

      
      

        
MicroVMs leverage hardware virtualization extensions (KVM, Apple Virtualization.framework, Hyper-V) to run jobs in independent guest kernels. Firecracker delivers sub-125ms boot times and <5MiB memory overhead, while Tart provides ephemeral APFS snapshot clones on Apple Silicon, ensuring memory and filesystem state are discarded upon job completion. [7](#r7)[9](#r9)[10](#r10)[16](#r16)

        

          
**Verification:** Firecracker documentation proves KVM hardware isolation with <125 ms boot and <5 MiB RAM overhead. Tart uses Apple Virtualization.framework for disposable macOS/Linux VMs. Microsoft distinguishes Hyper-V isolation as a hardware security boundary.
          
**Stated Limits:** Requires virtualization-capable hardware (KVM / Apple Silicon / Hyper-V extensions) and orchestration tooling like ARC or Tart/Tartelet.
        
      
    
    
      
    

      

        C8
        Direct Evidence
        HIGH CONFIDENCE
      
      

        
Telling GitHub to make a runner 'one-time use' only unplugs it from GitHub after the job. It does not automatically wipe clean the computer's hard drive unless you set up special software to delete the virtual machine. [1](#r1)[2](#r2)[13](#r13)

      
      

        
GitHub's --ephemeral flag deregisters the runner from GitHub's control plane after one job, but does not wipe the underlying filesystem. True ephemerality requires orchestration (ARC or VM snapshot rollback) to guarantee clean state. [1](#r1)[2](#r2)[13](#r13)

      
      

        
Registration with --ephemeral terminates the runner daemon process upon job completion and unbinds its registration token in GitHub Actions. Operating system state, temporary files, modified binaries, and cached artifacts remain on disk unless an external controller (ARC, Tart, or libvirt script) destroys the virtual disk image. [1](#r1)[2](#r2)[13](#r13)

        

          
**Verification:** GitHub Docs state --ephemeral handles logical de-registration from the GitHub service after one job, and explicitly advises operators to automate machine teardown to achieve clean state.
          
**Stated Limits:** Log files generated during ephemeral runs must be streamed externally or they are lost upon container/VM destruction.
        
      
    
    

      
      

        

          
            | Isolation Primitive | Kernel Boundary | Startup Latency | Persistence Risk | Security Verdict |

          
          
            | **Bare Metal Host** | Shared with host OS | 0 ms | Severe (Filesystem, Daemons, Cron) | REJECTED FOR CI |

            | **Docker (`/var/run/docker.sock`)** | Shared host Linux kernel | 1 – 2 sec | Root-equivalent host breakout | REJECTED FOR CI |

            | **Rootless Podman** | User namespaces (Shared kernel) | 1 – 3 sec | Mitigated host root, kernel 0-day risk | DEFENSE IN DEPTH |

            | **Firecracker / KVM (Linux)** | Hardware-isolated guest kernel | < 125 ms | Zero (Ephemeral VM per job) | PRODUCTION FLOOR |

            | **Tart / Apple Virtualization (macOS)** | Hardware-isolated guest macOS | 2 – 5 sec (Snapshot) | Zero (APFS clone destroyed per job) | PRODUCTION FLOOR |

            | **Hyper-V Containers (Windows)** | Hyper-V isolated kernel | 5 – 10 sec | Zero (VM container destroyed per job) | PRODUCTION FLOOR |

          
        

      
    

    
    

      
## 4. Network Architecture: Outbound-Only Pull vs Lateral Egress

      
The GitHub Actions runner architecture is inherently outbound: agents initiate long-polling TLS connections over TCP 443 to GitHub's message queue. No incoming ports are required [2](#r2)[14](#r14).

      
    

      

        C6
        Direct Evidence
        HIGH CONFIDENCE
      
      

        
Your local build machine only dials out to GitHub to ask for work; it never opens any incoming doors or ports to the public internet. You do not need to change your home or office router to let outside connections in. [2](#r2)[14](#r14)[22](#r22)

      
      

        
The GitHub runner architecture is strictly outbound. The runner initiates outbound HTTPS long-poll connections on port 443 to GitHub's message queue, requiring zero inbound port forwarding while runner groups partition repositories. [2](#r2)[14](#r14)[22](#r22)

      
      

        
The GitHub Actions runner agent establishes outbound HTTPS (TCP 443) sessions to GitHub API and long-polling message queues (~50s timeout). Because dispatch is pull-based over established TLS connections, runners operate behind NAT while runner group policies restrict dispatch to vetted private repositories. [2](#r2)[14](#r14)[22](#r22)

        

          
**Verification:** GitHub Actions runner architecture design documentation confirms outbound long-polling to https://api.github.com and message queues with ~50s timeouts. Runner groups enforce repo-level workflow boundaries.
          
**Stated Limits:** Runner still requires outbound access to GitHub API domains, package repositories, and artifact storage endpoints.
        
      
    
    
      
    

      

        C7
        Direct Evidence
        HIGH CONFIDENCE
      
      

        
If an infected build runs on your normal network, it can scan your home or office to find file servers, printers, and other computers to attack, or steal cloud account keys from nearby servers. [1](#r1)[3](#r3)[21](#r21)[23](#r23)

      
      

        
Without network segmentation, a compromised runner can scan internal subnets (RFC1918) and cloud metadata services (IMDS at 169.254.169.254). Dedicated CI VLANs and short-lived OIDC role assumption neutralize lateral movement. [1](#r1)[3](#r3)[21](#r21)[23](#r23)

      
      

        
Default CI host network routing allows workflow scripts to execute network discovery across private RFC1918 address spaces and probe link-local cloud metadata endpoints (169.254.169.254). Strict VLAN firewall rules must drop lateral RFC1918 egress while workflows authenticate to cloud providers via short-lived OIDC tokens. [1](#r1)[3](#r3)[21](#r21)[23](#r23)

        

          
**Verification:** Sysdig and Praetorian research confirm compromised CI jobs deploy nmap/curl to discover LAN services and harvest IMDS credentials. CISA software supply chain guidelines mandate blocking RFC1918, while GitHub OIDC eliminates static cloud keys.
          
**Stated Limits:** Mitigated by placing runners in a dedicated VLAN with switch-level default-deny rules for RFC1918 and link-local addresses.
        
      
    
    

      
      

        

          Blueprint // Zero-Trust CI Network Segmentation
          OUTBOUND LONG-POLL (TCP 443)
        
        

          

            
GitHub SaaS Control Plane
            
• `api.github.com`

              • `*.actions.githubusercontent.com`

              • Actions Runner Controller (JIT tokens)

              • HTTP Long-Poll (~50s timeout)

          

          

            ← Outbound Long-Poll
            

            ✕ Inbound Blocked
          

          

            
Dedicated CI VLAN / DMZ
            
• Disposable MicroVMs (Firecracker / Tart)

              • Strict DNS allowlist (registries & GitHub)

              • Default-deny all RFC1918 traffic

              • Block IMDS (`169.254.169.254`)

          

        

        

          

            BLOCKED LATERAL VECTORS (FIREWALL DROPS)
          
          
• Corporate LAN / Developer Workstations (10.0.0.0/8, 192.168.0.0/16, 172.16.0.0/12)

            • Cloud Metadata Services (AWS/GCP/Azure IMDS `http://169.254.169.254`)

            • Office NAS, Routers, Internal Databases, and Production Jump Hosts

        
      
    

    
    

      
## 5. Hardware Platforms: Apple Silicon, Linux Mini PCs, and Windows

      
Selecting the host hardware is constrained by build toolchains (Xcode requirement) and vendor licensing agreements [6](#r6)[7](#r7)[10](#r10)[12](#r12)[24](#r24).

      
    

      

        C5
        Direct Evidence
        HIGH CONFIDENCE
      
      

        
Apple's legal rules strictly forbid running more than two virtual Macs on a single physical Mac computer at the same time. Even if you buy an ultra-powerful Mac with 24 processor cores, you can only run two test builds at once. [6](#r6)[7](#r7)[12](#r12)

      
      

        
Apple's macOS license explicitly limits virtualization to two concurrent macOS guest instances per physical Mac. This creates a legal ceiling that renders high-end Mac Studios or Mac Pros inefficient for CI density, favoring horizontal fleets of base Mac minis. [6](#r6)[7](#r7)[12](#r12)

      
      

        
macOS SLA Section 2.B.iii restricts organizations to running at most two (2) additional virtual instances of macOS on physical Apple hardware. This EULA constraint limits VM density, forcing macOS CI farms to scale horizontally with dual-instance Mac mini nodes rather than vertically on high-core Apple Silicon (M4 Max/Ultra). [6](#r6)[7](#r7)[12](#r12)

        

          
**Verification:** Verified in macOS Sequoia Software License Agreement section 2.B.iii: 'you may install, use and run up to two (2) additional copies or instances of the Apple Software... within virtual operating system environments on each Apple-branded computer'.
          
**Stated Limits:** Applies strictly to macOS guest operating systems; Linux guests virtualized on Apple Silicon are unrestricted by Apple's macOS SLA.
        
      
    
    
      
    

      

        C9
        Inference
        MEDIUM CONFIDENCE
      
      

        
Constantly creating and deleting thousands of temporary build files puts huge wear on regular solid-state hard drives, which can wear out and break much faster than normal. [24](#r24)

      
      

        
High-volume CI churn causes 2x–5x SSD write amplification. Repeatedly extracting dependency archives and cloning VM disks can exhaust consumer SSD endurance limits within months, requiring enterprise-grade drives or tmpfs workspace mounts. [24](#r24)

      
      

        
High-frequency creation and teardown of container layers and ephemeral VM disk overlays produce heavy random write patterns. Because NAND flash blocks require erase-before-write cycles, garbage collection amplifies logical writes by 2x-5x WAF. A continuous CI pipeline writing 500GB/day can exhaust a 600 TBW consumer SSD warranty within 12–18 months. [24](#r24)

        

          
**Verification:** Storage engineering benchmarks show small random writes from uncompressing node_modules, Docker layer extraction, and VM snapshot churn cause 2x-5x WAF against NAND flash blocks. 1TB consumer drives rated at 600 TBW degrade rapidly.
          
**Stated Limits:** Can be mitigated by using Enterprise NVMe SSDs (>=1 DWPD), RAM disks (tmpfs) for build workspaces, or dedicated disposable cache drives.
        
      
    
    

      

        **The Apple Silicon Ceiling:** Apple's Software License Agreement Section 2.B.iii hardcodes a maximum of two virtual instances of macOS per Apple-branded host [6](#r6). Purchasing high-end 24-core Mac Studios or Mac Pros for macOS CI density is economically irrational; teams must scale horizontally using base Mac mini nodes (2 VMs each).
      
    

    
    

      
## 6. Stated Limits, Methodological Bounds & Disagreements

      
To preserve empirical integrity, this report explicitly documents the bounds of its models and where panel sources diverged:

      

        

          
2026 Pricing Volatility
          
We could not confirm if Microsoft will reintroduce a modified self-hosted fee in 2027 after its indefinite postponement. Current calculations remain unverified against future pricing shifts.

        
        

          
Workload-Specific Burst Latency
          
There is no public data on exact developer idle time costs during burst PR queues on local hardware. The trade-off between fixed local capacity and elasticity remains unmeasured across varying team sizes.

        
        

          
Enterprise Tart Licensing
          
Tart's Fair Source license is free up to 100 host CPU cores. Fleets exceeding 100 cores incur a $12,000/year licensing fee, which we could not establish as cost-effective for smaller mid-market fleets [11](#r11).

        
      
    

    
    

      

        

          RESEARCH METHODOLOGY & PROVENANCE COLOPHON
        
        
This report was synthesized from a multi-backend research panel comprising **112 verified citations** across Google Gemini (`deep-research-preview-04-2026`), OpenAI GPT (`gpt-5.6-terra`), and Perplexity Sonar (`sonar-deep-research`). Primary legal artifacts—including Apple's macOS Sequoia/Tahoe Software License Agreement (§2.B.iii) and GitHub's official 2026 Actions billing schedules—were verified against first-party vendor documentation [5](#r5)[6](#r6)[13](#r13)[21](#r21).

        
Environment: Darwin 25.6.0 · Compiler: Python 3.14 · Primary Sources: 24 first-party vendor and standards documents.

      
    

    
    

      
## Sources Registry

      
All 24 primary sources cited across Primer, Brief, and Technical registers:

      

        
        1. [1]
            [Secure use reference - GitHub Actions Documentation](https://docs.github.com/en/actions/reference/security/secure-use)
          
          
GitHub Docs
          
GitHub explicitly warns that private and internal repository contributors who can invoke workflows can compromise self-hosted runners, access GITHUB_TOKEN and secrets, and that self-hosted runners do not have clean ephemeral VM guarantees by default

        
        1. [2]
            [Self-hosted runners reference and configuration guide](https://docs.github.com/en/actions/reference/runners/self-hosted-runners)
          
          
GitHub Docs
          
Defines runner lifecycle, --ephemeral registration flag, outbound HTTPS/443 requirements, 30-day runner update policy, and states that container actions require Linux

        
        1. [3]
            [From Self-Hosted GitHub Runner to Self-Hosted Backdoor](https://www.praetorian.com/blog/self-hosted-github-runners-are-backdoors/)
          
          
Praetorian Security Research
          
Demonstrates full-chain compromise on private repos: token harvesting, process snooping, lateral movement into internal RFC1918 networks, and persistence across builds

        
        1. [4]
            [How Threat Actors Are Using Self-Hosted GitHub Actions Runners as Backdoors](https://www.sysdig.com/blog/how-threat-actors-are-using-self-hosted-github-actions-runners-as-backdoors)
          
          
Sysdig Threat Research
          
Analyzes the Shai-Hulud attack vector: bypassing cleanup via RUNNER_TRACKING_ID=0, overriding root protections via RUNNER_ALLOW_RUNASROOT=1, and routing C2 over GitHub Discussions

        
        1. [5]
            [Actions runner billing and per-minute rate schedules (2026)](https://docs.github.com/en/billing/reference/actions-runner-pricing)
          
          
GitHub Docs
          
Official 2026 published baseline rates: Linux 2-core at $0.006/min, Windows 2-core at $0.010/min, macOS 3/4-core at $0.062/min, and Linux ARM 4-core at $0.008/min

        
        1. [6]
            [macOS Sequoia Software License Agreement (Section 2.B.iii)](https://www.apple.com.cn/legal/sla/docs/macOSSequoia.pdf)
          
          
Apple Inc.
          
Apple SLA legally restricts virtualization to a maximum of two (2) additional copies/instances of macOS within virtual operating system environments on an Apple-branded host

        
        1. [7]
            [Apple Virtualization Framework API Reference](https://developer.apple.com/documentation/virtualization)
          
          
Apple Developer
          
Native framework for virtualizing macOS and Linux guests on Apple Silicon, exposing VZVirtualMachine, VZMacOSBootLoader, and hardware acceleration

        
        1. [8]
            [Docker Engine Security and Daemon Attack Surface](https://docs.docker.com/engine/security/)
          
          
Docker Docs
          
Exposing /var/run/docker.sock or granting docker group access confers root-equivalent host privileges and allows arbitrary host filesystem mounts

        
        1. [9]
            [Firecracker: Secure and Fast microVMs for Serverless Computing](https://firecracker-microvm.github.io/)
          
          
Firecracker MicroVM Project / AWS
          
Hardware-enforced KVM microVMs with <125 ms startup time, <5 MiB memory footprint per instance, and minimal device attack surface

        
        1. [10]
            [Tart: Virtualization toolset for macOS and Linux on Apple Silicon](https://tart.run/)
          
          
Cirrus Labs
          
CLI and OCI-based VM manager utilizing Apple Virtualization.framework for disposable macOS and Linux CI runners

        
        1. [11]
            [Tart Licensing and Support Tiers](https://tart.run/licensing/)
          
          
Cirrus Labs
          
Tart Fair Source license is free up to 100 host CPU cores; enterprise fleets exceeding 100 cores require commercial licensing starting at $12,000/year

        
        1. [12]
            [Tartelet: macOS app for ephemeral GitHub Actions runners on Apple Silicon](https://github.com/shapehq/tartelet)
          
          
ShapeHQ
          
Empirical benchmarks showing 3-4x build acceleration over GitHub-hosted M1 runners, 25-30s VM boot/clone latency, and 12% overhead for 2 parallel VMs

        
        1. [13]
            [Actions Runner Controller (ARC) Overview and Architecture](https://docs.github.com/en/actions/concepts/runners/actions-runner-controller)
          
          
GitHub Docs
          
Kubernetes operator for autoscaling ephemeral runner scale sets based on queue depth and JIT configuration tokens

        
        1. [14]
            [GitHub Actions Runner Authentication and Dispatch Design](https://github.com/actions/runner/blob/main/docs/design/auth.md)
          
          
GitHub Actions Runner Repository
          
Runner connects via outbound HTTPS/WSS (TCP 443) using HTTP long-poll message queues (50s timeouts); requires no inbound port forwarding

        
        1. [15]
            [Podman User Namespace and Rootless Container Isolation](https://docs.podman.io/en/latest/markdown/podman.1.html)
          
          
Podman Documentation
          
Rootless containers map UID 0 to unprivileged host subordinate UIDs via user namespaces, preventing root-level host modification but sharing the host kernel

        
        1. [16]
            [Secure Windows Containers: Process vs Hyper-V Isolation](https://learn.microsoft.com/en-us/virtualization/windowscontainers/manage-containers/container-security)
          
          
Microsoft Learn
          
Microsoft defines Hyper-V isolation as a hardware security boundary with dedicated kernels, while process-isolated containers share host kernel

        
        1. [17]
            [npm Scripts and Lifecycle Hooks Execution Reference](https://docs.npmjs.com/cli/using-npm/scripts/)
          
          
npm Documentation
          
npm ci and npm install automatically execute preinstall, install, postinstall, and prepare scripts with full runner execution privileges

        
        1. [18]
            [U.S. Electricity Prices and Factors Affecting Rates (2025/2026)](https://www.eia.gov/energyexplained/electricity/prices-and-factors-affecting-prices.php)
          
          
U.S. Energy Information Administration (EIA)
          
U.S. residential retail electricity prices averaged 17.30¢/kWh ($0.173/kWh) in 2025/2026, establishing the baseline for hardware power OpEx

        
        1. [19]
            [Intel N100 and Low-Power Mini PC Power Consumption Guide](https://bishalkshah.com.np/blog/low-power-homelab-n100-mini-pc)
          
          
Homelab Infrastructure Benchmarks
          
Intel N100 mini PCs idle at 6-8W and average 9-11W under container load, costing $8-$12/year in electricity with a 5-year hardware TCO under $250

        
        1. [20]
            [Preventing Pwn Requests in GitHub Actions Workflows](https://securitylab.github.com/resources/github-actions-preventing-pwn-requests/)
          
          
GitHub Security Lab
          
Explains pull_request_target risks, GITHUB_TOKEN exfiltration, and cache poisoning vulnerabilities across workflow boundaries

        
        1. [21]
            [Stopping Ransomware: CISA Software Supply Chain Guidelines](https://www.cisa.gov/stopransomware/ransomware-guide)
          
          
Cybersecurity and Infrastructure Security Agency (CISA)
          
Mandates strict network segmentation (VLANs), blocking lateral RFC1918 traffic, and restricting CI/CD egress to explicitly verified domains

        
        1. [22]
            [Managing Access to Self-Hosted Runners Using Groups](https://docs.github.com/en/actions/how-tos/manage-runners/self-hosted-runners/manage-access)
          
          
GitHub Docs
          
Details organizational runner groups, repository allowlists, and workflow path pinning to prevent unauthorized cross-repo runner execution

        
        1. [23]
            [OpenID Connect (OIDC) Authentication in GitHub Actions](https://docs.github.com/en/actions/concepts/security/openid-connect)
          
          
GitHub Docs
          
Enables short-lived, job-scoped cloud provider tokens (AWS/GCP/Azure) without persisting static long-lived credentials on runner disks

        
        1. [24]
            [SSD Endurance, TBW Specifications, and CI Write Amplification](https://download.semiconductor.samsung.com/resources/data-sheet/samsung_nvme_ssd_990_pro_datasheet_rev.2.0.pdf)
          
          
Samsung Semiconductor / Storage Engineering
          
Consumer 1TB NVMe SSDs are rated for ~600 TBW; high CI churn (Docker builds, VM rollbacks, dependency caches) creates 2x-5x write amplification

        
      

    

  

  
  

  

    

      [![](data:image/svg+xml;base64,<stripped>)](https://github.com/fledgeling-co/dossier-research-mcp)
      [![](data:image/svg+xml;base64,<stripped>)](https://margin.fledgeling.app/)
    
    

      
## CI/CD without the compromise.

      
Self-hosting GitHub Actions runners transforms SaaS per-minute billing into local infrastructure management. It saves substantial money on macOS workloads while requiring hardware-isolated microVMs and dedicated CI VLANs to prevent software supply chain compromise.

    
    
      Panel BackendsGoogle Gemini · OpenAI GPT · Perplexity Sonar
      Corpus Depth112 verified citations across 3 independent engines
      Isolation FloorDisposable microVM per job (KVM/Firecracker/Tart)
      Licensing BoundApple SLA limits macOS guests to 2 concurrent instances per physical host
