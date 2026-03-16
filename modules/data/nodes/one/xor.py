from typing import List, Any

from modules.data.gate import Gate


class Xor(Gate):
    """
    A class representing an XOR logic gate, inheriting from the Gate base class.

    Attributes:
        id (str/int): Unique identifier for the gate.
        name (str): Name of the component.
        type (str): Category of the component.
        gate_type (str): Specific logic type of the gate.
        inputs (List[int]): Current state of input pins.
        outputs (List[int]): Current state of output pins.
        inputs_sizes (List[int]): Signal width for input pins.
        outputs_sizes (List[int]): Signal width for output pins.
    """

    def __init__(self, id: Any) -> None:
        """
        Initialize the XOR gate with specific attributes and patterns.

        Parameters:
        - id: The unique identifier for the gate instance.
        """
        super().__init__(id)

        self.name: str = "XOR"
        self.type: str = "Gate"
        self.gate_type: str = "XOR"

        # Initialize input/output pins and their bit widths
        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [0]
        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1]

        # Generate visual representation for the UI
        self.calculate_display()
        self.gen_tile_pattern()
