"""
aEntry point for the Logic Box application.

This module initializes the core game systems, including logging, data loading,
and the primary window management, before launching the initial UI view.
"""

from modules.ui.window import Window
from modules.ui.main_menu.in_progress_view import MainMenuView
from modules.data import data
from modules.data.loader import Loader
from modules.logger import Logger
import arcade

arcade.enable_timings()

logger: Logger = Logger("Main")
loader: Loader = Loader()

logger.print(f"Logic Box, v.{data.VERSION}.")
logger.print(f"Current path: {data.current_path}")

try:
    data.load()
    logger.print("Loaded Preferences.")
except Exception as e:
    logger.warning(f"Failed to load preferences, back to default. {e}")

windows: Window = Window()
data.window = windows
logger.print("Created Window.")

loader.load()

Main: MainMenuView = MainMenuView()
Pause: MainMenuView = MainMenuView(pause=True)

data.main = Main
data.pause = Pause

windows.display(Main)

windows.run()
