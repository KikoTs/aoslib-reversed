#!/usr/bin/env python
import struct

def create_minimal_kv6(filename):
    """Create a minimal valid KV6 file that can be loaded"""
    
    # KV6 header structure:
    # Magic: "Kvxl" (4 bytes)
    # leng_x: uint32 (4 bytes)
    # leng_y: uint32 (4 bytes) 
    # pivot_x: float (4 bytes)
    # pivot_y: float (4 bytes)
    # pivot_z: float (4 bytes)
    # numvoxs: uint32 (4 bytes)
    # Total header: 28 bytes
    
    with open(filename, 'wb') as f:
        # Write magic
        f.write(b'Kvxl')
        
        # Write dimensions (very small model)
        leng_x = 2
        leng_y = 2
        f.write(struct.pack('<I', leng_x))  # leng_x
        f.write(struct.pack('<I', leng_y))  # leng_y
        
        # Write pivots (center of model)
        f.write(struct.pack('<f', 1.0))  # pivot_x
        f.write(struct.pack('<f', 1.0))  # pivot_y
        f.write(struct.pack('<f', 0.0))  # pivot_z
        
        # Write number of voxels
        numvoxs = 1
        f.write(struct.pack('<I', numvoxs))  # numvoxs
        
        # Write xoffset array: (leng_x + 1) * uint16
        # This array indicates where each x-column starts in xyoffset
        xoffset_size = leng_x + 1
        for i in range(xoffset_size):
            f.write(struct.pack('<H', i))  # Simple sequential offsets
            
        # Write xyoffset array: leng_x * leng_y * uint16  
        # This array indicates where each xy-column starts in voxdata
        xyoffset_size = leng_x * leng_y
        for i in range(xyoffset_size):
            if i == 0:  # First column has our single voxel
                f.write(struct.pack('<H', 0))
            else:  # Other columns are empty
                f.write(struct.pack('<H', 1))
                
        # Write voxel data: numvoxs * uint32
        # Format: z(10 bits) | y(10 bits) | x(10 bits) | color index(2 bits or similar)
        # Simple voxel at (0,0,0) with color 0x7F (127 - semi-transparent)
        voxel_data = 0  # z=0, y=0, x=0
        voxel_data |= (0x7F << 24)  # Add some color info in high bits
        f.write(struct.pack('<I', voxel_data))

if __name__ == "__main__":
    # Create test files in both locations
    create_minimal_kv6("test_minimal.kv6")
    create_minimal_kv6("aosdump/test_minimal.kv6")
    print("Created minimal KV6 files")
    
    # Also create an even simpler version
    with open("simple.kv6", 'wb') as f:
        f.write(b'Kvxl')  # Magic
        f.write(struct.pack('<I', 1))  # leng_x = 1
        f.write(struct.pack('<I', 1))  # leng_y = 1
        f.write(struct.pack('<f', 0.5))  # pivot_x
        f.write(struct.pack('<f', 0.5))  # pivot_y
        f.write(struct.pack('<f', 0.0))  # pivot_z
        f.write(struct.pack('<I', 0))  # numvoxs = 0 (empty model)
        
        # xoffset: 2 entries for leng_x+1
        f.write(struct.pack('<H', 0))
        f.write(struct.pack('<H', 0))
        
        # xyoffset: 1 entry for leng_x*leng_y
        f.write(struct.pack('<H', 0))
        
        # No voxel data since numvoxs = 0
    
    with open("aosdump/simple.kv6", 'wb') as f:
        f.write(b'Kvxl')  # Magic
        f.write(struct.pack('<I', 1))  # leng_x = 1
        f.write(struct.pack('<I', 1))  # leng_y = 1
        f.write(struct.pack('<f', 0.5))  # pivot_x
        f.write(struct.pack('<f', 0.5))  # pivot_y
        f.write(struct.pack('<f', 0.0))  # pivot_z
        f.write(struct.pack('<I', 0))  # numvoxs = 0 (empty model)
        
        # xoffset: 2 entries for leng_x+1
        f.write(struct.pack('<H', 0))
        f.write(struct.pack('<H', 0))
        
        # xyoffset: 1 entry for leng_x*leng_y
        f.write(struct.pack('<H', 0))
        
        # No voxel data since numvoxs = 0
        
    print("Created simple.kv6 files (empty models)") 