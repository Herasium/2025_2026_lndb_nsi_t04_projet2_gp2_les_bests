import arcade
from typing import Any

from modules.ui.mouse import mouse
from modules.ui.toolbox.button import Button
from modules.data import data


class SettingView(arcade.View):
    """
    A view representing the settings menu in the application.
    Handles rendering of UI elements, frame borders, and user input.
    """

    def __init__(self) -> None:
        """
        Initialize the SettingView, configure UI element positions, and set up assets.
        """
        super().__init__()

        self.background_color: arcade.Color = arcade.color.JET
        self.name_banner_sprite: Any = data.name_banner

        # Initialize buttons with specific dimensions and positions
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
        """
        Handle key press events. Exit the game if 'a' is pressed.

        Parameters:
        - key: The key code pressed.
        - key_modifiers: Bitwise combination of modifier keys.
        """
        if key == 97:  # Key code for "a"
            arcade.exit()

    def draw_tile(self, id: int, x: float, y: float) -> None:
        """
        Draw a specific UI tile from the data set at the given coordinates.

        Parameters:
        - id: The index/ID of the tile in the texture array.
        - x: X-coordinate for the drawing position.
        - y: Y-coordinate for the drawing position.
        """
        rect: arcade.XYWH = arcade.XYWH(
            x=x, y=y, width=64, height=64, anchor=arcade.Vec2(0, 0)
        )

        arcade.draw_texture_rect(data.ui_border_tiles[id], rect)

    def draw_frame_border(self) -> None:
        """
        Constructs and draws the UI frame border by placing various tiles.
        """
        start_x: int = 32
        start_y: int = 865
        y_len: int = 13
        x_len: int = 28

        # Top border row
        self.draw_tile(0, start_x, start_y)
        for i in range(x_len - 1):
            self.draw_tile(1, start_x + (i + 1) * 64, start_y)
        self.draw_tile(3, start_x + x_len * 64, start_y)

        # Side borders
        for i in range(y_len - 1):
            self.draw_tile(4, start_x, start_y - (i + 1) * 64)
            self.draw_tile(7, start_x + x_len * 64, start_y - (i + 1) * 64)

        # Bottom border row
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
        Fills the inner area of the frame with background tiles.
        """
        start_x: int = 32
        start_y: int = 865 + 64
        y_len: int = 15

        # Nested loop to tile the background area
        for i in range(y_len - 1):
            for a in range(29):
                self.draw_tile(9, start_x + (a) * 64, start_y - (i + 1) * 64)

    def on_draw(self) -> None:
        """
        Render all elements in the settings view.
        """
        self.clear(arcade.color.BLACK)

        self.draw_frame_background()
        self.draw_frame_border()

        # Draw UI buttons
        self.back_button.draw()
        self.settings1_button.draw()
        self.settings2_button.draw()
        self.settings3_button.draw()
        self.settings4_button.draw()

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """
        Update the mouse position variable when the mouse moves.

        Parameters:
        - x, y: Current mouse coordinates.
        - delta_x, delta_y: Change in mouse position.
        """
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """
        Handle mouse click events to trigger UI interactions.

        Parameters:
        - x, y: Position of the click.
        - button: The mouse button pressed.
        - key_modifiers: Modifier keys held down during the click.
        """
        if self.back_button.touched:  # Check if back button was clicked
            data.window.back()
