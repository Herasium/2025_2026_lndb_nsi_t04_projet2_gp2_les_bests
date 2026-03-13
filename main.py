#  Imports
# -------------------------------------------------
from modules.ui import Window, EditorView, MainMenuView # Menus
from modules.data import data # Global Shared Data
from modules.data.loader import Loader # Data Loading
from modules.logger import Logger # Debuging
import arcade # Game Engine
import os
# -------------------------------------------------

arcade.enable_timings() #Debug informations for stress test (fps,delta_time)
path = os.path.dirname(os.path.abspath(__file__)) # The path for data loading, such as saves and levels.

data.current_path = path

logger = Logger("Main") # Little logger for debug informations
loader = Loader() # Data loader, critical part.

logger.print(f"Logic Box, v.{data.VERSION}.") # Simple debug info, regarding the version stored in data.
logger.print(f"Current path: {path}")

windows = Window() # Window creation, needed to bake the textures.
data.window = windows
logger.print("Created Window.")

loader.load() #Load process of all data, saves, levels and textures.

view = MainMenuView() # Launching instance of the main menu
 
windows.display(view)
windows.run() # Game Launch.
