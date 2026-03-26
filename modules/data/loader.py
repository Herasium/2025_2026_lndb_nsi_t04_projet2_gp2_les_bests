import json
import traceback
from typing import List, Dict, Any, Union
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

"""
This module handles the initialization, asset loading, and procedural texture
baking for the game's data-driven architecture.
"""

logger: Logger = Logger("Loader")


class Loader:
    """
    Manages the loading of external JSON assets, game logic resources,
    and the generation of procedural UI textures.
    """

    def __init__(self) -> None:
        """Initializes the loader with a buffer for unresolved dependencies."""
        self.to_load_buffer: List[Chip] = []

    def load_files(self, sub_folder: str) -> List[Dict[str, Any]]:
        """
        Reads all JSON files from a specified subdirectory.

        Args:
            sub_folder: The directory path relative to the data root.

        Returns:
            A list containing the parsed contents of each JSON file.
        """
        path: str = join(data.current_path, sub_folder)

        if not isdir(path):
            return []

        results: List[Dict[str, Any]] = []
        files: List[str] = [f for f in listdir(path) if isfile(join(path, f))]

        for file_name in files:
            full_path: str = join(path, file_name)
            try:
                with open(full_path, "rb") as file:
                    results.append(json.loads(file.read()))
            except Exception as e:
                logger.error(f"Failed to read file {full_path} ({e})")

        return results

    def load_single_chip(self, raw_data: Dict[str, Any]) -> None:
        """
        Registers a chip object and handles its dependency requirements.

        Args:
            raw_data: The configuration dictionary for the chip.
        """
        chip: Chip = Chip("default_id")
        chip.partial_load(raw_data)

        if len(chip.requirements) == 0:
            chip.load()
            if len(chip.get_inputs()) + len(chip.get_outputs()) == 0:
                logger.warning(f"Empty Chip {chip}, not loading.")
                return
            data.loaded_chips[raw_data["id"]] = chip
        else:
            can_load: bool = True
            for i in chip.requirements:
                if i not in data.loaded_chips:
                    can_load = False
                    break

            if can_load:
                chip.load()
                if len(chip.get_inputs()) + len(chip.get_outputs()) == 0:
                    logger.warning(f"Empty Chip {chip}, not loading.")
                    return
                data.loaded_chips[raw_data["id"]] = chip
            else:
                self.to_load_buffer.append(chip)

    def load_saves(self) -> None:
        """Loads and processes all saved chip configurations."""
        for raw_data in self.load_files("saves"):
            try:
                self.load_single_chip(raw_data)
            except Exception:
                logger.error(f"Failed to load chip: {traceback.format_exc()}")

        logger.success(f"Loaded {len(data.loaded_chips)} Chips.")
        if len(self.to_load_buffer):
            logger.info(
                f"Chip loading not finished, {len(self.to_load_buffer)} chips with requirements left to load."
            )

    def load_saves_dependency_round(self) -> None:
        """Performs a single resolution pass on buffered chips."""
        for chip in self.to_load_buffer[:]:
            can_load: bool = True
            for i in chip.requirements:
                if i not in data.loaded_chips:
                    can_load = False
                    break

            if can_load:
                chip.load()
                if len(chip.get_inputs()) + len(chip.get_outputs()) == 0:
                    logger.warning(f"Empty Chip {chip}, not loading.")
                    return
                self.to_load_buffer.remove(chip)
                data.loaded_chips[chip.id] = chip

    def load_saves_dependency(self) -> None:
        """Iteratively resolves dependencies until all chips are loaded or limit reached."""
        max_count: int = 1000
        count: int = 0
        previous: int = len(self.to_load_buffer)

        while count < max_count and len(self.to_load_buffer) > 0:
            self.load_saves_dependency_round()

            if len(self.to_load_buffer) == previous:
                logger.error(
                    f"Failed to load {len(self.to_load_buffer)} gates with dependencies, maybe due to circular dependency or missing chips."
                )
                break
            else:
                previous = len(self.to_load_buffer)
            count += 1

        logger.debug(f"Finished loading gates with dependencies in {count} rounds.")

    def load_levels(self) -> None:
        """Loads all level definitions and their required assets."""
        for raw_data in self.load_files("levels"):
            try:
                level: Level = Level("default_id")
                if raw_data["level"]["version"] > 160:
                    for i in raw_data["requirements"]:
                        self.load_single_chip(i)

                self.load_saves_dependency()
                level.load(raw_data)
                if level.is_custom:
                    data.loaded_chips[level.chip.id] = level.chip
                data.loaded_levels[raw_data["level"]["id"]] = level
            except Exception:
                logger.error(f"Failed to load level: {traceback.format_exc()}")

        logger.success(f"Loaded {len(data.loaded_levels)} Levels.")

    def load_fonts(self) -> None:
        """Registers external TTF fonts with the rendering engine."""
        try:
            arcade.load_font("assets/fonts/press_start.ttf")
            logger.success("Loaded Fonts (1).")
        except Exception as e:
            logger.error(f"Failed to load fonts ({e}).")

    def load_tilesets(self) -> None:
        """Slices sprite sheets into texture grids for UI components."""
        data.ui_border_tiles = arcade.SpriteSheet(
            "assets/grid/ui_border_grid.png"
        ).get_texture_grid(size=(64, 64), columns=4, count=16)
        data.gate_tiles = arcade.SpriteSheet(
            "assets/grid/gate_grid.png"
        ).get_texture_grid(
            size=(data.UI_EDITOR_GRID_SIZE, data.UI_EDITOR_GRID_SIZE),
            columns=6,
            count=36,
        )

    def _bake_grid(self, width_px: int, height_px: int) -> arcade.Texture:
        """
        Generates a repeating background grid texture.

        Args:
            width_px: Total target width.
            height_px: Total target height.

        Returns:
            The generated arcade-compatible texture.
        """
        img: Image.Image = Image.new("RGBA", (width_px, height_px))
        tile: Image.Image = data.ui_border_tiles[9].image
        for y in range(0, height_px, 64):
            for x in range(0, width_px, 64):
                img.paste(tile, (x, y))
        return arcade.Texture(img)

    def _bake_border(self, width_px: int, rows: int) -> arcade.Texture:
        """
        Generates a custom-sized UI border frame.

        Args:
            width_px: Width of the frame.
            rows: Number of vertical tile rows.

        Returns:
            The generated frame texture.
        """
        height_px: int = rows * 64
        canvas: Image.Image = Image.new("RGBA", (width_px, height_px))
        cols: int = width_px // 64

        def paste(idx: int, x: int, y: int) -> None:
            canvas.paste(data.ui_border_tiles[idx].image, (x * 64, y * 64))

        paste(0, 0, 0)
        for i in range(1, cols - 1):
            paste(1, i, 0)
        paste(3, cols - 1, 0)

        for i in range(1, rows):
            paste(4, 0, i)
            paste(7, cols - 1, i)

        if rows > 3:
            for idx, off in [(12, 0), (13, 1), (5, 2), (6, 3), (10, 4)]:
                paste(idx, off, rows - 1)
            for i in range(5, cols - 1):
                paste(13, i, rows - 1)
            paste(15, cols - 1, rows - 1)

        return arcade.Texture(canvas)

    def render_gate_image(self, gate: Union[CustomGate, Any]) -> Image.Image:
        """
        Renders a composite image for a gate, including tiles and text labels.

        Args:
            gate: The gate component to render.

        Returns:
            The rendered PIL Image.
        """
        width: int = gate.tile_width
        height: int = 4
        new: Image.Image = Image.new(
            "RGBA",
            (width * data.UI_EDITOR_GRID_SIZE, height * data.UI_EDITOR_GRID_SIZE),
        )
        font: ImageFont.FreeTypeFont = ImageFont.truetype(
            "assets/fonts/press_start.ttf", 32
        )

        for i, pattern_idx in enumerate(gate.gate_tile_pattern):
            x, y = i % width, i // width
            tile: Image.Image = gate.tiles[pattern_idx].image.resize(
                (data.UI_EDITOR_GRID_SIZE, data.UI_EDITOR_GRID_SIZE)
            )
            new.paste(
                tile,
                (
                    x * data.UI_EDITOR_GRID_SIZE,
                    (height - 1 - y) * data.UI_EDITOR_GRID_SIZE,
                ),
            )

        draw: ImageDraw.ImageDraw = ImageDraw.Draw(new)
        tx: float = gate.width / 2
        ty: float = (height * data.UI_EDITOR_GRID_SIZE) - (
            gate.height / 1.6 + data.UI_EDITOR_GRID_SIZE / 4
        )

        draw.text((tx - 2, ty - 4), gate.name, font=font, fill="#5f556a", anchor="mm")
        draw.text((tx, ty), gate.name, font=font, fill="#b45252", anchor="mm")
        return new

    def bake_single_gate(self, gate: Any, id: str) -> bool:
        """
        Caches state-specific textures for a gate to optimize performance.

        Args:
            gate: The gate instance.
            id: Unique gate identifier.

        Returns:
            True if baking succeeded, False if input/output complexity exceeds limits.
        """
        data.IMAGE.add_gate_type(id)
        size: int = len(gate.inputs) + len(gate.outputs)

        if size >= 12:
            logger.warning(
                f"Large Texture count found {2**size}, this might take a while."
            )

        if size > 16:
            logger.error("Texture size too large, aborting.")
            return False

        for i in range(2**size):
            # Calculate input/output states using bitwise flag extraction
            vals: List[bool] = [bool(i & (1 << j)) for j in range(size)]
            gate.inputs, gate.outputs = (
                vals[: len(gate.inputs)],
                vals[len(gate.inputs) :],
            )
            gate.gen_tile_pattern()
            data.IMAGE.add_texture(id, i, arcade.Texture(self.render_gate_image(gate)))

        data.IMAGE.complete_gate(id)
        return True

    def bake_predefined_gates(self) -> None:
        """Generates textures for all built-in system gates."""
        for g_id in gate_types:
            gate = gate_types[g_id]("default_id")
            self.bake_single_gate(gate, g_id)

    def bake_custom_gates(self) -> None:
        """Generates textures for user-defined custom chips."""
        to_remove: List[str] = []

        for chip_id in data.loaded_chips:
            chip: Chip = data.loaded_chips[chip_id]
            new: CustomGate = CustomGate("no_id", chip.copy())
            result: bool = self.bake_single_gate(new, chip.id)
            if not result:
                to_remove.append(chip_id)

        for i in to_remove:
            logger.warning(f"Chip {i} failed to load textures, removed from register.")
            del data.loaded_chips[i]

    def bake_level_buttons(self) -> None:
        """Generates unique visual buttons for each available game level."""
        font: ImageFont.FreeTypeFont = ImageFont.truetype(
            "assets/fonts/press_start.ttf", 32
        )

        for i in data.loaded_levels:
            level: Level = data.loaded_levels[i]
            number: str = "0" * (2 - len(str(level.number))) + str(level.number)
            color: str = level.color

            new: Image.Image = Image.new("RGBA", (175, 175))
            new.paste(
                data.level_buttons_empty[data.level_colors[color]].texture.image, (0, 0)
            )

            draw: ImageDraw.ImageDraw = ImageDraw.Draw(new)
            draw.text(
                (175 / 2, 175 / 2 - 16), number, font=font, fill="#000000", anchor="mm"
            )
            draw.text(
                (175 / 2, 175 / 2 - 20), number, font=font, fill="#FFFFFF", anchor="mm"
            )
            data.LEVEL_BUTTONS.set(level.id, new)

    def bake_textures(self) -> None:
        """Coordinates the full procedural texture generation workflow."""
        logger.debug("Baking Textures")
        data.background_grid_texture = self._bake_grid(
            data.WINDOW_WIDTH, (((data.WINDOW_HEIGHT + 32) // 64) * 64)
        )
        self.bake_predefined_gates()
        self.bake_custom_gates()
        self.bake_level_buttons()

    def load_ui(self) -> None:
        """Loads and initializes static interface assets."""
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
        data.button_ok = arcade.Sprite("assets/buttons/button_ok.png")
        data.button_save = arcade.Sprite("assets/buttons/button_save.png")
        data.button_edit = arcade.Sprite("assets/buttons/button_edit.png")
        data.button_new = arcade.Sprite("assets/buttons/button_new.png")
        data.button_resume = arcade.Sprite("assets/buttons/button_resume.png")

        data.name_banner = arcade.Sprite("assets/titles/name_banner.png")
        data.level_info = arcade.Sprite("assets/titles/level_info.png")
        data.truth_table = arcade.Sprite("assets/titles/truth_table.png")
        data.chip_save = arcade.Sprite("assets/titles/chip_save.png")
        data.option_title = arcade.Sprite("assets/titles/options.png")
        data.input_title = arcade.Sprite("assets/titles/input.png")

        data.editor_border = arcade.Sprite("assets/borders/editor_border.png")
        data.chip_select = arcade.Sprite("assets/borders/chip_select.png")
        data.editor_border_no_bg = arcade.Sprite(
            "assets/borders/editor_border_no_bg.png"
        )
        data.level_player_border = arcade.Sprite(
            "assets/borders/level_player_border.png"
        )
        data.level_player_border_no_bg = arcade.Sprite(
            "assets/borders/level_player_no_bg.png"
        )
        data.level_player_win = arcade.Sprite("assets/borders/level_player_win.png")
        data.border_small = arcade.Sprite("assets/borders/border_small.png")
        data.level_player_empty = arcade.Sprite("assets/borders/level_player_empty.png")

        data.star = arcade.Sprite("assets/icons/star.png")
        data.star_empty = arcade.Sprite("assets/icons/star_empty.png")

        data.level_buttons_empty = {}
        data.level_buttons_empty["yellow"] = arcade.Sprite(
            "assets/buttons/levels/yellow.png"
        )
        data.level_buttons_empty["orange"] = arcade.Sprite(
            "assets/buttons/levels/orange.png"
        )
        data.level_buttons_empty["red"] = arcade.Sprite("assets/buttons/levels/red.png")
        data.level_buttons_empty["green"] = arcade.Sprite(
            "assets/buttons/levels/green.png"
        )
        data.level_buttons_empty["black"] = arcade.Sprite("assets/buttons/levels/black.png")
        data.level_buttons_empty["purple"] = arcade.Sprite("assets/buttons/levels/purple.png")

        data.editor_categories = {}
        data.editor_categories["1_bit"] = arcade.Sprite(
            "assets/buttons/editor_categories/1_bit.png"
        )
        data.editor_categories["8_bit"] = arcade.Sprite(
            "assets/buttons/editor_categories/8_bit.png"
        )
        data.editor_categories["custom"] = arcade.Sprite(
            "assets/buttons/editor_categories/custom.png"
        )

        data.tuto_truth = {}
        data.tuto_truth["or"] = arcade.Sprite("assets/truth/or_gate.png")
        data.tuto_truth["and"] = arcade.Sprite("assets/truth/and_gate.png")
        data.tuto_truth["nand"] = arcade.Sprite("assets/truth/nand_gate.png")
        data.tuto_truth["nor"] = arcade.Sprite("assets/truth/nor_gate.png")
        data.tuto_truth["not"] = arcade.Sprite("assets/truth/not_gate.png")
        data.tuto_truth["xor"] = arcade.Sprite("assets/truth/xor_gate.png")

    def load(self) -> None:
        """Executes the full asset loading and initialization pipeline."""
        logger.print("Loading Game Stuff.")

        try:
            self.load_fonts()
            self.load_tilesets()
            self.load_ui()
            self.load_saves()
            self.load_levels()

            if len(self.to_load_buffer) > 0:
                self.load_saves_dependency()

            self.bake_textures()

            logger.success("Finished loading stuff.")
        except Exception:
            logger.error(f"Failed to load stuff ({traceback.format_exc()})")
