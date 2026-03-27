from typing import Any, List

from modules.data.complex import Complex

"""Provides logic for the 8-bit register component."""


class Register(Complex):
    """Represents an 8-bit register component for system data routing."""

    def __init__(self, id: Any) -> None:
        """Initializes the register instance.

        Args:
            id: Unique identifier used for system component tracking.
        """
        super().__init__(id)

        self.name: str = "REGI"
        self.gate_type: str = "8REGISTER"

        self.inputs: List[int] = [0,0,0]
        self.outputs: List[int] = [0]

        self.inputs_sizes: List[int] = [8,1,1]
        self.outputs_sizes: List[int] = [8]

        self.current_value = 0

        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()
