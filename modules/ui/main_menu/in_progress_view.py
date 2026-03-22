import arcade
import colorsys
from typing import List, Dict, Tuple, Any, Optional

from modules.ui.mouse import mouse
from modules.ui.toolbox.button import Button
from modules.ui.editor.selector import EditorChipSelector
from modules.ui.level_list.view import LevelList
from modules.ui.level_editor.selector import LevelEditorSelector
from modules.ui.debug_display_all_tiles.view import DebugTilesView
from modules.ui.main_menu.settings_view import SettingView
from modules.ui.main_menu.tutorial_view import TutorialView
from modules.ui.saves_list.view import ChipList
from modules.data.nodes.path import Path
from modules.data import data
from modules.logger import Logger

logger: Logger = Logger("MainMenu")


class MainMenuView(arcade.View):
    """Manages the main menu interface, including UI rendering and navigation."""

    def __init__(self, pause=False) -> None:
        """Initializes the view, UI elements, and navigation state."""
        super().__init__()

        self.background_color: arcade.types.Color = arcade.color.JET
        self.pause = pause

        if self.pause:
            self.play_button_sprite = data.button_resume
        else:
            self.play_button_sprite = data.play_button
        self.name_banner_sprite = data.name_banner
        self.quit_button_sprite = data.button_quit
        self.level_button_sprite = data.button_level
        self.setting_button_sprite = data.button_options
        self.sandbox_button_sprite = data.button_sandbox
        self.tuto_button_sprite = data.button_tuto

        self.play_button: Button = Button()
        self.play_button.x = 1920 / 2 - 700 / 2 - 5
        self.play_button.y = 260 + 320 + 100 + 225 / 2
        self.play_button.width = 700
        self.play_button.height = 225

        self.quit_button: Button = Button()
        self.quit_button.x = 1920 - 350
        self.quit_button.y = 260 + 125
        self.quit_button.width = 175
        self.quit_button.height = 175

        self.setting_button: Button = Button()
        self.setting_button.x = 1920 / 7
        self.setting_button.y = 260 + 180
        self.setting_button.width = 200 * 1.5
        self.setting_button.height = 100 * 1.5

        self.sandbox_button: Button = Button()
        self.sandbox_button.x = 1920 - 830
        self.sandbox_button.y = 260 + 168
        self.sandbox_button.width = 160 * 1.5
        self.sandbox_button.height = 100 * 1.5

        self.level_button: Button = Button()
        self.level_button.x = 1920 / 2 - 200
        self.level_button.y = 260 + 250
        self.level_button.width = 180 * 1.25
        self.level_button.height = 100 * 1.25

        self.tuto_button: Button = Button()
        self.tuto_button.x = 1920 / 3 + 60
        self.tuto_button.y = 260
        self.tuto_button.width = 200 * 1.25
        self.tuto_button.height = 100 * 1.25

        self.button_touche: List[str] = [""]
        self.combinaison: List[str] = [
            "level_button",
            "sandbox_button",
            "tuto_button",
            "setting_button",
        ]
        self.compteur: float = 0

        self.paths: List[Path] = []
        self.add_paths()

    def rainbow_color(self, precision: int, index: int) -> str:
        """Calculates a hex color based on a cycling HSV value.

        Args:
            precision: The frequency of the color transition.
            index: The current animation step.

        Returns:
            The resulting hex string.
        """
        h: float = (index % precision) / precision
        r, g, b = colorsys.hsv_to_rgb(h, 1.0, 1.0)
        return "#{:02x}{:02x}{:02x}".format(int(r * 255), int(g * 255), int(b * 255))

    def add_paths(self) -> None:
        """Initializes and registers path structures for menu background visuals."""
        branches: List[Dict[int, List[Tuple[int, int]]]] = [
            {0: [(945, 702), (594, 702), (594, 837), (270, 837), (270, 891)], 1: []},
            {
                0: [
                    (945, 702),
                    (945, 648),
                    (540, 648),
                    (540, 540),
                    (243, 540),
                    (243, 648),
                    (81, 648),
                ],
                1: [],
            },
            {
                0: [
                    (945, 702),
                    (945, 459),
                    (675, 459),
                    (675, 351),
                    (189, 351),
                    (189, 270),
                    (81, 270),
                ],
                1: [],
            },
            {
                0: [
                    (945, 702),
                    (945, 351),
                    (729, 351),
                    (729, 216),
                    (297, 216),
                    (297, 81),
                ],
                1: [],
            },
            {
                0: [
                    (945, 702),
                    (972, 675),
                    (972, 648),
                    (1161, 648),
                    (1161, 351),
                    (1026, 351),
                    (1026, 189),
                    (918, 189),
                    (918, 81),
                ],
                1: [],
            },
            {
                0: [
                    (945, 702),
                    (1188, 702),
                    (1188, 297),
                    (1350, 297),
                    (1350, 135),
                    (1512, 135),
                    (1512, 81),
                ],
                1: [],
            },
            {
                0: [
                    (945, 702),
                    (1269, 702),
                    (1269, 351),
                    (1674, 351),
                    (1674, 297),
                    (1836, 297),
                ],
                1: [],
            },
            {0: [(945, 702), (1377, 702), (1377, 729), (1836, 729)], 1: []},
            {0: [(945, 702), (1026, 729), (1296, 729), (1296, 891)], 1: []},
        ]

        for branch in branches:
            self.paths.append(Path(""))
            self.paths[-1].do_points = False
            self.paths[-1].branch_points = branch

    def draw_paths(self) -> None:
        """Renders all initialized path visuals."""
        for path in self.paths:
            path.draw()

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Processes keyboard input for menu controls.

        Args:
            key: The numeric key code.
            key_modifiers: Bitmask of modifier keys.
        """
        if key == 65473:  # Emergency exit: F4
            arcade.exit()

    def draw_tile(self, id: int, x: int, y: int) -> None:
        """Renders a single UI border tile from the data registry.

        Args:
            id: The index of the tile texture.
            x: The horizontal screen coordinate.
            y: The vertical screen coordinate.
        """
        rect = arcade.XYWH(x=x, y=y, width=64, height=64, anchor=arcade.Vec2(0, 0))
        arcade.draw_texture_rect(data.ui_border_tiles[id], rect)

    def draw_frame_border(self) -> None:
        """Constructs the UI border using repetitive tile rendering."""
        start_x, start_y = 32, 865
        y_len, x_len = 13, 28

        self.draw_tile(0, start_x, start_y)
        for i in range(x_len - 1):
            self.draw_tile(1, start_x + (i + 1) * 64, start_y)
        self.draw_tile(3, start_x + x_len * 64, start_y)

        for i in range(y_len - 1):
            self.draw_tile(4, start_x, start_y - (i + 1) * 64)
            self.draw_tile(7, start_x + x_len * 64, start_y - (i + 1) * 64)

        self.draw_tile(12, start_x, start_y - y_len * 64)
        self.draw_tile(13, start_x + 64, start_y - y_len * 64)
        self.draw_tile(5, start_x + 2 * 64, start_y - y_len * 64)
        self.draw_tile(6, start_x + 3 * 64, start_y - y_len * 64)
        self.draw_tile(10, start_x + 4 * 64, start_y - y_len * 64)
        for i in range(x_len - 5):
            self.draw_tile(13, start_x + (i + 5) * 64, start_y - y_len * 64)
        self.draw_tile(15, start_x + x_len * 64, start_y - y_len * 64)

    def draw_frame_background(self) -> None:
        """Fills the internal menu background area."""
        start_x, start_y = 32, 865 + 64
        y_len = 15
        for i in range(y_len - 1):
            for a in range(29):
                self.draw_tile(9, start_x + (a) * 64, start_y - (i + 1) * 64)

    def on_draw(self) -> None:
        """Rendering pass for the menu scene."""
        self.clear(arcade.color.BLACK)
        self.draw_frame_background()
        self.draw_paths()

        self.compteur += 1

        rect = arcade.XYWH(
            x=1920 / 2,
            y=260 + 320 + 100,
            width=768,
            height=768,
            anchor=arcade.Vec2(0.5, 0.5),
        )
        arcade.draw_sprite_rect(self.play_button_sprite, rect)

        rect = arcade.XYWH(
            x=0, y=1080 - 128, width=1920, height=128, anchor=arcade.Vec2(0, 0)
        )
        arcade.draw_sprite_rect(self.name_banner_sprite, rect)

        arcade.draw_sprite_rect(
            self.quit_button_sprite,
            arcade.XYWH(1920 - 350, 260 + 125, 175, 175, arcade.Vec2(0, 1)),
        )
        arcade.draw_sprite_rect(
            self.setting_button_sprite,
            arcade.XYWH(1920 / 7, 260 + 180, 200 * 1.5, 100 * 1.5, arcade.Vec2(0, 1)),
        )
        arcade.draw_sprite_rect(
            self.sandbox_button_sprite,
            arcade.XYWH(1920 - 830, 260 + 168, 160 * 1.5, 100 * 1.5, arcade.Vec2(0, 1)),
        )
        arcade.draw_sprite_rect(
            self.level_button_sprite,
            arcade.XYWH(
                1920 / 2 - 200, 260 + 250, 180 * 1.25, 100 * 1.25, arcade.Vec2(0, 1)
            ),
        )
        arcade.draw_sprite_rect(
            self.tuto_button_sprite,
            arcade.XYWH(1920 / 3 + 60, 260, 200 * 1.25, 100 * 1.25, arcade.Vec2(0, 1)),
        )

        if self.button_touche == self.combinaison:
            color_val = round(self.compteur)
            for i in self.paths:
                i.input_on_color = arcade.types.Color.from_hex_string(
                    self.rainbow_color(100, color_val)
                )
                i.current_value = True

        self.quit_button.draw()
        self.play_button.draw()
        self.setting_button.draw()
        self.level_button.draw()
        self.sandbox_button.draw()
        self.tuto_button.draw()
        self.draw_frame_border()

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """Handles mouse tracking, UI hover states, and easter egg progression.

        Args:
            x: Current cursor X coordinate.
            y: Current cursor Y coordinate.
            delta_x: Horizontal mouse displacement.
            delta_y: Vertical mouse displacement.
        """
        mouse.position = (x, y)

        if self.play_button.touched:
            if self.button_touche[-1] != "play_button":
                self.button_touche.append("play_button")
            for i in self.paths:
                i.input_on_color = arcade.color.MINT_GREEN
                i.current_value = True
        elif self.tuto_button.touched:
            if self.button_touche[-1] != "tuto_button":
                self.button_touche.append("tuto_button")
            for i in self.paths:
                i.input_on_color = arcade.color.UNIVERSITY_OF_TENNESSEE_ORANGE
                i.current_value = True
        elif self.setting_button.touched and not self.button_touche == self.combinaison:
            if self.button_touche[-1] != "setting_button":
                self.button_touche.append("setting_button")
            for i in self.paths:
                i.input_on_color = arcade.color.SONIC_SILVER
                i.current_value = True
        elif self.sandbox_button.touched:
            if self.button_touche[-1] != "sandbox_button":
                self.button_touche.append("sandbox_button")
            for i in self.paths:
                i.input_on_color = arcade.color.SPIRO_DISCO_BALL
                i.current_value = True
        elif self.level_button.touched:
            if self.button_touche[-1] != "level_button":
                self.button_touche.append("level_button")
            for i in self.paths:
                i.input_on_color = arcade.color.ROSSO_CORSA
                i.current_value = True
        elif self.quit_button.touched:
            if self.button_touche[-1] != "quit_button":
                self.button_touche.append("quit_button")
            for i in self.paths:
                i.input_on_color = arcade.color.RUDDY
                i.current_value = True
        else:
            if self.button_touche != self.combinaison:
                for i in self.paths:
                    i.current_value = False

        if len(self.button_touche) > 4:
            self.button_touche.pop(0)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Handles interaction events for menu navigation.

        Args:
            x: X coordinate of the click.
            y: Y coordinate of the click.
            button: The mouse button pressed.
            key_modifiers: Active keyboard modifiers.
        """
        to_display: Optional[Any] = None

        if self.level_button.touched:
            to_display = LevelEditorSelector if key_modifiers in [17, 1] else LevelList
        elif self.sandbox_button.touched:
            to_display = ChipList
        elif self.play_button.touched:
            if self.pause:
                data.window.back()
            else:
                to_display = (
                    DebugTilesView if key_modifiers in [17, 1] else EditorChipSelector
                )
        elif self.quit_button.touched:
            logger.success("Bye Bye ! <3")
            arcade.exit()
        elif self.setting_button.touched:
            to_display = SettingView
        elif self.tuto_button.touched:
            to_display = TutorialView

        if to_display is not None:
            try:
                data.window.display(to_display())
                logger.success(f"Launching {to_display.__name__}")
            except Exception as e:
                logger.error(f"Failed to launch {to_display.__name__} : {e}")
                data.window.display(self)
