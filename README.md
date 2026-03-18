# Ace Of Spades Library Reverse Engineering Project

This project reverse engineers Ace Of Spades 1.x libraries with a focus on packets, map loading, world logic, and the long-term goal of rebuilding a 1:1 compatible server.

## Project Status

Current completed modules:

- **shared.packet**: 127/127 classes and functions completed (100%)
- **shared.bytes**: 3/3 classes completed (100%)

Current native restoration slices:

- **aoslib.vxl**: 61/61 tracked Python-facing native symbols restored and reference-matched for the current slice (100% slice parity)
- **aoslib.world**: 172/172 tracked Python-facing native symbols restored and reference-matched for the current slice (100% surface parity)
- **aoslib.kv6**: 28/28 tracked Python-facing native symbols restored and reference-matched for the current slice (100% slice parity)

Totals we can honestly claim right now:

- **Fully finished modules**: 130/130 classes and functions completed and matched 100%
- **Tracked native Python-facing symbols restored in active slices**: 261/261 reference-matched
  - `aoslib.vxl`: 61/61
  - `aoslib.world`: 172/172
  - `aoslib.kv6`: 28/28

Important scope note:

- `aoslib.vxl` is complete for the public API plus loader slice, but the full native `post_load_map_setup` pass is still a later follow-up.
- `aoslib.world` is complete for the public API/surface slice, but deeper kernel parity is still pending for non-player movement objects and remaining server-only compatibility behavior.
- `aoslib.kv6` is complete for the Python-facing data/path/save slice, while full OpenGL-backed display behavior is still represented by the current compatibility ownership path in headless tests.

Packet testing note:

- `tests/test_packets.py` executes 106 full packet compatibility tests.
- The remaining 21 packet-related classes are abstract bases, internal structs, or compiled types whose original Python 2 properties are not externally writable, so they are counted as restored but not covered by direct property-assignment style tests.

## Setup Requirements

### Python Versions

You need both Python versions to test properly:

- **Python 3.x**: for the new implementation
- **Python 2.7 32-bit**: for testing against the original binaries

**IMPORTANT**: Python 2.7 must be 32-bit to interact correctly with the original compiled library.

### Setting Up The Original Library

Create an `aosdump` folder in the project root and place the original Ace Of Spades 1.x files in this structure:

```text
aosdump/
|- aoslib/
|  `- ... original aoslib files
`- shared/
   `- ... original shared files
```

## Testing

### Packet Tests

Run against the original implementation:

```powershell
py2 .\tests\test_packets.py
```

Run against the Python 3 restoration:

```powershell
py .\tests\test_packets.py
```

### VXL Tests

Run against the original implementation:

```powershell
py2 .\tests\test_vxl.py
```

Run against the Python 3 restoration:

```powershell
py .\tests\test_vxl.py
```

### World Tests

Run against the original implementation:

```powershell
py2 .\tests\test_world.py
```

Run against the Python 3 restoration:

```powershell
py .\tests\test_world.py
py .\tests\test_player_physics.py
```

### KV6 Tests

Run against the original implementation:

```powershell
py2 .\tests\test_kv6.py
```

Run against the Python 3 restoration:

```powershell
py .\tests\test_kv6.py
```

Each test file adjusts import paths based on the Python version so it can target either the original `aosdump` binaries or the new Python 3 implementation.

## Project Structure

- **aosdump/**: original compiled binaries and dumped Python 2 files
- **aoslib/**: restored game library implementation
- **shared/**: restored shared components
- **build/**: compiled output for the Python 3 extensions
- **tests/test_packets.py**: packet compatibility tests
- **tests/test_vxl.py**: VXL restoration tests
- **tests/test_world.py**: world surface parity tests
- **tests/test_player_physics.py**: deterministic Python 3 physics tests
- **tests/test_kv6.py**: KV6 restoration tests
- **docs/vxl-restoration.md**: VXL restoration notes
- **docs/world-restoration.md**: world restoration notes
- **docs/kv6-restoration.md**: KV6 restoration notes

## Development Workflow

1. Study the original implementation in `aosdump/` and the matching native binary.
2. Rebuild the behavior in the Python 3 codebase.
3. Add or update a dedicated test file for the feature being restored.
4. Run the feature under Python 2 and Python 3.
5. Keep iterating until the surface and behavior match the original slice being targeted.

## Contribution

Contributions are welcome. A typical workflow is:

1. Pick a feature or module that is not fully restored yet.
2. Add or extend the matching test file under `tests/`.
3. Implement the behavior in the appropriate module.
4. Verify compatibility against the original implementation.
5. Submit a pull request.
