import arcade
from typing import List, Any

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text
from modules.data import data
from modules.ui.editor.view import EditorView

"""Module de gestion de l'interface de sélection de puces au sein de l'éditeur."""


class EditorChipSelector(arcade.View):
    """Fournit un menu de sélection pour les puces existantes et la navigation vers l'éditeur."""

    def __init__(self) -> None:
        """Initialise la vue et génère les composants de l'interface utilisateur."""
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK
        self.texts: List[Text] = []
        self.chips: List[Any] = []
        self.setup()

    def setup(self) -> None:
        """Configure les éléments initiaux de l'interface et liste les puces disponibles."""
        debug_list: List[str] = ["Sélecteur d'éditeur de puces", "<- Retour", "+ Nouveau +", ""]

        for i in data.loaded_chips:
            chip = data.loaded_chips[i]
            debug_list.append(f"Puce #{chip.id}")
            self.chips.append(i)

        start_y: int = data.WINDOW_HEIGHT - 70

        for index, item in enumerate(debug_list):
            self.texts.append(Text())
            self.texts[-1].x = 64
            self.texts[-1].y = start_y - (index * 25)
            self.texts[-1].text = item
            self.texts[-1].align = ("left", "center")

    def reset(self) -> None:
        """Réinitialise l'état de la vue."""
        pass

    def on_draw(self) -> None:
        """Rendu des éléments de l'interface et de leurs zones de collision (hitboxes) associées."""
        self.clear()

        for i in self.texts:
            i.draw()
            i.hitbox.draw()

    def on_update(self, delta_time: float) -> None:
        """Met à jour la logique à chaque image.

        Args:
            delta_time: Temps écoulé depuis la dernière image.
        """
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """Gère les entrées clavier.

        Args:
            key: Le code de la touche pressée.
            key_modifiers: Modificateurs de touches bitwise actifs.
        """
        if key == 97:
            arcade.exit()

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """Gère les événements de relâchement de touches.

        Args:
            key: Le code de la touche relâchée.
            key_modifiers: Modificateurs de touches bitwise actifs.
        """
        pass

    def on_mouse_motion(self, x: int, y: int, delta_x: int, delta_y: int) -> None:
        """Met à jour la position globale de la souris.

        Args:
            x: Position horizontale actuelle de la souris.
            y: Position verticale actuelle de la souris.
            delta_x: Variation de la position horizontale.
            delta_y: Variation de la position verticale.
        """
        mouse.position = (x, y)

    def on_mouse_press(self, x: int, y: int, button: int, key_modifiers: int) -> None:
        """Gère la sélection de l'interface selon les coordonnées du clic.

        Args:
            x: Coordonnée horizontale du clic.
            y: Coordonnée verticale du clic.
            button: Identifiant du bouton de la souris.
            key_modifiers: Modificateurs de touches bitwise actifs.
        """
        for index in range(len(self.texts)):
            text: Text = self.texts[index]

            if text.touched:
                if index > 3:
                    data.window.display(EditorView(self.chips[index - 4]))
                elif index == 1:
                    data.window.back()
                elif index == 2:
                    data.window.display(EditorView())

    def on_mouse_release(self, x: int, y: int, button: int, key_modifiers: int) -> None:
        """Gère les événements de relâchement de la souris.

        Args:
            x: Coordonnée horizontale du relâchement.
            y: Coordonnée verticale du relâchement.
            button: Identifiant du bouton de la souris.
            key_modifiers: Modificateurs de touches bitwise actifs.
        """
        pass