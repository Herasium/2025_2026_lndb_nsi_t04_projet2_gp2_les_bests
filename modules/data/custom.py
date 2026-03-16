import arcade
from typing import Any, Dict, List, Optional

from modules.data.complex import Complex
from modules.data import data as data_module


class CustomGate(Complex):
    """
    A class representing a user-defined custom logic gate within the simulator.
    Inherits from the Complex base class.
    """

    def __init__(self, id: int, chip: Optional[Any] = None) -> None:
        """Initialize a CustomGate instance.

        Parameters:
        - id: A unique integer identifier for this gate instance.
        - chip: An optional chip object representing the internal logic of this gate.
        """
        super().__init__(id)

        # Basic identification and metadata
        self.name: str = chip.name
        self.type: str = "Custom"
        self.base_chip_id: int = chip.id
        self.chip: Any = chip.copy()  # Create a unique instance of the internal chip
        self.gate_type: str = "Custom"

        # Initialize I/O structures based on the internal chip
        self.update_io()

        # Visual and UI setup
        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()

    def prop_io(self) -> None:
        """Propagate external input values to the internal chip's input gates.

        Returns:
        - None
        """
        chip_inputs: List[int] = self.chip.get_inputs()
        # Map this gate's inputs to the internal chip's corresponding input pins
        for i in range(len(self.inputs)):
            self.chip.gates[chip_inputs[i]].outputs[0] = self.inputs[i]

    def update_io(self) -> None:
        """Synchronize the gate's I/O pins and bus sizes with the internal chip structure.

        Returns:
        - None
        """
        self.inputs: List[int] = []
        self.outputs: List[int] = []
        self.inputs_sizes: List[int] = []
        self.outputs_sizes: List[int] = []

        # Process internal chip inputs to define external gate inputs
        chip_inputs: List[int] = self.chip.get_inputs()
        for i in chip_inputs:
            self.inputs.append(self.chip.gates[i].outputs[0])
            self.inputs_sizes.append(self.chip.gates[i].outputs_sizes[0])

        # Process internal chip outputs to define external gate outputs
        chip_outputs: List[int] = self.chip.get_outputs()
        for i in chip_outputs:
            self.outputs.append(self.chip.gates[i].inputs[0])
            self.outputs_sizes.append(self.chip.gates[i].inputs_sizes[0])

        # Refresh text elements to reflect new I/O states
        self.update_text_readings()

    def draw_tiles(self) -> None:
        """Render the gate's visual representation using textures and labels.

        Returns:
        - None
        """
        width: int = self.tile_width
        height: int = 4

        # Deep copy I/O states to calculate the specific texture variant (bitmask)
        out: List[int] = self.outputs.copy()
        inp: List[int] = self.inputs.copy()

        # Filter out bus values (size != 1) to simplify texture bitmask calculation
        for i in range(len(inp)):
            if self.inputs_sizes[i] != 1:
                inp[i] = 0

        for i in range(len(out)):
            if self.outputs_sizes[i] != 1:
                out[i] = 0

        # Create a binary string from reversed outputs and inputs to determine current state index
        out.reverse()
        inp.reverse()
        current: int = int("".join(map(str, map(int, (out + inp)))), 2)

        # Calculate coordinates relative to camera position
        tile_x: float = self.x + self._camera[0]
        tile_y: float = self.y + self._camera[1]

        # Define the rectangular area for drawing
        rect: arcade.XYWH = arcade.XYWH(
            x=tile_x,
            y=tile_y,
            width=width * data_module.UI_EDITOR_GRID_SIZE,
            height=height * data_module.UI_EDITOR_GRID_SIZE,
            anchor=arcade.Vec2(0, 0),
        )

        # Render the specific texture for this gate and state
        arcade.draw_texture_rect(
            data_module.IMAGE.get_texture(self.base_chip_id, current), rect
        )

        # Draw text labels if they aren't hidden
        if not self.hide_text:
            for i in self.texts:
                self.texts[i].draw()

    def save(self) -> Dict[str, Any]:
        """Serialize the current state of the gate for saving to a file.

        Returns:
        - Dict[str, Any]: A dictionary containing the gate's spatial and logical properties.
        """
        return {
            "x": self.x,
            "y": self.y,
            "type": self.type,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "gate": self.gate_type,
            "id": self.id,
            "parent": self.base_chip_id,
        }

    def load(self, data: Dict[str, Any]) -> None:
        """Restore the gate's state from a dictionary.

        Parameters:
        - data: A dictionary containing the saved state of the gate.

        Returns:
        - None
        """
        # Assign primary attributes from the dictionary
        self.type = data["type"]
        self.inputs = data.get("inputs", [])
        self.outputs = data.get("outputs", [])
        self.gate_type = data.get("gate", "")
        self.id = data["id"]
        self.x = data["x"]
        self.y = data["y"]
        self.base_chip_id = data["parent"]

        # Instantiate a fresh copy of the internal logic from the master library
        self.chip = data_module.loaded_chips[self.base_chip_id].copy()

        # Re-initialize visual and logical structures
        self.update_io()
        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()
