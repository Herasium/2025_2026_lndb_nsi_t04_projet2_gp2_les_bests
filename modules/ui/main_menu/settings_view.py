import arcade
from typing import Any

from modules.ui.mouse import mouse
from modules.ui.toolbox.button import Button
from modules.data import data


class SettingView(arcade.View):
    """Manages the settings menu interface, including UI layout and user interaction."""

    def __init__(self) -> None:
        """Initializes the view, configures UI component positioning, and sets visual assets."""
        super().__init__()

        self.background_color: arcade.Color = arcade.color.JET
        self.name_banner_sprite: Any = data.name_banner

        self.back_button: Button = Button()
        self.back_button.x = 192 / 2.5 - 30
        self.back_button.y = 1010 + 10
        self.back_button.width = 80
        self.back_button.height = 40

        self.settings1_button: Button = Button()
        self.settings1_button.x = 600
        self.settings1_button.y = 350
        self.settings1_button.width = 200
        self.settings1_button.height = 100

        self.settings2_button: Button = Button()
        self.settings2_button.x = 1200
        self.settings2_button.y = 350
        self.settings2_button.width = 200
        self.settings2_button.height = 100

        self.settings3_button: Button = Button()
        self.settings3_button.x = 600
        self.settings3_button.y = 650
        self.settings3_button.width = 200
        self.settings3_button.height = 100

        self.settings4_button: Button = Button()
        self.settings4_button.x = 1200
        self.settings4_button.y = 650
        self.settings4_button.width = 200
        self.settings4_button.height = 100

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Processes keyboard input.

        Args:
            key: The numeric code of the key pressed.
            key_modifiers: Bitwise flags for held modifier keys.
        """
        if key == 97:
            arcade.exit()

    def draw_tile(self, id: int, x: float, y: float) -> None:
        """Renders a specific UI texture segment at the provided coordinates.

        Args:
            id: The index corresponding to the texture in the data set.
            x: Horizontal screen position.
            y: Vertical screen position.
        """
        rect: arcade.XYWH = arcade.XYWH(
            x=x, y=y, width=64, height=64, anchor=arcade.Vec2(0, 0)
        )

        arcade.draw_texture_rect(data.ui_border_tiles[id], rect)

    def draw_frame_border(self) -> None:
        """Assembles the UI frame boundary using grid-based tile placement."""
        start_x: int = 32
        start_y: int = 865
        y_len: int = 13
        x_len: int = 28

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
        """Populates the interior of the frame with background tiles."""
        start_x: int = 32
        start_y: int = 865 + 64
        y_len: int = 15

        for i in range(y_len - 1):
            for a in range(29):
                self.draw_tile(9, start_x + (a) * 64, start_y - (i + 1) * 64)

    def on_draw(self) -> None:
        """Renders the complete view stack."""
        self.clear(arcade.color.BLACK)

        self.draw_frame_background()
        self.draw_frame_border()

        self.back_button.draw()
        self.settings1_button.draw()
        self.settings2_button.draw()
        self.settings3_button.draw()
        self.settings4_button.draw()

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """Synchronizes global mouse state with current cursor position.

        Args:
            x: Current horizontal cursor position.
            y: Current vertical cursor position.
            delta_x: Horizontal movement relative to last frame.
            delta_y: Vertical movement relative to last frame.
        """
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Processes mouse click input to trigger navigation or action events.

        Args:
            x: Horizontal cursor position at click.
            y: Vertical cursor position at click.
            button: The specific button triggered.
            key_modifiers: Bitwise flags for held modifier keys.
        """
        if self.back_button.touched:
            data.window.back()
