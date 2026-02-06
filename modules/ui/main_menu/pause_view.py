import arcade

from modules.ui.mouse import mouse
from modules.ui.toolbox.button import Button
from modules.ui.debug_display_all_tiles.view import DebugTilesView
from modules.ui.main_menu.settings_view import SettingView


from modules.data.nodes.path import Path

from modules.data import data

from pyglet.graphics import Batch
import sys


class PauseView(arcade.View):

    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.JET

        self.ui_border_sheet = arcade.SpriteSheet("assets/ui_border_grid.png")
        self.name_banner_sprite = arcade.Sprite("assets/name_banner.png")

        self.ui_border_tiles = self.ui_border_sheet.get_texture_grid(
            size = (64, 64),
            columns = 4,
            count = 4*4,
        )

        self.ui_sheet = arcade.SpriteSheet("assets/ui_grid.png")

        self.ui_tiles = self.ui_sheet.get_texture_grid(
            size = (32, 32),
            columns = 23,
            count = 9*23,
        )

        self.back_button = Button(self.ui_tiles)
        self.back_button.x = 700
        self.back_button.y = 800 - 25
        self.back_button.width = 520
        self.back_button.height = 100

        self.settings_button = Button(self.ui_tiles)
        self.settings_button.x = 700
        self.settings_button.y = 575 - 25
        self.settings_button.width = 520
        self.settings_button.height = 100

        self.quitter_button = Button(self.ui_tiles)
        self.quitter_button.x = 700
        self.quitter_button.y = 350 - 25
        self.quitter_button.width = 520
        self.quitter_button.height = 100


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

        arcade.draw_texture_rect(self.ui_border_tiles[id],rect)

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

       rect = arcade.XYWH(
                x=0,
                y=1080-128,
                width=1920,
                height=128,
                anchor=arcade.Vec2(0,0)
        )

       arcade.draw_sprite_rect(self.name_banner_sprite,rect)

       self.back_button.draw()
       self.settings_button.draw()
       self.quitter_button.draw()

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        mouse.position = (x,y)

    def on_mouse_press(self, x, y, button, key_modifiers):

        if self.back_button.touched :
            data.window.back()

        if self.settings_button.touched:
            data.window.display(SettingView())

        if self.quitter_button.touched :
            data.window.first()
