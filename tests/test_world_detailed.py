#!/usr/bin/env python3

import sys
import aoslib.world 
import shared.glm
import aoslib.vxl

print("Testing world module implementation...")
print(f"aoslib.world module: {aoslib.world}")

# Test VXL creation (matching original constructor)
print("\n1. Creating VXL object...")
try:
    vxl = aoslib.vxl.VXL(-1, "sadwasd", 7, 2)
    print(f"✓ VXL created: {vxl}")
except Exception as e:
    print(f"✗ VXL creation failed: {e}")
    sys.exit(1)

# Test World creation
print("\n2. Creating World object...")
try:
    world = aoslib.world.World(vxl)
    print(f"✓ World created: {world}")
    print(f"  World.map: {world.map}")
    print(f"  World.timer: {world.timer}")
except Exception as e:
    print(f"✗ World creation failed: {e}")
    sys.exit(1)

# Test Player creation
print("\n3. Creating Player object...")
try:
    player = aoslib.world.Player(world)
    print(f"✓ Player created: {player}")
except Exception as e:
    print(f"✗ Player creation failed: {e}")
    sys.exit(1)

# Test Player attributes
print("\n4. Testing Player attributes...")
try:
    print(f"  player.deleted: {player.deleted}")
    print(f"  player.position: {player.position}")
    print(f"  player.velocity: {player.velocity}")
    print(f"  player.orientation: {player.orientation}")
    print(f"  player.airborne: {player.airborne}")
    print(f"  player.crouch: {player.crouch}")
    print("✓ Player attributes accessible")
except Exception as e:
    print(f"✗ Player attribute access failed: {e}")

# Test Player methods
print("\n5. Testing Player methods...")
try:
    # Test orientation setting
    player.set_orientation(shared.glm.Vector3(0, 0, 0))
    print(f"✓ set_orientation called, result: {player.orientation}")
    
    # Test position setting
    player.set_position(0, 0, 0)
    print(f"✓ set_position called, result: {player.position}")
    
    # Test velocity setting
    player.set_velocity(0, 0, 0)
    print(f"✓ set_velocity called, result: {player.velocity}")
    
except Exception as e:
    print(f"✗ Player method calls failed: {e}")

# Test other classes
print("\n6. Testing other classes...")
try:
    # Test PlayerMovementHistory
    history = aoslib.world.PlayerMovementHistory()
    print(f"✓ PlayerMovementHistory created: {history}")
    
    # Test Grenade
    grenade = aoslib.world.Grenade(world)
    print(f"✓ Grenade created: {grenade}")
    
    # Test GenericMovement
    movement = aoslib.world.GenericMovement(world)
    print(f"✓ GenericMovement created: {movement}")
    
    # Test FallingBlocks
    falling = aoslib.world.FallingBlocks(world)
    print(f"✓ FallingBlocks created: {falling}")
    
    # Test Debris
    debris = aoslib.world.Debris(world)
    print(f"✓ Debris created: {debris}")
    
    # Test ControlledGenericMovement
    controlled = aoslib.world.ControlledGenericMovement(world)
    print(f"✓ ControlledGenericMovement created: {controlled}")
    
except Exception as e:
    print(f"✗ Other class creation failed: {e}")

# Test module-level functions
print("\n7. Testing module-level functions...")
try:
    result = aoslib.world.A2("test")
    print(f"✓ A2 function: {result}")
    
    result = aoslib.world.cube_line(1, 2, 3)
    print(f"✓ cube_line function: {result}")
    
    result = aoslib.world.floor(3.7)
    print(f"✓ floor function: {result}")
    
    result = aoslib.world.get_next_cube(1, 2)
    print(f"✓ get_next_cube function: {result}")
    
    result = aoslib.world.get_random_vector()
    print(f"✓ get_random_vector function: {result}")
    
    result = aoslib.world.is_centered("test")
    print(f"✓ is_centered function: {result}")
    
    result = aoslib.world.parse_constant_overrides("test")
    print(f"✓ parse_constant_overrides function: {result}")
    
except Exception as e:
    print(f"✗ Module function calls failed: {e}")

print("\n8. Testing World methods...")
try:
    gravity = world.get_gravity()
    print(f"✓ get_gravity: {gravity}")
    
    world.set_gravity(-35.0)
    print("✓ set_gravity called")
    
    world.update(0.016)  # 60 FPS
    print(f"✓ update called, timer: {world.timer}")
    
except Exception as e:
    print(f"✗ World method calls failed: {e}")

print("\n✓ All tests completed!") 