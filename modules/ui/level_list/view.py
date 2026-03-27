"""Provides a view for navigating and selecting game levels."""

import arcade
from typing import List, Dict, Any

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text
from modules.ui.toolbox.entity import Entity
from modules.data import data
from modules.ui.level_player.view import LevelPlayer
from modules.logger import Logger

logger: Logger = Logger("LevelList")


class LevelList(arcade.View):
    """Displays a categorized, scrollable list of selectable levels."""

    def __init__(self) -> None:
        """Initializes the view with default UI elements and state."""
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK
        self.texts: List[Text] = []
        self.levels: List[Any] = []
        self.camera_y: float = 0.0

        self.bg: Entity = None  # type: ignore
        self.border: Entity = None  # type: ignore
        self.title: Entity = None  # type: ignore
        self.buttons: Dict[str, Entity] = {}

        self.setup()

    def setup(self) -> None:
        """Constructs UI layout, organizes levels into categories, and initializes buttons."""
        self.bg = Entity(
            0,
            0,
            data.WINDOW_WIDTH,
            (((data.WINDOW_HEIGHT + 32) // 64) * 64),
            arcade.Sprite(data.background_grid_texture),
        )
        self.border = Entity(0, 0, data.WINDOW_WIDTH, 960, data.border_small)
        self.title = Entity(0, 952, data.WINDOW_WIDTH, 128, data.name_banner)

        self.back_button = Entity(
            x=1680, y=100, width=160, height=100, sprite=data.button_back
        )

        self.buttons = {}
        self.texts = []

        levels: List[str] = list(data.loaded_levels.keys())

        def sort_keys(i: str) -> int:
            """Determines sort order based on level sequence number."""
            return data.loaded_levels[i].number

        levels.sort(key=sort_keys)

        pos_y: float = 600 + self.camera_y
        pos_x: float = 75

        current_category: str = data.loaded_levels[levels[0]].category

        for i in levels:
            level = data.loaded_levels[i]

            if level.category != current_category:
                pos_y -= 300
                pos_x = 75
                current_category = level.category

            button = arcade.Sprite(arcade.Texture(data.LEVEL_BUTTONS.get(level.id)))

            self.buttons[level.id] = Entity(
                x=pos_x, y=pos_y, width=175, height=175, sprite=button
            )
            pos_x += 200

        c: int = 0
        for i in data.categories:
            self.texts.append(
                Text(
                    x=75,
                    y=800 - c * 300 + self.camera_y,
                    width=100,
                    height=300,
                    text=i,
                    align=("left", "center"),
                )
            )
            c += 1

    def reset(self) -> None:
        """Resets the view to initial state."""
        pass

    def on_draw(self) -> None:
        """Renders the background, level buttons, category labels, and UI overlay."""
        self.clear()
        self.bg.draw()

        for i in self.buttons:
            self.buttons[i].draw()

        for i in self.texts:
            i.draw()

        self.border.draw()
        self.title.draw()
        self.back_button.draw()

    def on_update(self, delta_time: float) -> None:
        """Performs frame-by-frame logic updates."""
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Handles navigation inputs."""
        if key == data.keys.back:
            data.window.display(data.main)
        if key == 65473:  # Emergency exit: F4
            arcade.exit()

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """Handles key release events."""
        pass

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """Updates the global mouse tracking state."""
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Detects level selection clicks and initiates scene transition."""
        for i in self.buttons:
            if self.buttons[i].touched:
                logger.success(f"Launching Level {i}")
                data.window.display(LevelPlayer(i))

        if self.back_button.touched:
            data.window.display(data.main)

    def on_mouse_scroll(
        self, x: float, y: float, scroll_x: float, scroll_y: float
    ) -> None:
        """Updates vertical camera offset and rebuilds layout."""
        self.camera_y += scroll_y * -data.MOUSE_SENSI
        self.camera_y = max(self.camera_y, 0)
        self.setup()

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Handles mouse release events."""
        pass
