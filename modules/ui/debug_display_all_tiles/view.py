import arcade
# form modules.ui.mouse import mouse # (Unused in snippet, kept if needed)
from modules.ui.toolbox.entity import Entity
# from modules.ui.toolbox.grid import Grid # (Unused in snippet)
# from modules.ui.toolbox.id_generator import random_id # (Unused in snippet)
from modules.data import data

class DebugTilesView(arcade.View):

    def __init__(self):
        super().__init__()

        self.grid_size = data.UI_EDITOR_GRID_SIZE

        self.follower = Entity()
        self.follower.height = self.grid_size
        self.follower.width = self.grid_size

        # --- TILESET CONFIGURATION ---
        # Define your list of tilesets here. 
        # This makes it easy to add more without changing logic code.
        self.tilesets = [
            {
                "name": "Gate Grid",
                "path": "assets/gate_grid.png",
                "tile_w": 27,
                "tile_h": 27,
                "columns": 6,
                "count": 6 * 6, # Rows * Cols
                "textures": []  # Will be populated automatically
            },
            {
                "name": "UI Grid",
                "path": "assets/ui_grid.png",
                "tile_w": 32,
                "tile_h": 32,
                "columns": 23,
                "count": 9 * 23,
                "textures": []
            },
            {
                "name": "UI Border Grid",
                "path": "assets/ui_border_grid.png",
                "tile_w": 64,
                "tile_h": 64,
                "columns": 4,
                "count": 4 * 4,
                "textures": []
            }
        ]

        # Load textures for all defined tilesets
        self.load_tilesets()

        # State tracking
        self.current_index = 0
        self.hovered_index = None

        # Display settings
        self.display_start_x = 500
        self.display_start_y = 500

    def load_tilesets(self):
        """Iterates through the config list and loads actual textures."""
        for ts in self.tilesets:
            try:
                sheet = arcade.SpriteSheet(ts["path"])
                ts["textures"] = sheet.get_texture_grid(
                    size=(ts["tile_w"], ts["tile_h"]),
                    columns=ts["columns"],
                    count=ts["count"]
                )
            except Exception as e:
                print(f"Error loading tileset {ts['name']}: {e}")
                ts["textures"] = []

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        self.hovered_index = None
        
        # Get current config
        current_set = self.tilesets[self.current_index]
        cols = current_set["columns"]
        total_count = current_set["count"]

        # Calculate grid position relative to the display offset
        # Note: We divide by self.grid_size (display size), not tile source size
        grid_x = (x - self.display_start_x) // self.grid_size
        grid_y = (y - self.display_start_y) // self.grid_size

        # Determine number of rows dynamically based on count and columns
        import math
        rows = math.ceil(total_count / cols)

        # Check if mouse is within bounds of the current grid
        if 0 <= grid_x < cols and 0 <= grid_y < rows:
            index = int(grid_y * cols + grid_x)
            if 0 <= index < total_count:
                self.hovered_index = f"{current_set['name']} Index: {index}"

    def on_draw(self):
        self.clear()

        current_set = self.tilesets[self.current_index]
        textures = current_set["textures"]
        cols = current_set["columns"]

        # Draw the title of the current set
        arcade.draw_text(
            f"Current Set: {current_set['name']} (Arrow Keys to Switch)",
            self.display_start_x,
            self.display_start_y + (len(textures) // cols * self.grid_size) + 50,
            arcade.color.WHITE,
            14
        )

        # Dynamic Drawing Loop
        for i, texture in enumerate(textures):
            # Calculate grid coordinates based on index
            column_x = i % cols
            row_y = i // cols

            tile_x = column_x * self.grid_size + self.display_start_x
            tile_y = row_y * self.grid_size + self.display_start_y

            rect = arcade.XYWH(
                x=tile_x,
                y=tile_y,
                width=self.grid_size,
                height=self.grid_size,
                anchor=arcade.Vec2(0, 0)
            )

            arcade.draw_texture_rect(texture, rect)

        # Draw Hover Info
        if self.hovered_index is not None:
            arcade.draw_text(
                f"Hovered: {self.hovered_index}",
                10,
                10,
                arcade.color.CYAN,
                16
            )

    def on_update(self, delta_time):
        pass

    def on_key_press(self, key, key_modifiers):
        # ESC Key
        if key == arcade.key.ESCAPE:
            self.current_path = None
            self.selected_follower = None
        
        # 'a' Key
        elif key == arcade.key.A:
            arcade.exit()

        # Switch Tilesets: Right Arrow (Next)
        elif key == arcade.key.RIGHT:
            self.current_index = (self.current_index + 1) % len(self.tilesets)
            print(f"Switched to: {self.tilesets[self.current_index]['name']}")

        # Switch Tilesets: Left Arrow (Previous)
        elif key == arcade.key.LEFT:
            self.current_index = (self.current_index - 1) % len(self.tilesets)
            print(f"Switched to: {self.tilesets[self.current_index]['name']}")

    def on_key_release(self, key, key_modifiers):
        pass

    def on_mouse_press(self, x, y, button, key_modifiers):
        pass

    def on_mouse_release(self, x, y, button, key_modifiers):
        pass