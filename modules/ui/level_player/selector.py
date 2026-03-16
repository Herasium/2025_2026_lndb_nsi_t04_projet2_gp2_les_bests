import arcade
from typing import List, Any

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text

from modules.data import data


from modules.ui.level_player.view import LevelPlayer


class LevelPlayerSelector(arcade.View):
    """
    A view for selecting and launching game levels.
    """

    def __init__(self) -> None:
        """
        Initialize the LevelPlayerSelector view.
        """
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK
        self.texts: List[Text] = []  # Stores UI Text objects
        self.levels: List[Any] = []  # Stores identifiers for loaded levels
        self.setup()

    def setup(self) -> None:
        """
        Configure the UI layout and populate the list of available levels.

        Returns:
            - None
        """
        # Define the static navigation headers
        debug_list: List[str] = ["Chip Editor Selector", "<- Back", ""]

        # Dynamically append levels from the data module
        for i in data.loaded_levels:
            level = data.loaded_levels[i]
            debug_list.append(f"Level {level.number} {level.name} #{level.id}")
            self.levels.append(i)

        start_y: int = 1080 - 70  # Y coordinate for the first menu item

        # Create Text objects for each item in the list
        for index, item in enumerate(debug_list):
            self.texts.append(Text())
            self.texts[-1].x = 64
            self.texts[-1].y = start_y - (index * 25)
            self.texts[-1].text = item
            self.texts[-1].align = ("left", "center")

    def reset(self) -> None:
        """
        Placeholder for state reset logic.
        """
        pass

    def on_draw(self) -> None:
        """
        Render the UI elements to the screen.
        """
        self.clear()

        # Iterate through text objects and draw both text and their hitboxes
        for i in self.texts:
            i.draw()
            i.hitbox.draw()

    def on_update(self, delta_time: float) -> None:
        """
        Update loop, currently unused.

        Parameters:
            - delta_time: time elapsed since last frame
        """
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """
        Handle keyboard inputs.

        Parameters:
            - key: identifier of the pressed key
            - key_modifiers: bitmask of active modifiers (e.g., Shift)
        """
        if key == 97:  # Key code 97 corresponds to 'a'
            arcade.exit()

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """
        Handle key release events, currently unused.
        """
        pass

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """
        Update the shared mouse position when moved.
        """
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """
        Handle mouse click events to detect menu interactions.

        Parameters:
            - x: current mouse x position
            - y: current mouse y position
            - button: mouse button pressed
            - key_modifiers: bitmask of active modifiers
        """
        # Iterate through text objects to check if any were clicked
        for index in range(len(self.texts)):
            text = self.texts[index]

            if text.touched:
                # If index > 2, it indicates a level button was clicked
                if index > 2:
                    data.window.display(LevelPlayer(self.levels[index - 3]))
                # Index 1 is the 'Back' button
                elif index == 1:
                    data.window.back()

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """
        Handle mouse release events, currently unused.
        """
        pass
