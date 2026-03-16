from typing import List

from modules.data.gate import Gate


class Or(Gate):
    """
    Represents an OR logic gate component in the simulation.
    Inherits from the base Gate class.
    """

    def __init__(self, id: str) -> None:
        """
        Initialize the OR gate instance.

        Parameters:
        - id: A unique identifier for the gate.
        """
        super().__init__(id)

        # Set identity and metadata for the gate
        self.name: str = "OR"
        self.type: str = "Gate"
        self.gate_type: str = "OR"

        # Initialize input/output state containers
        # Binary logic represented as integers 0 or 1
        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [0]

        # Define the structural sizes for input and output ports
        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1]

        # Trigger initial geometry and rendering setup
        self.calculate_display()
        self.gen_tile_pattern()
