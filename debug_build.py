import subprocess
import sys

print("Starting build...")
with open('build_log_py.txt', 'w') as f:
    try:
        subprocess.check_call([sys.executable, 'setup.py', 'build_ext', '--inplace'], stdout=f, stderr=subprocess.STDOUT)
        print("Build successful")
    except subprocess.CalledProcessError:
        print("Build failed")
