import arcade
import math

from modules.data.node import Node
from modules.data.gate import Gate

from line_profiler import profile

class Not(Gate):

    def __init__(self, id):
        super().__init__(id)

        self.name = "NOT"
        self.type = "Gate"
        self.gate_type = "NOT"

        self.inputs = [False]
        self.outputs = [True]

        self.calculate_display()
        self.gen_tile_pattern()
        