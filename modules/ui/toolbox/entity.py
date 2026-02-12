import arcade
from modules.ui.toolbox.hitbox import HitBox
from modules.data import data

class Entity:

    def __init__(self,x=0,y=0,width=10,height=10,sprite=None,anchor=arcade.Vec2(0,0)):

        self._x = x
        self._y = y

        self._width = width
        self._height = height

        self.sprite = sprite

        self._anchor = anchor

        self.hitbox = HitBox()
        self._update_hitbox()

    @property
    def x(self):
        return self._x
    @x.setter
    def x(self, value):
        self._x = value
        self._update_hitbox()

    @property
    def y(self):
        return self._y
    @y.setter
    def y(self, value):
        self._y = value
        self._update_hitbox()

    @property
    def width(self):
        return self._width
    @width.setter
    def width(self, value):
        self._width = value
        self._update_hitbox()

    @property
    def height(self):
        return self._height
    @height.setter
    def height(self, value):
        self._height = value
        self._update_hitbox()

    def _update_hitbox(self):
        self.hitbox._x = self._x
        self.hitbox._y = self._y
        self.hitbox._width = self._width
        self.hitbox._height = self._height
        self.hitbox.anchor = self._anchor #Do the hitbox math only once.

    def draw(self):
        if self.sprite == None:
            arcade.draw_rect_filled(
                arcade.rect.XYWH(self._x, self._y, self._width, self._height,anchor=self._anchor),
                self.color,
            )
        else:
            arcade.draw_sprite_rect(
                self.sprite,
                arcade.rect.XYWH(self._x, self._y, self._width, self._height,anchor=self._anchor),
                
            )
        self.hitbox.draw()
    @property
    def touched(self):
        return self.hitbox.touched