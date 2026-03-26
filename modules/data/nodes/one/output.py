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

