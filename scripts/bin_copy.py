from steam_app_info import *
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

try:
    os.mkdir(dist_dir)
except:
    pass

try:
    sdk_base_handle = SteamAppInfo(243730)
except SteamAppInfoException:
    print("Could not find SourceSDK 2013! Binary cant be copied.")

sdk_path = sdk_base_handle.get_app_path()

bin_dir = os.path.join(sdk_path, "bin")

try:
    for bin_file in bin:
        src_path = os.path.join(bin_dir, bin_file)
        dest_path = os.path.join(dist_dir, bin_file)
        shutil.copyfile(src=src_path, dst=dest_path)
    shutil.copytree(os.path.join(sdk_path, "platform", "resource"), dist_dir+"/resource")
    
    proj_bin_path = os.path.join(proj_bin, build_type)
    bin_list = os.listdir(proj_bin_path)
    for file in bin_list:
        if(file.endswith(".exe") or file.endswith(".dll")):
            shutil.move(src=os.path.join(proj_bin_path, file), dst=os.path.join(dist_dir, file))
    
except Exception:
    pass