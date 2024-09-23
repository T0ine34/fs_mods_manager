import sys, os
import shutil

from gamuLogger import Logger, LEVELS

try:
    from .config import Config
    from .mod import Mod
except ImportError:
    from config import Config
    from mod import Mod

Logger.setModule("modStack")

# C:\Users\antoi\Documents\My Games\FarmingSimulator2022
GAME_MODS_FOLDER = Config().get("game_mods_folder", os.path.expanduser("~") + "/Documents/My Games/FarmingSimulator2022/mods", True)

Logger.debug(f"Game mods folder: {GAME_MODS_FOLDER}")

def runCommand(command : str, cwd : str = None) -> int:
    if cwd is not None:
        Logger.debug(f"Running command {command} in {cwd}")
        currentDir = os.getcwd()
        os.chdir(cwd)
    else:
        Logger.debug(f"Running command {command}")
    returnCode = os.system(f"{command} > nul 2>&1")
    if cwd is not None:
        os.chdir(currentDir)
    
    if returnCode != 0:
        Logger.error(f"Command {command} in {cwd} returned {returnCode}")
        
    return returnCode

class ModStack:
    """
    A collection of mods that can be enabled or disabled without having to move files around
    """
    __instances = {} #type: dict[str, ModStack]
    def __init__(self, folder : str):
        if folder in ModStack.__instances:
            raise Exception("ModStack already exists for this folder")
        self.__folder = folder
        self.__mods = {} #type: dict[str, Mod]
        self.__name = os.path.basename(folder)
        self.__load()
        
        ModStack.__instances[folder] = self
        
    def __loadMod(self, file : str, failedMods : list[str]):
        if file.endswith(".zip"):
            try:
                self.__mods[file] = Mod(os.path.join(self.__folder, file))
            except Exception as e:
                failedMods.append(file)
                Logger.error(f"Could not load mod {file} : {e}")
        
    def __load(self):
        Logger.info(f"Loading mods from {self.__folder} (this may take a while)")
        nbMods = len(os.listdir(self.__folder))
        failedMods = []
        for file in os.listdir(self.__folder):
            self.__loadMod(file, failedMods)

        Logger.info(f"Loaded {nbMods - len(failedMods)}/{nbMods} mods from {self.__folder}")
        if failedMods:
            Logger.debug(f"Failed mods : {failedMods}")
            
            
    def __update(self):
        """
        Update the mod stack (check if mods have been added or removed)
        Load new mods and remove deleted ones
        """
        Logger.info(f"Updating {self.__folder}")
        nbMods = len(os.listdir(self.__folder))
        failedMods = []
        for file in os.listdir(self.__folder):
            if file in self.__mods.keys():
                continue # Mod already loaded
            self.__loadMod(file, failedMods)
        for file in self.__mods.keys():
            if file not in os.listdir(self.__folder):
                del self.__mods[file]
        Logger.info(f"Updated {self.__folder} : {nbMods - len(failedMods)}/{nbMods} mods")
            
            
    def enable(self):
        ModStack.disable()
        runCommand(f'mklink /J "{GAME_MODS_FOLDER}" "{self.__folder}"', os.path.dirname(self.__folder))
        Logger.info(f"Enabled {self.__folder}")
        
    @staticmethod
    def disable():
        if os.path.exists(GAME_MODS_FOLDER):
            os.unlink(GAME_MODS_FOLDER)
        # runCommand(f'rmdir "{GAME_MODS_FOLDER}"')
        Logger.info(f"Disabled current mod stack")
        
    def __str__(self) -> str:
        return "ModStack " + self.__name
    
    def getName(self) -> str:
        return self.__name
    
    def addMod(self, archivePath : str):
        """
        Add a mod to the stack (copy it into the folder)
        """
        if not archivePath.endswith(".zip"):
            raise ValueError("Only zip archives are supported")
        if not os.path.exists(archivePath):
            raise FileNotFoundError(f"Archive {archivePath} not found")
        if archivePath in self.__mods:
            raise ValueError(f"Mod {archivePath} is already in the stack (use updateMod instead if you want to update it)")
        shutil.copy(archivePath, self.__folder)
        self.__update()
        
    def updateMod(self, archivePath : str):
        """
        Update a mod in the stack
        """
        if not archivePath.endswith(".zip"):
            raise ValueError("Only zip archives are supported")
        if not os.path.exists(archivePath):
            raise FileNotFoundError(f"Archive {archivePath} not found")
        if archivePath in self.__mods:
            raise ValueError(f"Mod {archivePath} is not in the stack (use addMod instead if you want to add it)")
        shutil.copy(archivePath, self.__folder)
        self.__update()
        
    def removeMod(self, modName : str):
        """
        Remove a mod from the stack
        """
        os.remove(os.path.join(self.__folder, modName))
        self.__update()
        
    def getModByIndex(self, index : int) -> Mod:
        return list(self.__mods.values())[index]
        
    def __len__(self):
        return len(self.__mods)

if __name__ == "__main__":
    Logger.setLevel("stdout", LEVELS.INFO)
    
    try:
        old = ModStack(r"C:\Users\antoi\Games\mods\mods_old")
        crane = ModStack(r"C:\Users\antoi\Games\mods\mods crane")
        old.enable()
    except Exception as e:
        Logger.critical(' '.join(e.args))
        sys.exit(1)