# Layer7 — Universal Dissipative System Tool

Seven layers of intervention on any dissipative system.
Generative Geometry (van der Klein, 2026)

## The Seven Layers

1. **Position** — where is the system in its cycle
2. **Sub-phase** — what is happening here (Signal/Structure/Encounter/Conservation)
3. **Agent** — who/what covers each sub-phase
4. **Parameters** — potency, drain, overstay, depth
5. **Combination** — coverage × health = product of blockades
6. **Move** — the best next structural intervention
7. **Execution** — getting the agent to make the move

## The Loop

HOLD (L1-L5) → MOVE (L6) → LAUNCH (L7) → observe result → HOLD again

## Structure

- `layer7.py` — computation engine, domain registry, all formulas
- `app.py` — Flask API serving the loop
- `static/layer7.html` — frontend (display only, all computation via API)
- `calibration_db.json` — cancer agent calibration data (113 agents, 7 types)

## Domains

- **Organisation** — 64 binary events, 16 challenges, 4096 noun engine
- **Cancer** — 16 lifecycle events, 113 calibrated drug agents from DCRP

## Run locally

```
pip install flask
python app.py
# Open http://localhost:5000/layer7
```

## Deploy (Render)

Push to GitHub. Connect to Render. Uses `render.yaml` for configuration.

## The Formula

M_eff = M × (1−D) / (1+D)

One formula. Any agent. Any system.
