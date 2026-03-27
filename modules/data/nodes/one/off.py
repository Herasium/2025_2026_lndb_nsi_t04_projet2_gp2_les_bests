from typing import Any

from modules.data.gate import Gate

"""Logic gate implementation for the OFF."""


class Off(Gate):
    """Represents a logical OFF gate."""

    def __init__(self, id: Any) -> None:
        """Initializes the gate instance with required metadata and port configurations.

        Args:
            id: Unique identifier assigned to this gate instance.
        """
        super().__init__(id)

        self.name: str = "OFF"
        self.type: str = "Input"
        self.gate_type: str = "OFF"

        self.inputs: list[int] = []
        self.outputs: list[int] = [0]

        self.inputs_sizes: list[int] = []
        self.outputs_sizes: list[int] = [1]

        self.calculate_display()
        self.gen_tile_pattern()

    def switch(self):
        pass
