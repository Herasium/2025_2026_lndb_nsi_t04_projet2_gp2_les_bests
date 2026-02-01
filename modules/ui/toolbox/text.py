import arcade

from modules.ui.toolbox.hitbox import HitBox
from modules.data import data

class Text:

    def __init__(self):

        self._x = 0
        self._y = 0

        self._width = 0
        self._height = 0

        self._color = arcade.color.WHITE
        self.hitbox = HitBox()

        self._name = ""
        self._text = ""

        self.grid_size = data.UI_EDITOR_GRID_SIZE

        self.scale = 1.0

        self._align =("center","center")


    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, value):
        self._x = value
        self._recalculate_rect()

    
    @property
    def align(self):
        return self._align
    
    @align.setter
    def align(self, value):
        self._align = value
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

    def _recalculate_rect(self):
        
        self._text = arcade.Text(
            self._name,
            self._x,
            self._y,
            self._color,
            18, 
            anchor_x = self._align[0],
            anchor_y = self._align[1],
            font_name = "Press Start 2P"
        )

        self._width = self._text.content_width
        self._height = self._text.content_height

        if self._align[0] == "left":
            self.rect = arcade.XYWH(
                x = self._x ,
                y = self._y + self._height/2,
                width = self._width,
                height = self._height,
                anchor = arcade.Vec2(0,1)
            )
        if self._align[0] == "center":
            self.rect = arcade.XYWH(
                x = self._x + self._width/2,
                y = self._y + self._height/2,
                width = self._width,
                height = self._height,
                anchor = arcade.Vec2(0,1)
            )
        if self._align[0] == "right":
            self.rect = arcade.XYWH(
                x = self._x + self._width,
                y = self._y + self._height/2,
                width = self._width,
                height = self._height,
                anchor = arcade.Vec2(0,1)
            )

 
        self._update_hitbox()




    @property
    def text(self):
        return self._name
    
    @text.setter
    def text(self, value):
        self._name = value
        self._recalculate_rect()

    @property
    def color(self):
        return self._color
    
    @color.setter
    def color(self, value):
        self._color = value
        self._recalculate_rect()
    
    def _update_hitbox(self):
        self.hitbox.rect = self.rect


    def draw(self):   
        self._text.draw()

    @property
    def touched(self):
        return self.hitbox.touched