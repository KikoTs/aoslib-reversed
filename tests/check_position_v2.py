import sys
import os
sys.path.append(os.getcwd())
try:
    from shared import packet as packets
    
    # Check PositionData
    if hasattr(packets, 'PositionData'):
        p = packets.PositionData()
        if hasattr(p, 'data'):
            d_attrs = dir(p.data)
            print(f"PositionData.data has xyz: {'xyz' in d_attrs}, has x: {'x' in d_attrs}")
        else:
            print("PositionData has no data")
            
    # Check BlockBuild
    if hasattr(packets, 'BlockBuild'):
        b = packets.BlockBuild()
        attrs = dir(b)
        print(f"BlockBuild has xyz: {'xyz' in attrs}, has x: {'x' in attrs}")
        
    # Check BlockLine
    if hasattr(packets, 'BlockLine'):
        l = packets.BlockLine()
        attrs = dir(l)
        print(f"BlockLine has xyz1: {'xyz1' in attrs}, has x1: {'x1' in attrs}")
        
except Exception as e:
    print(e)
