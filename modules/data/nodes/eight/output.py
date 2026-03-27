import math
from typing import List, Any

from modules.data.complex import Complex

"""Provides the Output class for rendering output gate components within the UI."""


class Output(Complex):
    """Represents an output gate component in the UI system."""

    def __init__(self, id: Any) -> None:
        """Initializes the Output gate component.

        Args:
            id: The unique identifier for the component instance.
        """
        super().__init__(id)

        self.name: str = "OUT"
        self.type: str = "Output"
        self.gate_type: str = "8Output"

        self.inputs: List[int] = [0]
        self.outputs: List[Any] = []
        self.inputs_sizes: List[int] = [8]
        self.outputs_sizes: List[int] = []

        self.exceptional_size_offset: int = 2

        self.gen_tile_pattern()
        self.calculate_display()
        self.setup_texts()

