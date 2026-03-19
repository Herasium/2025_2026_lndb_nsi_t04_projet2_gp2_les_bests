"""Provides the SWC gate implementation for logic circuit simulations."""

from typing import Any, List

from modules.data.gate import Gate


class Swc(Gate):
    """Swc gate, provide a way to shut a gate output down, not propagating it futher."""

    def __init__(self, id: Any) -> None:
        """Initializes a new Swc gate instance.

        Args:
            id: Unique identifier for the gate instance.
        """
        super().__init__(id)

        self.name: str = "SWC"
        self.type: str = "Gate"
        self.gate_type: str = "SWC"

        self.inputs: List[int] = [0, 0]
        self.outputs: List[Any] = [None]

        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1]

        self.calculate_display()
        self.gen_tile_pattern()
