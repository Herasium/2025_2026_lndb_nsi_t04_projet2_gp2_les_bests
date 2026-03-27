import arcade
import arcade.geometry
from typing import List, Tuple, Dict, Any
from modules.ui.mouse import mouse

"""Fournit la logique de détection de collision et de rendu pour les zones de collision (hitboxes) basées sur des polygones."""


class PolyHitbox:
    """Gère les limites de collision basées sur des sommets et le rendu associé."""

    def __init__(self, points: List[Tuple[float, float]] = None) -> None:
        """Initialise une zone de collision polygonale.

        Args:
            points: Sommets définis comme des paires de coordonnées formant le périmètre du polygone.
        """
        self.points: List[Tuple[float, float]] = points if points is not None else []

    def draw(self) -> None:
        """Affiche le contour du polygone à l'écran."""
        if len(self.points) > 1:
            arcade.draw_polygon_outline(self.points, arcade.color.ALLOY_ORANGE)

    def save(self) -> Dict[str, Any]:
        """Sérialise les données de la zone de collision pour la persistance.

        Returns:
            Un dictionnaire contenant l'identifiant et la collection de sommets.
        """
        return {"type": "PolyHitbox", "points": self.points}

    @property
    def touched(self) -> bool:
        """Détermine si le curseur de la souris chevauche la zone du polygone.

        Returns:
            True si les coordonnées de la souris intersectent la géométrie du polygone.
        """
        mouse_x: float
        mouse_y: float
        mouse_x, mouse_y = mouse.position

        return arcade.geometry.is_point_in_polygon(
            x=mouse_x, y=mouse_y, polygon=self.points
        )

    def __repr__(self) -> str:
        """Retourne la représentation formelle de la zone de collision destinée au développeur."""
        return f"PolyHitBox (points={self.points})"

    def __str__(self) -> str:
        """Retourne la représentation informelle de la zone de collision destinée à l'utilisateur."""
        return f"PolyHitBox (points={self.points})"