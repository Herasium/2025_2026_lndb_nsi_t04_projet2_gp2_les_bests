import math
from typing import List, Union

from modules.data.gate import Gate

"""Clock gate implementation for circuit simulation."""


class Clock(Gate):
    """Represents a clock signal generator within the simulation environment."""

    def __init__(self, id: Union[int, str]) -> None:
        """Initializes the Clock component.

        Args:
            id: Unique identifier for the gate instance.
        """
        super().__init__(id)

        self.name: str = "CLK"
        self.type: str = "Gate"
        self.gate_type: str = "CLK"

        self.exceptional_size_offset: int = 2

        self.inputs: List[int] = []
        self.outputs: List[int] = [0]
        self.inputs_sizes: List[int] = []
        self.outputs_sizes: List[int] = [1]

        self.calculate_display()
        self.gen_tile_pattern()
