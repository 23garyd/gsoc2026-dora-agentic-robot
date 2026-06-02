#!/usr/bin/env bash
# Fetch the UR5e + Robotiq 2F-85 mesh assets from MuJoCo Menagerie.
#
# The robot model (simulation/models/ur5e_scene.xml) is vendored as text, but the
# ~33 MB of binary meshes it references are not committed. This script populates
# simulation/models/ur5e_assets/ from google-deepmind/mujoco_menagerie.
#
# Usage:  bash scripts/fetch_ur5e_assets.sh
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ASSETS="$ROOT/simulation/models/ur5e_assets"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT

echo "Cloning MuJoCo Menagerie (shallow)…"
git clone --depth 1 https://github.com/google-deepmind/mujoco_menagerie.git "$TMP/menagerie"

mkdir -p "$ASSETS"

# UR5e arm meshes (.obj)
cp "$TMP/menagerie/universal_robots_ur5e/assets/"*.obj "$ASSETS/"
# Robotiq 2F-85 gripper meshes (.stl)
cp "$TMP/menagerie/robotiq_2f85/assets/"*.stl "$ASSETS/"

echo "Fetched $(ls "$ASSETS" | wc -l | tr -d ' ') mesh files into $ASSETS"
echo "Done. You can now run:  dora up && MUJOCO_HEADLESS=1 dora start dataflows/ur5e_sim.yml"
