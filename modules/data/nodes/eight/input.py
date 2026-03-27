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

