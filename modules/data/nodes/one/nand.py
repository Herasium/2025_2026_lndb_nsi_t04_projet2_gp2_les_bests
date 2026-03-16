"""Provides implementations for standard logic gates used in circuit simulation."""

from typing import List, Union

from modules.data.gate import Gate


class Nand(Gate):
    """Represents a NAND logic gate in a circuit simulation."""

    def __init__(self, id: Union[int, str]) -> None:
        """Initializes the NAND gate configuration.

        Args:
            id: Unique identifier for the gate instance.
        """
        super().__init__(id)

        self.name: str = "NAND"
        self.type: str = "Gate"
        self.gate_type: str = "NAND"

        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [1]

        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1]

        self.calculate_display()
        self.gen_tile_pattern()
