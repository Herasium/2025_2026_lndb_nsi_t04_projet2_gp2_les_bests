"""Fournit la vue SaveFrame pour l'édition et la sauvegarde des données de configuration de niveau."""

import arcade
from typing import Any, Dict, List

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text
from modules.data import data


class SaveFrame(arcade.View):
    """Gère la disposition de l'interface utilisateur et les interactions pour l'édition des propriétés de niveau."""

    def __init__(self, level: Any) -> None:
        """Initialise l'instance SaveFrame.

        Args:
            level: L'objet de configuration contenant les données de niveau à modifier.
        """
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK
        self.texts: List[Text] = []
        self.level: Any = level
        self.setup()

    def setup(self) -> None:
        """Initialise et positionne les éléments textuels de l'interface basés sur les données actuelles du niveau."""
        self.texts = []
        debug_list: List[str] = [
            "Sauvegarde du Niveau",
            "<- Retour",
            "--------------",
            # Les noms de variables (id, name) restent inchangés mais le texte environnant est traduit
            f"Niveau {self.level.id} {self.level.name}",
            "Description du Niveau : ",
            self.level.description,
            "--------------",
            f"Temps du Niveau : {self.level.time}",
            "+ 30 sec",
            " - 30 sec",
            "--------------",
            f"Numéro du Niveau : {self.level.number}",
            "+ 1",
            "- 1",
            "--------------",
            f"Catégorie du Niveau : {self.level.category}",
            "+ 1",
            "- 1",
            "--------------",
            f"Couleur du Niveau : {data.level_colors[self.level.color]}",
            "-> Suivant",
            f"Puce Personnalisée Publique : {self.level.is_custom}",
            "-> Changer",
            "--> Sauvegarder <--",
        ]

        start_y: int = data.WINDOW_HEIGHT - 70

        for index, item in enumerate(debug_list):
            self.texts.append(Text())
            self.texts[-1].x = 64
            self.texts[-1].y = start_y - (index * 25)
            self.texts[-1].text = item
            self.texts[-1].align = ("left", "center")

    def reset(self) -> None:
        """Réinitialise l'état interne de la vue."""
        pass

    def on_draw(self) -> None:
        """Rendu de tous les éléments textuels configurés de l'interface utilisateur."""
        self.clear()
        for i in self.texts:
            i.draw()

    def on_update(self, delta_time: float) -> None:
        """Gère les mises à jour logiques périodiques."""
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Gère les événements de pression de touches du clavier.

        Args:
            key: L'identifiant de la touche pressée.
            key_modifiers: Drapeaux binaires pour les touches de modification.
        """
        if key == 97:
            arcade.exit()

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """Gère les événements de relâchement de touches."""
        pass

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """Met à jour l'état global du suivi de la souris.

        Args:
            x: La coordonnée x actuelle de la souris.
            y: La coordonnée y actuelle de la souris.
            delta_x: La variation de la coordonnée x depuis la dernière image.
            delta_y: La variation de la coordonnée y depuis la dernière image.
        """
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Traite les interactions de clic de souris avec les éléments de l'interface.

        Args:
            x: La coordonnée x du clic de souris.
            y: La coordonnée y du clic de souris.
            button: Le bouton de la souris pressé.
            key_modifiers: Drapeaux binaires pour les touches de modification.
        """
        if self.texts[1].touched:
            data.window.back()

        if self.texts[8].touched:
            self.level.time += 30
            self.setup()
        if self.texts[9].touched:
            self.level.time -= 30
            self.setup()

        if self.texts[12].touched:
            self.level.number += 1
            self.setup()
        if self.texts[13].touched:
            self.level.number -= 1
            self.setup()

        if self.texts[16].touched:
            self.level.category += 1
            self.setup()
        if self.texts[17].touched:
            self.level.category -= 1
            self.setup()

        if self.texts[20].touched:
            self.level.color = (self.level.color + 1) % len(data.level_colors)
            self.setup()
        if self.texts[22].touched:
            self.level.is_custom = not self.level.is_custom
            self.setup()
        if self.texts[23].touched:
            self.level.save()

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """Gère les événements de relâchement du bouton de la souris."""
        pass

    def get_save_gate_counts(self) -> Dict[Any, int]:
        """Calcule la fréquence des types de portes utilisés dans le niveau actuel.

        Returns:
            Un dictionnaire associant des types de portes spécifiques à leur nombre total d'occurrences.
        """
        result: Dict[Any, int] = {}
        for i in self.level.chip.gates:
            gate_type = self.level.chip.gates[i].gate_type
            if gate_type not in result:
                result[gate_type] = 0
            result[gate_type] += 1
        return result