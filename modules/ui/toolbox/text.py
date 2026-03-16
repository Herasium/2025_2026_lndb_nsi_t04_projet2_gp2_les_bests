import arcade
from typing import Tuple, Any

from modules.ui.toolbox.hitbox import HitBox
from modules.data import data


class Text:
    """
    A wrapper class for arcade.Text to handle positioning, alignment,
    and hitboxes for UI text elements.
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
        Initialize the Text object and set initial properties.

        Parameters:
        - x: X-coordinate of the text
        - y: Y-coordinate of the text
        - width: Width of the text box
        - height: Height of the text box
        - text: The string content to display
        - align: Tuple defining (anchor_x, anchor_y)
        - size: Font size
        - multiline: Boolean flag for multiline support
        """
        self._x: float = x
        self._y: float = y

        self._width: float = width
        self._height: float = height

        self._color: arcade.Color = arcade.color.WHITE
        self.hitbox: HitBox = HitBox()

        self._name: str = text
        self._text: Any = ""  # Will hold the arcade.Text instance

        self.grid_size: int = data.UI_EDITOR_GRID_SIZE

        self._size: int = size
        self._align: Tuple[str, str] = align
        self._multiline: bool = multiline

        self._recalculate_rect()  # Initialize the layout logic

    @property
    def x(self) -> float:
        """Get the current X-coordinate."""
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        """Set X-coordinate and refresh layout."""
        self._x = value
        self._recalculate_rect()

    @property
    def align(self) -> Tuple[str, str]:
        """Get the alignment tuple."""
        return self._align

    @align.setter
    def align(self, value: Tuple[str, str]) -> None:
        """Set alignment and refresh layout."""
        self._align = value
        self._recalculate_rect()

    @property
    def y(self) -> float:
        """Get the current Y-coordinate."""
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        """Set Y-coordinate and refresh layout."""
        self._y = value
        self._recalculate_rect()

    @property
    def width(self) -> float:
        """Get the current width."""
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        """Set width and refresh layout."""
        self._width = value
        self._recalculate_rect()

    @property
    def size(self) -> int:
        """Get the current font size."""
        return self._size

    @size.setter
    def size(self, value: int) -> None:
        """Set font size and refresh layout."""
        self._size = value
        self._recalculate_rect()

    @property
    def height(self) -> float:
        """Get the current height."""
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        """Set height and refresh layout."""
        self._height = value
        self._recalculate_rect()

    @property
    def multiline(self) -> bool:
        """Check if multiline mode is enabled."""
        return self._multiline

    @multiline.setter
    def multiline(self, value: bool) -> None:
        """Set multiline mode and refresh layout."""
        self._multiline = value
        self._recalculate_rect()

    def _recalculate_rect(self) -> None:
        """
        Internal helper to update the underlying arcade.Text object
        and calculate the hit detection box based on alignment.
        """
        # Configure arcade text instance based on multiline setting
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

        # Adjust dimensions based on text content
        if not self._multiline:
            self._width = self._text.content_width
        self._height = self._text.content_height

        # Calculate bounding box (rect) based on anchor alignment
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
        """Get the text content."""
        return self._name

    @text.setter
    def text(self, value: str) -> None:
        """Set text content and refresh layout."""
        self._name = value
        self._recalculate_rect()

    @property
    def color(self) -> arcade.Color:
        """Get the text color."""
        return self._color

    @color.setter
    def color(self, value: arcade.Color) -> None:
        """Set text color and refresh layout."""
        self._color = value
        self._recalculate_rect()

    def _update_hitbox(self) -> None:
        """Sync the internal hitbox with the calculated rectangle."""
        self.hitbox.rect = self.rect

    def draw(self) -> None:
        """Render the text to the screen."""
        self._text.draw()

    @property
    def touched(self) -> bool:
        """Return True if the text element is being interacted with."""
        return self.hitbox.touched
