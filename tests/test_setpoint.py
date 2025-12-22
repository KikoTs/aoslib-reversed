# Test set_point API
import os
os.chdir('aosdump')
import aoslib.vxl as v

m = v.VXL(-1,'',0,2)

print("Testing set_point patterns...")
print("Before: solid=%s color=%s" % (m.get_solid(100,100,32), hex(m.get_color(100,100,32))))

# Pattern from IDA: set_point(int, int, int, MapData*, bool, int)
# Python should be: set_point(x, y, z, ???, ???)

# The 4-arg version with RGBA tuple seemed to not error
try:
    result = m.set_point(100, 100, 32, (255, 0, 0, 255))
    print("set_point(100,100,32,(255,0,0,255)) returned: %s" % result)
    print("After: solid=%s color=%s" % (m.get_solid(100,100,32), hex(m.get_color(100,100,32))))
except Exception as e:
    print("FAILED: %s" % e)

# Also try remove_point to understand the inverse
print("\n\nTesting remove_point...")
try:
    result = m.remove_point(100, 100, 32)
    print("remove_point(100,100,32) returned: %s" % result)
except Exception as e:
    print("remove_point failed: %s" % e)
