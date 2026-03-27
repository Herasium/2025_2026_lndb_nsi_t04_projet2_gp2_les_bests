import arcade
from typing import List, Dict, Union

from modules.data.gate import Gate
from modules.data import data
from modules.ui.toolbox.text import Text

"""
This module provides the Complex gate implementation for logic simulation.
It handles multi-bit signal management and UI synchronization for gates.
"""


class Complex(Gate):
    """
    Manages a logic gate capable of processing multi-bit inputs and outputs,
    including the rendering of dynamic UI labels for these signals.
    """

    def __init__(self, id: Union[int, str]) -> None:
        """
        Args:
            id: Identifier used to reference this gate instance.
        """
        super().__init__(id)

        self.name: str = "COMP"
        self.type: str = "Complex"
        self.gate_type: str = "COMP"

        self.hide_text: bool = False

        self.inputs: List[int] = []
        self.outputs: List[int] = []
        self.inputs_sizes: List[int] = []
        self.outputs_sizes: List[int] = []

        self.texts: Dict[str, Text] = {}

        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()

    def setup_texts(self) -> None:
        """
        Initializes UI Text objects for any input or output pins defined with
        a bit-width greater than one.
        """
        self.texts = {}

        for i in range(len(self.inputs)):
            if self.inputs_sizes[i] != 1:
                x: float = self.inputs_hitboxes[i].x + data.UI_EDITOR_GRID_SIZE / 2
                y: float = self.inputs_hitboxes[i].y + data.UI_EDITOR_GRID_SIZE * 1.5
                new: Text = Text(
                    x=x,
                    y=y,
                    width=data.UI_EDITOR_GRID_SIZE,
                    height=data.UI_EDITOR_GRID_SIZE,
                    text=str(self.inputs[i]),
                    size=7,
                )
                self.texts[f"i{i}"] = new

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
                    size=7,
                )
                self.texts[f"o{i}"] = new

    def update_text_readings(self) -> None:
        """
        Synchronizes existing UI Text labels with the latest internal signal values.
        """
        if len(self.texts.keys()) == 0:
            return

        for i in range(len(self.inputs)):
            if self.inputs_sizes[i] != 1:
                self.texts[f"i{i}"].text = str(self.inputs[i])

        for i in range(len(self.outputs)):
            if self.outputs_sizes[i] != 1:
                self.texts[f"o{i}"].text = str(self.outputs[i])

    def update_text_position(self) -> None:
        """
        Updates UI Text coordinates to track movement of the gate hitboxes.
        """
        self.hide_text = False
        if len(self.texts.keys()) == 0:
            return

        for i in range(len(self.inputs)):
            if self.inputs_sizes[i] != 1:
                x: float = self.inputs_hitboxes[i].x + data.UI_EDITOR_GRID_SIZE / 2
                y: float = self.inputs_hitboxes[i].y + data.UI_EDITOR_GRID_SIZE * 1.5
                self.texts[f"i{i}"]._x = x
                self.texts[f"i{i}"].y = y

        for i in range(len(self.outputs)):
            if self.outputs_sizes[i] != 1:
                x: float = self.outputs_hitboxes[i].x + data.UI_EDITOR_GRID_SIZE / 2
                y: float = self.outputs_hitboxes[i].y + data.UI_EDITOR_GRID_SIZE * 1.5
                self.texts[f"o{i}"]._x = x
                self.texts[f"o{i}"].y = y

    def draw_tiles(self) -> None:
        """
        Renders the gate texture and associated labels based on the current logic state.
        """
        width: int = self.tile_width
        height: int = 4

        out: List[int] = self.outputs.copy()
        inp: List[int] = self.inputs.copy()

        for i in range(len(inp)):
            if self.inputs_sizes[i] != 1:
                inp[i] = 0

        for i in range(len(out)):
            if self.outputs_sizes[i] != 1:
                out[i] = 0

        out.reverse()
        inp.reverse()
        # Calculate texture state index by converting concatenated output/input binary values
        current: int = int("".join(map(str, map(int, (out + inp)))), 2)

        tile_x: float = self.x + self._camera[0]
        tile_y: float = self.y + self._camera[1]

        rect: arcade.XYWH = arcade.XYWH(
            x=tile_x,
            y=tile_y,
            width=width * data.UI_EDITOR_GRID_SIZE,
            height=height * data.UI_EDITOR_GRID_SIZE,
            anchor=arcade.Vec2(0, 0),
        )

        arcade.draw_texture_rect(data.IMAGE.get_texture(self.gate_type, current), rect)

        if not self.hide_text:
            for i in self.texts:
                self.texts[i].draw()
