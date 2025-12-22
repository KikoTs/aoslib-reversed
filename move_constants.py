
import os

file_path = r'g:\AoSRevival\aoslib-reversed\shared\constants.py'

with open(file_path, 'r') as f:
    lines = f.readlines()

# Find the start of the appended block
start_marker = "# Enums for server refactoring"
start_idx = -1
for i, line in enumerate(lines):
    if start_marker in line:
        start_idx = i
        break

if start_idx == -1:
    print("Could not find start marker")
    exit(1)

# Extract the block
enum_block = lines[start_idx:]
remaining_lines = lines[:start_idx]

# Insert at the top, after the header (around line 5)
# Find 'from .constants_gamemode import *' to insert before it
insert_idx = 0
for i, line in enumerate(remaining_lines):
    if "from .constants_gamemode import *" in line:
        insert_idx = i
        break

# If not found, just insert at top (after comments maybe?)
# But let's verify line 5
if insert_idx == 0 and "from .constants_gamemode" not in remaining_lines[0]:
    # iterate to find a good spot, e.g. after header comments
    for i, line in enumerate(remaining_lines):
        if line.strip().startswith("from") or line.strip().startswith("import"):
            insert_idx = i
            break

print(f"Moving block of {len(enum_block)} lines from line {start_idx+1} to line {insert_idx+1}")

new_lines = remaining_lines[:insert_idx] + enum_block + remaining_lines[insert_idx:]

with open(file_path, 'w') as f:
    f.writelines(new_lines)

print("Successfully moved constants.")
