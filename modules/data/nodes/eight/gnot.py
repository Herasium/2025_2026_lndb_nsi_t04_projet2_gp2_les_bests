import arcade
import math

from modules.data.node import Node
from modules.data.gate import Gate
from modules.data.complex import Complex

from line_profiler import profile

#Eight Bit Gate

class Not(Complex):

    def __init__(self, id):
        super().__init__(id)

        self.name = "NOT"
        self.gate_type = "8NOT"

        self.inputs = [0]
        self.outputs = [15]
        self.inputs_sizes = [8]
        self.outputs_sizes = [8]
        
        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()