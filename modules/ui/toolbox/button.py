"""Fournit une implémentation de bouton UI avec gestion géométrique et zones de collision (hitboxes) d'interaction."""

import arcade
from modules.ui.toolbox.hitbox import HitBox
from modules.data import data


class Button:
    """Représente un élément de bouton UI avec des fonctionnalités de positionnement, de dimensions et de zone de collision."""

    def __init__(self) -> None:
        """Initialise une nouvelle instance de bouton avec des propriétés physiques et visuelles par défaut."""
        self._x: float = 0.0
        self._y: float = 0.0

        self._width: float = 0.0
        self._height: float = 0.0

        self._color: arcade.color = arcade.color.BLUE
        self.hitbox: HitBox = HitBox()

        self._name: str = ""
        self._text: arcade.Text = None  # type: ignore

        self.grid_size: int = data.UI_EDITOR_GRID_SIZE

        self.scale: float = 1.0

        self._anchor: arcade.Vec2 = arcade.Vec2(0, 1)

    @property
    def x(self) -> float:
        """Retourne la position horizontale."""
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        """Définit la position horizontale et déclenche une mise à jour de la géométrie."""
        self._x = value
        self._recalculate_rect()

    @property
    def y(self) -> float:
        """Retourne la position verticale."""
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        """Définit la position verticale et déclenche une mise à jour de la géométrie."""
        self._y = value
        self._recalculate_rect()

    @property
    def width(self) -> float:
        """Retourne la largeur du bouton."""
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        """Définit la largeur du bouton et déclenche une mise à jour de la géométrie."""
        self._width = value
        self._recalculate_rect()

    @property
    def height(self) -> float:
        """Retourne la hauteur du bouton."""
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        """Définit la hauteur du bouton et déclenche une mise à jour de la géométrie."""
        self._height = value
        self._recalculate_rect()

    @property
    def anchor(self) -> arcade.Vec2:
        """Retourne le vecteur d'ancrage actuel."""
        return self._anchor

    @anchor.setter
    def anchor(self, value: arcade.Vec2) -> None:
        """Définit le vecteur d'ancrage et déclenche une mise à jour de la géométrie."""
        self._anchor = value
        self._recalculate_rect()

    def _recalculate_rect(self) -> None:
        """Met à jour le rectangle interne, synchronise la zone de collision et recrée le texte d'affichage."""
        self.rect = arcade.XYWH(
            x=self._x,
            y=self._y,
            width=self._width,
            height=self._height,
            anchor=self._anchor,
        )
        self._update_hitbox()

        self._text = arcade.Text(
            self._name,
            self._x,
            self._y,
            arcade.color.BLACK,
            18,
            anchor_x="center",
            anchor_y="center",
            font_name="Press Start 2P",
        )
        self._text.x = self._x + self._width / 2
        self._text.y = self._y - self._height / 2

    @property
    def name(self) -> str:
        """Retourne le nom de l'étiquette du bouton."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Définit le nom de l'étiquette du bouton et déclenche une mise à jour de la géométrie."""
        self._name = value
        self._recalculate_rect()

    @property
    def text(self) -> arcade.Text:
        """Retourne l'objet texte arcade sous-jacent."""
        return self._text

    @text.setter
    def text(self, value: arcade.Text) -> None:
        """Définit l'objet texte et déclenche une mise à jour de la géométrie."""
        self._text = value
        self._recalculate_rect()

    @property
    def color(self) -> arcade.color:
        """Retourne la couleur principale du bouton."""
        return self._color

    @color.setter
    def color(self, value: arcade.color) -> None:
        """Définit la couleur du bouton et déclenche une mise à jour de la géométrie."""
        self._color = value
        self._recalculate_rect()

    def _update_hitbox(self) -> None:
        """Aligne les dimensions et la position de la zone de collision avec les limites du bouton."""
        self.hitbox.x = self._x
        self.hitbox.y = self._y - self._height
        self.hitbox.width = self._width
        self.hitbox.height = self._height

    def draw(self) -> None:
        """Rendu du texte et de la zone de collision en fonction de l'échelle actuelle et des contraintes de la grille."""
        current_width = 10 * self.grid_size * self.scale
        current_height = 2 * self.grid_size * self.scale

        self.text.x = self.x + (current_width / 1.7)
        self.text.y = self.y - (
            (current_height / 2) + (self.grid_size * self.scale * 0.6)
        )

        self.text.font_size = 18 * self.scale

        self.text.draw()

    @property
    def touched(self) -> bool:
        """Retourne l'état d'interaction provenant de la zone de collision."""
        return self.hitbox.touched