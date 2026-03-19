from typing import Any

from modules.data.complex import Complex

"""Provides 8-bit logic gate implementations for circuit simulation."""


class Nor(Complex):
    """Represents an 8-bit Nor logic gate component.

    Attributes:
        name: The display name of the gate.
        gate_type: The identifier for the logic gate category.
        inputs: Pin offsets for input signals.
        outputs: Pin offsets for output signals.
        inputs_sizes: Bit width of input pins.
        outputs_sizes: Bit width of output pins.
    """

    def __init__(self, id: Any) -> None:
        """Initializes the Nor gate instance.

        Args:
            id: A unique identifier for the component.
        """
        super().__init__(id)

        self.name: str = "NOR"
        self.gate_type: str = "8NOR"

        self.inputs: list[int] = [0,0]
        self.outputs: list[int] = [0]
        self.inputs_sizes: list[int] = [8,8]
        self.outputs_sizes: list[int] = [8]

        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()
