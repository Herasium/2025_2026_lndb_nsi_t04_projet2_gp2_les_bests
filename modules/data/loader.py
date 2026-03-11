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
from modules.data.custom import CustomGate
from modules.logger import Logger

logger = Logger("Loader")

class Loader:

    def __init__(self):
        self.to_load_buffer = []

    def load_files(self,sub_folder):
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
        for raw_data in self.load_files("saves"):
            try:
                chip = Chip("default_id")
                chip.partial_load(raw_data)
                if len(chip.requirements) == 0:
                    chip.load()
                    data.loaded_chips[raw_data["id"]] = chip
                else:
                    can_load = True
                    for i in chip.requirements:
                        if not i in data.loaded_chips:
                            can_load = False
                    if can_load:
                        chip.load()
                        data.loaded_chips[raw_data["id"]] = chip
                    else:
                        self.to_load_buffer.append(chip)

            except Exception:
                logger.error(f"Failed to load chip: {traceback.format_exc()}")
        logger.success(f"Loaded {len(data.loaded_chips)} Chips.")
        if len(self.to_load_buffer):
            logger.info(f"Chip loading not finished, {len(self.to_load_buffer)} chips with requirements left to load.")

    def load_saves_dependency_round(self):
        for chip in self.to_load_buffer:
            can_load = True
            for i in chip.requirements:
                if not i in data.loaded_chips:
                    can_load = False
            if can_load:
                chip.load()
                self.to_load_buffer.remove(chip)
                data.loaded_chips[chip.id] = chip

    def load_saves_dependency(self):

        max_count = 1000
        count = 0
        previous = len(self.to_load_buffer)

        while count < max_count and len(self.to_load_buffer) > 0:
            self.load_saves_dependency_round()
            if len(self.to_load_buffer) == previous:
                logger.error(f"Failed to load {len(self.to_load_buffer)} gates with dependencies, maybe due to circular dependency or missing chips.")
            else:
                previous = len(self.to_load_buffer)
            count += 1

        logger.success(f"Finished loading gates with dependencies in {count} rounds.")

    def load_levels(self):
        for raw_data in self.load_files("levels"):
            try:
                level = Level("default_id")
                level.load(raw_data)
                data.loaded_levels[raw_data["level"]["id"]] = level
            except Exception:
                logger.error(f"Failed to load level: {traceback.format_exc()}")

        logger.success(f"Loaded {len(data.loaded_levels)} Levels.")
    def load_fonts(self):
        try:
            arcade.load_font("assets/fonts/press_start.ttf")
            logger.success("Loaded Fonts (1).")
        except Exception as e:
            logger.error(f"Failed to load fonts ({e}).")

    def load_tilesets(self):
        
        data.ui_border_tiles = arcade.SpriteSheet("assets/grid/ui_border_grid.png").get_texture_grid(
            size=(64, 64), columns=4, count=16
        )
        data.gate_tiles = arcade.SpriteSheet("assets/grid/gate_grid.png").get_texture_grid(
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

        for i in range(1, rows):
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
        font = ImageFont.truetype('assets/fonts/press_start.ttf', 32)
        
        for i, pattern_idx in enumerate(gate.gate_tile_pattern):
            x, y = i % width, i // width
            tile = gate.tiles[pattern_idx].image.resize((data.UI_EDITOR_GRID_SIZE, data.UI_EDITOR_GRID_SIZE))
            new.paste(tile, (x * data.UI_EDITOR_GRID_SIZE, (height - 1 - y) * data.UI_EDITOR_GRID_SIZE))

        draw = ImageDraw.Draw(new)
        tx, ty = gate.width / 2, (height * data.UI_EDITOR_GRID_SIZE) - (gate.height / 1.6 + data.UI_EDITOR_GRID_SIZE / 4)
        draw.text((tx - 2, ty - 4), gate.name, font=font, fill="#5f556a", anchor="mm")
        draw.text((tx, ty), gate.name, font=font, fill="#b45252", anchor="mm")
        return new

    def bake_single_gate(self,gate,id):
        data.IMAGE.add_gate_type(id)
        size = len(gate.inputs) + len(gate.outputs)
        if size >= 12:
            logger.warning(f"Large Texture count found {2**size}, this might take a while.")

        if size > 16 :
            logger.error(f"Texture size too large, aborting.")
            return False
        
        for i in range(2**size):
            vals = [bool(i & (1 << j)) for j in range(size)]
            gate.inputs, gate.outputs = vals[:len(gate.inputs)], vals[len(gate.inputs):]
            gate.gen_tile_pattern()
            data.IMAGE.add_texture(id, i, arcade.Texture(self.render_gate_image(gate)))
        data.IMAGE.complete_gate(id)

    def bake_predefined_gates(self):
        
        for g_id in gate_types:
            gate = gate_types[g_id]("default_id")
            self.bake_single_gate(gate,g_id)

    def bake_custom_gates(self):

        to_remove = []

        for chip_id in data.loaded_chips:
            chip = data.loaded_chips[chip_id]
            new = CustomGate("no_id",chip.copy())
            result = self.bake_single_gate(new,chip.id)
            if result == False:
                to_remove.append(chip_id)

        for i in to_remove:
            logger.warning(f"Chip {i} failed to load textures, removed from register.")
            del data.loaded_chips[i]

    def bake_level_buttons(self):
        
        font = ImageFont.truetype('assets/fonts/press_start.ttf', 32)

        for i in data.loaded_levels:
            level = data.loaded_levels[i]
            number = "0"*(2-len(str(level.number)))+str(level.number)
            color = level.color

            new = Image.new("RGBA", (175, 175))
            new.paste(data.level_buttons_empty[data.level_colors[color]].texture.image,(0,0))
            draw = ImageDraw.Draw(new)
            draw.text((175/2, 175/2 - 16), number, font=font, fill="#000000", anchor="mm")
            draw.text((175/2, 175/2 - 20), number, font=font, fill="#FFFFFF", anchor="mm")
            data.LEVEL_BUTTONS.set(level.id,new)

    def bake_textures(self):
        logger.debug("Baking Textures")
        data.background_grid_texture = self._bake_grid(1920, 1088)
        self.bake_predefined_gates()
        self.bake_custom_gates()
        self.bake_level_buttons()


    def load_ui(self):

        data.play_button = arcade.Sprite("assets/buttons/play_button.png")
        data.button_level = arcade.Sprite("assets/buttons/button_level.png")
        data.button_options = arcade.Sprite("assets/buttons/button_options.png")
        data.button_quit = arcade.Sprite("assets/buttons/button_quit.png")
        data.button_sandbox = arcade.Sprite("assets/buttons/button_sandbox.png")
        data.button_tuto = arcade.Sprite("assets/buttons/button_tuto.png")
        data.button_check = arcade.Sprite("assets/buttons/button_check.png")
        data.button_next_on = arcade.Sprite("assets/buttons/button_next_on.png")
        data.button_next_off = arcade.Sprite("assets/buttons/button_next_off.png")
        data.button_back = arcade.Sprite("assets/buttons/button_back.png")

        data.name_banner = arcade.Sprite("assets/titles/name_banner.png")
        data.level_info = arcade.Sprite("assets/titles/level_info.png")
        data.truth_table = arcade.Sprite("assets/titles/truth_table.png")

        data.editor_border = arcade.Sprite("assets/borders/editor_border.png")
        data.editor_border_no_bg = arcade.Sprite("assets/borders/editor_border_no_bg.png")
        data.level_player_border = arcade.Sprite("assets/borders/level_player_border.png")
        data.level_player_win = arcade.Sprite("assets/borders/level_player_win.png")
        data.border_small = arcade.Sprite("assets/borders/border_small.png")

        data.star = arcade.Sprite("assets/icons/star.png")
        data.star_empty = arcade.Sprite("assets/icons/star_empty.png")

        data.level_buttons_empty = {}

        data.level_buttons_empty["yellow"] = arcade.Sprite("assets/buttons/levels/yellow.png")
        data.level_buttons_empty["orange"] = arcade.Sprite("assets/buttons/levels/orange.png")
        data.level_buttons_empty["red"] = arcade.Sprite("assets/buttons/levels/red.png")
        data.level_buttons_empty["green"] = arcade.Sprite("assets/buttons/levels/green.png")


    def load(self):

        logger.print("Loading Game Stuff.")

        try:

            self.load_fonts()
            self.load_tilesets()
            self.load_ui()
            self.load_saves()
            if len(self.to_load_buffer) > 0:
                self.load_saves_dependency()
            self.load_levels()
            self.bake_textures()
            
            logger.success("Finished loading stuff.")
        except Exception as e:
            logger.error(f"Failed to load stuff ({e})")

        
