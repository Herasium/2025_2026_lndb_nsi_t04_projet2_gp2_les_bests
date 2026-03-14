import arcade
import math

from modules.data.node import Node
from modules.ui.toolbox.hitbox import HitBox
from modules.ui.toolbox.entity import Entity
from modules.ui.mouse import mouse
from modules.data import data
from modules.data.gate import Gate

from line_profiler import profile


class Output(Gate):

    def __init__(self, id):
        super().__init__(id)

        self.name = "OUT"
        self.type = "Output"
        self.gate_type = "8Output"

        self.inputs = [0]
        self.outputs = []
        self.inputs_sizes = [8]
        self.outputs_sizes = []

        self.exceptional_size_offset = 2

        self.gen_tile_pattern()
        self.calculate_display()


    def draw_tiles(self):
    
        width = self.tile_width
        height = 4

        tile_x = self.x + self._camera[0]
        tile_y = self.y + self._camera[1]

        rect = arcade.XYWH(
                    x=tile_x,
                    y=tile_y,
                    width=width * data.UI_EDITOR_GRID_SIZE,
                    height=height * data.UI_EDITOR_GRID_SIZE,
                    anchor=arcade.Vec2(0,0)
        )

        arcade.draw_rect_filled(rect,arcade.color.YELLOW)
        arcade.draw_text(f"Output: {self.inputs}",tile_x,tile_y,arcade.color.WHITE)
