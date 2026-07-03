# Community spotlight

Open-source **projects, harnesses, and benchmarks** that implement or evaluate self-evolving agents — contributed and reviewed by the community.

> Papers live in [README.md](README.md). **This file is for runnable repos, tools, and eval stacks.**  
> Add yours via [issue template](https://github.com/sukoji/awesome-self-evolving-agents/issues/new/choose) or PR (see [CONTRIBUTING.md](CONTRIBUTING.md#community-projects)).

<p align="center">
  <a href="CONTRIBUTING.md"><img src="https://img.shields.io/badge/add_your_project-PR_or_issue-d85a30?style=for-the-badge&labelColor=1b1b1b" alt="Add your project"></a>
</p>

---

## How entries are listed

| Column | Meaning |
|--------|---------|
| **Pathway** | What evolves — `model` · `memory` · `tool` · `workflow` (see [taxonomy](README.md#the-four-evolution-pathways)) |
| **Focus** | One-line, neutral description |
| **Signals** | Maintainer-maintained, has eval harness, safety-aware, etc. |

---

## Harnesses & agent runtimes

| Project | Author | Pathway | Focus |
|---------|--------|---------|-------|
| [**OpenHands**](https://github.com/OpenHands/OpenHands) | OpenHands | workflow · tool | Open platform for code agents — event stream, sandbox, delegation; active SWE-bench ecosystem. |
| [**DSPy**](https://github.com/stanfordnlp/dspy) | Stanford NLP | workflow | Compile declarative LM pipelines into self-improving programs (prompt/weight optimizers). |
| [**EvoAgentX**](https://github.com/EvoAgentX/EvoAgentX) | EvoAgentX | workflow | Framework for evolving multi-agent workflows with search and evaluation hooks. |
| [**smolagents**](https://github.com/huggingface/smolagents) | Hugging Face | tool · workflow | Minimal agent library — code actions, tool routing, small surface area for experiments. |

---

## Design-as-search & meta-agents

| Project | Author | Pathway | Focus |
|---------|--------|---------|-------|
| [**ADAS** (reference impl.)](https://github.com/ShengranHu/ADAS) | Shengran Hu et al. | workflow | Automated Design of Agentic Systems — meta-agent search over agentic code. |
| [**AFlow** (reference impl.)](https://github.com/FoundationAgents/aflow) | FoundationAgents | workflow | MCTS over reusable workflow operators; practical ADAS successor. |
| [**GPTSwarm**](https://github.com/metauto-ai/gptswarm) | metauto-ai | workflow | Language agents as optimizable graphs — node/edge-level search. |

---

## Benchmarks & eval harnesses

| Project | Author | Pathway | Focus |
|---------|--------|---------|-------|
| [**AgentBench**](https://github.com/THUDM/AgentBench) | THUDM | — | Multi-environment benchmark for LLM-as-agent capability. |
| [**τ-bench**](https://github.com/sierra-research/tau-bench) | Sierra Research | — | Tool–agent–user interaction in customer-service domains. |
| [**sympo**](https://github.com/sukoji/sympo) | sukoji | workflow | Multi-agent PRD→WBS debate with eval harness and ablations. |
| [**tierforge**](https://github.com/sukoji/tierforge) | sukoji | — | Agent failure taxonomy and trace tooling for production-style eval. |

---

## Safety, memory & monitoring

| Project | Author | Pathway | Focus |
|---------|--------|---------|-------|
| [**AgentHarm**](https://github.com/ai-safety-institute/AgentHarm) | UK AISI | — | Benchmark for harmful capabilities in tool-using agents. |
| [**Mem0**](https://github.com/mem0ai/mem0) | mem0ai | memory | Memory layer for personalized agents — write/retrieve over long horizons. |

---

## Curated lists & reading logs (siblings)

| Project | Author | Focus |
|---------|--------|-------|
| [**EvoAgentX/Awesome-Self-Evolving-Agents**](https://github.com/EvoAgentX/Awesome-Self-Evolving-Agents) | EvoAgentX | Companion awesome list to the comprehensive survey. |
| [**XMUDeepLIT/Awesome-Self-Evolving-Agents**](https://github.com/XMUDeepLIT/Awesome-Self-Evolving-Agents) | XMUDeepLIT | Survey-aligned paper collection (what/when/how/where). |
| [**multi-agent-paper-log**](https://github.com/sukoji/multi-agent-paper-log) | sukoji | Paper-by-paper TIL on multi-agent systems (feeds this list). |

---

## Recently added

<!-- Maintainers: move new merges here for one month, then file under a section above. -->

| Date | Project | Contributor |
|------|---------|-------------|
| — | *Be the first community addition* | [open an issue](https://github.com/sukoji/awesome-self-evolving-agents/issues/new?template=suggest-project.yml) |

---

## Submission checklist

1. Repo is **public** and **maintained** (commit in the last ~6 months, or tagged release).
2. Clearly implements or evaluates **self-evolution** (not a static agent framework with no learning loop).
3. One **neutral** sentence — what it does, not marketing copy.
4. Pick the primary **pathway** tag.
5. Open a PR editing this file **or** use the [Suggest a project](https://github.com/sukoji/awesome-self-evolving-agents/issues/new?template=suggest-project.yml) issue.

See [CONTRIBUTING.md](CONTRIBUTING.md) for the full review rubric.
