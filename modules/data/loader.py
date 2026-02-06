import json
import traceback
from os import listdir
from os.path import isdir, isfile, join
import arcade
from PIL import Image, ImageDraw, ImageFont
from modules.data import data
from modules.data.chip import Chip
from modules.data.level import Level
from modules.data.gate_index import gate_types
from modules.logger import Logger

logger = Logger("Loader")

class Loader:
    def load_json_files(self,sub_folder):
        path = join(data.current_path, sub_folder)
        if not isdir(path):
            return []
        
        results = []
        files = [f for f in listdir(path) if isfile(join(path, f))]
        for file_name in files:
            full_path = join(path, file_name)
            try:
                with open(full_path, "rb") as file:
                    results.append(json.loads(file.read()))
            except Exception as e:
                logger.error(f"Failed to read file {full_path} ({e})")
        return results

    def load_saves(self):
        for raw_data in self.load_json_files("saves"):
            try:
                chip = Chip("default_id")
                chip.load(raw_data)
                data.loaded_chips[raw_data["id"]] = chip
            except Exception:
                logger.error(f"Failed to load chip: {traceback.format_exc()}")

    def load_levels(self):
        for raw_data in self.load_json_files("levels"):
            try:
                level = Level("default_id")
                level.load(raw_data)
                data.loaded_levels[raw_data["level"]["id"]] = level
            except Exception:
                logger.error(f"Failed to load level: {traceback.format_exc()}")

    def load_assets(self):
        arcade.load_font("assets/press_start.ttf")
        
        data.ui_border_tiles = arcade.SpriteSheet("assets/ui_border_grid.png").get_texture_grid(
            size=(64, 64), columns=4, count=16
        )
        data.gate_tiles = arcade.SpriteSheet("assets/gate_grid.png").get_texture_grid(
            size=(data.UI_EDITOR_GRID_SIZE, data.UI_EDITOR_GRID_SIZE), columns=6, count=36
        )

    def _bake_grid(self, width_px, height_px):
        img = Image.new("RGBA", (width_px, height_px))
        tile = data.ui_border_tiles[9].image
        for y in range(0, height_px, 64):
            for x in range(0, width_px, 64):
                img.paste(tile, (x, y))
        return arcade.Texture(img)

    def _bake_border(self, width_px, rows):
        height_px = rows * 64
        canvas = Image.new("RGBA", (width_px, height_px))
        cols = width_px // 64

        def paste(idx, x, y):
            canvas.paste(data.ui_border_tiles[idx].image, (x * 64, y * 64))

        paste(0, 0, 0)
        for i in range(1, cols - 1): paste(1, i, 0)
        paste(3, cols - 1, 0)

        for i in range(1, rows - 1):
            paste(4, 0, i)
            paste(7, cols - 1, i)

        if rows > 3:
            for idx, off in [(12, 0), (13, 1), (5, 2), (6, 3), (10, 4)]:
                paste(idx, off, rows - 1)
            for i in range(5, cols - 1): paste(13, i, rows - 1)
            paste(15, cols - 1, rows - 1)
        
        return arcade.Texture(canvas)

    def render_gate_image(self, gate):
        width, height = gate.tile_width, 4
        new = Image.new("RGBA", (width * data.UI_EDITOR_GRID_SIZE, height * data.UI_EDITOR_GRID_SIZE))
        font = ImageFont.truetype('assets/press_start.ttf', 32)
        
        for i, pattern_idx in enumerate(gate.gate_tile_pattern):
            x, y = i % width, i // width
            tile = gate.tiles[pattern_idx].image.resize((data.UI_EDITOR_GRID_SIZE, data.UI_EDITOR_GRID_SIZE))
            new.paste(tile, (x * data.UI_EDITOR_GRID_SIZE, (height - 1 - y) * data.UI_EDITOR_GRID_SIZE))

        draw = ImageDraw.Draw(new)
        tx, ty = gate.width / 2, (height * data.UI_EDITOR_GRID_SIZE) - (gate.height / 1.6 + data.UI_EDITOR_GRID_SIZE / 4)
        draw.text((tx - 2, ty - 4), gate.name, font=font, fill="#5f556a", anchor="mm")
        draw.text((tx, ty), gate.name, font=font, fill="#b45252", anchor="mm")
        return new

    def bake_textures(self):
        logger.debug("Baking Textures")
        data.background_grid_texture = self._bake_grid(1920, 1088)
        data.editor_border_texture = self._bake_border(1920, 14)
        data.background_grid_texture_small = self._bake_grid(1920, 192)
        data.editor_border_texture_small = self._bake_border(1920, 3)
        data.background_grid_texture_level_player = self._bake_grid(1536, 1088)
        data.editor_border_texture_level_player = self._bake_border(1536, 14)

        for g_id in gate_types:
            gate = gate_types[g_id]("default_id")
            data.IMAGE.add_gate_type(g_id)
            size = len(gate.inputs) + len(gate.outputs)
            for i in range(2**size):
                vals = [bool(i & (1 << j)) for j in range(size)]
                gate.inputs, gate.outputs = vals[:len(gate.inputs)], vals[len(gate.inputs):]
                gate.gen_tile_pattern()
                data.IMAGE.add_texture(g_id, i, arcade.Texture(self.render_gate_image(gate)))
            data.IMAGE.complete_gate(g_id)