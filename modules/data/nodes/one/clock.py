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

    def gen_tile_pattern(self) -> None:
        """Generates the visual grid pattern for rendering the Clock gate."""

        gate_tile_pattern: List[int] = []

        self.gate_width: int = 5
        to_fill: float = (self.gate_width - 2 - (len(self.outputs))) / 2

        gate_tile_pattern.append(7)
        for _ in range(math.floor(to_fill)):
            gate_tile_pattern.append(0)
        for _ in range(len(self.outputs)):
            gate_tile_pattern.append(6)
        for _ in range(math.ceil(to_fill)):
            gate_tile_pattern.append(0)
        gate_tile_pattern.append(8)

        gate_tile_pattern.append(30)
        for _ in range(math.floor(to_fill)):
            gate_tile_pattern.append(34)
        for i in self.outputs:
            if i:
                gate_tile_pattern.append(15)
            else:
                gate_tile_pattern.append(21)
        for _ in range(math.ceil(to_fill)):
            gate_tile_pattern.append(33)
        gate_tile_pattern.append(32)

        gate_tile_pattern.append(31)
        for _ in range(self.gate_width - 2):
            gate_tile_pattern.append(13)
        gate_tile_pattern.append(25)

        gate_tile_pattern.append(28)
        for _ in range(self.gate_width - 2):
            gate_tile_pattern.append(2)
        gate_tile_pattern.append(27)

        self.gate_tile_pattern: List[int] = gate_tile_pattern
