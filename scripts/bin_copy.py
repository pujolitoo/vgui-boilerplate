from steam_app_info import *
from contextlib import suppress
import os
import sys
import shutil

bin = [
    "FileSystem_Stdio.dll",
    "vgui2.dll",
    "engine.dll",
    "vguimatsurface.dll",
    "tier0.dll",
    "vstdlib.dll"
]

cwdir = sys.argv[1]
proj_bin = sys.argv[2]

try:
    build_type = sys.argv[3]
except IndexError:
    build_type = "Debug"

dist_dir = os.path.join(cwdir, "dist")

with suppress(Exception):
    os.mkdir(dist_dir)

try:
    sdk_base_handle = SteamAppInfo(243730)
except SteamAppInfoException:
    print("Could not find SourceSDK 2013! Binary cant be copied.")

sdk_path = sdk_base_handle.get_app_path()

bin_dir = os.path.join(sdk_path, "bin")

for bin_file in bin:
    src_path = os.path.join(bin_dir, bin_file)
    dest_path = os.path.join(dist_dir, bin_file)
    with suppress(Exception):
        shutil.copyfile(src=src_path, dst=dest_path)
    
try:
    shutil.copytree(os.path.join(sdk_path, "platform", "resource"), dist_dir+"/resource")
except:
    pass
    
proj_bin_path = os.path.join(proj_bin, build_type)
bin_list = os.listdir(proj_bin_path)
for file in bin_list:
    if(file.endswith(".exe") or file.endswith(".dll")):
        dest_path = os.path.join(dist_dir, file)
        if(os.path.isfile(dest_path)):
            os.remove(dest_path)
        shutil.move(src=os.path.join(proj_bin_path, file), dst=os.path.join(dist_dir, file))
    