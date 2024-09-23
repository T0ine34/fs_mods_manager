import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import os

try:
    from .mod import Mod
except ImportError:
    from mod import Mod
    

def resizeText(text : str, maxLineLength : int):
    """
    Add new lines to the text to make sure no line is longer than maxLineLength
    Split on spaces
    """
    lines = []
    while text:
        if len(text) <= maxLineLength:
            lines.append(text)
            break
        else:
            splitIndex = text.rfind(" ", 0, maxLineLength)
            if splitIndex == -1:
                splitIndex = maxLineLength
            lines.append(text[:splitIndex])
            text = text[splitIndex+1:]
    return "\n".join(lines)


class ModWidget(ttk.Frame):
    def __init__(self, master, mod : Mod):
        super().__init__(master, width=200, height=400)
        self.__mod = mod
        
        #create a border around the widget
        self.config(borderwidth=2, relief="groove")
        self.grid_propagate(False)
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.__createWidgets()
        
    def __createWidgets(self):
        icon = Image.open(self.__mod.iconPath)
        icon.thumbnail((128, 128))
        icon = ImageTk.PhotoImage(icon)
        self.__iconLabel = ttk.Label(self, image=icon, compound=tk.CENTER)
        self.__iconLabel.grid(row=0, column=0, columnspan=2, padx=5, pady=5)
        self.__iconLabel.image = icon
        
        self.__title = ttk.Label(self, text=resizeText(self.__mod.title, 20), font=("Arial", 12, "bold"), justify="center")
        
        self.__title.grid(row=1, column=0, columnspan=2)
        
        self.__author = ttk.Label(self, text=resizeText(self.__mod.author, 20))
        self.__author.grid(row=2, column=0)
        
        self.__version = ttk.Label(self, text=self.__mod.version)
        self.__version.grid(row=2, column=1)
        
        self.__description = ttk.Label(self, text=resizeText(self.__mod.description, 40))
        self.__description.grid(row=3, column=0, columnspan=2)
        
        
if __name__ == "__main__":
    from gamuLogger import Logger, LEVELS
    
    Logger.setLevel("stdout", LEVELS.DEBUG)
    mod = Mod(r"E:\Code\fs_mods_manager\Ford Mustang.zip")
    root = ThemedTk()
    root.set_theme("arc")
    root.geometry("600x400")
    modWidget = ModWidget(root, mod)
    modWidget.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
    root.mainloop()