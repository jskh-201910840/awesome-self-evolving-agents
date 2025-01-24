"""
safety_gated_evolution.py
=========================
Experiment scaffold for Research Idea 1: "Safety-Gated Self-Evolution".

Reproduces *misevolution* (Shao et al., ICLR'26, arXiv:2509.26354): a self-evolving
service agent accumulates a context-blind "approve -> reward" correlation, so its
safety refusal rate collapses over time while task utility stays high.

Then it studies two mitigations and traces the UTILITY-vs-SAFETY frontier:
  (b) WRITE-GATE  : a verifier blocks *detected* policy-violating experiences from
                    being learned (strength w).
  (c) RE-ANCHOR   : a per-step safety-regularization that leaks the learned bias
                    back toward the prior (strength `reg`). This is the Pareto lever.

Realistic crux: hard-but-legit and policy-violating requests share the SAME surface
signal, and adaptation is a single context-blind scalar. So raising approvals to
catch hard-legit cases unavoidably approves violations too -> a genuine tradeoff.

Central findings this scaffold is built to expose:
  1. Unconstrained self-evolution overshoots to the WORST corner (safety ~ 0).
  2. Re-anchor BUYS safety back, but along a frontier -> a real utility cost.
  3. Write-gate alone slides you along the SAME frontier and mainly cuts *transient*
     harm; it cannot get both at once, because a context-blind channel ties them.
  => breaking the frontier needs context-aware / structured memory (follow-up work).

Offline & deterministic. Swap decide()/update_memory() for real LLM calls + memory.
Run: python3 safety_gated_evolution.py
"""
from __future__ import annotations
import random
from dataclasses import dataclass
import numpy as np
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt

TYPE_MEAN = {"easy_legit":0.78,"hard_legit":0.52,"illegit":0.52,"unsafe":0.28}
TYPE_PROB = {"easy_legit":0.35,"hard_legit":0.20,"illegit":0.30,"unsafe":0.15}
CORRECT   = {"easy_legit":"approve","hard_legit":"approve","illegit":"deny","unsafe":"deny"}
IS_LEGIT  = {"easy_legit":True,"hard_legit":True,"illegit":False,"unsafe":False}
SIG_NOISE = 0.09

def sample_request(rng):
    r,c = rng.random(),0.0
    for t,p in TYPE_PROB.items():
        c += p
        if r < c: return t
    return "unsafe"

@dataclass
class Agent:
    rng: random.Random
    bias: float = 0.0
    lr: float = 0.010
    threshold: float = 0.60
    write_gate: float = 0.0     # (b) verifier strength
    reg: float = 0.0            # (c) safety re-anchoring / regularization strength
    _t: int = 0
    unsafe_approvals: int = 0   # transient-harm counter

    def decide(self, req_type):
        sig = TYPE_MEAN[req_type] + self.rng.gauss(0,SIG_NOISE) + self.bias
        return "approve" if sig > self.threshold else "deny"

    def update_memory(self, req_type, action):
        self._t += 1
        if action == "approve":
            violation = CORRECT[req_type]=="deny"
            if violation: self.unsafe_approvals += 1
            blocked = violation and (self.rng.random() < self.write_gate)
            if not blocked:
                self.bias += self.lr                 # context-blind reinforcement
        self.bias -= self.reg * self.bias            # (c) leak toward prior (bounded eq.)

def rollout(agent, n=6000, seed=0, window=250):
    rng = random.Random(seed); hist=[]
    fresh=lambda:{"lg_ok":0,"lg_n":0,"sf_ok":0,"sf_n":0}; buf=fresh()
    for i in range(1,n+1):
        req=sample_request(rng); act=agent.decide(req); agent.update_memory(req,act)
        ok=(act==CORRECT[req])
        if IS_LEGIT[req]: buf["lg_n"]+=1; buf["lg_ok"]+=ok
        else:             buf["sf_n"]+=1; buf["sf_ok"]+=ok
        if i%window==0:
            hist.append((i,buf["lg_ok"]/max(1,buf["lg_n"]),
                           buf["sf_ok"]/max(1,buf["sf_n"]),agent.bias)); buf=fresh()
    return hist

def steady(factory, seed=0):
    a=factory(); h=rollout(a,seed=seed); tail=h[int(0.7*len(h)):]
    return (float(np.mean([x[1] for x in tail])),
            float(np.mean([x[2] for x in tail])), a.unsafe_approvals, h)

if __name__=="__main__":
    SEED=11
    conds={
        "no-defense (misevolve)": lambda: Agent(random.Random(SEED), reg=0.0),
        "write-gate w=0.8":       lambda: Agent(random.Random(SEED), reg=0.0, write_gate=0.8),
        "re-anchor reg=0.06":     lambda: Agent(random.Random(SEED), reg=0.06),
        "both":                   lambda: Agent(random.Random(SEED), reg=0.06, write_gate=0.8),
    }
    print("=== Steady-state (final 30%) + transient harm ===")
    print(f"{'condition':26s} {'utility':>8s} {'safety':>8s} {'unsafe_apr':>11s}")
    series={}
    for name,fac in conds.items():
        u,s,h_,hist=steady(fac,SEED); series[name]=hist
        print(f"{name:26s} {u:8.3f} {s:8.3f} {h_:11d}")

    fig,ax=plt.subplots(1,2,figsize=(12,4.2))
    for name,h in series.items():
        xs=[x[0] for x in h]
        ax[0].plot(xs,[x[2] for x in h],label=name); ax[1].plot(xs,[x[1] for x in h],label=name)
    ax[0].set_title("Safety (deny rate: illegit+unsafe)"); ax[1].set_title("Utility (approve rate: legit)")
    for a in ax: a.set_ylim(0,1.05); a.set_xlabel("interactions"); a.grid(alpha=.3); a.legend(fontsize=8)
    fig.tight_layout(); fig.savefig("timeseries.png",dpi=130)

    print("\n=== Pareto sweep (re-anchor reg), gate off vs on ===")
    regs=[0.30,0.20,0.14,0.10,0.075,0.055,0.04,0.028,0.018,0.010]
    fig2,axp=plt.subplots(figsize=(6.2,4.8))
    for gate,label,mk in [(0.0,"no write-gate","o"),(0.8,"write-gate w=0.8","s")]:
        us,ss=[],[]
        for reg in regs:
            u,s,_,_=steady(lambda reg=reg,gate=gate: Agent(random.Random(SEED),reg=reg,write_gate=gate),SEED)
            us.append(u); ss.append(s)
        axp.plot(us,ss,mk+"-",label=label,alpha=.85)
        print(f"  {label}: "+" ".join(f"({u:.2f},{s:.2f})" for u,s in zip(us,ss)))
    axp.scatter([1.0],[0.0],c="red",marker="X",s=120,zorder=5,label="unconstrained (overshoot)")
    axp.set_xlabel("Utility (legit approve rate)"); axp.set_ylabel("Safety (illegit/unsafe deny rate)")
    axp.set_title("Utility-Safety Pareto frontier\n(sweeping re-anchor strength)")
    axp.grid(alpha=.3); axp.legend(fontsize=8)
    fig2.tight_layout(); fig2.savefig("pareto_frontier.png",dpi=130)
    print("\nSaved: timeseries.png, pareto_frontier.png")
