import arcade
from typing import Optional
from modules.ui.toolbox.hitbox import HitBox

"""Provides the base Entity class for spatial management and rendering."""


class Entity:
    """Manages an entity's spatial properties and rendering state."""

    def __init__(
        self,
        x: float = 0,
        y: float = 0,
        width: float = 10,
        height: float = 10,
        sprite: Optional[arcade.Sprite] = None,
        anchor: arcade.Vec2 = arcade.Vec2(0, 0),
    ):
        """Initializes the entity.

        Args:
            x: Horizontal position.
            y: Vertical position.
            width: Horizontal dimension.
            height: Vertical dimension.
            sprite: Optional visual representation.
            anchor: Vector defining the pivot point.
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
        """Synchronizes hitbox dimensions and position with the entity."""
        self.hitbox._x = self._x
        self.hitbox._y = self._y
        self.hitbox._width = self._width
        self.hitbox._height = self._height
        self.hitbox.anchor = self._anchor

    def draw(self) -> None:
        """Renders the entity using either a primitive shape or a sprite."""
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
        """Returns the current collision state from the hitbox."""
        return self.hitbox.touched
