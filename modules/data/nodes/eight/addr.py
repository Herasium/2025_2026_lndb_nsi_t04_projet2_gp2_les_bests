"""Provides 8-bit logic gate implementations for circuit simulation."""

from typing import List, Union
from modules.data.complex import Complex


class Adder(Complex):
    """Represents an 8-bit Full Adder logic gate component.

    Attributes:
        name: The display name of the gate.
        gate_type: The identifier for the logic gate category.
        inputs: Pin offsets for input signals.
        outputs: Pin offsets for output signals.
        inputs_sizes: Bit width of input pins.
        outputs_sizes: Bit width of output pins.
    """

    def __init__(self, id: Union[int, str]) -> None:
        """Initializes the Adder gate with default binary input/output states.

        Args:
            id: Unique identifier used for tracking the gate instance.
        """
        super().__init__(id)

        self.name: str = "ADDER"
        self.gate_type: str = "8ADDER"

        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [0]
        self.inputs_sizes: List[int] = [8, 8]
        self.outputs_sizes: List[int] = [8]

        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()
