
import sys
import os

# Add local directory to path to ensure we load local aoslib
sys.path.insert(0, os.getcwd())

try:
    from aoslib.world import World, Player
    from aoslib.vxl import VXL
    print("Import successful!")
except ImportError as e:
    print(f"Import failed: {e}")
    sys.exit(1)

def test_gravity():
    # Create empty map
    vxl = VXL()
    # Fill bottom layer with solid to catch player? Or just check gravity in air
    # VXL is 512x512x64. Z=63 is bottom.
    
    world = World(vxl)
    player = Player(world)
    
    # Set high up (low Z value, e.g. 10)
    player.set_position(256, 256, 10.0)
    player.set_velocity(0, 0, 0)
    
    # Set multipliers (needed since logic uses them)
    # They should be set by default in __init__
    
    print(f"Initial Pos: {player.position}")
    print(f"Initial Vel: {player.velocity}")
    
    dt = 0.03
    # Run a few updates
    # Run enough updates to hit the bottom (approx 64 units)
    # Gravity is increasing velocity.
    for i in range(300):
        player.update(dt)
        # print(f"Update {i+1}: Pos={player.position}, Vel={player.velocity}, Airborne={player.airborne}")
        if player.fall_damage_this_frame > 0:
            print(f"Detected Fall Damage: {player.fall_damage_this_frame}")
            # Simulate server logic
            if player.fall_damage_this_frame >= 100:
                player.dead = True
                print("Player Killed by Fall Damage (Simulated)")
        
        if player.position[2] >= 61 and player.velocity[2] == 0:
            print(f"Hit ground at iteration {i}!")

            break
        if player.dead:
            print("Player DIED from fall damage!")
            break
            
    # Check final state
    z_final = player.position[2]
    print(f"Final Z: {z_final}")
    if player.dead:
         print("SUCCESS: Player died.")
    elif z_final > 10.0:
        print("SUCCESS: Player fell down (Z increased)")
    else:
        print("FAILURE: Player did not fall")

if __name__ == "__main__":
    test_gravity()
