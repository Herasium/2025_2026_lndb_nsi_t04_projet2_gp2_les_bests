import arcade
import math

from modules.data.node import Node
from modules.data.gate import Gate

from line_profiler import profile

class Nand(Gate):

    def __init__(self, id):
        super().__init__(id)

        self.name = "NAND"
        self.type = "Gate"
        self.gate_type = "NAND"

        self.inputs = [0,0]
        self.outputs = [1]
        self.inputs_sizes = [1,1]
        self.outputs_sizes = [1]

        self.calculate_display()
        self.gen_tile_pattern()
        