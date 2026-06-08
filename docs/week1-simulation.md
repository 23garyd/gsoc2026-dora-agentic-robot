# Week 1 — UR5e MuJoCo Simulation Environment

**Goal (per the accepted proposal):** a reproducible MuJoCo simulation with a UR5e
6-DOF arm + Robotiq 2F-85 gripper and scene objects, exposed as a dora node with
sensor outputs and actuator inputs.

## What's included

| Path | Purpose |
|------|---------|
| `simulation/models/ur5e_scene.xml` | MuJoCo scene: UR5e arm + Robotiq 2F-85 gripper, red ball (dynamic), green plate target, `home` keyframe. Meshes referenced from `ur5e_assets/` (fetched, not vendored). |
| `simulation/mujoco_node.py` | dora node: steps physics, applies `control_input` (arm) and `gripper_ctrl`, publishes `joint_positions`, `joint_velocities`, `sensor_data`. Headless-capable. |
| `simulation/named_poses.py` | FK-verified named joint configs (home, above_ball, grasp_ball, lift, above_plate, place_plate) and scene-object world positions. |
| `dataflows/ur5e_sim.yml` | Sim-only dataflow (10 ms timer drives stepping). |
| `scripts/fetch_ur5e_assets.sh` | Fetches the ~33 MB UR5e + Robotiq meshes from MuJoCo Menagerie. |
| `tests/` | 11 unit tests (poses + scene XML structure) that run without MuJoCo/dora. |

## Robot & scene

- **UR5e** — 6 position actuators (indices 0–5): shoulder_pan, shoulder_lift, elbow, wrist_1/2/3.
- **Robotiq 2F-85** — tendon-coupled gripper on actuator index 6 (`ctrlrange 0–255`, 0=open … 255=closed); physics-based grasping via friction (no weld constraints).
- **Red ball** — dynamic body with a `freejoint` at world `(0.35, -0.25, 0.028)`.
- **Green plate** — target marker `site` at world `(0.35, 0.25, 0.001)`. (It is a visual/target site, not a freejoint body.)
- The UR5e base carries `quat="0 0 0 -1"` (180° about Z), so the robot frame is rotated relative to the MuJoCo world frame — this is why the named poses look "mirrored".

## Run it

```bash
pip install -e .                      # mujoco, numpy, pyarrow, dora-rs
bash scripts/fetch_ur5e_assets.sh     # one-time: fetch meshes into simulation/models/ur5e_assets/
dora up
MUJOCO_HEADLESS=1 dora start dataflows/ur5e_sim.yml   # drop HEADLESS to open the viewer
dora stop
```

## Tests

```bash
pip install -e ".[dev]"
PYTHONPATH=. pytest tests/ -q          # 11 passed — no MuJoCo/dora/display required
```

## Validation status

- ✅ Named-pose and scene-XML structure tests pass (no simulator needed).
- ✅ Model XML vendored from the proven `dora-moveit2` UR5e demo (same author); FK-verified joint configs carried over from that demo.
- ⚠️ The physics sim (`mujoco_node.py` end-to-end) was **not executed in the authoring environment** — MuJoCo is not installed there. It needs a reviewer run after `fetch_ur5e_assets.sh`. The node code mirrors the working `dora-mujoco` node it is adapted from.

## Next (Week 2)

Tune the Robotiq 2F-85 friction/force/contact for reliable grasping and add the
`gripper_controller` node (`gripper_command` → `gripper_ctrl`).
