"""
This module defines the LevelEditorView, which provides the primary graphical
interface for constructing and managing circuit levels within the application.
"""

import arcade
import time
from typing import Optional, List, Tuple, Any

from modules.ui.mouse import mouse
from modules.ui.toolbox.entity import Entity
from modules.ui.toolbox.id_generator import random_id
from modules.ui.level_editor.save import SaveFrame
from modules.data.nodes.path import Path
from modules.data.level import Level
from modules.data import data
from modules.data.gate_index import gate_types
from modules.engine import Engine


class LevelEditorView(arcade.View):
    """
    Manages the level editor interface, handling gate placement,
    path creation, camera movement, and interaction logic.
    """

    def __init__(self, id: Optional[str] = None):
        super().__init__()

        self.follower: Entity = Entity()
        self.follower.height = data.UI_EDITOR_GRID_SIZE
        self.follower.width = data.UI_EDITOR_GRID_SIZE

        self.bottom_zone_collider: Entity = Entity()
        self.bottom_zone_collider.x = 0
        self.bottom_zone_collider.y = 0
        self.bottom_zone_collider.width = data.WINDOW_WIDTH
        self.bottom_zone_collider.height = 3 * 64

        self.selected_follower: Optional[Any] = None
        self.moving_gate: Optional[Any] = None
        self.current_path: Optional[Path] = None

        self.moving_gate_offset: Tuple[int, int] = (0, 0)

        self._real_camera_position: Tuple[int, int] = (0, 0)
        self.camera_position: Tuple[int, int] = (0, 0)

        self.bottom_gates: List[Any] = []
        self.bottom_gate_bar()

        self.background_color = arcade.types.Color.from_hex_string("121212")

        self.camera_hold: bool = False
        self.fps: float = 0
        self.delta_time: float = 1
        self.frame_count: int = 0
        self.last_time: float = 1

        self.engine: Engine = Engine()
        self.stress_test: bool = False

        if id is None:
            self.level = Level(random_id())
        else:
            if id in data.loaded_levels:
                self.level = data.loaded_levels[id]
            else:
                self.level = Level(random_id())

    def bottom_bar_width_sum(self) -> int:
        """
        Calculates the cumulative width of all gates currently in the toolbar.

        Returns:
            The total width in pixels.
        """
        result = 0
        for i in self.bottom_gates:
            result += i.tile_width
        return result

    def bottom_gate_bar(self) -> None:
        """Populates the bottom toolbar with available gate types."""
        for i in gate_types:
            position = (
                self.bottom_bar_width_sum() + len(self.bottom_gates)
            ) * data.UI_EDITOR_GRID_SIZE + 64
            self.bottom_gates.append(gate_types[i](f"bottom_gate_{random_id()}"))
            self.bottom_gates[-1].camera = (0, 0)
            self.bottom_gates[-1].y = 3 * data.UI_EDITOR_GRID_SIZE
            self.bottom_gates[-1].x = position

    def get_hovered_bottom_gate(self) -> Optional[str]:
        """
        Identifies if the cursor is hovering over a specific gate in the toolbar.

        Returns:
            The type of the hovered gate, or None if no gate is under the cursor.
        """
        for i in self.bottom_gates:
            if i.entity.touched:
                return i.gate_type
        return None

    def draw_bottom_gates(self) -> None:
        """Renders the UI elements within the bottom toolbar."""
        for i in self.bottom_gates:
            i.draw()

    def draw_tile(self, id: str, x: int, y: int) -> None:
        """
        Renders an individual border tile.

        Args:
            id: The unique identifier for the texture.
            x: Horizontal coordinate.
            y: Vertical coordinate.
        """
        rect = arcade.XYWH(x=x, y=y, width=64, height=64, anchor=arcade.Vec2(0, 0))
        arcade.draw_texture_rect(data.ui_border_tiles[id], rect)

    def reset(self) -> None:
        """Clears or reinitializes the editor state."""
        pass

    def draw_frame_border(self) -> None:
        """Renders the outer editor window interface overlay."""
        rect = arcade.XYWH(
            x=0,
            y=0,
            width=data.WINDOW_WIDTH,
            height=data.WINDOW_HEIGHT,
            anchor=arcade.Vec2(0, 0),
        )
        arcade.draw_sprite_rect(data.editor_border, rect)

    def draw_frame_background(self) -> None:
        """Renders the editor grid background."""
        rect = arcade.XYWH(
            x=0,
            y=0,
            width=data.WINDOW_WIDTH,
            height=(((data.WINDOW_HEIGHT + 32) // 64) * 64),
            anchor=arcade.Vec2(0, 0),
        )
        arcade.draw_texture_rect(data.background_grid_texture, rect)

    def draw_debug_text(self) -> None:
        """Renders performance metrics and current level information."""
        debug_list = [
            f"Level Editor {self.level.id}",
            f"Camera: {self.camera_position}",
            f"FPS: {self.fps} / {round(self.delta_time*100000)/100} ms / {self.frame_count}",
            f"Objects: {len(self.level.chip.gates.keys())}g/{len(self.level.chip.paths.keys())}p",
        ]

        start_y = data.WINDOW_HEIGHT - 70

        for index, item in enumerate(debug_list):
            arcade.draw_text(
                item,
                64,
                start_y - (index * 25),
                arcade.color.WHITE,
                14,
                font_name="Press Start 2P",
            )

    def on_draw(self) -> None:
        """Renders the active circuit and UI overlay."""
        self.clear()

        self.draw_frame_background()

        for p in self.level.chip.paths.values():
            p.draw()

        for g in self.level.chip.gates.values():
            g.draw()

        if self.current_path:
            self.current_path.draw()

        if self.selected_follower:
            self.selected_follower.draw()

        self.draw_debug_text()
        self.draw_frame_border()
        self.draw_bottom_gates()

        self.frame_count += 1
        self.delta_time = time.time() - self.last_time
        self.last_time = time.time()

    def on_update(self, delta_time: float) -> None:
        """
        Updates simulation state and timing metrics.

        Args:
            delta_time: Time elapsed since the previous update.
        """
        self.fps = 1 / self.delta_time * 10000 // 10000
        self.simulate()

    def save_frame(self) -> None:
        """Opens the save dialogue window."""
        data.window.display(SaveFrame(self.level))

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """
        Processes keyboard inputs for editor commands.

        Args:
            key: The numeric code of the pressed key.
            key_modifiers: Bitwise flags for modifier keys.
        """
        if key == 101:
            for g in self.level.chip.gates.values():
                if g.entity.touched and g.type == "Input":
                    g.switch()

        if key == 97:
            data.window.back()
        if key == 116:
            self.level.get_truth_table()
        if key == data.keys.back:
            if self.current_path:
                self.current_path.abort()
            self.current_path = None
            self.selected_follower = None

        if key == 115:
            self.save_frame()

        if key == 65288:
            self.delete()

    def delete_gate(self, id: str) -> None:
        """
        Removes a gate and prunes all orphaned paths.

        Args:
            id: The unique identifier of the gate to remove.
        """
        to_delete = []
        for index in self.level.chip.paths.keys():
            p = self.level.chip.paths[index]

            for input in p.inputs:
                if input[1] == id:
                    p.remove_branch(input[4])
                    if p.empty:
                        to_delete.append(index)
                        continue
                    p.clean_out_single_branch()

            for output in p.outputs:
                if output[1] == id:
                    p.remove_branch(output[4])
                    if p.empty:
                        to_delete.append(index)
                        continue
                    p.clean_out_single_branch()

        del self.level.chip.gates[id]
        for i in to_delete:
            del self.level.chip.paths[i]

    def delete(self) -> None:
        """Initiates deletion of the object currently under the cursor."""
        for g in self.level.chip.gates.values():
            if g.entity.touched:
                self.delete_gate(g.id)
                break

        for p in self.level.chip.paths.values():
            if p.touched:
                p.remove_branch(p.get_touched_branch)
                if p.empty:
                    del self.level.chip.paths[p.id]
                    break
                p.clean_out_single_branch()
                break

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """Handles key release events."""
        pass

    @property
    def camera(self) -> Tuple[int, int]:
        """Returns the current camera offset."""
        return self.camera_position

    @camera.setter
    def camera(self, value: Tuple[int, int]) -> None:
        """
        Sets the camera position and aligns it to the grid.

        Args:
            value: The target coordinate to align the camera.
        """
        self._real_camera_position = value
        self.camera_position = (
            (self._real_camera_position[0] // data.UI_EDITOR_GRID_SIZE)
            * data.UI_EDITOR_GRID_SIZE,
            (self._real_camera_position[1] // data.UI_EDITOR_GRID_SIZE)
            * data.UI_EDITOR_GRID_SIZE,
        )
        for g in self.level.chip.gates:
            self.level.chip.gates[g].camera_moving(self.camera_position)
        for p in self.level.chip.paths:
            self.level.chip.paths[p].camera = self.camera_position
        if self.current_path:
            self.current_path.camera = self.camera_position

    def on_mouse_motion(self, x: int, y: int, delta_x: int, delta_y: int) -> None:
        """
        Handles mouse interaction updates, including dragging and movement.

        Args:
            x: Mouse horizontal position.
            y: Mouse vertical position.
            delta_x: Horizontal change.
            delta_y: Vertical change.
        """
        mouse.position = (x, y)

        self.follower.x = mouse.cursor[0] - data.UI_EDITOR_GRID_SIZE / 2
        self.follower.y = mouse.cursor[1] - data.UI_EDITOR_GRID_SIZE / 2

        if self.camera_hold:
            self.camera = (
                self._real_camera_position[0] + delta_x,
                self._real_camera_position[1] + delta_y,
            )

        if self.selected_follower:
            self.selected_follower._camera = (0, 0)
            self.selected_follower.x = mouse.cursor[0] - data.UI_EDITOR_GRID_SIZE / 2
            self.selected_follower.y = mouse.cursor[1] - data.UI_EDITOR_GRID_SIZE / 2

        if self.moving_gate:
            self.moving_gate.x = mouse.cursor[0] - self.moving_gate_offset[0]
            self.moving_gate.y = mouse.cursor[1] - self.moving_gate_offset[1]

            for path in self.level.chip.paths.values():
                connected_inputs, connected_outputs = path.get_connected_points(
                    self.moving_gate.id
                )
                modified = False

                for i in connected_inputs:
                    modified = True
                    position = self.moving_gate.outputs_position[i[2]]
                    position = (
                        position[0] - self.camera_position[0],
                        position[1] - self.camera_position[1],
                    )
                    if i[3] == 1:
                        path.branch_points[i[4]][0] = position
                    elif i[3] == 2:
                        path.branch_points[i[4]][-1] = position

                for i in connected_outputs:
                    modified = True
                    position = self.moving_gate.inputs_position[i[2]]
                    position = (
                        position[0] - self.camera_position[0],
                        position[1] - self.camera_position[1],
                    )
                    if i[3] == 1:
                        path.branch_points[i[4]][0] = position
                    elif i[3] == 2:
                        path.branch_points[i[4]][-1] = position

                if modified:
                    path.recalculate_hitbox()

    def simulate(self) -> None:
        """Executes the circuit logic propagation."""
        self.engine.propagate_values(self.level.chip)

    def on_mouse_press(self, x: int, y: int, button: int, key_modifiers: int) -> None:
        """
        Handles mouse interaction triggers for path building and component placement.
        """
        if button == 2:
            self.camera_hold = True
            return
        if self.camera_hold:
            return

        for g in self.level.chip.gates.values():
            touched = g.touched
            if touched:
                if self.current_path is None:
                    pid = random_id()
                    self.current_path = Path(pid)
                    self.current_path.camera = self.camera
                    self.current_path.add_path()

                    if touched[0] == 1:
                        self.current_path.outputs.append(
                            [
                                1,
                                g.id,
                                touched[1],
                                1,
                                self.current_path.current_branch_count,
                            ]
                        )
                    else:
                        self.current_path.inputs.append(
                            [
                                2,
                                g.id,
                                touched[1],
                                1,
                                self.current_path.current_branch_count,
                            ]
                        )
                    return
                else:
                    if touched[0] == 1:
                        self.current_path.outputs.append(
                            [
                                1,
                                g.id,
                                touched[1],
                                2,
                                self.current_path.current_branch_count,
                            ]
                        )
                    else:
                        self.current_path.inputs.append(
                            [
                                2,
                                g.id,
                                touched[1],
                                2,
                                self.current_path.current_branch_count,
                            ]
                        )
                    self.current_path.camera = self.camera
                    self.current_path.finish()
                    if self.current_path.id not in self.level.chip.paths:
                        self.level.chip.paths[self.current_path.id] = self.current_path

                    self.current_path = None
                    return

        if not self.current_path:
            for p in self.level.chip.paths.values():
                if p.touched:
                    p.add_path()
                    self.current_path = p
                    return
        else:
            for p in self.level.chip.paths.values():
                if p.touched and p != self.current_path:
                    self.current_path.add_path()
                    p.merge(self.current_path)

                    if self.current_path.id in self.level.chip.paths:
                        del self.level.chip.paths[self.current_path.id]

                    self.current_path = None
                    return

                self.current_path.add_path()
                return

        if self.moving_gate is None:
            for g in self.level.chip.gates.values():
                if g.entity.touched:
                    self.moving_gate_offset = (
                        mouse.cursor[0] - g.x,
                        mouse.cursor[1] - g.y,
                    )
                    self.moving_gate = g
                    return

        if self.selected_follower is None:
            hovered = self.get_hovered_bottom_gate()
            if hovered in gate_types:
                self.selected_follower = gate_types[hovered](random_id())
                self.selected_follower.camera = self.camera
                self.selected_follower.x = (
                    mouse.cursor[0]
                    - data.UI_EDITOR_GRID_SIZE / 2
                    - self.camera_position[0]
                )
                self.selected_follower.y = (
                    mouse.cursor[1]
                    - data.UI_EDITOR_GRID_SIZE / 2
                    - self.camera_position[1]
                )

    def on_mouse_release(self, x: int, y: int, button: int, key_modifiers: int) -> None:
        """Finalizes camera drag or gate placement operations."""
        if button == 2:
            self.camera_hold = False
            for g in self.level.chip.gates:
                self.level.chip.gates[g].camera = self.camera_position
        else:
            if self.selected_follower is not None:
                if self.bottom_zone_collider.touched:
                    self.selected_follower = None
                else:
                    self.level.chip.gates[self.selected_follower.id] = (
                        self.selected_follower
                    )
                    self.selected_follower.camera = self.camera
                    self.selected_follower.x = (
                        mouse.cursor[0]
                        - data.UI_EDITOR_GRID_SIZE / 2
                        - self.camera_position[0]
                    )
                    self.selected_follower.y = (
                        mouse.cursor[1]
                        - data.UI_EDITOR_GRID_SIZE / 2
                        - self.camera_position[1]
                    )
                    self.selected_follower = None

        self.moving_gate = None
        self.moving_gate_offset = (0, 0)
