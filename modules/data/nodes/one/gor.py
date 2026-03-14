import arcade
import math

from modules.data.node import Node
from modules.data.gate import Gate

from line_profiler import profile

class Or(Gate):

    def __init__(self, id):
        super().__init__(id)

        self.name = "OR"
        self.type = "Gate"
        self.gate_type = "OR"

        self.inputs = [0,0]
        self.outputs = [0]
        self.inputs_sizes = [1,1]
        self.outputs_sizes = [1]

        self.calculate_display()
        self.gen_tile_pattern()
        