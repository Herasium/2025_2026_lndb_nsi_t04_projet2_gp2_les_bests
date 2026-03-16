from typing import List, Any

from modules.data.gate import Gate


class Xor(Gate):
    """Represents an XOR logic gate component."""

    def __init__(self, id: Any) -> None:
        """Initializes the XOR gate with default pin configurations.

        Args:
            id: The unique identifier for the gate instance.
        """
        super().__init__(id)

        self.name: str = "XOR"
        self.type: str = "Gate"
        self.gate_type: str = "XOR"

        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [0]
        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1]

        self.calculate_display()
        self.gen_tile_pattern()
