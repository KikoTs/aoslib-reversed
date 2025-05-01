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
from shared.bytes import ByteReader, ByteWriter, NoDataLeft



def toHex(data):
    #python 2 and 3 support
    if sys.version_info[0] < 3:
        return ' '.join('{:02X}'.format(ord(b)) for b in data)
    else:
        if isinstance(data, str):
            data = data.encode('cp437', 'replace')
        return ' '.join('{:02X}'.format(b) for b in data)

def test_bytes():
    print("Running in Python", sys.version_info[0])

    writer = ByteWriter()
    writer.write_uint64(1)
    writer.write_int(2)
    writer.write_int(3)
    writer.write_string("Test5")
    
    print("Raw output:")
    print(str(writer))
    print("Hex output:")
    print(toHex(str(writer)))

    reader = ByteReader(str(writer))



    uint64_val = reader.read_uint64()
    print("Uint64:", uint64_val)
    print("Type:", type(uint64_val))

    int_val = reader.read_int()
    print("Int:", int_val)
    print("Type:", type(int_val))

    int_val = reader.read_int()
    print("Int:", int_val)
    print("Type:", type(int_val))
    
    string_val = reader.read_string()
    print("String:", string_val)
    print("Type:", type(string_val))

test_bytes()