from typing import Any

from modules.data.complex import Complex

# Eight Bit Gate


class Not(Complex):
    """
    Represents an 8-bit NOT logic gate complex component.

    Inherits from the Complex class and handles the initialization
    and configuration of an 8-bit inversion logic gate.
    """

    def __init__(self, id: Any) -> None:
        """
        Initialize the Not gate with a unique identifier and default settings.

        Parameters:
        - id: A unique identifier for this gate instance.
        """
        # Initialize the base Complex class
        super().__init__(id)

        # Assign gate metadata
        self.name: str = "NOT"
        self.gate_type: str = "8NOT"

        # Define input/output pin offsets and data bit sizes
        self.inputs: list[int] = [0]
        self.outputs: list[int] = [15]
        self.inputs_sizes: list[int] = [8]
        self.outputs_sizes: list[int] = [8]

        # Trigger layout and visual generation routines
        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()
