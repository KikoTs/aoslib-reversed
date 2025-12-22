#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import print_function, division
import sys
import os

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
from shared.glm import Vector3, IntVector3, Matrix4

import math

import unittest


def test_vector3():
    print("\n=== Vector3 Tests ===")
    
    # Basic creation
    v1 = Vector3(1.0, 2.0, 3.0)
    v2 = Vector3(4.0, 5.0, 6.0)
    print("v1:", v1)
    print("v2:", v2)
    
    # Copy
    v3 = v1.copy()
    print("v3 (copy of v1):", v3)
    
    # Get/Set
    print("v1.get():", v1.get())
    v3.set(5.0, 6.0, 7.0)
    print("After v3.set(5.0, 6.0, 7.0):", v3)
    v3.set_vector(v2)
    print("After v3.set_vector(v2):", v3)
    
    # Translate
    v4 = Vector3(1.0, 1.0, 1.0)
    v4_translated = v4.translate(1.0, 2.0, 3.0)
    print("Original v4:", v4)
    print("Returned from v4.translate(1.0, 2.0, 3.0):", v4_translated)
    
    # Translate with Vector3 components
    v4a = Vector3(1.0, 1.0, 1.0)
    delta = Vector3(2.0, 3.0, 4.0)
    # Extract components from the vector and use them for translation
    v4a_translated = v4a.translate(delta[0], delta[1], delta[2])
    print("After v4a.translate with Vector3 components:", v4a_translated)
    
    # Distance calculations
    dist = v1.distance(v2)
    sq_dist = v1.sq_distance(v2)
    print("Distance v1 to v2:", dist)
    print("Squared distance v1 to v2:", sq_dist)
    
    # Dot product
    dot = v1.dot(v2)
    print("v1.dot(v2):", dot)
    
    # Cross product
    cross = v1.cross(v2)
    print("v1.cross(v2):", cross)
    
    # SLERP
    v5 = Vector3(1.0, 0.0, 0.0)
    v6 = Vector3(0.0, 1.0, 0.0)
    slerp_result = v5.slerp(v6, 0.5)
    print("v5.slerp(v6, 0.5):", slerp_result)
    
    # Magnitude
    mag = v1.magnitude()
    sq_mag = v1.sq_magnitude()
    print("v1.magnitude():", mag)
    print("v1.sq_magnitude():", sq_mag)
    
    # Normalization
    v7 = Vector3(3.0, 4.0, 0.0)
    norm_v7 = v7.norm()
    print("v7:", v7)
    print("v7.norm():", norm_v7)
    print("v7.norm().magnitude():", norm_v7.magnitude())
    
    # Clamping
    v8 = Vector3(-2.0, 1.5, 3.0)
    # Component-wise clamping
    x_clamped = max(min(v8[0], 2.0), -1.0)
    y_clamped = max(min(v8[1], 2.0), -1.0)
    z_clamped = max(min(v8[2], 2.0), -1.0)
    clamped = Vector3(x_clamped, y_clamped, z_clamped)
    print("v8:", v8)
    print("v8 clamped between -1.0 and 2.0:", clamped)
    
    # Indexing
    print("v1[0], v1[1], v1[2]:", v1[0], v1[1], v1[2])
    v1.set(10.0, v1[1], v1[2])
    print("After v1.set(10.0, v1[1], v1[2]):", v1)
    
    # Operators
    sum_v = v1 + v2
    diff_v = v2 - v1
    scaled_v = v1 * 2.0
    
    scaled_v2 = v2 * 3.0
    print("v2 * 3.0:", scaled_v2)
        
    # Use multiplication by reciprocal instead of division
    div_v = v2 * 0.5
    
    print("v1 + v2:", sum_v)
    print("v2 - v1:", diff_v)
    print("v1 * 2.0:", scaled_v)
    print("v2 * 0.5 (equivalent to v2 / 2.0):", div_v)

def test_int_vector3():
    print("\n=== IntVector3 Tests ===")
    
    # Basic creation
    iv1 = IntVector3(1, 2, 3)
    iv2 = IntVector3(4, 5, 6)
    print("iv1:", iv1)
    print("iv2:", iv2)
    
    # Copy
    iv3 = iv1.copy()
    print("iv3 (copy of iv1):", iv3)
    
    # Get/Set
    print("iv1.get():", iv1.get())
    iv3.set(5, 6, 7)
    print("After iv3.set(5, 6, 7):", iv3)
    iv3.set_vector(iv2)
    print("After iv3.set_vector(iv2):", iv3)
    
    # Indexing
    print("iv1[0], iv1[1], iv1[2]:", iv1[0], iv1[1], iv1[2])
    iv1.set(10, iv1[1], iv1[2])
    print("After iv1.set(10, iv1[1], iv1[2]):", iv1)

def test_matrix4():
    print("\n=== Matrix4 Tests ===")
    
    # Identity matrix
    m1 = Matrix4()
    print("Identity matrix m1:")
    print(m1)
    
    # Copy
    m2 = m1.copy()
    print("m2 (copy of m1):")
    print(m2)
    
    # Rotation with tuple axis
    m3 = Matrix4()
    m3.rotate(math.radians(90.0), (0.0, 0.0, 1.0))
    print("After 90-degree rotation around Z-axis:")
    print(m3)
    
    # Test rotation effect on a vector
    v = Vector3(1.0, 0.0, 0.0)
    rotated_v = m3.multiply_vector(v)
    print("Vector (1,0,0) after rotation:", rotated_v)
    
    # Translation - using the correct tuple syntax
    m4 = Matrix4()
    m4.translate((10.0, 20.0, 30.0))
    print("After translation by (10,20,30):")
    print(m4)
    
    # Test translation effect on a vector
    v2 = Vector3(1.0, 1.0, 1.0)
    translated_v = m4.multiply_vector(v2)
    print("Vector (1,1,1) after translation:", translated_v)
    
    # Orientation with tuples
    m5 = Matrix4()
    m5.orientation((1.0, 0.0, 0.0), (0.0, 0.0, 1.0))
    print("After orientation (forward=(1,0,0), up=(0,0,1)):")
    print(m5)
    
    # Matrix composition - create a composite transformation manually
    m6 = Matrix4()
    # Apply m4's translation to m6
    m6.translate((10.0, 20.0, 30.0))
    print("Composite transformation (manual):")
    print(m6)
    
    # Indexing
    print("m1[0,0], m1[1,1], m1[2,2], m1[3,3]:", m1[0,0], m1[1,1], m1[2,2], m1[3,3])
    m7 = Matrix4()
    print("Original matrix m7:")
    print(m7)
    m7.set_identity()
    print("After m7.set_identity():")
    print(m7)

def main():
    print("Testing GLM Module (Python {}.{})".format(sys.version_info[0], sys.version_info[1]))
    
    test_vector3()
    test_int_vector3()
    test_matrix4()
    
    print("\nAll tests completed!")

if __name__ == "__main__":
    main()