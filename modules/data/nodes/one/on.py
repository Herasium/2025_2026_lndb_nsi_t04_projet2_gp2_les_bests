from typing import Any

from modules.data.gate import Gate

"""Logic gate implementation for the ON."""


class On(Gate):
    """Represents a logical ON gate."""

    def __init__(self, id: Any) -> None:
        """Initializes the gate instance with required metadata and port configurations.

        Args:
            id: Unique identifier assigned to this gate instance.
        """
        super().__init__(id)

        self.name: str = "ON"
        self.type: str = "Input"
        self.gate_type: str = "ON"

        self.inputs: list[int] = []
        self.outputs: list[int] = [1]

        self.inputs_sizes: list[int] = []
        self.outputs_sizes: list[int] = [1]

        self.calculate_display()
        self.gen_tile_pattern()

    def switch(self):
        pass
