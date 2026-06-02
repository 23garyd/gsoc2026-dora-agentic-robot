"""FK-verified named joint configurations for the UR5e arm.

Joint order: [shoulder_pan, shoulder_lift, elbow, wrist_1, wrist_2, wrist_3] (radians).

The end-effector positions below were verified with MuJoCo forward kinematics on
`models/ur5e_scene.xml` (UR5e base has quat="0 0 0 -1", a 180 deg Z rotation, so
the robot frame is rotated relative to the MuJoCo world frame). Object positions in
the world frame: red ball at (0.35, -0.25, 0.028), green plate at (0.35, 0.25, 0.001).
"""

from __future__ import annotations

NUM_JOINTS = 6

# name -> 6 joint values (radians)
NAMED_POSES: dict[str, list[float]] = {
    "home":        [-1.5708, -1.5708,  1.5708, -1.5708, -1.5708, 0.0],
    "upright":     [ 0.0,    -1.5708,  0.0,    -1.5708,  0.0,    0.0],
    "zero":        [ 0.0,     0.0,     0.0,     0.0,     0.0,    0.0],
    "above_ball":  [ 2.2045, -1.6635,  2.1416, -2.049,  -1.5708, 0.0],
    "grasp_ball":  [ 2.2045, -1.4535,  2.3026, -2.4199, -1.5708, 0.0],
    "lift":        [ 2.2045, -1.7505,  1.944,  -1.7642, -1.5708, 0.0],
    "above_plate": [ 3.445,  -1.7505,  1.944,  -1.7642, -1.5708, 0.0],
    "place_plate": [ 3.445,  -1.4869,  2.326,  -2.4099, -1.5708, 0.0],
}

# Scene object positions in the MuJoCo world frame (meters).
SCENE_OBJECTS: dict[str, dict] = {
    "red_ball":    {"type": "sphere",   "position": [0.35, -0.25, 0.028], "radius": 0.03,
                    "rgba": [0.9, 0.1, 0.1, 1.0]},
    "green_plate": {"type": "cylinder", "position": [0.35,  0.25, 0.001], "radius": 0.05,
                    "rgba": [0.1, 0.9, 0.1, 1.0]},
}


def get_pose(name: str) -> list[float]:
    """Return the joint configuration for a named pose.

    Raises KeyError with the list of valid names if the pose is unknown.
    """
    key = name.lower().strip()
    if key not in NAMED_POSES:
        raise KeyError(f"unknown pose '{name}'. Known poses: {sorted(NAMED_POSES)}")
    return list(NAMED_POSES[key])
