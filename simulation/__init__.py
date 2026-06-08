"""UR5e + Robotiq 2F-85 MuJoCo simulation for the Agentic DORA project (Week 1).

Exposes the simulation as a dora node (`mujoco_node`) with FK-verified named
poses (`named_poses`) and scene objects (red ball, green plate).
"""

from .named_poses import NAMED_POSES, SCENE_OBJECTS, NUM_JOINTS, get_pose

__all__ = ["NAMED_POSES", "SCENE_OBJECTS", "NUM_JOINTS", "get_pose"]
