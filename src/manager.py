try:
    from .modStack import ModStack
    from .config import Config
except ImportError:
    from modStack import ModStack
    from config import Config
    
import os   
from gamuLogger import Logger, LEVELS

Logger.setModule("manager")
    
class Manager:
    """
    The top-level class that manages every stack of mods
    """
    __instance = None #type: Manager
    
    def __new__(cls):
        if cls.__instance is None:
            cls.__instance = super(Manager, cls).__new__(cls)
            cls.__instance.__initialized = False
        return cls.__instance
    
    def __init__(self):
        if self.__initialized: return
        self.__initialized = True
        
        self.__stack_folder = Config().get("stack_folder")
        self.__stacks = {}
        
        Logger.info("Manager initialized")
        
        self.__load()
        
    def __load(self):
        Logger.info(f"Loading stacks from {self.__stack_folder}")
        for folder in os.listdir(self.__stack_folder):
            if os.path.isdir(os.path.join(self.__stack_folder, folder)):
                stack = ModStack(os.path.join(self.__stack_folder, folder))
                self.__stacks[stack.getName()] = stack
        Logger.info(f"{len(self.__stacks)} stacks loaded")
        
    
    def getStack(self, name : str) -> ModStack:
        if name not in self.__stacks:
            Logger.error(f"Stack {name} not found")
            raise KeyError(f"Stack {name} not found")
        return self.__stacks[name]
    
    def getStacksNames(self) -> list[str]:
        return [str(stack) for stack in self.__stacks.keys()]
    
    
if __name__ == "__main__":
    Logger.setLevel("stdout", LEVELS.INFO)
    manager = Manager()
    stack = manager.getStack("mods_old")
    stack.enable()
    stacks = manager.getStacks()
    Logger.info(f"Got stacks {stacks}")