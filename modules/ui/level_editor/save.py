
import arcade

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text

from modules.data import data

from pyglet.graphics import Batch


class SaveFrame(arcade.View):

    def __init__(self,level):
        super().__init__()

        self.background_color = arcade.color.BLACK
        self.texts = []
        self.level = level
        self.setup()

    def setup(self):
        self.texts = []
        debug_list = [
            "Level Saver",
            "<- Back",
            "--------------",
            f"Level {self.level.id} {self.level.name}",
            f"Level Description : ",
            self.level.description,
            "--------------",
            f"Level Time : {self.level.time}",
            "+ 30 sec",
            " - 30 sec",
            "--------------",
            f"Level Number : {self.level.number}",
            "+ 1",
            "- 1",
            "--------------",
            f"Level Category : {self.level.category}",
            "+ 1",
            "- 1",
            "--------------",
            f"Level Color : {data.level_colors[self.level.color]}",
            "->",
            f"--> Save <--"
        ]



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

        if self.texts[1].touched:
            data.window.back()

        if self.texts[8].touched:
            self.level.time += 30
            self.setup()

        if self.texts[9].touched:
            self.level.time -= 30
            self.setup()

        if self.texts[12].touched:
            self.level.number += 1
            self.setup()

        if self.texts[13].touched:
            self.level.number -= 1
            self.setup()

        if self.texts[16].touched:
            self.level.category += 1
            self.setup()

        if self.texts[17].touched:
            self.level.category -= 1
            self.setup()

        if self.texts[20].touched:
            self.level.color = (self.level.color + 1) % len(data.level_colors)
            self.setup()

        if self.texts[21].touched:
            self.level.save()

    def on_mouse_release(self, x, y, button, key_modifiers):
        pass




    def get_save_gate_counts(self):
            result = {}
            for i in self.level.chip.gates:
                if not self.level.chip.gates[i].gate_type in result:
                    result[self.level.chip.gates[i].gate_type] = 0
                result[self.level.chip.gates[i].gate_type] += 1
            return result
