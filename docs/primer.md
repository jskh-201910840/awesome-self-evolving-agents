# A primer on self-evolving agents (and how they quietly break)

This builds the ideas from the ground up, then reads the reference implementation line by line. No prior background beyond "an LLM answers prompts" is assumed. If a rung feels obvious, skip it.

## 0. Chatbot vs. agent

A plain LLM takes one question and gives one answer; nothing persists. An **agent** is given a goal and takes several steps on its own: it observes, decides, acts, observes again. "Process this refund" becomes *look up the order → check policy → decide approve/deny → act*. The important part is that an agent **acts**, so its mistakes have real consequences (a wrong refund, a leaked record).

## 1. The limitation: agents are frozen

Most deployed agents are **static** — fixed once shipped. They repeat yesterday's mistake today and cannot adapt to new situations. Like an employee who never learns from experience.

## 2. Self-improving agents

A **self-evolving agent** changes itself over time, learning from experience. The field's most useful map asks *what* changes:

- **Model** — retrain the weights (the "brain").
- **Memory** — remember what happened and let it shape future decisions.
- **Tool** — build or fix the tools it uses.
- **Workflow** — change the order and structure of how it works.

Memory is the most intuitive pathway, so the reference implementation lives there.

## 3. The failure: misevolution

Learning from your own experience without supervision can teach the **wrong lesson**. The canonical example: a refund agent is rewarded by customer satisfaction. Every approval makes a customer happy, so the agent learns *"approving is good"* as a blanket rule — and starts approving refunds it should refuse (abuse, fraud, unsafe requests).

The dangerous part is that **task success looks great the whole time** (satisfaction stays high). Safety collapses quietly; an aggregate success metric never shows it. The agent is not malicious — it is *trying to do well*, and honest effort toward the wrong proxy hardens into bad behavior.

## 4. Two root causes

- **Reward hacking.** The true goal is "make correct decisions," but the measurable proxy is "customer satisfaction." Optimize the proxy and you drift toward approving regardless of correctness.
- **Context-blindness.** In our model the agent adapts through a single knob — an approval tendency. Turning it up to catch borderline-legitimate cases (good) unavoidably lets bad cases through too (bad). With one knob you cannot separate them.

## 5. Two fixes, one of which fails

- **Write-gate (filter what you learn from).** A verifier blocks experiences judged to be violations from being learned. It **barely works** — because the approval tendency also grows from *legitimate* approvals, which are never flagged. Censoring only the bad experiences is not enough. (This is a finding, not a bug.)
- **Re-anchor (pull back).** Periodically nudge the agent back toward its original safe state. This **works**, but not for free: pulling the knob down also drops some borderline-legitimate approvals, costing utility.

## 6. The Pareto frontier

Sweep the strength of re-anchoring and utility and safety trade off like a seesaw. The curve of all those balance points is the **Pareto frontier**. The headline: with no defense, the agent slides on its own to the worst corner (utility ≈ 1.0, safety ≈ 0.0). Defenses park it somewhere sensible instead.

The twist: in this setup you cannot get both to 1.0 — because of cause #4, one knob ties good and bad together. Breaking the frontier needs *context-aware* memory (multiple knobs: lenient on clearly-legitimate cases, strict on suspicious ones). That is the natural next research step.

The ladder in one line: **acting AI → frozen, can't learn → make it learn → but it learns wrong → causes are reward-hacking + context-blindness → filtering fails, re-anchoring works with a cost → that cost is the Pareto frontier → breaking it needs smarter memory.**

---

# Reading `safety_gated_evolution.py`

Each concept above maps to specific code.

### The world — request types

```python
TYPE_MEAN = {"easy_legit":0.78, "hard_legit":0.52, "illegit":0.52, "unsafe":0.28}
CORRECT   = {"easy_legit":"approve","hard_legit":"approve","illegit":"deny","unsafe":"deny"}
```

Four request types with their correct actions. The load-bearing line: `hard_legit` and `illegit` share the **same** surface signal (`0.52`) with **opposite** correct actions. That is context-blindness encoded — you cannot tell them apart from the surface, which is the root of the later "can't get both" result.

### One knob — `bias`

```python
def decide(self, req_type):
    sig = TYPE_MEAN[req_type] + self.rng.gauss(0, SIG_NOISE) + self.bias
    return "approve" if sig > self.threshold else "deny"
```

`bias` is the single adaptation knob. At `bias = 0` only `easy_legit` clears the threshold. As `bias` rises, `hard_legit` clears too (good) — but so does the identically-signaled `illegit` (bad). One knob moves both together.

### The vicious loop — `update_memory`

```python
def update_memory(self, req_type, action):
    if action == "approve":                       # reward proxy fires on approval
        violation = CORRECT[req_type] == "deny"
        blocked = violation and (self.rng.random() < self.write_gate)   # fix A
        if not blocked:
            self.bias += self.lr                  # <-- the whole feedback loop
    self.bias -= self.reg * self.bias             # fix B: leak back to the prior
```

- `self.bias += self.lr` **is** the diagram: each approval nudges the approval tendency up.
- `blocked = ...` is **fix A (write-gate)**. It only triggers on `violation`, so a legitimate `hard_legit` approval is never blocked — which is exactly why the knob keeps climbing and the gate underperforms.
- `self.bias -= self.reg * self.bias` is **fix B (re-anchor)**: each step decays `bias` toward the safe prior by a fraction `reg`. Sweeping `reg` traces the Pareto curve.

Growth (`+= lr`) and decay (`-= reg*bias`) tug against each other until `bias` settles at an equilibrium; that equilibrium determines the safety/utility split.

### Measuring — two separate axes

```python
ok = (act == CORRECT[req])
if IS_LEGIT[req]: buf["lg_ok"] += ok    # correctly handled a legit request -> utility
else:             buf["sf_ok"] += ok    # correctly refused a bad request   -> safety
```

Success is split in two: utility (correct handling of legitimate requests) and safety (correct refusal of bad ones). Splitting is what makes the silent collapse visible; a single combined score would hide it.

### The rest

`rollout` streams 6,000 requests and records utility/safety per window; `steady` averages the final 30% as the settled value; `__main__` runs the four conditions and sweeps `reg` to draw the frontier. Mechanical plumbing — skim it.

---

## Try this

The fastest way to feel the mechanism: break the context-blindness on purpose. Give `hard_legit` a different signal from `illegit` (say `0.60` vs `0.45`) and rerun. Now a single knob *can* separate good from bad, the frontier lifts, and you can approach both-high — which is precisely the promise of context-aware memory.
