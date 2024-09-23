import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk

try:
    from .manager import Manager
    from .config import Config
    from .modStack import ModStack
except ImportError:
    from manager import Manager
    from config import Config
    from modStack import ModStack

class UI(ThemedTk):
    def __init__(self):
        super().__init__()
        self.set_theme("equilux")

        self.title("Mod Manager")

        self.__manager = Manager()
        
        for stack in self.__manager.getStacksNames():
            self.__createStackButton(stack)
            
    def __createStackButton(self, stack : str):
        button = ttk.Button(self, text=stack, command=lambda: self.__enableStack(stack))
        button.pack()
        
    def __enableStack(self, stack : str):
        self.__manager.getStack(stack).enable()
