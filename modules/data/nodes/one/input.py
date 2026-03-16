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

    def gen_tile_pattern(self) -> None:
        """Constructs the grid-based visual representation for the gate."""
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
            if i:
                gate_tile_pattern.append(15)
            else:
                gate_tile_pattern.append(21)
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

        self.gate_tile_pattern = gate_tile_pattern
