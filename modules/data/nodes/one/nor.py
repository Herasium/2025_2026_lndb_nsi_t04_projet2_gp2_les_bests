from typing import List, Any

from modules.data.gate import Gate

"""Logic gate definitions for circuit simulation."""


class Nor(Gate):
    """Represents a NOR logic gate with two inputs and one output."""

    def __init__(self, id: Any) -> None:
        """Initializes the NOR gate with default state and configuration.

        Args:
            id: Unique identifier for the gate instance.
        """
        super().__init__(id)

        self.name: str = "NOR"
        self.type: str = "Gate"
        self.gate_type: str = "NOR"

        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [1]

        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1]

        self.calculate_display()
        self.gen_tile_pattern()
