import arcade
from typing import List, Dict, Union

from modules.data.gate import Gate
from modules.data import data
from modules.ui.toolbox.text import Text


class Complex(Gate):
    """
    A class representing a Complex logic gate, extending the base Gate functionality.
    Handles multi-bit inputs/outputs and manages associated UI text displays.
    """

    def __init__(self, id: Union[int, str]) -> None:
        """
        Initialize the Complex gate with default properties and display settings.

        Parameters:
        - id: A unique identifier for the gate instance.

        Returns:
        - None
        """
        super().__init__(id)

        # Basic gate identity metadata
        self.name: str = "COMP"
        self.type: str = "Complex"
        self.gate_type: str = "COMP"

        # Display and UI flags
        self.draw_hitboxes: bool = False
        self.hide_text: bool = False

        # State storage for signals and their bit-widths
        self.inputs: List[int] = []
        self.outputs: List[int] = []
        self.inputs_sizes: List[int] = []
        self.outputs_sizes: List[int] = []

        # Dictionary to hold UI Text objects for multi-bit labels
        self.texts: Dict[str, Text] = {}

        # Initialization routines for rendering and UI
        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()

    def setup_texts(self) -> None:
        """
        Create and position Text objects for inputs and outputs that have a
        size greater than 1 bit.

        Parameters:
        - None

        Returns:
        - None
        """
        self.texts = {}

        # Generate labels for multi-bit input pins
        for i in range(len(self.inputs)):
            if self.inputs_sizes[i] != 1:
                # Calculate X/Y position based on the pin's hitbox and grid sizing
                x: float = self.inputs_hitboxes[i].x + data.UI_EDITOR_GRID_SIZE / 2
                y: float = self.inputs_hitboxes[i].y + data.UI_EDITOR_GRID_SIZE * 1.5
                new: Text = Text(
                    x=x,
                    y=y,
                    width=data.UI_EDITOR_GRID_SIZE,
                    height=data.UI_EDITOR_GRID_SIZE,
                    text=str(self.inputs[i]),
                    size=10,
                )
                self.texts[f"i{i}"] = new

        # Generate labels for multi-bit output pins
        for i in range(len(self.outputs)):
            if self.outputs_sizes[i] != 1:
                x: float = self.outputs_hitboxes[i].x + data.UI_EDITOR_GRID_SIZE / 2
                y: float = self.outputs_hitboxes[i].y + data.UI_EDITOR_GRID_SIZE * 1.5
                new: Text = Text(
                    x=x,
                    y=y,
                    width=data.UI_EDITOR_GRID_SIZE,
                    height=data.UI_EDITOR_GRID_SIZE,
                    text=str(self.outputs[i]),
                    size=10,
                )
                self.texts[f"o{i}"] = new

    def update_text_readings(self) -> None:
        """
        Synchronize the string content of the UI Text objects with the current
        integer values of the inputs and outputs.

        Parameters:
        - None

        Returns:
        - None
        """
        # Optimization: exit if there are no text labels to update
        if len(self.texts.keys()) == 0:
            return

        # Update input labels
        for i in range(len(self.inputs)):
            if self.inputs_sizes[i] != 1:
                self.texts[f"i{i}"].text = str(self.inputs[i])

        # Update output labels
        for i in range(len(self.outputs)):
            if self.outputs_sizes[i] != 1:
                self.texts[f"o{i}"].text = str(self.outputs[i])

    def update_text_position(self) -> None:
        """
        Update the coordinates of the UI Text objects to match the current
        location of the gate's hitboxes (e.g., during movement).

        Parameters:
        - None

        Returns:
        - None
        """
        self.hide_text = False
        if len(self.texts.keys()) == 0:
            return

        # Re-calculate positions for input text labels
        for i in range(len(self.inputs)):
            if self.inputs_sizes[i] != 1:
                x: float = self.inputs_hitboxes[i].x + data.UI_EDITOR_GRID_SIZE / 2
                y: float = self.inputs_hitboxes[i].y + data.UI_EDITOR_GRID_SIZE * 1.5
                self.texts[f"i{i}"]._x = x
                self.texts[f"i{i}"].y = y

        # Re-calculate positions for output text labels
        for i in range(len(self.outputs)):
            if self.outputs_sizes[i] != 1:
                x: float = self.outputs_hitboxes[i].x + data.UI_EDITOR_GRID_SIZE / 2
                y: float = self.outputs_hitboxes[i].y + data.UI_EDITOR_GRID_SIZE * 1.5
                self.texts[f"o{i}"]._x = x
                self.texts[f"o{i}"].y = y

    def draw_tiles(self) -> None:
        """
        Render the gate's texture and its multi-bit text labels to the screen.
        Determines the specific texture variation based on current bit states.

        Parameters:
        - None

        Returns:
        - None
        """
        width: int = self.tile_width
        height: int = 4

        # Create copies to manipulate for texture ID calculation
        out: List[int] = self.outputs.copy()
        inp: List[int] = self.inputs.copy()

        # Zero out multi-bit values for bitwise string conversion (only single bits affect texture)
        for i in range(len(inp)):
            if self.inputs_sizes[i] != 1:
                inp[i] = 0

        for i in range(len(out)):
            if self.outputs_sizes[i] != 1:
                out[i] = 0

        # Reverse and concatenate lists to form a binary string, then convert to integer
        out.reverse()
        inp.reverse()
        current: int = int("".join(map(str, map(int, (out + inp)))), 2)

        # Calculate screen coordinates relative to camera position
        tile_x: float = self.x + self._camera[0]
        tile_y: float = self.y + self._camera[1]

        # Define the rectangle area for drawing the texture
        rect: arcade.XYWH = arcade.XYWH(
            x=tile_x,
            y=tile_y,
            width=width * data.UI_EDITOR_GRID_SIZE,
            height=height * data.UI_EDITOR_GRID_SIZE,
            anchor=arcade.Vec2(0, 0),
        )

        # Render the specific texture for the current bit state
        arcade.draw_texture_rect(data.IMAGE.get_texture(self.gate_type, current), rect)

        # Draw all active text labels if not hidden
        if not self.hide_text:
            for i in self.texts:
                self.texts[i].draw()
