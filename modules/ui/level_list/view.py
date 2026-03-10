import arcade

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text

from modules.data import data

from pyglet.graphics import Batch

from modules.ui.level_player.view import LevelPlayer

class LevelList(arcade.View):

    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.BLACK
        self.texts = []
        self.levels = []
        self.setup()

    def setup(self):
        pass

    def reset(self):
        pass

    def on_draw(self):
        self.clear()


    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, key_modifiers):
        if key == 97:
            arcade.exit()


    def on_key_release(self, key, key_modifiers):
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        mouse.position = (x,y)


    def on_mouse_press(self, x, y, button, key_modifiers):
        pass


    def on_mouse_release(self, x, y, button, key_modifiers):
        pass


