# Universal Dissipative System Architecture

## What this is
One computational model for any dissipative system. Cancer, organisation, climate, star, cell.
Two interaction modes: HOLD (understand) and CROSS (intervene).
Every insight from any domain feeds one structure.

## Files
```
architecture.py    # The engine. One System class. diagnose() = HOLD. intervene() = CROSS.
AXIOMS.md          # 12 axioms. If the engine is lost, rebuild from this. 
CLAUDE.md          # This file. Read first every conversation.
```

## The core formula
M_eff = M × (1 − D) / (1 + D)
- M: raw potency. D: conservation drain.
- Numerator: what the agent loses. Denominator: what the opponent gains.
- Applies to every agent in every system. Drug, person, policy, force.

## Architecture
- `System`: any dissipative system. Has position (1-64), agents, parallel cycles.
- `Agent`: any intervention function. Has function, potency, subphase, drain.
- `System.diagnose()`: HOLD mode. Position, health, speed, stress, observers.
- `System.intervene()`: CROSS mode. Strike order, supportive care, overstayed agents.
- `System.frontend()`: both modes + structural metadata for UI.

## Key rules
- Every structural element carries its axiom reference, description, and domain examples.
- Every new insight goes into architecture.py AND AXIOMS.md.
- The 12 axioms are numbered A0-A12. Reference by number.
- Agent functions are FUNCTIONS not titles. Sentinel, Miner, Architect, Catalyst, Observer.
- Domain constructors (cancer_system, org_system, climate_system) are convenience wrappers. The System class is universal.

## Validated against
- Crawford et al. (NSCLC RDI): predicted HR 1.10, observed 1.19 (CI 1.04-1.37)
- G-CSF meta-analysis: predicted RR 0.96, observed 0.93 (CI 0.90-0.96)
- DCRP: 35 evidence entries across 7 cancer types, 0.6% MAE
