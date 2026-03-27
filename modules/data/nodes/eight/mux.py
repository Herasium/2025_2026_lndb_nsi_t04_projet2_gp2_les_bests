from typing import Any, List

from modules.data.complex import Complex

"""Provides logic for the 8-bit Mux gate component."""


class Mux(Complex):
    """Represents an 8-bit Mux gate component for system data routing."""

    def __init__(self, id: Any) -> None:
        """Initializes the Mux gate instance.

        Args:
            id: Unique identifier used for system component tracking.
        """
        super().__init__(id)

        self.name: str = "MUX"
        self.gate_type: str = "8MUX"

        self.inputs: List[int] = [0,0,0,0,0,0,0,0,0]
        self.outputs: List[int] = [0]

        self.inputs_sizes: List[int] = [8,8,8,8,8,8,8,8,8]
        self.outputs_sizes: List[int] = [8]

        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()
