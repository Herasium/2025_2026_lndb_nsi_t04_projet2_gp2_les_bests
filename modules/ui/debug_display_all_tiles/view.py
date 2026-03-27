import arcade
import math
from typing import List, Dict, Any, Optional
from modules.ui.toolbox.entity import Entity
from modules.data import data
from modules.logger import Logger

"""Fournit une vue spécialisée pour le rendu et l'interaction avec des jeux de tuiles (tilesets) basés sur une grille."""

logger = Logger("DebugTilesView")


class DebugTilesView(arcade.View):
    """Gère la logique de visualisation et de sélection pour plusieurs jeux de tuiles d'atouts."""

    def __init__(self) -> None:
        """Initialise l'état de la vue, la configuration de la grille et les définitions des jeux de tuiles."""
        super().__init__()

        self.grid_size: int = data.UI_EDITOR_GRID_SIZE

        self.follower: Entity = Entity()
        self.follower.height = self.grid_size
        self.follower.width = self.grid_size

        self.tilesets: List[Dict[str, Any]] = [
            {
                "name": "Gate Grid",
                "path": "assets/grid/gate_grid.png",
                "tile_w": 27,
                "tile_h": 27,
                "columns": 6,
                "count": 6 * 6,
                "textures": [],
            },
            {
                "name": "UI Grid",
                "path": "assets/grid/ui_grid.png",
                "tile_w": 32,
                "tile_h": 32,
                "columns": 23,
                "count": 9 * 23,
                "textures": [],
            },
            {
                "name": "UI Border Grid",
                "path": "assets/grid/ui_border_grid.png",
                "tile_w": 64,
                "tile_h": 64,
                "columns": 4,
                "count": 4 * 4,
                "textures": [],
            },
        ]

        self.load_tilesets()

        self.current_index: int = 0
        self.hovered_index: Optional[str] = None

        self.display_start_x: int = 500
        self.display_start_y: int = 500

    def load_tilesets(self) -> None:
        """Analyse les chemins des jeux de tuiles et extrait les grilles de textures pour chaque entrée."""
        for ts in self.tilesets:
            try:
                sheet = arcade.SpriteSheet(ts["path"])
                ts["textures"] = sheet.get_texture_grid(
                    size=(ts["tile_w"], ts["tile_h"]),
                    columns=ts["columns"],
                    count=ts["count"],
                )
            except Exception as e:
                logger.error(f"Error loading tileset {ts['name']}: {e}")
                ts["textures"] = []

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """Met à jour hovered_index en fonction des coordonnées actuelles de la souris.

        Args:
            x: Coordonnée horizontale de la souris sur l'écran.
            y: Coordonnée verticale de la souris sur l'écran.
            delta_x: Variation de la position horizontale de la souris.
            delta_y: Variation de la position verticale de la souris.
        """
        self.hovered_index = None

        current_set = self.tilesets[self.current_index]
        cols = current_set["columns"]
        total_count = current_set["count"]

        grid_x = (x - self.display_start_x) // self.grid_size
        grid_y = (y - self.display_start_y) // self.grid_size

        rows = math.ceil(total_count / cols)

        if 0 <= grid_x < cols and 0 <= grid_y < rows:
            index = int(grid_y * cols + grid_x)
            if 0 <= index < total_count:
                self.hovered_index = f"{current_set['name']} Index: {index}"

    def on_draw(self) -> None:
        """Affiche le jeu de tuiles actif, l'interface de la grille et les étiquettes de retour utilisateur."""
        self.clear()

        current_set = self.tilesets[self.current_index]
        textures = current_set["textures"]
        cols = current_set["columns"]

        arcade.draw_text(
            f"Current Set: {current_set['name']} (Arrow Keys to Switch)",
            self.display_start_x,
            self.display_start_y + (len(textures) // cols * self.grid_size) + 50,
            arcade.color.WHITE,
            14,
        )

        for i, texture in enumerate(textures):
            column_x = i % cols
            row_y = i // cols

            tile_x = column_x * self.grid_size + self.display_start_x
            tile_y = row_y * self.grid_size + self.display_start_y

            rect = arcade.XYWH(
                x=tile_x,
                y=tile_y,
                width=self.grid_size,
                height=self.grid_size,
                anchor=arcade.Vec2(0, 0),
            )

            arcade.draw_texture_rect(texture, rect)

        if self.hovered_index is not None:
            arcade.draw_text(
                f"Hovered: {self.hovered_index}", 10, 10, arcade.color.CYAN, 16
            )

    def on_update(self, delta_time: float) -> None:
        """Structure pour la logique de mise à jour spécifique à chaque image (frame)."""
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Traite les touches de navigation pour la sélection des jeux de tuiles et le contrôle de l'application.

        Args:
            key: Le code de la touche déclenchée.
            key_modifiers: Masque de bits des touches de modification actives.
        """
        if key == arcade.key.ESCAPE:
            self.current_path = None
            self.selected_follower = None

        elif key == arcade.key.A:
            arcade.exit()

        elif key == arcade.key.RIGHT:
            # Retour au début si l'on dépasse les limites
            self.current_index = (self.current_index + 1) % len(self.tilesets)
            logger.debug(f"Switched to: {self.tilesets[self.current_index]['name']}")

        elif key == arcade.key.LEFT:
            # Retour à la fin si l'on descend en dessous de zéro
            self.current_index = (self.current_index - 1) % len(self.tilesets)
            logger.debug(f"Switched to: {self.tilesets[self.current_index]['name']}")

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """Structure pour les événements de relâchement de touche du clavier."""
        pass

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Structure pour les événements de pression des boutons de la souris."""
        pass

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Structure pour les événements de relâchement des boutons de la souris."""
        pass