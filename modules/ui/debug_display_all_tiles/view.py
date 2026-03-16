import arcade
import math
from typing import List, Dict, Any, Optional
from modules.ui.toolbox.entity import Entity
from modules.data import data
from modules.logger import Logger

# Initialize logger for the debug view
logger = Logger("DebugTilesView")


class DebugTilesView(arcade.View):
    """
    A view class for debugging and displaying tilesets in an grid-based layout.
    """

    def __init__(self) -> None:
        """
        Initialize the DebugTilesView, setting up tileset data and grid properties.
        """
        super().__init__()

        # Grid settings from configuration
        self.grid_size: int = data.UI_EDITOR_GRID_SIZE

        # Setup follower entity for visual reference or future interaction
        self.follower: Entity = Entity()
        self.follower.height = self.grid_size
        self.follower.width = self.grid_size

        # Define data structures for tilesets to be loaded
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

        # Populate tileset texture lists
        self.load_tilesets()

        # Selection state tracking
        self.current_index: int = 0
        self.hovered_index: Optional[str] = None

        # Screen coordinates for display
        self.display_start_x: int = 500
        self.display_start_y: int = 500

    def load_tilesets(self) -> None:
        """
        Loads the textures for all tilesets defined in self.tilesets.
        """
        for ts in self.tilesets:
            try:
                # Use arcade to load spritesheet and grid
                sheet = arcade.SpriteSheet(ts["path"])
                ts["textures"] = sheet.get_texture_grid(
                    size=(ts["tile_w"], ts["tile_h"]),
                    columns=ts["columns"],
                    count=ts["count"],
                )
            except Exception as e:
                # Log errors without crashing if an asset fails to load
                logger.error(f"Error loading tileset {ts['name']}: {e}")
                ts["textures"] = []

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """
        Handle mouse movement to determine which tile is being hovered.

        Parameters:
        - x: mouse x-coordinate
        - y: mouse y-coordinate
        - delta_x: change in x
        - delta_y: change in y
        """
        self.hovered_index = None

        current_set = self.tilesets[self.current_index]
        cols = current_set["columns"]
        total_count = current_set["count"]

        # Calculate grid cell based on screen position
        grid_x = (x - self.display_start_x) // self.grid_size
        grid_y = (y - self.display_start_y) // self.grid_size

        rows = math.ceil(total_count / cols)

        # Bounds check to verify if mouse is within valid grid area
        if 0 <= grid_x < cols and 0 <= grid_y < rows:
            index = int(grid_y * cols + grid_x)
            if 0 <= index < total_count:
                # Store descriptive string for the hovered tile
                self.hovered_index = f"{current_set['name']} Index: {index}"

    def on_draw(self) -> None:
        """
        Render the current tileset, grid labels, and hover info.
        """
        self.clear()

        current_set = self.tilesets[self.current_index]
        textures = current_set["textures"]
        cols = current_set["columns"]

        # Draw current tileset label
        arcade.draw_text(
            f"Current Set: {current_set['name']} (Arrow Keys to Switch)",
            self.display_start_x,
            self.display_start_y + (len(textures) // cols * self.grid_size) + 50,
            arcade.color.WHITE,
            14,
        )

        # Loop through all textures in the active set
        for i, texture in enumerate(textures):
            column_x = i % cols
            row_y = i // cols

            # Calculate screen coordinates for the tile
            tile_x = column_x * self.grid_size + self.display_start_x
            tile_y = row_y * self.grid_size + self.display_start_y

            # Draw tile texture using explicit rectangle anchor
            rect = arcade.XYWH(
                x=tile_x,
                y=tile_y,
                width=self.grid_size,
                height=self.grid_size,
                anchor=arcade.Vec2(0, 0),
            )

            arcade.draw_texture_rect(texture, rect)

        # Draw hover information if applicable
        if self.hovered_index is not None:
            arcade.draw_text(
                f"Hovered: {self.hovered_index}", 10, 10, arcade.color.CYAN, 16
            )

    def on_update(self, delta_time: float) -> None:
        """Update logic placeholder."""
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """
        Handle keyboard input for switching tilesets or exiting.

        Parameters:
        - key: arcade key constant
        - key_modifiers: active key modifiers
        """
        if key == arcade.key.ESCAPE:
            self.current_path = None
            self.selected_follower = None

        elif key == arcade.key.A:
            arcade.exit()

        # Handle cyclic switching between tilesets
        elif key == arcade.key.RIGHT:
            self.current_index = (self.current_index + 1) % len(self.tilesets)
            logger.debug(f"Switched to: {self.tilesets[self.current_index]['name']}")

        elif key == arcade.key.LEFT:
            self.current_index = (self.current_index - 1) % len(self.tilesets)
            logger.debug(f"Switched to: {self.tilesets[self.current_index]['name']}")

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """Key release placeholder."""
        pass

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Mouse press placeholder."""
        pass

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Mouse release placeholder."""
        pass
