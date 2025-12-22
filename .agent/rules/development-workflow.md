---
trigger: always_on
---

# Development Workflow

## Implementation Process
1. Study the original packet structure in the aosdump implementation
2. Implement equivalent functionality in the new codebase
3. Create test cases in [test_packets.py](mdc:test_packets.py)
4. Verify binary compatibility between old and new implementations

## Testing Workflow
1. Run `py2 ./test_packets.py` to test a packet against the original implementation
2. Run `py ./test_packets.py` to test the same packet against the new implementation
3. Compare outputs to ensure binary compatibility
4. Debug differences if outputs don't match

## Adding New Packet Support
When adding support for a new packet type:
1. Create a new test function in [test_packets.py](mdc:test_packets.py) following the pattern of existing tests
2. Implement the packet class in the appropriate module
3. Ensure the packet ID is correctly defined
4. Test with both Python 2 and Python 3 to verify compatibility

## Binary Compatibility
Binary compatibility between the old and new implementations is critical:
- Both implementations must produce identical binary output for the same packet
- Both implementations must correctly parse the binary data produced by the other
- Endianness, alignment, and padding must match exactly

