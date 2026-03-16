"""Provides grid rendering utilities for the UI editor environment."""

import arcade
from modules.data import data


class Grid:
    """Manages the visual point grid overlay for the UI editor interface."""

    def __init__(self) -> None:
        """Initializes the grid configuration using constants from the data module."""
        self.size: int = data.UI_EDITOR_GRID_SIZE

    def draw(self) -> None:
        """Renders a grid of points over the 1280x720 workspace area."""
        for y in range(0, 720, self.size):
            for x in range(0, 1280, self.size):
                arcade.draw_point(x, y, arcade.color.DARK_BLUE_GRAY, 5)
