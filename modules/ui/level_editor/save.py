import arcade
from typing import Any, Dict, List

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text
from modules.data import data


class SaveFrame(arcade.View):
    """
    A View class for managing and editing level configuration settings.
    """

    def __init__(self, level: Any) -> None:
        """
        Initialize the SaveFrame view.

        Parameters:
        - level: The level object containing data to be edited.
        """
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK
        self.texts: List[Text] = []
        self.level: Any = level
        self.setup()

    def setup(self) -> None:
        """
        Initialize and arrange the UI text elements for the level editor.
        """
        self.texts = []
        # Define the list of labels to display on the screen
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
            "->",
            "--> Save <--",
        ]

        start_y: int = 1080 - 70

        # Instantiate and position Text objects based on debug_list
        for index, item in enumerate(debug_list):
            self.texts.append(Text())
            self.texts[-1].x = 64
            self.texts[-1].y = start_y - (index * 25)
            self.texts[-1].text = item
            self.texts[-1].align = ("left", "center")

    def reset(self) -> None:
        """Placeholder for resetting the view state."""
        pass

    def on_draw(self) -> None:
        """Render all text elements to the screen."""
        self.clear()
        for i in self.texts:
            i.draw()

    def on_update(self, delta_time: float) -> None:
        """Placeholder for logic updates."""
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Handle keyboard input for exiting the application."""
        if key == 97:  # 'a' key
            arcade.exit()

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """Placeholder for key release events."""
        pass

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """Update the internal mouse position state."""
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """
        Handle UI interactions based on mouse clicks on text elements.
        """
        # Navigation
        if self.texts[1].touched:
            data.window.back()

        # Time adjustments
        if self.texts[8].touched:
            self.level.time += 30
            self.setup()
        if self.texts[9].touched:
            self.level.time -= 30
            self.setup()

        # Level number adjustments
        if self.texts[12].touched:
            self.level.number += 1
            self.setup()
        if self.texts[13].touched:
            self.level.number -= 1
            self.setup()

        # Category adjustments
        if self.texts[16].touched:
            self.level.category += 1
            self.setup()
        if self.texts[17].touched:
            self.level.category -= 1
            self.setup()

        # Color and Save operations
        if self.texts[20].touched:
            self.level.color = (self.level.color + 1) % len(data.level_colors)
            self.setup()
        if self.texts[21].touched:
            self.level.save()

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Placeholder for mouse release events."""
        pass

    def get_save_gate_counts(self) -> Dict[Any, int]:
        """
        Calculate the occurrences of each gate type in the level chip.

        Returns:
        - Dict[Any, int]: A dictionary mapping gate types to their count.
        """
        result: Dict[Any, int] = {}
        for i in self.level.chip.gates:
            gate_type = self.level.chip.gates[i].gate_type
            # Initialize count if gate type not yet in dictionary
            if gate_type not in result:
                result[gate_type] = 0
            # Increment count
            result[gate_type] += 1
        return result
