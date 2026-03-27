"""Provides the Pass gate implementation for logic circuit simulations."""

from typing import Any, List

from modules.data.gate import Gate


class Pass(Gate):
    """Buffer component that propagates input signals without modification."""

    def __init__(self, id: Any) -> None:
        """Initializes a new Pass gate instance.

        Args:
            id: Unique identifier for the gate instance.
        """
        super().__init__(id)

        self.name: str = "PASS"
        self.type: str = "Gate"
        self.gate_type: str = "PASS"

        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [0, 0]

        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1, 1]

        self.calculate_display()
        self.gen_tile_pattern()
