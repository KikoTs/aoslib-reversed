import sys
import aoslib.world
import aoslib.vxl
import math

print("Starting physics verification...")

class MockMap:
    def get_solid(self, x, y, z):
        # Floor usually at z=0, but let's make a block at (10,10,0) inclusive?
        # Player at z=10.
        if z <= 0:
            return True
        return False

fails = 0

def check(name, condition, msg=""):
    global fails
    if condition:
        print("PASS: %s" % name)
    else:
        print("FAIL: %s - %s" % (name, msg))
        fails += 1

try:
    vxl = aoslib.vxl.VXL(-1, "test", 7, 2)
    world = aoslib.world.World(vxl)
    world.map = MockMap()
    
    # Test 1: Gravity
    player = aoslib.world.Player(world)
    player.position = (10.0, 10.0, 10.0)
    player.velocity = (0.0, 0.0, 0.0)
    player.airborne = True
    player.update(0.1)
    
    # Gravity = -32. Expected vz = -3.2
    check("Gravity", abs(player.velocity[2] + 3.2) < 0.01, "Vel Z: %f" % player.velocity[2])

    # Test 2: Movement
    player = aoslib.world.Player(world)
    player.position = (10.0, 10.0, 10.0)
    player.velocity = (0.0, 0.0, 0.0)
    player.airborne = False
    player.up = True
    player.orientation = (1.0, 0.0, 0.0) # +X
    # update calls move logic
    player.update(0.1)
    
    check("Movement X+", player.velocity[0] > 0, "Vel X: %f" % player.velocity[0])
    
    # Test 3: get_block_face_center_position (New Signature)
    # Args: (pos, face) where pos is (x,y,z)
    center = world.get_block_face_center_position((5, 5, 5), 0) # +X face of (5,5,5) -> (6.0, 5.5, 5.5)
    expected = (6.0, 5.5, 5.5)
    check("Face Center", center == expected, "Got %s" % str(center))
    
    # Test 4: Hitscan (New DDA)
    # Start (10,10,10) dir (0,0,-1) -> should hit floor at (10,10,0) dist 10
    # map has solid at z <= 0. 
    # hitscan checks solids. 
    # int(floor(10 + 0*t)) -> 10. int(floor(10 + 0*t)) -> 10. int(floor(10 - 1*t)).
    # t=9.0 -> z=1.0 (not solid). t=9.1 -> z=0.9 -> 0 (solid).
    # Wait, simple floor at z<=0.
    # Ray down from 10.
    # floor(z) = 0 is solid.
    # z hits 0.999... -> floor = 0.
    
    hit = world.hitscan((10.0, 10.0, 10.0), (0.0, 0.0, -1.0), 100.0)
    if hit:
        pos, normal, dist = hit
        # pos should be (10.5, 10.5, 0.5)? 
        # dist approx 9.5? 
        # Block (10,10,0) is solid. Top face is at z=1.0.
        # Ray starts at 10.0. Hits z=1.0. Dist = 9.0.
        check("Hitscan Hit", True)
        if hit:
             check("Hitscan Dist", abs(dist - 9.0) < 0.01, "Dist: %f" % dist)
    else:
        check("Hitscan Hit", False, "No hit")

except Exception as e:
    import traceback
    traceback.print_exc()
    fails += 1

sys.exit(fails)
