from typing import List, Union

from modules.data.gate import Gate


class Nand(Gate):
    """
    Represents a NAND logic gate in the circuit simulation.
    Inherits from the base Gate class.
    """

    def __init__(self, id: Union[int, str]) -> None:
        """
        Initialize the Nand gate with specific properties and input/output structure.

        Parameters:
        - id: Unique identifier for the gate instance.

        Returns:
        - None
        """
        # Call the parent Gate constructor
        super().__init__(id)

        # Set identity metadata for the gate
        self.name: str = "NAND"
        self.type: str = "Gate"
        self.gate_type: str = "NAND"

        # Initialize input and output states (default binary values)
        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [1]

        # Define the structural sizes for input and output interfaces
        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1]

        # Trigger initial configuration for graphical representation
        self.calculate_display()
        self.gen_tile_pattern()
