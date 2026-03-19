"""Entry point for the Logic Box application.

This module initializes the core game systems, including logging, data loading,
and the primary window management, before launching the initial UI view.
"""

from modules.ui.window import Window
from modules.ui.main_menu.in_progress_view import MainMenuView
from modules.ui.loading.view import LoadingScreen
from modules.data import data
from modules.data.loader import Loader
from modules.logger import Logger
import arcade
import os

arcade.enable_timings()

path: str = os.path.dirname(os.path.abspath(__file__))
data.current_path = path

logger: Logger = Logger("Main")
loader: Loader = Loader()

logger.print(f"Logic Box, v.{data.VERSION}.")
logger.print(f"Current path: {path}")

windows: Window = Window()
data.window = windows
logger.print("Created Window.")

windows.display(LoadingScreen())

loader.load()

view: MainMenuView = MainMenuView()
windows.display(view)

windows.run()
