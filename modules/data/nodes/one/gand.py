from typing import List, Union

from modules.data.gate import Gate


class And(Gate):
    """
    Represents an AND logic gate.

    Attributes:
        name (str): The display name of the gate.
        type (str): The high-level category of the object.
        gate_type (str): The specific logic type (AND).
        inputs (List[int]): Current state of input signals.
        outputs (List[int]): Current state of output signals.
        inputs_sizes (List[int]): Expected bit-size for each input.
        outputs_sizes (List[int]): Bit-size for each output.
    """

    def __init__(self, id: Union[int, str]) -> None:
        """
        Initializes an And gate instance.

        Parameters:
            - id: Unique identifier for the gate instance.
        """
        # Initialize the base Gate class
        super().__init__(id)

        # Define gate metadata
        self.name: str = "AND"
        self.type: str = "Gate"
        self.gate_type: str = "AND"

        # Initialize signal arrays and their corresponding bit sizes
        self.inputs: List[int] = [0, 0]
        self.outputs: List[int] = [0]
        self.inputs_sizes: List[int] = [1, 1]
        self.outputs_sizes: List[int] = [1]

        # Prepare visual representations for the gate
        self.calculate_display()  # Calculate coordinate/display geometry
        self.gen_tile_pattern()  # Generate tile graphics for rendering
