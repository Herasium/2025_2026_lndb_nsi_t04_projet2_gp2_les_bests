import arcade
from modules.ui.mouse import mouse


class HitBox:
    """Represents a rectangular hit-box used for collision detection and UI interaction."""

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        width: float = 0,
        height: float = 0,
        anchor: arcade.Vec2 = arcade.Vec2(0, 0),
    ):
        """Initialize the HitBox instance.

        Parameters:
        - x: Horizontal coordinate
        - y: Vertical coordinate
        - width: Width of the hitbox
        - height: Height of the hitbox
        - anchor: Vec2 object defining the anchor point
        """
        self._x: float = x
        self._y: float = y
        self._width: float = width
        self._height: float = height
        self._anchor: arcade.Vec2 = anchor

        self._recalculate_rect()  # Ensure the internal rectangle is initialized

    @property
    def x(self) -> float:
        """Return the current x coordinate."""
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        """Set the x coordinate and update the rectangle."""
        self._x = value
        self._recalculate_rect()

    @property
    def y(self) -> float:
        """Return the current y coordinate."""
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        """Set the y coordinate and update the rectangle."""
        self._y = value
        self._recalculate_rect()

    @property
    def anchor(self) -> arcade.Vec2:
        """Return the current anchor position."""
        return self._anchor

    @anchor.setter
    def anchor(self, value: arcade.Vec2) -> None:
        """Set the anchor position and update the rectangle."""
        self._anchor = value
        self._recalculate_rect()

    @property
    def width(self) -> float:
        """Return the width of the hitbox."""
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        """Set the width and update the rectangle."""
        self._width = value
        self._recalculate_rect()

    @property
    def height(self) -> float:
        """Return the height of the hitbox."""
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        """Set the height and update the rectangle."""
        self._height = value
        self._recalculate_rect()

    def _recalculate_rect(self) -> None:
        """Update the underlying arcade.XYWH rectangle based on current properties."""
        self.rect: arcade.XYWH = arcade.XYWH(
            x=self._x,
            y=self._y,
            width=self._width,
            height=self._height,
            anchor=self._anchor,
        )

    def draw(self) -> None:
        """Draw the outline of the hitbox; color changes if the mouse is hovering."""
        color = arcade.color.ALLOY_ORANGE
        if self.touched:  # Check if mouse currently overlaps hitbox
            color = arcade.color.RED
        arcade.draw_rect_outline(self.rect, color)

    @property
    def touched(self) -> bool:
        """Determine if the mouse cursor is currently inside the hitbox."""
        return self.rect.point_in_rect(point=mouse.position)

    def __repr__(self) -> str:
        """Return a developer-readable string representation of the object."""
        return (
            f"HitBox(x={self._x}, y={self._y}, "
            f"width={self._width}, height={self._height})"
        )

    def __str__(self) -> str:
        """Return a user-friendly string representation of the object."""
        return (
            f"HitBox at ({self._x}, {self._y}) " f"size=({self._width}×{self._height})"
        )
