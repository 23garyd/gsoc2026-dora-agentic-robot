"""Structural checks on the MuJoCo scene XML — no MuJoCo needed (pure XML parse)."""

import xml.etree.ElementTree as ET
from pathlib import Path

import pytest

SCENE = Path(__file__).resolve().parents[1] / "simulation" / "models" / "ur5e_scene.xml"


@pytest.fixture(scope="module")
def root():
    return ET.parse(SCENE).getroot()


def test_scene_is_well_formed(root):
    assert root.tag == "mujoco"


def test_red_ball_is_a_freejoint_body(root):
    ball = next((b for b in root.iter("body") if b.get("name") == "red_ball"), None)
    assert ball is not None, "red_ball body missing"
    assert ball.find("freejoint") is not None, "red_ball must have a freejoint"
    assert ball.get("pos", "").startswith("0.35 -0.25")


def test_green_plate_target_site_present(root):
    site = next((s for s in root.iter("site") if s.get("name") == "place_target"), None)
    assert site is not None, "green plate target site missing"
    assert site.get("pos", "").startswith("0.35 0.25")


def test_home_keyframe_present(root):
    keys = [k.get("name") for k in root.iter("key")]
    assert "home" in keys


def test_gripper_actuator_index_six(root):
    # Arm has 6 position actuators (indices 0..5); the gripper is actuator 6.
    actuators = [a for parent in root.iter("actuator") for a in list(parent)]
    assert len(actuators) >= 7, f"expected >=7 actuators, got {len(actuators)}"
