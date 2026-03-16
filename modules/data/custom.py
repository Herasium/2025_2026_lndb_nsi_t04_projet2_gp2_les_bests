"""Provides the CustomGate class for managing user-defined logic gate instances."""

import arcade
from typing import Any, Dict, List, Optional

from modules.data.complex import Complex
from modules.data import data as data_module


class CustomGate(Complex):
    """Represents a user-defined logic gate wrapping an internal chip architecture."""

    def __init__(self, id: int, chip: Optional[Any] = None) -> None:
        """Initializes a new CustomGate instance.

        Args:
            id: Unique identifier for the gate.
            chip: The chip definition to encapsulate.
        """
        super().__init__(id)

        self.name: str = chip.name
        self.type: str = "Custom"
        self.base_chip_id: int = chip.id
        self.chip: Any = chip.copy()
        self.gate_type: str = "Custom"

        self.update_io()

        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()

    def prop_io(self) -> None:
        """Propagates current external input values into the internal chip structure."""
        chip_inputs: List[int] = self.chip.get_inputs()
        for i in range(len(self.inputs)):
            self.chip.gates[chip_inputs[i]].outputs[0] = self.inputs[i]

    def update_io(self) -> None:
        """Synchronizes gate I/O pins and bus metadata with the underlying chip."""
        self.inputs: List[int] = []
        self.outputs: List[int] = []
        self.inputs_sizes: List[int] = []
        self.outputs_sizes: List[int] = []

        chip_inputs: List[int] = self.chip.get_inputs()
        for i in chip_inputs:
            self.inputs.append(self.chip.gates[i].outputs[0])
            self.inputs_sizes.append(self.chip.gates[i].outputs_sizes[0])

        chip_outputs: List[int] = self.chip.get_outputs()
        for i in chip_outputs:
            self.outputs.append(self.chip.gates[i].inputs[0])
            self.outputs_sizes.append(self.chip.gates[i].inputs_sizes[0])

        self.update_text_readings()

    def draw_tiles(self) -> None:
        """Renders the gate using state-dependent textures."""
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
        # Pack state bits into an integer to select the appropriate texture index
        current: int = int("".join(map(str, map(int, (out + inp)))), 2)

        tile_x: float = self.x + self._camera[0]
        tile_y: float = self.y + self._camera[1]

        rect: arcade.XYWH = arcade.XYWH(
            x=tile_x,
            y=tile_y,
            width=width * data_module.UI_EDITOR_GRID_SIZE,
            height=height * data_module.UI_EDITOR_GRID_SIZE,
            anchor=arcade.Vec2(0, 0),
        )

        arcade.draw_texture_rect(
            data_module.IMAGE.get_texture(self.base_chip_id, current), rect
        )

        if not self.hide_text:
            for i in self.texts:
                self.texts[i].draw()

    def save(self) -> Dict[str, Any]:
        """Serializes the gate state for storage.

        Returns:
            Dictionary containing spatial and logical configuration data.
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
        """Hydrates the gate state from provided configuration data.

        Args:
            data: Configuration dictionary to load.
        """
        self.type = data["type"]
        self.inputs = data.get("inputs", [])
        self.outputs = data.get("outputs", [])
        self.gate_type = data.get("gate", "")
        self.id = data["id"]
        self.x = data["x"]
        self.y = data["y"]
        self.base_chip_id = data["parent"]

        self.chip = data_module.loaded_chips[self.base_chip_id].copy()

        self.update_io()
        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()
