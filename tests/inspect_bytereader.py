
import sys
import os

sys.path.insert(0, os.path.join(os.getcwd(), 'aosdump'))

try:
    from shared.bytes import ByteReader
except ImportError:
    print "Failed to import ByteReader from aosdump"
    sys.exit(1)

print "ByteReader dir:"
for name in dir(ByteReader):
    if name.startswith('read_'):
        print name
