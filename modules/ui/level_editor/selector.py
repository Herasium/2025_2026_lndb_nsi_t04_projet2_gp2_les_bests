import arcade
from typing import List, Any

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text
from modules.ui.toolbox.id_generator import random_id

from modules.data import data
from modules.data.level import Level


from modules.ui.editor.view import EditorView
from modules.ui.level_player.selector import LevelPlayerSelector

"""
Fournit la classe LevelEditorSelector pour la gestion des flux de sélection 
et de création de niveaux au sein de l'application arcade.
"""


class LevelEditorSelector(arcade.View):
    """
    Gère la vue de l'interface utilisateur pour parcourir les niveaux existants ou en créer de nouveaux.
    """

    def __init__(self) -> None:
        """
        Initialise la vue avec la couleur d'arrière-plan par défaut et les structures de conteneurs.
        """
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK
        self.texts: List[Text] = []
        self.levels: List[Any] = []
        self.camera: int = 0
        self.setup()

    def setup(self) -> None:
        """
        Remplit les étiquettes de l'interface et initialise les objets d'interaction pour les niveaux.
        """
        debug_list: List[str] = [
            "Sélecteur d'Éditeur de Niveau",
            "<- Retour",
            "+ Nouveau +",
            "Sélecteur de Niveau de Jeu",
            "",
        ]
        self.texts: List[Text] = []
        self.levels: List[Any] = []
        

        for i in data.loaded_levels:
            level = data.loaded_levels[i]
            debug_list.append(f"Niveau {level.number} {level.name} #{level.id}")
            self.levels.append(i)

        start_y: int = data.WINDOW_HEIGHT - 70 + self.camera

        for index, item in enumerate(debug_list):
            self.texts.append(Text())
            self.texts[-1].x = 64
            self.texts[-1].y = start_y - (index * 25)
            self.texts[-1].text = item
            self.texts[-1].align = ("left", "center")

    def reset(self) -> None:
        """
        Réinitialise l'état actuel de la vue.
        """
        pass

    def on_draw(self) -> None:
        """
        Rendu de tous les éléments textuels de l'interface et de leurs zones de collision (hitboxes) associées.
        """
        self.clear()

        for i in self.texts:
            i.draw()
            i.hitbox.draw()

    def on_update(self, delta_time: float) -> None:
        """
        Met à jour la logique à chaque image.

        Args:
            delta_time: Temps écoulé depuis la mise à jour précédente.
        """
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """
        Gère les événements de pression de touches du clavier.

        Args:
            key: Identifiant entier de la touche pressée.
            key_modifiers: Masque de bits des touches modificatrices actuellement maintenues.
        """
        if key == 97:
            arcade.exit()

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """
        Gère les événements de relâchement de touches du clavier.

        Args:
            key: Identifiant entier de la touche relâchée.
            key_modifiers: Masque de bits des touches modificatrices actuellement maintenues.
        """
        pass

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """
        Met à jour l'état global du suivi de la souris.

        Args:
            x: Position horizontale actuelle de la souris.
            y: Position verticale actuelle de la souris.
            delta_x: Changement de position en x.
            delta_y: Changement de position en y.
        """
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """
        Déclenche la navigation dans l'interface basée sur l'interaction avec les zones de collision du texte.

        Args:
            x: Position horizontale actuelle de la souris.
            y: Position verticale actuelle de la souris.
            button: Identifiant du bouton de la souris pressé.
            key_modifiers: Masque de bits des touches modificatrices actuellement maintenues.
        """
        for index in range(len(self.texts)):
            text = self.texts[index]

            if text.touched:
                if index > 4:
                    data.window.display(
                        EditorView(level=data.loaded_levels[self.levels[index - 5]])
                    )
                elif index == 1:
                    data.window.back()
                elif index == 2:
                    data.window.display(EditorView(level=Level(random_id())))
                elif index == 3:
                    data.window.display(LevelPlayerSelector())

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """
        Gère les événements de relâchement du bouton de la souris.

        Args:
            x: Position horizontale actuelle de la souris.
            y: Position verticale actuelle de la souris.
            button: Identifiant du bouton de la souris relâché.
            key_modifiers: Masque de bits des touches modificatrices actuellement maintenues.
        """
        pass
        
    def on_mouse_scroll(
        self, x: float, y: float, scroll_x: float, scroll_y: float
    ) -> None:
        """Met à jour le décalage vertical de la caméra et reconstruit la mise en page."""
        self.camera += scroll_y * -data.MOUSE_SENSI
        self.camera = max(self.camera, 0)

        self.setup()