from typing import Any

from modules.data.gate import Gate


class Not(Gate):
    """
    Represents a logical NOT gate.

    Inherits from the Gate base class and defines the specific
    properties and input/output structures for a NOT operation.
    """

    def __init__(self, id: Any) -> None:
        """
        Initialize the Not gate with a unique identifier and default settings.

        Parameters:
        - id: The unique identifier for the gate instance.
        """
        super().__init__(id)

        # Set identifying metadata for the gate
        self.name: str = "NOT"
        self.type: str = "Gate"
        self.gate_type: str = "NOT"

        # Define input/output structure: 1 input node, 1 output node
        self.inputs: list[int] = [0]
        self.outputs: list[int] = [1]

        # Define the size configuration for the ports
        self.inputs_sizes: list[int] = [1]
        self.outputs_sizes: list[int] = [1]

        # Initialize visual and functional patterns
        self.calculate_display()  # Calculate coordinate/visual bounds
        self.gen_tile_pattern()  # Generate the grid/tile representation
