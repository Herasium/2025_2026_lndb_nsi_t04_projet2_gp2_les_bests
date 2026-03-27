import math
from typing import List, Any

from modules.data.gate import Gate

"""Provides the Input gate implementation for circuit simulation."""


class Input(Gate):
    """Represents a manual input toggle gate within a circuit."""

    def __init__(self, id: Any) -> None:
        """Initializes the Input gate.

        Args:
            id: Unique identifier for the gate instance.
        """
        super().__init__(id)

        self.name: str = "IN"
        self.type: str = "Input"
        self.gate_type: str = "Input"

        self.inputs: List[Any] = []
        self.outputs: List[int] = [1]
        self.inputs_sizes: List[int] = []
        self.outputs_sizes: List[int] = [1]

        self.exceptional_size_offset: int = 2

        self.gen_tile_pattern()
        self.calculate_display()

    def switch(self) -> None:
        """Toggles the current output state between 0 and 1."""
        # Convert boolean inversion to integer representation
        self.outputs[0] = (not self.outputs[0] == 1) * 1
        self.gen_tile_pattern()

