# Contributing guide

Thank you for helping make this list more accurate and more useful. This guide walks through every contribution type step by step.

## Quick links

| I want to… | Do this |
|------------|---------|
| Add a **paper** | [Suggest paper issue](https://github.com/sukoji/awesome-self-evolving-agents/issues/new?template=suggest-paper.yml) or PR to `README.md` |
| Add an **open-source project** | [Suggest project issue](https://github.com/sukoji/awesome-self-evolving-agents/issues/new?template=suggest-project.yml) or PR to `COMMUNITY.md` |
| Fix a **wrong link / typo / section** | [Correction issue](https://github.com/sukoji/awesome-self-evolving-agents/issues/new?template=correction.yml) — highest priority |
| Run the **demos** | [`code/README.md`](../code/README.md) |
| Understand **scope** | [README § Scope and stance](../README.md#scope-and-stance) |

---

## Philosophy

This list is deliberately **opinionated and walkable**:

- **Accuracy over volume.** A verified entry without a link beats a guessed arXiv ID.
- **One change per PR.** Papers and community projects are reviewed separately.
- **Neutral tone.** Describe mechanisms, not hype.

---

## Adding a paper (README.md)

### 1. Check scope

The work must involve an LLM agent whose **behavior-generating machinery changes over time** from its own operation — automated design, test-time learning, evolving memory, skills, RL self-improvement, or the safety/eval problems these create.

**Usually out of scope:** one-shot prompting, static multi-agent chat with no learning loop, pure pre-training.

### 2. Pick a section

Use the [table of contents](../README.md#contents). If it spans multiple areas, pick the **primary** pathway and mention others in the sentence.

### 3. Format

```markdown
- **Paper Title** — Venue'Year. [arXiv:XXXX.XXXXX](https://arxiv.org/abs/XXXX.XXXXX). One neutral sentence describing what the system does.
```

If you cannot verify a stable ID:

```markdown
- **Paper Title** — Venue'Year. needs-link. One neutral sentence. (PR note: could not verify arXiv ID.)
```

### 4. Open a PR

- Branch name: `add/paper-short-name`
- One entry only
- Fill out the PR template checklist

**Example (good):**

```markdown
- **Reflexion: Language Agents with Verbal Reinforcement Learning** — NeurIPS 2023. [arXiv:2303.11366](https://arxiv.org/abs/2303.11366). Stores verbal self-reflection across episodes without weight updates.
```

**Example (bad):**

```markdown
- **Reflexion** — A groundbreaking paradigm-shifting agent that revolutionizes RL.
```

---

## Adding a community project (COMMUNITY.md)

Community entries are **open-source repositories** — frameworks, benchmarks, harnesses — not individual papers.

### Format (table row)

```markdown
| [**RepoName**](https://github.com/org/repo) | author | workflow | One neutral sentence. |
```

Pathway tags: `model` · `memory` · `tool` · `workflow` · `—` (benchmarks only).

### Requirements

- Public repo, meaningful README, signs of maintenance
- Implements or **evaluates** self-evolution (learning loop, search, memory writes, skill library, etc.)
- Not a duplicate of an existing row

Add your row under the best section, and append to **Recently added** with today's month.

---

## Review timeline

- **Corrections:** aim for &lt; 48h
- **New papers / projects:** usually within a week
- **Scope debates:** we may ask for a short justification comment — that is normal

---

## Code of conduct

Be direct and kind. See [CODE_OF_CONDUCT.md](../CODE_OF_CONDUCT.md).
