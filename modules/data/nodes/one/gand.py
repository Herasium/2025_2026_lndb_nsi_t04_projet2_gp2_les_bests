"""Provides implementations for standard logic gate components."""

from typing import List, Union

from modules.data.gate import Gate


class And(Gate):
    """Represents a standard two-input AND logic gate."""

    def __init__(self, id: Union[int, str]) -> None:
        """Initializes the AND gate with default binary input/output states.

        Args:
            id: Unique identifier used for tracking the gate instance.
        """
        super().__init__(id)

        self.name: str = "AND"
        self.type: str = "Gate"
        self.gate_type: str = "AND"

        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [0]
        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1]

        self.calculate_display()
        self.gen_tile_pattern()
