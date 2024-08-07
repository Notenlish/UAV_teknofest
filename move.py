import os
import shutil

source = "mavproxy_customui"
dest = "venv/Lib/site-packages/MAVProxy/modules/mavproxy_customui"

home_dir = os.path.expanduser("~")
# fmt: off
dest2 = os.path.join(home_dir, "AppData", "Local", "Programs", "Python", "Python311", "Lib", "site-packages", "MAVProxy", "modules", "mavproxy_customui")
# fmt: on
dest3 = "MAVProxy/build/lib/MAVProxy/modules/maproxy_customui"
dest4 = "MAVProxy/MAVProxy/modules/mavproxy_customui"

os.makedirs(dest, exist_ok=True)

shutil.copytree(source, dest, dirs_exist_ok=True)
shutil.copytree(source, dest2, dirs_exist_ok=True)
shutil.copytree(source, dest3, dirs_exist_ok=True)
shutil.copytree(source, dest4, dirs_exist_ok=True)

print(f"Copied {source} to {dest}. And also to 3 other places because why not :shrug:")
