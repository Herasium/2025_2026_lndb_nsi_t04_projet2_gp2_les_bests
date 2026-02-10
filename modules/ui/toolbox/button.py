import arcade
from modules.ui.toolbox.hitbox import HitBox
from modules.data import data


class Button:

    def __init__(self):

        self._x = 0
        self._y = 0

        self._width = 0
        self._height = 0

        self._color = arcade.color.BLUE
        self.hitbox = HitBox()

        self._name = ""
        self._text = ""

        self.grid_size = data.UI_EDITOR_GRID_SIZE

        self.scale = 1.0

        self._anchor = arcade.Vec2(0,1)


    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        self._recalculate_rect()

    @property
    def y(self):
        return self._y
    
    @y.setter
    def y(self, value):
        self._y = value
        self._recalculate_rect()    

    @property
    def width(self):
        return self._width
    
    @width.setter
    def width(self, value):
        self._width = value
        self._recalculate_rect()

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._height = value
        self._recalculate_rect()

    @property
    def anchor(self):
        return self.anchor
    
    @anchor.setter
    def anchor(self, value):
        self._anchor = value
        self._recalculate_rect()

    def _recalculate_rect(self):

        self.rect = arcade.XYWH(
            x = self._x,
            y = self._y,
            width = self._width,
            height = self._height,
            anchor = self._anchor
        )
        self._update_hitbox()
        
        self._text = arcade.Text(
            self._name,
            self._x,
            self._y,
            arcade.color.BLACK,
            18, 
            anchor_x = "center",
            anchor_y = "center",
            font_name = "Press Start 2P"
        )
        self.text.x = self.x + self.width /2
        self.text.y = self.y - self.height /2


    @property
    def name(self):
        return self._name
    
    @name.setter
    def name(self, value):
        self._name = value
        self._recalculate_rect()

    @property
    def text(self):
        return self._text
    
    @text.setter
    def text(self, value):
        self._text = value
        self._recalculate_rect()

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        self._color = value
        self._recalculate_rect()
    
    def _update_hitbox(self):
        self.hitbox.x = self._x
        self.hitbox.y = self._y-self._height
        self.hitbox.width = self._width
        self.hitbox.height = self._height

    def draw(self):
        # self.draw_tiles()
        current_width = 10 * self.grid_size * self.scale
        current_height = 2 * self.grid_size * self.scale
        
        self.text.x = self.x + (current_width / 1.7)
        self.text.y = self.y - ((current_height / 2) + (self.grid_size * self.scale * 0.6))
        
        self.text.font_size = 18 * self.scale

        self.text.draw()
        self.hitbox.draw()

    @property
    def touched(self):
        return self.hitbox.touched