import arcade
from typing import Tuple, Any

from modules.ui.toolbox.hitbox import HitBox
from modules.data import data

"""
Fournit une interface pour arcade.Text afin de gérer la disposition des éléments de l'interface utilisateur et leurs interactions.
"""


class Text:
    """
    Gère le rendu du texte, le positionnement, l'alignement et la détection de collision (hit detection).
    """

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        width: float = 10,
        height: float = 10,
        text: str = "Texte par défaut",
        align: Tuple[str, str] = ("center", "center"),
        size: int = 18,
        multiline: bool = False,
    ) -> None:
        """
        Initialise l'élément Text et ses propriétés de disposition.

        Args:
            x: Position horizontale.
            y: Position verticale.
            width: Contrainte horizontale pour la zone de texte.
            height: Contrainte verticale pour la zone de texte.
            text: Contenu de la chaîne de caractères affichée.
            align: Points d'ancrage pour l'alignement (horizontal, vertical).
            size: Taille de la police en pixels.
            multiline: Active le retour à la ligne automatique si True.
        """
        self._x: float = x
        self._y: float = y

        self._width: float = width
        self._height: float = height

        self._color: arcade.color = arcade.color.WHITE
        self.hitbox: HitBox = HitBox()

        self._name: str = text
        self._text: Any = ""

        self.grid_size: int = data.UI_EDITOR_GRID_SIZE

        self._size: int = size
        self._align: Tuple[str, str] = align
        self._multiline: bool = multiline

        self._recalculate_rect()

    @property
    def x(self) -> float:
        """Renvoie la coordonnée X actuelle."""
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        """Met à jour la coordonnée X et déclenche un recalcul de la disposition."""
        self._x = value
        self._recalculate_rect()

    @property
    def align(self) -> Tuple[str, str]:
        """Renvoie le tuple d'ancrage de l'alignement actuel."""
        return self._align

    @align.setter
    def align(self, value: Tuple[str, str]) -> None:
        """Met à jour les ancres d'alignement et déclenche un recalcul de la disposition."""
        self._align = value
        self._recalculate_rect()

    @property
    def y(self) -> float:
        """Renvoie la coordonnée Y actuelle."""
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        """Met à jour la coordonnée Y et déclenche un recalcul de la disposition."""
        self._y = value
        self._recalculate_rect()

    @property
    def width(self) -> float:
        """Renvoie la largeur actuelle de la boîte."""
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        """Met à jour la largeur et déclenche un recalcul de la disposition."""
        self._width = value
        self._recalculate_rect()

    @property
    def size(self) -> int:
        """Renvoie la taille actuelle de la police."""
        return self._size

    @size.setter
    def size(self, value: int) -> None:
        """Met à jour la taille de la police et déclenche un recalcul de la disposition."""
        self._size = value
        self._recalculate_rect()

    @property
    def height(self) -> float:
        """Renvoie la hauteur actuelle de la boîte."""
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        """Met à jour la hauteur et déclenche un recalcul de la disposition."""
        self._height = value
        self._recalculate_rect()

    @property
    def multiline(self) -> bool:
        """Indique si le support multiligne est activé."""
        return self._multiline

    @multiline.setter
    def multiline(self, value: bool) -> None:
        """Met à jour le paramètre multiligne et déclenche un recalcul de la disposition."""
        self._multiline = value
        self._recalculate_rect()

    def _recalculate_rect(self) -> None:
        """
        Met à jour l'instance interne arcade.Text et recalibre le
        rectangle de délimitation basé sur l'alignement actuel et la taille du contenu.
        """
        if self._multiline:
            self._text = arcade.Text(
                self._name,
                self._x,
                self._y,
                self._color,
                self._size,
                anchor_x=self._align[0],
                anchor_y=self._align[1],
                font_name="Press Start 2P",
                multiline=True,
                width=self._width,
            )
        else:
            self._text = arcade.Text(
                self._name,
                self._x,
                self._y,
                self._color,
                self._size,
                anchor_x=self._align[0],
                anchor_y=self._align[1],
                font_name="Press Start 2P",
                multiline=False,
            )

        if not self._multiline:
            self._width = self._text.content_width
        self._height = self._text.content_height

        # Calcul du décalage de l'ancre basé sur l'alignement horizontal
        if self._align[0] == "left":
            self.rect = arcade.XYWH(
                x=self._x,
                y=self._y + self._height / 2,
                width=self._width,
                height=self._height,
                anchor=arcade.Vec2(0, 1),
            )
        if self._align[0] == "center":
            self.rect = arcade.XYWH(
                x=self._x - self._width / 2,
                y=self._y + self._height / 2,
                width=self._width,
                height=self._height,
                anchor=arcade.Vec2(0, 1),
            )
        if self._align[0] == "right":
            self.rect = arcade.XYWH(
                x=self._x - self._width,
                y=self._y + self._height / 2,
                width=self._width,
                height=self._height,
                anchor=arcade.Vec2(0, 1),
            )

        self._update_hitbox()

    @property
    def text(self) -> str:
        """Renvoie le contenu textuel actuel."""
        return self._name

    @text.setter
    def text(self, value: str) -> None:
        """Met à jour le contenu textuel et déclenche un recalcul de la disposition."""
        self._name = value
        self._recalculate_rect()

    @property
    def color(self) -> arcade.color:
        """Renvoie la couleur actuelle du texte."""
        return self._color

    @color.setter
    def color(self, value: arcade.color) -> None:
        """Met à jour la couleur du texte et déclenche un recalcul de la disposition."""
        self._color = value
        self._recalculate_rect()

    def _update_hitbox(self) -> None:
        """Synchronise les limites de la HitBox interne avec le rectangle calculé."""
        self.hitbox.rect = self.rect

    def draw(self) -> None:
        """Effectue le rendu de l'élément texte."""
        self._text.draw()

    @property
    def touched(self) -> bool:
        """Indique si l'élément fait actuellement l'objet d'une interaction."""
        return self.hitbox.touched