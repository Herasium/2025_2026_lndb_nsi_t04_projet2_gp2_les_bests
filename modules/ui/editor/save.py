"""Provides the SaveFrame view for editing and saving chip configuration data."""

import arcade
from typing import Any

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text
from modules.ui.toolbox.entity import Entity
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
        self.typing: bool = False
        self.current_text = "Default Chip"

        self.setup()

    def setup(self) -> None:

        self.bg = Entity(0, 0, 1920, 1088, arcade.Sprite(data.background_grid_texture))
        self.border = Entity(0, 0, 1920, 960, data.border_small)
        self.title = Entity(0, 952, 1920, 128, data.name_banner)
        self.chip_save = Entity(1920 / 2 - 896 / 2, 700, 896, 128, data.chip_save)
        self.chip_name = Text(
            x=1920 / 2 - 200,
            y=1080 / 2,
            width=500,
            height=200,
            text=self.current_text,
            align=("left", "center"),
        )
        self.save_button = Entity(
            x=1920 / 2 - 262.5 / 2,
            y=1080 / 2 - 400,
            width=262.5,
            height=150,
            sprite=data.button_save,
        )
        self.sub_title = Text(
            x=1920 / 2 - 200,
            y=1080 / 2 + 30,
            width=500,
            height=200,
            text="Chip Name (Click to Edit.)",
            align=("left", "center"),
            size=12,
        )

        self.chip_id = Text(
            x=1920 / 2,
            y=1080 / 2 - 100,
            width=500,
            height=200,
            text=f"Chip Id: {self.chip.id}",
            align=("center", "center"),
            size=18,
        )
        self.chip_version = Text(
            x=1920 / 2,
            y=1080 / 2 - 150,
            width=500,
            height=200,
            text=f"Chip Version: {data.VERSION}",
            align=("center", "center"),
            size=18,
        )

        self.typing_collider = Entity(
            x=1920 / 2 - 250, y=1080 / 2 - 50, width=500, height=100
        )

    def reset(self) -> None:
        """Resets the internal state of the view."""
        pass

    def on_draw(self) -> None:
        """Renders all configured UI text elements."""
        self.clear()
        self.bg.draw()
        self.border.draw()
        self.title.draw()
        self.chip_save.draw()
        self.chip_name.draw()
        self.save_button.draw()
        self.sub_title.draw()
        self.chip_id.draw()
        self.chip_version.draw()

        if self.typing:
            arcade.draw_line(
                1920 / 2 - 200,
                1080 / 2 - 20,
                1920 / 2 + 200,
                1080 / 2 - 20,
                arcade.color.RED,
                2,
            )
        else:
            arcade.draw_line(
                1920 / 2 - 200,
                1080 / 2 - 20,
                1920 / 2 + 200,
                1080 / 2 - 20,
                arcade.color.WHITE,
                2,
            )

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
            self.current_text = apply_key(self.current_text, key, key_modifiers)[:17]
            self.chip_name.text = self.current_text
        if key == 65307:
            data.window.back()
        if key == 65473:  # Emergency exit: F4
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

        if self.typing_collider.touched:
            self.typing = not self.typing

        if self.save_button.touched:
            self.chip.name = self.current_text
            self.chip.save()
            data.window.back()

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Handles mouse release events."""
        pass
