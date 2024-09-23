try:
    from .ui import UI
except ImportError:
    from ui import UI

from gamuLogger import Logger, LEVELS


try:
    ui = UI()
    ui.mainloop()
except Exception as e:
    Logger.critical(f"An error occured: {e}")