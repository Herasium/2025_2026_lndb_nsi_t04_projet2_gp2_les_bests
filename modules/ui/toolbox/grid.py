"""Fournit des utilitaires de rendu de grille pour l'environnement de l'éditeur d'interface utilisateur."""

import arcade
from modules.data import data


class Grid:
    """Gère la superposition de la grille de points visuelle pour l'interface de l'éditeur d'interface utilisateur."""

    def __init__(self) -> None:
        """Initialise la configuration de la grille en utilisant les constantes du module data."""
        self.size: int = data.UI_EDITOR_GRID_SIZE

    def draw(self) -> None:
        """Affiche une grille de points sur la zone de l'espace de travail de 1280x720."""
        for y in range(0, 720, self.size):
            for x in range(0, 1280, self.size):
                arcade.draw_point(x, y, arcade.color.DARK_BLUE_GRAY, 5)