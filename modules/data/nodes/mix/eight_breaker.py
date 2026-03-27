from typing import Any, List

from modules.data.complex import Complex

"""Provides logic for the 8-bit breaker gate component."""


class Breaker(Complex):
    """Represents an 8-bit breaker gate component for system data routing."""

    def __init__(self, id: Any) -> None:
        """Initializes the Breaker gate instance.

        Args:
            id: Unique identifier used for system component tracking.
        """
        super().__init__(id)

        self.name: str = "BREAKER"
        self.gate_type: str = "8BREAK"

        self.inputs: List[int] = [0]
        self.outputs: List[int] = [0, 0, 0, 0, 0, 0, 0, 0]

        self.inputs_sizes: List[int] = [8]
        self.outputs_sizes: List[int] = [1, 1, 1, 1, 1, 1, 1, 1]

        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()
