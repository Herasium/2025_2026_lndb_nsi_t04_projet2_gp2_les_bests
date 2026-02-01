import arcade

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text

from modules.data import data

from pyglet.graphics import Batch

from modules.ui.editor.view import EditorView
from modules.ui.level_editor.view import LevelEditorView
from modules.ui.debug_display_all_tiles.view import DebugTilesView
from modules.ui.main_menu.settings_view import SettingView

class LevelEditorSelector(arcade.View):

    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.BLACK
        self.texts = []
        self.levels = []
        self.setup()

    def setup(self):
        debug_list = [
            "Level Editor Selector",
            "<- Back",
            "+ New +",
            ""
        ]

        for i in data.loaded_levels:
            level = data.loaded_levels[i]
            debug_list.append(f"Level {level.number} {level.name} #{level.id}")
            self.levels.append(i)

        start_y = 1080-70
        
        for index, item in enumerate(debug_list):
            self.texts.append(Text())
            self.texts[-1].x = 64
            self.texts[-1].y = start_y - (index * 25)
            self.texts[-1].text = item
            self.texts[-1].align = ("left","center")


    def reset(self):
        pass

    def on_draw(self):
        self.clear()

        for i in self.texts:
            i.draw()
            i.hitbox.draw()


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
        
        for index in range(len(self.texts)):
            text = self.texts[index]

            if text.touched:
                if index > 3:
                    data.window.display(LevelEditorView(self.levels[index-4]))
                elif index == 1:
                    data.window.back()
                elif index == 2:
                    data.window.display(LevelEditorView())

    def on_mouse_release(self, x, y, button, key_modifiers):
        pass


