# Reference implementations

Two small, dependency-light programs (Python 3.9+; `safety_gated_evolution.py` also uses `numpy` and `matplotlib`). Both are offline and deterministic. Each is written so a real LLM call drops into one clearly marked method — the search/learning machinery around it does not change.

## `auto_mas.py` — design-as-search in miniature

A faithful miniature of ADAS / AFlow / MaAS. Designing a multi-agent system is framed as searching over `(operators, topology)` to maximize a cost-aware utility. An evolutionary meta-search discovers a debate-style operator, and shows that adding more agents keeps raising raw accuracy while lowering utility once compute is priced in.

```bash
python3 auto_mas.py
```

Swap the body of `BaseSolver.solve` for a real model call to turn it into a real design search.

## `safety_gated_evolution.py` — misevolution and two defenses

Reproduces the misevolution collapse, then studies a write-gate and periodic re-anchoring, tracing the utility-safety Pareto frontier. Writes `pareto_frontier.png` and `timeseries.png`.

```bash
pip install numpy matplotlib
python3 safety_gated_evolution.py
```

Swap `Agent.decide` / `Agent.update_memory` for real model calls + memory writes to lift it out of the toy setting. A line-by-line walkthrough is in [`../docs/primer.md`](../docs/primer.md).
