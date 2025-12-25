import sys
import os
sys.path.append(os.getcwd())
try:
    from shared import packet as packets
    
    if hasattr(packets, 'PositionData'):
        p = packets.PositionData()
        print("PositionData attrs:", [d for d in dir(p) if not d.startswith('__') and d not in ('read', 'write', 'generate', 'compress_packet', 'id')])

except Exception as e:
    print(e)
