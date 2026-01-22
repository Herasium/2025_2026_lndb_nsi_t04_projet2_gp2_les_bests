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

        self.inputs = [False,False]
        self.outputs = [False]

        self.calculate_display()
        self.gen_tile_pattern()
        