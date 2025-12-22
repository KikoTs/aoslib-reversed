import unittest
import sys
import os

# Ensure aoslib is importable
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import aoslib.world
import shared.glm

class MockMap:
    def get_solid(self, x, y, z):
        # Create a simple floor at z=0
        if z <= 0:
            return True
        return False

class TestPlayerPhysics(unittest.TestCase):
    def setUp(self):
        # Setup world and player
        self.vxl = aoslib.vxl.VXL(-1, "test", 7, 2)
        self.world = aoslib.world.World(self.vxl)
        self.world.map = MockMap() # Override map for testing
        self.player = aoslib.world.Player(self.world)
        self.player.position = (10.0, 10.0, 10.0)
        self.player.velocity = (0.0, 0.0, 0.0)

    def test_gravity_application(self):
        # Test that gravity is applied correctly
        # Assuming gravity is -32.0 (default)
        # Verify dt usage
        initial_vz = self.player.velocity[2]
        self.player.airborne = True
        self.player.update(0.1)
        expected_vz = initial_vz + (-32.0 * 0.1)
        self.assertAlmostEqual(self.player.velocity[2], expected_vz, places=4)

    def test_movement_acceleration(self):
        # Test basic movement
        self.player.up = True # Press forward
        self.player.orientation = (1.0, 0.0, 0.0) # Facing +X
        self.player.airborne = False
        
        # Initial update 
        self.player.update(0.1)
        
        # Check if velocity increased in +X
        vx = self.player.velocity[0]
        self.assertGreater(vx, 0.0)
        
    def test_friction(self):
        # Set velocity and ensure it decreases when no input
        self.player.velocity = (10.0, 0.0, 0.0)
        self.player.up = False
        self.player.airborne = False
        
        self.player.update(0.1)
        
        vx = self.player.velocity[0]
        self.assertLess(vx, 10.0)
        self.assertGreater(vx, 0.0)
        
    def test_jump(self):
        self.player.jump = True
        self.player.airborne = False
        # Need to simulate jump logic frame
        # Player usually sets jump_this_frame = True on input
        self.player.jump_this_frame = True 
        
        self.player.update(0.1)
        
        self.assertTrue(self.player.airborne)
        self.assertGreater(self.player.velocity[2], 0.0)

if __name__ == '__main__':
    try:
        unittest.main(verbosity=2, buffer=False)
    except Exception as e:
        import traceback
        traceback.print_exc()
        sys.exit(1)
