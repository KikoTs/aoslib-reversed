# Ace Of Spades Library Reverse Engineering Project

This project aims to reverse engineer Ace Of Spades 1.x libraries, focusing on packets and server logic with the goal of remaking a server for the game.

## Project Status

Current decompilation progress:
- **shared.packet**: 88/125 functions completed (70.4%)
- **shared.bytes**: 3/3 classes completed (100%)

## Setup Requirements

### Python Versions
You will need both Python versions to test properly:
- **Python 3.x** (64-bit recommended) - For testing our new implementation
- **Python 2.7** (32-bit required) - For testing against the original implementation

⚠️ **IMPORTANT**: Python 2.7 MUST be 32-bit to properly interact with the original library!

### Setting Up the Original Library

1. Create an `aosdump` folder in the project root
2. Copy the original Ace Of Spades library files into this folder with the following structure:
   ```
   aosdump/
     ├── aoslib/
     │    └── ... (original aoslib files)
     └── shared/
          └── ... (original shared files)
   ```
3. The original files should be from Ace Of Spades 1.x

## Testing

To test the implementation:

1. For testing against the original implementation (Python 2.7):
   ```
   py2 ./test_packets.py
   ```

2. For testing our new implementation (Python 3):
   ```
   py ./test_packets.py
   ```

The test script automatically adjusts paths based on the Python version to test the appropriate implementation.

## Project Structure

- **aosdump/** - Contains the original compiled binary (YOU NEED TO ADD THIS)
- **aoslib/** - Our new implementation of the game library
- **shared/** - Our new implementation of shared components
- **build/** - Compiled versions of our new implementation
- **test_packets.py** - Test script for comparing original vs new implementations

## Development Workflow

1. Study the original packet structure in the aosdump implementation
2. Implement equivalent functionality in our new codebase
3. Test binary compatibility between old and new implementations
4. Add new test cases as needed

## Contribution

Contributions are welcome! If you'd like to help with the reverse engineering effort:

1. Pick a packet type that hasn't been implemented yet
2. Create a test function in test_packets.py
3. Implement the packet class in the appropriate module
4. Ensure binary compatibility with the original implementation
5. Submit a pull request
