import os
import sys

class SteamAppInfoException(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)
        
class SteamNotFound(SteamAppInfoException):
    def __init__(self, *args: object) -> None:
        super().__init__("Steam is either not found or is not installed on this system.")
        
class SteamAppNotFound(SteamAppInfoException):
    def __init__(self, *args: object) -> None:
        super().__init__("Steam app not found")
        
class OSUnsupported(SteamAppInfoException):
    def __init__(self, *args: object) -> None:
        super().__init__("This system is not currently supported. Only Windows is supported at the moment.")
    
def check_compatibility():
    if(not sys.platform.startswith("win32")):
        raise OSUnsupported()
    
check_compatibility()

import winreg
import vdf

def example():
    try:
        steam_app = SteamAppInfo(243730)
        state : dict = steam_app.get_app_state()
        message = "The game \"{gname}\" is {neg} running.".format(gname=state[SteamAppInfo.NAME_KEY], neg="not" if str(state[SteamAppInfo.RUNNING_KEY])=="0" else "\b")
        print(message)
        print(steam_app.get_app_path())
    except SteamAppInfoException as stnf:
        print(stnf.args)

class SteamAppInfo:
    
    INSTALLED_KEY = "Installed"
    CLOUD_KEY = "Cloud"
    NAME_KEY = "Name"
    RUNNING_KEY = "Running"
    UPDATING_KEY = "Updating"
    INSTALLTIONS_FILE = "libraryfolders.vdf"
    STEAMAPPS_FOLDER_NAME = "steamapps"
    STEAM_REGKEY_PATH = "Software\\Valve\\Steam"
        
    def __init__(self, appid: int):
        check_compatibility()
        self.appid : int = appid
        self.appid_str : str = str(appid)
        
    def get_steam_path() -> str: #static
        try:
            handle = winreg.OpenKey(winreg.HKEY_CURRENT_USER, SteamAppInfo.STEAM_REGKEY_PATH)
        except OSError:
            raise SteamNotFound()
        path = winreg.QueryValueEx(handle, "SteamPath")
        winreg.CloseKey(handle)
        return path[0]
    
    def get_app_state(self) -> dict:
        res : dict = {}
        
        #Check if Steam is installed in the system
        SteamAppInfo.get_steam_path()
        
        reg_app_path : str = self.__get_steam_app_info_path()
        try:
            key : winreg.HKEYType = winreg.OpenKey(winreg.HKEY_CURRENT_USER, reg_app_path)
        except OSError:
            raise SteamAppNotFound()
        
        index : int = 0
        while(True):
            try:
                value : tuple = winreg.EnumValue(key, index)
                res[value[0]] = value[1]
                index += 1
            except OSError:
                break

        winreg.CloseKey(key)
        
        return res
    
    def __get_dict_num_keys(self, di : dict) -> int:
        return len(list(di))
    
    def __find_installation_folder(self, vdf : dict) -> str:
        final : str = None
        iterable : dict = vdf["libraryfolders"]
        for i in range(self.__get_dict_num_keys(iterable)):
            obj : dict = list(iterable.values())[i]
            apps_iterable : dict = obj["apps"]
            for j in range(self.__get_dict_num_keys(apps_iterable)):
                if(list(apps_iterable)[j] == str(self.appid_str)):
                    final = obj["path"]
        return final
    
    def get_app_path(self) -> str:
        st_path = os.path.join(SteamAppInfo.get_steam_path(), SteamAppInfo.STEAMAPPS_FOLDER_NAME)

        folders_vdf : str = os.path.join(st_path, SteamAppInfo.INSTALLTIONS_FILE)
        fld_handle = vdf.load(open(folders_vdf))
        
        lib_drive : str = self.__find_installation_folder(fld_handle)
        
        if(lib_drive is None):
            raise SteamAppNotFound()
        
        lib_games_foler : str = os.path.join(lib_drive, SteamAppInfo.STEAMAPPS_FOLDER_NAME)
        
        game_lib_path : str = os.path.join(lib_games_foler, f"appmanifest_{self.appid_str}.acf")
        
        appmanifest_vdf : dict = vdf.load(open(game_lib_path))
        install_dir : str = appmanifest_vdf["AppState"]["installdir"]
        return os.path.join(lib_games_foler, "common", install_dir)
        
        
    def __get_steam_app_info_path(self) -> str:
        return f"{SteamAppInfo.STEAM_REGKEY_PATH}\\Apps\\{str(self.appid)}"
    
if __name__ == "__main__":
    example()