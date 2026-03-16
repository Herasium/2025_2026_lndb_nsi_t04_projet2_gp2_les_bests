from typing import List, Any

from modules.data.complex import Complex

# Eight Bit Gate


class Maker(Complex):
    """
    Represents an 8-bit Maker gate that aggregates eight 1-bit inputs into a single 8-bit output.
    Inherits from the Complex class.
    """

    def __init__(self, id: Any) -> None:
        """
        Initialize the Maker gate instance.

        Parameters:
        - id: Unique identifier for the gate instance.

        Returns:
        - None
        """
        super().__init__(id)

        # Set identity metadata for the gate
        self.name: str = "MAKER"
        self.gate_type: str = "8MAKER"

        # Initialize I/O structures
        # Eight 1-bit input slots initialized to 0
        self.inputs: List[int] = [0, 0, 0, 0, 0, 0, 0, 0]
        # Single 8-bit output slot initialized to 0
        self.outputs: List[int] = [0]

        # Define I/O sizes for simulation processing
        self.inputs_sizes: List[int] = [1, 1, 1, 1, 1, 1, 1, 1]
        self.outputs_sizes: List[int] = [8]

        # Trigger visual and structural setup methods inherited from parent classes
        self.calculate_display()  # Calculate bounding boxes and sprite positions
        self.gen_tile_pattern()  # Generate internal logic tile mapping
        self.setup_texts()  # Initialize UI label elements
