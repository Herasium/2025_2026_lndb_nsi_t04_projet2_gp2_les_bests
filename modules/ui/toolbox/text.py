import arcade
from typing import Tuple, Any

from modules.ui.toolbox.hitbox import HitBox
from modules.data import data

"""
Provides a wrapper for arcade.Text to manage UI element layout and interactions.
"""


class Text:
    """
    Manages text rendering, positioning, alignment, and hit detection.
    """

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        width: float = 10,
        height: float = 10,
        text: str = "Default Text",
        align: Tuple[str, str] = ("center", "center"),
        size: int = 18,
        multiline: bool = False,
    ) -> None:
        """
        Initializes the Text element and its layout properties.

        Args:
            x: Horizontal position.
            y: Vertical position.
            width: Horizontal constraint for the text box.
            height: Vertical constraint for the text box.
            text: Displayed string content.
            align: Anchor points for (horizontal, vertical) alignment.
            size: Font size in pixels.
            multiline: Enables automatic line wrapping if True.
        """
        self._x: float = x
        self._y: float = y

        self._width: float = width
        self._height: float = height

        self._color: arcade.Color = arcade.color.WHITE
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
        """Returns the current X-coordinate."""
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        """Updates X-coordinate and triggers layout recalculation."""
        self._x = value
        self._recalculate_rect()

    @property
    def align(self) -> Tuple[str, str]:
        """Returns the current alignment anchor tuple."""
        return self._align

    @align.setter
    def align(self, value: Tuple[str, str]) -> None:
        """Updates alignment anchors and triggers layout recalculation."""
        self._align = value
        self._recalculate_rect()

    @property
    def y(self) -> float:
        """Returns the current Y-coordinate."""
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        """Updates Y-coordinate and triggers layout recalculation."""
        self._y = value
        self._recalculate_rect()

    @property
    def width(self) -> float:
        """Returns the current box width."""
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        """Updates width and triggers layout recalculation."""
        self._width = value
        self._recalculate_rect()

    @property
    def size(self) -> int:
        """Returns the current font size."""
        return self._size

    @size.setter
    def size(self, value: int) -> None:
        """Updates font size and triggers layout recalculation."""
        self._size = value
        self._recalculate_rect()

    @property
    def height(self) -> float:
        """Returns the current box height."""
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        """Updates height and triggers layout recalculation."""
        self._height = value
        self._recalculate_rect()

    @property
    def multiline(self) -> bool:
        """Returns whether multiline support is enabled."""
        return self._multiline

    @multiline.setter
    def multiline(self, value: bool) -> None:
        """Updates multiline setting and triggers layout recalculation."""
        self._multiline = value
        self._recalculate_rect()

    def _recalculate_rect(self) -> None:
        """
        Updates the internal arcade.Text instance and recalibrates the
        bounding rectangle based on current alignment and content size.
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

        # Offset anchor calculation based on horizontal alignment
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
                x=self._x + self._width / 2,
                y=self._y + self._height / 2,
                width=self._width,
                height=self._height,
                anchor=arcade.Vec2(0, 1),
            )
        if self._align[0] == "right":
            self.rect = arcade.XYWH(
                x=self._x + self._width,
                y=self._y + self._height / 2,
                width=self._width,
                height=self._height,
                anchor=arcade.Vec2(0, 1),
            )

        self._update_hitbox()

    @property
    def text(self) -> str:
        """Returns the current string content."""
        return self._name

    @text.setter
    def text(self, value: str) -> None:
        """Updates string content and triggers layout recalculation."""
        self._name = value
        self._recalculate_rect()

    @property
    def color(self) -> arcade.Color:
        """Returns the current text color."""
        return self._color

    @color.setter
    def color(self, value: arcade.Color) -> None:
        """Updates text color and triggers layout recalculation."""
        self._color = value
        self._recalculate_rect()

    def _update_hitbox(self) -> None:
        """Syncs the internal HitBox bounds with the calculated rectangle."""
        self.hitbox.rect = self.rect

    def draw(self) -> None:
        """Renders the text element."""
        self._text.draw()

    @property
    def touched(self) -> bool:
        """Returns whether the element is currently under interaction."""
        return self.hitbox.touched
