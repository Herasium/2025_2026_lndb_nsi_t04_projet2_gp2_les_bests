"""Provides mouse tracking capabilities with grid-snapping and directional analysis."""

from typing import List, Tuple
from arcade import Vec2
from modules.data import data


class _Mouse:
    """Manages mouse state, including raw position, grid-aligned coordinates, and movement vectors."""

    def __init__(self) -> None:
        """Initializes the mouse tracker with default state."""
        self._x: float = 0.0
        self._y: float = 0.0
        self._cursor: Vec2 = Vec2(0, 0)
        self._position: Tuple[float, float] = (0.0, 0.0)

        self.history: List[Vec2] = []
        self.direction: str = "RIGHT"
        self.previous_direction: str = "RIGHT"

        self.direction_bias: int = 0

        self._grid_size: int = data.UI_EDITOR_GRID_SIZE

    def _calculate_cursor(self) -> None:
        """Updates the grid-snapped cursor position based on current raw coordinates."""
        self._cursor = Vec2(
            round(self._x / self._grid_size) * self._grid_size,
            round(self._y / self._grid_size) * self._grid_size,
        )

    def _calculate_direction(self) -> None:
        """Analyzes recent position history to determine current movement direction."""
        if len(self.history) > 4:
            self.history.pop(0)
            self.history.append(self.cursor)

            x1, y1 = self.history[0]
            x2, y2 = self.history[-1]

            dx: float = x2 - x1
            dy: float = y2 - y1

            self.previous_direction = self.direction

            if self.previous_direction == "RIGHT":
                dx += self.direction_bias
            if self.previous_direction == "LEFT":
                dx -= self.direction_bias

            if self.previous_direction == "UP":
                dy += self.direction_bias
            if self.previous_direction == "DOWN":
                dy -= self.direction_bias

            if abs(dx) >= abs(dy):
                self.direction = "RIGHT" if dx > 0 else "LEFT"
            else:
                self.direction = "UP" if dy > 0 else "DOWN"
        else:
            self.history.append(self.cursor)

    @property
    def position(self) -> Tuple[float, float]:
        """Returns the raw mouse coordinates."""
        return self._position

    @position.setter
    def position(self, value: Tuple[float, float]) -> Tuple[float, float]:
        """Updates the raw mouse position and triggers dependent state calculations.

        Args:
            value: The (x, y) coordinates.

        Returns:
            The updated position tuple.
        """
        self._position = value
        self._x = self._position[0]
        self._y = self._position[1]
        self._calculate_cursor()
        self._calculate_direction()
        return self._position

    @property
    def x(self) -> float:
        """Returns the current x coordinate."""
        return self._x

    @property
    def y(self) -> float:
        """Returns the current y coordinate."""
        return self._y

    @property
    def cursor(self) -> Vec2:
        """Returns the current grid-snapped cursor position."""
        return self._cursor

    @property
    def grid_size(self) -> int:
        """Returns the active grid size."""
        return self._grid_size

    @grid_size.setter
    def grid_size(self, value: int) -> None:
        """Updates the grid size and adjusts the snapped cursor position.

        Args:
            value: The pixel size of the grid.
        """
        self._grid_size = value
        self._calculate_cursor()


mouse: _Mouse = _Mouse()
