
import sys
import os
import binascii

# Setup path to import from aosdump
script_dir = os.path.dirname(os.path.abspath(__file__))
aosdump_dir = os.path.join(script_dir, "aosdump")

if not os.path.exists(aosdump_dir):
    print "Error: aosdump directory not found at", aosdump_dir
    sys.exit(1)

sys.path.insert(0, aosdump_dir)

# Import original packet and ByteReader
import shared.packet as packet
from shared.bytes import ByteReader

# Mock proxy.packet because aosdump/shared/packet.py imports it
# We need to simulate the environment enough for it to load
import imp
proxy_module = imp.new_module("proxy")
proxy_packet = imp.new_module("proxy.packet")
sys.modules["proxy"] = proxy_module
sys.modules["proxy.packet"] = proxy_packet
# We need to inject WorldUpdate into proxy.packet so shared.packet can inherit/use it if needed
# Actually shared/packet.py likely defines WorldUpdate inheriting from proxy or similar
# Let's inspect shared/packet.py logic if it fails.
# Based on previous runs, it seemed to work via proxy initialization.

# Define a Debug classes to inspect reading
class DebugWU(packet.WorldUpdate):
    def read(self, reader):
        print "DEBUG: WorldUpdate.read called."
        super(DebugWU, self).read(reader)
        print "Successfully decoded WorldUpdate!"
        # Print some values
        print "Loop count:", hasattr(self, 'loop_count') and self.loop_count or "N/A"
        try:
             print "Player updates:", self.player_updates
        except:
             pass

# Monkey patch packet.WorldUpdate
packet.WorldUpdate = DebugWU

def test_decode():
    try:
        with open("worldupdate_hex.txt", "r") as f:
            hex_data = f.read().strip()
    except:
        print "Error: worldupdate_hex.txt not found. Run generate_worldupdate_hex.py first."
        return

    print "Hex Data:", hex_data
    try:
        data = binascii.unhexlify(hex_data)
    except:
        print "Error: Invalid hex data"
        return
        
    reader = ByteReader(data)
    
    # Read Packet ID (1 byte)
    try:
        pid = reader.read_byte()
        print "Packet ID:", pid
    except Exception as e:
        print "Failed to read Packet ID:", e
        return

    wu = packet.WorldUpdate()
    try:
        wu.read(reader)
    except Exception as e:
        print "Failed to decode WorldUpdate:", e
        import traceback
        traceback.print_exc()
        
    if reader.data_left():
        print "WARNING: Data left after reading!"
    else:
        print "SUCCESS: Packet consumed exactly."

if __name__ == "__main__":
    # Initialize packet proxy stub if needed
    # The aosdump/shared/packet.py seems to register packets. 
    # We might need to call initializer if it exists.
    if hasattr(packet, 'initializer'):
        print "Initializing proxy for Packet functions..."
        packet.initializer()
        print "Packet proxy initialization complete!"
        
    test_decode()
