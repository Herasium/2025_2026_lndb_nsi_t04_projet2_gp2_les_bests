import math
from typing import List, Any

from modules.data.complex import Complex


class Output(Complex):
    """Represents an output gate component in the UI system."""

    def __init__(self, id: Any) -> None:
        """
        Initialize the Output gate.

        Parameters:
        - id: Unique identifier for the component.
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
        """
        Generates the tile grid pattern representing the visual structure
        of the output gate.

        Calculates the filling based on input sizes and populates
        self.gate_tile_pattern with mapping indices.
        """
        gate_tile_pattern: List[int] = []

        self.gate_width: int = 5
        # Calculate how many empty tiles are needed to center the input connectors
        to_fill: float = (self.gate_width - 2 - (len(self.inputs))) / 2

        # Bottom Row: Frame corner and input connectors
        gate_tile_pattern.append(7)
        for _ in range(math.floor(to_fill)):
            gate_tile_pattern.append(0)
        for _ in range(len(self.inputs)):
            gate_tile_pattern.append(6)
        for _ in range(math.ceil(to_fill)):
            gate_tile_pattern.append(0)
        gate_tile_pattern.append(8)

        # First Row: Decorative frame and logic connector points
        gate_tile_pattern.append(30)
        for _ in range(math.floor(to_fill)):
            gate_tile_pattern.append(34)
        for i in self.inputs:
            gate_tile_pattern.append(22)
        for _ in range(math.ceil(to_fill)):
            gate_tile_pattern.append(33)
        gate_tile_pattern.append(32)

        # Second Row: Internal structure body
        gate_tile_pattern.append(31)
        for _ in range(self.gate_width - 2):
            gate_tile_pattern.append(13)
        gate_tile_pattern.append(25)

        # Top Row: Frame ceiling
        gate_tile_pattern.append(28)
        for _ in range(self.gate_width - 2):
            gate_tile_pattern.append(2)
        gate_tile_pattern.append(27)

        # Store the computed pattern for rendering
        self.gate_tile_pattern = gate_tile_pattern
