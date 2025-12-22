# Discover VXL add_point API
import os
import sys
os.chdir('aosdump')
import aoslib.vxl as vxl

m = vxl.VXL(-1, '', 0, 2)

# Try different argument patterns
patterns = [
    # Single tuple
    ((100, 100, 32, 0xFF0000),),
    # List of tuples  
    ([(100, 100, 32, 0xFF0000)],),
    # Separate x,y,z and color
    ((100, 100, 32), 0xFF0000),
    # Two tuples - point and color
    ((100, 100, 32), (255, 0, 0)),
    # Array-like with shape
    ([100, 100, 32, 0xFF0000],),
]

for i, args in enumerate(patterns):
    try:
        result = m.add_point(*args)
        print("SUCCESS pattern %d: %s -> %s" % (i, args, result))
    except TypeError as e:
        print("FAIL pattern %d: %s -> %s" % (i, args, str(e)[:60]))
    except Exception as e:
        print("ERROR pattern %d: %s -> %s" % (i, args, str(e)[:60]))

# Check what other methods look like
print("\n--- Method comparison ---")
for name in ['get_point', 'get_color', 'get_solid', 'color_block']:
    try:
        method = getattr(m, name)
        result = method(0, 0, 0)
        print("%s at 0,0,0: %s" % (name, result))
    except Exception as e:
        print("%s failed: %s" % (name, str(e)[:50]))
