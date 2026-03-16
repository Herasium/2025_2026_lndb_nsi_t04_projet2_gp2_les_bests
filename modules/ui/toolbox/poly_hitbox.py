import arcade
import arcade.geometry
from typing import List, Tuple, Dict, Any
from modules.ui.mouse import mouse


class PolyHitbox:
    """
    Represents a polygon-shaped hitbox for collision detection and rendering.
    """

    def __init__(self, points: List[Tuple[float, float]] = None) -> None:
        """
        Initialize the PolyHitbox with a list of coordinate points.

        Parameters:
        - points: A list of (x, y) tuples representing the polygon vertices.
        """
        # Default to an empty list if no points are provided
        self.points: List[Tuple[float, float]] = points if points is not None else []

    def draw(self) -> None:
        """
        Draws the outline of the polygon if it contains sufficient points.
        """
        # A polygon needs at least 2 points to draw an outline
        if len(self.points) > 1:
            arcade.draw_polygon_outline(self.points, arcade.color.ALLOY_ORANGE)

    def save(self) -> Dict[str, Any]:
        """
        Serializes the hitbox data into a dictionary for storage.

        Returns:
        - Dict: A dictionary containing the type and the list of points.
        """
        return {"type": "PolyHitbox", "points": self.points}

    @property
    def touched(self) -> bool:
        """
        Checks if the current mouse position is within the polygon boundaries.

        Returns:
        - bool: True if the mouse is inside the polygon, False otherwise.
        """
        # Get the current mouse coordinates from the imported module
        mouse_x: float
        mouse_y: float
        mouse_x, mouse_y = mouse.position

        # Use arcade's geometric utility to check point-in-polygon containment
        return arcade.geometry.is_point_in_polygon(
            x=mouse_x, y=mouse_y, polygon=self.points
        )

    def __repr__(self) -> str:
        """
        Returns a formal string representation of the object.
        """
        return f"PolyHitBox (points={self.points})"

    def __str__(self) -> str:
        """
        Returns a user-friendly string representation of the object.
        """
        return f"PolyHitBox (points={self.points})"
