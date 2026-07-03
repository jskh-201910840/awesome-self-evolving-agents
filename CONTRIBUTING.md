# Contributing

Contributions are welcome. This list aims to stay *walkable*, so quality and accuracy matter more than volume.

**Start here:** [Contributing guide](docs/contributing-guide.md) — step-by-step for papers, projects, and corrections.

| I want to… | Fast path |
|------------|-----------|
| Add a **paper** | [Suggest paper issue](https://github.com/sukoji/awesome-self-evolving-agents/issues/new?template=suggest-paper.yml) or PR → `README.md` |
| Add an **OSS project** | [Suggest project issue](https://github.com/sukoji/awesome-self-evolving-agents/issues/new?template=suggest-project.yml) or PR → [`COMMUNITY.md`](COMMUNITY.md) |
| Fix a **link / typo / section** | [Correction issue](https://github.com/sukoji/awesome-self-evolving-agents/issues/new?template=correction.yml) — highest priority |

---

## Guidelines (papers)

- **One entry per pull request.** It keeps review honest and history clean.
- **Describe what the work does, not how good it is.** One neutral sentence. "Samples a query-specific system from a supernet" — not "a groundbreaking approach that revolutionizes…".
- **Provide a verifiable link.** A stable arXiv, OpenReview, or venue URL. If you cannot verify a stable ID, say so in the PR and add the entry with a `needs-link` note rather than a guessed identifier. We would rather have a linkless entry than a wrong link.
- **Put it in the right section.** If it spans several, pick the primary one and mention the others in the description.
- **Match the existing format:** `- **Title** — venue'year. [arXiv:ID](url). One sentence.`

---

## Community projects

**Papers** live in `README.md`. **Runnable repos, harnesses, and benchmarks** live in [`COMMUNITY.md`](COMMUNITY.md).

Table row format:

```markdown
| [**RepoName**](https://github.com/org/repo) | author | workflow | One neutral sentence. |
```

Pathway tags: `model` · `memory` · `tool` · `workflow` · `—` (eval-only).

Requirements:

- Public repo with signs of maintenance (commit in ~6 months, or a release tag)
- Implements or **evaluates** self-evolution — not a static agent demo with no learning loop
- One neutral sentence; no marketing copy

After merging, append the project to **Recently added** in `COMMUNITY.md` for one month.

---

## What belongs here

Work where the agent's behavior-generating machinery changes over time from its own operation: automated design, test-time learning, evolving memory, skill acquisition, RL-driven self-improvement, and the safety/evaluation problems these create.

## What does not

One-shot prompting techniques, static frameworks with no learning loop, and non-agentic pre/post-training. Borderline cases are fine to propose — open a PR and we can discuss scope.

## Fixing mistakes

Corrections (wrong attribution, dead link, mis-sectioned entry) are the most valuable PRs of all. No entry is too small to fix.

## Review

- **Corrections:** aim for &lt; 48h
- **New papers / projects:** usually within a week
- Scope questions are normal — we may ask for a short justification

## Code of conduct

Be direct and kind. See [CODE_OF_CONDUCT.md](CODE_OF_CONDUCT.md).
