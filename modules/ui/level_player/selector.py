import arcade
from typing import List, Any

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text

from modules.data import data


from modules.ui.level_player.view import LevelPlayer


class LevelPlayerSelector(arcade.View):
    """Provides an interface for users to select and launch game levels."""

    def __init__(self) -> None:
        """Initializes the view and populates the level selection UI."""
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK
        self.texts: List[Text] = []
        self.levels: List[Any] = []
        self.setup()

    def setup(self) -> None:
        """Configures the UI layout and maps available levels to selectable elements."""
        debug_list: List[str] = ["Chip Editor Selector", "<- Back", ""]

        for i in data.loaded_levels:
            level = data.loaded_levels[i]
            debug_list.append(f"Level {level.number} {level.name} #{level.id}")
            self.levels.append(i)

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
        """Renders text elements and their associated hitboxes."""
        self.clear()

        for i in self.texts:
            i.draw()
            i.hitbox.draw()

    def on_update(self, delta_time: float) -> None:
        """
        Args:
            delta_time: Time elapsed since the last update frame.
        """
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """
        Args:
            key: Integer identifier of the pressed key.
            key_modifiers: Bitmask of active modifier keys.
        """
        if key == 97:
            arcade.exit()

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """
        Args:
            key: Integer identifier of the released key.
            key_modifiers: Bitmask of active modifier keys.
        """
        pass

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """
        Args:
            x: Current horizontal mouse position.
            y: Current vertical mouse position.
            delta_x: Change in horizontal position.
            delta_y: Change in vertical position.
        """
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """
        Args:
            x: Horizontal mouse position during click.
            y: Vertical mouse position during click.
            button: Identifier of the mouse button pressed.
            key_modifiers: Bitmask of active modifier keys.
        """
        for index in range(len(self.texts)):
            text = self.texts[index]

            if text.touched:
                if index > 2:
                    data.window.display(LevelPlayer(self.levels[index - 3]))
                elif index == 1:
                    data.window.back()

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """
        Args:
            x: Horizontal mouse position.
            y: Vertical mouse position.
            button: Identifier of the mouse button released.
            key_modifiers: Bitmask of active modifier keys.
        """
        pass
