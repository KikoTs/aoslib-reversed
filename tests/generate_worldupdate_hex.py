
import sys
import os
import binascii

# Set path for shared module
sys.path.append(os.getcwd())

from shared import packet as packets
from shared import glm
# Mock enet
from unittest.mock import MagicMock
sys.modules['enet'] = MagicMock()

def generate_hex():
    print("Generating WorldUpdate packet hex...")
    
    # Create WorldUpdate packet
    wu = packets.WorldUpdate()
    wu.loop_count = 1
    
    # Add one player update
    # Data: (pos, orient, vel, ping, pong, hp, input, action, tool)
    # Using simple values to easily verify
    pos = (1.0, 2.0, 3.0)
    orient = (0.0, 1.0, 0.0)
    vel = (0.1, 0.2, 0.3)
    ping = 0.05
    pong = 0.05
    hp = 100
    inp = 0
    action = 0
    tool = 1
    
    wu[1] = (pos, orient, vel, ping, pong, hp, inp, action, tool)
    
    # Generate bytes
    writer = wu.generate()
    # Use raw bytes using the newly added __bytes__ method
    data = bytes(writer) 
    
    # Output hex
    hex_data = binascii.hexlify(data).decode('ascii').upper()
    print(f"HEX: {hex_data}")
    
    # Also write to file for the py2 script to read
    with open("worldupdate_hex.txt", "w") as f:
        f.write(hex_data)

if __name__ == "__main__":
    generate_hex()
