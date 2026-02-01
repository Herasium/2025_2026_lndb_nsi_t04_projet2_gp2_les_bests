import arcade
import math

from modules.data.node import Node
from modules.data.gate import Gate

from line_profiler import profile

class Pass(Gate):

    def __init__(self, id):
        super().__init__(id)

        self.name = "PASS"
        self.type = "Gate"
        self.gate_type = "PASS"

        self.inputs = [False,False]
        self.outputs = [False,False]

        self.calculate_display()
        self.gen_tile_pattern()
        