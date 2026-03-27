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
Ce module gère l'initialisation, le chargement des ressources et la génération 
procédurale de textures pour l'architecture orientée données du jeu.
"""

logger: Logger = Logger("Loader")


class Loader:
    """
    Gère le chargement des ressources JSON externes, des ressources de logique de jeu,
    ainsi que la génération des textures procédurales de l'interface utilisateur.
    """

    def __init__(self) -> None:
        """Initialise le chargeur avec un tampon pour les dépendances non résolues."""
        self.to_load_buffer: List[Chip] = []

    def load_files(self, sub_folder: str) -> List[Dict[str, Any]]:
        """
        Lit tous les fichiers JSON d'un sous-répertoire spécifié.

        Args:
            sub_folder: Le chemin du répertoire relatif à la racine des données.

        Returns:
            Une liste contenant le contenu analysé de chaque fichier JSON.
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
                logger.error(f"Échec de la lecture du fichier {full_path} ({e})")

        return results

    def load_single_chip(self, raw_data: Dict[str, Any]) -> None:
        """
        Enregistre un objet puce (chip) et gère ses besoins en dépendances.

        Args:
            raw_data: Le dictionnaire de configuration pour la puce.
        """
        chip: Chip = Chip("default_id")
        chip.partial_load(raw_data)

        if len(chip.requirements) == 0:
            chip.load()
            if len(chip.get_inputs()) + len(chip.get_outputs()) == 0:
                logger.warning(f"Puce {chip} vide, chargement annulé.")
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
                    logger.warning(f"Puce {chip} vide, chargement annulé.")
                    return
                data.loaded_chips[raw_data["id"]] = chip
            else:
                self.to_load_buffer.append(chip)

    def load_saves(self) -> None:
        """Charge et traite toutes les configurations de puces sauvegardées."""
        for raw_data in self.load_files("saves"):
            try:
                self.load_single_chip(raw_data)
            except Exception:
                logger.error(f"Échec du chargement de la puce : {traceback.format_exc()}")

        logger.success(f"{len(data.loaded_chips)} puces chargées.")
        if len(self.to_load_buffer):
            logger.info(
                f"Chargement des puces non terminé, {len(self.to_load_buffer)} puces avec des dépendances restent à charger."
            )

    def load_saves_dependency_round(self) -> None:
        """Effectue une seule passe de résolution sur les puces en tampon."""
        for chip in self.to_load_buffer[:]:
            can_load: bool = True
            for i in chip.requirements:
                if i not in data.loaded_chips:
                    can_load = False
                    break

            if can_load:
                chip.load()
                if len(chip.get_inputs()) + len(chip.get_outputs()) == 0:
                    logger.warning(f"Puce {chip} vide, chargement annulé.")
                    return
                self.to_load_buffer.remove(chip)
                data.loaded_chips[chip.id] = chip

    def load_saves_dependency(self) -> None:
        """Résout itérativement les dépendances jusqu'à ce que toutes les puces soient chargées ou que la limite soit atteinte."""
        max_count: int = 1000
        count: int = 0
        previous: int = len(self.to_load_buffer)

        while count < max_count and len(self.to_load_buffer) > 0:
            self.load_saves_dependency_round()

            if len(self.to_load_buffer) == previous:
                logger.error(
                    f"Échec du chargement de {len(self.to_load_buffer)} portes avec dépendances, peut-être dû à une dépendance circulaire ou des puces manquantes."
                )
                break
            else:
                previous = len(self.to_load_buffer)
            count += 1

        logger.debug(f"Chargement des portes avec dépendances terminé en {count} itérations.")

    def load_levels(self) -> None:
        """Charge toutes les définitions de niveaux et leurs ressources requises."""
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
                logger.error(f"Échec du chargement du niveau : {traceback.format_exc()}")

        logger.success(f"{len(data.loaded_levels)} niveaux chargés.")

    def load_fonts(self) -> None:
        """Enregistre les polices TTF externes dans le moteur de rendu."""
        try:
            arcade.load_font("assets/fonts/press_start.ttf")
            logger.success("Polices chargées (1).")
        except Exception as e:
            logger.error(f"Échec du chargement des polices ({e}).")

    def load_tilesets(self) -> None:
        """Découpe les feuilles de sprites en grilles de textures pour les composants de l'interface."""
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
        Génère une texture de grille d'arrière-plan répétitive.

        Args:
            width_px: Largeur totale cible.
            height_px: Hauteur totale cible.

        Returns:
            La texture générée compatible avec arcade.
        """
        img: Image.Image = Image.new("RGBA", (width_px, height_px))
        tile: Image.Image = data.ui_border_tiles[9].image
        for y in range(0, height_px, 64):
            for x in range(0, width_px, 64):
                img.paste(tile, (x, y))
        return arcade.Texture(img)

    def _bake_border(self, width_px: int, rows: int) -> arcade.Texture:
        """
        Génère un cadre de bordure d'interface de taille personnalisée.

        Args:
            width_px: Largeur du cadre.
            rows: Nombre de rangées de tuiles verticales.

        Returns:
            La texture de cadre générée.
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
        Génère une image composite pour une porte, incluant les tuiles et les étiquettes de texte.

        Args:
            gate: Le composant porte à restituer.

        Returns:
            L'image PIL générée.
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
        Met en cache les textures spécifiques aux états pour une porte afin d'optimiser les performances.

        Args:
            gate: L'instance de la porte.
            id: Identifiant unique de la porte.

        Returns:
            True si la génération a réussi, False si la complexité des entrées/sorties dépasse les limites.
        """
        data.IMAGE.add_gate_type(id)
        size: int = len(gate.inputs) + len(gate.outputs)

        if size >= 12:
            logger.warning(
                f"Grand nombre de textures détecté {2**size}, cela pourrait prendre un certain temps."
            )

        if size > 16:
            logger.error("Taille de texture trop importante, abandon.")
            return False

        for i in range(2**size):
            # Calcul des états d'entrée/sortie en utilisant l'extraction par indicateurs bit à bit
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
        """Génère les textures pour toutes les portes système prédéfinies."""
        for g_id in gate_types:
            gate = gate_types[g_id]("default_id")
            self.bake_single_gate(gate, g_id)

    def bake_custom_gates(self) -> None:
        """Génère les textures pour les puces personnalisées définies par l'utilisateur."""
        to_remove: List[str] = []

        for chip_id in data.loaded_chips:
            chip: Chip = data.loaded_chips[chip_id]
            new: CustomGate = CustomGate("no_id", chip.copy())
            result: bool = self.bake_single_gate(new, chip.id)
            if not result:
                to_remove.append(chip_id)

        for i in to_remove:
            logger.warning(f"La puce {i} n'a pas pu charger ses textures, retrait du registre.")
            del data.loaded_chips[i]

    def bake_level_buttons(self) -> None:
        """Génère des boutons visuels uniques pour chaque niveau de jeu disponible."""
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
        """Coordonne l'ensemble du flux de génération de textures procédurales."""
        logger.debug("Génération des textures en cours (Baking)")
        data.background_grid_texture = self._bake_grid(
            data.WINDOW_WIDTH, (((data.WINDOW_HEIGHT + 32) // 64) * 64)
        )
        self.bake_predefined_gates()
        self.bake_custom_gates()
        self.bake_level_buttons()

    def load_ui(self) -> None:
        """Charge et initialise les ressources statiques de l'interface."""
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
        data.button_answer = arcade.Sprite("assets/buttons/button_answer.png")

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
        data.level_buttons_empty["blue"] = arcade.Sprite(
            "assets/buttons/levels/blue.png"
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
        """Exécute l'intégralité du pipeline de chargement des ressources et d'initialisation."""
        logger.print("Chargement des ressources du jeu.")

        try:
            self.load_fonts()
            self.load_tilesets()
            self.load_ui()
            self.load_saves()
            self.load_levels()

            if len(self.to_load_buffer) > 0:
                self.load_saves_dependency()

            self.bake_textures()

            logger.success("Chargement des ressources terminé.")
        except Exception:
            logger.error(f"Échec du chargement des ressources ({traceback.format_exc()})")