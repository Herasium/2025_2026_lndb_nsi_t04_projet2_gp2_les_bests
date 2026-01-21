from modules.ui import Window, EditorView, GameView
from modules.data import data
import arcade
import os

arcade.load_font("assets/press_start.ttf")

version = "0.12"
path = os.path.dirname(os.path.abspath(__file__)) 

data.current_path = path

print(f"Logic Box, v{version}.")
print(f"Current path: {path}")

windows = Window()
data.window = windows

view = GameView()

windows.display(view)
windows.run()
