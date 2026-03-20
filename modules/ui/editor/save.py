"""Provides the SaveFrame view for editing and saving chip configuration data."""

import arcade
from typing import Any, Dict, List

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text
from modules.ui.toolbox.keys import apply_key
from modules.data import data


class SaveFrame(arcade.View):
    """Manages the UI layout and user interactions for editing chip properties."""

    def __init__(self, chip: Any) -> None:
        """Initializes the SaveFrame instance.

        Args:
            chip: The configuration object containing chip data to be modified.
        """
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK
        self.chip: Any = chip
        self.typing: bool = True
        self.current_text = "Default Chip"

        self.setup()

    def setup(self) -> None:
        
        self.chip_name = Text(x=1920/2,y=1080/2,width=500,height=200,text=self.current_text)
        self.save_button = Text(x=1920/2,y=1080/2+100,width=500,height=200,text="Save!")

    def reset(self) -> None:
        """Resets the internal state of the view."""
        pass

    def on_draw(self) -> None:
        """Renders all configured UI text elements."""
        self.clear()
        self.chip_name.draw()
        self.save_button.draw()



    def on_update(self, delta_time: float) -> None:
        """Handles periodic logic updates."""
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Handles keyboard input events.

        Args:
            key: The identifier of the pressed key.
            key_modifiers: Bitwise flags for modifier keys.
        """
        if self.typing:
            if key == 65307:
                self.typing = False
                return
            self.current_text = apply_key(self.current_text,key,key_modifiers)
            self.chip_name.text = self.current_text
        else:
            if key == 97:
                arcade.exit()

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """Handles key release events."""
        pass

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """Updates the global mouse tracking state.

        Args:
            x: The current x-coordinate of the mouse.
            y: The current y-coordinate of the mouse.
            delta_x: The change in x-coordinate since the last frame.
            delta_y: The change in y-coordinate since the last frame.
        """
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Processes mouse click interactions with UI elements.

        Args:
            x: The x-coordinate of the mouse click.
            y: The y-coordinate of the mouse click.
            button: The mouse button pressed.
            key_modifiers: Bitwise flags for modifier keys.
        """
        if self.save_button.touched:
            self.chip.save()
            data.window.back()

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Handles mouse release events."""
        pass

