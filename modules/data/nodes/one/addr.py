"""Provides implementations for standard logic gate components."""

from typing import List, Union

from modules.data.gate import Gate


class Adder(Gate):
    """Represents a standard Full Adder gate."""

    def __init__(self, id: Union[int, str]) -> None:
        """Initializes the Adder gate with default binary input/output states.

        Args:
            id: Unique identifier used for tracking the gate instance.
        """
        super().__init__(id)

        self.name: str = "ADDER"
        self.type: str = "Gate"
        self.gate_type: str = "ADDER"

        self.inputs: List[int] = [0, 0, 0]
        self.outputs: List[int] = [0, 0]
        self.inputs_sizes: List[int] = [1, 1, 1]
        self.outputs_sizes: List[int] = [1, 1]

        self.calculate_display()
        self.gen_tile_pattern()
