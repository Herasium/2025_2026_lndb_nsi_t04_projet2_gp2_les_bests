import arcade
import math

from modules.data.node import Node
from modules.ui.toolbox.hitbox import HitBox
from modules.ui.toolbox.entity import Entity
from modules.ui.mouse import mouse
from modules.data import data
from modules.engine.logic import calculate_output
from modules.data.gate import Gate

from line_profiler import profile


class Input(Gate):

    def __init__(self, id):
        super().__init__(id)

        self.name = "IN"
        self.type = "Input"
        self.gate_type = "Input"

        self.inputs = []
        self.outputs = [True]

        self.exceptional_size_offset = 2

        self.gen_tile_pattern()
        self.calculate_display()
        
        
    def switch(self):
        self.outputs[0] = not self.outputs[0]
        self.gen_tile_pattern()

    def gen_tile_pattern(self):

        gate_tile_pattern = []

        self.gate_width = 5
        to_fill = (self.gate_width - 2 - (len(self.outputs)))  / 2

        #Bottom Row
        gate_tile_pattern.append(7)
        for _ in range(math.floor(to_fill)):
            gate_tile_pattern.append(0)
        for _ in range(len(self.outputs)):
            gate_tile_pattern.append(6)
        for _ in range(math.ceil(to_fill)):
            gate_tile_pattern.append(0)
        gate_tile_pattern.append(8)

        #First Row
        gate_tile_pattern.append(30)
        for _ in range(math.floor(to_fill)):
            gate_tile_pattern.append(34)
        for i in self.outputs:
            if i:
                gate_tile_pattern.append(15)
            else:
                gate_tile_pattern.append(21)
        for _ in range(math.ceil(to_fill)):
            gate_tile_pattern.append(33)
        gate_tile_pattern.append(32)

        #Second Row
        gate_tile_pattern.append(31)
        for _ in range(self.gate_width-2):
            gate_tile_pattern.append(13)
        gate_tile_pattern.append(25)

        #Top Row
        gate_tile_pattern.append(28)
        for _ in range(self.gate_width-2):
            gate_tile_pattern.append(2)
        gate_tile_pattern.append(27)

        self.gate_tile_pattern = gate_tile_pattern


