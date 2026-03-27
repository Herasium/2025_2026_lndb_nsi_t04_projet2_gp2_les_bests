import arcade
from typing import List

from modules.ui.mouse import mouse
from modules.ui.toolbox.button import Button
from modules.ui.editor.view import EditorView
from modules.ui.debug_display_all_tiles.view import DebugTilesView
from modules.ui.main_menu.in_progress_view import MainMenuView

from modules.data import data

"""Ancien menu, n'est plus utilisé."""


class GameView(arcade.View):
    """Gère la disposition, le rendu et la logique d'interaction du menu principal."""

    def __init__(self) -> None:
        """Initialise les éléments de l'interface utilisateur, les ressources et les paramètres d'affichage."""
        super().__init__()

        self.background_color: arcade.color = arcade.color.JET

        self.ui_sheet: arcade.SpriteSheet = arcade.SpriteSheet("assets/ui_grid.png")
        self.ui_tiles: List[arcade.Texture] = self.ui_sheet.get_texture_grid(
            size=(32, 32),
            columns=23,
            count=9 * 23,
        )

        self.button_play: Button = Button(self.ui_tiles)
        self.button_play.x = 120
        self.button_play.y = 540
        self.button_play.width = 340
        self.button_play.height = 90
        self.button_play.name = "Jouer"

        self.button_quit: Button = Button(self.ui_tiles)
        self.button_quit.x = 120
        self.button_quit.y = 400
        self.button_quit.width = 340
        self.button_quit.height = 90
        self.button_quit.name = "Quitter"

        self.titre1: arcade.Text = arcade.Text(
            "Welcome to",
            x=120,
            y=760,
            color=arcade.color.BLOND,
            font_size=60,
            font_name="Press Start 2P",
        )
        self.shadow_titre1: arcade.Text = arcade.Text(
            "Welcome to",
            x=120,
            y=754,
            color=arcade.color.DEEP_SAFFRON,
            font_size=60,
            font_name="Press Start 2P",
        )
        self.titreL: arcade.Text = arcade.Text(
            "LogicBox",
            x=120,
            y=640,
            color=arcade.color.BLOND,
            font_size=60,
            font_name="Press Start 2P",
        )
        self.shadow_titreL: arcade.Text = arcade.Text(
            "LogicBox",
            x=120,
            y=634,
            color=arcade.color.DEEP_SAFFRON,
            font_size=60,
            font_name="Press Start 2P",
        )

    def reset(self) -> None:
        """Réinitialise l'état de la vue."""
        pass

    def on_draw(self) -> None:
        """Affiche les composants de l'interface utilisateur à l'écran."""
        self.clear()
        self.button_play.draw()
        self.button_quit.draw()
        self.shadow_titre1.draw()
        self.titre1.draw()
        self.shadow_titreL.draw()
        self.titreL.draw()

    def on_update(self, delta_time: float) -> None:
        """Met à jour la logique de la vue."""
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """
        Arguments:
            key: L'identifiant numérique de la touche pressée.
            key_modifiers: Drapeaux binaires représentant les touches de modification actives.
        """
        if key == 97:
            arcade.exit()

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """
        Arguments:
            key: L'identifiant numérique de la touche relâchée.
            key_modifiers: Drapeaux binaires représentant les touches de modification actives.
        """
        pass

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """
        Arguments:
            x: Coordonnée horizontale de la souris sur l'écran.
            y: Coordonnée verticale de la souris sur l'écran.
            delta_x: Variation de la position horizontale.
            delta_y: Variation de la position verticale.
        """
        mouse.position = (x, y)

        if self.button_play.rect.point_in_rect((x, y)):
            self.button_play.scale = 1.1
        else:
            self.button_play.scale = 1.0

        if self.button_quit.rect.point_in_rect((x, y)):
            self.button_quit.scale = 1.1
        else:
            self.button_quit.scale = 1.0

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """
        Arguments:
            x: Coordonnée horizontale du clic sur l'écran.
            y: Coordonnée verticale du clic sur l'écran.
            button: Le bouton de la souris pressé.
            key_modifiers: Drapeaux binaires représentant les touches de modification actives.
        """
        if self.button_play.touched:
            data.window.hide()
            # Routage de la navigation basé sur les masques de bits des touches de modification
            if key_modifiers == 16 or key_modifiers == 0:
                data.window.display(EditorView())
            elif key_modifiers == 17 or key_modifiers == 1:
                data.window.display(DebugTilesView())
            elif key_modifiers == 2 or key_modifiers == 18:
                data.window.display(MainMenuView())
            else:
                data.window.display(EditorView())

        if self.button_quit.touched:
            arcade.exit()

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """
        Arguments:
            x: Coordonnée horizontale du relâchement sur l'écran.
            y: Coordonnée verticale du relâchement sur l'écran.
            button: Le bouton de la souris relâché.
            key_modifiers: Drapeaux binaires représentant les touches de modification actives.
        """
        pass