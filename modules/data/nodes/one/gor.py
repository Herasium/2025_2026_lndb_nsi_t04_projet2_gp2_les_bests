from typing import List

from modules.data.gate import Gate


class Or(Gate):
    """Represents an OR logic gate component within the simulation."""

    def __init__(self, id: str) -> None:
        """Initializes the OR gate instance.

        Args:
            id: A unique identifier for the gate instance.
        """
        super().__init__(id)

        self.name: str = "OR"
        self.type: str = "Gate"
        self.gate_type: str = "OR"

        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [0]

        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1]

        self.calculate_display()
        self.gen_tile_pattern()
