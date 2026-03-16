import math
from typing import List, Any

from modules.data.complex import Complex

"""Provides the Output class for rendering output gate components within the UI."""


class Output(Complex):
    """Represents an output gate component in the UI system."""

    def __init__(self, id: Any) -> None:
        """Initializes the Output gate component.

        Args:
            id: The unique identifier for the component instance.
        """
        super().__init__(id)

        self.name: str = "OUT"
        self.type: str = "Output"
        self.gate_type: str = "8Output"

        self.inputs: List[int] = [0]
        self.outputs: List[Any] = []
        self.inputs_sizes: List[int] = [8]
        self.outputs_sizes: List[int] = []

        self.exceptional_size_offset: int = 2

        self.gen_tile_pattern()
        self.calculate_display()
        self.setup_texts()

    def gen_tile_pattern(self) -> None:
        """Generates the grid indices representing the visual structure of the output gate."""
        gate_tile_pattern: List[int] = []

        self.gate_width: int = 5
        # Calculate padding needed to center input connectors within the fixed-width gate
        to_fill: float = (self.gate_width - 2 - (len(self.inputs))) / 2

        gate_tile_pattern.append(7)
        for _ in range(math.floor(to_fill)):
            gate_tile_pattern.append(0)
        for _ in range(len(self.inputs)):
            gate_tile_pattern.append(6)
        for _ in range(math.ceil(to_fill)):
            gate_tile_pattern.append(0)
        gate_tile_pattern.append(8)

        gate_tile_pattern.append(30)
        for _ in range(math.floor(to_fill)):
            gate_tile_pattern.append(34)
        for i in self.inputs:
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

        self.gate_tile_pattern = gate_tile_pattern
