import arcade
import math

from modules.data.node import Node
from modules.data.gate import Gate

from modules.data import data
from line_profiler import profile


class Complex(Gate):

    def __init__(self, id):
        super().__init__(id)

        self.name = "COMP"
        self.type = "Complex"
        self.gate_type = "COMP"
        self.draw_hitboxes = True

        self.inputs = []
        self.outputs = []
        self.inputs_sizes = []
        self.outputs_sizes = []

        self.calculate_display()
        self.gen_tile_pattern()
        


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

        arcade.draw_rect_filled(rect,arcade.color.RED)
