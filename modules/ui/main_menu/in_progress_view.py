import arcade

from modules.ui.mouse import mouse
from modules.ui.toolbox.button import Button
from modules.ui.editor.view import EditorView
from modules.ui.editor.selector import EditorChipSelector
from modules.ui.level_editor.view import LevelEditorView
from modules.ui.level_editor.selector import LevelEditorSelector
from modules.ui.debug_display_all_tiles.view import DebugTilesView
from modules.ui.main_menu.settings_view import SettingView

from modules.data.nodes.path import Path

from modules.data import data
from modules.logger import Logger

from pyglet.graphics import Batch
import sys

logger = Logger("MainMenu")

class MainMenuView(arcade.View):

    def __init__(self):
        super().__init__()

        self.background_color = arcade.color.JET

        self.ui_border_sheet = arcade.SpriteSheet("assets/ui_border_grid.png")

        self.ui_border_tiles = self.ui_border_sheet.get_texture_grid(
            size = (64, 64),
            columns = 4,
            count = 4*4,
        )

        self.play_button_sprite = arcade.Sprite("assets/play_button.png")
        self.name_banner_sprite = arcade.Sprite("assets/name_banner.png")
        self.quit_button_sprite = arcade.Sprite("assets/button_quit.png")
        self.level_button_sprite = arcade.Sprite("assets/button_level.png")
        self.setting_button_sprite = arcade.Sprite("assets/button_options.png")
        self.sandbox_button_sprite = arcade.Sprite("assets/button_sandbox.png")
        self.tuto_button_sprite = arcade.Sprite("assets/button_tuto.png")

        self.ui_sheet = arcade.SpriteSheet("assets/ui_grid.png")

        self.ui_tiles = self.ui_sheet.get_texture_grid(
            size = (32, 32),
            columns = 23,
            count = 9*23,
        )

        self.play_button = Button(self.ui_tiles)
        self.play_button.x = 1920 / 2 - 700 / 2 - 5
        self.play_button.y = 260 + 320 + 100 + 225 / 2
        self.play_button.width = 700
        self.play_button.height = 225

        self.quit_button = Button(self.ui_tiles)
        self.quit_button.x = 1920 - 350
        self.quit_button.y = 260 + 125
        self.quit_button.width = 175
        self.quit_button.height = 175

        self.setting_button = Button(self.ui_tiles)
        self.setting_button.x = 1920 / 7
        self.setting_button.y = 260 + 180 
        self.setting_button.width = 200*1.5
        self.setting_button.height = 100*1.5

        self.sandbox_button = Button(self.ui_tiles)
        self.sandbox_button.x = 1920 - 830
        self.sandbox_button.y = 260 + 168
        self.sandbox_button.width = 160*1.5
        self.sandbox_button.height = 100*1.5   

        self.level_button = Button(self.ui_tiles)
        self.level_button.x = 1920 / 2 - 200
        self.level_button.y = 260 + 250
        self.level_button.width = 180*1.25
        self.level_button.height = 100*1.25

        self.tuto_button = Button(self.ui_tiles)
        self.tuto_button.x = 1920 / 3 + 60
        self.tuto_button.y = 260
        self.tuto_button.width = 200*1.25
        self.tuto_button.height = 100*1.25

        self.button_touche = [""]
        self.combinaison = ["level_button", "sandbox_button", "tuto_button", "setting_button"]
        self.arcade_colors = [
                        "#FF004D", "#00E756", "#29ADFF", "#FFA300",
                        "#FFEC27", "#FF77A8", "#83769C", "#7E2553",
                        "#1D2B53", "#008751", "#AB5236", "#5F574F",
                        "#C2C3C7", "#FFF1E8", "#FF6F59", "#254441",
                        "#43AA8B", "#B2B09B", "#EF3054", "#3A86FF",
                        "#8338EC", "#FFBE0B", "#FB5607", "#FF006E",
                        "#2EC4B6", "#E71D36", "#011627", "#FF9F1C",
                        "#AACC00", "#00F5D4", "#F15BB5", "#9B5DE5",
                        "#FEE440", "#00BBF9", "#D00000", "#FFBA08",
                        "#6A4C93", "#1982C4", "#8AC926", "#FF595E"
                        ]
        self.compteur = 0


        self.paths = []
        self.add_paths()

    def add_paths(self):

        branches = [
            {0: [(945, 702), (594, 702), (594, 837), (270, 837), (270, 891)], 1: []},
            {0: [(945, 702), (945, 648), (540, 648), (540, 540), (243, 540), (243, 648), (81, 648)], 1: []},
            {0: [(945, 702), (945, 459), (675, 459), (675, 351), (189, 351), (189, 270), (81, 270)], 1: []},
            {0: [(945, 702), (945, 351), (729, 351), (729, 216), (297, 216), (297, 81)], 1: []},
            {0: [(945, 702), (972, 675), (972, 648), (1161, 648), (1161, 351), (1026, 351), (1026, 189), (918, 189), (918, 81)], 1: []},
            {0: [(945, 702), (1188, 702), (1188, 297), (1350, 297), (1350, 135), (1512, 135), (1512, 81)], 1: []},
            {0: [(945, 702), (1269, 702), (1269, 351), (1674, 351), (1674, 297), (1836, 297)], 1: []},
            {0: [(945, 702), (1377, 702), (1377, 729), (1836, 729)], 1: []},
            {0: [(945, 702), (1026, 729), (1296, 729), (1296, 891)], 1: []}
        ]

        for branch in branches:

            self.paths.append(Path(""))
            self.paths[len(self.paths)-1].do_points = False
            self.paths[len(self.paths)-1].branch_points = branch

    def draw_paths(self):

        for i in self.paths:
            i.draw()

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

        self.draw_paths()

        self.compteur += 0.1

        rect = arcade.XYWH(
                x = 1920 / 2,
                y = 260 + 320 + 100,
                width = 768,
                height = 768,
                anchor = arcade.Vec2(0.5,0.5)
        )

        arcade.draw_sprite_rect(self.play_button_sprite,rect)

        rect = arcade.XYWH(
                x=0,
                y=1080-128,
                width=1920,
                height=128,
                anchor=arcade.Vec2(0,0)
        )

        arcade.draw_sprite_rect(self.name_banner_sprite,rect)

        rect = arcade.XYWH(
                x = 1920 - 350,
                y = 260 + 125,
                width = 175,
                height = 175,
                anchor = arcade.Vec2(0, 1)
        )

        arcade.draw_sprite_rect(self.quit_button_sprite,rect)

        rect = arcade.XYWH(
                x = 1920 / 7,
                y = 260 + 180,
                width = 200*1.5,
                height = 100*1.5,
                anchor = arcade.Vec2(0, 1)
        )

        arcade.draw_sprite_rect(self.setting_button_sprite,rect)

        rect = arcade.XYWH(
                x = 1920 - 830,
                y = 260 + 168,
                width = 160*1.5,
                height = 100*1.5,
                anchor = arcade.Vec2(0, 1)
        )

        arcade.draw_sprite_rect(self.sandbox_button_sprite,rect)

        rect = arcade.XYWH(
                x = 1920 / 2 - 200,
                y = 260 + 250,
                width = 180*1.25,
                height = 100*1.25,
                anchor = arcade.Vec2(0, 1)
        )

        arcade.draw_sprite_rect(self.level_button_sprite,rect)

        rect = arcade.XYWH(
                x = 1920 / 3 + 60,
                y = 260,
                width = 200*1.25,
                height = 100*1.25,
                anchor = arcade.Vec2(0, 1)
        )

        arcade.draw_sprite_rect(self.tuto_button_sprite,rect)

        if self.button_touche == self.combinaison:
            color = (round(self.compteur) % (len(self.arcade_colors)))
            for i in self.paths :
                i.input_on_color = arcade.types.Color.from_hex_string(self.arcade_colors[color])
                i.current_value = True

        self.quit_button.draw()
        self.play_button.draw()
        self.setting_button.draw()
        self.level_button.draw()
        self.sandbox_button.draw()
        self.tuto_button.draw()
        self.draw_frame_border()

        
        

    def on_mouse_motion(self, x, y, delta_x, delta_y):
        mouse.position = (x,y)
        if self.play_button.touched:
            if self.button_touche[-1] != "play_button":
                self.button_touche.append("play_button")
            for i in self.paths :
                i.input_on_color = arcade.color.MINT_GREEN
                i.current_value = True

        elif self.quit_button.touched:
            if self.button_touche[-1] != "quit_button":
                self.button_touche.append("quit_button")
            for i in self.paths :
                i.input_on_color = arcade.color.RED
                i.current_value = True

        elif self.level_button.touched:
            if self.button_touche[-1] != "level_button":
                self.button_touche.append("level_button")
            for i in self.paths :
                i.input_on_color = arcade.color.UPSDELL_RED
                i.current_value = True

        elif self.setting_button.touched:
            if self.button_touche[-1] != "setting_button":
                self.button_touche.append("setting_button")
            for i in self.paths :
                i.input_on_color = arcade.color.GRAY
                i.current_value = True

        elif self.sandbox_button.touched:
            if self.button_touche[-1] != "sandbox_button":
                self.button_touche.append("sandbox_button")
            for i in self.paths :
                i.input_on_color = arcade.color.PICTON_BLUE
                i.current_value = True

        elif self.tuto_button.touched:
            if self.button_touche[-1] != "tuto_button":
                self.button_touche.append("tuto_button")
            for i in self.paths :
                i.input_on_color = arcade.color.UNIVERSITY_OF_TENNESSEE_ORANGE
                i.current_value = True

        else :
            for i in self.paths :
                i.current_value = False

        if len(self.button_touche) > 4:
            self.button_touche.pop(0)
            print (self.button_touche)


        


    def on_mouse_press(self, x, y, button, key_modifiers):
            
            if self.level_button.touched:
                data.window.display(LevelEditorSelector())
                logger.success("Launching LevelEditorSelector.")     

            if self.play_button.touched:
                data.window.hide()
                if key_modifiers == 16 or key_modifiers == 0:
                    data.window.display(EditorChipSelector())
                    logger.success("Launching EditorChipSelector.")
                elif key_modifiers == 17 or key_modifiers == 1:
                    data.window.display(DebugTilesView())
                    logger.print("Launching DebugTilesView.")
                elif key_modifiers == 2 or key_modifiers == 18:
                    data.window.display(MainMenuView())
                    logger.print("Launching Main Menu ???")
                else:
                    logger.warning(f"Modificator not found, defaulting to EditorView. ({key_modifiers})")
                    data.window.display(EditorView())
            
            if self.quit_button.touched:
                logger.success("Bye Bye ! <3")
                arcade.exit()

            if self.setting_button.touched:
                data.window.display(SettingView())