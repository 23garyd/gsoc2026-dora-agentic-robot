# gsoc2026-dora-agentic-robot

GSOC 2026 | Agentic DORA — agent-driven framework for intelligent robot control, autonomous decision-making, and robotic task orchestration.

## Status

**Week 1 — UR5e MuJoCo simulation environment.** A reproducible MuJoCo scene
(UR5e 6-DOF arm + Robotiq 2F-85 gripper, red ball, green plate target) exposed as
a dora node. See **[docs/week1-simulation.md](docs/week1-simulation.md)**.

```bash
pip install -e .
bash scripts/fetch_ur5e_assets.sh                       # one-time: fetch meshes
dora up
MUJOCO_HEADLESS=1 dora start dataflows/ur5e_sim.yml
dora stop
```

Tests (no MuJoCo/dora/display required):

```bash
pip install -e ".[dev]"
PYTHONPATH=. pytest tests/ -q
```

## Layout

```
simulation/      UR5e MuJoCo node, named poses, scene model
dataflows/       dora dataflow configs
scripts/         asset fetch helper
tests/           unit tests
docs/            per-week deliverable notes
```
