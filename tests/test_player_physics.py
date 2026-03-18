import os
import sys
import unittest


IS_PY2 = sys.version_info[0] < 3
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(SCRIPT_DIR)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

import aoslib.vxl as vxl
import aoslib.world as world
from shared import glm


def make_blank_map():
    return vxl.VXL(-1, b"", 0, 2)


def fill_floor(map_obj, z_level, x_range, y_range, color=(90, 90, 90)):
    for x in x_range:
        for y in y_range:
            map_obj.set_point(x, y, z_level, color)


class TestPlayerPhysics(unittest.TestCase):
    def setUp(self):
        self.map = make_blank_map()
        fill_floor(self.map, 12, range(0, 16), range(0, 16))
        self.world = world.World(self.map)
        self.player = world.Player(self.world)
        self.player.set_position(4.5, 4.5, 9.3)
        self.player.set_velocity(0.0, 0.0, 0.0)
        self.player.set_orientation(glm.Vector3(1.0, 0.0, 0.0))
        self.world.set_gravity(1.0)

    def test_walk_acceleration_forward(self):
        self.player.set_walk(True, False, False, False)
        result = self.player.update(0.1, [])
        self.assertEqual(result, 0)
        self.assertGreater(self.player.velocity.x, 0.0)
        self.assertAlmostEqual(self.player.velocity.y, 0.0, places=5)

    def test_jump_impulse_sets_airborne(self):
        self.player.jump = True
        result = self.player.update(0.1, [])
        self.assertEqual(result, 0)
        self.assertTrue(self.player.airborne)
        self.assertLess(self.player.velocity.z, 0.0)

    def test_crouch_and_uncrouch_shift(self):
        self.player.set_position(5.0, 5.0, 5.0)
        self.player.set_crouch(True, [], 0)
        self.assertTrue(self.player.crouch)
        self.assertAlmostEqual(self.player.position.z, 5.9, places=5)

        self.player.set_crouch(False, [], 0)
        self.assertFalse(self.player.crouch)
        self.assertAlmostEqual(self.player.position.z, 5.0, places=5)

    def test_hitscan_hits_block(self):
        self.map.set_point(4, 4, 4, (10, 20, 30))
        hit = self.world.hitscan(glm.Vector3(4.5, 4.5, 0.0), glm.Vector3(0.0, 0.0, 1.0))
        accurate = self.world.hitscan_accurate(
            glm.Vector3(4.5, 4.5, 0.0), glm.Vector3(0.0, 0.0, 1.0), 10.0, False
        )
        self.assertEqual(hit[0].xyz, (4, 4, 4))
        self.assertEqual(hit[1], 4)
        self.assertEqual(accurate[1].xyz, (4, 4, 4))
        self.assertEqual(accurate[2], 4)
        self.assertAlmostEqual(accurate[0].z, 4.0, places=5)

    def test_check_valid_position_bounds(self):
        self.assertTrue(self.player.check_valid_position(glm.Vector3(0.0, 0.0, 0.0)))
        self.assertFalse(self.player.check_valid_position(glm.Vector3(-1.0, 0.0, 0.0)))
        self.assertFalse(self.player.check_valid_position(glm.Vector3(0.0, -1.0, 0.0)))
        self.assertFalse(self.player.check_valid_position(glm.Vector3(512.0, 0.0, 0.0)))
        self.assertFalse(self.player.check_valid_position(glm.Vector3(0.0, 512.0, 0.0)))
        self.assertTrue(self.player.check_valid_position(glm.Vector3(0.0, 0.0, -1.0)))
        self.assertTrue(self.player.check_valid_position(glm.Vector3(0.0, 0.0, 240.0)))

    def test_lock_box_clamps_position(self):
        self.player.set_locked_to_box((4.0, 4.0, 8.0, 5.0, 5.0, 10.0))
        self.player.set_velocity(10.0, 10.0, 0.0)
        self.player.update(0.1, [])
        self.assertGreaterEqual(self.player.position.x, 4.0)
        self.assertGreaterEqual(self.player.position.y, 4.0)
        self.assertLessEqual(self.player.position.x, 5.0)
        self.assertLessEqual(self.player.position.y, 5.0)


if __name__ == "__main__":
    if IS_PY2:
        print("[SKIP] test_player_physics.py is Python 3 only.")
        sys.exit(0)
    unittest.main(verbosity=2)
