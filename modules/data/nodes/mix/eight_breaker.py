from typing import Any, List

from modules.data.complex import Complex

# Eight Bit Gate


class Breaker(Complex):
    """
    Represents an 8-bit breaker gate component in the system.
    Inherits from Complex to handle complex logic and structural components.
    """

    def __init__(self, id: Any) -> None:
        """
        Initialize the Breaker instance.

        Parameters:
        - id: Unique identifier for the gate instance.

        Returns:
        - None
        """
        # Initialize the parent Complex class
        super().__init__(id)

        self.name: str = "BREAKER"
        self.gate_type: str = "8BREAK"

        # Initialize input and output states
        self.inputs: List[int] = [0]
        self.outputs: List[int] = [0, 0, 0, 0, 0, 0, 0, 0]

        # Define the bit widths for inputs and outputs
        self.inputs_sizes: List[int] = [8]
        self.outputs_sizes: List[int] = [1, 1, 1, 1, 1, 1, 1, 1]

        # Trigger internal setup routines for visualization and data
        self.calculate_display()  # Calculate dimensions for rendering
        self.gen_tile_pattern()  # Generate tile graphics pattern
        self.setup_texts()  # Initialize display labels/texts
