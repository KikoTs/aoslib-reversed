import sys
import os

# Add current directory to sys.path
sys.path.append(os.getcwd())

try:
    from shared import packet as packets
    
    if hasattr(packets, 'PositionData'):
        print("PositionData found")
        p = packets.PositionData()
        print("PositionData attributes:", [d for d in dir(p) if not d.startswith('__')])
        if hasattr(p, 'data'):
            print("p.data type:", type(p.data))
            print("p.data attributes:", [d for d in dir(p.data) if not d.startswith('__')])
        else:
            print("p has no 'data' attribute")
    else:
        print("PositionData NOT found in shared.packet")
        
except Exception as e:
    print(f"Error: {e}")
