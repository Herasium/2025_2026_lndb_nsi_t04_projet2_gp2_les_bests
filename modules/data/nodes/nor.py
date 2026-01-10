import arcade
import math

from modules.data.node import Node
from modules.data.gate import Gate

from line_profiler import profile

class Nor(Gate):

    def __init__(self, id, tiles):
        super().__init__(id,tiles)

        self.name = "NOR"
        self.type = "Gate"
        self.gate_type = "NOR"

        self.inputs = [False,False]
        self.outputs = [True]

        self.calculate_display()
        self.gen_tile_pattern()
        