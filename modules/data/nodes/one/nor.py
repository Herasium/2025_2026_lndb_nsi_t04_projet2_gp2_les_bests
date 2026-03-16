from typing import List, Any

from modules.data.gate import Gate


class Nor(Gate):
    """
    Represents a NOR logic gate in the circuit simulation.
    Inherits from the Gate base class.
    """

    def __init__(self, id: Any) -> None:
        """
        Initialize the NOR gate instance.

        Parameters:
        - id: Unique identifier for the gate instance
        """
        # Initialize the parent Gate class
        super().__init__(id)

        # Define metadata for the gate
        self.name: str = "NOR"
        self.type: str = "Gate"
        self.gate_type: str = "NOR"

        # Initialize gate states (2 inputs, 1 output)
        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [1]

        # Define dimensions or sizes for inputs and outputs
        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1]

        # Calculate display properties and generate visual pattern
        self.calculate_display()
        self.gen_tile_pattern()
