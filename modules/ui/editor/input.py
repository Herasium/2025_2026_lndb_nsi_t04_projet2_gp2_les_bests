"""Provides the InputValue view for editing and saving gate configuration data."""

import arcade
from typing import Any
import random

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text
from modules.ui.toolbox.entity import Entity
from modules.ui.toolbox.keys import apply_key
from modules.data import data


class InputFrame(arcade.View):
    """Manages the UI layout and user interactions for editing gate properties."""

    def __init__(self, chip: Any, gate: str) -> None:
        """Initializes the InputValue instance.

        Args:
            chip: The configuration object containing chip data to be modified.
        """
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK
        self.chip: Any = chip
        self.typing: bool = False
        self.current_text = "0"
        self.gate = gate

        self.setup()

    def setup(self) -> None:

        self.bg = Entity(
            0,
            0,
            data.WINDOW_WIDTH,
            (((data.WINDOW_HEIGHT + 32) // 64) * 64),
            arcade.Sprite(data.background_grid_texture),
        )
        self.border = Entity(0, 0, data.WINDOW_WIDTH, 960, data.border_small)
        self.title = Entity(0, 952, data.WINDOW_WIDTH, 128, data.name_banner)
        self.chip_save = Entity(
            data.WINDOW_WIDTH / 2 - 896 / 2, 700, 896, 128, data.input_title
        )
        self.chip_name = Text(
            x=data.WINDOW_WIDTH / 2 - 200,
            y=data.WINDOW_HEIGHT / 2,
            width=500,
            height=200,
            text=self.current_text,
            align=("left", "center"),
        )
        self.save_button = Entity(
            x=data.WINDOW_WIDTH / 2 - (137+137/2) / 2,
            y=data.WINDOW_HEIGHT / 2 - 400,
            width=(137+137/2),
            height=150,
            sprite=data.button_ok,
        )
        self.sub_title = Text(
            x=data.WINDOW_WIDTH / 2 - 200,
            y=data.WINDOW_HEIGHT / 2 + 30,
            width=500,
            height=200,
            text="Input Value (Click to Edit.)",
            align=("left", "center"),
            size=12,
        )


        self.typing_collider = Entity(
            x=data.WINDOW_WIDTH / 2 - 250,
            y=data.WINDOW_HEIGHT / 2 - 50,
            width=500,
            height=100,
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

        if self.typing:
            arcade.draw_line(
                data.WINDOW_WIDTH / 2 - 200,
                data.WINDOW_HEIGHT / 2 - 20,
                data.WINDOW_WIDTH / 2 + 200,
                data.WINDOW_HEIGHT / 2 - 20,
                arcade.color.RED,
                2,
            )
        else:
            arcade.draw_line(
                data.WINDOW_WIDTH / 2 - 200,
                data.WINDOW_HEIGHT / 2 - 20,
                data.WINDOW_WIDTH / 2 + 200,
                data.WINDOW_HEIGHT / 2 - 20,
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
            if key == data.keys.back:
                self.typing = False
                return
            self.current_text = apply_key(self.current_text, key, key_modifiers,int_only=True)
            self.chip_name.text = self.current_text
        if key == data.keys.back:
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
        if len(str(self.current_text)) == 0:
            self.current_text = 0

        if self.typing_collider.touched:
            self.typing = not self.typing
            self.current_text = str(max(min(2**self.chip.gates[self.gate].outputs_sizes[0]-1,int(self.current_text)),0))
        else:
            self.current_text = str(max(min(2**self.chip.gates[self.gate].outputs_sizes[0]-1,int(self.current_text)),0))
            self.typing = False
        self.chip_name.text = self.current_text
        if self.save_button.touched:
            if key_modifiers in [17, 1]:
                self.chip.gates[self.gate].outputs[0] = random.randint(0,2**self.chip.gates[self.gate].outputs_sizes[0]-1)
            else:
                self.chip.gates[self.gate].outputs[0] = max(min(2**self.chip.gates[self.gate].outputs_sizes[0]-1,int(self.current_text)),0)
            self.chip.gates[self.gate].update_text_readings()
            data.window.back()

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Handles mouse release events."""
        pass
