import arcade
from typing import Any

from modules.ui.mouse import mouse
from modules.ui.toolbox.button import Button
from modules.ui.main_menu.settings_view import SettingView

from modules.data import data


class PauseView(arcade.View):
    """
    A view representing the pause menu, containing buttons for navigation and settings.
    """

    def __init__(self) -> None:
        """
        Initialize the PauseView, setting up background colors and UI components.
        """
        super().__init__()

        self.background_color: arcade.color = arcade.color.JET

        # Data references for UI assets
        self.ui_border_sheet: Any = data.ui_border_tiles
        self.name_banner_sprite: Any = data.name_banner

        # Initialize and configure navigation buttons
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
        """
        Handle key press events.

        Parameters:
        - key: The key that was pressed.
        - key_modifiers: Bitwise combination of modifiers.
        """
        if key == 97:  # "a" key triggers application exit
            arcade.exit()

    def draw_tile(self, id: int, x: float, y: float) -> None:
        """
        Draw a specific UI tile at the given coordinates.

        Parameters:
        - id: Index of the tile in the ui_border_sheet.
        - x: X coordinate.
        - y: Y coordinate.
        """
        rect = arcade.XYWH(x=x, y=y, width=64, height=64, anchor=arcade.Vec2(0, 0))
        arcade.draw_texture_rect(
            self.ui_border_sheet[id], rect
        )  # Draw the specified tile texture

    def draw_frame_border(self) -> None:
        """
        Draw the decorative border frame for the pause menu using multiple tiles.
        """
        start_x: int = 32
        start_y: int = 865
        y_len: int = 13
        x_len: int = 28

        # Draw top row
        self.draw_tile(0, start_x, start_y)
        for i in range(x_len - 1):
            self.draw_tile(1, start_x + (i + 1) * 64, start_y)
        self.draw_tile(3, start_x + x_len * 64, start_y)

        # Draw vertical sides
        for i in range(y_len - 1):
            self.draw_tile(4, start_x, start_y - (i + 1) * 64)
            self.draw_tile(7, start_x + x_len * 64, start_y - (i + 1) * 64)

        # Draw bottom row
        self.draw_tile(12, start_x, start_y - y_len * 64)
        self.draw_tile(13, start_x + 64, start_y - y_len * 64)
        self.draw_tile(5, start_x + 2 * 64, start_y - y_len * 64)
        self.draw_tile(6, start_x + 3 * 64, start_y - y_len * 64)
        self.draw_tile(10, start_x + 4 * 64, start_y - y_len * 64)
        for i in range(x_len - 5):
            self.draw_tile(13, start_x + (i + 5) * 64, start_y - y_len * 64)
        self.draw_tile(15, start_x + x_len * 64, start_y - y_len * 64)

    def draw_frame_background(self) -> None:
        """
        Fill the interior of the frame with background tiles.
        """
        start_x: int = 32
        start_y: int = 865 + 64
        y_len: int = 15

        # Nested loop to fill the grid area
        for i in range(y_len - 1):
            for a in range(29):
                self.draw_tile(9, start_x + (a) * 64, start_y - (i + 1) * 64)

    def on_draw(self) -> None:
        """
        Render the UI elements to the screen.
        """
        self.clear(arcade.color.BLACK)

        self.draw_frame_background()  # Render background first
        self.draw_frame_border()  # Render border on top

        # Define banner rectangle
        rect = arcade.XYWH(
            x=0, y=1080 - 128, width=1920, height=128, anchor=arcade.Vec2(0, 0)
        )
        arcade.draw_sprite_rect(self.name_banner_sprite, rect)

        # Draw buttons
        self.back_button.draw()
        self.settings_button.draw()
        self.quitter_button.draw()

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """
        Update the global mouse position tracking.
        """
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """
        Handle mouse click events for UI navigation.
        """
        if self.back_button.touched:
            data.window.back()

        if self.settings_button.touched:
            data.window.display(SettingView())

        if self.quitter_button.touched:
            data.window.first()
