import math
from typing import List, Any

from modules.data.gate import Gate


class Output(Gate):
    """
    Represents an Output gate in the logic circuit simulation.
    Inherits from the Gate base class.
    """

    def __init__(self, id: Any) -> None:
        """
        Initialize the Output gate instance.

        Parameters:
        - id: Unique identifier for the gate.
        """
        super().__init__(id)

        self.name: str = "OUT"
        self.type: str = "Output"
        self.gate_type: str = "Output"

        self.inputs: List[int] = [0]
        self.outputs: List[Any] = []
        self.inputs_sizes: List[int] = [1]
        self.outputs_sizes: List[int] = []

        self.exceptional_size_offset: int = 2

        self.gen_tile_pattern()
        self.calculate_display()

    def gen_tile_pattern(self) -> None:
        """
        Generates the visual tile pattern (grid representation) for the Output gate
        based on its current input states and width.
        """
        gate_tile_pattern: List[int] = []

        self.gate_width: int = 5
        # Calculate padding needed to center inputs
        to_fill: float = (self.gate_width - 2 - (len(self.inputs))) / 2

        # Bottom Row: Generate the connection ports and base tiles
        gate_tile_pattern.append(7)
        for _ in range(math.floor(to_fill)):
            gate_tile_pattern.append(0)
        for _ in range(len(self.inputs)):
            gate_tile_pattern.append(6)  # Port indicators
        for _ in range(math.ceil(to_fill)):
            gate_tile_pattern.append(0)
        gate_tile_pattern.append(8)

        # First Row: Generate tiles based on input signal state (On/Off)
        gate_tile_pattern.append(30)
        for _ in range(math.floor(to_fill)):
            gate_tile_pattern.append(34)
        for i in self.inputs:
            # If input is truthy (active), use 'On' tile (15), else 'Off' tile (21)
            if i:
                gate_tile_pattern.append(15)
            else:
                gate_tile_pattern.append(21)
        for _ in range(math.ceil(to_fill)):
            gate_tile_pattern.append(33)
        gate_tile_pattern.append(32)

        # Second Row: Generate the central body tiles
        gate_tile_pattern.append(31)
        for _ in range(self.gate_width - 2):
            gate_tile_pattern.append(13)
        gate_tile_pattern.append(25)

        # Top Row: Generate the top boundary tiles
        gate_tile_pattern.append(28)
        for _ in range(self.gate_width - 2):
            gate_tile_pattern.append(2)
        gate_tile_pattern.append(27)

        # Store the final pattern for rendering
        self.gate_tile_pattern = gate_tile_pattern
