"""Provides the SaveFrame view for editing and saving level configuration data."""

import arcade
from typing import Any, Dict, List

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text
from modules.data import data


class SaveFrame(arcade.View):
    """Manages the UI layout and user interactions for editing level properties."""

    def __init__(self, level: Any) -> None:
        """Initializes the SaveFrame instance.

        Args:
            level: The configuration object containing level data to be modified.
        """
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK
        self.texts: List[Text] = []
        self.level: Any = level
        self.setup()

    def setup(self) -> None:
        """Initializes and positions UI text elements based on current level data."""
        self.texts = []
        debug_list: List[str] = [
            "Level Saver",
            "<- Back",
            "--------------",
            f"Level {self.level.id} {self.level.name}",
            "Level Description : ",
            self.level.description,
            "--------------",
            f"Level Time : {self.level.time}",
            "+ 30 sec",
            " - 30 sec",
            "--------------",
            f"Level Number : {self.level.number}",
            "+ 1",
            "- 1",
            "--------------",
            f"Level Category : {self.level.category}",
            "+ 1",
            "- 1",
            "--------------",
            f"Level Color : {data.level_colors[self.level.color]}",
            "-> Next",
            f"Public Custom Chip : {self.level.is_custom}",
            "-> Change",
            "--> Save <--",
        ]

        start_y: int = 1080 - 70

        for index, item in enumerate(debug_list):
            self.texts.append(Text())
            self.texts[-1].x = 64
            self.texts[-1].y = start_y - (index * 25)
            self.texts[-1].text = item
            self.texts[-1].align = ("left", "center")

    def reset(self) -> None:
        """Resets the internal state of the view."""
        pass

    def on_draw(self) -> None:
        """Renders all configured UI text elements."""
        self.clear()
        for i in self.texts:
            i.draw()

    def on_update(self, delta_time: float) -> None:
        """Handles periodic logic updates."""
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Handles keyboard input events.

        Args:
            key: The identifier of the pressed key.
            key_modifiers: Bitwise flags for modifier keys.
        """
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
        if self.texts[1].touched:
            data.window.back()

        if self.texts[8].touched:
            self.level.time += 30
            self.setup()
        if self.texts[9].touched:
            self.level.time -= 30
            self.setup()

        if self.texts[12].touched:
            self.level.number += 1
            self.setup()
        if self.texts[13].touched:
            self.level.number -= 1
            self.setup()

        if self.texts[16].touched:
            self.level.category += 1
            self.setup()
        if self.texts[17].touched:
            self.level.category -= 1
            self.setup()

        if self.texts[20].touched:
            self.level.color = (self.level.color + 1) % len(data.level_colors)
            self.setup()
        if self.texts[22].touched:
            self.level.is_custom = not self.level.is_custom
            self.setup()
        if self.texts[23].touched:
            self.level.save()

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Handles mouse release events."""
        pass

    def get_save_gate_counts(self) -> Dict[Any, int]:
        """Calculates the frequency of gate types used in the current level.

        Returns:
            A dictionary mapping specific gate types to their total occurrences.
        """
        result: Dict[Any, int] = {}
        for i in self.level.chip.gates:
            gate_type = self.level.chip.gates[i].gate_type
            if gate_type not in result:
                result[gate_type] = 0
            result[gate_type] += 1
        return result
