import arcade
from typing import Optional
from modules.ui.toolbox.hitbox import HitBox


class Entity:
    """
    Represents a basic game entity with position, dimensions, and collision capabilities.
    """

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        width: float = 10,
        height: float = 10,
        sprite: Optional[arcade.Sprite] = None,
        anchor: arcade.Vec2 = arcade.Vec2(0, 0),
    ):
        """
        Initialize the Entity.

        Parameters:
        - x: Initial X-coordinate
        - y: Initial Y-coordinate
        - width: Entity width
        - height: Entity height
        - sprite: Optional arcade Sprite object
        - anchor: Vec2 object defining the anchor point
        """
        self._x: float = x
        self._y: float = y

        self._width: float = width
        self._height: float = height

        self.sprite: Optional[arcade.Sprite] = sprite

        self._anchor: arcade.Vec2 = anchor

        self.color: arcade.Color = arcade.color.ALLOY_ORANGE

        self.hitbox: HitBox = HitBox()
        self._update_hitbox()  # Sync hitbox with initial spatial properties

    @property
    def x(self) -> float:
        """Returns the current X-coordinate."""
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        """Sets the X-coordinate and updates the associated hitbox."""
        self._x = value
        self._update_hitbox()

    @property
    def y(self) -> float:
        """Returns the current Y-coordinate."""
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        """Sets the Y-coordinate and updates the associated hitbox."""
        self._y = value
        self._update_hitbox()

    @property
    def width(self) -> float:
        """Returns the entity width."""
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        """Sets the width and updates the associated hitbox."""
        self._width = value
        self._update_hitbox()

    @property
    def height(self) -> float:
        """Returns the entity height."""
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        """Sets the height and updates the associated hitbox."""
        self._height = value
        self._update_hitbox()

    def _update_hitbox(self) -> None:
        """
        Updates the internal hitbox properties based on the entity's spatial state.
        Synchronizes all dimensions and coordinates.
        """
        self.hitbox._x = self._x
        self.hitbox._y = self._y
        self.hitbox._width = self._width
        self.hitbox._height = self._height
        self.hitbox.anchor = self._anchor  # Do the hitbox math only once.

    def draw(self) -> None:
        """
        Draws the entity to the screen.
        Uses a rectangle if no sprite is provided, otherwise draws the sprite.
        """
        if self.sprite is None:
            # Draw a filled rectangle if no texture/sprite is present
            arcade.draw_rect_filled(
                arcade.rect.XYWH(
                    self._x, self._y, self._width, self._height, anchor=self._anchor
                ),
                self.color,
            )
        else:
            # Draw the assigned sprite using the entity's dimensions
            arcade.draw_sprite_rect(
                self.sprite,
                arcade.rect.XYWH(
                    self._x, self._y, self._width, self._height, anchor=self._anchor
                ),
                pixelated=True,
            )

    @property
    def touched(self) -> bool:
        """Returns the collision status from the internal hitbox."""
        return self.hitbox.touched
