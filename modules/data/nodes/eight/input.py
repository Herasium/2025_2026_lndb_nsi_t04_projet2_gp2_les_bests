import math
from typing import List, Any
import random

from modules.data.complex import Complex


class Input(Complex):
    """
    Represents an 8-bit Input gate component in a logic simulation.
    Inherits from the Complex base class.
    """

    def __init__(self, id: Any) -> None:
        """
        Initialize the Input gate instance.

        Parameters:
        - id: Unique identifier for the component.
        """
        super().__init__(id)

        self.name: str = "IN"
        self.type: str = "Input"
        self.gate_type: str = "8Input"

        self.inputs: List[Any] = []
        self.outputs: List[int] = [1]  # List containing current output value
        self.inputs_sizes: List[int] = []
        self.outputs_sizes: List[int] = [8]

        self.exceptional_size_offset: int = 2

        # Initialize gate visuals and UI
        self.gen_tile_pattern()
        self.calculate_display()
        self.setup_texts()

    def switch(self) -> None:
        """
        Simulate switching the input gate by generating a new random 8-bit value.
        Updates internal state and UI text.
        """
        self.outputs[0] = random.randint(0, 255)  # Generate 8-bit random integer
        self.gen_tile_pattern()
        self.update_text_readings()

    def gen_tile_pattern(self) -> None:
        """
        Generate the visual tile pattern (grid representation) for the gate.
        Calculates and fills rows based on gate width and output configuration.
        """
        gate_tile_pattern: List[int] = []

        self.gate_width: int = 5
        # Calculate padding needed based on number of outputs
        to_fill: float = (self.gate_width - 2 - (len(self.outputs))) / 2

        # Bottom Row: Frame elements
        gate_tile_pattern.append(7)
        for _ in range(math.floor(to_fill)):
            gate_tile_pattern.append(0)
        for _ in range(len(self.outputs)):
            gate_tile_pattern.append(6)
        for _ in range(math.ceil(to_fill)):
            gate_tile_pattern.append(0)
        gate_tile_pattern.append(8)

        # First Row: Data output indicators
        gate_tile_pattern.append(30)
        for _ in range(math.floor(to_fill)):
            gate_tile_pattern.append(34)
        for i in self.outputs:
            gate_tile_pattern.append(22)
        for _ in range(math.ceil(to_fill)):
            gate_tile_pattern.append(33)
        gate_tile_pattern.append(32)

        # Second Row: Interface/Connection line visual
        gate_tile_pattern.append(31)
        for _ in range(self.gate_width - 2):
            gate_tile_pattern.append(13)
        gate_tile_pattern.append(25)

        # Top Row: Cap/Header visual
        gate_tile_pattern.append(28)
        for _ in range(self.gate_width - 2):
            gate_tile_pattern.append(2)
        gate_tile_pattern.append(27)

        # Store the generated pattern
        self.gate_tile_pattern: List[int] = gate_tile_pattern
