from modules.ui import Window, EditorView, MainMenuView
from modules.data import data
from modules.data.loader import Loader
from modules.logger import Logger
import arcade 
import os

arcade.enable_timings()
path = os.path.dirname(os.path.abspath(__file__)) 

data.current_path = path

logger = Logger("Main")
loader = Loader()

logger.print(f"Logic Box, v.{data.VERSION}.")
logger.print(f"Current path: {path}")

windows = Window()
data.window = windows
logger.print("Created Window.")

loader.load()

view = MainMenuView()

windows.display(view)
windows.run()
