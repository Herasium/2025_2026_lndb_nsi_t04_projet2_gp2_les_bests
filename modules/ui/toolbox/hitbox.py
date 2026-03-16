"""Provides a modular hitbox implementation for collision and interaction logic."""

import arcade
from modules.ui.mouse import mouse


class HitBox:
    """Manages a rectangular boundary for collision detection and UI interaction.

    Attributes:
        rect (arcade.XYWH): The internal arcade representation of the rectangle.
    """

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        width: float = 0,
        height: float = 0,
        anchor: arcade.Vec2 = arcade.Vec2(0, 0),
    ):
        """Initializes the HitBox instance.

        Args:
            x: Horizontal position.
            y: Vertical position.
            width: Horizontal span of the boundary.
            height: Vertical span of the boundary.
            anchor: Origin point for coordinate calculations.
        """
        self._x: float = x
        self._y: float = y
        self._width: float = width
        self._height: float = height
        self._anchor: arcade.Vec2 = anchor

        self._recalculate_rect()

    @property
    def x(self) -> float:
        """float: Current horizontal coordinate."""
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        self._x = value
        self._recalculate_rect()

    @property
    def y(self) -> float:
        """float: Current vertical coordinate."""
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        self._y = value
        self._recalculate_rect()

    @property
    def anchor(self) -> arcade.Vec2:
        """arcade.Vec2: Current anchor point."""
        return self._anchor

    @anchor.setter
    def anchor(self, value: arcade.Vec2) -> None:
        self._anchor = value
        self._recalculate_rect()

    @property
    def width(self) -> float:
        """float: Width of the boundary."""
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        self._width = value
        self._recalculate_rect()

    @property
    def height(self) -> float:
        """float: Height of the boundary."""
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        self._height = value
        self._recalculate_rect()

    def _recalculate_rect(self) -> None:
        """Synchronizes internal rectangle geometry with current hitbox attributes."""
        self.rect: arcade.XYWH = arcade.XYWH(
            x=self._x,
            y=self._y,
            width=self._width,
            height=self._height,
            anchor=self._anchor,
        )

    def draw(self) -> None:
        """Renders the hitbox boundary with visual feedback for hover states."""
        color = arcade.color.ALLOY_ORANGE
        if self.touched:
            color = arcade.color.RED
        arcade.draw_rect_outline(self.rect, color)

    @property
    def touched(self) -> bool:
        """bool: Indicates if the current mouse position intersects the hitbox."""
        return self.rect.point_in_rect(point=mouse.position)

    def __repr__(self) -> str:
        """Returns the internal state for debugging."""
        return (
            f"HitBox(x={self._x}, y={self._y}, "
            f"width={self._width}, height={self._height})"
        )

    def __str__(self) -> str:
        """Returns a user-facing string summary of the hitbox."""
        return (
            f"HitBox at ({self._x}, {self._y}) " f"size=({self._width}×{self._height})"
        )
