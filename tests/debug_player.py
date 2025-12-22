import sys
import aoslib.world
import aoslib.vxl

print("Starting debug...")

class MockMap:
    def get_solid(self, x, y, z):
        print("MockMap.get_solid called with", x, y, z)
        return False

try:
    print("Creating VXL...")
    vxl = aoslib.vxl.VXL(-1, "test", 7, 2)
    print("Creating World...")
    world = aoslib.world.World(vxl)
    
    print("Setting MockMap...")
    world.map = MockMap()
    
    print("Creating Player...")
    player = aoslib.world.Player(world)
    player.position = (10.0, 10.0, 10.0)
    
    print("Updating Player...")
    player.update(0.1)
    
    print("Debug complete!")
except Exception as e:
    import traceback
    traceback.print_exc()
