import arcade
from typing import List

from modules.ui.mouse import mouse
from modules.ui.toolbox.button import Button
from modules.ui.editor.view import EditorView
from modules.ui.debug_display_all_tiles.view import DebugTilesView
from modules.ui.main_menu.in_progress_view import MainMenuView

from modules.data import data


class GameView(arcade.View):
    """
    Main menu view for the game, handling initial UI rendering and interactions.
    """

    def __init__(self) -> None:
        """
        Initialize the GameView, setting up UI elements, buttons, and text.
        """
        super().__init__()

        self.background_color: arcade.color = arcade.color.JET

        # Load the UI sprite sheet and create a grid of textures
        self.ui_sheet: arcade.SpriteSheet = arcade.SpriteSheet("assets/ui_grid.png")
        self.ui_tiles: List[arcade.Texture] = self.ui_sheet.get_texture_grid(
            size=(32, 32),
            columns=23,
            count=9 * 23,
        )

        # Initialize Play Button
        self.button_play: Button = Button(self.ui_tiles)
        self.button_play.x = 120
        self.button_play.y = 540
        self.button_play.width = 340
        self.button_play.height = 90
        self.button_play.name = "Jouer"

        # Initialize Quit Button
        self.button_quit: Button = Button(self.ui_tiles)
        self.button_quit.x = 120
        self.button_quit.y = 400
        self.button_quit.width = 340
        self.button_quit.height = 90
        self.button_quit.name = "Quitter"

        # Initialize titles and their corresponding drop shadows for styling
        self.titre1: arcade.Text = arcade.Text(
            "Welcome to",
            x=120,
            y=760,
            color=arcade.color.BLOND,
            font_size=60,
            font_name="Press Start 2P",
        )
        self.shadow_titre1: arcade.Text = arcade.Text(
            "Welcome to",
            x=120,
            y=754,
            color=arcade.color.DEEP_SAFFRON,
            font_size=60,
            font_name="Press Start 2P",
        )
        self.titreL: arcade.Text = arcade.Text(
            "LogicBox",
            x=120,
            y=640,
            color=arcade.color.BLOND,
            font_size=60,
            font_name="Press Start 2P",
        )
        self.shadow_titreL: arcade.Text = arcade.Text(
            "LogicBox",
            x=120,
            y=634,
            color=arcade.color.DEEP_SAFFRON,
            font_size=60,
            font_name="Press Start 2P",
        )

    def reset(self) -> None:
        """Reset the view state if necessary."""
        pass

    def on_draw(self) -> None:
        """Render the UI elements and text to the screen."""
        self.clear()
        self.button_play.draw()
        self.button_quit.draw()
        self.shadow_titre1.draw()
        self.titre1.draw()
        self.shadow_titreL.draw()
        self.titreL.draw()

    def on_update(self, delta_time: float) -> None:
        """Update logic for the view."""
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """
        Handle key press events.

        Parameters:
        - key: The key code pressed
        - key_modifiers: Bitwise modifiers (shift, ctrl, etc.)
        """
        if key == 97:  # ASCII value for "a"
            arcade.exit()

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """Handle key release events."""
        pass

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """
        Handle mouse movement and trigger hover effects on buttons.
        """
        mouse.position = (x, y)

        # Apply hover scaling effect for Play button
        if self.button_play.rect.point_in_rect((x, y)):
            self.button_play.scale = 1.1
        else:
            self.button_play.scale = 1.0

        # Apply hover scaling effect for Quit button
        if self.button_quit.rect.point_in_rect((x, y)):
            self.button_quit.scale = 1.1
        else:
            self.button_quit.scale = 1.0

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """
        Handle mouse click events to navigate menus or exit the game.
        """
        if self.button_play.touched:
            data.window.hide()
            # Navigation based on key modifiers held during click
            if key_modifiers == 16 or key_modifiers == 0:
                data.window.display(EditorView())
            elif key_modifiers == 17 or key_modifiers == 1:
                data.window.display(DebugTilesView())
            elif key_modifiers == 2 or key_modifiers == 18:
                data.window.display(MainMenuView())
            else:
                # Fallback default if modifier is unrecognized
                print(
                    f"Modificator not found, defaulting to EditorView. ({key_modifiers})"
                )
                data.window.display(EditorView())

        if self.button_quit.touched:
            arcade.exit()

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Handle mouse release events."""
        pass
