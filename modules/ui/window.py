
import arcade
from modules.data import data

class Window():

    def __init__(self):
        
        self.width = data.WINDOW_WIDTH
        self.height = data.WINDOW_HEIGHT
        self.title = "Starting Template"

        self.window = arcade.Window(self.width, self.height, self.title,fullscreen=data.WINDOW_FULLSCREEN)

    def run(self):
        arcade.run()

    def display(self,view: arcade.View):
        self.window.show_view(view)

    def hide(self):
        self.window.hide_view()