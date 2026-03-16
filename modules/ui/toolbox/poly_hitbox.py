import arcade
import arcade.geometry
from typing import List, Tuple, Dict, Any
from modules.ui.mouse import mouse

"""Provides collision detection and rendering logic for polygon-based hitboxes."""


class PolyHitbox:
    """Manages vertex-based collision boundaries and associated rendering."""

    def __init__(self, points: List[Tuple[float, float]] = None) -> None:
        """Initializes a polygon hitbox.

        Args:
            points: Vertices defined as coordinate pairs forming the polygon perimeter.
        """
        self.points: List[Tuple[float, float]] = points if points is not None else []

    def draw(self) -> None:
        """Renders the polygon outline to the screen."""
        if len(self.points) > 1:
            arcade.draw_polygon_outline(self.points, arcade.color.ALLOY_ORANGE)

    def save(self) -> Dict[str, Any]:
        """Serializes hitbox data for persistence.

        Returns:
            A dictionary containing the identifier and vertex collection.
        """
        return {"type": "PolyHitbox", "points": self.points}

    @property
    def touched(self) -> bool:
        """Determines if the mouse cursor overlaps with the polygon area.

        Returns:
            True if the mouse coordinates intersect the polygon geometry.
        """
        mouse_x: float
        mouse_y: float
        mouse_x, mouse_y = mouse.position

        return arcade.geometry.is_point_in_polygon(
            x=mouse_x, y=mouse_y, polygon=self.points
        )

    def __repr__(self) -> str:
        """Returns the formal developer-facing representation of the hitbox."""
        return f"PolyHitBox (points={self.points})"

    def __str__(self) -> str:
        """Returns the informal user-facing representation of the hitbox."""
        return f"PolyHitBox (points={self.points})"
