"""Provides the Maker gate implementation for 8-bit signal aggregation."""

from typing import List, Any
from modules.data.complex import Complex


class Maker(Complex):
    """Aggregates eight 1-bit signal inputs into a single 8-bit output."""

    def __init__(self, id: Any) -> None:
        """Initializes the Maker gate instance.

        Args:
            id: Unique identifier for the gate instance.
        """
        super().__init__(id)

        self.name: str = "MAKER"
        self.gate_type: str = "8MAKER"

        self.inputs: List[int] = [0, 0, 0, 0, 0, 0, 0, 0]
        self.outputs: List[int] = [0]

        self.inputs_sizes: List[int] = [1, 1, 1, 1, 1, 1, 1, 1]
        self.outputs_sizes: List[int] = [8]

        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()
