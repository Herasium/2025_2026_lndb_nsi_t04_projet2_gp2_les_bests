import arcade
from typing import List, Dict, Tuple, Any, Union

from modules.data.node import Node
from modules.ui.toolbox.hitbox import HitBox
from modules.ui.toolbox.entity import Entity
from modules.data import data

from line_profiler import profile


class Gate(Node):
    """
    Represents a logic gate node within the UI editor, handling visual
    representation, hitboxes for interaction, and data state.
    """

    def __init__(self, id: int) -> None:
        """
        Initialize a new Gate instance.

        Parameters:
        - id: Unique identifier for the gate node.
        """
        super().__init__(id)

        # Positioning logic based on grid size
        self._x: float = 0 + data.UI_EDITOR_GRID_SIZE / 2
        self._y: float = 0 + data.UI_EDITOR_GRID_SIZE / 2

        # Lists to store state and metadata for connection points
        self.inputs: List[int] = []
        self.outputs: List[int] = []
        self.inputs_sizes: List[int] = []
        self.outputs_sizes: List[int] = []

        self._name: str = "Default Gate"
        self.type: str = "Gate"
        self.gate_type: str = "Default"
        self.texts: Dict[str, Any] = {}

        # Visual entity components
        self.bg: Entity = Entity()
        self.bg.color = arcade.types.Color.from_hex_string("0F3FA8")
        self.entity: Entity = Entity()  # Assumed inherited or logic-defined entity
        self.entity.color = arcade.types.Color.from_hex_string("2563EB")

        self._camera: Tuple[float, float] = (0, 0)

        # Color constants for logic states
        self.input_off_color: arcade.types.Color = arcade.types.Color.from_hex_string(
            data.COLORS.VALUE_OFF
        )
        self.input_on_color: arcade.types.Color = arcade.types.Color.from_hex_string(
            data.COLORS.VALUE_ON
        )

        # Foreground label
        self.text: arcade.Text = arcade.Text(
            self._name,
            self.x,
            self.y,
            arcade.types.Color.from_hex_string("b45252"),
            24,
            anchor_x="center",
            anchor_y="center",
            font_name="Press Start 2P",
        )

        # Shadow/Background label
        self.bg_text: arcade.Text = arcade.Text(
            self._name,
            self.x,
            self.y,
            arcade.types.Color.from_hex_string("5f556a"),
            24,
            anchor_x="center",
            anchor_y="center",
            font_name="Press Start 2P",
        )

        self.tiles: Any = data.gate_tiles
        self.draw_hitboxes: bool = False
        self.exceptional_size_offset: int = 0

        # Initial layout calculations
        self.calculate_display()
        self.gen_tile_pattern()

    @property
    def name(self) -> str:
        """Get the name of the gate."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """
        Set the name and update input defaults and text displays.

        Parameters:
        - value: The new name string.
        """
        self._name = value
        # Logic to set default pin counts based on gate identity
        if self._name == "NOT":
            self.inputs = [0]
        else:
            self.inputs = [0, 0]

        # Sync text objects if they exist
        if hasattr(self, "text"):
            self.text.text = self._name
            self.bg_text.text = self._name

        # Recalculate dimensions if grid context is available
        if hasattr(self, "grid_size"):
            self.calculate_display()

    @property
    def x(self) -> float:
        """Get the x-coordinate of the gate."""
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        """Set x-coordinate and refresh display."""
        self._x = value
        self.calculate_display()

    @property
    def y(self) -> float:
        """Get the y-coordinate of the gate."""
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        """Set y-coordinate and refresh display."""
        self._y = value
        self.calculate_display()

    def calculate_display_lite(self) -> None:
        """
        Perform a lightweight update of visual positions without full hitbox recalculation.
        Used primarily during camera movements.
        """
        self.hide_text: bool = True
        # Update text positions relative to camera and center
        self.text.x = self.x + self.width / 2 + self._camera[0]
        self.text.y = (
            self.y + self.height / 1.6 + data.UI_EDITOR_GRID_SIZE / 4 + self._camera[1]
        )

        self.bg_text.x = self.text.x - 1
        self.bg_text.y = self.text.y + 2

        # Update entity and background bounds
        self.entity._x = self.x + self._camera[0]
        self.entity._y = self.y + self._camera[1]
        self.entity._width = self.width
        self.entity._height = self.height

        self.bg._x = self.x - 5
        self.bg._y = self.y - 5
        self.bg._width = self.width + 10
        self.bg._height = self.height + 10

    def update_text_position(self) -> None:
        """Placeholder for custom text position updates."""
        pass

    def calculate_display(self) -> None:
        """
        Calculate full gate dimensions, positions, and regenerate all input/output hitboxes.
        """
        self.both: bool = len(self.inputs) > 0 and len(self.outputs) > 0

        # Determine width based on the number of pins and offsets
        self.tile_width: int = (
            2 + len(self.inputs) + len(self.outputs) + self.exceptional_size_offset
        )
        self.tile_width += int(self.both) * 1  # Add spacing if both in and out exist

        self.width: float = self.tile_width * data.UI_EDITOR_GRID_SIZE
        self.height: float = 4 * data.UI_EDITOR_GRID_SIZE
        self.max: int = max(len(self.inputs), len(self.outputs)) + 1

        # Center text elements
        self.text.x = self.x + self.width / 2 + self._camera[0]
        self.text.y = (
            self.y + self.height / 1.6 + data.UI_EDITOR_GRID_SIZE / 4 + self._camera[1]
        )

        self.bg_text.x = self.text.x - 1
        self.bg_text.y = self.text.y + 2

        # Update main entities
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

        # Generate Input Hitboxes
        for i in range(len(self.inputs)):
            y = self.y + self._camera[1]
            x = (
                self.x
                + data.UI_EDITOR_GRID_SIZE * (i + 1 + self.exceptional_size_offset // 2)
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

        # Generate Output Hitboxes
        for i in range(len(self.outputs)):
            y = self.y + self._camera[1]
            # Offset x based on inputs and spacing
            x = (
                self.x
                + data.UI_EDITOR_GRID_SIZE
                * (
                    i
                    + 1
                    + int(self.both) * 1
                    + len(self.inputs)
                    + self.exceptional_size_offset // 2
                )
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

        self.update_text_position()

    @property
    def camera(self) -> Tuple[float, float]:
        """Get current camera offset."""
        return self._camera

    @camera.setter
    def camera(self, value: Tuple[float, float]) -> None:
        """Set camera offset and perform full recalculation."""
        self._camera = value
        self.calculate_display()

    def camera_moving(self, value: Tuple[float, float]) -> None:
        """
        Update camera offset during active movement.

        Parameters:
        - value: New (x, y) camera coordinates.
        """
        self._camera = value
        self.calculate_display_lite()

    def gen_tile_pattern(self) -> None:
        """
        Generates an array of tile indices representing the visual layout
        of the gate based on its inputs and outputs.
        """
        gate_tile_pattern: List[int] = []

        # Bottom Row: Corner, Input tiles, optional spacer, Output tiles, Corner
        gate_tile_pattern.append(7)
        for _ in range(len(self.inputs)):
            gate_tile_pattern.append(6)
        if self.both:
            gate_tile_pattern.append(0)
        for _ in range(len(self.outputs)):
            gate_tile_pattern.append(6)
        gate_tile_pattern.append(8)

        # First Row (Logic Row): Edge, logic-state tiles for inputs/outputs, Edge
        gate_tile_pattern.append(26)
        for i in range(len(self.inputs)):
            if self.inputs_sizes[i] == 1:
                gate_tile_pattern.append(15 if self.inputs[i] else 21)
            else:
                gate_tile_pattern.append(22)
        if self.both:
            gate_tile_pattern.append(1)
        for i in range(len(self.outputs)):
            if self.outputs_sizes[i] == 1:
                gate_tile_pattern.append(15 if self.outputs[i] else 21)
            else:
                gate_tile_pattern.append(22)
        gate_tile_pattern.append(19)

        # Second Row: Fill row
        gate_tile_pattern.append(31)
        for _ in range(self.tile_width - 2):
            gate_tile_pattern.append(13)
        gate_tile_pattern.append(25)

        # Top Row: Top border corners and edges
        gate_tile_pattern.append(28)
        for _ in range(self.tile_width - 2):
            gate_tile_pattern.append(2)
        gate_tile_pattern.append(27)

        self.gate_tile_pattern = gate_tile_pattern

    @profile
    def draw_tiles(self) -> None:
        """
        Renders the gate's texture to the screen.
        Determines the specific texture variant based on input/output binary state.
        """
        width: int = self.tile_width
        height: int = 4

        # Prepare state bits for texture lookup
        out: List[int] = self.outputs.copy()
        inp: List[int] = self.inputs.copy()

        # Zero out multi-bit signals for the visual representation
        for i in range(len(inp)):
            if self.inputs_sizes[i] != 1:
                inp[i] = 0
        for i in range(len(out)):
            if self.outputs_sizes[i] != 1:
                out[i] = 0

        # Create a binary integer key from the reversed pin states
        out.reverse()
        inp.reverse()
        current: int = int("".join(map(str, map(int, (out + inp)))), 2)

        tile_x: float = self.x + self._camera[0]
        tile_y: float = self.y + self._camera[1]

        # Define destination rectangle
        rect: arcade.XYWH = arcade.XYWH(
            x=tile_x,
            y=tile_y,
            width=width * data.UI_EDITOR_GRID_SIZE,
            height=height * data.UI_EDITOR_GRID_SIZE,
            anchor=arcade.Vec2(0, 0),
        )

        # Fetch and draw the calculated texture
        arcade.draw_texture_rect(data.IMAGE.get_texture(self.gate_type, current), rect)

    @profile
    def draw(self) -> None:
        """
        Main draw call for the gate. Renders tiles and optional debug hitboxes.
        """
        self.draw_tiles()

        # Debugging: Draw hitboxes if enabled
        if self.draw_hitboxes:
            for i in self.inputs_hitboxes:
                i.draw()
            for i in self.outputs_hitboxes:
                i.draw()
            self.entity.hitbox.draw()

    @property
    def touched(self) -> Union[bool, Tuple[int, int, int]]:
        """
        Check if any gate hitboxes are being interacted with.

        Returns:
        - bool: False if no hitboxes are touched.
        - tuple: (type, index, size) where type 1 is input, 2 is output.
        """
        touched: Union[bool, Tuple[int, int, int]] = False

        # Check all input pins
        for a in range(len(self.inputs_hitboxes)):
            i = self.inputs_hitboxes[a]
            if i.touched:
                touched = (1, a, self.inputs_sizes[a])

        # Check all output pins
        for a in range(len(self.outputs_hitboxes)):
            i = self.outputs_hitboxes[a]
            if i.touched:
                touched = (2, a, self.outputs_sizes[a])

        return touched

    def save(self) -> Dict[str, Any]:
        """
        Serialize the gate's state for saving.

        Returns:
        - dict: A dictionary containing position, type, pin data, and ID.
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
        Restore the gate's state from a dictionary.

        Parameters:
        - data: Dictionary containing gate state data.
        """
        self.type = data["type"]
        self.inputs = data.get("inputs", [])
        self.outputs = data.get("outputs", [])
        self.gate_type = data.get("gate", "")
        self.id = data["id"]
        # Setting x and y triggers calculate_display()
        self.x = data["x"]
        self.y = data["y"]

    def __str__(self) -> str:
        """
        Return a string representation of the gate.

        Returns:
        - str: Formatted gate details.
        """
        result: str = (
            f"Gate {self._name} (#{self.id}), {len(self.inputs)} Inputs ({self.inputs}), {len(self.outputs)} Outputs ({self.outputs})"
        )
        return result
