import math
from typing import List, Any

from modules.data.gate import Gate

"""Provides the Output gate implementation for the logic circuit simulation."""


class Output(Gate):
    """Represents an output node in the circuit.

    Attributes:
        name: Internal identifier name for the gate.
        type: General classification of the gate.
        gate_type: Specific operational type.
        inputs: List of current boolean input states.
        outputs: List of connected output terminals.
        inputs_sizes: Required dimensions for input ports.
        outputs_sizes: Required dimensions for output ports.
        exceptional_size_offset: Vertical offset for rendering logic.
        gate_width: Horizontal span of the gate representation.
        gate_tile_pattern: Flattened grid map for graphical rendering.
    """

    def __init__(self, id: Any) -> None:
        """Initializes the Output gate instance.

        Args:
            id: Unique identifier for the gate instance.
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
        """Computes the grid-based visual representation of the gate."""
        gate_tile_pattern: List[int] = []

        self.gate_width: int = 5
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
            # Map input state to active (15) or inactive (21) tile identifiers
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
