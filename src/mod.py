from zipfile import ZipFile
import os

from gamuLogger import Logger

try:
    from .moddesc import ModDesc
except ImportError:
    from moddesc import ModDesc
    
TEMP_FOLDER = os.path.join(os.environ["TEMP"], "mod_manager")
os.makedirs(TEMP_FOLDER, exist_ok=True)
    
Logger.setModule("mod")

class Mod:
    def __init__(self, zippath : str):
        Logger.debug(f"Loading mod {zippath}")
        self.zippath = zippath
        self.__zipfile = ZipFile(zippath)
        Logger.deepDebug(f"Zipfile opened")
        self.__moddesc = ModDesc(self.__zipfile.open("modDesc.xml"))
        Logger.deepDebug(f"ModDesc loaded")
        self.__iconPath = self.saveIcon()

        self.__zipfile.close() # Close the zipfile after we're done with it
        Logger.debug(f"Mod {zippath} loaded")

    def saveIcon(self):
        # copy the icon to the temp folder and return the path
        iconName = self.findRealIcon()
        iconPath = os.path.join(TEMP_FOLDER, iconName)
        os.makedirs(os.path.dirname(iconPath), exist_ok=True)
        with open(iconPath, "w+b") as file:
            file.write(self.__zipfile.open(iconName).read())
        Logger.debug(f"Icon saved to {iconPath}")
        return iconPath
        

    def findRealIcon(self):
        Logger.deepDebug(f"Finding real icon for mod {self.zippath}")
        if self.__moddesc.icon in self.__zipfile.namelist():
            Logger.deepDebug(f"Icon found (exact match)")
            return self.__moddesc.icon
        Logger.deepDebug(f"No exact match for icon {self.__moddesc.icon}, trying case insensitive")
        
        #try without case sensitivity
        for file in self.__zipfile.namelist():
            if file.lower() == self.__moddesc.icon.lower():
                Logger.deepDebug(f"Icon found (case insensitive) : {file}")
                return file
        Logger.deepDebug(f"No case insensitive match for icon {self.__moddesc.icon}, trying with the same name")
            
        #try with the same name, but with a different extension (dds, png, jpg, jpeg, ...)
        for file in self.__zipfile.namelist():
            if file.split(".")[0] == self.__moddesc.icon.split(".")[0]:
                Logger.deepDebug(f"Icon found (same name) : {file}")
                return file

        Logger.error(f"Could not find icon {self.__moddesc.icon} for mod {self.zippath}")
        raise FileNotFoundError(f"Could not find icon {self.__moddesc.icon} for mod {self.zippath}")
        
    @property
    def iconPath(self):
        return self.__iconPath
        
    def __getattr__(self, attr):
        return getattr(self.__moddesc, attr)