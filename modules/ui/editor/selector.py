import arcade
from typing import List, Any

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text
from modules.data import data
from modules.ui.editor.view import EditorView

"""Module for managing the chip selection interface within the editor."""


class EditorChipSelector(arcade.View):
    """Provides a selection menu for existing chips and navigation to the editor."""

    def __init__(self) -> None:
        """Initializes the view and populates UI components."""
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK
        self.texts: List[Text] = []
        self.chips: List[Any] = []
        self.setup()

    def setup(self) -> None:
        """Configures the initial UI elements and populates available chips."""
        debug_list: List[str] = ["Chip Editor Selector", "<- Back", "+ New +", ""]

        for i in data.loaded_chips:
            chip = data.loaded_chips[i]
            debug_list.append(f"Chip #{chip.id}")
            self.chips.append(i)

        start_y: int = data.WINDOW_HEIGHT - 70

        for index, item in enumerate(debug_list):
            self.texts.append(Text())
            self.texts[-1].x = 64
            self.texts[-1].y = start_y - (index * 25)
            self.texts[-1].text = item
            self.texts[-1].align = ("left", "center")

    def reset(self) -> None:
        """Resets the view state."""
        pass

    def on_draw(self) -> None:
        """Renders the UI elements and their associated hitboxes."""
        self.clear()

        for i in self.texts:
            i.draw()
            i.hitbox.draw()

    def on_update(self, delta_time: float) -> None:
        """Updates frame-by-frame logic.

        Args:
            delta_time: Elapsed time since the last frame.
        """
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Handles keyboard input.

        Args:
            key: The pressed key code.
            key_modifiers: Active bitwise key modifiers.
        """
        if key == 97:
            arcade.exit()

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """Handles key release events.

        Args:
            key: The released key code.
            key_modifiers: Active bitwise key modifiers.
        """
        pass

    def on_mouse_motion(self, x: int, y: int, delta_x: int, delta_y: int) -> None:
        """Updates global mouse position.

        Args:
            x: Current horizontal mouse position.
            y: Current vertical mouse position.
            delta_x: Change in horizontal position.
            delta_y: Change in vertical position.
        """
        mouse.position = (x, y)

    def on_mouse_press(self, x: int, y: int, button: int, key_modifiers: int) -> None:
        """Handles UI selection based on click coordinates.

        Args:
            x: Click horizontal coordinate.
            y: Click vertical coordinate.
            button: Mouse button identifier.
            key_modifiers: Active bitwise key modifiers.
        """
        for index in range(len(self.texts)):
            text: Text = self.texts[index]

            if text.touched:
                if index > 3:
                    data.window.display(EditorView(self.chips[index - 4]))
                elif index == 1:
                    data.window.back()
                elif index == 2:
                    data.window.display(EditorView())

    def on_mouse_release(self, x: int, y: int, button: int, key_modifiers: int) -> None:
        """Handles mouse release events.

        Args:
            x: Release horizontal coordinate.
            y: Release vertical coordinate.
            button: Mouse button identifier.
            key_modifiers: Active bitwise key modifiers.
        """
        pass
