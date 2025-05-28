import os, sys
import unittest

# This runs for both python 2 and 3
# Those whole reason for this file is to test original impelementation vs our implementation
# That way we can see if our implementation is correct

#Make root directory "aosdump" if python 2 else keep this dir as root

# Set the root directory based on Python version
if sys.version_info[0] < 3:
    # For Python 2, set "aosdump" as root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.join(script_dir, "aosdump")
    if not os.path.exists(root_dir):
        os.makedirs(root_dir)
    os.chdir(root_dir)
    sys.path.insert(0, root_dir)
else:
    # For Python 3+, keep current directory as root
    pass

# Import after setting up the paths
import aoslib.world 
import shared.glm
import aoslib.vxl
print(aoslib.world)

# VXL Args 
# _state Converted via PyInt_AsLong into a C int (you can also pass -1 if you want to disable whatever update logic it drives).
# _data Must be a Python 2 str (i.e. a bytestring) - the code calls PyString_AsStringAndSize(_data, &s, &len);
# _data_size Again converted via PyInt_AsLong to a C int. This is not auto-derived from len(_data) - you must pass the number of bytes you actually intend the C++ side to read.
# _detail_level (default 2) Converted to int and stashed away in the freshly created MapData. (optional)
vxl = aoslib.vxl.VXL(-1,"sadwasd", 7, 2)
world = aoslib.world.World(vxl)
player = aoslib.world.Player(world)

player.set_orientation(shared.glm.Vector3(0,0,0))
player.set_position(0,0,0)

player.set_velocity(0,0,0)

# player.set_acceleration((0,0,0))

print(player)
