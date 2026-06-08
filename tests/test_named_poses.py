"""Unit tests for named poses — run without MuJoCo, dora, or a display."""

import math

from simulation.named_poses import NAMED_POSES, SCENE_OBJECTS, NUM_JOINTS, get_pose

# UR5e joint limits (radians): elbow is +/- pi, the rest +/- 2*pi.
LIMITS = [
    (-2 * math.pi, 2 * math.pi),
    (-2 * math.pi, 2 * math.pi),
    (-math.pi, math.pi),
    (-2 * math.pi, 2 * math.pi),
    (-2 * math.pi, 2 * math.pi),
    (-2 * math.pi, 2 * math.pi),
]


def test_every_pose_has_six_floats():
    for name, joints in NAMED_POSES.items():
        assert len(joints) == NUM_JOINTS, f"{name} must have {NUM_JOINTS} joints"
        assert all(isinstance(j, (int, float)) for j in joints), name


def test_poses_within_joint_limits():
    for name, joints in NAMED_POSES.items():
        for i, (val, (lo, hi)) in enumerate(zip(joints, LIMITS)):
            assert lo <= val <= hi, f"{name} joint {i}={val} outside [{lo:.3f},{hi:.3f}]"


def test_expected_poses_present():
    for required in ("home", "above_ball", "grasp_ball", "lift", "above_plate", "place_plate"):
        assert required in NAMED_POSES


def test_get_pose_is_case_insensitive_and_copies():
    a = get_pose("HOME")
    b = get_pose("home")
    assert a == b == NAMED_POSES["home"]
    a[0] = 99.0  # mutating the result must not corrupt the table
    assert NAMED_POSES["home"][0] != 99.0


def test_get_pose_unknown_raises():
    try:
        get_pose("nonsense")
    except KeyError as e:
        assert "nonsense" in str(e)
    else:
        raise AssertionError("expected KeyError for unknown pose")


def test_scene_objects_positions():
    assert SCENE_OBJECTS["red_ball"]["position"] == [0.35, -0.25, 0.028]
    assert SCENE_OBJECTS["green_plate"]["position"] == [0.35, 0.25, 0.001]
