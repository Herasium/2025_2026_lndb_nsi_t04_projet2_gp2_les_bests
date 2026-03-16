"""Provides specialized logic gate components for simulation environments."""

import math
from typing import List, Any
import random

from modules.data.complex import Complex


class Input(Complex):
    """Represents an 8-bit input gate within a logic simulation circuit."""

    def __init__(self, id: Any) -> None:
        """Initializes the input component.

        Args:
            id: Unique identifier for the gate instance.
        """
        super().__init__(id)

        self.name: str = "IN"
        self.type: str = "Input"
        self.gate_type: str = "8Input"

        self.inputs: List[Any] = []
        self.outputs: List[int] = [1]
        self.inputs_sizes: List[int] = []
        self.outputs_sizes: List[int] = [8]

        self.exceptional_size_offset: int = 2

        self.gen_tile_pattern()
        self.calculate_display()
        self.setup_texts()

    def switch(self) -> None:
        """Simulates an input state change by generating a new random 8-bit integer."""
        self.outputs[0] = random.randint(0, 255)
        self.gen_tile_pattern()
        self.update_text_readings()

    def gen_tile_pattern(self) -> None:
        """Generates the visual grid pattern for rendering the gate interface."""
        gate_tile_pattern: List[int] = []

        self.gate_width: int = 5
        to_fill: float = (self.gate_width - 2 - (len(self.outputs))) / 2

        gate_tile_pattern.append(7)
        for _ in range(math.floor(to_fill)):
            gate_tile_pattern.append(0)
        for _ in range(len(self.outputs)):
            gate_tile_pattern.append(6)
        for _ in range(math.ceil(to_fill)):
            gate_tile_pattern.append(0)
        gate_tile_pattern.append(8)

        gate_tile_pattern.append(30)
        for _ in range(math.floor(to_fill)):
            gate_tile_pattern.append(34)
        for i in self.outputs:
            gate_tile_pattern.append(22)
        for _ in range(math.ceil(to_fill)):
            gate_tile_pattern.append(33)
        gate_tile_pattern.append(32)

        gate_tile_pattern.append(31)
        for _ in range(self.gate_width - 2):
            gate_tile_pattern.append(13)
        gate_tile_pattern.append(25)

        gate_tile_pattern.append(28)
        for _ in range(self.gate_width - 2):
            gate_tile_pattern.append(2)
        gate_tile_pattern.append(27)

        self.gate_tile_pattern: List[int] = gate_tile_pattern
