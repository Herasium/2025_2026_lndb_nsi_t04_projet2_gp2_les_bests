"""Fournit la gestion des fenêtres et l'état de navigation des vues pour l'application LogicBox."""

import arcade
from modules.data import data
from typing import List
from modules.logger import Logger

logger: Logger = Logger("Window")


class Window:
    """Gère la fenêtre principale de l'application et fournit un système de navigation basé sur une pile."""

    def __init__(self) -> None:
        """Initialise l'instance de la fenêtre avec les paramètres de configuration et l'état de navigation."""
        self.width: int = data.WINDOW_WIDTH
        self.height: int = data.WINDOW_HEIGHT
        self.title: str = "LogicBox"

        self.window: arcade.Window = arcade.Window(
            self.width,
            self.height,
            self.title,
            fullscreen=data.WINDOW_FULLSCREEN,
            # Définit les taux de mise à jour et de rendu à environ 60 FPS
            update_rate=1 / data.WINDOW_FRAMERATE,
            draw_rate=1 / data.WINDOW_FRAMERATE,
        )

        self.view_history: List[arcade.View] = []

    def back(self) -> None:
        """Navigue vers la vue précédente dans la pile d'historique."""
        if len(self.view_history) < 2:
            logger.warning("No view to go back to. Doing Nothing.")
            return
        self.view_history.pop()
        view: arcade.View = self.view_history[-1]
        self.window.show_view(view)

    def first(self) -> None:
        """Réinitialise la navigation vers la vue initiale et vide la pile d'historique."""
        view: arcade.View = self.view_history[0]
        self.window.show_view(view)
        self.view_history = []

    def run(self) -> None:
        """Lance la boucle d'événements principale de l'application."""
        arcade.run()

    def display(self, view: arcade.View) -> None:
        """Ajoute une nouvelle vue à la pile d'historique et l'affiche.

        Args:
            view: L'instance de la vue à afficher.
        """
        self.view_history.append(view)
        self.window.show_view(view)

    def hide(self) -> None:
        """Masque la vue actuellement active."""
        self.window.hide_view()