import arcade

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text
from modules.ui.toolbox.entity import Entity

from modules.data import data

from pyglet.graphics import Batch

from modules.ui.level_player.view import LevelPlayer

from modules.logger import Logger

logger = Logger("LevelList")

class LevelList(arcade.View):

    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.BLACK
        self.texts = []
        self.levels = []
        self.camera_y = 0
        self.setup()

    def setup(self):
        
        self.bg = Entity(0,0,1920,1088,arcade.Sprite(data.background_grid_texture))
        self.border = Entity(0,0,1920,960,data.border_small)
        self.title = Entity(0,952,1920,128,data.name_banner)

        self.buttons = {}
        self.texts = []

        levels = []
        for i in data.loaded_levels:
            levels.append(i)

        def sort_keys(i):
            return data.loaded_levels[i].number
        
        levels.sort(key=sort_keys)

        pos_y = 600 + self.camera_y
        pos_x = 75

        current_category = data.loaded_levels[levels[0]].category

        for i in levels:
            level = data.loaded_levels[i]

            if level.category != current_category:
                pos_y -= 300
                pos_x = 75
                current_category = level.category

            button = arcade.Sprite(arcade.Texture(data.LEVEL_BUTTONS.get(level.id)))

            self.buttons[level.id] = Entity(x=pos_x,y=pos_y,width=175,height=175,sprite=button)
            pos_x += 200

        c = 0
        for i in data.categories:
            self.texts.append(Text(x=75,y=800-c*300 + self.camera_y,width=100,height=300,text=i,align=("left","center")))
            c += 1

    def reset(self):
        pass

    def on_draw(self):
        self.clear()
        self.bg.draw()

        for i in self.buttons:
            self.buttons[i].draw()

        for i in self.texts:
            i.draw()

        self.border.draw()
        self.title.draw()

    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, key_modifiers):
        if key == 97:
            data.window.back()


    def on_key_release(self, key, key_modifiers):
        pass

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        mouse.position = (x,y)


    def on_mouse_press(self, x, y, button, key_modifiers):
        
        for i in self.buttons:
            if self.buttons[i].touched:
                logger.success(f"Launching Level {i}")
                data.window.display(LevelPlayer(i))

    def on_mouse_scroll(self,x,y,scroll_x,scroll_y):
        self.camera_y += scroll_y * 15
        self.camera_y = max(self.camera_y,0)
        self.setup()
    def on_mouse_release(self, x, y, button, key_modifiers):
        pass


