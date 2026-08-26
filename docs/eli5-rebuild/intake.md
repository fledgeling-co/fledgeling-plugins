# Intake: eli5 Skill Teardown & Baseline Analysis

## 1. Source Artifacts
- **Repository**: `anthropics/claude-plugins-community` (Path: `eli5/`)
- **Author**: Thariq Shihipar
- **License**: MIT
- **Plugin Manifest**:
  ```json
  {
    "name": "eli5",
    "version": "1.0.0",
    "description": "Explain any topic like I'm 5: a dead-simple HTML picture explainer with big visuals and few words. Use /eli5 <topic>.",
    "author": { "name": "Thariq Shihipar" },
    "keywords": ["explain", "eli5", "learning", "explainer", "html"]
  }
  ```
- **SKILL.md**:
  ```markdown
  ---
  name: eli5
  description: Explain a topic like I'm a 5 year old. Use when the user types /eli5 <topic> or asks for a dead-simple picture explainer of how something works.
  ---

  # eli5

  Explain like I'm someone who knows nothing about this topic, using a HTML artifact with big pictures and few words.

  Topic: $ARGUMENTS
  ```

## 2. Core Intent vs Real-World Failure Modes
The original `eli5` targets a fundamental developer and thinker need: rapid intuitive grasp of complex abstractions (distributed consensus, quantum computing, memory allocators, zero-knowledge proofs, TCP handshakes, derivatives pricing).

However, in practice, a one-line prompt causes four fatal failure modes:

1. **The Image & Asset Collapse (Artifact CSP Violation)**:
   - When asked for "big pictures", LLMs instinctively output `<img src="https://...">` (Unsplash, placeholder.com, or hallucinated URLs).
   - In Claude Code / modern sandboxed web artifacts, strict CSP blocks all remote image requests.
   - Result: Broken image icons across the entire explainer artifact.

2. **The Analogy Trap & Misconception Creep (Structure Mapping Failure)**:
   - Superficial analogies (e.g. "DNS is a phonebook", "Raft consensus is a group of friends picking a movie", "Transformers are a librarian") map surface attributes rather than structural mechanisms.
   - When the user asks "how does failover work" or "how do attention weights compute", the metaphor shatters or actively misleads.
   - Missing: Dedra Gentner's Structure-Mapping constraint, boundary declarations ("Where this analogy holds vs where it breaks").

3. **Absence of Bret Victor's "Ladder of Abstraction"**:
   - Complex concepts require moving seamlessly between:
     - Rung 1: Concrete Physical Intuition (Anchoring story/analogy)
     - Rung 2: Interactive Simulation / Parameter Exploration (Scrubbable variables, step-by-step state machine)
     - Rung 3: Mechanical Anatomy (Pure inline SVG diagram with clear visual hierarchy)
     - Rung 4: Technical Reality (How real-world systems actually implement it)
   - The original skill produces a flat, static document with walls of text disguised with oversized emojis.

4. **Tone Degradation (Patronizing vs Feynman Technique)**:
   - Prompting "like I'm a 5 year old" leads to condescending nursery-school framing ("Imagine a magical fairy flying through cables!").
   - Real ELI5 is the Feynman Technique: Explaining deep physics or systems engineering in plain, clear, non-jargon language that respects the reader's intellect.

5. **Visual Architecture Deficits**:
   - No CSS custom property design system (`:root` / `@media (prefers-color-scheme: dark)`).
   - SVG diagrams lack responsive `viewBox` scaling, crisp semantic palette, typography scale, or touch/hover interaction states.
