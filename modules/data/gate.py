import arcade
from typing import List, Dict, Tuple, Any, Union
import math

from modules.data.node import Node
from modules.ui.toolbox.hitbox import HitBox
from modules.ui.toolbox.entity import Entity
from modules.data import data

from line_profiler import profile

"""
Provides the Gate class for representing and rendering logic components
within the visual editor environment.
"""


class Gate(Node):
    """
    Manages the lifecycle, visual state, and interaction hitboxes of a
    logic gate node in the UI editor.
    """

    @profile
    def __init__(self, id: int) -> None:
        """
        Args:
            id: Unique identifier for the gate instance.
        """
        super().__init__(id)

        self._x: float = 0 + data.UI_EDITOR_GRID_SIZE / 2
        self._y: float = 0 + data.UI_EDITOR_GRID_SIZE / 2

        self.inputs: List[int] = []
        self.outputs: List[int] = []
        self.inputs_sizes: List[int] = []
        self.outputs_sizes: List[int] = []

        self._name: str = "DG"
        self.type: str = "Gate"
        self.gate_type: str = "Default"
        self.texts: Dict[str, Any] = {}

        self.bg: Entity = Entity()
        self.bg.color = arcade.types.Color.from_hex_string("0F3FA8")
        self.entity: Entity = Entity()
        self.entity.color = arcade.types.Color.from_hex_string("2563EB")

        self._camera: Tuple[float, float] = (0, 0)

        self.input_off_color: arcade.types.Color = arcade.types.Color.from_hex_string(
            data.COLORS.VALUE_OFF
        )
        self.input_on_color: arcade.types.Color = arcade.types.Color.from_hex_string(
            data.COLORS.VALUE_ON
        )

        self.tiles: Any = data.gate_tiles
        self.draw_hitboxes: bool = True
        self.exceptional_size_offset: int = 0
        self._moving = False

        self.calculate_display()
        self.gen_tile_pattern()

    @property
    def name(self) -> str:
        """Returns the current gate name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Args:
            value: String identifier to apply to the gate.
        """
        self._name = value

        self.calculate_display()

    @property
    def moving(self) -> str:
        return self._moving

    @name.setter
    def moving(self, value: str) -> None:
        self._moving = value
        self.hide_text = value
        if self._moving == False:
            self.calculate_display()

    @property
    def x(self) -> float:
        """Returns the current x-coordinate."""
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        """
        Args:
            value: New horizontal position.
        """
        self._x = value
        self.calculate_display()

    @property
    def y(self) -> float:
        """Returns the current y-coordinate."""
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        """
        Args:
            value: New vertical position.
        """
        self._y = value
        self.calculate_display()

    def calculate_display_lite(self) -> None:
        """Performs optimized visual update for camera movement scenarios."""
        self.hide_text: bool = True

        self.entity._x = self.x + self._camera[0]
        self.entity._y = self.y + self._camera[1]
        self.entity._width = self.width
        self.entity._height = self.height

        self.bg._x = self.x - 5
        self.bg._y = self.y - 5
        self.bg._width = self.width + 10
        self.bg._height = self.height + 10

    def update_text_position(self) -> None:
        """Hook for specialized label alignment updates."""
        pass

    def calculate_display(self) -> None:
        """Calculates internal dimensions and refreshes input/output interaction hitboxes."""
        self.both: bool = len(self.inputs) > 0 and len(self.outputs) > 0

        pin_width_required = 2 + len(self.inputs) + len(self.outputs) + (1 if self.both else 0)
        text_width_required = max(round(len(self._name) * 40/27),5)

        if text_width_required > pin_width_required:
            self.exceptional_size_offset = text_width_required - pin_width_required
        else:
            self.exceptional_size_offset = 0

        self.tile_width = pin_width_required + self.exceptional_size_offset

        self.width: float = self.tile_width * data.UI_EDITOR_GRID_SIZE
        self.height: float = 4 * data.UI_EDITOR_GRID_SIZE
        self.max: int = max(len(self.inputs), len(self.outputs)) + 1

        self.entity.x = self.x + self._camera[0]
        self.entity.y = self.y + self._camera[1]
        self.entity.width = self.width
        self.entity.height = self.height

        self.bg.x = self.x - 5
        self.bg.y = self.y - 5
        self.bg.width = self.width + 10
        self.bg.height = self.height + 10

        self.inputs_position: List[Tuple[float, float]] = []
        self.outputs_position: List[Tuple[float, float]] = []
        self.inputs_hitboxes: List[HitBox] = []
        self.outputs_hitboxes: List[HitBox] = []

        for i in range(len(self.inputs)):
            y = self.y + self._camera[1]
            input_index = i + 1 
            x = (
                self.x
                + data.UI_EDITOR_GRID_SIZE * input_index
                + self._camera[0]
            )

            self.inputs_position.append(
                (x + data.UI_EDITOR_GRID_SIZE / 2, y + data.UI_EDITOR_GRID_SIZE / 2)
            )
            self.inputs_hitboxes.append(
                HitBox(
                    x=x,
                    y=y,
                    width=data.UI_EDITOR_GRID_SIZE,
                    height=data.UI_EDITOR_GRID_SIZE,
                )
            )

        for i in range(len(self.outputs)):
            y = self.y + self._camera[1]
            output_index = self.tile_width - len(self.outputs) - 1 + i
            x = (
                self.x
                + data.UI_EDITOR_GRID_SIZE * output_index
                + self._camera[0]
            )

            self.outputs_position.append(
                (x + data.UI_EDITOR_GRID_SIZE / 2, y + data.UI_EDITOR_GRID_SIZE / 2)
            )
            self.outputs_hitboxes.append(
                HitBox(
                    x=x,
                    y=y,
                    width=data.UI_EDITOR_GRID_SIZE,
                    height=data.UI_EDITOR_GRID_SIZE,
                )
            )
        if not self._moving:
            self.update_text_position()

    @property
    def camera(self) -> Tuple[float, float]:
        """Returns the active camera offset."""
        return self._camera

    @camera.setter
    def camera(self, value: Tuple[float, float]) -> None:
        """
        Args:
            value: (x, y) coordinates for the camera view.
        """
        self._camera = value
        self.calculate_display()

    def camera_moving(self, value: Tuple[float, float]) -> None:
        """
        Args:
            value: Intermediate (x, y) coordinates during camera transition.
        """
        self._camera = value
        self.calculate_display_lite()

    def gen_tile_pattern(self) -> None:
        """Generates the grid-based tile indices array based on node configuration."""
        gate_tile_pattern: List[int] = []

        sum_io = len(self.inputs) + len(self.outputs) + 2

        gate_tile_pattern.append(7)
        for _ in range(len(self.inputs)):
            gate_tile_pattern.append(6)
        for i in range(self.tile_width - sum_io):
            gate_tile_pattern.append(0)
        for _ in range(len(self.outputs)):
            gate_tile_pattern.append(6)
        gate_tile_pattern.append(8)

        if len(self.inputs) > 0:
            gate_tile_pattern.append(26)
        else:
            gate_tile_pattern.append(30)
        for i in range(len(self.inputs)):
            if self.inputs_sizes[i] == 1:
                gate_tile_pattern.append(15 if self.inputs[i] else 21)
            else:
                gate_tile_pattern.append(22)

        for i in range(self.tile_width - sum_io):
            if i == 0 and i == self.tile_width - sum_io -1 and self.both:
                gate_tile_pattern.append(1)
            elif i == 0 and len(self.inputs)>0:
                gate_tile_pattern.append(33)
            elif i == self.tile_width - sum_io - 1 and len(self.outputs)>0:
                gate_tile_pattern.append(34)
            else:
                gate_tile_pattern.append(13)


        for i in range(len(self.outputs)):
            if self.outputs_sizes[i] == 1:
                gate_tile_pattern.append(15 if self.outputs[i] else 21)
            else:
                gate_tile_pattern.append(22)

        if len(self.outputs) > 0:
            gate_tile_pattern.append(19)
        else:
            gate_tile_pattern.append(32)



        gate_tile_pattern.append(31)
        for _ in range(self.tile_width - 2):
            gate_tile_pattern.append(13)
        gate_tile_pattern.append(25) 

        gate_tile_pattern.append(28)
        for _ in range(self.tile_width - 2):
            gate_tile_pattern.append(2)
        gate_tile_pattern.append(27)

        self.gate_tile_pattern = gate_tile_pattern

    def draw_tiles(self) -> None:
        """Renders the graphical texture representation of the gate state."""
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

        # Construct binary state key: [Output State] + [Input State] reversed
        out.reverse()
        inp.reverse()
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

    def draw(self) -> None:
        """Executes rendering logic for the gate and optional debug hitboxes."""
        self.draw_tiles()

        if self.draw_hitboxes:
            for i in self.inputs_hitboxes:
                i.draw()
            for i in self.outputs_hitboxes:
                i.draw()
            self.entity.hitbox.draw()

    @property
    def touched(self) -> Union[bool, Tuple[int, int, int]]:
        """
        Returns:
            Either False or a tuple containing (Pin Type, Index, Bit Size)
            where Pin Type 1 represents input and 2 represents output.
        """
        touched: Union[bool, Tuple[int, int, int]] = False

        for a in range(len(self.inputs_hitboxes)):
            i = self.inputs_hitboxes[a]
            if i.touched:
                touched = (1, a, self.inputs_sizes[a])

        for a in range(len(self.outputs_hitboxes)):
            i = self.outputs_hitboxes[a]
            if i.touched:
                touched = (2, a, self.outputs_sizes[a])

        return touched

    def save(self) -> Dict[str, Any]:
        """
        Returns:
            Dict representing the serializable gate state.
        """
        return {
            "x": self.x,
            "y": self.y,
            "type": self.type,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "gate": self.gate_type,
            "id": self.id,
        }

    def load(self, data: Dict[str, Any]) -> None:
        """
        Args:
            data: State dictionary containing gate properties to restore.
        """
        self.type = data["type"]
        self.inputs = data.get("inputs", [])
        self.outputs = data.get("outputs", [])
        self.gate_type = data.get("gate", "")
        self.id = data["id"]
        self.x = data["x"]
        self.y = data["y"]

    def __str__(self) -> str:
        """
        Returns:
            Human-readable summary of the gate and its connectivity.
        """
        result: str = (
            f"Gate {self._name} (#{self.id}), {len(self.inputs)} Inputs ({self.inputs}), {len(self.outputs)} Outputs ({self.outputs})"
        )
        return result
