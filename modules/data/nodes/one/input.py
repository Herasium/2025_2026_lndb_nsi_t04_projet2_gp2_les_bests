import math
from typing import List, Any

from modules.data.gate import Gate


class Input(Gate):
    """
    Represents an Input logic gate in the circuit simulator.
    Inherits from the Gate base class.
    """

    def __init__(self, id: Any) -> None:
        """
        Initialize the Input gate instance.

        Parameters:
        - id: Unique identifier for the gate.
        """
        super().__init__(id)

        # Basic metadata for the gate
        self.name: str = "IN"
        self.type: str = "Input"
        self.gate_type: str = "Input"

        # Connection and size specifications
        self.inputs: List[Any] = []
        self.outputs: List[int] = [1]
        self.inputs_sizes: List[int] = []
        self.outputs_sizes: List[int] = [1]

        # Offset for graphical representation
        self.exceptional_size_offset: int = 2

        # Initialize graphical pattern and UI display properties
        self.gen_tile_pattern()
        self.calculate_display()

    def switch(self) -> None:
        """
        Toggle the output state of the input gate between 0 and 1.
        Updates the graphical tile pattern after the state change.
        """
        # Toggle output: if 1 becomes 0, if 0 becomes 1
        self.outputs[0] = (not self.outputs[0] == 1) * 1
        self.gen_tile_pattern()

    def gen_tile_pattern(self) -> None:
        """
        Generates the grid-based tile representation (layout) for the gate.
        Populates self.gate_tile_pattern based on current gate width and state.
        """
        gate_tile_pattern: List[int] = []

        # Define grid width
        self.gate_width: int = 5
        # Calculate padding to center the output indicator
        to_fill: float = (self.gate_width - 2 - (len(self.outputs))) / 2

        # Bottom Row: Frame edges with central output slot
        gate_tile_pattern.append(7)
        for _ in range(math.floor(to_fill)):
            gate_tile_pattern.append(0)
        for _ in range(len(self.outputs)):
            gate_tile_pattern.append(6)
        for _ in range(math.ceil(to_fill)):
            gate_tile_pattern.append(0)
        gate_tile_pattern.append(8)

        # First Row: Main visual row containing the state indicator (15 for ON, 21 for OFF)
        gate_tile_pattern.append(30)
        for _ in range(math.floor(to_fill)):
            gate_tile_pattern.append(34)
        for i in self.outputs:
            if i:
                gate_tile_pattern.append(15)  # Representing logic high
            else:
                gate_tile_pattern.append(21)  # Representing logic low
        for _ in range(math.ceil(to_fill)):
            gate_tile_pattern.append(33)
        gate_tile_pattern.append(32)

        # Second Row: Decorative interior row
        gate_tile_pattern.append(31)
        for _ in range(self.gate_width - 2):
            gate_tile_pattern.append(13)
        gate_tile_pattern.append(25)

        # Top Row: Top frame border
        gate_tile_pattern.append(28)
        for _ in range(self.gate_width - 2):
            gate_tile_pattern.append(2)
        gate_tile_pattern.append(27)

        # Store the generated pattern
        self.gate_tile_pattern = gate_tile_pattern
