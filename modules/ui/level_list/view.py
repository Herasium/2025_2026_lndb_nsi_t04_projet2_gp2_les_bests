"""Fournit une vue pour la navigation et la sélection des niveaux de jeu."""

import arcade
from typing import List, Dict, Any

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text
from modules.ui.toolbox.entity import Entity
from modules.data import data
from modules.ui.level_player.view import LevelPlayer
from modules.logger import Logger

logger: Logger = Logger("LevelList")


class LevelList(arcade.View):
    """Affiche une liste défilante et catégorisée de niveaux sélectionnables."""

    def __init__(self) -> None:
        """Initialise la vue avec les éléments d'interface utilisateur et l'état par défaut."""
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK
        self.texts: List[Text] = []
        self.levels: List[Any] = []
        self.camera_y: float = 0.0

        self.bg: Entity = None  # type: ignore
        self.border: Entity = None  # type: ignore
        self.title: Entity = None  # type: ignore
        self.buttons: Dict[str, Entity] = {}

        self.setup()

    def setup(self) -> None:
        """Construit la disposition de l'interface, organise les niveaux par catégories et initialise les boutons."""
        self.bg = Entity(
            0,
            0,
            data.WINDOW_WIDTH,
            (((data.WINDOW_HEIGHT + 32) // 64) * 64),
            arcade.Sprite(data.background_grid_texture),
        )
        self.border = Entity(0, 0, data.WINDOW_WIDTH, 960, data.border_small)
        self.title = Entity(0, 952, data.WINDOW_WIDTH, 128, data.name_banner)

        self.back_button = Entity(
            x=1680, y=100, width=160, height=100, sprite=data.button_back
        )

        self.buttons = {}
        self.texts = []

        levels: List[str] = list(data.loaded_levels.keys())

        def sort_keys(i: str) -> int:
            """Détermine l'ordre de tri en fonction du numéro de séquence du niveau."""
            return data.loaded_levels[i].number

        levels.sort(key=sort_keys)

        pos_y: float = 600 + self.camera_y
        pos_x: float = 75

        current_category: str = data.loaded_levels[levels[0]].category

        for i in levels:
            level = data.loaded_levels[i]

            if level.category != current_category:
                pos_y -= 300
                pos_x = 75
                current_category = level.category

            button = arcade.Sprite(arcade.Texture(data.LEVEL_BUTTONS.get(level.id)))

            self.buttons[level.id] = Entity(
                x=pos_x, y=pos_y, width=175, height=175, sprite=button
            )
            pos_x += 200

        c: int = 0
        for i in data.categories:
            self.texts.append(
                Text(
                    x=75,
                    y=800 - c * 300 + self.camera_y,
                    width=100,
                    height=300,
                    text=i,
                    align=("left", "center"),
                )
            )
            c += 1

    def reset(self) -> None:
        """Réinitialise la vue à son état initial."""
        pass

    def on_draw(self) -> None:
        """Affiche l'arrière-plan, les boutons de niveau, les étiquettes de catégorie et l'interface utilisateur."""
        self.clear()
        self.bg.draw()

        for i in self.buttons:
            self.buttons[i].draw()

        for i in self.texts:
            i.draw()

        self.border.draw()
        self.title.draw()
        self.back_button.draw()

    def on_update(self, delta_time: float) -> None:
        """Effectue les mises à jour logiques à chaque image."""
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Gère les entrées de navigation clavier."""
        if key == data.keys.back:
            data.window.display(data.main)
        if key == 65473:  # Sortie d'urgence : F4
            arcade.exit()

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """Gère les événements de relâchement de touches."""
        pass

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """Met à jour l'état global du suivi de la souris."""
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Détecte les clics de sélection de niveau et lance la transition de scène."""
        for i in self.buttons:
            if self.buttons[i].touched:
                logger.success(f"Launching Level {i}")
                data.window.display(LevelPlayer(i))

        if self.back_button.touched:
            data.window.display(data.main)

    def on_mouse_scroll(
        self, x: float, y: float, scroll_x: float, scroll_y: float
    ) -> None:
        """Met à jour le décalage vertical de la caméra et reconstruit la disposition."""
        self.camera_y += scroll_y * -data.MOUSE_SENSI
        self.camera_y = max(self.camera_y, 0)
        self.setup()

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Gère les événements de relâchement de la souris."""
        pass