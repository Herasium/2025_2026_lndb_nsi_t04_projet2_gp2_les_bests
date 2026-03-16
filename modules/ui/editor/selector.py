import arcade
from typing import List, Any

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text
from modules.data import data

# Assuming these imports exist in your project structure
from modules.ui.editor.view import EditorView


class EditorChipSelector(arcade.View):
    """
    A view responsible for displaying and selecting available chips for editing.
    """

    def __init__(self) -> None:
        """
        Initialize the EditorChipSelector view.
        """
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK
        self.texts: List[Text] = []  # List of UI text elements
        self.chips: List[Any] = []  # List of chip identifiers/objects
        self.setup()

    def setup(self) -> None:
        """
        Populate the UI elements and chip list for the selector view.
        """
        # Define the base headers and navigation options
        debug_list: List[str] = ["Chip Editor Selector", "<- Back", "+ New +", ""]

        # Dynamically add loaded chips to the list
        for i in data.loaded_chips:
            chip = data.loaded_chips[i]
            debug_list.append(f"Chip #{chip.id}")
            self.chips.append(i)

        start_y: int = 1080 - 70

        # Instantiate and position Text objects for the UI
        for index, item in enumerate(debug_list):
            self.texts.append(Text())
            self.texts[-1].x = 64
            self.texts[-1].y = start_y - (index * 25)
            self.texts[-1].text = item
            self.texts[-1].align = ("left", "center")

    def reset(self) -> None:
        """
        Placeholder for resetting the view state if necessary.
        """
        pass

    def on_draw(self) -> None:
        """
        Render the UI elements and their hitboxes to the screen.
        """
        self.clear()

        # Iterate through all text objects and draw them along with hitboxes
        for i in self.texts:
            i.draw()
            i.hitbox.draw()

    def on_update(self, delta_time: float) -> None:
        """
        Placeholder for frame-by-frame logic updates.

        Parameters:
        - delta_time: Time elapsed since the last frame
        """
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """
        Handle keyboard input for exiting the application.

        Parameters:
        - key: The key code pressed
        - key_modifiers: Bitwise modifiers (Ctrl, Alt, etc.)
        """
        if key == 97:  # Assuming 'a' key exits
            arcade.exit()

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """
        Placeholder for key release logic.
        """
        pass

    def on_mouse_motion(self, x: int, y: int, delta_x: int, delta_y: int) -> None:
        """
        Update the shared mouse position when moved.
        """
        mouse.position = (x, y)

    def on_mouse_press(self, x: int, y: int, button: int, key_modifiers: int) -> None:
        """
        Handle mouse clicks on text UI elements to navigate or edit chips.

        Parameters:
        - x, y: Coordinates of the click
        - button: Mouse button clicked
        - key_modifiers: Active key modifiers
        """
        for index in range(len(self.texts)):
            text: Text = self.texts[index]

            if text.touched:
                # Handle click logic based on index
                if index > 3:
                    # Navigate to specific chip editor
                    data.window.display(EditorView(self.chips[index - 4]))
                elif index == 1:
                    # Go back to previous view
                    data.window.back()
                elif index == 2:
                    # Create new chip
                    data.window.display(EditorView())

    def on_mouse_release(self, x: int, y: int, button: int, key_modifiers: int) -> None:
        """
        Placeholder for mouse release logic.
        """
        pass
