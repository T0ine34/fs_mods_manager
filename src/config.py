import sys
import os

from json5 import load, dump

from gamuLogger import Logger

# CONFIG_FILE_PATH = os.environ["APPDATA"] + "\\mod_manager\\config.txt" if sys.platform == "win32" else os.environ["HOME"] + "/.config/mod_manager/config.txt"
CONFIG_FILE_PATH = os.environ["APPDATA"] + "\\mod_manager\\config.json"

Logger.setModule("config")

class Config:
    __instance = None
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Config, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance
    
    def __init__(self):
        if self.__initialized: return
        self.__initialized = True
        
        self.__config = {}
        self.__load()
        
        Logger.info("Config initialized")
        
        
    def __load(self):
        """Load the config from the config file"""
        try:
            with open(CONFIG_FILE_PATH) as file:
                self.__config = load(file)
        except FileNotFoundError:
            Logger.warning("Config file not found, creating a new one")
            os.makedirs(os.path.dirname(CONFIG_FILE_PATH), exist_ok=True)
            self.__save()
        except Exception as e:
            Logger.error(f"Could not load config file : {e}")
    
    
    def __save(self):
        """Write the config to the config file in json format"""
        with open(CONFIG_FILE_PATH, "w") as file:
            dump(self.__config, file,
                    indent=4,
                    sort_keys=True,
                    ensure_ascii=False,
                    quote_keys=True,
                    trailing_commas=False,
                    allow_duplicate_keys=False
                )
            
                
    def get(self, key : str, default = None, setDefault = False):
        """
        Get a value from the config file, if the key is not found, return the default value
        Write the default value to the config file if setDefault is True
        """
        if key not in self.__config:
            if setDefault:
                self.set(key, default)
            return default
        return self.__config[key]
    
    
    def set(self, key : str, value):
        """Set a value in the config file"""
        self.__config[key] = value
        self.__save()
        
        
    def __contains__(self, key : str):
        return key in self.__config
    
    
    def keys(self):
        return self.__config.keys()