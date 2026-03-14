import arcade
import math

from modules.data.node import Node
from modules.data.gate import Gate

from modules.data import data
from modules.ui.toolbox.text import Text
from line_profiler import profile


class Complex(Gate):

    def __init__(self, id):
        super().__init__(id)

        self.name = "COMP"
        self.type = "Complex"
        self.gate_type = "COMP"
        self.draw_hitboxes = False
        self.hide_text = False

        self.inputs = []
        self.outputs = []
        self.inputs_sizes = []
        self.outputs_sizes = []
        self.texts = {}

        self.calculate_display()
        self.gen_tile_pattern()
        self.setup_texts()
        
    def setup_texts(self):
        self.texts = {}

        for i in range(len(self.inputs)):
            if self.inputs_sizes[i] != 1:
                x = self.inputs_hitboxes[i].x + data.UI_EDITOR_GRID_SIZE/2
                y = self.inputs_hitboxes[i].y + data.UI_EDITOR_GRID_SIZE*1.5
                new = Text(x=x,y=y,width=data.UI_EDITOR_GRID_SIZE,height=data.UI_EDITOR_GRID_SIZE,text=str(self.inputs[i]),size=10)
                self.texts[f"i{i}"] = new

        
        for i in range(len(self.outputs)):
            if self.outputs_sizes[i] != 1:
                x = self.outputs_hitboxes[i].x + data.UI_EDITOR_GRID_SIZE/2
                y = self.outputs_hitboxes[i].y + data.UI_EDITOR_GRID_SIZE*1.5
                new = Text(x=x,y=y,width=data.UI_EDITOR_GRID_SIZE,height=data.UI_EDITOR_GRID_SIZE,text=str(self.outputs[i]),size=10)
                self.texts[f"o{i}"] = new
                
    def update_text_readings(self):
        if len(self.texts.keys()) == 0: return
        for i in range(len(self.inputs)):
            if self.inputs_sizes[i] != 1:
                self.texts[f"i{i}"].text = str(self.inputs[i])

        
        for i in range(len(self.outputs)):
            if self.outputs_sizes[i] != 1:
                self.texts[f"o{i}"].text = str(self.outputs[i])

    def update_text_position(self):
        self.hide_text = False
        if len(self.texts.keys()) == 0: return
        for i in range(len(self.inputs)):
            if self.inputs_sizes[i] != 1:
                x = self.inputs_hitboxes[i].x + data.UI_EDITOR_GRID_SIZE/2
                y = self.inputs_hitboxes[i].y + data.UI_EDITOR_GRID_SIZE*1.5
                self.texts[f"i{i}"]._x = x
                self.texts[f"i{i}"].y = y

        for i in range(len(self.outputs)):
            if self.outputs_sizes[i] != 1:
                x = self.outputs_hitboxes[i].x + data.UI_EDITOR_GRID_SIZE/2
                y = self.outputs_hitboxes[i].y + data.UI_EDITOR_GRID_SIZE*1.5
                self.texts[f"o{i}"]._x = x
                self.texts[f"o{i}"].y = y


    def draw_tiles(self):
    
        width = self.tile_width
        height = 4
        out = self.outputs.copy()
        inp = self.inputs.copy()

        for i in range(len(inp)):
            if self.inputs_sizes[i] != 1:
                inp[i] = 0

        for i in range(len(out)):
            if self.outputs_sizes[i] != 1:
                out[i] = 0

        out.reverse()
        inp.reverse()
        current = int(''.join(map(str, map(int, (out+inp)))), 2)

        tile_x = self.x + self._camera[0]
        tile_y = self.y + self._camera[1]

        rect = arcade.XYWH(
                    x=tile_x,
                    y=tile_y,
                    width=width * data.UI_EDITOR_GRID_SIZE,
                    height=height * data.UI_EDITOR_GRID_SIZE,
                    anchor=arcade.Vec2(0,0)
        )

        
        arcade.draw_texture_rect(data.IMAGE.get_texture(self.gate_type,current),rect)
        if not self.hide_text:
            for i in self.texts:
                self.texts[i].draw()
