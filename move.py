import shutil
import os

source = "mavproxy_customui"
dest = "venv/Lib/site-packages/MAVProxy/modules/mavproxy_customui"

# Ensure the destination folder exists
os.makedirs(dest, exist_ok=True)

# Copy the entire folder
shutil.copytree(source, dest, dirs_exist_ok=True)

print(f"Copied {source} to {dest}")
