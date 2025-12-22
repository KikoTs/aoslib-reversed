"""
VXL Module Tests - Binary Compatibility
=======================================
Tests the VXL module implementation by comparing Python 2 (original) vs Python 3 (ours).
Focuses on binary output comparison for 100% game compatibility.

Usage:
    py2 ./test_vxl.py   - Test original implementation, save output to files
    py  ./test_vxl.py   - Test our new implementation, compare with original

Workflow:
    1. Run with py2 first to generate reference outputs
    2. Run with py3 to test our implementation and compare
"""

import os
import sys

# ============================================================================
# Helper Functions
# ============================================================================

def toHex(data):
    """Convert bytes to hex string for display"""
    if sys.version_info[0] < 3:
        if isinstance(data, unicode):
            data = data.encode('utf-8')
        return ' '.join('{:02X}'.format(ord(b)) for b in data)
    else:
        if isinstance(data, str):
            data = data.encode('cp437', 'replace')
        return ' '.join('{:02X}'.format(b) for b in data)

def save_reference(name, data):
    """Save reference binary data from py2"""
    filename = "vxl_ref_%s.bin" % name
    with open(filename, 'wb') as f:
        if isinstance(data, str) and sys.version_info[0] < 3:
            f.write(data)
        else:
            f.write(data if isinstance(data, bytes) else str(data).encode())
    print("[SAVED] %s (%d bytes)" % (filename, len(data) if data else 0))

def compare_with_reference(name, data):
    """Compare our output with py2 reference"""
    # py2 saves refs in aosdump/, py3 looks from main dir
    if IS_PY2:
        filename = "vxl_ref_%s.bin" % name
    else:
        filename = "aosdump/vxl_ref_%s.bin" % name
    if not os.path.exists(filename):
        print("[SKIP] No reference file: %s" % filename)
        return None
    
    with open(filename, 'rb') as f:
        reference = f.read()
    
    if isinstance(data, str):
        data = data.encode('utf-8')
    elif data is None:
        data = b''
    
    if data == reference:
        print("[MATCH] %s - %d bytes identical" % (name, len(data)))
        return True
    else:
        print("[DIFF] %s" % name)
        print("  Reference: %s" % toHex(reference[:50]))
        print("  Ours:      %s" % toHex(data[:50] if data else b''))
        return False


# ============================================================================
# Setup
# ============================================================================

IS_PY2 = sys.version_info[0] < 3

if IS_PY2:
    # Python 2: Test against original implementation in aosdump
    script_dir = os.path.dirname(os.path.abspath(__file__))
    root_dir = os.path.join(script_dir, "aosdump")
    os.chdir(root_dir)
    sys.path.insert(0, root_dir)
    print("=" * 60)
    print("TESTING ORIGINAL (Python 2) - Generating reference files")
    print("=" * 60)
else:
    print("=" * 60)
    print("TESTING NEW IMPLEMENTATION (Python 3) - Comparing with reference")
    print("=" * 60)

# Import VXL module
try:
    import aoslib.vxl as vxl
    print("[OK] Imported aoslib.vxl\n")
except ImportError as e:
    print("[FAIL] Could not import aoslib.vxl:", e)
    sys.exit(1)


# ============================================================================
# Binary Comparison Tests
# ============================================================================

print("--- Binary Compatibility Tests ---\n")

# Test 1: Create VXL instance with test data
test_data = b"test1234" if not IS_PY2 else "test1234"
try:
    test_vxl = vxl.VXL(-1, test_data, len(test_data), 2)
    print("[OK] VXL(-1, data, %d, 2) created" % len(test_data))
except Exception as e:
    print("[FAIL] VXL creation:", e)
    test_vxl = None

# Test 2: get_color_tuple output
print("\n--- get_color_tuple Tests ---")

color_tests = [
    0x000000,      # Black
    0xFFFFFF,      # White  
    0xFF0000,      # Red (BGR order)
    0x00FF00,      # Green
    0x0000FF,      # Blue
    0xFF8040,      # Custom color
    0x7F804020,    # With alpha
]

for color in color_tests:
    try:
        result = vxl.get_color_tuple(color)
        result_str = str(result)
        if IS_PY2:
            save_reference("color_%08X" % color, result_str)
        else:
            compare_with_reference("color_%08X" % color, result_str)
        print("  0x%08X -> %s" % (color, result))
    except Exception as e:
        print("  [FAIL] 0x%08X: %s" % (color, e))

# Test 3: VXL generate_vxl (serialize to bytes)
print("\n--- VXL Serialization Tests ---")

if test_vxl:
    try:
        vxl_bytes = test_vxl.generate_vxl()
        if vxl_bytes:
            if IS_PY2:
                save_reference("vxl_serialize", vxl_bytes)
            else:
                compare_with_reference("vxl_serialize", vxl_bytes)
            print("  generate_vxl(): %d bytes" % len(vxl_bytes))
            print("  First 32 bytes: %s" % toHex(vxl_bytes[:32]))
        else:
            print("  generate_vxl(): returned None (not implemented yet)")
    except Exception as e:
        print("  [FAIL] generate_vxl():", e)

# Test 4: VXL get_solid / get_point / get_color
print("\n--- Block Query Tests ---")

if test_vxl:
    test_coords = [(0, 0, 0), (128, 128, 32), (255, 255, 63)]
    
    for x, y, z in test_coords:
        try:
            solid = test_vxl.get_solid(x, y, z)
            color = test_vxl.get_color(x, y, z)
            result_str = "%d,%d" % (1 if solid else 0, color)
            if IS_PY2:
                save_reference("block_%d_%d_%d" % (x, y, z), result_str)
            else:
                compare_with_reference("block_%d_%d_%d" % (x, y, z), result_str)
            print("  (%d,%d,%d): solid=%s, color=0x%08X" % (x, y, z, solid, color))
        except Exception as e:
            print("  [FAIL] (%d,%d,%d): %s" % (x, y, z, e))

# Test 5: sphere_in_frustum
print("\n--- Frustum Tests ---")

frustum_tests = [
    (0.0, 0.0, 0.0, 1.0),
    (100.0, 100.0, 32.0, 5.0),
    (256.0, 256.0, 32.0, 10.0),
]

for x, y, z, r in frustum_tests:
    try:
        result = vxl.sphere_in_frustum(x, y, z, r)
        result_str = str(result)
        if IS_PY2:
            save_reference("frustum_%.0f_%.0f_%.0f_%.0f" % (x, y, z, r), result_str)
        else:
            compare_with_reference("frustum_%.0f_%.0f_%.0f_%.0f" % (x, y, z, r), result_str)
    except Exception as e:
        print("  [FAIL] sphere_in_frustum(%.0f,%.0f,%.0f,%.0f): %s" % (x, y, z, r, e))


# ============================================================================
# Test 6: Block Manipulation (set_point, remove_point)
# API discovered via IDA: set_point(x, y, z, (r,g,b,a)), remove_point(x, y, z)
# NOTE: py2 crashes on these calls due to missing game engine state
# ============================================================================
print("\n--- Block Manipulation Tests ---")

if not IS_PY2 and test_vxl:
    # Test set_point(x, y, z, (r,g,b,a))
    print("  Testing set_point(100, 100, 32, (255, 0, 0, 255))...")
    try:
        before_solid = test_vxl.get_solid(100, 100, 32)
        test_vxl.set_point(100, 100, 32, (255, 0, 0, 255))
        after_solid = test_vxl.get_solid(100, 100, 32)
        after_color = test_vxl.get_color(100, 100, 32)
        result_str = "before=%s,after=%s,color=0x%X" % (before_solid, after_solid, after_color)
        print("    Result: %s" % result_str)
        # Store as reference for future comparison
        with open("vxl_ref_set_point.txt", "w") as f:
            f.write(result_str)
    except Exception as e:
        print("    [FAIL] set_point: %s" % e)
    
    # Test remove_point(x, y, z)
    print("  Testing remove_point(100, 100, 32)...")
    try:
        test_vxl.remove_point(100, 100, 32)
        after_remove = test_vxl.get_solid(100, 100, 32)
        result_str = "after_remove=%s" % after_remove
        print("    Result: %s" % result_str)
        with open("vxl_ref_remove_point.txt", "w") as f:
            f.write(result_str)
    except Exception as e:
        print("    [FAIL] remove_point: %s" % e)
    
    # Test get_color_tuple on a set block
    print("  Testing get_color_tuple after set_point...")
    try:
        test_vxl.set_point(200, 200, 32, (128, 64, 32, 253))  # Alpha 253 = alpha_byte 127
        color_tuple = test_vxl.get_color_tuple(200, 200, 32)
        result_str = str(color_tuple)
        print("    get_color_tuple(200,200,32) = %s" % result_str)
        with open("vxl_ref_color_tuple_after_set.txt", "w") as f:
            f.write(result_str)
    except Exception as e:
        print("    [FAIL] get_color_tuple after set: %s" % e)
else:
    print("  [SKIP] py2 or no VXL object - block manipulation crashes in original")


# ============================================================================
# Test 7: Ground Colors
# ============================================================================
print("\n--- Ground Color Tests ---")

try:
    vxl.reset_ground_colors()
    vxl.add_ground_color(255, 128, 64, 255)
    vxl.add_ground_color(100, 200, 50, 128)
    
    if test_vxl:
        ground_colors = test_vxl.get_ground_colors()
        result_str = str(ground_colors)
        if IS_PY2:
            save_reference("ground_colors", result_str)
        else:
            compare_with_reference("ground_colors", result_str)
        print("  get_ground_colors(): %s" % result_str[:80])
except Exception as e:
    print("  [FAIL] ground colors: %s" % e)


# ============================================================================
# Test 8: Z-Limits
# ============================================================================
print("\n--- Z-Limit Tests ---")

if test_vxl:
    try:
        # Get default max_modifiable_z
        default_z = test_vxl.get_max_modifiable_z()
        result_str = str(default_z)
        if IS_PY2:
            save_reference("max_modifiable_z_default", result_str)
        else:
            compare_with_reference("max_modifiable_z_default", result_str)
        print("  get_max_modifiable_z() default: %s" % default_z)
        
        # Set and get
        test_vxl.set_max_modifiable_z(48)
        new_z = test_vxl.get_max_modifiable_z()
        result_str = str(new_z)
        if IS_PY2:
            save_reference("max_modifiable_z_set48", result_str)
        else:
            compare_with_reference("max_modifiable_z_set48", result_str)
        print("  set_max_modifiable_z(48), get: %s" % new_z)
    except Exception as e:
        print("  [FAIL] z-limits: %s" % e)


# ============================================================================
# Test 9: Clamp Function (module level)
# ============================================================================
print("\n--- Clamp Function Tests ---")

clamp_tests = [
    (0.5, 0, 1),      # Within range
    (-0.5, 0, 1),     # Below min
    (1.5, 0, 1),      # Above max
    (50, 10, 100),    # Integer within range
    (5, 10, 100),     # Integer below min
    (150, 10, 100),   # Integer above max
]

for value, min_val, max_val in clamp_tests:
    try:
        result = vxl.clamp(value, min_val, max_val)
        result_str = str(result)
        if IS_PY2:
            save_reference("clamp_%s_%s_%s" % (value, min_val, max_val), result_str)
        else:
            compare_with_reference("clamp_%s_%s_%s" % (value, min_val, max_val), result_str)
        print("  clamp(%s, %s, %s) = %s" % (value, min_val, max_val, result))
    except Exception as e:
        print("  [FAIL] clamp(%s, %s, %s): %s" % (value, min_val, max_val, e))


# ============================================================================
# Test 10: has_neighbors
# ============================================================================
print("\n--- has_neighbors Tests ---")

if test_vxl:
    # Test on empty position (no neighbors)
    try:
        result = test_vxl.has_neighbors(50, 50, 32, 1, 0)
        result_str = str(result)
        if IS_PY2:
            save_reference("has_neighbors_empty", result_str)
        else:
            compare_with_reference("has_neighbors_empty", result_str)
        print("  has_neighbors(50,50,32) on empty: %s" % result)
    except Exception as e:
        print("  [FAIL] has_neighbors empty: %s" % e)


# ============================================================================
# Test 11: done_processing
# ============================================================================
print("\n--- Threading Tests ---")

if test_vxl:
    try:
        result = test_vxl.done_processing()
        result_str = str(result)
        if IS_PY2:
            save_reference("done_processing", result_str)
        else:
            compare_with_reference("done_processing", result_str)
        print("  done_processing(): %s" % result)
    except Exception as e:
        print("  [FAIL] done_processing: %s" % e)


# ============================================================================
# Test 12: is_space_to_add_blocks
# ============================================================================
print("\n--- Block Space Tests ---")

if test_vxl:
    try:
        result = test_vxl.is_space_to_add_blocks(100)
        result_str = str(result)
        if IS_PY2:
            save_reference("is_space_100", result_str)
        else:
            compare_with_reference("is_space_100", result_str)
        print("  is_space_to_add_blocks(100): %s" % result)
    except Exception as e:
        print("  [FAIL] is_space_to_add_blocks: %s" % e)


# ============================================================================
# Test 13: A2 function (module level)
# ============================================================================
print("\n--- A2 Function Tests ---")

a2_tests = [
    "test_string",
    12345,
    3.14159,
    None,
]

for value in a2_tests:
    try:
        result = vxl.A2(value)
        result_str = str(result)
        if IS_PY2:
            save_reference("A2_%s" % type(value).__name__, result_str)
        else:
            compare_with_reference("A2_%s" % type(value).__name__, result_str)
        print("  A2(%s) = %s" % (repr(value), result))
    except Exception as e:
        print("  [FAIL] A2(%s): %s" % (repr(value), e))


# ============================================================================
# Summary
# ============================================================================
print("\n" + "=" * 60)
if IS_PY2:
    print("Reference files generated. Now run with 'py test_vxl.py' to compare.")
else:
    print("Comparison complete. Check for [DIFF] items above.")
print("=" * 60)

