import arcade
import time
from typing import Optional, List, Tuple, Any, Dict

from modules.ui.mouse import mouse
from modules.ui.toolbox.entity import Entity
from modules.ui.toolbox.id_generator import random_id
from modules.ui.toolbox.easing import BackEaseOut, ElasticEaseOut
from modules.ui.toolbox.text import Text

from modules.data.nodes.path import Path

from modules.data.custom import CustomGate

from modules.data import data
from modules.data.gate_index import gate_types

from modules.logger import Logger

from modules.engine import Engine

logger: Logger = Logger("LevelPlayer")


class LevelPlayer(arcade.View):
    """Manages the interactive game level view, including UI rendering,
    user-driven editing, and logic gate simulation.
    """

    def __init__(self, id: Optional[str] = None) -> None:
        """Initializes the LevelPlayer view and loads level configuration.

        Args:
            id: Identifier of the level.
        """
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

        if id is None:
            logger.error("No level id provided, going back.")
            data.window.back()
            arcade.quit()
        else:
            if id in data.loaded_levels:
                self.level = data.loaded_levels[id]
                self.level.play_mode()
            else:
                logger.error("Invalid level id provided, going back.")
                data.window.back()
                arcade.quit()

        self.moving_gate_offset: Tuple[int, int] = (0, 0)
        self._real_camera_position: Tuple[int, int] = (0, 0)
        self.camera_position: Tuple[int, int] = (0, 0)
        self.bottom_camera_position: List[int] = [0, 0]

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

        self.display_hint_frame: bool = True
        self.current_hint_frame: int = 0

        if self.stress_test:
            self.perf_graph_list = arcade.SpriteList()
            graph = arcade.PerfGraph(400, 400, graph_data="FPS")
            graph.position = 200, 200
            self.perf_graph_list.append(graph)

        self.prepare_right_frame()
        self.prepare_won_frame()
        self.prepare_hint_frame()

    def reload_hint(self):
        self.hint_frame_text.text = self.level.hints[self.current_hint_frame]

    def prepare_hint_frame(self) -> None:
        """Initializes UI elements for the hints screen. (Level Instructions.)"""

        self.hint_frame = Entity(
            x=384, y=220, width=576 * 2, height=320 * 2, sprite=data.level_player_empty
        )
        self.hint_frame_text = Text(
            x=data.WINDOW_WIDTH / 2,
            y=data.WINDOW_HEIGHT / 2,
            width=1000,
            height=300,
            text="",
            multiline=True,
        )
        self.hint_frame_ok = Entity(
            x=384 + 576 * 2 - 137 * 1.2 - 90,
            y=310,
            width=137 * 1.2,
            height=120,
            sprite=data.button_ok,
        )
        self.hint_frame_next = Entity(
            x=384 + 576 * 2 - 169 * 1.2 - 90,
            y=310,
            width=169 * 1.2,
            height=120,
            sprite=data.button_next_on,
        )
        self.hint_frame_back = Entity(
            x=384 + 90, y=310, width=160 * 1.2, height=120, sprite=data.button_back
        )

        if (len(self.level.hints) - 1) < 1:
            self.display_hint_frame = False
            return

        self.hint_frame_text.text = self.level.hints[0]

    def prepare_won_frame(self) -> None:
        """Initializes UI elements for the victory screen."""
        self.win_frame_ease = BackEaseOut(-500, 220, 90)
        self.win_frame = Entity(
            x=384, y=-500, width=576 * 2, height=320 * 2, sprite=data.level_player_win
        )

        self.win_text_level_num = arcade.Text(
            f"Level {self.level.number}",
            512,
            580,
            arcade.color.WHITE,
            20,
            font_name="Press Start 2P",
        )
        self.win_text_level_name = arcade.Text(
            f"{self.level.name}",
            512,
            540,
            arcade.color.WHITE,
            20,
            font_name="Press Start 2P",
        )

        self.win_button_next = Entity(
            x=990, y=348, width=432, height=256, sprite=data.button_next_on
        )

        self.win_stars: List[Entity] = []
        self.win_stars_ease: List[ElasticEaseOut] = []

        for i in range(3):
            sprite = data.star
            if i > self.level.get_stars_count() - 1:
                sprite = data.star_empty
            self.win_stars.append(
                Entity(
                    x=535 + i * 135 + 54,
                    y=410 + 54,
                    width=108,
                    height=108,
                    sprite=sprite,
                    anchor=arcade.Vec2(0.5, 0.5),
                )
            )
            self.win_stars_ease.append(
                ElasticEaseOut(-20 + i * -20, end=108, duration=128 + i * 20)
            )

    def prepare_right_frame_basic(self) -> None:
        """Constructs the right-hand sidebar UI, including the truth table rendering."""
        self.check_button = Entity(
            x=1402, y=57, width=216, height=128, sprite=data.button_check
        )
        self.truth_table = Entity(
            x=1402,
            y=data.WINDOW_HEIGHT - 383,
            width=448,
            height=64,
            sprite=data.truth_table,
        )
        self.button_next_off = Entity(
            x=1634, y=57, width=216, height=128, sprite=data.button_next_off
        )
        self.level_info = Entity(
            x=1402,
            y=data.WINDOW_HEIGHT - 127,
            width=448,
            height=64,
            sprite=data.level_info,
        )

        self.level_name_text = arcade.Text(
            f"Level {self.level.number} : {self.level.name}",
            1408,
            900,
            arcade.color.WHITE,
            12,
            font_name="Press Start 2P",
        )

        self.level_desc_text: List[arcade.Text] = []
        texts: List[str] = self.level.description.split(" ")
        c: int = 0

        # Perform basic greedy word wrap
        for _ in range(len(texts)):
            if c > len(texts) - 2:
                break
            if len(texts[c] + texts[c + 1]) + 1 <= 24:
                b = texts.pop(c + 1)
                texts[c] += " " + b
            else:
                c += 1

        for i in range(len(texts)):
            self.level_desc_text.append(
                arcade.Text(
                    texts[i],
                    1408,
                    850 - 25 * i,
                    arcade.color.WHITE,
                    10,
                    font_name="Press Start 2P",
                )
            )

    def prepare_right_frame(self) -> None:
        self.prepare_right_frame_basic()
        if self.level.is_complex:
            self.prepare_right_frame_complex()
        else:
            self.prepare_right_frame_simple()

    def prepare_right_frame_complex(self) -> None:
        self.truth_inputs = arcade.Text(
            "Input(s)",
            1626,
            data.WINDOW_HEIGHT - (447),
            arcade.color.WHITE,
            18,
            font_name="Press Start 2P",
            anchor_x="center",
        )
        result = ""

        for i in self.level.compare_fail["in"]:
            result += f"{i} "

        self.truth_inputs_values = arcade.Text(
            result,
            1626,
            data.WINDOW_HEIGHT - (497),
            arcade.color.WHITE,
            16,
            font_name="Press Start 2P",
            anchor_x="center",
        )

        self.truth_targets = arcade.Text(
            "Target(s)",
            1626,
            data.WINDOW_HEIGHT - (547),
            arcade.color.WHITE,
            18,
            font_name="Press Start 2P",
            anchor_x="center",
        )

        result = ""

        for i in self.level.compare_fail["target"]:
            result += f"{i} "

        self.truth_targets_values = arcade.Text(
            result,
            1626,
            data.WINDOW_HEIGHT - (597),
            arcade.color.WHITE,
            16,
            font_name="Press Start 2P",
            anchor_x="center",
        )

        self.truth_outputs = arcade.Text(
            "Output(s)",
            1626,
            data.WINDOW_HEIGHT - (647),
            arcade.color.WHITE,
            18,
            font_name="Press Start 2P",
            anchor_x="center",
        )

        result = ""

        for i in self.level.compare_fail["out"]:
            result += f"{i} "

        self.truth_outputs_values = arcade.Text(
            result,
            1626,
            data.WINDOW_HEIGHT - (697),
            arcade.color.WHITE,
            16,
            font_name="Press Start 2P",
            anchor_x="center",
        )

    def prepare_right_frame_simple(self) -> None:

        table = self.level.truth[self.level.answer.id]
        chip_truth: Optional[Dict] = None

        if self.level.chip.id in self.level.truth:
            chip_truth = self.level.truth[self.level.chip.id]

        self.truth_table_inputs: List[List[arcade.Text]] = [
            [] for _ in range(len(table["meta"]["inputs"]))
        ]
        self.truth_table_outputs: List[List[arcade.Text]] = [
            [] for _ in range(len(table["meta"]["outputs"]))
        ]
        self.line_set: List[List[Tuple[Tuple[float, float], Tuple[float, float]]]] = []
        self.truth_table_titles: List[arcade.Text] = []

        add_y = 28
        add_x = 27
        total_len = (len(table["data"][0]) * 2 + table["meta"]["size"] + 4) * add_x
        start_x = (
            1402
            + (7 * 32)
            - ((len(table["data"][0]) * 2 + table["meta"]["size"] + 4) / 2 * add_x)
        )
        start_y = data.WINDOW_HEIGHT - (447)

        offset_x = 0
        offset_y = 0

        self.line_set.append(
            [
                (start_x - 10, start_y - offset_y + add_y - 4),
                (start_x + total_len + 10, start_y + add_y - offset_y - 4),
            ]
        )
        self.truth_table_titles.append(
            arcade.Text(
                "Inputs",
                start_x + (table["meta"]["size"] / 2) * add_x,
                start_y + add_y + 5,
                arcade.color.WHITE,
                10,
                font_name="Press Start 2P",
                anchor_x="center",
            )
        )
        self.truth_table_titles.append(
            arcade.Text(
                "Target",
                start_x
                + (table["meta"]["size"] + 2 + len(table["data"][0]) / 2) * add_x
                - 5,
                start_y + add_y + 5,
                arcade.color.WHITE,
                9,
                font_name="Press Start 2P",
                anchor_x="center",
            )
        )
        self.truth_table_titles.append(
            arcade.Text(
                "Current",
                start_x
                + (table["meta"]["size"] + 4 + len(table["data"][0]) * 1.5) * add_x,
                start_y + add_y + 5,
                arcade.color.WHITE,
                9,
                font_name="Press Start 2P",
                anchor_x="center",
            )
        )

        if not table["meta"]["complex"]:
            for current in range(table["meta"]["power"]):
                values = [
                    bool(current & (1 << i)) for i in range(table["meta"]["size"])
                ]
                for i in range(len(values)):
                    self.truth_table_inputs[i].append(
                        arcade.Text(
                            str(values[i] * 1),
                            start_x + offset_x,
                            start_y - offset_y,
                            arcade.color.WHITE,
                            14,
                            font_name="Press Start 2P",
                            anchor_x="center",
                        )
                    )
                    offset_x += add_x
                offset_x += add_x * 2
                for i in range(len(table["data"][current])):
                    self.truth_table_outputs[i].append(
                        arcade.Text(
                            str(table["data"][current][i] * 1),
                            start_x + offset_x,
                            start_y - offset_y,
                            arcade.color.WHITE,
                            14,
                            font_name="Press Start 2P",
                            anchor_x="center",
                        )
                    )
                    offset_x += add_x
                offset_x += add_x * 2
                if chip_truth:
                    for i in range(len(chip_truth["data"][current])):
                        color = arcade.color.RED_PURPLE
                        if table["data"][current][i] == chip_truth["data"][current][i]:
                            color = arcade.color.GREEN_YELLOW
                        self.truth_table_outputs[i].append(
                            arcade.Text(
                                str(chip_truth["data"][current][i] * 1),
                                start_x + offset_x,
                                start_y - offset_y,
                                color,
                                14,
                                font_name="Press Start 2P",
                                anchor_x="center",
                            )
                        )
                        offset_x += add_x
                else:
                    for i in range(len(table["data"][current])):
                        self.truth_table_outputs[i].append(
                            arcade.Text(
                                "?",
                                start_x + offset_x,
                                start_y - offset_y,
                                arcade.color.WHITE,
                                14,
                                font_name="Press Start 2P",
                                anchor_x="center",
                            )
                        )
                        offset_x += add_x
                self.line_set.append(
                    [
                        (start_x - 10, start_y - offset_y - 4),
                        (start_x + offset_x + 10, start_y - offset_y - 4),
                    ]
                )
                offset_x = 0
                offset_y += add_y

    def bottom_bar_width_sum(self) -> int:
        """Returns the aggregate width of all gate icons in the bottom toolbar."""
        result: int = 0
        for i in self.bottom_gates:
            result += i.tile_width
        return result

    def bottom_gate_bar(self) -> None:
        """Populates the bottom UI toolbar with available gates based on level constraints."""
        self.bottom_gates = []
        for i in self.level.max_usage:
            if i != "Input" and i != "Output":
                if i in gate_types:
                    position = (
                        self.bottom_bar_width_sum() + len(self.bottom_gates)
                    ) * data.UI_EDITOR_GRID_SIZE + 64
                    self.bottom_gates.append(
                        gate_types[i](f"bottom_gate_{random_id()}")
                    )
                    self.bottom_gates[-1].camera = self.bottom_camera_position
                    self.bottom_gates[-1].y = 3 * data.UI_EDITOR_GRID_SIZE
                    self.bottom_gates[-1].x = position
                elif i in data.loaded_chips:
                    chip = data.loaded_chips[i]
                    position = (
                        self.bottom_bar_width_sum() + len(self.bottom_gates)
                    ) * data.UI_EDITOR_GRID_SIZE + 64
                    self.bottom_gates.append(
                        CustomGate(f"bottom_gate_{random_id()}", chip)
                    )
                    self.bottom_gates[-1].camera = self.bottom_camera_position
                    self.bottom_gates[-1].y = 3 * data.UI_EDITOR_GRID_SIZE
                    self.bottom_gates[-1].x = position

    def get_hovered_bottom_gate(self) -> Optional[str]:
        """Identifies which gate icon in the toolbar is currently being hovered."""
        for i in self.bottom_gates:
            if i.entity.touched:
                if i.type == "Custom":
                    return i.base_chip_id
                return i.gate_type
        return None

    def draw_bottom_gates(self) -> None:
        """Renders the gate icons in the bottom toolbar."""
        for i in self.bottom_gates:
            i.draw()

    def reset(self) -> None:
        """Resets the current level state."""
        pass

    def draw_frame_border(self) -> None:
        """Renders the outer UI window boundary."""
        rect = arcade.XYWH(
            x=0,
            y=0,
            width=data.WINDOW_WIDTH,
            height=data.WINDOW_HEIGHT,
            anchor=arcade.Vec2(0, 0),
        )
        arcade.draw_sprite_rect(data.level_player_border, rect)

    def draw_frame_border_top(self) -> None:
        """Renders the outer UI window boundary top (second layer to prevent clipping)."""
        rect = arcade.XYWH(
            x=0,
            y=0,
            width=data.WINDOW_WIDTH,
            height=data.WINDOW_HEIGHT,
            anchor=arcade.Vec2(0, 0),
        )
        arcade.draw_sprite_rect(data.level_player_border_no_bg, rect)

    def draw_frame_background(self) -> None:
        """Renders the level grid background texture."""
        rect = arcade.XYWH(
            x=0,
            y=0,
            width=data.WINDOW_WIDTH,
            height=(((data.WINDOW_HEIGHT + 32) // 64) * 64),
            anchor=arcade.Vec2(0, 0),
        )
        arcade.draw_texture_rect(data.background_grid_texture, rect)

    def draw_debug_text(self) -> None:
        """Renders engine performance metrics and object counts."""
        debug_list = [
            f"Camera: {self.camera_position}",
            f"FPS: {self.fps} / {round(self.delta_time * 100000) / 100} ms / {self.frame_count}",
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

    def draw_level_time(self) -> None:
        """Renders current elapsed time versus limits and progress markers."""
        debug_list = [
            f"Time Limit: {round(time.time() - self.level.start_time)}s / {self.level.time}s",
            f"Stars: {self.level.get_stars_count()}",
        ]
        start_y = data.WINDOW_HEIGHT - 80
        for index, item in enumerate(debug_list):
            arcade.draw_text(
                item,
                64,
                start_y - (index * 25),
                arcade.color.WHITE,
                14,
                font_name="Press Start 2P",
            )
        arcade.draw_sprite_rect(
            data.star, arcade.rect.XYWH(64 + 8 * 20 + 7, 986, 25, 25)
        )

    def draw_won(self) -> None:
        """Renders the victory modal and animated star icons."""
        if not self.win_frame_ease.done:
            value = self.win_frame_ease.tick()
            self.win_frame.y = value
        self.win_frame.draw()
        if self.win_frame_ease.done:
            self.win_text_level_num.draw()
            self.win_text_level_name.draw()
            for i in range(len(self.win_stars)):
                value = self.win_stars_ease[i].tick()
                star = self.win_stars[i]
                star._width = value
                star.height = value
                star.draw()
            self.win_button_next.draw()

    def draw_right(self) -> None:
        """Renders the sidebar components and calculated truth table."""
        self.check_button.draw()
        self.truth_table.draw()
        self.button_next_off.draw()
        self.level_info.draw()
        self.level_name_text.draw()
        for i in self.level_desc_text:
            i.draw()

        if not self.level.is_complex:
            for i in self.truth_table_inputs:
                for a in i:
                    a.draw()
            for i in self.truth_table_outputs:
                for a in i:
                    a.draw()
            for coords in self.line_set:
                arcade.draw_line(
                    coords[0][0],
                    coords[0][1],
                    coords[1][0],
                    coords[1][1],
                    arcade.color.WHITE,
                    1,
                )
            for i in self.truth_table_titles:
                i.draw()
        else:
            self.truth_inputs.draw()
            self.truth_outputs.draw()
            self.truth_targets.draw()
            self.truth_inputs_values.draw()
            self.truth_targets_values.draw()
            self.truth_outputs_values.draw()

    def draw_hint(self) -> None:
        """Render the hints frame, to provide basic level instructions."""

        if self.display_hint_frame:
            self.hint_frame.draw()
            self.hint_frame_text.draw()

            if self.current_hint_frame == (len(self.level.hints) - 1):
                self.hint_frame_ok.draw()
            if self.current_hint_frame < (len(self.level.hints) - 1):
                self.hint_frame_next.draw()
            if self.current_hint_frame > 0:
                self.hint_frame_back.draw()

    def on_draw(self) -> None:
        """Main rendering loop: updates component visual states and draws layers."""
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

        self.draw_frame_border()
        self.draw_bottom_gates()
        self.draw_frame_border_top()
        self.draw_right()
        self.draw_level_time()
        self.draw_hint()

        if self.level.won:
            self.draw_won()
        if self.stress_test:
            self.perf_graph_list.draw()

        self.frame_count += 1
        self.delta_time = time.time() - self.last_time
        self.last_time = time.time()

    def on_update(self, delta_time: float) -> None:
        """Per-frame update loop for simulation and state tracking."""
        self.fps = 1 / self.delta_time * 10000 // 10000
        self.simulate()

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Handles keyboard shortcuts for interaction, deletion, and navigation."""
        if key == data.keys.input_toggle and not self.level.won:
            for g in self.level.chip.gates.values():
                if g.entity.touched and g.type == "Input":
                    g.switch()
        if key == 65473:  # Emergency exit: F4
            arcade.exit()

        if key == data.keys.back:
            if self.current_path or self.selected_follower:
                if self.current_path:
                    self.current_path.abort()
                self.current_path = None
                self.selected_follower = None
            else:
                data.window.display(data.pause)

        if (
            key == data.keys.gate_delete
            and not self.level.won
            and self.current_path is None
        ):
            self.delete()

    def delete_gate(self, id: str) -> None:
        """Removes specified gate and reconciles affected circuit paths."""
        to_delete: List[str] = []
        if self.level.chip.gates[id].type in ["Gate", "Custom", "Complex"]:
            for index in self.level.chip.paths.keys():
                p = self.level.chip.paths[index]
                for input in p.inputs:
                    if input[1] == id:
                        to_delete.append(index)
   
                for output in p.outputs:
                    if output[1] == id:
                        to_delete.append(index)

            del self.level.chip.gates[id]
            for i in to_delete:
                self.delete_path(i)
            self.level.chip.changed = True

    def delete_path(self,path_id):

        p = self.level.chip.paths[path_id]
        for i in self.level.chip.paths[path_id].outputs:
                    gate_id = i[1]
                    gate_output_id = i[2]    
                    if gate_id in self.level.chip.gates:
                        self.level.chip.gates[gate_id].inputs[gate_output_id] = 0
        del self.level.chip.paths[path_id]

    def delete(self) -> None:
        """Initiates the deletion process for the currently selected object."""
        for g in self.level.chip.gates.values():
            if g.entity.touched:
                self.delete_gate(g.id)
                break

        to_delete = []
        for p in self.level.chip.paths.values():
            if p.touched:
                to_delete.append(p.id)

        for p in to_delete:
            self.delete_path(p)

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """Handles key-up events."""
        pass

    @property
    def camera(self) -> Tuple[int, int]:
        """Provides the current quantized camera position."""
        return self.camera_position

    @camera.setter
    def camera(self, value: Tuple[int, int]) -> None:
        """Updates camera position and recalibrates object offsets."""
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
        """Handles mouse movement for dragging objects and updating circuit layout."""
        mouse.position = (x, y)
        if self.level.won:
            return
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
            # Recalculate wire geometry based on gate movement
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
                    self.level.chip.changed = True
                    path.recalculate_hitbox()

    def simulate(self) -> None:
        """Propagates logic states through the current circuit chip."""
        self.engine.propagate_values(self.level.chip)
        if self.level.chip.changed:
            self.level.chip.changed = False
            self.level.calculate_inventory()
            self.bottom_gate_bar()

    def won(self) -> None:
        """Activates victory-related UI and logic states."""
        self.prepare_won_frame()

    def launch_next_level(self) -> None:
        """Transitions application to the subsequent level in the sequence."""
        levels: List[str] = list(data.loaded_levels.keys())

        def sort_keys(i: str) -> int:
            return data.loaded_levels[i].number

        levels.sort(key=sort_keys)
        current = levels.index(self.level.id)
        if (current + 1) < len(levels):
            data.window.display(LevelPlayer(levels[current + 1]))

    def next_hint(self):
        if self.current_hint_frame < (len(self.level.hints) - 1):
            self.current_hint_frame += 1
        else:
            self.display_hint_frame = False
        self.reload_hint()

    def previous_hint(self):
        if self.current_hint_frame > 0:
            self.current_hint_frame = 0
        self.reload_hint()

    def on_mouse_press(self, x: int, y: int, button: int, key_modifiers: int) -> None:
        """Handles click events for UI navigation, wiring paths, and gate placement."""
        if self.level.won:
            if self.win_button_next.touched:
                self.launch_next_level()
            return

        if self.display_hint_frame:
            if self.hint_frame_ok.touched or self.hint_frame_next.touched:
                self.next_hint()
            if self.hint_frame_back.touched:
                self.previous_hint()
            return

        if button == 2:
            self.camera_hold = True
            return
        if self.camera_hold:
            return
        if self.check_button.touched:
            self.level.get_truth_table()
            self.prepare_right_frame()
            if self.level.check_victory():
                self.won()
            return
        # Wiring logic
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
                    self.level.chip.changed = True
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
                    self.level.chip.changed = True
                    return
        if not self.current_path:
            for p in self.level.chip.paths.values():
                if p.touched:
                    p.add_path()
                    self.current_path = p
                    self.level.chip.changed = True
                    return
        else:
            for p in self.level.chip.paths.values():
                if p.touched and p != self.current_path:
                    self.current_path.add_path()
                    p.merge(self.current_path)
                    if self.current_path.id in self.level.chip.paths:
                        del self.level.chip.paths[self.current_path.id]
                    self.current_path = None
                    self.level.chip.changed = True
                    return
            self.current_path.add_path()
            self.level.chip.changed = True
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
            elif hovered in data.loaded_chips:
                self.selected_follower = CustomGate(
                    random_id(), data.loaded_chips[hovered]
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

    def bottom_bar_update_camera(self) -> None:
        """Syncs the scroll position of bottom bar gates."""
        for gate in self.bottom_gates:
            gate.camera = self.bottom_camera_position

    def on_mouse_scroll(
        self, x: float, y: float, scroll_x: float, scroll_y: float
    ) -> None:
        """Handles scrolling within the bottom bar UI."""
        if self.bottom_zone_collider.touched:
            self.bottom_camera_position[0] += scroll_y * -data.MOUSE_SENSI
            self.bottom_camera_position[0] = min(self.bottom_camera_position[0], 0)
            self.bottom_bar_update_camera()

    def on_mouse_release(self, x: int, y: int, button: int, key_modifiers: int) -> None:
        """Handles mouse button release interactions."""
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
                    self.level.chip.changed = True

        self.moving_gate = None
        self.moving_gate_offset = (0, 0)
