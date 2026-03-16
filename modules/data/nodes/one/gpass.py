from typing import Any, List

from modules.data.gate import Gate


class Pass(Gate):
    """Represents a Pass gate in the logic circuit simulation.

    Inherits from Gate and acts as a buffer component.
    """

    def __init__(self, id: Any) -> None:
        """Initialize the Pass gate with a unique identifier.

        Parameters:
        - id: The unique identifier for the gate instance.
        """
        super().__init__(id)

        # Set identity attributes for the gate
        self.name: str = "PASS"
        self.type: str = "Gate"
        self.gate_type: str = "PASS"

        # Initialize I/O state lists with default values
        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [0, 0]

        # Define the bit-widths for the input and output ports
        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1, 1]

        # Prepare visual representation and internal tiling data
        self.calculate_display()
        self.gen_tile_pattern()
