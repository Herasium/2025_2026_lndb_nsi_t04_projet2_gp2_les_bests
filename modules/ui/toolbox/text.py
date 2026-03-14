import arcade

from modules.ui.toolbox.hitbox import HitBox
from modules.data import data

class Text:

    def __init__(self,x=0,y=0,width=10,height=10,text="Default Text",align = ("center","center"),size = 18,multiline=False):

        self._x = x
        self._y = y

        self._width = width
        self._height = height

        self._color = arcade.color.WHITE
        self.hitbox = HitBox()

        self._name = text
        self._text = ""

        self.grid_size = data.UI_EDITOR_GRID_SIZE

        self._size = size
        self._align =align
        self._multiline = multiline

        self._recalculate_rect()


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
    def size(self):
        return self._size
    
    @size.setter
    def size(self, value):
        self._size = value
        self._recalculate_rect()

    @property
    def height(self):
        return self._height
    
    @height.setter
    def height(self, value):
        self._height = value
        self._recalculate_rect()

    @property
    def multiline(self):
        return self._multiline
    
    @multiline.setter
    def multiline(self, value):
        self._multiline = value
        self._recalculate_rect()

    def _recalculate_rect(self):
        
        if self._multiline:
            self._text = arcade.Text(
                self._name,
                self._x,
                self._y,
                self._color,
                self._size, 
                anchor_x = self._align[0],
                anchor_y = self._align[1],
                font_name = "Press Start 2P",
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
                anchor_x = self._align[0],
                anchor_y = self._align[1],
                font_name = "Press Start 2P",
                multiline=False,
            )
        
        if not self._multiline:
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