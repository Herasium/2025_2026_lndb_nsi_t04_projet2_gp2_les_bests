import json
import traceback
from typing import List, Dict, Any, Union
from os import listdir
from os.path import isdir, isfile, join
import arcade
from PIL import Image, ImageDraw, ImageFont

# Internal module imports
from modules.data import data
from modules.data.chip import Chip
from modules.data.level import Level
from modules.data.gate_index import gate_types
from modules.data.custom import CustomGate
from modules.logger import Logger

# Initialize the logger for the Loader class
logger: Logger = Logger("Loader")


class Loader:
    """Class responsible for loading assets, levels, chips, and baking textures for the game."""

    def __init__(self) -> None:
        """Initialize the Loader with an empty buffer for chips pending dependency resolution."""
        self.to_load_buffer: List[Chip] = []

    def load_files(self, sub_folder: str) -> List[Dict[str, Any]]:
        """
        Read all JSON files within a specific subdirectory of the data path.

        Parameters:
        - sub_folder (str): The name of the folder to scan within the data directory.

        Returns:
        - List[Dict[str, Any]]: A list of dictionaries representing the JSON content of the files.
        """
        path: str = join(data.current_path, sub_folder)

        # Verify if the directory exists before proceeding
        if not isdir(path):
            return []

        results: List[Dict[str, Any]] = []
        # Filter for files only in the directory
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
        Process raw data to create and register a Chip object, handling dependencies.

        Parameters:
        - raw_data (Dict[str, Any]): The dictionary containing chip configuration.

        Returns:
        - None
        """
        chip: Chip = Chip("default_id")
        chip.partial_load(raw_data)

        # If chip has no dependencies, load it immediately
        if len(chip.requirements) == 0:
            chip.load()
            data.loaded_chips[raw_data["id"]] = chip
        else:
            # Check if all required chips are already loaded
            can_load: bool = True
            for i in chip.requirements:
                if i not in data.loaded_chips:
                    can_load = False
                    break

            if can_load:
                chip.load()
                data.loaded_chips[raw_data["id"]] = chip
            else:
                # Store in buffer to resolve dependencies later
                self.to_load_buffer.append(chip)

    def load_saves(self) -> None:
        """
        Load all saved chip files from the 'saves' directory.

        Returns:
        - None
        """
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
        """
        Perform a single pass through the buffer to load chips whose dependencies are now met.

        Returns:
        - None
        """
        # Iterate over a copy to allow removal during iteration
        for chip in self.to_load_buffer[:]:
            can_load: bool = True
            for i in chip.requirements:
                if i not in data.loaded_chips:
                    can_load = False
                    break

            if can_load:
                chip.load()
                self.to_load_buffer.remove(chip)
                data.loaded_chips[chip.id] = chip

    def load_saves_dependency(self) -> None:
        """
        Repeatedly resolve dependencies for chips in the buffer until all are loaded or a limit is reached.

        Returns:
        - None
        """
        max_count: int = 1000
        count: int = 0
        previous: int = len(self.to_load_buffer)

        # Loop until buffer is empty or no progress is made (to detect circularity)
        while count < max_count and len(self.to_load_buffer) > 0:
            self.load_saves_dependency_round()

            if len(self.to_load_buffer) == previous:
                logger.error(
                    f"Failed to load {len(self.to_load_buffer)} gates with dependencies, maybe due to circular dependency or missing chips."
                )
                break  # Exit to prevent infinite loop
            else:
                previous = len(self.to_load_buffer)
            count += 1

        logger.debug(f"Finished loading gates with dependencies in {count} rounds.")

    def load_levels(self) -> None:
        """
        Load all level files from the 'levels' directory and their associated requirements.

        Returns:
        - None
        """
        for raw_data in self.load_files("levels"):
            try:
                level: Level = Level("default_id")
                # Version check to handle dependency loading for newer level formats
                if raw_data["level"]["version"] > 160:
                    for i in raw_data["requirements"]:
                        self.load_single_chip(i)

                self.load_saves_dependency()
                level.load(raw_data)
                data.loaded_levels[raw_data["level"]["id"]] = level
            except Exception:
                logger.error(f"Failed to load level: {traceback.format_exc()}")

        logger.success(f"Loaded {len(data.loaded_levels)} Levels.")

    def load_fonts(self) -> None:
        """
        Load game fonts into the arcade engine.

        Returns:
        - None
        """
        try:
            arcade.load_font("assets/fonts/press_start.ttf")
            logger.success("Loaded Fonts (1).")
        except Exception as e:
            logger.error(f"Failed to load fonts ({e}).")

    def load_tilesets(self) -> None:
        """
        Load sprite sheets and slice them into texture grids for the UI and gates.

        Returns:
        - None
        """
        # Load the UI border grid
        data.ui_border_tiles = arcade.SpriteSheet(
            "assets/grid/ui_border_grid.png"
        ).get_texture_grid(size=(64, 64), columns=4, count=16)
        # Load the gate component grid
        data.gate_tiles = arcade.SpriteSheet(
            "assets/grid/gate_grid.png"
        ).get_texture_grid(
            size=(data.UI_EDITOR_GRID_SIZE, data.UI_EDITOR_GRID_SIZE),
            columns=6,
            count=36,
        )

    def _bake_grid(self, width_px: int, height_px: int) -> arcade.Texture:
        """
        Create a tiled background texture of a specific size.

        Parameters:
        - width_px (int): Total width in pixels.
        - height_px (int): Total height in pixels.

        Returns:
        - arcade.Texture: The generated grid texture.
        """
        img: Image.Image = Image.new("RGBA", (width_px, height_px))
        tile: Image.Image = data.ui_border_tiles[9].image
        # Fill the image by pasting tiles in a grid pattern
        for y in range(0, height_px, 64):
            for x in range(0, width_px, 64):
                img.paste(tile, (x, y))
        return arcade.Texture(img)

    def _bake_border(self, width_px: int, rows: int) -> arcade.Texture:
        """
        Create a custom-sized border texture using the UI tileset.

        Parameters:
        - width_px (int): Width in pixels.
        - rows (int): Number of vertical tiles.

        Returns:
        - arcade.Texture: The generated border texture.
        """
        height_px: int = rows * 64
        canvas: Image.Image = Image.new("RGBA", (width_px, height_px))
        cols: int = width_px // 64

        def paste(idx: int, x: int, y: int) -> None:
            """Helper to paste a specific tile index at grid coordinates."""
            canvas.paste(data.ui_border_tiles[idx].image, (x * 64, y * 64))

        # Top row
        paste(0, 0, 0)
        for i in range(1, cols - 1):
            paste(1, i, 0)
        paste(3, cols - 1, 0)

        # Side walls
        for i in range(1, rows):
            paste(4, 0, i)
            paste(7, cols - 1, i)

        # Bottom row logic for larger UI elements
        if rows > 3:
            for idx, off in [(12, 0), (13, 1), (5, 2), (6, 3), (10, 4)]:
                paste(idx, off, rows - 1)
            for i in range(5, cols - 1):
                paste(13, i, rows - 1)
            paste(15, cols - 1, rows - 1)

        return arcade.Texture(canvas)

    def render_gate_image(self, gate: Union[CustomGate, Any]) -> Image.Image:
        """
        Render the visual representation of a gate including its tile pattern and name.

        Parameters:
        - gate: The gate object to render.

        Returns:
        - Image.Image: A PIL Image of the rendered gate.
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

        # Draw the gate tiles based on the pattern
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
        # Calculate text positioning (Shadow and main text)
        tx: float = gate.width / 2
        ty: float = (height * data.UI_EDITOR_GRID_SIZE) - (
            gate.height / 1.6 + data.UI_EDITOR_GRID_SIZE / 4
        )

        # Draw shadow
        draw.text((tx - 2, ty - 4), gate.name, font=font, fill="#5f556a", anchor="mm")
        # Draw main text
        draw.text((tx, ty), gate.name, font=font, fill="#b45252", anchor="mm")
        return new

    def bake_single_gate(self, gate: Any, id: str) -> bool:
        """
        Generate and cache all possible input/output state textures for a single gate.

        Parameters:
        - gate (Any): The gate instance.
        - id (str): Unique identifier for the gate type.

        Returns:
        - bool: True if successful, False if texture count exceeded limits.
        """
        data.IMAGE.add_gate_type(id)
        size: int = len(gate.inputs) + len(gate.outputs)

        # Log warnings for high complexity gates
        if size >= 12:
            logger.warning(
                f"Large Texture count found {2**size}, this might take a while."
            )

        if size > 16:
            logger.error("Texture size too large, aborting.")
            return False

        # Iterate through every possible bit combination of inputs and outputs
        for i in range(2**size):
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
        """
        Generate textures for all built-in gate types.

        Returns:
        - None
        """
        for g_id in gate_types:
            gate = gate_types[g_id]("default_id")
            self.bake_single_gate(gate, g_id)

    def bake_custom_gates(self) -> None:
        """
        Generate textures for all user-defined/loaded chips.

        Returns:
        - None
        """
        to_remove: List[str] = []

        for chip_id in data.loaded_chips:
            chip: Chip = data.loaded_chips[chip_id]
            new: CustomGate = CustomGate("no_id", chip.copy())
            result: bool = self.bake_single_gate(new, chip.id)
            if result == False:
                to_remove.append(chip_id)

        # Cleanup chips that could not be baked (e.g., too many I/Os)
        for i in to_remove:
            logger.warning(f"Chip {i} failed to load textures, removed from register.")
            del data.loaded_chips[i]

    def bake_level_buttons(self) -> None:
        """
        Generate unique textures for level selection buttons with their respective numbers.

        Returns:
        - None
        """
        font: ImageFont.FreeTypeFont = ImageFont.truetype(
            "assets/fonts/press_start.ttf", 32
        )

        for i in data.loaded_levels:
            level: Level = data.loaded_levels[i]
            # Format number to be 2 digits (e.g., "01")
            number: str = "0" * (2 - len(str(level.number))) + str(level.number)
            color: str = level.color

            new: Image.Image = Image.new("RGBA", (175, 175))
            # Paste the background button based on level color
            new.paste(
                data.level_buttons_empty[data.level_colors[color]].texture.image, (0, 0)
            )

            draw: ImageDraw.ImageDraw = ImageDraw.Draw(new)
            # Center the number text with a small shadow offset
            draw.text(
                (175 / 2, 175 / 2 - 16), number, font=font, fill="#000000", anchor="mm"
            )
            draw.text(
                (175 / 2, 175 / 2 - 20), number, font=font, fill="#FFFFFF", anchor="mm"
            )
            data.LEVEL_BUTTONS.set(level.id, new)

    def bake_textures(self) -> None:
        """
        Orchestrate the generation of all procedural textures.

        Returns:
        - None
        """
        logger.debug("Baking Textures")
        data.background_grid_texture = self._bake_grid(1920, 1088)
        self.bake_predefined_gates()
        self.bake_custom_gates()
        self.bake_level_buttons()

    def load_ui(self) -> None:
        """
        Load static UI assets and sprites from the assets directory.

        Returns:
        - None
        """
        # Load Main Menu and general buttons
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

        # Load Title and Info banners
        data.name_banner = arcade.Sprite("assets/titles/name_banner.png")
        data.level_info = arcade.Sprite("assets/titles/level_info.png")
        data.truth_table = arcade.Sprite("assets/titles/truth_table.png")

        # Load Borders
        data.editor_border = arcade.Sprite("assets/borders/editor_border.png")
        data.editor_border_no_bg = arcade.Sprite(
            "assets/borders/editor_border_no_bg.png"
        )
        data.level_player_border = arcade.Sprite(
            "assets/borders/level_player_border.png"
        )
        data.level_player_win = arcade.Sprite("assets/borders/level_player_win.png")
        data.border_small = arcade.Sprite("assets/borders/border_small.png")

        # Load Icons
        data.star = arcade.Sprite("assets/icons/star.png")
        data.star_empty = arcade.Sprite("assets/icons/star_empty.png")

        # Load empty button templates for coloring
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

        # Load Category Icons for the Editor
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

    def load(self) -> None:
        """
        The main entry point to trigger the full sequence of loading and baking assets.

        Returns:
        - None
        """
        logger.print("Loading Game Stuff.")

        try:
            self.load_fonts()
            self.load_tilesets()
            self.load_ui()
            self.load_saves()
            self.load_levels()

            # Resolve dependencies if any chips were buffered
            if len(self.to_load_buffer) > 0:
                self.load_saves_dependency()

            self.bake_textures()

            logger.success("Finished loading stuff.")
        except Exception:
            # Catching all to log the specific traceback for debugging
            logger.error(f"Failed to load stuff ({traceback.format_exc()})")
