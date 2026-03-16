"""Provides the PauseView class for handling the pause menu interface."""

import arcade
from typing import Any

from modules.ui.mouse import mouse
from modules.ui.toolbox.button import Button
from modules.ui.main_menu.settings_view import SettingView

from modules.data import data


class PauseView(arcade.View):
    """Represents the pause menu interface containing navigation and settings."""

    def __init__(self) -> None:
        """Initializes the view with background colors and UI components."""
        super().__init__()

        self.background_color: arcade.color = arcade.color.JET

        self.ui_border_sheet: Any = data.ui_border_tiles
        self.name_banner_sprite: Any = data.name_banner

        self.back_button: Button = Button()
        self.back_button.x = 700
        self.back_button.y = 800 - 25
        self.back_button.width = 520
        self.back_button.height = 100

        self.settings_button: Button = Button()
        self.settings_button.x = 700
        self.settings_button.y = 575 - 25
        self.settings_button.width = 520
        self.settings_button.height = 100

        self.quitter_button: Button = Button()
        self.quitter_button.x = 700
        self.quitter_button.y = 350 - 25
        self.quitter_button.width = 520
        self.quitter_button.height = 100

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Handles key press events.

        Args:
            key: The identifier of the key pressed.
            key_modifiers: Bitwise combination of active modifier keys.
        """
        if key == 97:
            arcade.exit()

    def draw_tile(self, id: int, x: float, y: float) -> None:
        """Draws a UI tile from the sprite sheet at specified coordinates.

        Args:
            id: Index of the tile within the sprite sheet.
            x: Horizontal position.
            y: Vertical position.
        """
        rect = arcade.XYWH(x=x, y=y, width=64, height=64, anchor=arcade.Vec2(0, 0))
        arcade.draw_texture_rect(self.ui_border_sheet[id], rect)

    def draw_frame_border(self) -> None:
        """Constructs the decorative frame perimeter using UI tiles."""
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
        """Renders the interior grid of the menu frame."""
        start_x: int = 32
        start_y: int = 865 + 64
        y_len: int = 15

        for i in range(y_len - 1):
            for a in range(29):
                self.draw_tile(9, start_x + (a) * 64, start_y - (i + 1) * 64)

    def on_draw(self) -> None:
        """Renders all pause menu UI components to the screen."""
        self.clear(arcade.color.BLACK)

        self.draw_frame_background()
        self.draw_frame_border()

        rect = arcade.XYWH(
            x=0, y=1080 - 128, width=1920, height=128, anchor=arcade.Vec2(0, 0)
        )
        arcade.draw_sprite_rect(self.name_banner_sprite, rect)

        self.back_button.draw()
        self.settings_button.draw()
        self.quitter_button.draw()

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """Synchronizes global mouse tracking with current view coordinates.

        Args:
            x: Current horizontal mouse position.
            y: Current vertical mouse position.
            delta_x: Change in horizontal movement.
            delta_y: Change in vertical movement.
        """
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Processes interaction with menu buttons.

        Args:
            x: Horizontal click position.
            y: Vertical click position.
            button: Mouse button identifier.
            key_modifiers: Bitwise combination of active modifier keys.
        """
        if self.back_button.touched:
            data.window.back()

        if self.settings_button.touched:
            data.window.display(SettingView())

        if self.quitter_button.touched:
            data.window.first()
