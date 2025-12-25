#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Byte-by-byte diff between working and our hex.
"""
# Working hex from real server
WORKING = "72 00 7C 55 81 7A 0E 40 01 58 50 9B FC 87 69 00 00 43 54 46 5F 54 49 54 4C 45 00 43 54 46 5F 44 45 53 43 52 49 50 54 49 4F 4E 00 43 54 46 5F 49 4E 46 4F 47 52 41 50 48 49 43 5F 54 45 58 54 31 00 43 54 46 5F 49 4E 46 4F 47 52 41 50 48 49 43 5F 54 45 58 54 32 00 43 54 46 5F 49 4E 46 4F 47 52 41 50 48 49 43 5F 54 45 58 54 33 00 43 69 74 79 20 6F 66 20 43 68 69 63 61 67 6F 00 4C 6F 6E 64 6F 6E 00 80 1B 53 23 08 00 EB 69 00 01 00 C0 01 00 01 01 01 00 01 00 01 00 01 40 00 40 00 01 00 00 12 5A 00 5D 00 46 00 50 00 5A 00 6A 00 55 00 60 00 60 00 60 00 60 00 60 00 60 00 C0 00 C0 00 40 00 63 00 56 00 02 00 01 01 4B 69 6B 6F 54 73 20 41 63 65 2E 70 79 20 3C 33 00 02 3B 3A 37 EE 28 36 40 EF 00 01 01 00 01 08"

# Our broken hex (zeros for steam ID, different byte positions)
OURS = "72 00 00 00 00 00 00 00 00 58 50 9B FC 87 69 00 00 43 54 46 5F 54 49 54 4C 45 00 43 54 46 5F 44 45 53 43 52 49 50 54 49 4F 4E 00 43 54 46 5F 49 4E 46 4F 47 52 41 50 48 49 43 5F 54 45 58 54 31 00 43 54 46 5F 49 4E 46 4F 47 52 41 50 48 49 43 5F 54 45 58 54 32 00 43 54 46 5F 49 4E 46 4F 47 52 41 50 48 49 43 5F 54 45 58 54 33 00 43 69 74 79 20 6F 66 20 43 68 69 63 61 67 6F 00 4C 6F 6E 64 6F 6E 00 80 1B 53 23 08 00 EB 69 00 01 00 C0 01 00 01 01 01 00 01 00 01 00 01 40 00 40 00 01 01 00 00 12 5A 00 5D 00 46 00 50 00 5A 00 6A 00 55 00 60 00 60 00 60 00 60 00 60 00 60 00 C0 00 C0 00 40 00 63 00 56 00 02 00 01 01 4B 69 6B 6F 54 73 20 41 63 65 2E 70 79 20 3C 33 00 02 3B 3A 37 EE 28 36 40 EF 00 01 01 00 01 08"

def hex_to_bytes(s):
    return [int(x, 16) for x in s.strip().split()]

working = hex_to_bytes(WORKING)
ours = hex_to_bytes(OURS)

print("Working length: {} bytes".format(len(working)))
print("Ours length: {} bytes".format(len(ours)))
print("")

# Find differences
diffs = []
for i in range(max(len(working), len(ours))):
    w = working[i] if i < len(working) else None
    o = ours[i] if i < len(ours) else None
    if w != o:
        diffs.append((i, w, o))

if not diffs:
    print("NO DIFFERENCES!")
else:
    print("DIFFERENCES:")
    for pos, w, o in diffs:
        w_str = "{:02X}".format(w) if w is not None else "MISSING"
        o_str = "{:02X}".format(o) if o is not None else "MISSING"
        print("  Byte {:3d}: working={} ours={}".format(pos, w_str, o_str))
