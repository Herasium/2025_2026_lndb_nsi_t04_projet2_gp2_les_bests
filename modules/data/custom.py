import arcade
import math

from modules.data.node import Node
from modules.data.gate import Gate
from modules.data import data

from line_profiler import profile

class CustomGate(Gate):

    def __init__(self, id, chip):
        super().__init__(id)

        self.name = chip.name
        self.type = "Custom"
        self.base_chip_id = chip.id
        self.chip = chip.copy()
        self.gate_type = "Custom"

        self.update_io()

        self.calculate_display()
        self.gen_tile_pattern()
        
    def prop_io(self):
        chip_inputs = self.chip.get_inputs()
        for i in range(len(self.inputs)):
            self.chip.gates[chip_inputs[i]].outputs[0] = self.inputs[i]

    def update_io(self):
        self.inputs = []
        self.outputs = []

        chip_inputs = self.chip.get_inputs()
        for i in chip_inputs:
            self.inputs.append(self.chip.gates[i].outputs[0])

        chip_outputs = self.chip.get_outputs()
        for i in chip_outputs:
            self.outputs.append(self.chip.gates[i].inputs[0])

    def draw_tiles(self):
    
        width = self.tile_width
        height = 4
        out = self.outputs.copy()
        inp = self.inputs.copy()

        out.reverse()
        inp.reverse()
        current = int(''.join(map(str, map(int, (out+inp)))), 2)

        tile_x = self.x + self._camera[0]
        tile_y = self.y + self._camera[1]

        rect = arcade.XYWH(
                    x=tile_x,
                    y=tile_y,
                    width=width * data.UI_EDITOR_GRID_SIZE,
                    height=height * data.UI_EDITOR_GRID_SIZE,
                    anchor=arcade.Vec2(0,0)
        )

        arcade.draw_texture_rect(data.IMAGE.get_texture(self.base_chip_id,current),rect)