import arcade

from modules.ui.mouse import mouse
from modules.ui.toolbox.button import Button
from modules.ui.toolbox.text import Text
from modules.ui.debug_display_all_tiles.view import DebugTilesView

from modules.data.nodes.path import Path

from modules.data import data

import sys


class TutorialView(arcade.View):

    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.JET

        self.name_banner_sprite = data.name_banner

        self.back_button = Button()
        self.back_button.x = 192 / 2.5 - 30
        self.back_button.y = 1010 + 10
        self.back_button.width = 80
        self.back_button.height = 40

        self.regletexte = Text(x=120, y=820, text=data.language.tutorial["title_1"], align=("left", "center"))
        self.listeportetexte = Text(x=120, y=520, text=data.language.tutorial["title_2"], align=("left", "center"))

        self.regleplay_button = Text(x=160, y=740, text=data.language.tutorial["button_1"], align=("left", "center"), size=16)
        self.commande_button = Text(x=160, y=685, text=data.language.tutorial["button_2"], align=("left", "center"), size=16)

        self.namebutton = ["button_3", "button_4", "button_5", "button_6", "button_7", "button_8", "button_9", "button_10", "button_11", "button_12"]
        self.buttons = []

        a = 485
        for i in self.namebutton :
            a = a - 45
            self.buttons.append(Text(x=160, y=a, text=data.language.tutorial[i], align=("left", "center"), size=16))

        self.texte_button = Text()


    def on_key_press(self, key, key_modifiers):
        if key == 97: #"a"
            arcade.exit()

    def draw_tile(self,id,x,y):
        rect = arcade.XYWH(
            x=x,
            y=y,
            width=64,
            height=64,
            anchor=arcade.Vec2(0,0)
        )

        arcade.draw_texture_rect(data.ui_border_tiles[id],rect)

    def draw_frame_border(self):
        start_x = 32
        start_y = 865
        y_len = 13
        x_len = 28

        self.draw_tile(0,start_x,start_y)
        for i in range(x_len-1):
            self.draw_tile(1,start_x + (i+1)*64,start_y)
        self.draw_tile(3,start_x+x_len*64,start_y)

        for i in range(y_len-1):
            self.draw_tile(4,start_x,start_y - (i+1)*64)
            self.draw_tile(7,start_x+x_len*64,start_y - (i+1)*64)


        self.draw_tile(12,start_x,start_y - y_len*64)
        self.draw_tile(13,start_x + 64,start_y- y_len*64)
        self.draw_tile(5,start_x + 2*64,start_y- y_len*64)
        self.draw_tile(6,start_x + 3*64,start_y- y_len*64)
        self.draw_tile(10,start_x + 4*64,start_y- y_len*64)
        for i in range(x_len-5):
            self.draw_tile(13,start_x + (i+5)*64,start_y- y_len*64)
        self.draw_tile(15,start_x+x_len*64,start_y- y_len*64)

    def draw_frame_background(self):

        start_x = 32
        start_y = 865+64
        y_len = 15

        for i in range(y_len-1):
            for a in range(29):
                self.draw_tile(9,start_x + (a)*64,start_y- (i+1)*64)

    def on_draw(self):
        self.clear(arcade.color.BLACK)

        self.draw_frame_background()
        self.draw_frame_border()

        self.texte_button.draw()
        self.back_button.draw()

        self.regletexte.draw()
        self.listeportetexte.draw()

        self.regleplay_button.draw()
        self.commande_button.draw()
       
        for i in self.buttons :
           i.draw()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        mouse.position = (x,y)

    def on_mouse_press(self, x, y, button, key_modifiers):
        if self.back_button.touched :
            data.window.back()

        if self.regleplay_button.touched :
            self.texte_button = Text(x=300, y=820, text=data.language.tutorial["button_01"], align=("left", "center"))
        
        if self.commande_button.touched : 
            self.texte_button = Text(x=300, y=820, text=data.language.tutorial["button_02"], align=("left", "center"))

        for i in self.buttons :
            if self.buttons[i].touched :
                pass
