import arcade
import math
from typing import List, Dict, Any, Optional
from modules.ui.toolbox.entity import Entity
from modules.data import data
from modules.logger import Logger

"""Provides a specialized view for rendering and interacting with grid-based tilesets."""

logger = Logger("DebugTilesView")


class DebugTilesView(arcade.View):
    """Manages the visualization and selection logic for multiple asset tilesets."""

    def __init__(self) -> None:
        """Initializes the view state, grid configuration, and tileset definitions."""
        super().__init__()

        self.grid_size: int = data.UI_EDITOR_GRID_SIZE

        self.follower: Entity = Entity()
        self.follower.height = self.grid_size
        self.follower.width = self.grid_size

        self.tilesets: List[Dict[str, Any]] = [
            {
                "name": "Gate Grid",
                "path": "assets/grid/gate_grid.png",
                "tile_w": 27,
                "tile_h": 27,
                "columns": 6,
                "count": 6 * 6,
                "textures": [],
            },
            {
                "name": "UI Grid",
                "path": "assets/grid/ui_grid.png",
                "tile_w": 32,
                "tile_h": 32,
                "columns": 23,
                "count": 9 * 23,
                "textures": [],
            },
            {
                "name": "UI Border Grid",
                "path": "assets/grid/ui_border_grid.png",
                "tile_w": 64,
                "tile_h": 64,
                "columns": 4,
                "count": 4 * 4,
                "textures": [],
            },
        ]

        self.load_tilesets()

        self.current_index: int = 0
        self.hovered_index: Optional[str] = None

        self.display_start_x: int = 500
        self.display_start_y: int = 500

    def load_tilesets(self) -> None:
        """Parses tileset paths and extracts texture grids for each entry."""
        for ts in self.tilesets:
            try:
                sheet = arcade.SpriteSheet(ts["path"])
                ts["textures"] = sheet.get_texture_grid(
                    size=(ts["tile_w"], ts["tile_h"]),
                    columns=ts["columns"],
                    count=ts["count"],
                )
            except Exception as e:
                logger.error(f"Error loading tileset {ts['name']}: {e}")
                ts["textures"] = []

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """Updates the hovered_index based on the current mouse coordinates.

        Args:
            x: Horizontal screen coordinate of the mouse.
            y: Vertical screen coordinate of the mouse.
            delta_x: Change in horizontal mouse position.
            delta_y: Change in vertical mouse position.
        """
        self.hovered_index = None

        current_set = self.tilesets[self.current_index]
        cols = current_set["columns"]
        total_count = current_set["count"]

        grid_x = (x - self.display_start_x) // self.grid_size
        grid_y = (y - self.display_start_y) // self.grid_size

        rows = math.ceil(total_count / cols)

        if 0 <= grid_x < cols and 0 <= grid_y < rows:
            index = int(grid_y * cols + grid_x)
            if 0 <= index < total_count:
                self.hovered_index = f"{current_set['name']} Index: {index}"

    def on_draw(self) -> None:
        """Renders the active tileset, grid interface, and UI feedback labels."""
        self.clear()

        current_set = self.tilesets[self.current_index]
        textures = current_set["textures"]
        cols = current_set["columns"]

        arcade.draw_text(
            f"Current Set: {current_set['name']} (Arrow Keys to Switch)",
            self.display_start_x,
            self.display_start_y + (len(textures) // cols * self.grid_size) + 50,
            arcade.color.WHITE,
            14,
        )

        for i, texture in enumerate(textures):
            column_x = i % cols
            row_y = i // cols

            tile_x = column_x * self.grid_size + self.display_start_x
            tile_y = row_y * self.grid_size + self.display_start_y

            rect = arcade.XYWH(
                x=tile_x,
                y=tile_y,
                width=self.grid_size,
                height=self.grid_size,
                anchor=arcade.Vec2(0, 0),
            )

            arcade.draw_texture_rect(texture, rect)

        if self.hovered_index is not None:
            arcade.draw_text(
                f"Hovered: {self.hovered_index}", 10, 10, arcade.color.CYAN, 16
            )

    def on_update(self, delta_time: float) -> None:
        """Stub for frame-specific update logic."""
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Processes navigation keys for tileset selection and application control.

        Args:
            key: The key code triggered.
            key_modifiers: Bitmask of modifier keys active.
        """
        if key == arcade.key.ESCAPE:
            self.current_path = None
            self.selected_follower = None

        elif key == arcade.key.A:
            arcade.exit()

        elif key == arcade.key.RIGHT:
            # Wrap to start if exceeding bounds
            self.current_index = (self.current_index + 1) % len(self.tilesets)
            logger.debug(f"Switched to: {self.tilesets[self.current_index]['name']}")

        elif key == arcade.key.LEFT:
            # Wrap to end if going below zero
            self.current_index = (self.current_index - 1) % len(self.tilesets)
            logger.debug(f"Switched to: {self.tilesets[self.current_index]['name']}")

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """Stub for keyboard release events."""
        pass

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Stub for mouse button down events."""
        pass

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Stub for mouse button up events."""
        pass
