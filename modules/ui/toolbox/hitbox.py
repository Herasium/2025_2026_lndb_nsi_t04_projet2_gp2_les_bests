"""Fournit une implémentation modulaire de hitbox pour la logique de collision et d'interaction."""

import arcade
from modules.ui.mouse import mouse


class HitBox:
    """Gère une zone rectangulaire pour la détection de collision et l'interaction UI.

    Attributes:
        rect (arcade.XYWH): La représentation interne du rectangle via arcade.
    """

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        width: float = 0,
        height: float = 0,
        anchor: arcade.Vec2 = arcade.Vec2(0, 0),
    ):
        """Initialise l'instance de HitBox.

        Args:
            x: Position horizontale.
            y: Position verticale.
            width: Étendue horizontale de la zone.
            height: Étendue verticale de la zone.
            anchor: Point d'ancrage pour les calculs de coordonnées.
        """
        self._x: float = x
        self._y: float = y
        self._width: float = width
        self._height: float = height
        self._anchor: arcade.Vec2 = anchor

        self._recalculate_rect()

    @property
    def x(self) -> float:
        """float: Coordonnée horizontale actuelle."""
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = value
        self._recalculate_rect()

    @property
    def y(self) -> float:
        """float: Coordonnée verticale actuelle."""
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = value
        self._recalculate_rect()

    @property
    def anchor(self) -> arcade.Vec2:
        """arcade.Vec2: Point d'ancrage actuel."""
        return self._anchor

    @anchor.setter
    def anchor(self, value: arcade.Vec2) -> None:
        self._anchor = value
        self._recalculate_rect()

    @property
    def width(self) -> float:
        """float: Largeur de la zone."""
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        self._width = value
        self._recalculate_rect()

    @property
    def height(self) -> float:
        """float: Hauteur de la zone."""
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        self._height = value
        self._recalculate_rect()

    def _recalculate_rect(self) -> None:
        """Synchronise la géométrie interne du rectangle avec les attributs actuels de la hitbox."""
        self.rect: arcade.XYWH = arcade.XYWH(
            x=self._x,
            y=self._y,
            width=self._width,
            height=self._height,
            anchor=self._anchor,
        )

    def draw(self) -> None:
        """Affiche les limites de la hitbox avec un retour visuel pour l'état de survol."""
        color = arcade.color.ALLOY_ORANGE
        if self.touched:
            color = arcade.color.RED
        arcade.draw_rect_outline(self.rect, color)

    @property
    def touched(self) -> bool:
        """bool: Indique si la position actuelle de la souris intersecte la hitbox."""
        return self.rect.point_in_rect(point=mouse.position)

    def __repr__(self) -> str:
        """Retourne l'état interne pour le débogage."""
        return (
            f"HitBox(x={self._x}, y={self._y}, "
            f"width={self._width}, height={self._height})"
        )

    def __str__(self) -> str:
        """Retourne un résumé textuel de la hitbox destiné à l'utilisateur."""
        return (
            f"HitBox à ({self._x}, {self._y}) " f"taille=({self._width}×{self._height})"
        )