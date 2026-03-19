"""Provides the Delay gate implementation for logic circuit simulations."""

from typing import Any, List

from modules.data.gate import Gate


class Delay(Gate):
    """Delay gate, hold the signal for 1 tick."""

    def __init__(self, id: Any) -> None:
        """Initializes a new Delay gate instance.

        Args:
            id: Unique identifier for the gate instance.
        """
        super().__init__(id)

        self.name: str = "DLY"
        self.type: str = "Gate"
        self.gate_type: str = "DLY"

        self.inputs: List[int] = [0]
        self.outputs: List[int] = [0]

        self.old_output: int = 0

        self.inputs_sizes: List[int] = [1]
        self.outputs_sizes: List[int] = [1]

        self.calculate_display()
        self.gen_tile_pattern()
