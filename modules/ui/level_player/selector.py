import arcade
from typing import List, Any

from modules.ui.mouse import mouse
from modules.ui.toolbox.text import Text

from modules.data import data


from modules.ui.level_player.view import LevelPlayer


class LevelPlayerSelector(arcade.View):
    """Fournit une interface permettant aux utilisateurs de sélectionner et de lancer les niveaux du jeu."""

    def __init__(self) -> None:
        """Initialise la vue et génère l'interface utilisateur de sélection de niveau."""
        super().__init__()

        self.background_color: arcade.Color = arcade.color.BLACK
        self.texts: List[Text] = []
        self.camera: int = 0
        self.levels: List[Any] = []
        self.setup()

    def setup(self) -> None:
        """Configure la disposition de l'interface et associe les niveaux disponibles aux éléments sélectionnables."""
        debug_list: List[str] = ["Chip Editor Selector", "<- Back", ""]
        self.texts: List[Text] = []
        self.levels: List[Any] = []

        for i in data.loaded_levels:
            level = data.loaded_levels[i]
            debug_list.append(f"Level {level.number} {level.name} #{level.id}")
            self.levels.append(i)

        start_y: int = data.WINDOW_HEIGHT - 70 + self.camera
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
        """Rendu des éléments textuels et de leurs zones de collision (hitboxes) associées."""
        self.clear()

        for i in self.texts:
            i.draw()
            i.hitbox.draw()

    def on_update(self, delta_time: float) -> None:
        """
        Args:
            delta_time: Temps écoulé depuis la dernière mise à jour de l'image.
        """
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """
        Args:
            key: Identifiant entier de la touche pressée.
            key_modifiers: Masque de bits des touches de modification actives.
        """
        if key == 97:
            arcade.exit()

    def on_key_release(self, key: int, key_modifiers: int) -> None:
        """
        Args:
            key: Identifiant entier de la touche relâchée.
            key_modifiers: Masque de bits des touches de modification actives.
        """
        pass

    def on_mouse_motion(
        self, x: float, y: float, delta_x: float, delta_y: float
    ) -> None:
        """
        Args:
            x: Position horizontale actuelle de la souris.
            y: Position verticale actuelle de la souris.
            delta_x: Variation de la position horizontale.
            delta_y: Variation de la position verticale.
        """
        mouse.position = (x, y)

    def on_mouse_press(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """
        Args:
            x: Position horizontale de la souris lors du clic.
            y: Position verticale de la souris lors du clic.
            button: Identifiant du bouton de la souris pressé.
            key_modifiers: Masque de bits des touches de modification actives.
        """
        for index in range(len(self.texts)):
            text = self.texts[index]

            if text.touched:
                if index > 2:
                    data.window.display(LevelPlayer(self.levels[index - 3]))
                elif index == 1:
                    data.window.back()

    def on_mouse_release(
        self, x: float, y: float, button: int, key_modifiers: int
    ) -> None:
        """
        Args:
            x: Position horizontale de la souris.
            y: Position verticale de la souris.
            button: Identifiant du bouton de la souris relâché.
            key_modifiers: Masque de bits des touches de modification actives.
        """
        pass

    def on_mouse_scroll(
        self, x: float, y: float, scroll_x: float, scroll_y: float
    ) -> None:
        """Met à jour le décalage vertical de la caméra et reconstruit la disposition."""
        self.camera += scroll_y * -data.MOUSE_SENSI
        self.camera = max(self.camera, 0)
        self.setup()