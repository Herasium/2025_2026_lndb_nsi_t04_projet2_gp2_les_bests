import arcade
import math

from modules.data.node import Node
from modules.data.gate import Gate

from line_profiler import profile

class And(Gate):

    def __init__(self, id, tiles):
        super().__init__(id,tiles)

        self.name = "AND"
        self.type = "Gate"
        self.gate_type = "AND"

        self.inputs = [False,False]
        self.outputs = [False]

        self.calculate_display()
        self.gen_tile_pattern()
        