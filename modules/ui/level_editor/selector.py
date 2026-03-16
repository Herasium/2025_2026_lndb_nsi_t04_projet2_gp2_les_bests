import arcade
from typing import List, Any

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text
from modules.ui.toolbox.id_generator import random_id

from modules.data import data
from modules.data.level import Level


from modules.ui.editor.view import EditorView
from modules.ui.level_player.selector import LevelPlayerSelector


class LevelEditorSelector(arcade.View):
    """
    A view for selecting or creating game levels within the editor interface.
    """

    def __init__(self) -> None:
        """
        Initialize the LevelEditorSelector view, set background, and setup UI components.
        """
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK
        self.texts: List[Text] = []  # List to hold UI Text objects
        self.levels: List[Any] = []  # List to store references to loaded level data
        self.setup()

    def setup(self) -> None:
        """
        Configure the display elements and populate the list of available levels.
        """
        # Define static UI labels for the menu
        debug_list: List[str] = [
            "Level Editor Selector",
            "<- Back",
            "+ New +",
            "Play Level Selector",
            "",
        ]

        # Iterate through loaded data and add level details to the display list
        for i in data.loaded_levels:
            level = data.loaded_levels[i]
            debug_list.append(f"Level {level.number} {level.name} #{level.id}")
            self.levels.append(i)

        start_y: int = 1080 - 70

        # Instantiate and position UI Text objects based on the debug_list
        for index, item in enumerate(debug_list):
            self.texts.append(Text())
            self.texts[-1].x = 64
            self.texts[-1].y = start_y - (index * 25)
            self.texts[-1].text = item
            self.texts[-1].align = ("left", "center")

    def reset(self) -> None:
        """
        Reset the view state if necessary.
        """
        pass

    def on_draw(self) -> None:
        """
        Render the UI elements and their hitboxes to the screen.
        """
        self.clear()

        for i in self.texts:
            i.draw()  # Draw the text label
            i.hitbox.draw()  # Draw the interaction area for debugging

    def on_update(self, delta_time: float) -> None:
        """
        Handle per-frame game logic updates.

        Parameters:
        - delta_time: time elapsed since the last frame
        """
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """
        Handle keyboard input for exiting the application.

        Parameters:
        - key: integer representation of the key pressed
        - key_modifiers: bitmask for pressed modifiers (Shift, Ctrl, etc.)
        """
        if key == 97:  # ASCII 'a'
            arcade.exit()

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """
        Handle key release events.
        """
        pass

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """
        Update global mouse position tracker.
        """
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """
        Check for interaction with UI elements when the mouse is pressed.
        """
        for index in range(len(self.texts)):
            text = self.texts[index]

            if text.touched:  # If the text element is clicked
                if index > 4:
                    # Switch to EditorView with the selected level
                    data.window.display(
                        EditorView(level=data.loaded_levels[self.levels[index - 5]])
                    )
                elif index == 1:
                    # Return to the previous menu
                    data.window.back()
                elif index == 2:
                    # Initialize a new level
                    data.window.display(EditorView(level=Level(random_id())))
                elif index == 3:
                    # Switch to the level selector
                    data.window.display(LevelPlayerSelector())

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """
        Handle mouse release events.
        """
        pass
