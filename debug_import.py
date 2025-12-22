import sys
import os
import traceback
sys.path.append(os.getcwd())
sys.stdout.reconfigure(encoding='utf-8')
try:
    # std imports

        import shared.constants
        print("Imported shared.constants", flush=True)
        import shared.packet
        print("Imported shared.packet", flush=True)
        import aoslib.world
        print("Imported aoslib.world", flush=True)
        import server.connection
        print("Imported server.connection", flush=True)
        import server.protocol
        print("Imported server.protocol", flush=True)
        print("Success all", flush=True)
except Exception:
    with open('debug_error.txt', 'w') as f:
        traceback.print_exc(file=f)
    print("FAILED")
    traceback.print_exc()
