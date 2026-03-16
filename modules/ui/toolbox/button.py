import arcade
from modules.ui.toolbox.hitbox import HitBox
from modules.data import data


class Button:
    """
    Represents a UI button element with positioning, dimensions, and hitbox functionality.
    """

    def __init__(self) -> None:
        """Initialize the Button with default properties."""
        self._x: float = 0.0
        self._y: float = 0.0

        self._width: float = 0.0
        self._height: float = 0.0

        self._color: arcade.Color = arcade.color.BLUE
        self.hitbox: HitBox = HitBox()

        self._name: str = ""
        self._text: arcade.Text = None  # type: ignore

        self.grid_size: int = data.UI_EDITOR_GRID_SIZE

        self.scale: float = 1.0

        self._anchor: arcade.Vec2 = arcade.Vec2(0, 1)

    @property
    def x(self) -> float:
        """Get the x-coordinate."""
        return self._x

    @x.setter
    def x(self, value: float) -> None:
        """Set the x-coordinate and update geometry."""
        self._x = value
        self._recalculate_rect()

    @property
    def y(self) -> float:
        """Get the y-coordinate."""
        return self._y

    @y.setter
    def y(self, value: float) -> None:
        """Set the y-coordinate and update geometry."""
        self._y = value
        self._recalculate_rect()

    @property
    def width(self) -> float:
        """Get the width."""
        return self._width

    @width.setter
    def width(self, value: float) -> None:
        """Set the width and update geometry."""
        self._width = value
        self._recalculate_rect()

    @property
    def height(self) -> float:
        """Get the height."""
        return self._height

    @height.setter
    def height(self, value: float) -> None:
        """Set the height and update geometry."""
        self._height = value
        self._recalculate_rect()

    @property
    def anchor(self) -> arcade.Vec2:
        """Get the current anchor vector."""
        return self._anchor

    @anchor.setter
    def anchor(self, value: arcade.Vec2) -> None:
        """Set the anchor and update geometry."""
        self._anchor = value
        self._recalculate_rect()

    def _recalculate_rect(self) -> None:
        """Recalculate the internal XYWH rectangle, hitbox, and text element."""
        self.rect = arcade.XYWH(
            x=self._x,
            y=self._y,
            width=self._width,
            height=self._height,
            anchor=self._anchor,
        )
        self._update_hitbox()  # Sync hitbox dimensions

        # Create text instance for display
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
        # Position text relative to button center
        self._text.x = self._x + self._width / 2
        self._text.y = self._y - self._height / 2

    @property
    def name(self) -> str:
        """Get the button name."""
        return self._name

    @name.setter
    def name(self, value: str) -> None:
        """Set the name and trigger geometry update."""
        self._name = value
        self._recalculate_rect()

    @property
    def text(self) -> arcade.Text:
        """Get the text object."""
        return self._text

    @text.setter
    def text(self, value: arcade.Text) -> None:
        """Set the text object and trigger geometry update."""
        self._text = value
        self._recalculate_rect()

    @property
    def color(self) -> arcade.Color:
        """Get the button color."""
        return self._color

    @color.setter
    def color(self, value: arcade.Color) -> None:
        """Set the button color and trigger geometry update."""
        self._color = value
        self._recalculate_rect()

    def _update_hitbox(self) -> None:
        """Sync internal hitbox properties with current button dimensions."""
        self.hitbox.x = self._x
        self.hitbox.y = self._y - self._height
        self.hitbox.width = self._width
        self.hitbox.height = self._height

    def draw(self) -> None:
        """Draw the button text and its associated hitbox."""
        current_width = 10 * self.grid_size * self.scale
        current_height = 2 * self.grid_size * self.scale

        # Adjust text position based on current scale and grid size
        self.text.x = self.x + (current_width / 1.7)
        self.text.y = self.y - (
            (current_height / 2) + (self.grid_size * self.scale * 0.6)
        )

        # Scale text size dynamically
        self.text.font_size = 18 * self.scale

        self.text.draw()
        self.hitbox.draw()

    @property
    def touched(self) -> bool:
        """Check if the button hitbox is currently being touched/interacted with."""
        return self.hitbox.touched
