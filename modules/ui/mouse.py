from typing import List, Tuple
from arcade import Vec2
from modules.data import data


class _Mouse:
    """
    Tracks mouse movement, snaps to a grid, and calculates movement direction.
    """

    def __init__(self) -> None:
        """Initialize the Mouse tracking object with default values."""
        self._x: float = 0.0
        self._y: float = 0.0
        self._cursor: Vec2 = Vec2(0, 0)
        self._position: Tuple[float, float] = (0.0, 0.0)

        self.history: List[Vec2] = (
            []
        )  # Stores recent cursor positions for direction tracking
        self.direction: str = "RIGHT"
        self.previous_direction: str = "RIGHT"

        self.direction_bias: int = 0

        self._grid_size: int = data.UI_EDITOR_GRID_SIZE

    def _calculate_cursor(self) -> None:
        """
        Snap the current mouse coordinates to the defined grid size
        and update the _cursor attribute.
        """
        # Round coordinates to the nearest grid step
        self._cursor = Vec2(
            round(self._x / self._grid_size) * self._grid_size,
            round(self._y / self._grid_size) * self._grid_size,
        )

    def _calculate_direction(self) -> None:
        """
        Update the movement direction based on recent history of cursor positions.
        """
        if len(self.history) > 4:
            # Maintain a sliding window of positions
            self.history.pop(0)
            self.history.append(self.cursor)

            x1, y1 = self.history[0]
            x2, y2 = self.history[-1]

            dx: float = x2 - x1
            dy: float = y2 - y1

            self.previous_direction = self.direction

            # Apply bias based on current movement state to influence new direction
            if self.previous_direction == "RIGHT":
                dx += self.direction_bias
            if self.previous_direction == "LEFT":
                dx -= self.direction_bias

            if self.previous_direction == "UP":
                dy += self.direction_bias
            if self.previous_direction == "DOWN":
                dy -= self.direction_bias

            # Determine dominant axis of movement
            if abs(dx) >= abs(dy):
                self.direction = "RIGHT" if dx > 0 else "LEFT"
            else:
                self.direction = "UP" if dy > 0 else "DOWN"
        else:
            # Build initial history until threshold is met
            self.history.append(self.cursor)

    @property
    def position(self) -> Tuple[float, float]:
        """Get the raw mouse position."""
        return self._position

    @position.setter
    def position(self, value: Tuple[float, float]) -> Tuple[float, float]:
        """
        Set raw mouse position and trigger dependent calculations.

        Parameters:
        - value: (x, y) coordinates

        Returns:
        - The updated position tuple
        """
        self._position = value
        self._x = self._position[0]
        self._y = self._position[1]
        self._calculate_cursor()  # Snap to grid
        self._calculate_direction()  # Update movement state
        return self._position

    @property
    def x(self) -> float:
        """Get current x coordinate."""
        return self._x

    @property
    def y(self) -> float:
        """Get current y coordinate."""
        return self._y

    @property
    def cursor(self) -> Vec2:
        """Get the current grid-snapped cursor position."""
        return self._cursor

    @property
    def grid_size(self) -> int:
        """Get the current grid size."""
        return self._grid_size

    @grid_size.setter
    def grid_size(self, value: int) -> None:
        """
        Update the grid size and recalculate cursor snap.

        Parameters:
        - value: New grid size in pixels
        """
        self._grid_size = value
        self._calculate_cursor()


# Global mouse tracking instance
mouse: _Mouse = _Mouse()
