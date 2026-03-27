import arcade
from typing import Optional
from modules.ui.toolbox.hitbox import HitBox

"""Fournit la classe de base Entity pour la gestion spatiale et le rendu."""


class Entity:
    """Gère les propriétés spatiales et l'état de rendu d'une entité."""

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        width: float = 10,
        height: float = 10,
        sprite: Optional[arcade.Sprite] = None,
        anchor: arcade.Vec2 = arcade.Vec2(0, 0),
    ):
        """Initialise l'entité.

        Args:
            x: Position horizontale.
            y: Position verticale.
            width: Dimension horizontale.
            height: Dimension verticale.
            sprite: Représentation visuelle optionnelle.
            anchor: Vecteur définissant le point de pivot.
        """
        self._x: float = x
        self._y: float = y

        self._width: float = width
        self._height: float = height

        self.sprite: Optional[arcade.Sprite] = sprite

        self._anchor: arcade.Vec2 = anchor

        self.color: arcade.Color = arcade.color.ALLOY_ORANGE

        self.hitbox: HitBox = HitBox()
        self._update_hitbox()

    @property
    def x(self) -> float:
        """Retourne la coordonnée X actuelle."""
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        """Définit la coordonnée X et met à jour la hitbox associée."""
        self._x = value
        self._update_hitbox()

    @property
    def y(self) -> float:
        """Retourne la coordonnée Y actuelle."""
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        """Définit la coordonnée Y et met à jour la hitbox associée."""
        self._y = value
        self._update_hitbox()

    @property
    def width(self) -> float:
        """Retourne la largeur de l'entité."""
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        """Définit la largeur et met à jour la hitbox associée."""
        self._width = value
        self._update_hitbox()

    @property
    def height(self) -> float:
        """Retourne la hauteur de l'entité."""
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        """Définit la hauteur et met à jour la hitbox associée."""
        self._height = value
        self._update_hitbox()

    def _update_hitbox(self) -> None:
        """Synchronise les dimensions et la position de la hitbox avec l'entité."""
        self.hitbox._x = self._x
        self.hitbox._y = self._y
        self.hitbox._width = self._width
        self.hitbox._height = self._height
        self.hitbox.anchor = self._anchor

    def draw(self) -> None:
        """Rendu de l'entité en utilisant soit une forme primitive, soit un sprite."""
        if self.sprite is None:
            arcade.draw_rect_filled(
                arcade.rect.XYWH(
                    self._x, self._y, self._width, self._height, anchor=self._anchor
                ),
                self.color,
            )
        else:
            arcade.draw_sprite_rect(
                self.sprite,
                arcade.rect.XYWH(
                    self._x, self._y, self._width, self._height, anchor=self._anchor
                ),
                pixelated=True,
            )

    @property
    def touched(self) -> bool:
        """Retourne l'état de collision actuel de la hitbox."""
        return self.hitbox.touched