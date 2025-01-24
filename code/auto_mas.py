"""
auto_mas.py — A minimal, runnable miniature of "automated multi-agent system design".

It demonstrates the core idea shared by ADAS / AFlow / MaAS / GPTSwarm:
    designing a multi-agent system = searching over a space of (operators, topology)
    to optimize a multi-objective score (accuracy AND cost).

To stay offline & verifiable, "agents" here are deterministic rule-based stand-ins
for LLM calls. Each agent has a noisy success profile, exactly like a real LLM call.
Swap `BaseSolver.solve` for a real API call and the search machinery is unchanged.

Run:  python3 auto_mas.py
"""
from __future__ import annotations
import random, itertools, statistics
from dataclasses import dataclass, field
from typing import Callable

# ----------------------------------------------------------------------------
# 1. A TASK DISTRIBUTION  (stand-in for a benchmark like GSM8K / MATH)
#    Each task is a noisy arithmetic problem; "noise" = distractor text that
#    makes a naive single agent fail part of the time.
# ----------------------------------------------------------------------------
def make_task(rng: random.Random):
    a, b = rng.randint(2, 30), rng.randint(2, 30)
    op = rng.choice(["+", "-", "*"])
    answer = {"+": a + b, "-": a - b, "*": a * b}[op]
    hardness = rng.random()  # 0 = easy, 1 = hard (more distractors)
    return {"a": a, "b": b, "op": op, "answer": answer, "hardness": hardness}


# ----------------------------------------------------------------------------
# 2. BASE AGENT  (one "LLM call"). Imperfect: fails more on hard tasks.
#    A real implementation would put an API call inside solve().
# ----------------------------------------------------------------------------
@dataclass
class BaseSolver:
    skill: float          # competence in [0,1]
    rng: random.Random

    def solve(self, task) -> int:
        # probability of a correct computation drops with task hardness
        p_correct = self.skill * (1 - 0.6 * task["hardness"])
        a, b, op = task["a"], task["b"], task["op"]
        correct = {"+": a + b, "-": a - b, "*": a * b}[op]
        if self.rng.random() < p_correct:
            return correct
        # a plausible-but-wrong answer (off-by-something / wrong op)
        return correct + self.rng.choice([-2, -1, 1, 2, 3]) * self.rng.randint(1, 4)


# ----------------------------------------------------------------------------
# 3. OPERATORS  = the reusable agentic patterns the search composes.
#    (This mirrors AFlow's "operators" and MaAS's "operator pool".)
#    Each operator returns (answer, cost_in_llm_calls).
# ----------------------------------------------------------------------------
def op_single(solvers, task, rng):
    return solvers[0].solve(task), 1

def op_self_consistency(solvers, task, rng, k=3):
    # sample k times from one agent, majority vote (Wang et al. self-consistency)
    votes = [solvers[0].solve(task) for _ in range(k)]
    return statistics.mode(votes), k

def op_debate(solvers, task, rng, rounds=2):
    # several agents answer; a "judge" picks the majority across agents (Du et al.)
    answers = [s.solve(task) for s in solvers]
    cost = len(solvers)
    for _ in range(rounds - 1):  # extra rounds = extra cost, small accuracy gain
        answers += [s.solve(task) for s in solvers]
        cost += len(solvers)
    return statistics.mode(answers), cost

def op_reflexion(solvers, task, rng):
    # solve, then a verifier re-checks; on disagreement, resolve by a 3rd opinion
    first = solvers[0].solve(task)
    check = solvers[1].solve(task)
    cost = 2
    if first == check:
        return first, cost
    tie = solvers[2].solve(task)
    return statistics.mode([first, check, tie]), cost + 1

OPERATORS = {
    "single": op_single,
    "self_consistency": op_self_consistency,
    "debate": op_debate,
    "reflexion": op_reflexion,
}

# ----------------------------------------------------------------------------
# 4. A CANDIDATE MAS = a choice of operator + how many agents (topology size).
#    This is the genome the search mutates. ADAS searches code; here we search
#    a compact structured space for clarity.
# ----------------------------------------------------------------------------
@dataclass
class MASCandidate:
    operator: str
    n_agents: int
    skills: tuple  # per-agent competence

    def build_solvers(self, rng):
        return [BaseSolver(skill=s, rng=rng) for s in self.skills]

    def run(self, task, rng):
        solvers = self.build_solvers(rng)
        fn = OPERATORS[self.operator]
        return fn(solvers, task, rng)


# ----------------------------------------------------------------------------
# 5. EVALUATOR  -> multi-objective score (accuracy minus cost penalty).
#    This is the MaAS/AutoMaAS insight: optimize cost-aware utility, not raw acc.
# ----------------------------------------------------------------------------
def evaluate(cand: MASCandidate, n_tasks=400, lam=0.015, seed=0):
    rng = random.Random(seed)
    correct, total_cost = 0, 0
    for _ in range(n_tasks):
        task = make_task(rng)
        ans, cost = cand.run(task, rng)
        correct += (ans == task["answer"])
        total_cost += cost
    acc = correct / n_tasks
    avg_cost = total_cost / n_tasks
    utility = acc - lam * avg_cost     # multi-objective: accuracy vs. compute
    return {"acc": acc, "avg_cost": avg_cost, "utility": utility}


# ----------------------------------------------------------------------------
# 6. SEARCH  — an evolutionary meta-search over MAS candidates.
#    (ADAS uses a meta-agent; AFlow uses MCTS; MaAS samples a supernet.
#     Evolution is the simplest faithful illustration of the loop.)
# ----------------------------------------------------------------------------
def random_candidate(rng):
    op = rng.choice(list(OPERATORS))
    n = rng.choice([1, 2, 3, 4])
    n = max(n, 3) if op in ("debate", "reflexion") else n  # those need >=3 agents
    skills = tuple(round(rng.uniform(0.6, 0.9), 2) for _ in range(n))
    return MASCandidate(op, n, skills)

def mutate(c, rng):
    op = c.operator
    if rng.random() < 0.4:
        op = rng.choice(list(OPERATORS))
    n = len(c.skills)
    if rng.random() < 0.4:
        n = max(1, n + rng.choice([-1, 1]))
    n = max(n, 3) if op in ("debate", "reflexion") else n
    skills = tuple(round(min(0.95, max(0.5, s + rng.uniform(-0.1, 0.1))), 2)
                   for s in (c.skills * 3)[:n])
    return MASCandidate(op, n, skills)

def evolutionary_search(generations=12, pop_size=10, seed=42):
    rng = random.Random(seed)
    population = [random_candidate(rng) for _ in range(pop_size)]
    history = []
    for gen in range(generations):
        scored = [(evaluate(c, seed=gen), c) for c in population]
        scored.sort(key=lambda x: x[0]["utility"], reverse=True)
        best_score, best_c = scored[0]
        history.append((gen, best_score, best_c))
        # keep top half (elitism), breed the rest by mutation
        survivors = [c for _, c in scored[: pop_size // 2]]
        children = [mutate(rng.choice(survivors), rng)
                    for _ in range(pop_size - len(survivors))]
        population = survivors + children
    return history


if __name__ == "__main__":
    print("=== Baselines (one fixed design, no search) ===")
    rng = random.Random(7)
    for op in OPERATORS:
        n = 3 if op in ("debate", "reflexion") else 2
        cand = MASCandidate(op, n, tuple([0.75] * n))
        r = evaluate(cand)
        print(f"  {op:18s} acc={r['acc']:.3f}  cost={r['avg_cost']:.2f}  "
              f"utility={r['utility']:.3f}")

    print("\n=== Evolutionary meta-search (design-as-search) ===")
    hist = evolutionary_search()
    for gen, score, cand in hist:
        print(f"  gen {gen:2d}: utility={score['utility']:.3f} "
              f"(acc={score['acc']:.3f}, cost={score['avg_cost']:.2f}) "
              f"<- {cand.operator}, n={len(cand.skills)}")

    best = max(hist, key=lambda h: h[1]["utility"])
    print(f"\nDISCOVERED DESIGN: operator={best[2].operator}, "
          f"agents={len(best[2].skills)}, "
          f"utility={best[1]['utility']:.3f}")
