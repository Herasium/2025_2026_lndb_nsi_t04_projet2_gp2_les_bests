import arcade
from modules.data import data


class Grid:
    """Represents a visual grid for the UI editor."""

    def __init__(self) -> None:
        """Initialize the Grid object with a size defined by data constants."""

        # Set the grid spacing size from the external data module
        self.size: int = data.UI_EDITOR_GRID_SIZE

    def draw(self) -> None:
        """Draw a grid of points across the screen based on the set size.

        The grid covers a resolution of 1280x720.
        """

        # Iterate through vertical positions (y-axis) up to 720
        for y in range(0, 720, self.size):
            # Iterate through horizontal positions (x-axis) up to 1280
            for x in range(0, 1280, self.size):
                # Draw a point at the current coordinate with specified color and size
                arcade.draw_point(x, y, arcade.color.DARK_BLUE_GRAY, 5)
