import tkinter as tk
from tkinter import ttk
from ttkthemes import ThemedTk
from PIL import Image, ImageTk
import os

try:
    from .modStack import ModStack
    from .config import Config
    from .tk_mod import ModWidget
except ImportError:
    from modStack import ModStack
    from config import Config
    from tk_mod import ModWidget
    
    
class ScrollableFrame(ttk.Frame):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        
        self.__canvas = tk.Canvas(self)
        self.__canvas.pack(side="left", fill="both", expand=True)
        
        self.__scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.__canvas.yview)
        self.__scrollbar.pack(side="right", fill="y")
        
        self.__canvas.configure(yscrollcommand=self.__scrollbar.set)
        
        self.__content = ttk.Frame(self.__canvas)
        self.__contentID = self.__canvas.create_window((0, 0), window=self.__content, anchor="nw")
        
        self.__content.bind("<Configure>", self.__onFrameConfigure)
        self.__canvas.bind("<Configure>", self.__onCanvasConfigure)
        
        self.bind("<MouseWheel>", self.__onMouseWheel)
        
    def __onFrameConfigure(self, event):
        self.__canvas.configure(scrollregion=self.__canvas.bbox("all"))
        
    def __onCanvasConfigure(self, event):
        self.__canvas.itemconfig(self.__contentID, width=event.width)
        
    def __onMouseWheel(self, event):
        self.__canvas.yview_scroll(-1*(event.delta//120), "units")
        
    def getContent(self):
        return self.__content
    

class ModStackWidget(ttk.Frame):
    def __init__(self, master, stack : ModStack):
        super().__init__(master)
        self.__stack = stack
        
        self.__startIndex = 0 # the index of the first mod to display
        self.__endIndex = 18 # the index of the last mod to display( not included)
        
        self.__createWidgets()
        
    def __createWidgets(self):
        self.__navbar = ttk.Frame(self)
        self.__navbar.pack(fill="x")
        self.__navbar.grid_columnconfigure(0, weight=1)
        self.__name = ttk.Label(self.__navbar, text=self.__stack.getName())
        self.__name.grid(row=0, column=0)
        
        self.__enableButton = ttk.Button(self.__navbar, text="Enable", command=self.__enable)
        self.__enableButton.grid(row=0, column=1)
        
        self.__disableButton = ttk.Button(self.__navbar, text="Disable", command=self.__disable)
        self.__disableButton.grid(row=0, column=2)
        
        self.__mods = ScrollableFrame(self)
        self.__mods.pack(fill="both", expand=True)
        
        self.__createModWidgets()
        
    def __clearModWidgets(self):
        for widget in self.__mods.getContent().winfo_children():
            widget.destroy()
        
    def __createModWidgets(self):
            start = max(0, self.__startIndex)
            end = min(len(self.__stack), self.__endIndex)
            for i in range(start, end):
                Logger.debug(f"({i+1}/{len(self.__stack)})\tCreating widget for mod {self.__stack.getModByIndex(i).zippath}")
                mod = self.__stack.getModByIndex(i)
                modWidget = ModWidget(self.__mods.getContent(), mod)
                modWidget.grid(row=i//5, column=i%5, padx=5, pady=5, sticky="nsew")
                
    def setPage(self, page : int):
        self.__startIndex = page * 18
        self.__endIndex = (page + 1) * 18
        self.__clearModWidgets()
        self.__createModWidgets()
        
        # for i, mod in enumerate(self.__stack.content()):
        #     Logger.debug(f"({i+1}/{len(self.__stack)})\tCreating widget for mod {mod.zippath}")
        #     modWidget = ModWidget(self.__mods, mod)
        #     modWidget.grid(row=i, column=0)
            
    def __enable(self):
        self.__stack.enable()
        
    def __disable(self):
        self.__stack.disable()
        
        
if __name__ == "__main__":
    from gamuLogger import Logger, LEVELS
    
    Logger.setLevel("stdout", LEVELS.DEBUG)
    stack = ModStack(os.path.join(Config().get("stack_folder"), "mods crane"))
    root = ThemedTk()
    root.set_theme("arc")
    root.geometry("600x400")
    
    modStackWidget = ModStackWidget(root, stack)
    modStackWidget.pack(fill="both", expand=True)
    
    root.mainloop()
