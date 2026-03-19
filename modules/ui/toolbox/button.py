"""Provides a UI button implementation with geometric management and interaction hitboxes."""

import arcade
from modules.ui.toolbox.hitbox import HitBox
from modules.data import data


class Button:
    """Represents a UI button element with positioning, dimensions, and hitbox functionality."""

    def __init__(self) -> None:
        """Initializes a new button instance with default physical and visual properties."""
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
        """Returns the horizontal position."""
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        """Sets the horizontal position and triggers a geometry update."""
        self._x = value
        self._recalculate_rect()

    @property
    def y(self) -> float:
        """Returns the vertical position."""
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        """Sets the vertical position and triggers a geometry update."""
        self._y = value
        self._recalculate_rect()

    @property
    def width(self) -> float:
        """Returns the button width."""
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        """Sets the button width and triggers a geometry update."""
        self._width = value
        self._recalculate_rect()

    @property
    def height(self) -> float:
        """Returns the button height."""
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        """Sets the button height and triggers a geometry update."""
        self._height = value
        self._recalculate_rect()

    @property
    def anchor(self) -> arcade.Vec2:
        """Returns the current anchor vector."""
        return self._anchor

    @anchor.setter
    def anchor(self, value: arcade.Vec2) -> None:
        """Sets the anchor vector and triggers a geometry update."""
        self._anchor = value
        self._recalculate_rect()

    def _recalculate_rect(self) -> None:
        """Updates the internal rectangle, syncs the hitbox, and recreates the display text."""
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
        """Returns the button label name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Sets the button label name and triggers a geometry update."""
        self._name = value
        self._recalculate_rect()

    @property
    def text(self) -> arcade.Text:
        """Returns the underlying arcade text object."""
        return self._text

    @text.setter
    def text(self, value: arcade.Text) -> None:
        """Sets the text object and triggers a geometry update."""
        self._text = value
        self._recalculate_rect()

    @property
    def color(self) -> arcade.color:
        """Returns the primary button color."""
        return self._color

    @color.setter
    def color(self, value: arcade.color) -> None:
        """Sets the button color and triggers a geometry update."""
        self._color = value
        self._recalculate_rect()

    def _update_hitbox(self) -> None:
        """Aligns the interaction hitbox dimensions and position with the button's bounds."""
        self.hitbox.x = self._x
        self.hitbox.y = self._y - self._height
        self.hitbox.width = self._width
        self.hitbox.height = self._height

    def draw(self) -> None:
        """Renders the text and hitbox based on current scaling and grid constraints."""
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
        """Returns the interaction state from the hitbox."""
        return self.hitbox.touched
