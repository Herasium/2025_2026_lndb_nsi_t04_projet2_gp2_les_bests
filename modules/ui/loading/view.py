import arcade
import data

class LoadingScreen(arcade.View):
    """
    Représente l'écran de chargement de l'application.
    Cette vue gère l'affichage initial et la transition des ressources.
    """

    def __init__(self) -> None:
        """ Initialise la vue de l'écran de chargement. """
        super().__init__()

        # Définit la couleur d'arrière-plan de la vue en noir
        self.background_color: arcade.Color = arcade.color.BLACK

    def reset(self) -> None:
        """ Réinitialise l'état de l'écran de chargement si nécessaire. """
        pass

    def on_draw(self) -> None:
        """ Gère le rendu de l'écran. """
        self.clear()

        # Affiche le texte de chargement au centre de la fenêtre
        arcade.draw_text(
            "Loading", data.WINDOW_WIDTH / 2, data.WINDOW_HEIGHT / 2, arcade.color.WHITE
        )

    def on_update(self, delta_time: float) -> None:
        """
        Logique de mise à jour de la vue.
        
        :param delta_time: Temps écoulé depuis la dernière mise à jour.
        """
        pass

    def on_key_press(self, key: int, key_modifiers: int) -> None:
        """
        Gère les entrées clavier de l'utilisateur.
        
        :param key: Touche pressée.
        :param key_modifiers: Modificateurs de touches (Shift, Ctrl, etc.).
        """
        # Quitte l'application si la touche spécifique (code 97) est pressée
        if key == 97:
            arcade.exit()

    def on_mouse_motion(self, x, y, dx, dy):
        """
        Gère les mouvements de la souris.
        
        :param x: Position X actuelle de la souris.
        :param y: Position Y actuelle de la souris.
        :param dx: Déplacement relatif sur l'axe X.
        :param dy: Déplacement relatif sur l'axe Y.
        """
        pass