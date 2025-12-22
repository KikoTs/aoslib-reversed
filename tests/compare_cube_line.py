import sys
import os

# Set the root directory based on Python version to match test_packets.py logic
if sys.version_info[0] < 3:
    # For Python 2, set "aosdump" as root directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.join(script_dir, "aosdump")
    if not os.path.exists(root_dir):
        print("Error: aosdump directory not found")
        sys.exit(1)
    os.chdir(root_dir)
    sys.path.insert(0, root_dir)
else:
    # For Python 3+, keep current directory as root
    pass

import aoslib.world

def test_line(name, x1, y1, z1, x2, y2, z2):
    print("Testing %s: (%d,%d,%d) -> (%d,%d,%d)" % (name, x1, y1, z1, x2, y2, z2))
    points = aoslib.world.cube_line(x1, y1, z1, x2, y2, z2)
    
    # Print format tailored for diffing: "Index: (x, y, z)"
    for i, p in enumerate(points):
        print("%d: %s" % (i, str(p)))

if __name__ == "__main__":
    version = "py2" if sys.version_info[0] < 3 else "py3"
    filename = "cube_line_%s.txt" % version
    
    with open(filename, "w") as f:
        def log(msg):
            print(msg)
            f.write(msg + "\n")
            
        points = aoslib.world.cube_line(0, 0, 0, 20, 10, 5)
        log("Long1: (0,0,0) -> (20,10,5)")
        for i, p in enumerate(points):
            log("%d: %s" % (i, str(p)))
            
        points = aoslib.world.cube_line(0, 0, 0, 30, 20, 10)
        log("Long2: (0,0,0) -> (30,20,10)")
        for i, p in enumerate(points):
            log("%d: %s" % (i, str(p)))

