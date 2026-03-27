"""Fournit la vue SaveFrame pour l'édition et la sauvegarde des données de configuration de la puce."""

import arcade
from typing import Any

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text
from modules.ui.toolbox.entity import Entity
from modules.ui.toolbox.keys import apply_key
from modules.data import data


class SaveFrame(arcade.View):
    """Gère la disposition de l'interface utilisateur et les interactions pour l'édition des propriétés de la puce."""

    def __init__(self, chip: Any) -> None:
        """Initialise l'instance SaveFrame.

        Args:
            chip: L'objet de configuration contenant les données de la puce à modifier.
        """
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK
        self.chip: Any = chip
        self.typing: bool = False
        self.current_text = "Puce par défaut"

        self.setup()

    def setup(self) -> None:

        self.bg = Entity(
            0,
            0,
            data.WINDOW_WIDTH,
            (((data.WINDOW_HEIGHT + 32) // 64) * 64),
            arcade.Sprite(data.background_grid_texture),
        )
        self.border = Entity(0, 0, data.WINDOW_WIDTH, 960, data.border_small)
        self.title = Entity(0, 952, data.WINDOW_WIDTH, 128, data.name_banner)
        self.chip_save = Entity(
            data.WINDOW_WIDTH / 2 - 896 / 2, 700, 896, 128, data.chip_save
        )
        self.chip_name = Text(
            x=data.WINDOW_WIDTH / 2 - 200,
            y=data.WINDOW_HEIGHT / 2,
            width=500,
            height=200,
            text=self.current_text,
            align=("left", "center"),
        )
        self.save_button = Entity(
            x=data.WINDOW_WIDTH / 2 - 262.5 / 2,
            y=data.WINDOW_HEIGHT / 2 - 400,
            width=262.5,
            height=150,
            sprite=data.button_save,
        )
        self.sub_title = Text(
            x=data.WINDOW_WIDTH / 2 - 200,
            y=data.WINDOW_HEIGHT / 2 + 30,
            width=500,
            height=200,
            text="Nom de la puce (Cliquer pour éditer.)",
            align=("left", "center"),
            size=12,
        )

        self.chip_id = Text(
            x=data.WINDOW_WIDTH / 2,
            y=data.WINDOW_HEIGHT / 2 - 100,
            width=500,
            height=200,
            text=f"ID Puce : {self.chip.id}",
            align=("center", "center"),
            size=18,
        )
        self.chip_version = Text(
            x=data.WINDOW_WIDTH / 2,
            y=data.WINDOW_HEIGHT / 2 - 150,
            width=500,
            height=200,
            text=f"Version Puce : {data.VERSION}",
            align=("center", "center"),
            size=18,
        )

        self.typing_collider = Entity(
            x=data.WINDOW_WIDTH / 2 - 250,
            y=data.WINDOW_HEIGHT / 2 - 50,
            width=500,
            height=100,
        )

    def reset(self) -> None:
        """Réinitialise l'état interne de la vue."""
        pass

    def on_draw(self) -> None:
        """Affiche tous les éléments textuels configurés de l'interface utilisateur."""
        self.clear()
        self.bg.draw()
        self.border.draw()
        self.title.draw()
        self.chip_save.draw()
        self.chip_name.draw()
        self.save_button.draw()
        self.sub_title.draw()
        self.chip_id.draw()
        self.chip_version.draw()

        if self.typing:
            arcade.draw_line(
                data.WINDOW_WIDTH / 2 - 200,
                data.WINDOW_HEIGHT / 2 - 20,
                data.WINDOW_WIDTH / 2 + 200,
                data.WINDOW_HEIGHT / 2 - 20,
                arcade.color.RED,
                2,
            )
        else:
            arcade.draw_line(
                data.WINDOW_WIDTH / 2 - 200,
                data.WINDOW_HEIGHT / 2 - 20,
                data.WINDOW_WIDTH / 2 + 200,
                data.WINDOW_HEIGHT / 2 - 20,
                arcade.color.WHITE,
                2,
            )

    def on_update(self, delta_time: float) -> None:
        """Gère les mises à jour logiques périodiques."""
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Gère les événements de pression de touches du clavier.

        Args:
            key: L'identifiant de la touche pressée.
            key_modifiers: Drapeaux binaires pour les touches de modification.
        """
        if self.typing:
            if key == data.keys.back:
                self.typing = False
                return
            self.current_text = apply_key(self.current_text, key, key_modifiers)[:17]
            self.chip_name.text = self.current_text
        if key == data.keys.back:
            data.window.back()
        if key == 65473:  # Sortie de secours : F4
            arcade.exit()

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """Gère les événements de relâchement de touches."""
        pass

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """Met à jour l'état global du suivi de la souris.

        Args:
            x: Coordonnée x actuelle de la souris.
            y: Coordonnée y actuelle de la souris.
            delta_x: Variation de la coordonnée x depuis la dernière image.
            delta_y: Variation de la coordonnée y depuis la dernière image.
        """
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Traite les interactions par clic de souris avec les éléments de l'interface.

        Args:
            x: Coordonnée x du clic de souris.
            y: Coordonnée y du clic de souris.
            button: Le bouton de la souris pressé.
            key_modifiers: Drapeaux binaires pour les touches de modification.
        """

        if self.typing_collider.touched:
            self.typing = not self.typing

        if self.save_button.touched:
            self.chip.name = self.current_text
            self.chip.save()
            data.window.back()

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Gère les événements de relâchement du bouton de la souris."""
        pass