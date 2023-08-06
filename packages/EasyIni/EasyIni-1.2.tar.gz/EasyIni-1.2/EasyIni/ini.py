from ctypes import cdll,c_char_p,c_bool
import os
class Ini:
    def __init__(self) -> None:
        add_path = os.path.split(os.path.abspath(__file__))[0]+'\\'
        os.add_dll_directory(add_path) #添加dll搜索路径
        
    def get(self,section:str,key:str,words:str="") ->str:
        lib = cdll.LoadLibrary("inilib.dll")
        lib.gget.restype= c_char_p
        data = lib.gget(section.encode("utf-8"),key.encode("utf-8"),words.encode("utf-8"))
        return data.decode()
    def set(self,section:str,key:str,words:str="") ->bool:
        lib = cdll.LoadLibrary("inilib.dll")
        lib.sset.restype= c_bool
        data = lib.sset(section.encode("utf-8"),key.encode("utf-8"),words.encode("utf-8"))
        return data


