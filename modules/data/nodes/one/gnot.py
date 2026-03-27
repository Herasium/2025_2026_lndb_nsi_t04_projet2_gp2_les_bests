from typing import Any

from modules.data.gate import Gate

"""Logic gate implementation for the NOT operation."""


class Not(Gate):
    """Represents a logical NOT gate."""

    def __init__(self, id: Any) -> None:
        """Initializes the gate instance with required metadata and port configurations.

        Args:
            id: Unique identifier assigned to this gate instance.
        """
        super().__init__(id)

        self.name: str = "NOT"
        self.type: str = "Gate"
        self.gate_type: str = "NOT"

        self.inputs: list[int] = [0]
        self.outputs: list[int] = [1]

        self.inputs_sizes: list[int] = [1]
        self.outputs_sizes: list[int] = [1]

        self.calculate_display()
        self.gen_tile_pattern()
