#  Imports
# -------------------------------------------------
from modules.ui.window import Window
from modules.ui.main_menu.in_progress_view import MainMenuView
from modules.data import data  # Global shared data
from modules.data.loader import Loader  # Data loading
from modules.logger import Logger  # Debugging
import arcade  # Game engine
import os  # File system operations

# -------------------------------------------------

# Enable arcade's internal timing to track FPS and delta_time for debugging/stress testing
arcade.enable_timings()

# Get the directory path of the current script file for data loading (saves, levels, etc.)
path: str = os.path.dirname(os.path.abspath(__file__))

# Set the current path in the global data object
data.current_path = path

# Initialize a logger instance for debugging purposes
logger: Logger = Logger("Main")

# Initialize the data loader, responsible for loading all game assets, saves, and levels
loader: Loader = Loader()

# Print the game version and current path for debug purposes
logger.print(f"Logic Box, v.{data.VERSION}.")  # Version info from data
logger.print(f"Current path: {path}")  # Current working directory

# Create the main game window (handles textures and display)
windows: Window = Window()
data.window = windows  # Store the window instance in global data
logger.print("Created Window.")  # Confirm window creation in logs

# Load all necessary game data (levels, saves, textures)
loader.load()  # Critical step for initializing game content

# Instantiate the main menu view (first UI displayed to the player)
view: MainMenuView = MainMenuView()

# Display the main menu view in the game window
windows.display(view)

# Start the game loop (blocks execution and runs the arcade window)
windows.run()
