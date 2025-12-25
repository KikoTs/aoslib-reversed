import sys
import os

# Set the root directory based on Python version
if sys.version_info[0] < 3:
    # For Python 2, set "aosdump" as root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.join(script_dir, "aosdump")
    os.chdir(root_dir)
    sys.path.insert(0, root_dir)
else:
    # For Python 3+, use current directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, script_dir)

from shared import packet
from shared.bytes import ByteReader

def hex_to_bytes(hex_str):
    return bytearray.fromhex(hex_str.replace(' ', ''))

def find_packet_class(packet_id):
    for attr in dir(packet):
        obj = getattr(packet, attr)
        # Check if it's a class and has an 'id' attribute
        if isinstance(obj, type) and hasattr(obj, 'id'):
            if obj.id == packet_id:
                return obj
    return None

def main():
    # Working hex from real server
    hex_str = "0F 02 00 00 00 4B 69 6B 6F 54 73 00"
    
    data = hex_to_bytes(hex_str)
    packet_id = data[0] if isinstance(data[0], int) else ord(data[0])
    
    print("Packet ID: {} (0x{:02X})".format(packet_id, packet_id))
    
    PacketClass = find_packet_class(packet_id)
    if not PacketClass:
        print("Could not find packet class with ID {}".format(packet_id))
        return

    print("Found Packet Class: {}".format(PacketClass.__name__))
    
    # Initialize reader with data, skipping the first byte (ID)
    # ByteReader expects raw bytes (or string that it encodes, but here we prefer passing bytes if supported or careful string)
    # Looking at ByteReader.__cinit__:
    # if isinstance(data, str): encode... else: self.data = data
    # So we can pass bytes directly.
    
    # We must pass the FULL data to ByteReader, but we advance the position past the ID manually
    # OR we pass the slice.
    # The current StateData fix suggests passing the full stream and reading the byte.
    # Let's verify how test_packets did it: reader = ByteReader(str(writer)); reader.read_byte()
    
    # In Py3, str(writer) might return the string representation.
    # ByteReader accepts 'str' or bytes.
    # If we pass bytes:
    # ByteReader in Python 2 expects a string, Python 3 expects bytes
    if sys.version_info[0] < 3:
        data = str(data)
    else:
        data = bytes(data)
    reader = ByteReader(data)
    reader.read_byte() # Consume ID
    
    pkt = PacketClass()
    try:
        pkt.read(reader)
        print("\n=== Decoded Packet Data ===")
        for attr in sorted(dir(pkt)):
            if attr.startswith("_") or attr in ('read', 'write', 'data', 'id', 'compress_packet') or callable(getattr(pkt, attr)):
                continue
            val = getattr(pkt, attr)
            print("{}: {}".format(attr, val))
    except Exception as e:
        print("Error reading packet: {}".format(e))

if __name__ == "__main__":
    main()
