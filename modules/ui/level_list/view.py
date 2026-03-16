import arcade
from typing import List, Dict, Any

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text
from modules.ui.toolbox.entity import Entity
from modules.data import data
from modules.ui.level_player.view import LevelPlayer
from modules.logger import Logger

# Initialize logger for tracking level list operations
logger: Logger = Logger("LevelList")


class LevelList(arcade.View):
    """
    A view class to display a list of levels, categorized and selectable by the user.
    """

    def __init__(self) -> None:
        """Initialize the LevelList view with default settings."""
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK
        self.texts: List[Text] = []
        self.levels: List[Any] = []
        self.camera_y: float = 0.0

        # UI Entities
        self.bg: Entity = None  # type: ignore
        self.border: Entity = None  # type: ignore
        self.title: Entity = None  # type: ignore
        self.buttons: Dict[str, Entity] = {}

        self.setup()

    def setup(self) -> None:
        """
        Configure the UI layout, including background, border, title,
        and generating buttons based on loaded levels.
        """
        # Define structural UI elements
        self.bg = Entity(0, 0, 1920, 1088, arcade.Sprite(data.background_grid_texture))
        self.border = Entity(0, 0, 1920, 960, data.border_small)
        self.title = Entity(0, 952, 1920, 128, data.name_banner)

        self.buttons = {}
        self.texts = []

        # Extract and sort level keys by their assigned numerical order
        levels: List[str] = list(data.loaded_levels.keys())

        def sort_keys(i: str) -> int:
            """Helper to extract the level number for sorting."""
            return data.loaded_levels[i].number

        levels.sort(key=sort_keys)

        # Positioning variables
        pos_y: float = 600 + self.camera_y
        pos_x: float = 75

        # Initialize grouping by category
        current_category: str = data.loaded_levels[levels[0]].category

        # Generate buttons for each level
        for i in levels:
            level = data.loaded_levels[i]

            # Shift position if the category changes
            if level.category != current_category:
                pos_y -= 300
                pos_x = 75
                current_category = level.category

            button = arcade.Sprite(arcade.Texture(data.LEVEL_BUTTONS.get(level.id)))

            # Store button entity in dictionary keyed by level ID
            self.buttons[level.id] = Entity(
                x=pos_x, y=pos_y, width=175, height=175, sprite=button
            )
            pos_x += 200

        # Create category labels
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
        """Reset the view state."""
        pass

    def on_draw(self) -> None:
        """Render all UI elements to the screen."""
        self.clear()
        self.bg.draw()  # Draw background

        # Draw all level buttons
        for i in self.buttons:
            self.buttons[i].draw()

        # Draw category labels
        for i in self.texts:
            i.draw()

        self.border.draw()
        self.title.draw()

    def on_update(self, delta_time: float) -> None:
        """Update logic for the view."""
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Handle key press events, specifically for navigating back."""
        if key == 97:  # Assuming 97 is the key code for 'a'
            data.window.back()

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """Handle key release events."""
        pass

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """Update the global mouse position tracker."""
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Check for clicks on level buttons and launch the selected level."""
        for i in self.buttons:
            if self.buttons[i].touched:
                logger.success(f"Launching Level {i}")
                data.window.display(LevelPlayer(i))

    def on_mouse_scroll(
        self, x: float, y: float, scroll_x: float, scroll_y: float
    ) -> None:
        """Handle vertical scrolling to move through the level list."""
        self.camera_y += scroll_y * -15
        self.camera_y = max(self.camera_y, 0)
        self.setup()  # Rebuild UI to apply new camera position

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Handle mouse release events."""
        pass
