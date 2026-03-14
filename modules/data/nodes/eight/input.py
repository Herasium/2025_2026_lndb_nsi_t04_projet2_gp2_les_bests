import arcade
import math

from modules.data.complex import Complex
from modules.data import data

from line_profiler import profile
import random


class Input(Complex):

    def __init__(self, id):
        super().__init__(id)

        self.name = "IN"
        self.type = "Input"
        self.gate_type = "8Input"

        self.inputs = []
        self.outputs = [1]
        self.inputs_sizes = []
        self.outputs_sizes = [8]

        self.exceptional_size_offset = 2

        self.gen_tile_pattern()
        self.calculate_display()
        
        
    def switch(self):
        self.outputs[0] = random.randint(0,255)
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

        arcade.draw_rect_filled(rect,arcade.color.BLUE)
        arcade.draw_text(f"Input: {self.outputs}",tile_x,tile_y,arcade.color.WHITE)
